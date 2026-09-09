import { useEffect, useRef } from "react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import Chapter from "./Chapter";
import { IconStrip, IconNormalize, IconSwap, IconWave, IconVoice, IconTag, IconSeal } from "./VectorIcons";
gsap.registerPlugin(ScrollTrigger);

const STEPS = [
  { n: "01", t: "Strip", d: "Remove zero-width, NBSP, homoglyphs.", Icon: IconStrip },
  { n: "02", t: "Normalize", d: "Collapse whitespace, quotes, dashes.", Icon: IconNormalize },
  { n: "03", t: "De-lex", d: "Swap AI vocab for human terms.", Icon: IconSwap },
  { n: "04", t: "Reshape", d: "Break predictable n-grams & burst.", Icon: IconWave },
  { n: "05", t: "Humanize", d: "Rewrite cadence in chosen voice.", Icon: IconVoice },
  { n: "06", t: "Metadata", d: "Scrub DOCX/PDF/IPYNB traces.", Icon: IconTag },
  { n: "07", t: "Certify", d: "Issue SHA-256 provenance record.", Icon: IconSeal },
];

export default function Pipeline() {
  const ref = useRef<HTMLElement>(null);
  useEffect(() => {
    const ctx = gsap.context(() => {
      gsap.from(".layers-head > *", { y: 16, opacity: 0, duration: .6, stagger: .08, ease: "expo.out", scrollTrigger: { trigger: ".layers", start: "top 82%" } });
      gsap.from(".step", { y: 18, opacity: 0, duration: .55, stagger: .06, ease: "expo.out", scrollTrigger: { trigger: ".steps", start: "top 82%" } });
    }, ref);
    return () => ctx.revert();
  }, []);
  return (
    <section ref={ref} id="pipeline" className="layers" data-chapter="pipeline">
      <div className="layers-head">
        <div>
          <Chapter n={5} label="The Pipeline" />
          <div className="kicker">How Aphanis works</div>
          <h2>A 7-layer sanitization pipeline.</h2>
          <p style={{ color: "#5E5749", marginTop: 8, maxWidth: 640, lineHeight: 1.6 }}>Audit → understand → sanitize with control. Each layer is measurable, reversible, and explained. No black-box paraphrasing.</p>
        </div>
        <div style={{ fontFamily: "var(--mono)", fontSize: 11, color: "var(--muted)", letterSpacing: ".06em", textTransform: "uppercase" }}>Paranoid → Minimal • choose your trade-off</div>
      </div>
      <div className="steps">
        {STEPS.map((s) => (
          <div key={s.n} className="step">
            <div className="step-top">
              <div className="step-num">{s.n}</div>
              <div className="step-icon"><s.Icon /></div>
            </div>
            <h4>{s.t}</h4>
            <p>{s.d}</p>
          </div>
        ))}
      </div>
      <div style={{ marginTop: 12, display: "flex", gap: 8, flexWrap: "wrap" }}>
        <span className="badge">Mode: paranoid • aggressive • standard • minimal</span>
        <span className="badge">Tone: conversational • tech-lead • academic • executive • casual</span>
        <span className="badge">Perturb + Humanize toggles</span>
      </div>
    </section>
  );
}
