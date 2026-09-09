import { useEffect, useRef } from "react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import Chapter from "./Chapter";
import { IconDocument, IconSeal } from "./VectorIcons";
import WaxSeal from "./WaxSeal";
gsap.registerPlugin(ScrollTrigger);

export default function Trust() {
  const ref = useRef<HTMLElement>(null);
  useEffect(() => {
    const ctx = gsap.context(() => {
      gsap.from(".trust-head > *", { y: 16, opacity: 0, duration: .6, stagger: .08, ease: "expo.out", scrollTrigger: { trigger: ref.current, start: "top 82%" } });
      gsap.from(".trust-diagram", { y: 20, opacity: 0, duration: .65, ease: "expo.out", scrollTrigger: { trigger: ".trust-diagram", start: "top 85%" } });
      gsap.from(".trust-card", { y: 18, opacity: 0, duration: .55, stagger: .08, ease: "expo.out", scrollTrigger: { trigger: ".trust-grid", start: "top 88%" } });
    }, ref);
    return () => ctx.revert();
  }, []);
  return (
    <section ref={ref} id="trust" className="trust" data-chapter="trust">
      <div className="trust-head">
        <Chapter n={7} label="The Vow" />
        <div className="kicker">Trust & privacy</div>
        <h2>Nothing leaves your browser. <em>Ever.</em></h2>
        <p>Your text stays local. The lab calls your own API: no exfiltration, no training, no retention. Open source, auditable, SHA-256 certified.</p>
      </div>

      <div className="trust-diagram">
        <div className="trust-node">
          <div className="trust-icon"><IconDocument /></div>
          <strong>Your text</strong>
          <span>paste or drop</span>
        </div>
        <div className="trust-arrow">→</div>
        <div className="trust-node accent">
          <div className="trust-icon trust-icon-seal"><WaxSeal /></div>
          <strong>Aphanis API</strong>
          <span>localhost / your Render</span>
        </div>
        <div className="trust-arrow">→</div>
        <div className="trust-node">
          <div className="trust-icon"><IconSeal /></div>
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
          <h3>SHA-256 audit trail</h3>
          <p>Every clean issues a provenance certificate: a hash of the original, the cleaned text, and the mode, verifiable offline.</p>
          <code className="mono">aphanis cert &quot;your text&quot;</code>
        </div>
        <div className="trust-card">
          <h3>Open source</h3>
          <p>Python and TypeScript. Read the 7-stage pipeline, the lexicon, the DCT pass. No black box.</p>
          <a href="https://github.com/sanyamk23/aphanis" target="_blank" rel="noreferrer" className="mono">github.com/sanyamk23/aphanis →</a>
        </div>
        <div className="trust-card">
          <h3>Runs everywhere</h3>
          <p>CLI, MCP server, Claude Code hook, GitHub Action, Cursor: same engine, any surface.</p>
          <span className="mono">pip install aphanis · npm i -g aphanis</span>
        </div>
      </div>
    </section>
  );
}
