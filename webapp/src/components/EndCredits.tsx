import { useEffect, useRef } from "react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
gsap.registerPlugin(ScrollTrigger);

function scrollTo(id: string) {
  document.getElementById(id)?.scrollIntoView({ behavior: "smooth", block: "start" });
}

export default function EndCredits() {
  const ref = useRef<HTMLElement>(null);
  useEffect(() => {
    const ctx = gsap.context(() => {
      gsap.from(".credits-top > *, .credits-grid > *", { y: 18, opacity: 0, duration: .6, stagger: .06, ease: "expo.out", scrollTrigger: { trigger: ref.current, start: "top 88%" } });
      gsap.to(".credits-word", { opacity: 1, duration: 1.2, ease: "power1.out", scrollTrigger: { trigger: ref.current, start: "top 70%" } });
    }, ref);
    return () => ctx.revert();
  }, []);
  return (
    <footer ref={ref} className="credits">
      <div className="credits-word" aria-hidden>APHANIS</div>
      <div className="credits-inner">
        <div className="credits-top">
          <div>
            <div className="kicker">End credits</div>
            <h3 className="credits-h">That's the whole trace.</h3>
            <p className="credits-p">Zero-trust AI provenance, from first exhibit to final seal.</p>
          </div>
          <button className="btn-pill dark" onClick={() => scrollTo("lab")}>Run one more scan →</button>
        </div>

        <div className="credits-grid">
          <div>
            <div className="credits-label">The saga</div>
            <a href="#story" onClick={(e) => { e.preventDefault(); scrollTo("story"); }}>The Tell</a>
            <a href="#exhibits" onClick={(e) => { e.preventDefault(); scrollTo("exhibits"); }}>Ten Exhibits</a>
            <a href="#pipeline" onClick={(e) => { e.preventDefault(); scrollTo("pipeline"); }}>The Pipeline</a>
            <a href="#lab" onClick={(e) => { e.preventDefault(); scrollTo("lab"); }}>The Lab</a>
          </div>
          <div>
            <div className="credits-label">The vow</div>
            <a href="#trust" onClick={(e) => { e.preventDefault(); scrollTo("trust"); }}>Trust & privacy</a>
            <a href="https://github.com/sanyamk23/aphanis" target="_blank" rel="noreferrer">Source · GitHub</a>
            <span className="mono">SHA-256 certified</span>
          </div>
          <div>
            <div className="credits-label">Everywhere</div>
            <span className="mono">pip install aphanis</span>
            <span className="mono">npm i -g aphanis</span>
            <span className="mono">CLI · MCP · REST /api/*</span>
          </div>
        </div>

        <div className="credits-bottom">
          <span>◈ Aphanis — Zero-Trust AI Provenance Firewall · v1.4.3</span>
          <span>drawn from code · no trackers · reduced-motion honored</span>
        </div>
      </div>
    </footer>
  );
}
