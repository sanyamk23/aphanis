import { useState } from "react";
import { api } from "../api";

export default function Convert() {
  const [input, setInput] = useState("");
  const [output, setOutput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleConvert = async () => {
    if (!input.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const res = await api.clean(input, "paranoid", "conversational", true, true);
      setOutput(res.cleaned);
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="convert-page">
      <div className="convert-header">
        <span className="convert-kicker">◬ Text Sanitizer &amp; Humanizer</span>
        <h2>Convert</h2>
      </div>

      <div className="convert-shell">
        <div className="convert-panel">
          <div className="convert-label">Input</div>
          <textarea
            className="convert-textarea"
            placeholder="Paste content to convert…"
            value={input}
            onChange={(e) => setInput(e.target.value)}
          />
        </div>

        <div className="convert-center">
          <button
            className="btn primary convert-btn"
            onClick={handleConvert}
            disabled={loading || !input.trim()}
          >
            {loading ? "Converting…" : "Convert"}
          </button>
        </div>

        <div className="convert-panel">
          <div className="convert-label">Output</div>
          <textarea
            className="convert-textarea"
            placeholder="Converted content will appear here…"
            value={output}
            onChange={(e) => setOutput(e.target.value)}
            readOnly
          />
          {error && <div className="convert-error">{error}</div>}
        </div>
      </div>
    </div>
  );
}
