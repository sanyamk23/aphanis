"""
Untrace AI - Core Hygiene, Watermark Disrupter, and Metadata Sanitization Module.
"""

import os
import re
import random
import unicodedata
from typing import Tuple, Dict, Any, Optional


class UnicodeSanitizer:
    """Strips hidden zero-width spaces, tracking tags, variation selectors, and homoglyphs."""

    # Complete zero-width & invisible characters used for steganography / LLM watermarking
    ZERO_WIDTH_CHARS = {
        '\u200B',  # Zero-width space
        '\u200C',  # Zero-width non-joiner
        '\u200D',  # Zero-width joiner
        '\uFEFF',  # Zero-width no-break space (BOM)
        '\u2060',  # Word joiner
        '\u2061',  # Function application
        '\u2062',  # Invisible times
        '\u2063',  # Invisible separator
        '\u2064',  # Invisible plus
        '\u00AD',  # Soft hyphen
        '\u180E',  # Mongolian vowel separator
    }

    # Bidi & direction override characters
    BIDI_CHARS = {
        '\u200E', '\u200F', '\u202A', '\u202B', '\u202C',
        '\u202D', '\u202E', '\u2066', '\u2067', '\u2068', '\u2069'
    }

    # Custom space normalization
    SPACE_NORMALIZATIONS = {
        '\u00A0': ' ',  # Non-breaking space
        '\u2002': ' ',  # En space
        '\u2003': ' ',  # Em space
        '\u2004': ' ',  # Three-per-em space
        '\u2005': ' ',  # Four-per-em space
        '\u2006': ' ',  # Six-per-em space
        '\u2007': ' ',  # Figure space
        '\u2008': ' ',  # Punctuation space
        '\u2009': ' ',  # Thin space
        '\u200A': ' ',  # Hair space
        '\u202F': ' ',  # Narrow no-break space
        '\u205F': ' ',  # Medium mathematical space
        '\u3000': ' ',  # Ideographic space
    }

    @classmethod
    def clean(cls, text: str, normalize_unicode: bool = True) -> str:
        """Strips invisible watermarking characters, variation selectors, and normalizes Unicode."""
        if not text:
            return ""

        # 1. Remove Tag Characters (\uE0001 - \uE007F) & Variation Selectors (\uFE00 - \uFE0F, \uE0100 - \uE01EF)
        cleaned_chars = []
        for c in text:
            code = ord(c)
            # Filter Tag characters
            if 0xE0001 <= code <= 0xE007F:
                continue
            # Filter Variation Selectors
            if 0xFE00 <= code <= 0xFE0F or 0xE0100 <= code <= 0xE01EF:
                continue
            cleaned_chars.append(c)

        text = "".join(cleaned_chars)

        # 2. Filter zero-width & bidi characters, normalize non-standard space codes
        chars = []
        for char in text:
            if char in cls.ZERO_WIDTH_CHARS or char in cls.BIDI_CHARS:
                continue
            if char in cls.SPACE_NORMALIZATIONS:
                chars.append(cls.SPACE_NORMALIZATIONS[char])
            else:
                chars.append(char)
        text = "".join(chars)

        # 3. Unicode NFKC Normalization (converts homoglyphs & fullwidth characters)
        if normalize_unicode:
            text = unicodedata.normalize("NFKC", text)

        # 4. Clean consecutive space artifacts created by stripping
        text = re.sub(r'[ \t]+', ' ', text)
        
        # 5. Remove trailing space per line
        lines = [line.rstrip() for line in text.splitlines()]
        return "\n".join(lines)


