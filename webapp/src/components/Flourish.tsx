import { useEffect, useRef } from "react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
gsap.registerPlugin(ScrollTrigger);

export default function Flourish() {
  const ref = useRef<SVGPathElement>(null);
  const diamondRef = useRef<SVGRectElement>(null);

  useEffect(() => {
    const path = ref.current;
    const diamond = diamondRef.current;
    if (!path || !diamond) return;
    const len = path.getTotalLength();
    gsap.set(path, { strokeDasharray: len, strokeDashoffset: len });
    gsap.set(diamond, { scale: 0, transformOrigin: "center" });
    const ctx = gsap.context(() => {
      const tl = gsap.timeline({ scrollTrigger: { trigger: path, start: "top 88%" } });
      tl.to(path, { strokeDashoffset: 0, duration: 1.1, ease: "power2.inOut" })
        .to(diamond, { scale: 1, duration: 0.4, ease: "back.out(3)" }, "-=.2");
    });
    return () => ctx.revert();
  }, []);

  return (
    <div className="flourish">
      <svg viewBox="0 0 400 32" preserveAspectRatio="none" aria-hidden>
        <path
          ref={ref}
          d="M0 16 C 60 -4, 100 36, 160 16 C 185 8, 195 8, 200 16 C 205 24, 215 24, 240 16 C 300 -4, 340 36, 400 16"
          fill="none"
          stroke="var(--line)"
          strokeWidth="1.4"
        />
        <rect ref={diamondRef} x="194" y="10" width="12" height="12" transform="rotate(45 200 16)" fill="var(--violet)" />
      </svg>
    </div>
  );
}
