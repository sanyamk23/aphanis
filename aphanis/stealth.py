"""
Aphanis - Enterprise Stealth Engine & Stego Risk Matrix Module.
Provides multi-dimensional provenance risk vector scoring and configurable stealth presets:
PARANOID, AGGRESSIVE, STANDARD, MINIMAL.
"""

import enum
from typing import Dict, Any, List, Optional


class StealthMode(str, enum.Enum):
    PARANOID = "paranoid"
    AGGRESSIVE = "aggressive"
    STANDARD = "standard"
    MINIMAL = "minimal"


class StealthProfile:
    """Configures sanitization aggressiveness based on selected stealth mode."""

    def __init__(self, mode: StealthMode = StealthMode.STANDARD):
        if isinstance(mode, str):
            try:
                mode = StealthMode(mode.lower())
            except ValueError:
                mode = StealthMode.STANDARD
        self.mode = mode

    @property
    def clean_unicode(self) -> bool:
        return True

    @property
    def clean_punctuation(self) -> bool:
        return self.mode in [StealthMode.PARANOID, StealthMode.AGGRESSIVE, StealthMode.STANDARD]

    @property
    def clean_ai_comments(self) -> bool:
        return self.mode in [StealthMode.PARANOID, StealthMode.AGGRESSIVE, StealthMode.STANDARD]

    @property
    def perturb_stats(self) -> bool:
        return self.mode in [StealthMode.PARANOID, StealthMode.AGGRESSIVE]

    @property
    def disrupt_image_jitter(self) -> bool:
        return self.mode in [StealthMode.PARANOID, StealthMode.AGGRESSIVE]

    @property
    def strip_metadata(self) -> bool:
        return self.mode in [StealthMode.PARANOID, StealthMode.AGGRESSIVE, StealthMode.STANDARD]


class StegoRiskMatrix:
    """Evaluates input across 4 independent provenance risk vectors."""

    @classmethod
    def evaluate(cls, text: str, file_ext: Optional[str] = None) -> Dict[str, Any]:
        """
        Calculates a 4-Vector Risk Assessment:
        Vector 1: Unicode Steganography Risk (Zero-width chars, bidi control codes, tag chars)
        Vector 2: Statistical N-Gram Model Risk (AI cliché density, sentence length variance, entropy)
        Vector 3: Metadata & Container Risk (Comments, HTML meta tags, headers)
        Vector 4: Spatial Frequency Risk (Image pixel signatures, if image file)
        """
        if not text:
            text = ""

        # Vector 1: Unicode Steganography
        v1_count = 0
        from aphanis.cleaner import UnicodeSanitizer
        for c in text:
            code = ord(c)
            if c in UnicodeSanitizer.ZERO_WIDTH_CHARS or c in UnicodeSanitizer.BIDI_CHARS:
                v1_count += 1
            if 0xE0001 <= code <= 0xE007F or 0xFE00 <= code <= 0xFE0F:
                v1_count += 1

        v1_risk = min(100.0, round(v1_count * 25.0, 1))

        # Vector 2: Statistical N-Gram Model
        from aphanis.cleaner import StatisticalPerturber
        from aphanis.entropy import EntropyAnalyzer
        
        telltale_count = 0
        import re
        for pattern in StatisticalPerturber.AI_VOCAB_SWAPS.keys():
            telltale_count += len(re.findall(pattern, text, flags=re.IGNORECASE))

        em_dash_count = text.count('—')
        entropy_res = EntropyAnalyzer.analyze(text)
        predictability = entropy_res.get("predictability_score", 0.0)

        v2_score = (telltale_count * 15.0) + (em_dash_count * 10.0) + (predictability * 0.4)
        v2_risk = min(100.0, round(v2_score, 1))

        # Vector 3: Metadata Container
        from aphanis.cleaner import AICommentSanitizer
        comment_count = 0
        for pattern in AICommentSanitizer.SINGLE_LINE_PATTERNS + AICommentSanitizer.MULTI_LINE_PATTERNS:
            comment_count += len(re.findall(pattern, text, flags=re.IGNORECASE))

        v3_risk = min(100.0, round(comment_count * 30.0, 1))

        # Vector 4: Spatial Frequency
        if file_ext in ['.png', '.jpg', '.jpeg']:
            v4_risk = 50.0 # Potential spatial frequency watermark
        else:
            v4_risk = 0.0

        # Overall composite score & level
        avg_risk = (v1_risk * 0.35) + (v2_risk * 0.35) + (v3_risk * 0.20) + (v4_risk * 0.10)
        overall_clean_score = max(0.0, round(100.0 - avg_risk, 1))

        if avg_risk >= 70.0:
            level = "CRITICAL"
        elif avg_risk >= 40.0:
            level = "ELEVATED"
        elif avg_risk >= 15.0:
            level = "MODERATE"
        elif avg_risk > 0.0:
            level = "LOW"
        else:
            level = "ZERO_TRUST_CLEAN"

        return {
            "overall_clean_score": overall_clean_score,
            "provenance_risk_level": level,
            "vectors": {
                "vector_1_unicode_steganography": {
                    "risk_score": v1_risk,
                    "status": "CLEAN" if v1_risk == 0 else "RISK_DETECTED",
                    "issues_found": v1_count
                },
                "vector_2_statistical_model": {
                    "risk_score": v2_risk,
                    "status": "CLEAN" if v2_risk < 20 else "RISK_DETECTED",
                    "telltale_phrases": telltale_count,
                    "em_dashes": em_dash_count,
                    "predictability_score": predictability
                },
                "vector_3_metadata_container": {
                    "risk_score": v3_risk,
                    "status": "CLEAN" if v3_risk == 0 else "RISK_DETECTED",
                    "ai_comments_found": comment_count
                },
                "vector_4_spatial_frequency": {
                    "risk_score": v4_risk,
                    "status": "CLEAN" if v4_risk == 0 else "UNVERIFIED_PIXEL_DATA"
                }
            },
            "entropy": entropy_res
        }