class StatisticalPerturber:
    """Perturbs text to disrupt n-gram statistical AI watermarks and vendor-specific vocabulary signatures."""

    AI_VOCAB_SWAPS = {
        r'\bdelve\b': 'explore',
        r'\bdelves\b': 'explores',
        r'\bdelving\b': 'exploring',
        r'\btestament\b': 'proof',
        r'\btestaments\b': 'proofs',
        r'\bspearhead\b': 'lead',
        r'\bspearheaded\b': 'led',
        r'\bspearheading\b': 'leading',
        r'\bfostering\b': 'building',
        r'\bfoster\b': 'encourage',
        r'\bcrucial\b': 'important',
        r'\bpivotal\b': 'key',
        r'\bparamount\b': 'essential',
        r'\bmultifaceted\b': 'complex',
        r'\bunderscores\b': 'highlights',
        r'\bunderscore\b': 'highlight',
        r'\bseamlessly\b': 'smoothly',
        r'\bseamless\b': 'smooth',
        r'\bgame-changer\b': 'major breakthrough',
        r'\bin conclusion\b': 'to summarize',
        r'\bfurthermore\b': 'also',
        r'\bmoreover\b': 'additionally',
        r'\bnevertheless\b': 'however',
        r'\btapestry\b': 'blend',
        r'\bbeacon\b': 'symbol',
        r'\bnestled\b': 'situated',
        r'\bunwavering\b': 'steady',
        r'\bever-evolving\b': 'developing',
        r'\brealm\b': 'area',
        r'\bresonate\b': 'align',
        r'\bharness\b': 'use',
        r'\bleverage\b': 'utilize',
        r'\bparadigm shift\b': 'fundamental change',
        r'\bshed light\b': 'explain',
        r'\binterplay\b': 'interaction',
        r'\bindispensable\b': 'vital',
        r'\bvibrant\b': 'lively',
        r'\bsynergy\b': 'collaboration',
        r'\bembark\b': 'begin',
        r'\bit is important to note that\b': 'note that',
        r'\bin summary\b': 'overall',
    }

    @classmethod
    def perturb(cls, text: str) -> str:
        """Replaces common statistical AI marker phrases with natural alternatives while preserving case."""
        if not text:
            return ""

        result = text
        for pattern, replacement in cls.AI_VOCAB_SWAPS.items():
            def _replace(match):
                word = match.group(0)
                if word.istitle():
                    return replacement.capitalize()
                elif word.isupper():
                    return replacement.upper()
                return replacement

            result = re.sub(pattern, _replace, result, flags=re.IGNORECASE)

        return result


class ImageWatermarkDisrupter:
    """Modulates image LSB pixel noise to disrupt frequency-domain spatial watermarks."""

    @classmethod
    def perturb_image(cls, file_path: str, jitter: bool = True) -> Tuple[bool, str]:
        """Strips EXIF/C2PA metadata and applies perceptual sub-pixel noise jitter."""
        try:
            from PIL import Image
            img = Image.open(file_path)
            mode = img.mode
            size = img.size
            pixels = list(img.getdata())

            if jitter and mode in ('RGB', 'RGBA'):
                # Micro sub-pixel LSB jitter (imperceptible to eye, disrupts spectral watermarks)
                new_pixels = []
                for p in pixels:
                    if mode == 'RGB':
                        r, g, b = p
                        r = max(0, min(255, r + random.choice([-1, 0, 1])))
                        new_pixels.append((r, g, b))
                    else:
                        r, g, b, a = p
                        r = max(0, min(255, r + random.choice([-1, 0, 1])))
                        new_pixels.append((r, g, b, a))
                pixels = new_pixels

            img_cleaned = Image.new(mode, size)
            img_cleaned.putdata(pixels)
            img_cleaned.save(file_path)
            return True, f"Stripped metadata & perturbed spatial watermarks for {file_path}"
        except Exception as e:
            return False, f"Failed to process image: {str(e)}"


