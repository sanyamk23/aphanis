import type { AuditResponse } from "../types";

function scoreColor(score: number) {
  if (score >= 80) return "var(--emerald)";
  if (score >= 50) return "var(--amber)";
  return "var(--rose)";
}

export default function ScoreCards({ audit }: { audit: AuditResponse }) {
  const { risk_matrix, entropy } = audit;
  const vectors = risk_matrix?.vectors;

  return (
    <div className="card score-cards">
      <div className="card-head">
        <h2>Provenance Report</h2>
        <span className={`risk-badge ${risk_matrix?.provenance_risk_level}`}>
          {risk_matrix?.provenance_risk_level}
        </span>
      </div>

      <div className="overall-score">
        <svg viewBox="0 0 120 120" className="score-ring">
          <circle cx="60" cy="60" r="52" className="ring-bg" />
          <circle
            cx="60"
            cy="60"
            r="52"
            className="ring-fg"
            stroke={scoreColor(risk_matrix?.overall_clean_score ?? 0)}
            strokeDasharray={`${((risk_matrix?.overall_clean_score ?? 0) / 100) * 327} 327`}
          />
          <text x="60" y="66" className="ring-text">
            {Math.round(risk_matrix?.overall_clean_score ?? 0)}
          </text>
        </svg>
        <div className="overall-label">
          <strong>Clean Score</strong>
          <span>higher = fewer detectable signals</span>
        </div>
      </div>

      <div className="vector-grid">
        {vectors &&
          Object.values(vectors).map((v, i) => (
            <div className="vector" key={i}>
              <div className="vector-top">
                <span className="vector-label">{v.label}</span>
                <span className="vector-score" style={{ color: scoreColor(v.score) }}>
                  {Math.round(v.score)}
                </span>
              </div>
              <div className="bar">
                <div
                  className="bar-fill"
                  style={{ width: `${v.score}%`, background: scoreColor(v.score) }}
                />
              </div>
              {v.signals.length > 0 && (
                <ul className="signals">
                  {v.signals.slice(0, 3).map((s, j) => (
                    <li key={j}>{s}</li>
                  ))}
                </ul>
              )}
            </div>
          ))}
      </div>

      <div className="entropy-strip">
        <div><strong>{entropy?.shannon_entropy?.toFixed(2)}</strong><span>Shannon entropy</span></div>
        <div><strong>{entropy?.ttr?.toFixed(2)}</strong><span>type-token ratio</span></div>
        <div><strong>{entropy?.predictability_score}%</strong><span>predictability</span></div>
        <div><strong>{entropy?.ai_likelihood}</strong><span>AI likelihood</span></div>
      </div>
    </div>
  );
}
