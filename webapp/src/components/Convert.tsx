import { useRef, useState } from "react";
import { api } from "../api";
import type { AuditResponse, Mode, Tone, VerifyResponse, CleanFileResponse } from "../types";

type FilePreview = { url: string; type: string; filename: string; downloadName: string };

const MODES: Mode[] = ["paranoid", "aggressive", "standard", "minimal"];
const TONES: Tone[] = ["conversational", "casual", "tech-lead", "academic", "executive"];

const VECTOR_LABELS: Record<string, string> = {
  vector_1_unicode_steganography: "Unicode Steganography",
  vector_2_statistical_model: "Statistical Fingerprint",
  vector_3_metadata_container: "Metadata & Container",
  vector_4_spatial_frequency: "Spatial Frequency",
};

function scoreColor(s: number) {
  if (s >= 80) return "var(--emerald)";
  if (s >= 50) return "var(--amber)";
  return "var(--rose)";
}
function riskColor(s: number) {
  if (s >= 60) return "var(--rose)";
  if (s >= 25) return "var(--amber)";
  return "var(--emerald)";
}
function riskClass(l: string) {
  if (!l) return "risk-clean";
  const v = l.toLowerCase();
  if (v.includes("high") || v.includes("strong")) return "risk-high";
  if (v.includes("moderate") || v.includes("mixed")) return "risk-moderate";
  if (v.includes("low") || v.includes("invisible")) return "risk-low";
  return "risk-clean";
}
function vectorSignals(v: { issues_found?: number; telltale_phrases?: number; em_dashes?: number; ai_comments_found?: number; status: string }): string[] {
  const out: string[] = [];
  if (v.issues_found) out.push(`${v.issues_found} hidden byte${v.issues_found === 1 ? "" : "s"}`);
  if (v.telltale_phrases) out.push(`${v.telltale_phrases} cliché${v.telltale_phrases === 1 ? "" : "s"}`);
  if (v.em_dashes) out.push(`${v.em_dashes} em-dash${v.em_dashes === 1 ? "" : "es"}`);
  if (v.ai_comments_found) out.push(`${v.ai_comments_found} AI comment${v.ai_comments_found === 1 ? "" : "s"}`);
  return out.length ? out : [v.status];
}

const SAMPLE = "The results demonstrate a tapestry of findings that delve into robust evaluation. Moreover, it should be noted that the approach is crucial and comprehensive — a testament to the synergy — and it is not limited to baseline performance across benchmarks.";

