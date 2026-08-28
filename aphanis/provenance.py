"""
Aphanis - Honest Provenance Record Generator.

This module produces a *provenance record* describing signals detected in a piece
of text or a file. It is the counterpart to ``cert.py``'s "Zero-Trust Clean
Certificate": the clean certificate asserts that signals have been hidden, while
the provenance record asserts what was actually found.

The record is signed (SHA-256 of the input + the record body) so downstream
consumers can verify it has not been modified. Verifying a tampered record
returns ``TAMPERED`` rather than crashing, so the verify path is safe to call
on records from untrusted sources.

The detector composition reuses ``aphanis.cleaner.AuditTool`` and
``aphanis.entropy.EntropyAnalyzer``. No new detection logic is added here —
this module composes existing primitives and emits a different kind of artifact.
"""

import hashlib
import json
import re
import time
import unicodedata
import uuid
from typing import Any, Dict, List

from aphanis.cleaner import UnicodeSanitizer, StatisticalPerturber, AICommentSanitizer
from aphanis.entropy import EntropyAnalyzer


VERDICT_NO_SIGNALS = "no_signals_detected"
VERDICT_INVISIBLE_UNICODE = "contains_invisible_unicode"
VERDICT_AI_COMMENTS = "contains_ai_attribution_comments"
VERDICT_AI_VOCAB = "contains_ai_vocabulary_signals"
VERDICT_MIXED = "mixed_signals"
VERDICT_STRONGLY_ATTRIBUTED = "strongly_attributed_to_ai_assistance"


class ProvenanceRecord:
    """Generates a signed provenance record describing signals detected in input."""

    def __init__(self, raw_input: str, source_name: str = "Input Text") -> None:
        if not isinstance(raw_input, str):
            raise TypeError("raw_input must be a string")

        self.raw_input = raw_input
        self.source_name = source_name
        self.record_id = f"APHANIS-PROV-{uuid.uuid4().hex[:8].upper()}"
        self.timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    def _count_unicode_categories(self, text: str) -> Dict[str, int]:
        """Count invisible / bidi / tag characters by category, using the same
        constants the sanitizer uses so the record is consistent with cleaning."""
        zero_width = 0
        bidi = 0
        tag = 0
        homoglyph_candidates = 0

        for c in text:
            code = ord(c)
            if c in UnicodeSanitizer.ZERO_WIDTH_CHARS:
                zero_width += 1
            if c in UnicodeSanitizer.BIDI_CHARS:
                bidi += 1
            if 0xE0001 <= code <= 0xE007F or 0xFE00 <= code <= 0xFE0F:
                tag += 1

        # Homoglyph candidates: characters whose Unicode name indicates a
        # non-Latin script (Cyrillic, Greek). We only count them; we do not
        # claim any specific substitution.
        for c in text:
            try:
                name = unicodedata.name(c)
            except ValueError:
                continue
            if "CYRILLIC" in name or "GREEK" in name:
                homoglyph_candidates += 1

        return {
            "zero_width": zero_width,
            "bidi_overrides": bidi,
            "tag_or_variation_selectors": tag,
            "homoglyph_candidates": homoglyph_candidates,
        }

    def _scan_ai_comments(self, text: str) -> List[str]:
        """Return matched AI-attribution comment strings (the actual matches, not counts)."""
        matches: List[str] = []
        for pattern in AICommentSanitizer.SINGLE_LINE_PATTERNS + AICommentSanitizer.MULTI_LINE_PATTERNS:
            found = re.findall(pattern, text, flags=re.IGNORECASE)
            matches.extend(found)
        return matches

    def _scan_ai_vocabulary(self, text: str) -> List[str]:
        """Return matched AI-vocabulary patterns (the actual matches, not counts)."""
        matches: List[str] = []
        for pattern in StatisticalPerturber.AI_VOCAB_SWAPS.keys():
            found = re.findall(pattern, text, flags=re.IGNORECASE)
            matches.extend(found)
        return matches

    def _classify(self, signals: Dict[str, Any]) -> str:
        """Map raw signal counts to a single human-readable verdict.

        Direct evidence (invisible Unicode, AI-attribution comments, AI
        vocabulary) counts toward the strong-evidence tally. Statistical
        entropy is treated as a soft hint that can nudge a mixed verdict
        toward strongly-attributed but never stands on its own — entropy
        heuristics are unreliable for short inputs and document vs paragraph
        length changes their calibration.
        """
        has_unicode = (
            signals["unicode"]["zero_width"] > 0
            or signals["unicode"]["bidi_overrides"] > 0
            or signals["unicode"]["tag_or_variation_selectors"] > 0
        )
        has_comments = len(signals["ai_attribution_comments"]) > 0
        has_vocab = len(signals["ai_vocabulary_signals"]) > 0
        has_soft_entropy = (
            signals["entropy"]["ai_likelihood"] == "HIGH"
        )

        strong = sum(bool(x) for x in (has_unicode, has_comments, has_vocab))

        if strong == 0:
            return VERDICT_NO_SIGNALS
        if has_unicode and not has_comments and not has_vocab:
            return VERDICT_INVISIBLE_UNICODE
        if has_comments and strong == 1:
            return VERDICT_AI_COMMENTS
        if has_vocab and strong == 1:
            return VERDICT_AI_VOCAB
        if strong >= 2:
            return VERDICT_STRONGLY_ATTRIBUTED
        if has_soft_entropy:
            return VERDICT_MIXED
        return VERDICT_MIXED

    def generate(self) -> Dict[str, Any]:
        """Build the provenance record (without the signature)."""
        text = self.raw_input

        unicode_signals = self._count_unicode_categories(text)
        ai_comments = self._scan_ai_comments(text)
        ai_vocab = self._scan_ai_vocabulary(text)
        em_dash_count = text.count("—")
        smart_quote_count = sum(text.count(c) for c in ("“", "”", "‘", "’"))
        entropy = EntropyAnalyzer.analyze(text)

        signals: Dict[str, Any] = {
            "unicode": unicode_signals,
            "ai_attribution_comments": ai_comments,
            "ai_vocabulary_signals": ai_vocab,
            "em_dashes": em_dash_count,
            "smart_quotes": smart_quote_count,
            "entropy": entropy,
        }

        verdict = self._classify(signals)

        record_body: Dict[str, Any] = {
            "record_id": self.record_id,
            "timestamp": self.timestamp,
            "issuer": "Aphanis Honest Provenance Toolkit",
            "source_name": self.source_name,
            "input_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
            "input_length_chars": len(text),
            "input_length_words": len(text.split()),
            "verdict": verdict,
            "signals": signals,
        }

        record_body["signature"] = self._sign(record_body)
        return record_body

    @staticmethod
    def _sign(record_body: Dict[str, Any]) -> str:
        """Sign a record body by hashing a canonical JSON serialization of the
        fields that are part of the verifiable payload. Excludes ``signature``
        itself to avoid self-reference."""
        payload = {k: v for k, v in record_body.items() if k != "signature"}
        canonical = json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def verify_provenance_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """Verify a provenance record's signature.

    Returns a small status dict that is safe to print or surface in a UI.
    Does not raise on tampered or malformed records.
    """
    required = {"record_id", "timestamp", "issuer", "source_name", "input_sha256", "verdict", "signals", "signature"}
    missing = [k for k in required if k not in record]
    if missing:
        return {"status": "MISSING_FIELDS", "missing": missing}

    claimed = record.get("signature", "")
    payload = {k: v for k, v in record.items() if k != "signature"}
    canonical = json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    expected = hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    if claimed != expected:
        return {"status": "TAMPERED", "record_id": record.get("record_id")}

    return {
        "status": "VALID",
        "record_id": record.get("record_id"),
        "timestamp": record.get("timestamp"),
        "verdict": record.get("verdict"),
        "issuer": record.get("issuer"),
    }


