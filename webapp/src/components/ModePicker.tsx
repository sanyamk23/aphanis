import type { Mode, Tone } from "../types";

const MODES: { value: Mode; label: string; desc: string }[] = [
  { value: "paranoid", label: "Paranoid", desc: "Maximum sanitization" },
  { value: "aggressive", label: "Aggressive", desc: "Thorough cleaning" },
  { value: "standard", label: "Standard", desc: "Balanced" },
  { value: "minimal", label: "Minimal", desc: "Light touch" },
];

const TONES: Tone[] = ["conversational", "casual", "tech-lead", "academic", "executive"];

export default function ModePicker({
  mode,
  tone,
  onMode,
  onTone,
}: {
  mode: Mode;
  tone: Tone;
  onMode: (m: Mode) => void;
  onTone: (t: Tone) => void;
}) {
  return (
    <div className="mode-picker">
      <div className="mode-group">
        {MODES.map((m) => (
          <button
            key={m.value}
            className={`mode-btn ${mode === m.value ? "active" : ""}`}
            onClick={() => onMode(m.value)}
            title={m.desc}
          >
            {m.label}
          </button>
        ))}
      </div>
      <select
        className="tone-select"
        value={tone}
        onChange={(e) => onTone(e.target.value as Tone)}
        title="Humanizer tone"
      >
        {TONES.map((t) => (
          <option key={t} value={t}>
            {t}
          </option>
        ))}
      </select>
    </div>
  );
}
