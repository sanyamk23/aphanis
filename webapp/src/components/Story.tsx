import { useEffect, useRef } from "react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import Chapter from "./Chapter";
gsap.registerPlugin(ScrollTrigger);

export default function Story() {
  const ref = useRef<HTMLElement>(null);
  useEffect(() => {
    const ctx = gsap.context(() => {
      gsap.from(".story-copy > *", { y: 18, opacity: 0, duration: .6, stagger: .08, ease: "expo.out", scrollTrigger: { trigger: ".story-copy", start: "top 82%" } });
      gsap.from(".reveal", { y: 24, opacity: 0, duration: .7, ease: "expo.out", scrollTrigger: { trigger: ".reveal", start: "top 82%" } });
      gsap.from(".point", { y: 14, opacity: 0, duration: .5, stagger: .08, ease: "expo.out", scrollTrigger: { trigger: ".story-points", start: "top 85%" } });
    }, ref);
    return () => ctx.revert();
  }, []);
  return (
    <section ref={ref} id="story" className="story" data-chapter="story">
      <div className="story-copy">
        <Chapter n={2} label="The Tell" />
        <div className="kicker">The invisible problem</div>
        <h2>AI doesn&apos;t just write.<br /><em>It leaves a trace.</em></h2>
        <p>Detectors don&apos;t read meaning. They read <em>micro-signals</em>. Zero-width characters tucked between letters. Words LLMs overuse. Predictable cadence. Hidden metadata in files. Even a human essay can trigger a false positive.</p>
        <p>If you publish, submit, or archive anything that ever touched AI, you need a firewall, not a filter.</p>
        <div className="story-points">
          <div className="point"><b>1</b><div><strong>False positives ruin reputations</strong><div style={{ color: "#5E5749", fontSize: 13, marginTop: 4, lineHeight: 1.5 }}>Students, researchers, and teams get flagged for writing that is genuinely theirs.</div></div></div>
          <div className="point"><b>2</b><div><strong>Detectors keep getting sharper</strong><div style={{ color: "#5E5749", fontSize: 13, marginTop: 4, lineHeight: 1.5 }}>Unicode, statistical, metadata, and spatial models, each watching a different fingerprint.</div></div></div>
          <div className="point"><b>3</b><div><strong>Aphanis makes the invisible visible</strong><div style={{ color: "#5E5749", fontSize: 13, marginTop: 4, lineHeight: 1.5 }}>Audit first, understand the signals, then sanitize with control. Not blind paraphrasing.</div></div></div>
        </div>
      </div>
      <div className="reveal">
        <div className="reveal-grid" />
        <div style={{ position: "relative", display: "grid", gap: 12 }}>
          <div className="reveal-card">
            <h3>Raw input — what detectors see</h3>
            <div style={{ marginTop: 10, fontFamily: "var(--mono)", fontSize: 12.5, lineHeight: 1.7, color: "#D9D2BE" }}>
              The study <span className="invis" data-label="zero-width">​</span> investigates the
              <span className="invis" data-label="AI vocab"> comprehensive</span> impact of
              <span className="invis" data-label="non-breaking space"> </span>large language models
              on academic writing<span className="invis" data-label="zero-width">‌</span>.
            </div>
            <div className="divider" style={{ background: "rgba(255,255,255,.08)", marginTop: 12 }} />
            <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
              <span className="badge" style={{ background: "rgba(244,63,94,.14)", color: "#FFD1D9", borderColor: "rgba(244,63,94,.3)" }}>3 invisible chars</span>
              <span className="badge" style={{ background: "rgba(245,158,11,.14)", color: "#FFE9B3", borderColor: "rgba(245,158,11,.28)" }}>AI vocab ×2</span>
            </div>
          </div>
          <div className="reveal-card">
            <h3>After Aphanis — paranoid mode</h3>
            <div style={{ marginTop: 10, fontFamily: "var(--mono)", fontSize: 12.5, lineHeight: 1.7, color: "#D9D2BE" }}>
              The study looks at how large language models are reshaping academic writing: where they help, where they fail, and what that means for evaluation.
            </div>
            <div className="divider" style={{ background: "rgba(255,255,255,.08)", marginTop: 12 }} />
            <div style={{ display: "flex", gap: 8, flexWrap: "wrap", alignItems: "center" }}>
              <span className="badge" style={{ background: "rgba(16,185,129,.14)", color: "#B7F7E0", borderColor: "rgba(16,185,129,.28)" }}>No invisible chars</span>
              <span className="badge" style={{ background: "rgba(16,185,129,.14)", color: "#B7F7E0", borderColor: "rgba(16,185,129,.28)" }}>Human cadence</span>
              <span style={{ fontFamily: "var(--mono)", fontSize: 11, color: "var(--muted2)" }}>Clean score 89</span>
            </div>
          </div>
          <div style={{ fontFamily: "var(--mono)", fontSize: 11, color: "var(--muted2)", letterSpacing: ".06em", textTransform: "uppercase" }}>Every audit explains <em style={{ color: "white", fontStyle: "normal" }}>why</em>. Not just a number.</div>
        </div>
      </div>
    </section>
  );
}