def record_to_text(record: Dict[str, Any]) -> str:
    """Render a provenance record as a human-readable plain-text report."""
    verdict = record.get("verdict", "unknown")
    verdict_lines = {
        VERDICT_NO_SIGNALS: "No AI-attribution signals detected.",
        VERDICT_INVISIBLE_UNICODE: "Contains invisible Unicode characters (likely steganography or pasted watermark).",
        VERDICT_AI_COMMENTS: "Contains AI-attribution code comments (e.g. '# Generated by Claude').",
        VERDICT_AI_VOCAB: "Contains AI-vocabulary statistical signals.",
        VERDICT_MIXED: "Mixed AI-attribution signals detected.",
        VERDICT_STRONGLY_ATTRIBUTED: "Multiple AI-attribution signals detected — content strongly appears AI-assisted.",
    }

    sig = record.get("signals", {})
    unicode = sig.get("unicode", {})
    entropy = sig.get("entropy", {})

    lines = [
        f"Provenance Record : {record.get('record_id', '?')}",
        f"Timestamp         : {record.get('timestamp', '?')}",
        f"Issuer            : {record.get('issuer', '?')}",
        f"Source            : {record.get('source_name', '?')}",
        f"Input SHA-256     : {record.get('input_sha256', '?')}",
        f"Input length      : {record.get('input_length_chars', 0)} chars / {record.get('input_length_words', 0)} words",
        f"Verdict           : {verdict}",
        f"  → {verdict_lines.get(verdict, '')}",
        "",
        "Signals",
        f"  Zero-width chars        : {unicode.get('zero_width', 0)}",
        f"  Bidi overrides          : {unicode.get('bidi_overrides', 0)}",
        f"  Tag / variation select. : {unicode.get('tag_or_variation_selectors', 0)}",
        f"  Homoglyph candidates    : {unicode.get('homoglyph_candidates', 0)}",
        f"  Em-dashes               : {sig.get('em_dashes', 0)}",
        f"  Smart quotes            : {sig.get('smart_quotes', 0)}",
        f"  AI comments             : {len(sig.get('ai_attribution_comments', []))}",
        f"  AI vocabulary matches   : {len(sig.get('ai_vocabulary_signals', []))}",
        f"  Entropy (bits/char)     : {entropy.get('shannon_entropy', 0.0)}",
        f"  AI likelihood           : {entropy.get('ai_likelihood', 'UNKNOWN')}",
        "",
        f"Signature (SHA-256): {record.get('signature', '?')}",
    ]
    return "\n".join(lines)
