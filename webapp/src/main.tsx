import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./styles.css";
import Lenis from "lenis";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import gsap from "gsap";

gsap.registerPlugin(ScrollTrigger);

const lenis = new Lenis({ duration: 1.2, easing: (t: number) => Math.min(1, 1.001 - Math.pow(2, -10 * t)), orientation: "vertical", smoothWheel: true, syncTouch: false });

lenis.on("scroll", ScrollTrigger.update);
gsap.ticker.add((time: number) => { lenis.raf(time * 1000); });
gsap.ticker.lagSmoothing(0);

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
