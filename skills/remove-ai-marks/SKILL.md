---
name: remove-ai-marks
description: Strips zero-width tracking marks, invisible Unicode characters, C2PA/EXIF metadata, and statistical watermarks from Claude's text and generated files.
---

# Remove AI Marks Skill

This skill ensures that all text outputs, generated code comments, and exported files are thoroughly sanitized of invisible AI watermarks, zero-width tracking characters, metadata signatures, and telltale statistical n-gram patterns.

## Instructions for Claude

When this skill is active or when generating text/documents for the user:

### 1. Unicode Hygiene Rules
- **Never insert zero-width characters**: Strictly avoid `\u200B` (Zero-Width Space), `\u200C` (Zero-Width Non-Joiner), `\u200D` (Zero-Width Joiner), `\uFEFF` (BOM), `\u2060` (Word Joiner), `\u00AD` (Soft Hyphen), and bidi direction overrides (`\u200E`, `\u200F`, `\u202A`..`\u202E`).
- **Use Standard Spaces**: Use canonical ASCII spaces (`\u0020`). Never insert non-breaking spaces (`\u00A0`), thin spaces (`\u2009`), or figure spaces.
- **Normalize Unicode**: Keep output in standard NFKC Unicode normalization form.

### 2. Statistical Vocabulary Hygiene
- Avoid repetitive or cliché AI transition words that signal automated generation:
  - Replace "delve" -> "explore" or "examine"
  - Replace "testament" -> "proof" or "demonstration"
  - Replace "spearhead" -> "lead" or "drive"
  - Replace "crucial" / "pivotal" / "paramount" -> "important" or "key"
  - Replace "multifaceted" -> "complex" or "varied"
  - Replace "seamlessly" -> "smoothly"
  - Replace "In conclusion" -> "To summarize" or omit

### 3. File & Metadata Hygiene
- If creating or processing files (PNG, SVG, PDF, DOCX, HTML, Markdown), execute the `watermark-remover clean-file` tool or invoke the `sanitize_file` MCP tool to strip all C2PA, EXIF, XMP, and XML comments before delivering the file to the user.

### 4. MCP Server Integration
If connected to the `WatermarkRemover` MCP Server:
- Use `sanitize_text` on raw input/output strings.
- Use `sanitize_file` on saved artifacts.
- Use `perturb_text` when rewriting content to defeat detector classifiers.
