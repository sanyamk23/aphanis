import type {
  AuditResponse,
  CertResponse,
  CleanFileResponse,
  CleanResponse,
  EntropyResult,
  HumanizeResponse,
  Mode,
  ProvenanceResponse,
  RiskMatrix,
  Tone,
} from "./types";

async function postJSON<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(path, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ error: res.statusText }));
    throw new Error(err.error || `request failed: ${res.status}`);
  }
  return res.json() as Promise<T>;
}

export const api = {
  audit: (text: string) => postJSON<AuditResponse>("/api/audit", { text }),
  clean: (text: string, mode: Mode, tone: Tone, perturb: boolean, humanize: boolean) =>
    postJSON<CleanResponse>("/api/clean", { text, mode, tone, perturb, humanize }),
  humanize: (text: string, tone: Tone) =>
    postJSON<HumanizeResponse>("/api/humanize", { text, tone }),
  scrub: (text: string) => postJSON<{ cleaned: string }>("/api/scrub", { text }),
  matrix: (text: string) => postJSON<RiskMatrix>("/api/matrix", { text }),
  entropy: (text: string) => postJSON<EntropyResult>("/api/entropy", { text }),
  provenance: (text: string) =>
    postJSON<ProvenanceResponse>("/api/provenance", { text }),
  cert: (text: string) => postJSON<CertResponse>("/api/cert", { text }),
  heatmap: (text: string) => postJSON<{ html: string }>("/api/heatmap", { text }),

  async cleanFile(file: File, mode: Mode, perturb: boolean, jitter: boolean): Promise<CleanFileResponse> {
    const fd = new FormData();
    fd.append("file", file);
    fd.append("mode", mode);
    fd.append("perturb", String(perturb));
    fd.append("jitter", String(jitter));
    const res = await fetch("/api/clean-file", { method: "POST", body: fd });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ error: res.statusText }));
      throw new Error(err.error || `upload failed: ${res.status}`);
    }
    return res.json() as Promise<CleanFileResponse>;
  },
};
