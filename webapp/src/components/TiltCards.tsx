import { useEffect } from "react";

const SELECTOR = ".bento-card, .exhibit-card, .trust-card, .compare-card, .step";

export default function TiltCards() {
  useEffect(() => {
    const mq = window.matchMedia("(hover: hover) and (pointer: fine)");
    if (!mq.matches) return;
    const els = Array.from(document.querySelectorAll<HTMLElement>(SELECTOR));
    const cleanups: Array<() => void> = [];
    els.forEach((el) => {
      el.classList.add("tilt");
      function onMove(e: MouseEvent) {
        const r = el.getBoundingClientRect();
        const px = (e.clientX - r.left) / r.width;
        const py = (e.clientY - r.top) / r.height;
        el.style.setProperty("--tilt-x", `${(0.5 - py) * 5}deg`);
        el.style.setProperty("--tilt-y", `${(px - 0.5) * 5}deg`);
        el.style.setProperty("--glow-x", `${px * 100}%`);
        el.style.setProperty("--glow-y", `${py * 100}%`);
      }
      function onLeave() {
        el.style.setProperty("--tilt-x", "0deg");
        el.style.setProperty("--tilt-y", "0deg");
      }
      el.addEventListener("mousemove", onMove);
      el.addEventListener("mouseleave", onLeave);
      cleanups.push(() => {
        el.removeEventListener("mousemove", onMove);
        el.removeEventListener("mouseleave", onLeave);
        el.classList.remove("tilt");
      });
    });
    return () => cleanups.forEach((c) => c());
  }, []);
  return null;
}
