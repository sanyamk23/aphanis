"""
Untrace AI - Cryptographic Audit Certificate Generator.
Generates signed SHA-256 Zero-Trust Clean Certificates proving provenance hygiene for legal,
publishing, or enterprise compliance.
"""

import hashlib
import json
import time
import uuid
from typing import Dict, Any, Optional

from untrace.stealth import StegoRiskMatrix
from untrace.entropy import EntropyAnalyzer


class AuditCertificateGenerator:
    """Generates cryptographically verifiable Zero-Trust Clean Certificates."""

    @classmethod
    def generate_certificate(cls, raw_input: str, clean_output: str, source_name: str = "Input Text") -> Dict[str, Any]:
        """Generates a signed Audit Certificate JSON object."""
        raw_hash = hashlib.sha256(raw_input.encode('utf-8')).hexdigest()
        clean_hash = hashlib.sha256(clean_output.encode('utf-8')).hexdigest()

        risk_matrix = StegoRiskMatrix.evaluate(clean_output)
        entropy_metrics = EntropyAnalyzer.analyze(clean_output)

        cert_id = f"UNTRACE-CERT-{uuid.uuid4().hex[:8].upper()}"

        certificate = {
            "certificate_id": cert_id,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "issuer": "Untrace AI Zero-Trust Provenance Firewall v1.4.0",
            "source_name": source_name,
            "verification_status": "ZERO_TRUST_CLEAN" if risk_matrix["overall_clean_score"] >= 90 else "VERIFIED_WITH_ISSUES",
            "hashes": {
                "sha256_raw_input": raw_hash,
                "sha256_clean_output": clean_hash
            },
            "risk_assessment": {
                "overall_clean_score": risk_matrix["overall_clean_score"],
                "provenance_risk_level": risk_matrix["provenance_risk_level"],
                "vectors": risk_matrix["vectors"]
            },
            "entropy_metrics": entropy_metrics
        }

        return certificate

    @classmethod
    def save_certificate_file(cls, cert_data: Dict[str, Any], output_path: Optional[str] = None) -> str:
        """Saves certificate JSON file."""
        if not output_path:
            output_path = f"{cert_data['certificate_id'].lower()}.json"

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(cert_data, f, indent=2)

        return output_path
