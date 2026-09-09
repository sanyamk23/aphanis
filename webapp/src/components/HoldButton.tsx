import { useRef, useState } from "react";

export default function HoldButton({
  onComplete, duration = 900, disabled, children, className = "",
}: {
  onComplete: () => void; duration?: number; disabled?: boolean; children: React.ReactNode; className?: string;
}) {
  const [holding, setHolding] = useState(false);
  const completedRef = useRef(false);

  function start() {
    if (disabled) return;
    completedRef.current = false;
    setHolding(true);
  }
  function cancel() {
    if (completedRef.current) return;
    setHolding(false);
  }
  function onTransitionEnd(e: React.TransitionEvent<HTMLSpanElement>) {
    if (e.propertyName !== "transform" || !holding) return;
    completedRef.current = true;
    setHolding(false);
    onComplete();
  }

  return (
    <button
      type="button"
      className={`${className} hold-btn`}
      disabled={disabled}
      onMouseDown={start}
      onMouseUp={cancel}
      onMouseLeave={cancel}
      onTouchStart={start}
      onTouchEnd={cancel}
    >
      <span
        className="hold-fill"
        style={{ transform: holding ? "scaleX(1)" : "scaleX(0)", transitionDuration: `${duration}ms` }}
        onTransitionEnd={onTransitionEnd}
      />
      <span className="hold-label">{holding ? "keep holding…" : children}</span>
    </button>
  );
}
