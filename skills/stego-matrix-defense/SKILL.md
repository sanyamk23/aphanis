---
name: stego-matrix-defense
description: Guidance on auditing and mitigating 4-Vector Stego Risks (Unicode invisible watermarks, statistical n-grams, comment metadata, spatial frequency) and analyzing Shannon entropy.
---

# Stego Matrix Defense Skill

Use this skill to analyze and evaluate steganographic risk vectors across code, text, image, and document assets.

## The 4 Stego Vectors

1. **Vector 1: Unicode Invisible Watermarks**
   - Detects hidden ZWSP (`\u200B`), non-joiner (`\u200C`), joiner (`\u200D`), BOM (`\uFEFF`), and variation selectors.
   - Cleans by stripping non-printable zero-width unicode ranges.

2. **Vector 2: Statistical N-Gram & Model Markers**
   - Measures Shannon entropy (target: $4.5$ - $5.5$ bits/char) and Type-Token Ratio.
   - Evaluates phrase frequencies against known LLM output profiles.

3. **Vector 3: Container & File Metadata**
   - Audits source code for auto-generated AI header tags, EXIF tags, and C2PA signatures.

4. **Vector 4: Spatial Frequency & Sub-Pixel Dither**
   - Applies Discrete Cosine Transform (DCT) noise modulation to PNG/JPEG image assets to disrupt SynthID-style frequency watermarks.
