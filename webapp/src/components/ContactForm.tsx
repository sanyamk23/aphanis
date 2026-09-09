import { useState } from "react";
import "./ContactForm.css";

export default function ContactForm() {
  const [email, setEmail] = useState("");
  const [status, setStatus] = useState<"idle" | "sending" | "sent">("idle");

  const validate = (v: string) => v.includes("@") && v.includes(".");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!validate(email)) return;
    setStatus("sent");
  };

  return (
    <section className="contact-section" data-chapter="contact">
      <div className="contact-card">
        <h2>Join the provenance movement</h2>
        <p>Get early access to the full Aphanis suite – forensic-grade watermark removal, zero-shot sanitization, and SHA-256 certified provenance.</p>
        {status === "sent" ? (
          <div className="success-state">
            <div className="success-icon">✓</div>
            <p> Signed. Check your inbox for the invite link.</p>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="contact-form">
            <input
              type="email"
              placeholder="you@company.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="contact-input"
              disabled={status === "sending"}
            />
            <button
              type="submit"
              className="btn primary contact-btn"
              disabled={status === "sending" || !validate(email)}
              style={{ minWidth: 120 }}
            >
              {status === "sending" ? "…" : "Request access"}
            </button>
            {!validate(email) && email.length > 0 && (
              <span className="error-hint">Enter a valid email</span>
            )}
          </form>
        )}
      </div>
    </section>
  );
}
