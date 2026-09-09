import { useState } from "react";
import { api } from "../api";

type Tab = "provenance" | "cert" | "heatmap";

export default function ForensicsPanel({ text }: { text: string }) {
  const [tab, setTab] = useState<Tab>("provenance");
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const [data, setData] = useState<any>(null);
  const [busy, setBusy] = useState(false);

  async function load() {
    setBusy(true);
    try {
      if (tab === "provenance") setData(await api.provenance(text));
      else if (tab === "cert") setData(await api.cert(text));
      else setData(await api.heatmap(text));
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="card forensics-panel">
      <div className="card-head">
        <h2>Forensics</h2>
      </div>
      <div className="tabs">
        {(["provenance", "cert", "heatmap"] as Tab[]).map((t) => (
          <button
            key={t}
            className={`tab ${tab === t ? "active" : ""}`}
            onClick={() => {
              setTab(t);
              setData(null);
            }}
          >
            {t}
          </button>
        ))}
      </div>
      <button className="btn primary" onClick={load} disabled={busy || !text.trim()}>
        {busy ? "Generating…" : `Generate ${tab}`}
      </button>

      {data && tab !== "heatmap" && (
        <pre className="json-out">{JSON.stringify(data, null, 2)}</pre>
      )}
      {data && tab === "heatmap" && (
        <iframe className="heatmap-frame" srcDoc={data.html} title="heatmap" />
      )}
    </div>
  );
}
