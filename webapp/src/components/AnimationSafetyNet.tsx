import { useEffect } from "react";
import gsap from "gsap";

const SELECTOR = [
  ".ink-kicker", ".ink-h1 .line", ".ink-sub", ".ink-actions > *", ".ink-meta", ".ink-card",
  ".companion", ".story-copy > *", ".reveal", ".point",
  ".vectors h2", ".vectors .sub", ".bento-card",
  ".layers-head > *", ".step",
  ".exhibits-kicker > *", ".exhibit-card",
  ".trust-head > *", ".trust-diagram", ".trust-card",
  ".credits-top > *", ".credits-grid > *",
].join(",");

// .credits-word carries a positioning transform (translateX for centering), not
// an animation one -- only its opacity is ever GSAP-animated, so it must never
// have "transform" cleared or it loses its centering.
const OPACITY_ONLY_SELECTOR = ".credits-word";

export default function AnimationSafetyNet() {
  useEffect(() => {
    const t = setTimeout(() => {
      gsap.set(SELECTOR, { clearProps: "opacity,transform" });
      gsap.set(OPACITY_ONLY_SELECTOR, { opacity: 1 });
    }, 3200);
    return () => clearTimeout(t);
  }, []);
  return null;
}
