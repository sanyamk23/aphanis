export default function Nav({ onLab }: { onLab: () => void }) {
  return (
    <div className="nav-wrap">
      <nav className="nav">
        <a href="#" className="nav-brand">
          <span className="nav-mark">◈</span>
          Aphanis
          <span style={{ fontWeight: 400, color: "var(--muted)", fontSize: 12, letterSpacing: ".08em", textTransform: "uppercase", marginLeft: 6 }}>Provenance Firewall</span>
        </a>
        <div className="nav-links">
          <a href="#story">the tell</a>
          <a href="#exhibits">exhibits</a>
          <a href="#lab">the lab</a>
          <a href="#trust">the vow</a>
          <a href="https://github.com/sanyamk23/aphanis" target="_blank" rel="noreferrer">github</a>
        </div>
        <div className="nav-cta">
          <a href="#lab" onClick={(e) => { e.preventDefault(); onLab(); }} className="btn-pill dark">Open Lab →</a>
        </div>
      </nav>
    </div>
  );
}
