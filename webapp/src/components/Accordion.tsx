import { useState } from "react";

const QUESTIONS = [
  { q: "Does Aphanis modify the original file?", a: "No. It analyzes the copy in memory and outputs a cleaned version. Your source file is untouched." },
  { q: "Which models does it detect?", a: "All major LLMs that leave steganographic signatures: GPT-4 family, Claude, Gemini, Llama, Mistral. The detection lexicon updates weekly." },
  { q: "Is the SHA-256 certificate verifiable offline?", a: "Yes. Anyone with the original and cleaned text can recompute the hash and confirm the certificate — no API call required." },
  { q: "Does it work on images and audio?", a: "Phase 1 covers text provenance. Image and audio vector detection is in the roadmap — subscribe for the alpha invite." },
  { q: "Is it open source?", a: "Fully. The pipeline, lexicon, and cert logic are on GitHub under an MIT license." },
];

export default function Accordion() {
  const [open, setOpen] = useState<number | null>(null);
  return (
    <div style={{ maxWidth: 760, margin: "0 auto" }}>
      {QUESTIONS.map((item, i) => (
        <div key={i} style={{ borderBottom: "1px solid var(--line)", padding: "20px 0" }}>
          <button onClick={() => setOpen(open === i ? null : i)} style={{ width: "100%", display: "flex", justifyContent: "space-between", alignItems: "center", gap: 16, background: "none", border: "none", cursor: "pointer", fontFamily: "var(--display)", fontSize: "clamp(16px,2vw,20px)", letterSpacing: "-.02em", textAlign: "left", color: "var(--ink)" }}>
            <span>{item.q}</span>
            <span style={{ fontFamily: "var(--mono)", fontSize: 18, color: "var(--violet)", flexShrink: 0, transition: "transform .25s var(--ease)", transform: open === i ? "rotate(45deg)" : "rotate(0deg)" }}>+</span>
          </button>
          {open === i && <p style={{ color: "#3A342A", lineHeight: 1.7, marginTop: 14, fontSize: 14.5 }}>{item.a}</p>}
        </div>
      ))}
    </div>
  );
}
