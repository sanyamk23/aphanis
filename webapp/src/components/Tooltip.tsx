import { useState, useRef, useEffect } from "react";

export function Tooltip({ content, children }: { content: string; children: React.ReactNode }) {
  const [show, setShow] = useState(false);
  const [pos, setPos] = useState<{ x: number; y: number } | null>(null);
  const r = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!show || !r.current) return;
    const el = r.current;
    const rect = el.getBoundingClientRect();
    const tooltipW = 240;
    const tooltipH = 64;
    let x = rect.left + rect.width / 2;
    let y = rect.top - tooltipH - 8;
    const vx = window.scrollX;
    const vy = window.scrollY;
    if (x + tooltipW / 2 + 12 > vx + window.innerWidth) x = rect.right - tooltipW - 4;
    if (x - tooltipW / 2 - 12 < vx) x = rect.left + 4;
    if (y < vy) y = rect.bottom + 8;
    setPos({ x, y });
  }, [show]);

  return (
    <div
      ref={r}
      className="aph-tip"
      onMouseEnter={() => setShow(true)}
      onMouseLeave={() => setShow(false)}
      onFocus={() => setShow(true)}
      onBlur={() => setShow(false)}
      style={{ display: "inline-block", cursor: "help" }}
    >
      {children}
      {show && pos && (
        <div
          className="aph-tip-bubble"
          style={{
            position: "fixed",
            left: pos.x,
            top: pos.y,
            zIndex: 9999,
            width: 240,
            maxWidth: "var(--tip-max-width, 240px)",
            padding: "6px 10px",
            background: "var(--ink)",
            color: "var(--paper)",
            fontFamily: "var(--mono)",
            fontSize: 11,
            lineHeight: 1.5,
            borderRadius: 8,
            pointerEvents: "none",
            opacity: show ? 1 : 0,
            transition: "opacity .15s ease",
            boxShadow: "0 8px 24px rgba(0,0,0,.18)",
          }}
        >
          {content}
          <div
            className="aph-tip-arrow"
            style={{
              position: "absolute",
              top: "100%",
              left: "50%",
              marginLeft: -4,
              border: "4px solid transparent",
              borderTopColor: "var(--ink)",
              width: 0,
              height: 0,
              pointerEvents: "none",
            }}
          />
        </div>
      )}
    </div>
  );
}
