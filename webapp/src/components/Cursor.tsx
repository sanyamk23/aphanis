import { useEffect, useState } from "react";

export default function Cursor() {
  const [pos, setPos] = useState({ x: -100, y: -100 });
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    let idle = 0;
    const cur = { x: 0, y: 0 };
    const onMove = (e: MouseEvent) => {
      cur.x = e.clientX; cur.y = e.clientY;
    setPos({ x: cur.x, y: cur.y });
      setVisible(true);
      clearTimeout(idle);
    };
    const onLeave = () => setVisible(false);
    const onVis = () => { if (document.hidden) setVisible(false); };
    window.addEventListener("mousemove", onMove);
    window.addEventListener("mouseleave", onLeave);
    document.addEventListener("visibilitychange", onVis);
    return () => { window.removeEventListener("mousemove", onMove); window.removeEventListener("mouseleave", onLeave); document.removeEventListener("visibilitychange", onVis); };
  }, []);

  return (
    <>
      <style>{`
        .cursor-dot, .cursor-ring {
          position: fixed; pointer-events: none; z-index: 99998;
          border-radius: 50%; transform: translate(-50%, -50%);
          transition: opacity .2s;
        }
        .cursor-dot { width: 6px; height: 6px; background: var(--violet); border-radius: 50%; }
        .cursor-ring { width: 36px; height: 36px; border: 1.5px solid rgba(201,58,31,.35); }
        .cursor-ring.hover { border-color: var(--violet); transform: translate(-50%, -50%) scale(1.4); }
        a:hover ~ .cursor-dot, button:hover ~ .cursor-dot, [tabindex]:hover ~ .cursor-dot { opacity: 0; }
        a:hover ~ .cursor-ring, button:hover ~ .cursor-ring, [tabindex]:hover ~ .cursor-ring { border-color: var(--violet); transform: translate(-50%, -50%) scale(1.4); }
        @media (max-width: 980px) { .cursor-dot, .cursor-ring { display: none; } }
        @media (prefers-reduced-motion: reduce) { .cursor-dot, .cursor-ring { display: none; } }
      `}</style>
      <div className="cursor-dot" style={{ left: pos.x, top: pos.y, opacity: visible ? 1 : 0 }} />
      <div className="cursor-ring" style={{ left: pos.x, top: pos.y, opacity: visible ? 1 : 0 }} />
    </>
  );
}
