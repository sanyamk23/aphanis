import { useEffect, useState } from "react";

const CHAPTERS: Record<string, string> = {
  hero: "I · The Signature",
  story: "II · The Tell",
  exhibits: "III · Ten Exhibits",
  vectors: "IV · The Vectors",
  pipeline: "V · The Pipeline",
  lab: "VI · The Lab",
  trust: "VII · The Vow",
  integrations: "Epilogue · Everywhere",
};

export default function SaveFile() {
  const [chapter, setChapter] = useState("I · The Signature");
  const [seen, setSeen] = useState(0);
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const sections = Array.from(document.querySelectorAll<HTMLElement>("[data-chapter]"));
    if (sections.length === 0) return;
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) {
            const key = e.target.getAttribute("data-chapter") ?? "";
            if (CHAPTERS[key]) setChapter(CHAPTERS[key]);
            if (key !== "hero") setVisible(true);
          }
        });
      },
      { rootMargin: "-40% 0px -40% 0px" }
    );
    sections.forEach((s) => io.observe(s));

    const exhibitIo = new IntersectionObserver(
      (entries) => {
        setSeen((prev) => {
          let count = prev;
          entries.forEach((e) => { if (e.isIntersecting) count = Math.max(count, Number(e.target.getAttribute("data-exhibit")) || 0); });
          return count;
        });
      },
      { rootMargin: "0px 0px -50% 0px" }
    );
    document.querySelectorAll<HTMLElement>("[data-exhibit]").forEach((el) => exhibitIo.observe(el));

    return () => { io.disconnect(); exhibitIo.disconnect(); };
  }, []);

  return (
    <div className={`save-file ${visible ? "visible" : ""}`}>
      <span className="save-dot" />
      <div>
        <div className="save-title">save file · ep. 1.4.3</div>
        <div className="save-line">chapter <strong>{chapter}</strong></div>
        {seen > 0 && <div className="save-line">exhibits seen <strong>{seen} / 10</strong></div>}
      </div>
    </div>
  );
}
