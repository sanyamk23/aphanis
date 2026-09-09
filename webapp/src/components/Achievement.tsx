import { useEffect, useState } from "react";

export default function Achievement({ id, title, sub }: { id: string; title: string; sub: string }) {
  const [show, setShow] = useState(false);

  useEffect(() => {
    let seen = false;
    try { seen = sessionStorage.getItem(`aphanis_ach_${id}`) === "1"; } catch { /* ignore */ }
    if (seen) return;
    try { sessionStorage.setItem(`aphanis_ach_${id}`, "1"); } catch { /* ignore */ }
    const t1 = window.setTimeout(() => setShow(true), 250);
    const t2 = window.setTimeout(() => setShow(false), 4200);
    return () => { clearTimeout(t1); clearTimeout(t2); };
  }, [id]);

  return (
    <div className={`achievement ${show ? "visible" : ""}`} role="status">
      <span className="achievement-icon">◈</span>
      <div>
        <div className="achievement-title">{title}</div>
        <div className="achievement-sub">{sub}</div>
      </div>
    </div>
  );
}
