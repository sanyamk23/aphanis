import { useRef } from "react";

export default function TextPanel({
  text,
  setText,
  onAudit,
  loading,
}: {
  text: string;
  setText: (t: string) => void;
  onAudit: () => void;
  loading: boolean;
}) {
  const ref = useRef<HTMLTextAreaElement>(null);

  return (
    <div className="card text-panel">
      <div className="card-head">
        <h2>Input</h2>
        <span className="count">{text.length} chars</span>
      </div>
      <textarea
        ref={ref}
        className="text-input"
        placeholder="Paste your text here — an essay, email, code, anything. We'll scan it for invisible watermarks, AI vocabulary markers, and statistical fingerprints."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />
      <div className="row">
        <button className="btn primary" onClick={onAudit} disabled={loading || !text.trim()}>
          {loading ? "Scanning…" : "🔍 Audit"}
        </button>
        <button className="btn ghost" onClick={() => setText("")}>
          Clear
        </button>
      </div>
    </div>
  );
}