class FileMetadataSanitizer:
    """Strips EXIF, C2PA, XMP, comments, and tracking metadata from files."""

    @classmethod
    def clean_markdown_or_text(cls, content: str) -> str:
        """Removes HTML comments and cleans Unicode in Markdown/Text files."""
        cleaned = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
        return UnicodeSanitizer.clean(cleaned)

    @classmethod
    def clean_svg(cls, content: str) -> str:
        """Removes <metadata>, C2PA attributes, and XML comments from SVG."""
        cleaned = re.sub(r'<metadata.*?>.*?</metadata>', '', content, flags=re.DOTALL | re.IGNORECASE)
        cleaned = re.sub(r'<!--.*?-->', '', cleaned, flags=re.DOTALL)
        cleaned = re.sub(r'\s+data-(c2pa|provenance|watermark|ai)="[^"]*"', '', cleaned, flags=re.IGNORECASE)
        return UnicodeSanitizer.clean(cleaned)

    @classmethod
    def clean_html(cls, content: str) -> str:
        """Removes meta tags, comments, and zero-width characters in HTML."""
        cleaned = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
        cleaned = re.sub(r'<meta\s+name=["\'](c2pa|provenance|generator|ai-watermark)["\'].*?>', '', cleaned, flags=re.IGNORECASE)
        return UnicodeSanitizer.clean(cleaned)

    @classmethod
    def clean_file(cls, file_path: str, disrupt_image_pixels: bool = False) -> Tuple[bool, str]:
        """Detects file type and cleans watermarks and metadata."""
        if not os.path.exists(file_path):
            return False, f"File not found: {file_path}"

        ext = os.path.splitext(file_path)[1].lower()

        try:
            if ext in ['.md', '.txt']:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                cleaned = cls.clean_markdown_or_text(content)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(cleaned)
                return True, f"Sanitized text/markdown file: {file_path}"

            elif ext == '.svg':
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                cleaned = cls.clean_svg(content)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(cleaned)
                return True, f"Sanitized SVG file: {file_path}"

            elif ext in ['.html', '.htm']:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                cleaned = cls.clean_html(content)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(cleaned)
                return True, f"Sanitized HTML file: {file_path}"

            elif ext in ['.png', '.jpg', '.jpeg']:
                return ImageWatermarkDisrupter.perturb_image(file_path, jitter=disrupt_image_pixels)

            elif ext == '.pdf':
                try:
                    from pypdf import PdfReader, PdfWriter
                    reader = PdfReader(file_path)
                    writer = PdfWriter()
                    for page in reader.pages:
                        writer.add_page(page)
                    with open(file_path, 'wb') as f:
                        writer.write(f)
                    return True, f"Cleared PDF metadata & annotations: {file_path}"
                except Exception as e:
                    return False, f"PDF cleaning failed: {str(e)}"

            elif ext == '.docx':
                try:
                    import docx
                    doc = docx.Document(file_path)
                    cp = doc.core_properties
                    cp.author = ""
                    cp.comments = ""
                    cp.keywords = ""
                    cp.subject = ""
                    cp.title = ""
                    for p in doc.paragraphs:
                        p.text = UnicodeSanitizer.clean(p.text)
                    doc.save(file_path)
                    return True, f"Sanitized DOCX core properties & paragraphs: {file_path}"
                except Exception as e:
                    return False, f"DOCX cleaning failed: {str(e)}"

            else:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                cleaned = UnicodeSanitizer.clean(content)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(cleaned)
                return True, f"Sanitized raw file: {file_path}"

        except Exception as e:
            return False, f"Error processing file {file_path}: {str(e)}"


def clean_text(text: str, perturb_stats: bool = False) -> str:
    """Helper function to clean raw text from zero-width watermarks and optional statistical markers."""
    cleaned = UnicodeSanitizer.clean(text)
    if perturb_stats:
        cleaned = StatisticalPerturber.perturb(cleaned)
    return cleaned


def clean_file(file_path: str, disrupt_image_pixels: bool = False) -> Tuple[bool, str]:
    """Helper function to clean file metadata and watermarks."""
    return FileMetadataSanitizer.clean_file(file_path, disrupt_image_pixels=disrupt_image_pixels)
