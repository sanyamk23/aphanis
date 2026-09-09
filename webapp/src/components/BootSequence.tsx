import { useEffect, useRef, useState } from "react";
import gsap from "gsap";

const LINES = [
  "APHANIS FORENSIC ENGINE v1.4.3",
  "initializing zero-trust scanner...",
  "loading vector_1 :: unicode steganography ......... OK",
  "loading vector_2 :: statistical fingerprint ........ OK",
  "loading vector_3 :: metadata & container ........... OK",
  "loading vector_4 :: spatial frequency ............... OK",
  "arming 7-stage sanitization pipeline",
  "ready.",
];

export default function BootSequence() {
  const [visible, setVisible] = useState(false);
  const [lines, setLines] = useState<string[]>([]);
  const overlayRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    let seen = false;
    try { seen = sessionStorage.getItem("aphanis_boot_seen") === "1"; } catch { /* ignore */ }
    if (seen || reduced) return;
    setVisible(true);
    try { sessionStorage.setItem("aphanis_boot_seen", "1"); } catch { /* ignore */ }
    const prevOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";

    const timers: number[] = [];
    const dismiss = () => close();
    LINES.forEach((line, idx) => {
      timers.push(window.setTimeout(() => {
        setLines((prev) => [...prev, line]);
      }, 140 * idx));
    });
    const hardStop = window.setTimeout(close, 140 * LINES.length + 700);
    function forceHide() { setVisible(false); document.body.style.overflow = prevOverflow; }
    function close() {
      timers.forEach(clearTimeout);
      clearTimeout(hardStop);
      const el = overlayRef.current;
      if (!el) { forceHide(); return; }
      // GSAP's rAF-driven tween can stall if the tab is throttled/backgrounded;
      // this timer-based fallback guarantees the overlay is never stuck forever.
      const forceTimer = window.setTimeout(forceHide, 900);
      gsap.to(el, {
        yPercent: -100, duration: 0.6, ease: "power3.inOut",
        onComplete: () => { clearTimeout(forceTimer); forceHide(); },
      });
    }
    document.addEventListener("click", dismiss, { once: true });
    document.addEventListener("keydown", dismiss, { once: true });
    return () => {
      timers.forEach(clearTimeout);
      clearTimeout(hardStop);
      document.removeEventListener("click", dismiss);
      document.removeEventListener("keydown", dismiss);
      document.body.style.overflow = prevOverflow;
    };
  }, []);

  if (!visible) return null;
  return (
    <div ref={overlayRef} className="boot-overlay" role="status" aria-live="polite">
      <div className="boot-lines">
        {lines.map((l, idx) => <div key={idx} className="boot-line">{l}</div>)}
        <span className="boot-cursor" />
      </div>
      <div className="boot-skip">click or press any key to skip</div>
    </div>
  );
}
