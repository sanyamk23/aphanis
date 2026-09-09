import { useEffect, useRef, useState } from "react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import Chapter from "./Chapter";
gsap.registerPlugin(ScrollTrigger);

type Exhibit = { n: string; title: string; signal: string; before: string; after: string; fix: string; vector: string };

const EXHIBITS: Exhibit[] = [
  { n: "01", title: "Zero-width steganography", signal: "Vector 1 · unicode", before: "hello​world‌ — invisible between letters", after: "helloworld — stripped, zero ghosts", fix: "Strip \\u200B \\u200C \\u200D \\uFEFF + Bidi isolates", vector: "1" },
  { n: "02", title: "Non-breaking spaces & homoglyphs", signal: "Vector 1 · unicode", before: "café with NBSP and сyrillic а", after: "cafe with plain spaces and latin a", fix: "Normalize NBSP, homoglyph map, NFKC", vector: "1" },
  { n: "03", title: "AI vocabulary clichés", signal: "Vector 2 · statistical", before: "delve into the tapestry — a testament to robust synergy", after: "explore the pattern — evidence of strong collaboration", fix: "Lexicon swap: delve→explore, tapestry→pattern, testament→evidence", vector: "2" },
  { n: "04", title: "Em-dash fingerprint", signal: "Vector 2 · statistical", before: "results — moreover — crucial — comprehensive —", after: "results. Moreover, the findings are thorough.", fix: "Collapse em-dash chains, restore sentence rhythm", vector: "2" },
  { n: "05", title: "Wordy hedges & throat-clearing", signal: "Vector 2 · statistical", before: "It should be noted that it is crucial to observe that…", after: "Note: this matters because…", fix: "Hedge collapse + active voice", vector: "2" },
  { n: "06", title: "Missing contractions", signal: "Vector 2 · statistical", before: "It is not possible and we are not able to ensure…", after: "It's not possible and we can't ensure…", fix: "Contraction injection (tone-aware)", vector: "2" },
  { n: "07", title: "Predictability & burstiness", signal: "Vector 2 · entropy", before: "TTR 0.52 · predictability 78% · uniform sentence length", after: "TTR 0.71 · predictability 41% · varied cadence", fix: "N-gram breaker + sentence reshaper", vector: "2" },
  { n: "08", title: "Formulaic openers", signal: "Vector 2 · statistical", before: "In conclusion, the results demonstrate that…", after: "The results show that…", fix: "Opener diversification, list-pattern breaker", vector: "2" },
  { n: "09", title: "Container metadata", signal: "Vector 3 · metadata", before: "DOCX core.xml: creator=ChatGPT, app=python-docx", after: "core.xml: creator — , lastModifiedBy — , scrubbed", fix: "C2PA / EXIF / XML scrub for docx/pdf/ipynb", vector: "3" },
  { n: "10", title: "Spatial frequency (images)", signal: "Vector 4 · spatial", before: "DCT artifacts: GAN grid in high-frequency", after: "Frequency normalized — spectral watermark removed", fix: "DCT-domain perturbation", vector: "4" },
];

export default function Exhibits() {
  const ref = useRef<HTMLElement>(null);
  const [active, setActive] = useState(0);

  useEffect(() => {
    const ctx = gsap.context(() => {
      gsap.from(".exhibits-kicker > *", { y: 14, opacity: 0, duration: .6, stagger: .08, ease: "expo.out", scrollTrigger: { trigger: ".exhibits", start: "top 82%" } });
      // pin the rail on desktop
      ScrollTrigger.matchMedia({
        "(min-width: 981px)": () => {
          ScrollTrigger.create({
            trigger: ".exhibits-body",
            start: "top 96px",
            end: "bottom bottom",
            pin: ".exhibits-rail",
            pinSpacing: false,
          });
        },
      });
      // activate on scroll
      const cards = gsap.utils.toArray<HTMLElement>(".exhibit-card");
      cards.forEach((el, i) => {
        ScrollTrigger.create({
          trigger: el,
          start: "top 58%",
          end: "bottom 42%",
          onEnter: () => setActive(i),
          onEnterBack: () => setActive(i),
        });
      });
    }, ref);
    return () => ctx.revert();
  }, []);

  function jump(i: number) {
    document.getElementById(`exhibit-${EXHIBITS[i].n}`)?.scrollIntoView({ behavior: "smooth", block: "center" });
    setActive(i);
  }

  return (
    <section ref={ref} id="exhibits" className="exhibits">
      <div className="exhibits-kicker">
        <Chapter n={3} label="Ten Exhibits" />
        <div className="kicker">The method — 10 exhibits</div>
        <h2>Every signal, shown before & after.</h2>
        <p>Ten forensic checks that detectors actually use. Click the rail to jump — each exhibit shows the raw tell and the exact fix Aphanis applies.</p>
      </div>

      <div className="exhibits-body">
        <nav className="exhibits-rail" aria-label="Exhibits">
          {EXHIBITS.map((e, i) => (
            <button key={e.n} className={`rail-item ${i === active ? "active" : ""}`} onClick={() => jump(i)} aria-current={i === active ? "true" : undefined}>
              <span className="rail-n">{e.n}</span>
              <span className="rail-t">{e.title}</span>
              <span className="rail-v">V{e.vector}</span>
            </button>
          ))}
          <div className="rail-progress"><i style={{ height: `${((active + 1) / EXHIBITS.length) * 100}%` }} /></div>
        </nav>

        <div className="exhibits-list">
          {EXHIBITS.map((e) => (
            <article key={e.n} id={`exhibit-${e.n}`} className="exhibit-card">
              <div className="exhibit-head">
                <span className="exhibit-num">{e.n}</span>
                <span className="exhibit-signal">{e.signal}</span>
              </div>
              <h3>{e.title}</h3>
              <div className="exhibit-compare">
                <div className="exhibit-before">
                  <span className="label">Before — flagged</span>
                  <code>{e.before}</code>
                </div>
                <div className="exhibit-arrow">→</div>
                <div className="exhibit-after">
                  <span className="label">After — clean</span>
                  <code>{e.after}</code>
                </div>
              </div>
              <div className="exhibit-fix"><span>Fix:</span> {e.fix}</div>
            </article>
          ))}
        </div>
      </div>

      <div className="exhibits-foot">
        <span className="badge">7 stages orchestrate these 10 exhibits</span>
        <span className="badge">Paranoid → minimal — you choose the trade-off</span>
      </div>
    </section>
  );
}
