"""
Untrace AI :: Enterprise Zero-Trust AI Provenance Firewall & Humanizer Platform.
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
from untrace.clipboard import ClipboardDaemon
from untrace.hooks import HookInstaller
from untrace.office import OfficeSanitizer
from untrace.cert import AuditCertificateGenerator
from untrace.heatmap import HeatmapRenderer
from untrace.spectral import SpectralNoiseDisrupter

__version__ = "1.4.0"

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
    "ClipboardDaemon",
    "HookInstaller",
    "OfficeSanitizer",
    "AuditCertificateGenerator",
    "HeatmapRenderer",
    "SpectralNoiseDisrupter",
    "clean_text",
    "clean_file",
    "audit_text",
    "humanize_text",
]
