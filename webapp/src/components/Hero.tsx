import { useEffect, useRef } from "react";
import gsap from "gsap";

export default function Hero({ onPrimary, onSecondary }: { onPrimary: () => void; onSecondary: () => void }) {
  const root = useRef<HTMLElement>(null);

  useEffect(() => {
    const ctx = gsap.context(() => {
      const tl = gsap.timeline({ defaults: { ease: "expo.out" } });
      tl.from(".hero-kicker", { y: 16, opacity: 0, duration: .6 }, 0)
        .from(".hero h1 .line span", { yPercent: 110, duration: .9, stagger: .08 }, .08)
        .from(".hero-sub", { y: 14, opacity: 0, duration: .6 }, .45)
        .from(".hero-actions .btn-pill", { y: 12, opacity: 0, duration: .5, stagger: .08 }, .55)
        .from(".hero-meta div", { y: 10, opacity: 0, duration: .5, stagger: .06 }, .62)
        .from(".hero-visual", { y: 18, opacity: 0, duration: .7 }, .35)
        .from(".hero-float", { y: 16, opacity: 0, duration: .6 }, .75);

      gsap.to(".hero-card", { y: -6, duration: 2.2, yoyo: true, repeat: -1, ease: "sine.inOut" });
      gsap.to(".hero-float", { y: -8, duration: 2.6, yoyo: true, repeat: -1, ease: "sine.inOut", delay: .4 });
    }, root);
    return () => ctx.revert();
  }, []);

  return (
    <section ref={root} className="hero">
      <div className="hero-grid" />
      <div className="hero-inner">
        <div className="hero-copy">
          <div className="hero-kicker kicker">Zero-Trust AI Provenance Firewall — v1.4.3</div>
          <h1>
            <span className="line"><span>Your words carry</span></span>
            <span className="line"><span className="grad">invisible</span> <span>fingerprints.</span></span>
          </h1>
          <p className="hero-sub">
            Every sentence you publish carries hidden signals — unicode tricks, vocabulary tells, statistical rhythms, metadata traces. Detectors read them before a human does. <strong style={{ color: "var(--ink)" }}>Aphanis finds those signals, explains them, and erases them.</strong>
          </p>
          <div className="hero-actions">
            <button className="btn-pill dark" onClick={onPrimary}>Try the live lab — free →</button>
            <button className="btn-pill ghost" onClick={onSecondary}>How it works</button>
          </div>
          <div className="hero-meta">
            <div><strong>4</strong> stego vectors</div>
            <div><strong>7</strong> sanitization layers</div>
            <div><strong>SHA-256</strong> certificates</div>
            <div><strong>CLI + MCP + Web</strong></div>
          </div>
          <div className="hero-badges">
            <span className="badge">Python 3.11 • REST API • React</span>
            <span className="badge">DOCX • PDF • PNG • IPYNB</span>
          </div>
        </div>

        <div className="hero-visual">
          <div className="hero-card">
            <div className="hero-card-top"><span>live scan — sample.docx</span><span className="dot" /></div>
            <div className="hero-scan">
              The results demonstrate a <span className="hl">significant improvement</span> over baseline.
              Moreover<span className="hl cyan">, it should be noted</span> that the approach is
              <span className="hl amber"> crucial</span> for future work. The dataset exhibits
              <span className="hl"> comprehensive</span> coverage and robust evaluation.
            </div>
            <div style={{ padding: "0 16px 16px", display: "grid", gap: 8 }}>
              <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
                <span className="badge" style={{ background: "rgba(255,255,255,.08)", color: "var(--muted2)", borderColor: "rgba(255,255,255,.12)" }}>vector_1 — unicode</span>
                <span className="badge" style={{ background: "rgba(255,255,255,.08)", color: "var(--muted2)", borderColor: "rgba(255,255,255,.12)" }}>vector_2 — statistical</span>
              </div>
              <div style={{ height: 6, background: "rgba(255,255,255,.12)", borderRadius: 999, overflow: "hidden" }}><i style={{ display: "block", height: "100%", width: "72%", background: "linear-gradient(90deg,var(--violet),var(--cyan))" }} /></div>
              <div style={{ fontFamily: "var(--mono)", fontSize: 11, color: "var(--muted2)", letterSpacing: ".06em", textTransform: "uppercase" }}>Overall clean score — 28 / 100 • High risk</div>
            </div>
          </div>
          <div className="hero-float">
            <strong>Before → After</strong>
            <p>Aphanis rewrites cadence, swaps tells, strips ghosts.</p>
            <div className="mini-bar"><div className="mini-fill" /></div>
            <div style={{ fontFamily: "var(--mono)", fontSize: 11, color: "var(--muted)", marginTop: 6 }}>Clean score 28 → 89</div>
          </div>
        </div>
      </div>
    </section>
  );
}
