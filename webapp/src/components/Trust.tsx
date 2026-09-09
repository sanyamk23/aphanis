import Chapter from "./Chapter";

export default function Trust() {
  return (
    <section id="trust" className="trust">
      <div className="trust-head">
        <Chapter n={7} label="The Vow" />
        <div className="kicker">Trust & privacy</div>
        <h2>Nothing leaves your browser. <em>Ever.</em></h2>
        <p>Your text stays local — the lab calls your own API. No exfiltration, no training, no retention. Open source, auditable, SHA-256 certified.</p>
      </div>

      <div className="trust-diagram">
        <div className="trust-node">
          <div className="trust-icon">◐</div>
          <strong>Your text</strong>
          <span>paste or drop</span>
        </div>
        <div className="trust-arrow">→</div>
        <div className="trust-node accent">
          <div className="trust-icon">◈</div>
          <strong>Aphanis API</strong>
          <span>localhost / your Render</span>
        </div>
        <div className="trust-arrow">→</div>
        <div className="trust-node">
          <div className="trust-icon">⬡</div>
          <strong>SHA-256 cert</strong>
          <span>APHANIS-CERT-2026-…</span>
        </div>
        <div className="trust-cross">
          <span>✕ No third party</span>
          <span>✕ No storage</span>
          <span>✕ No training</span>
        </div>
      </div>

      <div className="trust-grid">
        <div className="trust-card">
          <h4>SHA-256 audit trail</h4>
          <p>Every clean issues a provenance certificate — hash of original + cleaned + mode, verifiable offline.</p>
          <code className="mono">aphanis cert &quot;your text&quot;</code>
        </div>
        <div className="trust-card">
          <h4>Open source</h4>
          <p>Python + TypeScript. Read the 7-stage pipeline, the lexicon, the DCT pass. No black box.</p>
          <a href="https://github.com/sanyamk23/aphanis" target="_blank" rel="noreferrer" className="mono">github.com/sanyamk23/aphanis →</a>
        </div>
        <div className="trust-card">
          <h4>Runs everywhere</h4>
          <p>CLI, MCP server, Claude Code hook, GitHub Action, Cursor — same engine, any surface.</p>
          <span className="mono">pip install aphanis · npm i -g aphanis</span>
        </div>
      </div>
    </section>
  );
}
