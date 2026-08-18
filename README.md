# Watermark Remover - Provenance Hygiene Toolkit & Claude Plugin

A high-performance provenance hygiene toolkit, CLI, Claude Skill, and Model Context Protocol (MCP) server designed to strip zero-width tracking marks, invisible Unicode characters, C2PA/EXIF metadata, and statistical watermarks.

---

## 🚀 Features

- **Unicode Hygiene**: Strips invisible zero-width spaces (`\u200B`, `\u200C`, `\u200D`, `\uFEFF`), direction overrides, soft hyphens (`\u00AD`), tag characters, and normalizes non-standard space codes (`\u00A0`).
- **Metadata & C2PA Removal**: Strips EXIF, C2PA signatures, XMP, and structural comments from PNG, JPEG, SVG, PDF, DOCX, HTML, and Markdown.
- **Statistical Perturbation**: Rephrases telltale AI vocabulary (e.g., *delve*, *testament*, *spearhead*, *crucial*) to defeat n-gram statistical AI detectors.
- **Claude Plugin & MCP Integration**: Works seamlessly with **Claude Desktop** (via MCP Server) and **Claude Code** (via Claude Skill).

---

## 📦 Installation

```bash
pip install -e .
```

---

## 🛠️ Usage

### 1. Command Line Interface (CLI)

**Clean text from stdin or direct argument:**
```bash
watermark-remover clean-text "Delve\u200b into the matter." --perturb
```

**Clean file metadata and zero-width characters:**
```bash
watermark-remover clean-file document.pdf
watermark-remover clean-file image.png
watermark-remover clean-file notes.md
```

### 2. Integration with Claude Desktop (MCP Server)

Add the following to your `claude_desktop_config.json` (located at `~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "watermark-remover": {
      "command": "python3",
      "args": [
        "-m",
        "watermark_remover.cli",
        "server"
      ]
    }
  }
}
```

Restart Claude Desktop. Claude will now have access to `sanitize_text`, `sanitize_file`, and `perturb_text` tools directly inside your chat sessions.

---

## 🧪 Running Tests

```bash
python3 -m pytest tests/
```
