import { useEffect, useRef, useState } from "react";
import gsap from "gsap";
import Companion from "./Companion";
import CountUp from "./CountUp";
import ScrambleText from "./ScrambleText";

const CHIPS = [
  { k: "invisible", label: "invisible · zero-width", color: "#F43F5E" },
  { k: "cliche", label: "cliché · delve / tapestry", color: "#4A5488" },
  { k: "emdash", label: "em-dash · — fingerprint", color: "#F59E0B" },
  { k: "wordy", label: "wordy · it should be noted", color: "#97907E" },
  { k: "contraction", label: "missing contraction", color: "#10B981" },
];

export default function HeroInk({ onPrimary, onSecondary }: { onPrimary: () => void; onSecondary: () => void }) {
  const ref = useRef<HTMLElement>(null);
  const paraRef = useRef<HTMLParagraphElement>(null);
  const [pos, setPos] = useState({ x: 50, y: 50 });
  const [active, setActive] = useState(false);

  useEffect(() => {
    const ctx = gsap.context(() => {
      const tl = gsap.timeline({ defaults: { ease: "expo.out" } });
      tl.from(".ink-kicker", { y: 14, opacity: 0, duration: .6 })
        .from(".ink-h1 .line", { y: 28, opacity: 0, duration: .7, stagger: .08 }, "-=.3")
        .from(".ink-sub", { y: 14, opacity: 0, duration: .6 }, "-=.3")
        .from(".ink-actions > *", { y: 12, opacity: 0, duration: .5, stagger: .07 }, "-=.2")
        .from(".ink-meta", { opacity: 0, duration: .5 }, "-=.2")
        .from(".ink-card", { y: 16, opacity: 0, duration: .7 }, "-=.4");
      gsap.to(".ink-float", { y: -8, duration: 2.2, yoyo: true, repeat: -1, ease: "sine.inOut" });
    }, ref);
    const t = setTimeout(() => {
      const el = paraRef.current;
      if (!el) return;
      const r = el.getBoundingClientRect();
      setPos({ x: r.width * 0.52, y: r.height * 0.5 });
      setActive(true);
      setTimeout(() => setActive(false), 900);
    }, 900);
    return () => { ctx.revert(); clearTimeout(t); };
  }, []);

  function handleMove(e: React.MouseEvent) {
    const el = paraRef.current;
    if (!el) return;
    const r = el.getBoundingClientRect();
    setPos({ x: e.clientX - r.left, y: e.clientY - r.top });
    if (!active) setActive(true);
  }

  return (
    <section ref={ref} className="ink-hero" data-chapter="hero">
      <div className="ink-hero-grid">
        <div className="ink-hero-copy">
          <div className="ink-kicker"><span className="dot" /> Chapter I · The Signature — v1.4.3</div>
          <h1 className="ink-h1">
            <span className="line">Your AI wrote</span>
            <span className="line">more than <em>words.</em></span>
            <span className="line grad"><ScrambleText text="It left a signature" delay={1.15} /></span>
            <span className="line grad"><ScrambleText text="you can't see." delay={1.35} /></span>
          </h1>
          <p className="ink-sub">
            Every model leaves forensic traces: zero-width steganography, statistical fingerprints, container metadata.
            Aphanis finds them and erases them before anyone else looks.
          </p>
          <div className="ink-actions">
            <button className="btn-pill dark" onClick={onPrimary}>Try live lab →</button>
            <button className="btn-pill ghost" onClick={onSecondary}>See the 10 exhibits</button>
          </div>
          <div className="ink-meta">
            <span><strong><CountUp to={4} /></strong> vectors</span><i>·</i>
            <span><strong><CountUp to={7} /></strong> stages</span><i>·</i>
            <span><strong>SHA-256</strong> cert</span><i>·</i>
            <span>CLI + MCP + Web</span>
          </div>
          <Companion
            onShort={() => document.getElementById("story")?.scrollIntoView({ behavior: "smooth", block: "start" })}
            onFull={() => document.getElementById("exhibits")?.scrollIntoView({ behavior: "smooth", block: "start" })}
          />
        </div>

        <div className="ink-hero-visual">
          <div className="ink-card">
            <div className="ink-card-head">
              <span className="mono">forensic sample. move cursor to reveal.</span>
              <span className="badge-live">try it</span>
            </div>

            <div
              className={`ink-reveal-wrap ${active ? "active" : ""}`}
              onMouseMove={handleMove}
              onMouseEnter={() => setActive(true)}
              onMouseLeave={() => setActive(false)}
              onTouchMove={(e) => {
                const t = e.touches[0]; if (!t || !paraRef.current) return;
                const r = paraRef.current.getBoundingClientRect();
                setPos({ x: t.clientX - r.left, y: t.clientY - r.top }); setActive(true);
              }}
            >
              <p ref={paraRef} className="ink-reveal-text">
                The results <span className="hl hl-cliche" data-tip="cliché: delve / realm">delve into a tapestry</span> of findings — moreover, it should be noted that the approach is <span className="hl hl-wordy" data-tip="wordy hedge">crucial and comprehensive</span> — robust evaluation across <span className="hl hl-emdash" data-tip="em-dash fingerprint">benchmarks — including</span> <span className="hl hl-invis" data-tip="zero-width steganography">invisible​​ markers</span> — and it <span className="hl hl-contraction" data-tip="missing contraction: it is → it's">is not limited</span> to baseline.
              </p>
              <div
                className="ink-spotlight"
                style={{
                  // @ts-ignore css var
                  "--mx": `${pos.x}px`, "--my": `${pos.y}px`,
                  opacity: active ? 1 : 0.18,
                } as React.CSSProperties}
              />
              <div className="ink-spotlight-glow" style={{ left: pos.x, top: pos.y, opacity: active ? 1 : 0 }} />
            </div>

            <div className="ink-chips">
              {CHIPS.map((c) => (
                <span key={c.k} className={`chip chip-${c.k}`}><i style={{ background: c.color }} />{c.label}</span>
              ))}
            </div>

            <div className="ink-scores">
              <div className="ink-score bad"><span>Before</span><strong><CountUp to={28} duration={1} /></strong><em>High risk</em></div>
              <div className="ink-score good"><span>After · paranoid</span><strong><CountUp to={89} duration={1.4} /></strong><em>Clean</em></div>
              <div className="ink-score-bar"><i style={{ width: "72%" }} /></div>
            </div>

            <div className="ink-float">Before <strong>28</strong> → After <strong>89</strong> · paranoid + conversational</div>
          </div>
        </div>
      </div>
    </section>
  );
}
