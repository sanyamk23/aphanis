"""
Untrace AI :: Zero-Trust AI Provenance Firewall & Automatic Humanizer Engine.
"""

from untrace.cleaner import (
    UnicodeSanitizer,
    FileMetadataSanitizer,
    StatisticalPerturber,
    ImageWatermarkDisrupter,
    AuditTool,
    clean_text,
    clean_file,
    audit_text,
)
from untrace.entropy import EntropyAnalyzer
from untrace.rules import RuleEngine
from untrace.stealth import StealthProfile, StealthMode, StegoRiskMatrix
from untrace.humanizer import HumanizerEngine, humanize_text

__version__ = "1.3.0"

__all__ = [
    "UnicodeSanitizer",
    "FileMetadataSanitizer",
    "StatisticalPerturber",
    "ImageWatermarkDisrupter",
    "AuditTool",
    "EntropyAnalyzer",
    "RuleEngine",
    "StealthProfile",
    "StealthMode",
    "StegoRiskMatrix",
    "HumanizerEngine",
    "clean_text",
    "clean_file",
    "audit_text",
    "humanize_text",
]
