export default function Hero() {
  return (
    <section className="hero">
      <div className="hero-glow" />
      <h1 className="hero-title">
        Your words carry <span className="grad">invisible fingerprints</span>.
      </h1>
      <p className="hero-sub">
        AI detectors, forensic watermark scanners, and statistical profilers can tell
        machine-generated text from yours — even when you wrote it yourself. Aphanis
        finds those signals and erases them.
      </p>
      <div className="hero-stats">
        <div><strong>4</strong><span>stego vectors</span></div>
        <div><strong>7</strong><span>sanitization layers</span></div>
        <div><strong>SHA-256</strong><span>audit certificates</span></div>
      </div>
    </section>
  );
}
