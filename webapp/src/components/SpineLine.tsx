import { useEffect, useRef } from "react";

export default function SpineLine() {
  const ref = useRef<HTMLDivElement>(null);
  useEffect(() => {
    function onScroll() {
      const h = document.documentElement;
      const max = h.scrollHeight - h.clientHeight;
      const pct = max > 0 ? (h.scrollTop / max) * 100 : 0;
      if (ref.current) ref.current.style.height = `${pct}%`;
    }
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll);
    return () => { window.removeEventListener("scroll", onScroll); window.removeEventListener("resize", onScroll); };
  }, []);
  return (
    <div className="spine-track" aria-hidden>
      <div ref={ref} className="spine-fill" />
    </div>
  );
}
