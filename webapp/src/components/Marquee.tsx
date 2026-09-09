export default function Marquee() {
  const items = ["Zero-Trust Provenance", "Invisible Fingerprints Removed", "SHA-256 Certificates", "7-Layer Pipeline", "Paranoid → Minimal Control", "MCP • CLI • REST • Web"];
  const doubled = [...items, ...items, ...items];
  return (
    <div className="marquee">
      <div className="marquee-track">
        {doubled.map((t, i) => (
          <span key={i}><i>◈</i> {t} &nbsp; <i>—</i> &nbsp;</span>
        ))}
      </div>
    </div>
  );
}
