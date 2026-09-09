import { useEffect, useRef } from "react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
gsap.registerPlugin(ScrollTrigger);

export default function WaxSeal() {
  const ref = useRef<SVGSVGElement>(null);
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    gsap.set(el, { scale: 0, rotate: -20, transformOrigin: "center" });
    const ctx = gsap.context(() => {
      gsap.to(el, {
        scale: 1, rotate: 0, duration: 0.7, ease: "back.out(2.2)",
        scrollTrigger: { trigger: el, start: "top 85%", once: true },
      });
    });
    return () => ctx.revert();
  }, []);
  return (
    <svg ref={ref} viewBox="0 0 64 64" width="40" height="40" aria-hidden>
      <circle cx="32" cy="32" r="27" fill="none" stroke="currentColor" strokeWidth="1.4" strokeDasharray="4 3.2" opacity="0.6" />
      <circle cx="32" cy="32" r="21" fill="currentColor" opacity="0.12" />
      <circle cx="32" cy="32" r="21" fill="none" stroke="currentColor" strokeWidth="1.6" />
      <path d="M32 20 L38 32 L32 44 L26 32 Z" fill="currentColor" />
      <path d="M32 20 L38 32 L32 44 L26 32 Z" fill="none" stroke="currentColor" strokeWidth="1" opacity="0.4" />
    </svg>
  );
}
