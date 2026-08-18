<div align="center">

# 🛡️ UNTRACE AI :: Enterprise Suite v1.4.0

```text
  _   _ _  _ _____ ___    _   ___ ___   _   ___ 
 | | | | \| |_   _| _ \  /_\ / __| __| /_\ |_ _|
 | |_| | .` | | | |   / / _ \ (__| _| / _ \ | | 
  \___/|_|\_| |_| |_|_\/_/ \_\___|___/_/ \_\___|
```

### *The Enterprise Zero-Trust AI Provenance Firewall, Automatic Humanizer & Stego Matrix*

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg?style=for-the-badge&logo=python)](https://python.org)
[![MCP Server](https://img.shields.io/badge/MCP-Enterprise--v1.4.0-000000.svg?style=for-the-badge&logo=anthropic)](https://modelcontextprotocol.io)
[![Claude Skill](https://img.shields.io/badge/Claude%20Code-Stealth--Skill-7A1FA2.svg?style=for-the-badge&logo=anthropic)](https://anthropic.com)
[![License](https://img.shields.io/badge/license-MIT-green.svg?style=for-the-badge)](LICENSE)

<br/>

[Enterprise Suite Features](#-enterprise-suite-features) •
[Clipboard Daemon](#-clipboard-hygiene-daemon) •
[Git Hooks & CI/CD](#-git-pre-commit-hook--github-action) •
[Audit Certificates](#-cryptographic-audit-certificates) •
[Forensics Heatmap](#-forensics-heatmap-visualizer) •
[Jupyter & Office](#-jupyter-ipynb--office-sanitizer) •
[Quick Start](#-quick-start)

</div>

---

## ⚡ What is Untrace AI?

**Untrace AI** is an enterprise-grade **Zero-Trust AI Provenance Firewall, Automatic Humanizer & Stego Defense Platform**. It audits, sanitizes, and neutralizes multi-vendor AI provenance signals, zero-width steganography, C2PA/EXIF metadata, em-dash signatures, and **automatically converts AI text into authentic conversational human tone**.

---

## 🌟 Enterprise Suite Features (v1.4.0)

### 1. 📋 Automatic Clipboard Hygiene Daemon (`untrace clipboard`)
Runs a real-time background listener on your system clipboard (`Cmd+C` / `Ctrl+C`). Automatically scrubs zero-width spaces and humanizes text copied from ChatGPT/Claude before you paste it anywhere.

### 2. 🪝 Git Pre-Commit Hook & GitHub Action (`untrace install-hook`)
- `untrace install-hook`: Installs `.git/hooks/pre-commit` to prevent commits containing invisible watermarks or C2PA metadata.
- `untrace init-github-action`: Generates `.github/workflows/untrace-hygiene.yml` for automated CI/CD pipeline audits.

### 3. 🎨 Custom Tone Personas (`--tone`)
Choose from targeted humanization personas: `conversational`, `casual`, `tech-lead`, `academic`, `executive`.

### 4. 📓 Jupyter Notebook (`.ipynb`) & Office (`.pptx` / `.xlsx`) Sanitizer
Sanitizes notebook markdown/code cells, strips prompt execution logs, and purges core OpenXML properties.

### 5. 📜 Cryptographic Audit Certificates (`untrace cert`)
Computes SHA-256 hashes of original vs clean inputs, generating signed audit certificates (`UNTRACE-CERT-2026-XXXX`).

### 6. 🔥 Forensics Heatmap Visualizer (`untrace heatmap`)
Generates an interactive HTML visual heatmap rendering character offsets of zero-width bytes, em-dashes, and AI clichés.

### 7. 🌊 Spectral Frequency DCT Noise Injector (`--dct-jitter`)
Modulates 2D Discrete Cosine Transform (DCT) coefficients in image assets to disrupt spatial frequency watermarks (SynthID style).

---

## 💻 Command Line Interface (CLI)

```bash
# 1. Background Clipboard Daemon
untrace clipboard

# 2. Install Git Pre-Commit Hook & GitHub Action
untrace install-hook
untrace init-github-action

# 3. Generate SHA-256 Zero-Trust Clean Certificate
untrace cert document.txt -o audit_cert.json

# 4. Generate Visual Forensics Heatmap
untrace heatmap "Delve\u200b into crucial matters." -o heatmap.html

# 5. Clean text with Tone Personas
untrace clean-text "In order to achieve this, it is necessary to build." --tone tech-lead

# 6. Evaluate 4-Vector Stego Risk Matrix
untrace matrix document.ipynb

# 7. Launch Cyber-Stealth Web Dashboard
untrace ui
```

---

## 🧪 Testing Suite

Untrace AI includes a comprehensive test suite:

```bash
python3 -m unittest discover tests
```

---

## 📄 License

Distributed under the MIT License. See [`LICENSE`](LICENSE) for details.
