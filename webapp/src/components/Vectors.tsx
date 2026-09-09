import { useEffect, useRef } from "react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import Chapter from "./Chapter";
gsap.registerPlugin(ScrollTrigger);

const V = [
  { k: "Vector 1", title: "Unicode Steganography", desc: "Zero-width joiners, non-breaking spaces, homoglyphs — ghosts between characters.", chips: ["\\u200B", "\\u00A0", "homoglyphs"], pct: 82, icon: "◬" },
  { k: "Vector 2", title: "Statistical Fingerprint", desc: "Vocabulary tells, n-gram predictability, burstiness that betrays a model.", chips: ["T-T-R", "perplexity proxy", "AI vocab"], pct: 74, icon: "◎" },
  { k: "Vector 3", title: "Metadata & Container", desc: "DOCX/PDF/IPYNB/PPTX — author fields, revision history, execution traces.", chips: ["DOCX core.xml", "PDF Info", "notebook cells"], pct: 68, icon: "⬢" },
  { k: "Vector 4", title: "Spatial Frequency", desc: "Pixel-level watermarks in PNG/JPG — invisible noise only a spectrum reveals.", chips: ["DCT", "spectral trace"], pct: 58, icon: "⬣" },
];

export default function Vectors() {
  const ref = useRef<HTMLElement>(null);
  useEffect(() => {
    const ctx = gsap.context(() => {
      gsap.from(".vectors h2, .vectors .sub", { y: 16, opacity: 0, duration: .6, stagger: .08, ease: "expo.out", scrollTrigger: { trigger: ".vectors", start: "top 82%" } });
      gsap.from(".bento-card", { y: 20, opacity: 0, duration: .6, stagger: .08, ease: "expo.out", scrollTrigger: { trigger: ".bento", start: "top 82%" } });
      ScrollTrigger.create({
        trigger: ".bento", start: "top 75%",
        onEnter: () => gsap.to(".bar2 i", { width: (_i: number, el: Element) => (el as HTMLElement).dataset.w + "%", duration: .9, stagger: .08, ease: "expo.out" }),
      });
    }, ref);
    return () => ctx.revert();
  }, []);
  return (
    <section ref={ref} id="vectors" className="vectors">
      <Chapter n={4} label="The Vectors" />
      <div className="kicker">Four vectors, one firewall</div>
      <h2>The four fingerprints detectors read first.</h2>
      <p className="sub">Aphanis audits each vector independently — so you see exactly where the signal lives before you sanitize it.</p>
      <div className="bento">
        {V.map((v) => (
          <div key={v.k} className="bento-card">
            <div className="bento-top">
              <span className="mono" style={{ fontSize: 11, letterSpacing: ".08em", textTransform: "uppercase", color: "var(--muted)", fontWeight: 700 }}>{v.k}</span>
              <span className="bento-icon">{v.icon}</span>
            </div>
            <h3>{v.title}</h3>
            <p>{v.desc}</p>
            <div className="bento-meta">{v.chips.map((c) => <span key={c} className="chip">{c}</span>)}</div>
            <div className="bar2"><i data-w={String(v.pct)} /></div>
            <div className="mono" style={{ fontSize: 11, color: "var(--muted)", marginTop: 6, letterSpacing: ".04em" }}>Typical signal strength — {v.pct}%</div>
          </div>
        ))}
      </div>
    </section>
  );
}
