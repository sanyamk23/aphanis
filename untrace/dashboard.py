"""
Untrace AI - Cyber-Stealth Interactive Web Dashboard & Visualizer.
Launches a zero-dependency local web server for multi-vector provenance auditing,
stealth profile configuration, and visual diff inspection.
"""

import http.server
import socketserver
import json
import webbrowser
import urllib.parse
from typing import Dict, Any

from untrace.cleaner import clean_text, audit_text
from untrace.entropy import EntropyAnalyzer
from untrace.stealth import StegoRiskMatrix, StealthProfile, StealthMode

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>🛡️ Untrace AI :: Zero-Trust AI Provenance Firewall</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-dark: #030712;
      --card-bg: rgba(17, 24, 39, 0.7);
      --border-color: rgba(75, 85, 99, 0.4);
      --primary: #6366f1;
      --primary-hover: #4f46e5;
      --neon-cyan: #06b6d4;
      --neon-violet: #a855f7;
      --neon-emerald: #10b981;
      --neon-rose: #f43f5e;
      --text-main: #f9fafb;
      --text-muted: #9ca3af;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Inter', sans-serif;
      background: var(--bg-dark);
      color: var(--text-main);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      background-image: 
        radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.12) 0px, transparent 50%),
        radial-gradient(at 100% 100%, rgba(168, 85, 247, 0.12) 0px, transparent 50%);
    }

    header {
      background: rgba(17, 24, 39, 0.85);
      backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--border-color);
      padding: 1rem 2rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .logo {
      display: flex;
      align-items: center;
      gap: 0.75rem;
      font-size: 1.3rem;
      font-weight: 800;
      letter-spacing: -0.02em;
    }

    .badge-firewall {
      background: rgba(99, 102, 241, 0.2);
      color: #a5b4fc;
      border: 1px solid rgba(99, 102, 241, 0.5);
      padding: 0.25rem 0.75rem;
      border-radius: 9999px;
      font-size: 0.75rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }

    main {
      flex: 1;
      padding: 2rem;
      max-width: 1650px;
      width: 100%;
      margin: 0 auto;
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1.5rem;
    }

    .panel {
      background: var(--card-bg);
      backdrop-filter: blur(16px);
      border: 1px solid var(--border-color);
      border-radius: 14px;
      display: flex;
      flex-direction: column;
      overflow: hidden;
      box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5);
    }

    .panel-header {
      padding: 1rem 1.25rem;
      border-bottom: 1px solid var(--border-color);
      background: rgba(3, 7, 18, 0.6);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .panel-title {
      font-size: 0.95rem;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 0.5rem;
      color: #e5e7eb;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }

    .panel-body {
      padding: 1.25rem;
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 1rem;
    }

    textarea {
      width: 100%;
      height: 300px;
      background: #030712;
      border: 1px solid var(--border-color);
      border-radius: 10px;
      color: #f3f4f6;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.9rem;
      padding: 1rem;
      resize: vertical;
      outline: none;
      transition: border-color 0.2s;
    }

    textarea:focus {
      border-color: var(--primary);
    }

    .visual-output {
      width: 100%;
      min-height: 220px;
      background: #030712;
      border: 1px solid var(--border-color);
      border-radius: 10px;
      color: #f3f4f6;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.88rem;
      padding: 1rem;
      white-space: pre-wrap;
      word-break: break-word;
      overflow-y: auto;
    }

    .tag-zero-width {
      background: rgba(244, 63, 94, 0.25);
      color: #fda4af;
      border: 1px solid var(--neon-rose);
      padding: 0 4px;
      border-radius: 4px;
      font-weight: 600;
    }

    .tag-em-dash {
      background: rgba(245, 158, 11, 0.25);
      color: #fcd34d;
      border: 1px solid #f59e0b;
      padding: 0 4px;
      border-radius: 4px;
      font-weight: 600;
    }

    .tag-ai-cliche {
      background: rgba(168, 85, 247, 0.25);
      color: #e9d5ff;
      border: 1px solid var(--neon-violet);
      padding: 0 4px;
      border-radius: 4px;
    }

    .vectors-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 0.8rem;
    }

    .vector-card {
      background: rgba(3, 7, 18, 0.8);
      border: 1px solid var(--border-color);
      border-radius: 10px;
      padding: 0.85rem;
      text-align: center;
    }

    .vector-score {
      font-size: 1.4rem;
      font-weight: 800;
      margin-top: 0.25rem;
    }

    .vector-label {
      font-size: 0.7rem;
      color: var(--text-muted);
      text-transform: uppercase;
      font-weight: 700;
      letter-spacing: 0.05em;
    }

    .btn {
      background: var(--primary);
      color: white;
      border: none;
      padding: 0.6rem 1.2rem;
      border-radius: 8px;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.2s;
    }

    .btn:hover {
      background: var(--primary-hover);
      box-shadow: 0 0 15px rgba(99, 102, 241, 0.4);
    }

    .btn-secondary {
      background: rgba(55, 65, 81, 0.8);
      color: #f3f4f6;
    }

    .btn-secondary:hover {
      background: rgba(75, 85, 99, 0.9);
    }

    .controls {
      display: flex;
      align-items: center;
      gap: 0.75rem;
    }

    select {
      background: #111827;
      color: #f3f4f6;
      border: 1px solid var(--border-color);
      padding: 0.55rem 0.8rem;
      border-radius: 8px;
      font-weight: 600;
      outline: none;
    }

    .risk-banner {
      background: rgba(16, 185, 129, 0.15);
      border: 1px solid var(--neon-emerald);
      color: #6ee7b7;
      padding: 0.75rem 1rem;
      border-radius: 8px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-weight: 700;
      font-size: 0.9rem;
    }
  </style>
</head>
<body>
  <header>
    <div class="logo">
      <span>🛡️ UNTRACE AI</span>
      <span class="badge-firewall">Zero-Trust Firewall v1.2</span>
    </div>
    <div class="controls">
      <label style="font-size: 0.8rem; font-weight: 600; color: var(--text-muted);">STEALTH PROFILE:</label>
      <select id="modeSelect" onchange="auditLive()">
        <option value="paranoid" selected>PARANOID (Max Protection)</option>
        <option value="aggressive">AGGRESSIVE (Standard + Stats)</option>
        <option value="standard">STANDARD (Hygiene + Metadata)</option>
        <option value="minimal">MINIMAL (Zero-Width Only)</option>
      </select>
      <button class="btn btn-secondary" onclick="loadSampleText()">Sample Text</button>
      <button class="btn" onclick="sanitizeInput()">Sanitize Now</button>
    </div>
  </header>

  <main>
    <!-- Left Panel: 4-Vector Audit -->
    <div class="panel">
      <div class="panel-header">
        <div class="panel-title">🔍 4-Vector Stego Risk Matrix</div>
        <span id="riskLevelBadge" class="badge-firewall" style="background: rgba(16, 185, 129, 0.2); color: #6ee7b7;">ZERO_TRUST_CLEAN</span>
      </div>
      <div class="panel-body">
        <textarea id="inputText" placeholder="Paste text, code, or AI output here to inspect 4-Vector provenance risk..." oninput="auditLive()"></textarea>

        <div class="risk-banner" id="riskBanner">
          <span>PROVENANCE RISK LEVEL: <span id="bannerRisk">ZERO_TRUST_CLEAN</span></span>
          <span>CLEAN SCORE: <span id="bannerScore">100</span>/100</span>
        </div>

        <div class="vectors-grid">
          <div class="vector-card">
            <div class="vector-label">V1: Unicode</div>
            <div class="vector-score" id="v1Score" style="color: #6ee7b7;">0.0%</div>
          </div>
          <div class="vector-card">
            <div class="vector-label">V2: Statistical</div>
            <div class="vector-score" id="v2Score" style="color: #6ee7b7;">0.0%</div>
          </div>
          <div class="vector-card">
            <div class="vector-label">V3: Metadata</div>
            <div class="vector-score" id="v3Score" style="color: #6ee7b7;">0.0%</div>
          </div>
          <div class="vector-card">
            <div class="vector-label">V4: Spatial</div>
            <div class="vector-score" id="v4Score" style="color: #6ee7b7;">0.0%</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Right Panel: Visual Highlight & Sanitized Result -->
    <div class="panel">
      <div class="panel-header">
        <div class="panel-title">✨ Visual Diff Inspector & Stealth Result</div>
        <div style="display: flex; gap: 0.5rem;">
          <button class="btn btn-secondary" onclick="exportCertificate()" style="padding: 0.35rem 0.75rem; font-size: 0.75rem;">Export Certificate</button>
          <button class="btn btn-secondary" onclick="copyOutput()" style="padding: 0.35rem 0.75rem; font-size: 0.75rem;">Copy Clean Text</button>
        </div>
      </div>
      <div class="panel-body">
        <div class="panel-title" style="font-size: 0.8rem; color: var(--text-muted);">VISUAL PROVENANCE HIGHLIGHT:</div>
        <div class="visual-output" id="visualHighlight"></div>

        <div class="panel-title" style="font-size: 0.8rem; color: var(--text-muted); margin-top: 0.5rem;">SANITIZED & HUMANIZED STEALTH RESULT:</div>
        <textarea id="cleanOutput" readonly style="height: 150px;"></textarea>
      </div>
    </div>
  </main>

  <script>
    let lastAnalysis = null;

    async function auditLive() {
      const text = document.getElementById('inputText').value;
      const mode = document.getElementById('modeSelect').value;

      if (!text) {
        document.getElementById('visualHighlight').innerHTML = '';
        document.getElementById('cleanOutput').value = '';
        return;
      }

      const res = await fetch('/api/audit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text, mode })
      });
      const data = await res.json();
      lastAnalysis = data;

      const matrix = data.risk_matrix;
      document.getElementById('bannerScore').innerText = matrix.overall_clean_score;
      document.getElementById('bannerRisk').innerText = matrix.provenance_risk_level;

      document.getElementById('v1Score').innerText = `${matrix.vectors.vector_1_unicode_steganography.risk_score}%`;
      document.getElementById('v2Score').innerText = `${matrix.vectors.vector_2_statistical_model.risk_score}%`;
      document.getElementById('v3Score').innerText = `${matrix.vectors.vector_3_metadata_container.risk_score}%`;
      document.getElementById('v4Score').innerText = `${matrix.vectors.vector_4_spatial_frequency.risk_score}%`;

      // Render highlight
      renderHighlight(text);
      document.getElementById('cleanOutput').value = data.cleaned;
    }

    function renderHighlight(text) {
      let html = text
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/[\u200B\u200C\u200D\uFEFF\u2060\u00AD]/g, '<span class="tag-zero-width">[ZERO-WIDTH]</span>')
        .replace(/—/g, '<span class="tag-em-dash">[EM-DASH: —]</span>')
        .replace(/\b(delve|crucial|pivotal|paramount|testament|tapestry|spearhead|multifaceted)\b/gi, '<span class="tag-ai-cliche">$1</span>');
      document.getElementById('visualHighlight').innerHTML = html;
    }

    async function sanitizeInput() {
      await auditLive();
    }

    function loadSampleText() {
      const sample = `# Generated by Claude\\nDelve\\u200b into crucial\\ufeff matters — today, to showcase this testament and rich tapestry of ideas.`;
      document.getElementById('inputText').value = sample.replace(/\\\\u200b/g, '\\u200b').replace(/\\\\ufeff/g, '\\ufeff');
      auditLive();
    }

    function copyOutput() {
      const clean = document.getElementById('cleanOutput').value;
      navigator.clipboard.writeText(clean);
      alert('Clean text copied to clipboard!');
    }

    function exportCertificate() {
      if (!lastAnalysis) return;
      const cert = JSON.stringify(lastAnalysis, null, 2);
      const blob = new Blob([cert], { type: 'application/json' });
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = `untrace_ai_audit_certificate.json`;
      a.click();
    }
  </script>
