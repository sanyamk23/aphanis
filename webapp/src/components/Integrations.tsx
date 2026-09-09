const ITEMS = [
  "Claude Code", "MCP Server", "Cursor", "Windsurf", "CLI", "GitHub Action", "REST API", "Python SDK", "pre-commit hook", "VS Code", "Watcher daemon", "Clipboard",
];

import Chapter from "./Chapter";

export default function Integrations() {
  return (
    <section className="integrations" data-chapter="integrations">
      <div className="integrations-head">
        <Chapter n={8} label="Epilogue" />
        <div className="kicker">Everywhere you write</div>
        <h3>Aphanis follows your workflow.</h3>
      </div>
      <div className="integrations-marquee" aria-hidden>
        <div className="integrations-track">
          {[...ITEMS, ...ITEMS].map((t, i) => (
            <span key={i} className="integration-pill">{t}</span>
          ))}
        </div>
      </div>
      <div className="integrations-cta">
        <code className="mono">aphanis audit &quot;your draft…&quot; · aphanis clean --mode paranoid essay.docx</code>
        <span className="mono muted">pip install aphanis · npx aphanis dashboard</span>
      </div>
    </section>
  );
}
