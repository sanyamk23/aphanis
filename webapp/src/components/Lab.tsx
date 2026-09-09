import { useEffect, useRef, useState } from "react";
import { api } from "../api";
import type { AuditResponse, Mode, Tone } from "../types";
import Chapter from "./Chapter";

type Tab = "provenance" | "cert" | "heatmap";

const MODES: Mode[] = ["paranoid", "aggressive", "standard", "minimal"];
const TONES: Tone[] = ["conversational", "casual", "tech-lead", "academic", "executive"];

function scoreColor(s: number) {
  if (s >= 80) return "var(--emerald)";
  if (s >= 50) return "var(--amber)";
  return "var(--rose)";
}
function riskClass(l: string) {
  if (!l) return "risk-clean";
  const v = l.toLowerCase();
  if (v.includes("high") || v.includes("strong")) return "risk-high";
  if (v.includes("moderate") || v.includes("mixed")) return "risk-moderate";
  if (v.includes("low") || v.includes("invisible")) return "risk-low";
  return "risk-clean";
}

const SAMPLE = "The results demonstrate a tapestry of findings that delve into robust evaluation. Moreover, it should be noted that the approach is crucial and comprehensive — a testament to the synergy — and it is not limited to baseline performance across benchmarks.";

export default function Lab() {
  const [text, setText] = useState(SAMPLE);
  const [mode, setMode] = useState<Mode>("paranoid");
  const [tone, setTone] = useState<Tone>("conversational");
  const [audit, setAudit] = useState<AuditResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [cleaned, setCleaned] = useState<string | null>(null);
  const [cleanBusy, setCleanBusy] = useState(false);
  const [perturb, setPerturb] = useState(false);
  const [humanize, setHumanize] = useState(true);
  const [tab, setTab] = useState<Tab>("provenance");
  const [forensics, setForensics] = useState<unknown>(null);
  const [forensicsBusy, setForensicsBusy] = useState(false);
  const [fileInfo, setFileInfo] = useState<string | null>(null);
  const [fileBusy, setFileBusy] = useState(false);
  const fileRef = useRef<HTMLInputElement>(null);

  useEffect(()=>{ if(text.trim()) runAudit(); },[]);
  async function runAudit() {
    if (!text.trim()) return;
    setLoading(true); setError(null);
    try { setAudit(await api.audit(text)); } catch (e) { setError((e as Error).message); } finally { setLoading(false); }
  }
  async function runClean() {
    if (!text.trim()) return;
    setCleanBusy(true);
    try { const r = await api.clean(text, mode, tone, perturb, humanize); setCleaned(r.cleaned); } catch (e) { setError((e as Error).message); } finally { setCleanBusy(false); }
  }
  async function runForensics() {
    if (!text.trim()) return;
    setForensicsBusy(true);
    try {
      if (tab === "provenance") setForensics(await api.provenance(text));
      else if (tab === "cert") setForensics(await api.cert(text));
      else setForensics(await api.heatmap(text));
    } catch (e) { setError((e as Error).message); } finally { setForensicsBusy(false); }
  }
  async function handleFile(f: File) {
    const ext = f.name.split(".").pop()?.toLowerCase() ?? "";
    const isText = ["txt", "md", "py", "js", "ts", "json", "html", "svg", "csv"].includes(ext);
    if (isText) {
      const t = await f.text(); setText(t);
      setFileInfo(`Loaded ${f.name} — ${t.length} chars`);
      try { setLoading(true); setAudit(await api.audit(t)); } catch (e) { setError((e as Error).message); } finally { setLoading(false); }
    } else {
      setFileBusy(true); setFileInfo(null);
      try {
        const res = await api.cleanFile(f, mode, perturb, false);
        setFileInfo(res.message);
        if (res.success && res.data_base64) {
          const blob = new Blob([Uint8Array.from(atob(res.data_base64), (c) => c.charCodeAt(0))], { type: "application/octet-stream" });
          const url = URL.createObjectURL(blob); const a = document.createElement("a"); a.href = url; a.download = `aphanis_${res.filename}`; a.click(); URL.revokeObjectURL(url);
        }
      } catch (e) { setFileInfo((e as Error).message); } finally { setFileBusy(false); }
    }
  }

  const rm = audit?.risk_matrix; const ent = audit?.entropy; const vectors = rm?.vectors ? Object.values(rm.vectors) : [];

  return (
    <section id="lab" className="lab" data-chapter="lab">
      <div className="lab-head">
        <div>
          <Chapter n={6} label="The Lab" />
          <div className="kicker">Interactive lab</div>
          <h2>Audit. Understand. Sanitize.</h2>
          <p style={{ color: "#5E5749", marginTop: 6, lineHeight: 1.6, maxWidth: 640 }}>Paste text or drop a file — get a full provenance report across four vectors, then clean it with precise control.</p>
        </div>
        <div style={{ fontFamily: "var(--mono)", fontSize: 11, color: "var(--muted)", letterSpacing: ".06em", textTransform: "uppercase" }}>Live • POST /api/audit • /api/clean • /api/clean-file</div>
      </div>

      <div className="lab-shell">
        <div className="lab-top">
          <span>◈ Aphanis Lab — paranoid by default</span>
          <span style={{ display: "flex", gap: 8, alignItems: "center" }}><span style={{ width: 8, height: 8, borderRadius: 999, background: "var(--emerald)", display: "inline-block", boxShadow: "0 0 10px var(--emerald)" }} /> API: /api/health</span>
        </div>

        <div className="lab-grid">
          {/* left */}
          <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
            <div className="panel">
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <h3>Input</h3>
                <span className="mono" style={{ fontSize: 11, color: "var(--muted)" }}>{text.length} chars</span>
              </div>
              <div className="mode-row">
                {MODES.map((m) => (
                  <button key={m} className={`mode-btn ${mode === m ? "active" : ""}`} onClick={() => setMode(m)}>{m}</button>
                ))}
                <select className="tone" value={tone} onChange={(e) => setTone(e.target.value as Tone)}>
                  {TONES.map((t) => <option key={t} value={t}>{t}</option>)}
                </select>
              </div>
              <textarea className="textarea" placeholder="Paste your text — essay, email, code, anything. We'll scan for invisible watermarks, AI vocabulary tells, and statistical fingerprints." value={text} onChange={(e) => setText(e.target.value)} />
              <div className="row">
                <button className="btn primary" onClick={runAudit} disabled={loading || !text.trim()}>{loading ? "Scanning…" : "🔍 Audit"}</button>
                <button className="btn ghost" onClick={() => { setText(""); setAudit(null); setCleaned(null); setForensics(null); setError(null); }}>Clear</button>
                <button className="btn ghost" onClick={() => setText("The results demonstrate a significant improvement over baseline. Moreover, it should be noted that the approach is crucial for future work. The dataset exhibits comprehensive coverage and robust evaluation.")}>Load sample</button>
              </div>

              <div className="drop" onDragOver={(e) => e.preventDefault()} onDrop={(e) => { e.preventDefault(); const f = e.dataTransfer.files?.[0]; if (f) handleFile(f); }} onClick={() => fileRef.current?.click()}>
                <input ref={fileRef} type="file" accept=".txt,.md,.py,.js,.ts,.json,.html,.svg,.docx,.pptx,.xlsx,.ipynb,.pdf,.png,.jpg,.jpeg,.csv" style={{ display: "none" }} onChange={(e) => { const f = e.target.files?.[0]; if (f) handleFile(f); }} />
                <div style={{ fontSize: 18 }}>📂</div>
                <div style={{ fontWeight: 700, fontSize: 13, marginTop: 4 }}>Drop a file or click to upload</div>
                <div style={{ color: "var(--muted)", fontSize: 12, marginTop: 4 }}>Text files scan inline. DOCX / PDF / PNG / IPYNB are cleaned server-side and downloaded as aphanis_*</div>
                {fileInfo && <div className="file-name">{fileInfo}</div>}
                {fileBusy && <div className="file-status">Cleaning…</div>}
              </div>
              {error && <div className="error-box">{error}</div>}
            </div>

            <div className="cardx">
              <h3>Sanitize</h3>
              <div className="toggles">
                <label><input type="checkbox" checked={perturb} onChange={(e) => setPerturb(e.target.checked)} /> Perturb AI vocabulary</label>
                <label><input type="checkbox" checked={humanize} onChange={(e) => setHumanize(e.target.checked)} /> Humanize tone</label>
              </div>
              <div className="row">
                <button className="btn primary" onClick={runClean} disabled={cleanBusy || !text.trim()}>{cleanBusy ? "Cleaning…" : "✨ Clean & Humanize"}</button>
                {cleaned && <button className="btn ghost" onClick={() => navigator.clipboard.writeText(cleaned)}>Copy</button>}
              </div>
              {cleaned && <div className="result-box"><pre>{cleaned}</pre></div>}
            </div>

            <div className="cardx">
              <h3>Forensics</h3>
              <div className="tabs">
                {(["provenance", "cert", "heatmap"] as Tab[]).map((t) => (
                  <button key={t} className={`tab ${tab === t ? "active" : ""}`} onClick={() => { setTab(t); setForensics(null); }}>{t}</button>
                ))}
              </div>
              <div className="row">
                <button className="btn primary" onClick={runForensics} disabled={forensicsBusy || !text.trim()}>{forensicsBusy ? "Generating…" : `Generate ${tab}`}</button>
              </div>
              {forensics != null && tab === "cert" && <div className="stamp" style={{ textAlign: "center", margin: "10px 0" }}><span className="badge" style={{ background: "rgba(201,58,31,.1)", borderColor: "rgba(201,58,31,.3)", color: "var(--vermilion)" }}>◈ sealed — provenance certified</span></div>}
              {forensics != null && tab !== "heatmap" && <pre className="json-out">{JSON.stringify(forensics, null, 2)}</pre>}
              {forensics != null && tab === "heatmap" && <iframe className="heatmap-frame" srcDoc={(forensics as { html: string }).html} title="heatmap" />}
            </div>
          </div>

          {/* right */}
          <div className="cards">
            {!audit ? (
              <div className="empty">
                <div style={{ fontSize: 22 }}>◈</div>
                <div style={{ fontWeight: 700, marginTop: 8 }}>No audit yet</div>
                <p style={{ color: "var(--muted)", fontSize: 13, marginTop: 6, lineHeight: 1.6 }}>Paste text on the left and hit <strong style={{ color: "var(--ink)" }}>Audit</strong> — your full provenance report appears here: clean score, four vectors, entropy, and AI likelihood.</p>
                <div style={{ marginTop: 12, display: "flex", gap: 8, justifyContent: "center", flexWrap: "wrap" }}>
                  <span className="badge">vector_1 — unicode</span>
                  <span className="badge">vector_2 — statistical</span>
                  <span className="badge">vector_3 — metadata</span>
                  <span className="badge">vector_4 — spatial</span>
                </div>
              </div>
            ) : (
              <>
                <div className="cardx">
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                    <h3>Provenance Report</h3>
                    <span className={`badge-risk ${riskClass(rm?.provenance_risk_level ?? "")}`}>{rm?.provenance_risk_level ?? "—"}</span>
                  </div>
                  <div className="score-row">
                    <svg viewBox="0 0 92 92" className="ring">
                      <circle cx="46" cy="46" r="36" className="ring-bg" />
                      <circle cx="46" cy="46" r="36" className="ring-fg" stroke={scoreColor(rm?.overall_clean_score ?? 0)} strokeDasharray={`${((rm?.overall_clean_score ?? 0) / 100) * 226} 226`} />
                      <text x="46" y="51" textAnchor="middle" className="ring-text" style={{ fontSize: 22 }}>{Math.round(rm?.overall_clean_score ?? 0)}</text>
                    </svg>
                    <div>
                      <div style={{ fontWeight: 800, letterSpacing: "-.02em" }}>Clean Score</div>
                      <div style={{ color: "var(--muted)", fontSize: 12, marginTop: 2 }}>higher = fewer detectable signals</div>
                      <div style={{ fontFamily: "var(--mono)", fontSize: 11, color: "var(--muted)", marginTop: 6 }}>{rm?.provenance_risk_level} • entropy {ent?.shannon_entropy?.toFixed(2)}</div>
                    </div>
                  </div>

                  <div className="vector-grid">
                    {vectors.map((v, i) => (
                      <div key={i} className="vector">
                        <div className="vector-top">
                          <span className="vector-label">{(v as { label: string }).label}</span>
                          <span style={{ fontWeight: 800, color: scoreColor((v as { score: number }).score) }}>{Math.round((v as { score: number }).score)}</span>
                        </div>
                        <div className="bar2" style={{ marginTop: 8 }}><i style={{ width: `${(v as { score: number }).score}%`, background: scoreColor((v as { score: number }).score) }} /></div>
                        {(v as { signals: string[] }).signals?.length > 0 && (
                          <ul style={{ listStyle: "none", marginTop: 8 }}>
                            {(v as { signals: string[] }).signals.slice(0, 3).map((s, j) => <li key={j} style={{ fontSize: 11, color: "var(--muted)", padding: "2px 0" }}>{s}</li>)}
                          </ul>
                        )}
                      </div>
                    ))}
                  </div>

                  <div className="entropy-strip">
                    <div><strong>{ent?.shannon_entropy?.toFixed(2)}</strong><span>Shannon</span></div>
                    <div><strong>{ent?.ttr?.toFixed(2)}</strong><span>T-T-R</span></div>
                    <div><strong>{ent?.predictability_score}%</strong><span>predictability</span></div>
                    <div><strong style={{ fontSize: 12 }}>{ent?.ai_likelihood}</strong><span>AI likelihood</span></div>
                  </div>
                </div>

                <div className="cardx">
                  <h3>What this means</h3>
                  <p style={{ color: "#3A342A", fontSize: 13, lineHeight: 1.6, marginTop: 8 }}>
                    Clean score blends four vectors. <strong>Unicode</strong> catches ghosts between characters; <strong>Statistical</strong> reads vocabulary & predictability; <strong>Metadata</strong> reflects container risk; <strong>Spatial</strong> applies to images. Entropy and predictability tell you how “model-like” the rhythm feels to a detector.
                  </p>
                  <div style={{ marginTop: 10, display: "flex", gap: 8, flexWrap: "wrap" }}>
                    <span className="badge">Tip: try paranoid → standard to compare</span>
                    <span className="badge">Toggle perturb + humanize</span>
                  </div>
                </div>
              </>
            )}
          </div>
        </div>
      </div>
    </section>
  );
}
