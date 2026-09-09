import { useEffect, useRef } from "react";

export default function Particles({ count = 40, radius = 120, color = "rgba(201,58,31,.12)" }) {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current!;
    const ctx = canvas.getContext("2d")!;

    let w = 0, h = 0;
    const pts: { x: number; y: number; vx: number; vy: number; r: number }[] = [];

    function resize() {
      w = canvas.width = window.innerWidth;
      h = canvas.height = window.innerHeight;
    }
    resize();
    window.addEventListener("resize", resize);

    for (let i = 0; i < count; i++) {
      pts.push({ x: Math.random() * w, y: Math.random() * h, vx: (Math.random() - .5) * .35, vy: (Math.random() - .5) * .35, r: Math.random() * 1.8 + .6 });
    }

    let anim = true;
    function draw() {
      if (!anim) return;
      ctx.clearRect(0, 0, w, h);
      for (const p of pts) {
        p.x += p.vx; p.y += p.vy;
        if (p.x < 0) p.x = w; if (p.x > w) p.x = 0;
        if (p.y < 0) p.y = h; if (p.y > h) p.y = 0;
        ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2); ctx.fillStyle = color; ctx.fill();
      }
      for (let i = 0; i < pts.length; i++) {
        for (let j = i + 1; j < pts.length; j++) {
          const dx = pts[i].x - pts[j].x, dy = pts[i].y - pts[j].y;
          const d = Math.sqrt(dx * dx + dy * dy);
          if (d < radius) {
            ctx.beginPath(); ctx.moveTo(pts[i].x, pts[i].y); ctx.lineTo(pts[j].x, pts[j].y);
            ctx.strokeStyle = `rgba(201,58,31,${(.12 * (1 - d / radius)).toFixed(3)})`;
            ctx.lineWidth = .5; ctx.stroke();
          }
        }
      }
      requestAnimationFrame(draw);
    }
    draw();

    const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduced) { anim = false; ctx.clearRect(0, 0, w, h); }

    return () => { anim = false; window.removeEventListener("resize", resize); };
  }, [count, radius, color]);

  return <canvas ref={canvasRef} style={{ position: "fixed", inset: 0, zIndex: 0, pointerEvents: "none", opacity: .55 }} />;
}
