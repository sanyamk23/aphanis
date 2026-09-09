import { useState } from "react";
import Hero from "./components/Hero";
import TextPanel from "./components/TextPanel";
import FileDrop from "./components/FileDrop";
import ScoreCards from "./components/ScoreCards";
import CleanPanel from "./components/CleanPanel";
import ForensicsPanel from "./components/ForensicsPanel";
import ModePicker from "./components/ModePicker";
import { api } from "./api";
import type { AuditResponse, Mode, Tone } from "./types";

export default function App() {
  const [text, setText] = useState("");
  const [mode, setMode] = useState<Mode>("paranoid");
  const [tone, setTone] = useState<Tone>("conversational");
  const [audit, setAudit] = useState<AuditResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function runAudit(input: string) {
    setLoading(true);
    setError(null);
    try {
      const res = await api.audit(input);
      setAudit(res);
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app">
      <header className="topbar">
        <div className="brand">
          <span className="brand-mark">🛡️</span>
          <span className="brand-name">Aphanis</span>
        </div>
        <ModePicker mode={mode} tone={tone} onMode={setMode} onTone={setTone} />
      </header>

      <Hero />

      <section className="workspace">
        <div className="panel-left">
          <TextPanel
            text={text}
            setText={setText}
            onAudit={() => runAudit(text)}
            loading={loading}
          />
          <FileDrop
            onTextLoaded={(t) => {
              setText(t);
              runAudit(t);
            }}
          />
          {error && <div className="error-box">{error}</div>}
        </div>

        <div className="panel-right">
          {audit ? (
            <>
              <ScoreCards audit={audit} />
              <CleanPanel text={text} mode={mode} tone={tone} />
              <ForensicsPanel text={text} />
            </>
          ) : (
            <div className="empty-state">
              <p>Drop text on the left and hit <strong>Audit</strong> to see your full provenance report.</p>
            </div>
          )}
        </div>
      </section>

      <footer className="footer">
        <span>Aphanis :: Zero-Trust AI Provenance Firewall</span>
      </footer>
    </div>
  );
}
