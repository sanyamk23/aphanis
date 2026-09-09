export default function Compare() {
  return (
    <section className="compare">
      <div className="compare-card">
        <h3>Without Aphanis — raw AI text</h3>
        <p>“It is important to note that the comprehensive analysis demonstrates a significant improvement. Moreover, the findings highlight the crucial role of robust evaluation methodologies.”</p>
        <div style={{ marginTop: 10, display: "flex", gap: 8, flexWrap: "wrap" }}>
          <span className="badge" style={{ background: "rgba(244,63,94,.10)", borderColor: "rgba(244,63,94,.22)", color: "#BE123C" }}>Flagged — AI likelihood: high</span>
          <span className="badge">Predictability 78%</span>
        </div>
        <div className="bar2" style={{ marginTop: 10 }}><i style={{ width: "78%", background: "var(--rose)" }} /></div>
      </div>
      <div className="compare-card" style={{ outline: "2px solid var(--ink)", outlineOffset: 0 }}>
        <h3>With Aphanis — paranoid + conversational</h3>
        <p>“Here’s what changed: the analysis actually moves the needle. What stood out was how much careful evaluation mattered: not just the numbers, but how they were checked.”</p>
        <div style={{ marginTop: 10, display: "flex", gap: 8, flexWrap: "wrap" }}>
          <span className="badge" style={{ background: "rgba(16,185,129,.12)", borderColor: "rgba(16,185,129,.22)", color: "#0B7A5A" }}>Clean — AI likelihood: low</span>
          <span className="badge">Predictability 32%</span>
        </div>
        <div className="bar2" style={{ marginTop: 10 }}><i style={{ width: "32%", background: "var(--emerald)" }} /></div>
      </div>
    </section>
  );
}
