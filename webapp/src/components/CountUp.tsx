import { useEffect, useRef } from "react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
gsap.registerPlugin(ScrollTrigger);

export default function CountUp({ to, suffix = "", duration = 1.2 }: { to: number; suffix?: string; duration?: number }) {
  const ref = useRef<HTMLSpanElement>(null);
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const obj = { v: 0 };
    const ctx = gsap.context(() => {
      gsap.to(obj, {
        v: to,
        duration,
        ease: "power2.out",
        scrollTrigger: { trigger: el, start: "top 92%", once: true },
        onUpdate: () => { if (el) el.textContent = `${Math.round(obj.v)}${suffix}`; },
      });
    });
    return () => ctx.revert();
  }, [to, suffix, duration]);
  return <span ref={ref} className="count-up">0{suffix}</span>;
}
