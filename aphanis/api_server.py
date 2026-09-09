"""
Aphanis - Full-Stack REST API Server.

Zero-dependency local HTTP server that exposes the real Aphanis engine
(cleaner, stealth, entropy, heatmap, cert, spectral, office, provenance,
rules, humanizer) as a clean REST API, and serves the built React
frontend from ``aphanis/dashboard_static/``.

Launched via ``aphanis dashboard`` / ``aphanis ui``.
"""

import base64
import http.server
import json
import mimetypes
import os
import socketserver
import tempfile
import urllib.parse
import uuid
import webbrowser
from typing import Any, Dict, Optional, Tuple

from aphanis.cleaner import clean_file, clean_text, audit_text
from aphanis.entropy import EntropyAnalyzer
from aphanis.heatmap import HeatmapRenderer
from aphanis.humanizer import HumanizerEngine
from aphanis.provenance import ProvenanceRecord, verify_provenance_record
from aphanis.cert import AuditCertificateGenerator
from aphanis.rules import RuleEngine
from aphanis.stealth import StealthMode, StegoRiskMatrix

# ---------------------------------------------------------------------------
# Static asset directory (built React app)
# ---------------------------------------------------------------------------

_STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dashboard_static")

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

VALID_MODES = {"paranoid", "aggressive", "standard", "minimal"}
VALID_TONES = {"conversational", "casual", "tech-lead", "academic", "executive"}


def _json_response(handler: http.server.BaseHTTPRequestHandler, code: int, data: Any) -> None:
    payload = json.dumps(data, ensure_ascii=False, default=str).encode("utf-8")
    handler.send_response(code)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(payload)))
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
    handler.send_header("Access-Control-Allow-Headers", "Content-Type")
    handler.end_headers()
    handler.wfile.write(payload)


def _error(handler: http.server.BaseHTTPRequestHandler, code: int, message: str) -> None:
    _json_response(handler, code, {"error": message})


