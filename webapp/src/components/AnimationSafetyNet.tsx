import { useEffect } from "react";
import gsap from "gsap";

const SELECTOR = [
  ".ink-kicker", ".ink-h1 .line", ".ink-sub", ".ink-actions > *", ".ink-meta", ".ink-card",
  ".companion", ".story-copy > *", ".reveal", ".point",
  ".vectors h2", ".vectors .sub", ".bento-card",
  ".layers-head > *", ".step",
  ".exhibits-kicker > *", ".exhibit-card",
  ".trust-head > *", ".trust-diagram", ".trust-card",
].join(",");

export default function AnimationSafetyNet() {
  useEffect(() => {
    const t = setTimeout(() => {
      gsap.set(SELECTOR, { clearProps: "opacity,transform" });
    }, 3200);
    return () => clearTimeout(t);
  }, []);
  return null;
}