export default function Convert() {
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
  const [verifyResult, setVerifyResult] = useState<VerifyResponse | null>(null);
  const [verifyBusy, setVerifyBusy] = useState(false);
  const [fileInfo, setFileInfo] = useState<string | null>(null);
  const [cleanedFile, setCleanedFile] = useState<FilePreview | null>(null);
  const [fileBusy, setFileBusy] = useState(false);
  const fileRef = useRef<HTMLInputElement>(null);

  async function runAudit() {
    if (!text.trim()) return;
    setLoading(true); setError(null);
    try { setAudit(await api.audit(text)); } catch (e) { setError((e as Error).message); } finally { setLoading(false); }
  }

  async function runClean() {
    if (!text.trim()) return;
    setCleanBusy(true);
    try {
      const r = await api.clean(text, mode, tone, perturb, humanize);
      setCleaned(r.cleaned);
      navigator.clipboard.writeText(r.cleaned);
    } catch (e) { setError((e as Error).message); } finally { setCleanBusy(false); }
  }

  async function runVerify() {
    if (!text.trim()) return;
    setVerifyBusy(true); setError(null);
    try { setVerifyResult(await api.verify(text)); } catch (e) { setError((e as Error).message); } finally { setVerifyBusy(false); }
  }

  async function handleFile(f: File) {
    const ext = f.name.split(".").pop()?.toLowerCase() ?? "";
    const isText = ["txt", "md", "py", "js", "ts", "json", "html", "svg", "csv"].includes(ext);
    if (isText) {
      const t = await f.text(); setText(t);
      setFileInfo(`Loaded ${f.name} — ${t.length} chars`);
      try { setLoading(true); setAudit(await api.audit(t)); } catch (e) { setError((e as Error).message); } finally { setLoading(false); }
    } else {
      const mimeByExt: Record<string, string> = {
        png: "image/png", jpg: "image/jpeg", jpeg: "image/jpeg", gif: "image/gif",
        pdf: "application/pdf", html: "text/html", svg: "image/svg+xml",
      };
      const mimeType = mimeByExt[ext] ?? "application/octet-stream";
      const viewable = ["png","jpg","jpeg","gif","pdf","html","svg"].includes(ext);
      setFileBusy(true); setFileInfo(null);
      try {
        const res: CleanFileResponse = await api.cleanFile(f, mode, perturb, false);
        setFileInfo(res.message);
        if (res.success && res.data_base64) {
          const blob = new Blob([Uint8Array.from(atob(res.data_base64), (c) => c.charCodeAt(0))], { type: mimeType });
          const url = URL.createObjectURL(blob);
          if (viewable) {
            setCleanedFile({ url, type: mimeType, filename: res.filename ?? f.name, downloadName: `aphanis_${res.filename ?? f.name}` });
          } else {
            const a = document.createElement("a");
            a.href = url;
            a.download = `aphanis_${res.filename ?? f.name}`;
            a.style.display = "none";
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            setCleanedFile({ url, type: mimeType, filename: res.filename ?? f.name, downloadName: a.download });
          }
        }
      } catch (e) { setFileInfo((e as Error).message); } finally { setFileBusy(false); }
    }
  }

  const rm = audit?.risk_matrix; const ent = audit?.entropy;
  const vectors = rm?.vectors ? Object.entries(rm.vectors) : [];

  return (
    <section className="convert-page">
      <div className="convert-header">
        <span className="convert-kicker">Aphanis Convert</span>
        <h2>Audit &middot; Verify &middot; Convert</h2>
        <p style={{ color: "#5E5749", marginTop: 8, fontSize: 15, lineHeight: 1.6, maxWidth: 640, margin: "8px auto 0" }}>
          Paste text or drop a file to get a full provenance report, then convert with precise control.
        </p>
      </div>

      <div className="convert-shell">
        {/* Left: input + controls + audit */}
        <div className="convert-panel">
          <div className="convert-label">Input</div>
          <div style={{ display: "flex", gap: 8, flexWrap: "wrap", marginBottom: 10 }}>
            {MODES.map((m) => (
              <button key={m} className={`mode-btn ${mode === m ? "active" : ""}`} onClick={() => setMode(m)}>{m}</button>
            ))}
            <select className="tone" value={tone} onChange={(e) => setTone(e.target.value as Tone)}>
              {TONES.map((t) => <option key={t} value={t}>{t}</option>)}
            </select>
          </div>
          <div className="toggles" style={{ marginBottom: 10 }}>
            <label><input type="checkbox" checked={perturb} onChange={(e) => setPerturb(e.target.checked)} /> Perturb AI vocabulary</label>
            <label><input type="checkbox" checked={humanize} onChange={(e) => setHumanize(e.target.checked)} /> Humanize tone</label>
          </div>
          <textarea
            className="convert-textarea"
            placeholder="Paste your text here..."
            value={text}
            onChange={(e) => setText(e.target.value)}
          />
          <div style={{ fontFamily: "var(--mono)", fontSize: 11, color: "var(--muted)", marginTop: 8 }}>{text.length} chars</div>

          <div className="row" style={{ marginTop: 12 }}>
            <button className="btn primary" onClick={runAudit} disabled={loading || !text.trim()} style={{ flex: 1 }}>
              {loading ? "Scanning…" : "🔍 Audit"}
            </button>
            <button className="btn ghost" onClick={() => { setText(""); setAudit(null); setCleaned(null); setVerifyResult(null); setError(null); }}>Clear</button>
            <button className="btn ghost" onClick={() => setText(SAMPLE)}>Load sample</button>
          </div>

          <div className="row" style={{ marginTop: 8, gap: 6 }}>
            <button className="btn ghost" onClick={runVerify} disabled={verifyBusy || !text.trim()} style={{ flex: 1 }}>
              {verifyBusy ? "Verifying…" : "◬ Verify AI"}
            </button>
          </div>

          <div className="drop" style={{ marginTop: 12 }} onDragOver={(e) => e.preventDefault()} onDrop={(e) => { e.preventDefault(); const f = e.dataTransfer.files?.[0]; if (f) handleFile(f); }} onClick={() => fileRef.current?.click()}>
            <input ref={fileRef} type="file" accept=".txt,.md,.py,.js,.ts,.json,.html,.svg,.docx,.pptx,.xlsx,.ipynb,.pdf,.png,.jpg,.jpeg,.csv" style={{ display: "none" }} onChange={(e) => { const f = e.target.files?.[0]; if (f) handleFile(f); }} />
            <div style={{ fontSize: 18 }}>📂</div>
            <div style={{ fontWeight: 700, fontSize: 13, marginTop: 4 }}>Drop a file or click to upload</div>
            <div style={{ color: "var(--muted)", fontSize: 12, marginTop: 4 }}>Text files scan inline. DOCX / PDF / PNG / IPYNB are cleaned server-side.</div>
            {fileInfo && <div className="file-name">{fileInfo}</div>}
            {fileBusy && <div className="file-status">Cleaning…</div>}
          </div>

          {cleanedFile && (
            <div className="result-box file-result-box" style={{ marginTop: 12 }}>
              <div className="file-result-header">
                <span className="file-result-name">{cleanedFile.filename}</span>
                <a href={cleanedFile.url} download={cleanedFile.downloadName} className="file-download-btn" aria-label={`Download ${cleanedFile.filename}`}>💾 Download</a>
              </div>
              {cleanedFile.type.startsWith("image/") && (
                <img src={cleanedFile.url} alt={cleanedFile.filename} className="file-preview-img" loading="lazy" />
              )}
              {(cleanedFile.type === "application/pdf" || cleanedFile.type === "text/html" || cleanedFile.type === "image/svg+xml") && (
                <iframe src={cleanedFile.url} title={cleanedFile.filename} className="file-preview-frame" />
              )}
            </div>
          )}

          {verifyResult && (
            <div style={{ marginTop: 14, padding: 14, borderRadius: 12, background: "var(--paper)", border: "1px solid var(--line)" }}>
              <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 8 }}>
                <span style={{ fontFamily: "var(--mono)", fontSize: 11, color: "var(--muted)" }}>AI likelihood score</span>
                <div style={{ flex: 1, height: 6, background: "#ECE8E2", borderRadius: 999, overflow: "hidden" }}>
                  <div style={{ width: `${verifyResult.ai_likelihood * 100}%`, height: "100%", background: `linear-gradient(90deg,var(--violet),var(--cyan))`, transition: "width .5s var(--ease)" }} />
                </div>
                <span style={{ fontFamily: "var(--mono)", fontSize: 12, fontWeight: 700 }}>{Math.round(verifyResult.ai_likelihood * 100)}%</span>
              </div>
              {verifyResult.signals.map((s, i) => (
                <div key={i} style={{ fontSize: 11, color: "#5E5749", marginBottom: 4, fontFamily: "var(--mono)" }}>• {s}</div>
              ))}
            </div>
          )}

          {error && <div className="error-box" style={{ marginTop: 12 }}>{error}</div>}
        </div>

        {/* Center: convert button */}
        <div className="convert-center">
          <button className="convert-btn btn primary" onClick={runClean} disabled={cleanBusy || !text.trim() || !audit}>
            {cleanBusy ? "Converting…" : cleaned ? "Convert again" : "✨ Convert"}
          </button>
        </div>

        {/* Right: audit report / converted output */}
        <div className="convert-panel">
          {!audit ? (
            <div className="empty" style={{ height: "100%" }}>
              <div style={{ fontSize: 22 }}>◈</div>
              <div style={{ fontWeight: 700, marginTop: 8 }}>No audit yet</div>
              <p style={{ color: "var(--muted)", fontSize: 13, marginTop: 6, lineHeight: 1.6 }}>
                Paste text on the left and hit <strong style={{ color: "var(--ink)" }}>Audit</strong> to see your full provenance report. Then hit Convert to clean & humanize.
              </p>
              <div style={{ marginTop: 12, display: "flex", gap: 8, justifyContent: "center", flexWrap: "wrap" }}>
                <span className="badge">vector_1 — unicode</span>
                <span className="badge">vector_2 — statistical</span>
                <span className="badge">vector_3 — metadata</span>
                <span className="badge">vector_4 — spatial</span>
              </div>
            </div>
          ) : cleaned ? (
            <>
              <div className="convert-label">Converted Output</div>
              <div style={{ marginBottom: 8, display: "flex", gap: 8 }}>
                <button className="btn ghost" onClick={() => navigator.clipboard.writeText(cleaned)}>Copy</button>
              </div>
              <pre style={{ whiteSpace: "pre-wrap", fontFamily: "var(--mono)", fontSize: 12.5, lineHeight: 1.6, color: "var(--ink)", maxHeight: 480, overflow: "auto", background: "var(--paper)", border: "1px solid var(--line)", borderRadius: 12, padding: 12 }}>{cleaned}</pre>
            </>
          ) : (
            <>
              <div className="convert-label">Provenance Report</div>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginTop: 8 }}>
                <h3 style={{ fontSize: 13, letterSpacing: ".06em", textTransform: "uppercase", color: "#5E5749", fontFamily: "var(--mono)" }}>Risk: {rm?.provenance_risk_level ?? "—"}</h3>
                <span className={`badge-risk ${riskClass(rm?.provenance_risk_level ?? "")}`}>{rm?.provenance_risk_level ?? "—"}</span>
              </div>

              <div className="score-row" style={{ marginTop: 16 }}>
                <svg viewBox="0 0 92 92" className="ring" role="img" aria-label={`Clean score ${Math.round(rm?.overall_clean_score ?? 0)} out of 100`}>
                  <circle cx="46" cy="46" r="36" className="ring-bg" />
                  <circle cx="46" cy="46" r="36" className="ring-fg" stroke={scoreColor(rm?.overall_clean_score ?? 0)} strokeDasharray={`${((rm?.overall_clean_score ?? 0) / 100) * 226} 226`} />
                  <text x="46" y="51" textAnchor="middle" className="ring-text" style={{ fontSize: 22 }} aria-hidden="true">{Math.round(rm?.overall_clean_score ?? 0)}</text>
                </svg>
                <div>
                  <div style={{ fontWeight: 800, letterSpacing: "-.02em" }}>Clean Score</div>
                  <div style={{ color: "var(--muted)", fontSize: 12, marginTop: 2 }}>higher = fewer detectable signals</div>
                  <div style={{ fontFamily: "var(--mono)", fontSize: 11, color: "var(--muted)", marginTop: 6 }}>{rm?.provenance_risk_level} • entropy {ent?.shannon_entropy?.toFixed(2)}</div>
                </div>
              </div>

              <div className="vector-grid" style={{ marginTop: 16 }}>
                {vectors.map(([key, v]) => (
                  <div key={key} className="vector">
                    <div className="vector-top">
                      <span className="vector-label">{VECTOR_LABELS[key] ?? key}</span>
                      <span style={{ fontWeight: 800, color: riskColor(v.risk_score) }}>{Math.round(v.risk_score)}</span>
                    </div>
                    <div className="bar2" style={{ marginTop: 8 }}><i style={{ width: `${v.risk_score}%`, background: riskColor(v.risk_score) }} /></div>
                    <ul style={{ listStyle: "none", marginTop: 8 }}>
                      {vectorSignals(v).slice(0, 3).map((s, j) => <li key={j} style={{ fontSize: 11, color: "var(--muted)", padding: "2px 0" }}>{s}</li>)}
                    </ul>
                  </div>
                ))}
              </div>

              <div className="entropy-strip" style={{ marginTop: 16 }}>
                <div><strong>{ent?.shannon_entropy?.toFixed(2)}</strong><span>Shannon</span></div>
                <div><strong>{ent?.ttr?.toFixed(2)}</strong><span>T-T-R</span></div>
                <div><strong>{ent?.predictability_score}%</strong><span>predictability</span></div>
                <div style={{ fontSize: 12 }}><strong>{ent?.ai_likelihood}</strong><span>AI likelihood</span></div>
              </div>

              <div style={{ marginTop: 16, padding: 12, borderRadius: 12, background: "var(--paper)", border: "1px solid var(--line)" }}>
                <div style={{ fontFamily: "var(--mono)", fontSize: 10, letterSpacing: ".08em", textTransform: "uppercase", color: "var(--muted)" }}>What this means</div>
                <p style={{ color: "#3A342A", fontSize: 12, lineHeight: 1.6, marginTop: 6 }}>
                  Clean score blends four vectors. Unicode catches ghosts between characters; Statistical reads vocabulary & predictability; Metadata reflects container risk; Spatial applies to images. Entropy and predictability tell you how "model-like" the rhythm feels to a detector.
                </p>
                <div style={{ marginTop: 8, display: "flex", gap: 6, flexWrap: "wrap" }}>
                  <span className="badge" style={{ fontSize: 9 }}>Tip: try paranoid → standard</span>
                  <span className="badge" style={{ fontSize: 9 }}>Toggle perturb + humanize</span>
                </div>
              </div>
            </>
          )}
        </div>
      </div>
    </section>
  );
}