def _read_json_body(handler: http.server.BaseHTTPRequestHandler) -> Dict[str, Any]:
    length = int(handler.headers.get("Content-Length", 0))
    if length <= 0:
        return {}
    raw = handler.rfile.read(length)
    try:
        return json.loads(raw.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return {}


def _resolve_mode(raw: Any) -> Optional[StealthMode]:
    m = (raw or "paranoid").lower()
    if m not in VALID_MODES:
        return None
    return StealthMode(m)


def _resolve_tone(raw: Any) -> str:
    t = (raw or "conversational").lower()
    return t if t in VALID_TONES else "conversational"


# ---------------------------------------------------------------------------
# Engine endpoint handlers
# ---------------------------------------------------------------------------

def _handle_audit(handler: http.server.BaseHTTPRequestHandler) -> None:
    body = _read_json_body(handler)
    text = body.get("text", "")
    if not isinstance(text, str):
        return _error(handler, 400, "text must be a string")
    file_ext = body.get("file_ext")
    audit_res = audit_text(text)
    entropy_res = EntropyAnalyzer.analyze(text)
    risk_matrix = StegoRiskMatrix.evaluate(text, file_ext=file_ext)
    _json_response(handler, 200, {"audit": audit_res, "entropy": entropy_res, "risk_matrix": risk_matrix})


def _handle_clean(handler: http.server.BaseHTTPRequestHandler) -> None:
    body = _read_json_body(handler)
    text = body.get("text", "")
    if not isinstance(text, str):
        return _error(handler, 400, "text must be a string")
    mode = _resolve_mode(body.get("mode"))
    if mode is None:
        return _error(handler, 400, f"invalid mode; choose from {sorted(VALID_MODES)}")
    tone = _resolve_tone(body.get("tone"))
    perturb = bool(body.get("perturb", False))
    humanize = bool(body.get("humanize", True))
    rules_path = body.get("rules")
    rules_engine = None
    if rules_path:
        try:
            rules_engine = RuleEngine.from_file(rules_path)
        except FileNotFoundError as e:
            return _error(handler, 400, str(e))
    cleaned = clean_text(
        text,
        perturb_stats=perturb,
        rules_engine=rules_engine,
        mode=mode.value,
        humanize=humanize,
        tone=tone,
    )
    _json_response(handler, 200, {"cleaned": cleaned, "mode": mode.value, "tone": tone})


def _handle_humanize(handler: http.server.BaseHTTPRequestHandler) -> None:
    body = _read_json_body(handler)
    text = body.get("text", "")
    if not isinstance(text, str):
        return _error(handler, 400, "text must be a string")
    tone = _resolve_tone(body.get("tone"))
    humanized = HumanizerEngine.humanize(text, tone=tone)
    _json_response(handler, 200, {"humanized": humanized, "tone": tone})


def _handle_scrub(handler: http.server.BaseHTTPRequestHandler) -> None:
    body = _read_json_body(handler)
    text = body.get("text", "")
    if not isinstance(text, str):
        return _error(handler, 400, "text must be a string")
    cleaned = clean_text(text, perturb_stats=False, clean_ai_comments=True, mode=None, humanize=False)
    _json_response(handler, 200, {"cleaned": cleaned})


def _handle_matrix(handler: http.server.BaseHTTPRequestHandler) -> None:
    body = _read_json_body(handler)
    text = body.get("text", "")
    if not isinstance(text, str):
        return _error(handler, 400, "text must be a string")
    file_ext = body.get("file_ext")
    matrix = StegoRiskMatrix.evaluate(text, file_ext=file_ext)
    _json_response(handler, 200, matrix)


def _handle_entropy(handler: http.server.BaseHTTPRequestHandler) -> None:
    body = _read_json_body(handler)
    text = body.get("text", "")
    if not isinstance(text, str):
        return _error(handler, 400, "text must be a string")
    res = EntropyAnalyzer.analyze(text)
    _json_response(handler, 200, res)


def _handle_provenance(handler: http.server.BaseHTTPRequestHandler) -> None:
    body = _read_json_body(handler)
    text = body.get("text", "")
    if not isinstance(text, str):
        return _error(handler, 400, "text must be a string")
    source = body.get("source", "inline text")
    record = ProvenanceRecord(text, source_name=source).generate()
    _json_response(handler, 200, record)


def _handle_cert(handler: http.server.BaseHTTPRequestHandler) -> None:
    body = _read_json_body(handler)
    text = body.get("text", "")
    if not isinstance(text, str):
        return _error(handler, 400, "text must be a string")
    source = body.get("source", "inline text")
    cleaned = clean_text(text)
    cert_data = AuditCertificateGenerator.generate_certificate(text, cleaned, source_name=source)
    _json_response(handler, 200, cert_data)


def _handle_heatmap(handler: http.server.BaseHTTPRequestHandler) -> None:
    body = _read_json_body(handler)
    text = body.get("text", "")
    if not isinstance(text, str):
        return _error(handler, 400, "text must be a string")
    title = body.get("title", "Aphanis Forensics Heatmap")
    html = HeatmapRenderer.render_html_heatmap(text, title=title)
    _json_response(handler, 200, {"html": html})


def _handle_clean_file(handler: http.server.BaseHTTPRequestHandler) -> None:
    """Multipart file upload -> clean_file -> stream cleaned bytes back."""
    content_type = handler.headers.get("Content-Type", "")
    if not content_type.startswith("multipart/form-data"):
        return _error(handler, 400, "expected multipart/form-data upload")

    # Parse boundary
    boundary = ""
    for part in content_type.split(";"):
        part = part.strip()
        if part.startswith("boundary="):
            boundary = part.split("=", 1)[1].strip('"')
    if not boundary:
        return _error(handler, 400, "missing multipart boundary")

    length = int(handler.headers.get("Content-Length", 0))
    if length <= 0:
        return _error(handler, 400, "empty upload body")
    raw = handler.rfile.read(length)

    # Minimal multipart parser (single file field + optional mode/perturb)
    sep = ("--" + boundary).encode()
    chunks = raw.split(sep)
    file_bytes = None
    filename = "upload.bin"
    mode = "paranoid"
    perturb = False
    jitter = False

    for chunk in chunks:
        chunk = chunk.strip(b"\r\n")
        if not chunk or chunk == b"--":
            continue
        if b"\r\n\r\n" not in chunk:
            continue
        head, data = chunk.split(b"\r\n\r\n", 1)
        head_str = head.decode("utf-8", errors="ignore")
        if "filename=" in head_str:
            # extract filename
            for token in head_str.split(";"):
                token = token.strip()
                if token.startswith("filename="):
                    filename = token.split("=", 1)[1].strip('"').split("/")[-1] or "upload.bin"
            file_bytes = data.rstrip(b"\r\n")
        elif 'name="mode"' in head_str:
            mode = data.rstrip(b"\r\n").decode("utf-8", errors="ignore").lower()
        elif 'name="perturb"' in head_str:
            perturb = data.rstrip(b"\r\n").decode("utf-8", errors="ignore").lower() in ("true", "1", "on")
        elif 'name="jitter"' in head_str:
            jitter = data.rstrip(b"\r\n").decode("utf-8", errors="ignore").lower() in ("true", "1", "on")

    if file_bytes is None:
        return _error(handler, 400, "no file field in upload")

    if mode not in VALID_MODES:
        mode = "paranoid"

    # Write to temp, clean, read back
    suffix = os.path.splitext(filename)[1] or ".bin"
    fd, tmp_path = tempfile.mkstemp(prefix="aphanis_upload_", suffix=suffix)
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(file_bytes)
        success, msg = clean_file(
            tmp_path,
            disrupt_image_pixels=jitter,
            perturb_stats=perturb,
            mode=mode,
            humanize=True,
        )
        if not success:
            return _json_response(handler, 200, {"success": False, "message": msg})

        with open(tmp_path, "rb") as f:
            cleaned_bytes = f.read()

        b64 = base64.b64encode(cleaned_bytes).decode("ascii")
        _json_response(handler, 200, {
            "success": True,
            "message": msg,
            "filename": filename,
            "size": len(cleaned_bytes),
            "data_base64": b64,
        })
    finally:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass


def _handle_health(handler: http.server.BaseHTTPRequestHandler) -> None:
    _json_response(handler, 200, {"status": "ok", "service": "aphanis-api"})


_AI_TRANSITION_WORDS = {
    "moreover", "furthermore", "additionally", "additionally", "likewise",
    "notably", "significantly", "subsequently", "consequently", "therefore",
    "thus", "hence", "nevertheless", "nonetheless", "rather", "meanwhile",
    "furthermore", "in addition", "in conclusion", "to conclude",
    "that said", "having said that", "it is important to note",
    "it should be noted", "it is worth noting", "it is clear that",
    "it is evident that", "it is obvious that", "this demonstrates",
    "this illustrates", "this suggests", "this indicates", "this suggests",
    "in today's landscape", "in today's era", "in today's world",
    "in this landscape", "in this era", "in this world",
    "leverage", "utilize", "facilitate", "demonstrate", "exemplify",
    "delve", "tapestry", "robust", "comprehensive", "paradigm",
    "synergy", "holistic", "at the end of the day", "going forward",
    "it is crucial to note", "it is important to",
}


def _handle_verify(handler: http.server.BaseHTTPRequestHandler) -> None:
    """Local-only AI detection heuristic — no external APIs consumed."""
    content_length = int(handler.headers.get("Content-Length", 0))
    raw = handler.rfile.read(content_length) if content_length else b"{}"
    try:
        payload = json.loads(raw) if raw else {}
    except json.JSONDecodeError:
        return _error(handler, 400, "invalid JSON")
    text = payload.get("text", "")
    if not isinstance(text, str) or not text.strip():
        return _error(handler, 400, "text must be a non-empty string")

    words = text.split()
    sentences = []
    for chunk in text.replace("\n", " ").replace("?", ".").replace("!", ".").split("."):
        chunk = chunk.strip()
        if len(chunk.split()) >= 3:
            sentences.append(chunk)

    result: Dict[str, Any] = {"ai_likelihood": 0.0, "signals": [], "breakdown": {}}

    # 1. Sentence length consistency (AI tends toward uniform lengths)
    if sentences:
        lengths = [len(s.split()) for s in sentences]
        avg_len = sum(lengths) / len(lengths)
        if lengths:
            variance = sum((l - avg_len) ** 2 for l in lengths) / len(lengths)
            std_dev = variance ** 0.5
            cv = std_dev / avg_len if avg_len > 0 else 0
            length_score = min(1.0, max(0.0, 1.0 - cv))
            result["signals"].append(f"Sentence length consistency: {length_score:.0%}")
            result["breakdown"]["sentence_length_score"] = round(length_score, 4)
            result["ai_likelihood"] += length_score * 0.30

    # 2. Vocabulary diversity (TTR — AI tends to have lower diversity)
    if words:
        unique = len(set(w.lower().strip(".,;:!?()[]{}\"'") for w in words))
        ttr = unique / len(words) if words else 0
        ttr_score = min(1.0, max(0.0, 1.0 - ttr))
        result["signals"].append(f"Vocabulary diversity (TTR): {ttr:.0%}")
        result["breakdown"]["vocabulary_diversity_ttr"] = round(ttr, 4)
        result["breakdown"]["vocabulary_score"] = round(ttr_score, 4)
        result["ai_likelihood"] += ttr_score * 0.30

    # 3. AI transition word frequency
    lower = text.lower()
    found = [w for w in _AI_TRANSITION_WORDS if w in lower]
    if words:
        freq = len(found) / len(words)
        trans_score = min(1.0, freq * 20)
        result["signals"].append(f"AI transition words found: {len(found)} ({found[:5]}{'...' if len(found) > 5 else ''})")
        result["breakdown"]["transition_words_found"] = len(found)
        result["breakdown"]["transition_word_freq"] = round(freq, 6)
        result["breakdown"]["transition_score"] = round(trans_score, 4)
        result["ai_likelihood"] += trans_score * 0.25

    # 4. Predictability / cliché phrases
    cliches = [w for w in found if w in ("tapestry", "delve", "robust", "comprehensive", "paradigm", "synergy", "holistic")]
    if words and cliches:
        clich_score = min(0.5, len(cliches) / len(words) * 50)
        result["signals"].append(f"Cliché / predictable phrasing: {len(cliches)} ({list(set(cliches))})")
        result["breakdown"]["cliche_count"] = len(cliches)
        result["breakdown"]["cliche_score"] = round(clich_score, 4)
        result["ai_likelihood"] += clich_score * 0.15

    result["ai_likelihood"] = round(min(1.0, result["ai_likelihood"]), 4)
    _json_response(handler, 200, result)


# ---------------------------------------------------------------------------
# Static file serving (built React SPA)
# ---------------------------------------------------------------------------

def _serve_static(handler: http.server.BaseHTTPRequestHandler) -> None:
    """Serve files from _STATIC_DIR, falling back to index.html for SPA routes."""
    rel = urllib.parse.urlparse(handler.path).path.lstrip("/")
    if rel == "" or rel == "index.html":
        rel = "index.html"

    # Resolve safely within _STATIC_DIR
    candidate = os.path.normpath(os.path.join(_STATIC_DIR, rel))
    if not candidate.startswith(_STATIC_DIR):
        return _error(handler, 403, "forbidden")

    if os.path.isfile(candidate):
        ctype, _ = mimetypes.guess_type(candidate)
        ctype = ctype or "application/octet-stream"
        with open(candidate, "rb") as f:
            data = f.read()
        handler.send_response(200)
        handler.send_header("Content-Type", ctype)
        handler.send_header("Content-Length", str(len(data)))
        handler.send_header("Cache-Control", "no-cache")
        handler.end_headers()
        handler.wfile.write(data)
    else:
        # SPA fallback: serve index.html for client-side routing
        index_path = os.path.join(_STATIC_DIR, "index.html")
        if os.path.isfile(index_path):
            with open(index_path, "rb") as f:
                data = f.read()
            handler.send_response(200)
            handler.send_header("Content-Type", "text/html; charset=utf-8")
            handler.send_header("Content-Length", str(len(data)))
            handler.end_headers()
            handler.wfile.write(data)
        else:
            _error(handler, 404, "frontend not built — run `npm run build` in webapp/")


# ---------------------------------------------------------------------------
# Request handler
# ---------------------------------------------------------------------------

class APIRequestHandler(http.server.BaseHTTPRequestHandler):
    """REST API + static frontend handler."""

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_HEAD(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path in ("/", "/index.html") or not parsed.path.startswith("/api/"):
            candidate = os.path.normpath(os.path.join(_STATIC_DIR, parsed.path.lstrip("/") or "index.html"))
            if not candidate.startswith(_STATIC_DIR):
                self.send_response(403); self.end_headers(); return
            if os.path.isfile(candidate):
                ctype, _ = mimetypes.guess_type(candidate)
                self.send_response(200)
                self.send_header("Content-Type", ctype or "application/octet-stream")
                self.send_header("Content-Length", str(os.path.getsize(candidate)))
                self.send_header("Cache-Control", "no-cache")
                self.end_headers()
            else:
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                index_path = os.path.join(_STATIC_DIR, "index.html")
                if os.path.isfile(index_path):
                    self.send_header("Content-Length", str(os.path.getsize(index_path)))
                self.end_headers()
        elif parsed.path == "/api/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
        else:
            self.send_response(404)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

    def do_GET(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path in ("/", "/index.html") or not parsed.path.startswith("/api/"):
            _serve_static(self)
        elif parsed.path in ("/api/health", "/api/verify"):
            if parsed.path == "/api/health":
                _handle_health(self)
            else:
                _handle_verify(self)
        else:
            _error(self, 404, "not found")

    def do_POST(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        route = parsed.path
        handlers = {
            "/api/audit": _handle_audit,
            "/api/clean": _handle_clean,
            "/api/humanize": _handle_humanize,
            "/api/scrub": _handle_scrub,
            "/api/matrix": _handle_matrix,
            "/api/entropy": _handle_entropy,
            "/api/provenance": _handle_provenance,
            "/api/cert": _handle_cert,
            "/api/heatmap": _handle_heatmap,
            "/api/clean-file": _handle_clean_file,
            "/api/verify": _handle_verify,
        }
        fn = handlers.get(route)
        if fn:
            try:
                fn(self)
            except Exception as e:
                _error(self, 500, f"internal error: {e}")
        else:
            _error(self, 404, "not found")

    def log_message(self, format, *args) -> None:
        pass


# ---------------------------------------------------------------------------
# Server entry point
# ---------------------------------------------------------------------------

class _ThreadingHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


def launch_dashboard(port: int = 8080, open_browser: bool = True) -> None:
    """Launch the Aphanis full-stack dashboard server.

    Render (and other PaaS) set the ``PORT`` env var and require binding
    ``0.0.0.0``.  When ``PORT`` is present we honour it and bind all
    interfaces; the browser is never opened in a headless environment.
    """
    env_port = os.environ.get("PORT")
    if env_port:
        try:
            port = int(env_port)
        except ValueError:
            pass
    bind_host = "0.0.0.0" if env_port else ""
    server = _ThreadingHTTPServer((bind_host, port), APIRequestHandler)
    url = f"http://localhost:{port}"
    print(f"🚀 Aphanis full-stack dashboard running at {url}")
    print(f"   REST API:  {url}/api/*")
    print(f"   Frontend:  {url}/")
    if open_browser and not env_port:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Aphanis dashboard server stopped.")


if __name__ == "__main__":
    launch_dashboard()
