"""Core watermark cleaning and provenance hygiene module."""

import os
import re
import unicodedata
from typing import Union, Tuple, Dict, Any


class UnicodeSanitizer:
    """Sanitizes text by removing hidden zero-width spaces, tracking markers, and homoglyphs."""

    # Zero-width & invisible characters commonly used for steganography / watermarking
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
        """Strips invisible watermarking characters and normalizes Unicode."""
        if not text:
            return ""

        # 1. Remove Tag Characters (\uE0001 - \uE007F) used for invisible tracking payloads
        cleaned = [c for c in text if not (0xE0001 <= ord(c) <= 0xE007F)]
        text = "".join(cleaned)

        # 2. Remove zero-width & bidi characters
        chars = []
        for char in text:
            if char in cls.ZERO_WIDTH_CHARS or char in cls.BIDI_CHARS:
                continue
            if char in cls.SPACE_NORMALIZATIONS:
                chars.append(cls.SPACE_NORMALIZATIONS[char])
            else:
                chars.append(char)
        text = "".join(chars)

        # 3. Unicode NFKC Normalization (converts homoglyphs & fullwidth chars to standard ASCII/Unicode)
        if normalize_unicode:
            text = unicodedata.normalize("NFKC", text)

        # 4. Clean consecutive duplicate spaces created by stripping
        text = re.sub(r'[ \t]+', ' ', text)
        
        # 5. Remove trailing space per line
        lines = [line.rstrip() for line in text.splitlines()]
        return "\n".join(lines)


class StatisticalPerturber:
    """Perturbs text to disrupt statistical n-gram AI watermarks and vendor-specific vocabulary signatures."""

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
    }

    @classmethod
    def perturb(cls, text: str) -> str:
        """Replaces common statistical AI marker phrases with natural alternatives."""
        if not text:
            return ""

        result = text
        for pattern, replacement in cls.AI_VOCAB_SWAPS.items():
            # Match case insensitive while preserving capitalization if starting with uppercase
            def _replace(match):
                word = match.group(0)
                if word.istitle():
                    return replacement.capitalize()
                elif word.isupper():
                    return replacement.upper()
                return replacement

            result = re.sub(pattern, _replace, result, flags=re.IGNORECASE)

        return result


class FileMetadataSanitizer:
    """Strips EXIF, C2PA, XMP, and structural comments from files."""

    @classmethod
    def clean_markdown_or_text(cls, content: str) -> str:
        """Removes HTML comments and cleans Unicode in Markdown/Text files."""
        # Strip HTML comments <!-- ... -->
        cleaned = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
        return UnicodeSanitizer.clean(cleaned)

    @classmethod
    def clean_svg(cls, content: str) -> str:
        """Removes <metadata>, C2PA attributes, and XML comments from SVG."""
        # Strip <metadata>...</metadata> blocks
        cleaned = re.sub(r'<metadata.*?>.*?</metadata>', '', content, flags=re.DOTALL | re.IGNORECASE)
        # Strip comments
        cleaned = re.sub(r'<!--.*?-->', '', cleaned, flags=re.DOTALL)
        # Strip c2pa or custom tracking data attributes
        cleaned = re.sub(r'\s+data-(c2pa|provenance|watermark|ai)="[^"]*"', '', cleaned, flags=re.IGNORECASE)
        return UnicodeSanitizer.clean(cleaned)

    @classmethod
    def clean_html(cls, content: str) -> str:
        """Removes meta tags, comments, and zero-width characters in HTML."""
        # Strip comments
        cleaned = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
        # Strip C2PA/AI meta generator tags
        cleaned = re.sub(r'<meta\s+name=["\'](c2pa|provenance|generator|ai-watermark)["\'].*?>', '', cleaned, flags=re.IGNORECASE)
        return UnicodeSanitizer.clean(cleaned)

    @classmethod
    def clean_image(cls, file_path: str) -> Tuple[bool, str]:
        """Strips EXIF and metadata chunks (including C2PA) from PNG/JPEG image files."""
        try:
            from PIL import Image
            img = Image.open(file_path)
            data = list(img.getdata())
            img_cleaned = Image.new(img.mode, img.size)
            img_cleaned.putdata(data)
            img_cleaned.save(file_path)
            return True, f"Metadata stripped successfully from {file_path}"
        except Exception as e:
            return False, f"Failed to strip image metadata: {str(e)}"

    @classmethod
    def clean_file(cls, file_path: str) -> Tuple[bool, str]:
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
                return True, f"Cleaned text/markdown file: {file_path}"

            elif ext == '.svg':
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                cleaned = cls.clean_svg(content)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(cleaned)
                return True, f"Cleaned SVG metadata and comments: {file_path}"

            elif ext in ['.html', '.htm']:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                cleaned = cls.clean_html(content)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(cleaned)
                return True, f"Cleaned HTML metadata: {file_path}"

            elif ext in ['.png', '.jpg', '.jpeg']:
                return cls.clean_image(file_path)

            elif ext == '.pdf':
                try:
                    from pypdf import PdfReader, PdfWriter
                    reader = PdfReader(file_path)
                    writer = PdfWriter()
                    for page in reader.pages:
                        writer.add_page(page)
                    # Exclude metadata / annotations payload
                    with open(file_path, 'wb') as f:
                        writer.write(f)
                    return True, f"Cleared PDF metadata: {file_path}"
                except Exception as e:
                    return False, f"PDF cleaning failed: {str(e)}"

            elif ext == '.docx':
                try:
                    import docx
                    doc = docx.Document(file_path)
                    # Clean core properties
                    cp = doc.core_properties
                    cp.author = ""
                    cp.comments = ""
                    cp.keywords = ""
                    cp.subject = ""
                    cp.title = ""
                    # Clean text inside paragraphs
                    for p in doc.paragraphs:
                        p.text = UnicodeSanitizer.clean(p.text)
                    doc.save(file_path)
                    return True, f"Cleaned DOCX file metadata and Unicode: {file_path}"
                except Exception as e:
                    return False, f"DOCX cleaning failed: {str(e)}"

            else:
                # Fallback text cleaner
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                cleaned = UnicodeSanitizer.clean(content)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(cleaned)
                return True, f"Cleaned raw file: {file_path}"

        except Exception as e:
            return False, f"Error processing file {file_path}: {str(e)}"


def clean_text(text: str, perturb_stats: bool = False) -> str:
    """Helper function to clean raw text from zero-width watermarks and optional statistical markers."""
    cleaned = UnicodeSanitizer.clean(text)
    if perturb_stats:
        cleaned = StatisticalPerturber.perturb(cleaned)
    return cleaned


def clean_file(file_path: str) -> Tuple[bool, str]:
    """Helper function to clean file metadata and watermarks."""
    return FileMetadataSanitizer.clean_file(file_path)