</body>
</html>
"""


class DashboardRequestHandler(http.server.BaseHTTPRequestHandler):
    """HTTP Request Handler providing dashboard web UI and REST API."""

    def do_GET(self):
        if self.path in ['/', '/index.html']:
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(HTML_TEMPLATE.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path in ['/api/audit', '/api/sanitize']:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            try:
                payload = json.loads(body)
            except Exception:
                payload = {}

            text = payload.get('text', '')
            mode = payload.get('mode', 'paranoid')

            audit_res = audit_text(text)
            entropy_res = EntropyAnalyzer.analyze(text)
            risk_matrix = StegoRiskMatrix.evaluate(text)
            cleaned_text = clean_text(text, mode=mode)

            response_data = {
                "audit": audit_res,
                "entropy": entropy_res,
                "risk_matrix": risk_matrix,
                "cleaned": cleaned_text,
                "mode": mode
            }

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass


def launch_dashboard(port: int = 8080, open_browser: bool = True):
    """Launches local Untrace AI Web Dashboard server."""
    handler = DashboardRequestHandler
    try:
        with socketserver.TCPServer(("", port), handler) as httpd:
            url = f"http://localhost:{port}"
            print(f"🚀 Untrace AI Cyber-Stealth Dashboard running at {url}")
            if open_browser:
                webbrowser.open(url)
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\n🛑 Dashboard server stopped.")
    except Exception as e:
        print(f"❌ Failed to launch dashboard server on port {port}: {e}")
