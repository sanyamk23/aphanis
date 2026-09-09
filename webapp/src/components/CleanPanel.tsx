import { useState } from "react";
import { api } from "../api";
import type { Mode, Tone } from "../types";

export default function CleanPanel({
  text,
  mode,
  tone,
}: {
  text: string;
  mode: Mode;
  tone: Tone;
}) {
  const [result, setResult] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const [perturb, setPerturb] = useState(false);
  const [humanize, setHumanize] = useState(true);

  async function runClean() {
    setBusy(true);
    try {
      const res = await api.clean(text, mode, tone, perturb, humanize);
      setResult(res.cleaned);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="card clean-panel">
      <div className="card-head">
        <h2>Sanitize</h2>
      </div>
      <div className="toggles">
        <label>
          <input type="checkbox" checked={perturb} onChange={(e) => setPerturb(e.target.checked)} />
          Perturb AI vocabulary
        </label>
        <label>
          <input type="checkbox" checked={humanize} onChange={(e) => setHumanize(e.target.checked)} />
          Humanize tone
        </label>
      </div>
      <button className="btn primary" onClick={runClean} disabled={busy || !text.trim()}>
        {busy ? "Cleaning…" : "✨ Clean & Humanize"}
      </button>
      {result && (
        <div className="result-box">
          <pre>{result}</pre>
          <button
            className="btn ghost small"
            onClick={() => navigator.clipboard.writeText(result)}
          >
            Copy
          </button>
        </div>
      )}
    </div>
  );
}
