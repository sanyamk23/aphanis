export type Mode = "paranoid" | "aggressive" | "standard" | "minimal";
export type Tone = "conversational" | "casual" | "tech-lead" | "academic" | "executive";

export interface AuditResult {
  status: string;
  score: number;
  issues: string[];
  entropy?: number;
  risk_matrix?: RiskMatrix;
}

export interface RiskVector {
  score: number;
  label: string;
  signals: string[];
}

export interface RiskMatrix {
  overall_clean_score: number;
  provenance_risk_level: string;
  entropy: number;
  vectors: {
    vector_1_unicode_steganography: RiskVector;
    vector_2_statistical_model: RiskVector;
    vector_3_metadata_container: RiskVector;
    vector_4_spatial_frequency: RiskVector;
  };
}

export interface EntropyResult {
  shannon_entropy: number;
  ttr: number;
  predictability_score: number;
  ai_likelihood: string;
  word_count: number;
  unique_word_count: number;
  avg_sentence_length: number;
  sentence_length_std: number;
  details: string[];
}

export interface AuditResponse {
  audit: AuditResult;
  entropy: EntropyResult;
  risk_matrix: RiskMatrix;
}

export interface CleanResponse {
  cleaned: string;
  mode: Mode;
  tone: Tone;
}

export interface HumanizeResponse {
  humanized: string;
  tone: Tone;
}

export interface ProvenanceResponse {
  record_id: string;
  timestamp: string;
  issuer: string;
  source_name: string;
  input_sha256: string;
  verdict: string;
  signals: string[];
  signature: string;
}

export interface CertResponse {
  certificate_id: string;
  timestamp: string;
  issuer: string;
  source_name: string;
  verification_status: string;
  hashes: { sha256_raw_input: string; sha256_clean_output: string };
  risk_assessment: string;
  entropy_metrics: EntropyResult;
}

export interface CleanFileResponse {
  success: boolean;
  message: string;
  filename?: string;
  size?: number;
  data_base64?: string;
}
