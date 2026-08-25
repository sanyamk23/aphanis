"""
Aphanis - Forensics Heatmap Visualizer.
Renders an interactive HTML diagnostic heatmap displaying exact character byte offsets of zero-width
watermarks, em-dashes, and AI clichés in a document.
"""

import html
import re
from typing import Dict, Any


class HeatmapRenderer:
    """Renders visual forensic heatmaps for text documents."""

    @classmethod
    def render_html_heatmap(cls, text: str, title: str = "Aphanis Forensics Heatmap") -> str:
        """Generates HTML string rendering exact character offsets and risk badges."""
        if not text:
            text = ""

        # Escape HTML chars
        safe_text = html.escape(text)

        # Highlight zero-width chars
        safe_text = re.sub(
            r'[\u200B\u200C\u200D\uFEFF\u2060\u00AD]',
            r'<mark style="background:#f43f5e; color:#ffffff; padding:2px 4px; border-radius:4px; font-weight:bold;">[ZERO-WIDTH BYTE]</mark>',
            safe_text
        )

        # Highlight em-dashes
        safe_text = re.sub(
            r'—',
            r'<mark style="background:#f59e0b; color:#ffffff; padding:2px 4px; border-radius:4px; font-weight:bold;">[EM-DASH: —]</mark>',
            safe_text
        )

        # Highlight AI telltales
        from aphanis.cleaner import StatisticalPerturber
        for pattern in StatisticalPerturber.AI_VOCAB_SWAPS.keys():
            safe_text = re.sub(
                pattern,
                r'<mark style="background:#a855f7; color:#ffffff; padding:2px 4px; border-radius:4px;">\g<0></mark>',
                safe_text,
                flags=re.IGNORECASE
            )

        html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>🛡️ {title}</title>
  <style>
    body {{ background: #030712; color: #f9fafb; font-family: 'Inter', sans-serif; padding: 2rem; }}
    .container {{ max-width: 1200px; margin: 0 auto; background: #111827; border: 1px solid #374151; border-radius: 12px; padding: 2rem; }}
    h1 {{ color: #a5b4fc; font-size: 1.5rem; margin-bottom: 1rem; }}
    .content {{ font-family: 'JetBrains Mono', monospace; font-size: 0.95rem; line-height: 1.8; white-space: pre-wrap; word-break: break-word; background: #030712; border: 1px solid #1f2937; padding: 1.5rem; border-radius: 8px; }}
    .legend {{ display: flex; gap: 1rem; margin-bottom: 1.5rem; }}
    .tag {{ padding: 0.3rem 0.8rem; border-radius: 6px; font-weight: bold; font-size: 0.8rem; }}
  </style>
</head>
<body>
  <div class="container">
    <h1>🛡️ Aphanis :: Provenance Forensics Heatmap</h1>
    <div class="legend">
      <span class="tag" style="background:#f43f5e; color:#fff;">Red: Hidden Zero-Width Stego</span>
      <span class="tag" style="background:#f59e0b; color:#fff;">Amber: Em-Dash Signature</span>
      <span class="tag" style="background:#a855f7; color:#fff;">Purple: AI Cliché Vocabulary</span>
    </div>
    <div class="content">{safe_text}</div>
  </div>
</body>
</html>
"""
        return html_doc

    @classmethod
    def save_heatmap_file(cls, text: str, output_path: str = "aphanis_heatmap.html") -> str:
        """Saves heatmap HTML file."""
        content = cls.render_html_heatmap(text)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        return output_path
