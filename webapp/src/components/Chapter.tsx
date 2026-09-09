const ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII"];

export default function Chapter({ n, label }: { n: number; label: string }) {
  return (
    <div className="chapter-mark">
      <span className="chapter-roman">{ROMAN[n - 1] ?? n}</span>
      <span className="chapter-label">{label}</span>
    </div>
  );
}
