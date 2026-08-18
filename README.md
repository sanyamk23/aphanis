<div align="center">

# 🛡️ UNTRACE AI :: Humanizer & Stealth Engine

```text
  _   _ _  _ _____ ___    _   ___ ___   _   ___ 
 | | | | \| |_   _| _ \  /_\ / __| __| /_\ |_ _|
 | |_| | .` | | | |   / / _ \ (__| _| / _ \ | | 
  \___/|_|\_| |_| |_|_\/_/ \_\___|___/_/ \_\___|
```

### *The Enterprise Zero-Trust AI Provenance Firewall & Automatic Humanizer Engine*

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg?style=for-the-badge&logo=python)](https://python.org)
[![MCP Server](https://img.shields.io/badge/MCP-Firewall%20%26%20Humanizer-000000.svg?style=for-the-badge&logo=anthropic)](https://modelcontextprotocol.io)
[![Claude Skill](https://img.shields.io/badge/Claude%20Code-Humanizer--Skill-7A1FA2.svg?style=for-the-badge&logo=anthropic)](https://anthropic.com)
[![License](https://img.shields.io/badge/license-MIT-green.svg?style=for-the-badge)](LICENSE)

<br/>

[Automatic Humanizer](#-automatic-humanizer-engine) •
[4-Vector Risk Matrix](#-4-vector-stego-risk-matrix) •
[Stealth Presets](#-stealth-profile-presets) •
[Cyber-Stealth Dashboard](#-cyber-stealth-dashboard) •
[Quick Start](#-quick-start) •
[Claude Integrations](#-claude-desktop--claude-code-integrations)

</div>

---

## ⚡ What is Untrace AI?

**Untrace AI** is an enterprise-grade **Zero-Trust AI Provenance Firewall & Automatic Humanizer Engine**. It neutralizes AI provenance signals, zero-width steganography, C2PA/EXIF metadata, em-dash signatures, and **automatically rewrites text into an authentic, natural human tone** (synthesizing contractions, removing passive filler phrases, and balancing sentence cadence).

---

## ✍️ Automatic Humanizer Engine

By default, all content processed through Untrace AI is **automatically humanized**:

### Humanizer Transformations:
- **Contraction Synthesizer**: Converts rigid LLM expansions (*"it is"*, *"cannot"*, *"we have"*, *"do not"*) into natural human contractions (*"it's"*, *"can't"*, *"we've"*, *"don't"*).
- **Passive Filler Reducer**: Replaces 50+ robotic LLM filler phrases (*"in order to"*, *"it is important to note that"*, *"due to the fact that"*, *"at this point in time"*) with concise active phrasing.
- **Organic Transition Variator**: Replaces rigid transitions (*"furthermore"*, *"moreover"*, *"consequently"*, *"nevertheless"*) with natural human connectors.
- **Sentence Burstiness & Rhythm**: Varies sentence structure to eliminate uniform AI token cadence.

```bash
# Humanize text inline or from file
untrace humanize "In order to succeed, it is important to note that we cannot fail."
# Output: "To succeed, note that we can't fail."
```

---

## 📊 4-Vector Stego Risk Matrix

Untrace AI evaluates content against 4 independent provenance threat vectors:

```text
🛡️ --- 4-VECTOR STEGO RISK MATRIX REPORT --- 🛡️
PROVENANCE RISK LEVEL : ZERO_TRUST_CLEAN
OVERALL CLEAN SCORE   : 100.0/100

[VECTOR 1] Unicode Steganography  :   0.0% Risk [CLEAN] (0 hidden bytes)
[VECTOR 2] Statistical Model Risk :   0.0% Risk [CLEAN] (0 clichés, 0 em-dashes)
[VECTOR 3] Metadata & Containers  :   0.0% Risk [CLEAN] (0 AI comments)
[VECTOR 4] Spatial Frequency      :   0.0% Risk [CLEAN]
```

---

## ⚙️ Stealth Profile Presets

| Stealth Preset | Description | Features Enabled |
| :--- | :--- | :--- |
| 🛡️ `PARANOID` | **Maximum Defense** (Default) | Humanization, Zero-width, 120+ telltale swaps, em-dash, LSB jitter, metadata purge, rules |
| ⚡ `AGGRESSIVE` | **High Protection** | Humanization, Zero-width, statistical rephrasing, LSB jitter, metadata purge |
| 🔒 `STANDARD` | **Balanced Hygiene** | Humanization, Zero-width, em-dash/smart quote normalization, metadata purge |
| 🧼 `MINIMAL` | **Light Scrubbing** | Zero-width character stripping only |

---

## 🖥️ Cyber-Stealth Dashboard (`untrace ui`)

Launch the local visual visualizer featuring live side-by-side diff inspection, 4-Vector risk gauges, and automatic Humanized output:

```bash
untrace dashboard
# or
untrace ui --port 8080
```

---

## 📦 Quick Start

### Installation

```bash
git clone https://github.com/sanyamk23/untrace-ai.git
cd untrace-ai
pip install -e .
```

---

## 💻 Command Line Interface (CLI)

```bash
# 1. Clean & Humanize inline text (humanized by default)
untrace clean-text "Furthermore, it is necessary to delve into this crucial matter."

# 2. Dedicated Humanize Command
untrace humanize "In order to build this, it is essential to proceed."

# 3. Clean without tone humanization
untrace clean-text "Furthermore, it is necessary to delve into this." --no-humanize

# 4. Evaluate 4-Vector Stego Risk Matrix
untrace matrix "Delve\u200b into crucial\ufeff matters — today."

# 5. Real-time Folder Watcher
untrace watch .
```

---

## 🐍 Python SDK Usage

```python
from untrace import clean_text, humanize_text, StegoRiskMatrix

# 1. Automatically clean and humanize string
clean_humanized = clean_text("Furthermore, it is important to note that we cannot fail.")
print(clean_humanized)
# Output: "Also, note that we can't fail."

# 2. Standalone Humanizer Engine
human = humanize_text("In order to achieve this, it is necessary to move forward.")
print(human)
# Output: "To achieve this, note that we need to move next."
```

---

## 📄 License

Distributed under the MIT License. See [`LICENSE`](LICENSE) for details.
