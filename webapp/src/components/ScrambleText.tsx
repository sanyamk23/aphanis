import { useEffect, useRef } from "react";
import gsap from "gsap";

const CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ01#$%&+-/\\";

export default function ScrambleText({ text, delay = 0, duration = 0.9, className }: { text: string; delay?: number; duration?: number; className?: string }) {
  const ref = useRef<HTMLSpanElement>(null);
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const obj = { p: 0 };
    const tween = gsap.to(obj, {
      p: text.length,
      duration,
      delay,
      ease: "power1.inOut",
      onUpdate: () => {
        const revealed = Math.floor(obj.p);
        let out = "";
        for (let i = 0; i < text.length; i++) {
          out += i < revealed || text[i] === " " ? text[i] : CHARS[Math.floor(Math.random() * CHARS.length)];
        }
        if (el) el.textContent = out;
      },
      onComplete: () => { if (el) el.textContent = text; },
    });
    return () => { tween.kill(); if (el) el.textContent = text; };
  }, [text, delay, duration]);
  return <span ref={ref} className={className}>{text}</span>;
}
