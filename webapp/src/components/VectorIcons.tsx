const common = { fill: "none", stroke: "currentColor", strokeWidth: 1.6, strokeLinecap: "round" as const, strokeLinejoin: "round" as const };

export function IconGhost() {
  return (
    <svg viewBox="0 0 24 24" width="18" height="18" {...common}>
      <path d="M8 4 L5 4 L5 20 L8 20" />
      <path d="M16 4 L19 4 L19 20 L16 20" />
      <circle cx="12" cy="12" r="1.3" strokeDasharray="0.1 4" />
    </svg>
  );
}

export function IconPulse() {
  return (
    <svg viewBox="0 0 24 24" width="18" height="18" {...common}>
      <path d="M3 14 L7 14 L9 6 L12 18 L14 9 L15.5 14 L21 14" />
    </svg>
  );
}

export function IconSeal() {
  return (
    <svg viewBox="0 0 24 24" width="18" height="18" {...common}>
      <path d="M6 3 H14 L18 7 V21 H6 Z" />
      <path d="M14 3 V7 H18" />
      <circle cx="15.5" cy="15" r="2.6" />
      <path d="M14.3 17 L13.5 20.5 L15.5 19.2 L17.5 20.5 L16.7 17" />
    </svg>
  );
}

export function IconDocument() {
  return (
    <svg viewBox="0 0 24 24" width="18" height="18" {...common}>
      <path d="M6 3 H14 L18 7 V21 H6 Z" />
      <path d="M14 3 V7 H18" />
      <path d="M9 12 H15 M9 15.5 H15 M9 9 H12" />
    </svg>
  );
}

export function IconGrid() {
  return (
    <svg viewBox="0 0 24 24" width="18" height="18" {...common}>
      <rect x="3" y="4" width="6" height="6" opacity={1} />
      <rect x="10" y="4" width="6" height="6" opacity={0.65} />
      <rect x="17" y="4" width="4" height="6" opacity={0.35} />
      <rect x="3" y="11" width="6" height="6" opacity={0.65} />
      <rect x="10" y="11" width="6" height="6" opacity={0.35} />
    </svg>
  );
}
