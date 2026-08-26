"""
Aphanis :: Enterprise Zero-Trust AI Provenance Firewall & Automatic Humanizer Platform.
"""

from aphanis.cleaner import (
    UnicodeSanitizer,
    FileMetadataSanitizer,
    StatisticalPerturber,
    ImageWatermarkDisrupter,
    AuditTool,
    clean_text,
    clean_file,
    audit_text,
)
from aphanis.entropy import EntropyAnalyzer
from aphanis.rules import RuleEngine
from aphanis.stealth import StealthProfile, StealthMode, StegoRiskMatrix
from aphanis.humanizer import HumanizerEngine, humanize_text
from aphanis.clipboard import ClipboardDaemon
from aphanis.hooks import HookInstaller
from aphanis.office import OfficeSanitizer
from aphanis.cert import AuditCertificateGenerator
from aphanis.heatmap import HeatmapRenderer
from aphanis.spectral import SpectralNoiseDisrupter
from aphanis.autoinstall import AutoInstaller, auto_install_all

__version__ = "1.4.1"

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
    "AutoInstaller",
    "auto_install_all",
    "clean_text",
    "clean_file",
    "audit_text",
    "humanize_text",
]
