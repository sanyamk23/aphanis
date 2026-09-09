import { useEffect } from "react";
import gsap from "gsap";

const SELECTOR = ".btn-pill.dark, .btn.primary, .companion-choice.primary";

export default function MagneticButtons() {
  useEffect(() => {
    const mq = window.matchMedia("(hover: hover) and (pointer: fine)");
    if (!mq.matches) return;
    const cleanups: Array<() => void> = [];
    const attach = (els: HTMLElement[]) => {
      els.forEach((el) => {
        if (el.dataset.magnetic) return;
        el.dataset.magnetic = "1";
        function onMove(e: MouseEvent) {
          const r = el.getBoundingClientRect();
          const x = (e.clientX - r.left - r.width / 2) * 0.3;
          const y = (e.clientY - r.top - r.height / 2) * 0.3;
          gsap.to(el, { x, y, duration: 0.3, ease: "power2.out" });
        }
        function onLeave() {
          gsap.to(el, { x: 0, y: 0, duration: 0.4, ease: "elastic.out(1, 0.4)" });
        }
        el.addEventListener("mousemove", onMove);
        el.addEventListener("mouseleave", onLeave);
        cleanups.push(() => {
          el.removeEventListener("mousemove", onMove);
          el.removeEventListener("mouseleave", onLeave);
          delete el.dataset.magnetic;
        });
      });
    };
    attach(Array.from(document.querySelectorAll<HTMLElement>(SELECTOR)));
    const mo = new MutationObserver(() => {
      attach(Array.from(document.querySelectorAll<HTMLElement>(SELECTOR)));
    });
    mo.observe(document.body, { childList: true, subtree: true });
    return () => { mo.disconnect(); cleanups.forEach((c) => c()); };
  }, []);
  return null;
}
