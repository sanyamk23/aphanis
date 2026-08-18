"""
Untrace AI - Jupyter Notebook (.ipynb) & Office (.pptx/.xlsx) Sanitizer.
Cleans zero-width watermarks, AI comments, and document metadata properties from notebooks and office files.
"""

import json
import os
import re
import zipfile
import tempfile
import shutil
from typing import Tuple

from untrace.cleaner import UnicodeSanitizer, AICommentSanitizer
from untrace.humanizer import HumanizerEngine


class OfficeSanitizer:
    """Sanitizes Jupyter Notebooks (.ipynb) and Office OpenXML documents (.pptx, .xlsx)."""

    @staticmethod
    def sanitize_ipynb(file_path: str, humanize: bool = True) -> Tuple[bool, str]:
        """Sanitizes Jupyter notebook cells, metadata, and zero-width tracking characters."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Strip notebook-level metadata
            if "metadata" in data:
                data["metadata"].pop("authors", None)
                data["metadata"].pop("signature", None)

            cells = data.get("cells", [])
            for cell in cells:
                cell_type = cell.get("cell_type")
                source = cell.get("source", [])

                if isinstance(source, list):
                    text = "".join(source)
                else:
                    text = str(source)

                cleaned = UnicodeSanitizer.clean(text)
                cleaned = AICommentSanitizer.clean(cleaned)
                if humanize and cell_type == "markdown":
                    cleaned = HumanizerEngine.humanize(cleaned)

                cell["source"] = [cleaned]

                # Clear cell metadata
                if "metadata" in cell:
                    cell["metadata"].pop("execution", None)

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=1)

            return True, f"Sanitized Jupyter Notebook: {file_path}"
        except Exception as e:
            return False, f"Failed to sanitize .ipynb file: {str(e)}"

    @staticmethod
    def sanitize_openxml_metadata(file_path: str) -> Tuple[bool, str]:
        """Clears core properties (author, title, subject, company, comments) from PPTX/XLSX zip structures."""
        try:
            temp_dir = tempfile.mkdtemp()
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)

            core_xml_path = os.path.join(temp_dir, 'docProps', 'core.xml')
            if os.path.exists(core_xml_path):
                with open(core_xml_path, 'r', encoding='utf-8', errors='ignore') as f:
                    xml_content = f.read()

                # Clean dc:creator, cp:lastModifiedBy, dc:title, dc:subject, cp:keywords
                xml_content = re.sub(r'<dc:creator>.*?</dc:creator>', '<dc:creator></dc:creator>', xml_content)
                xml_content = re.sub(r'<cp:lastModifiedBy>.*?</cp:lastModifiedBy>', '<cp:lastModifiedBy></cp:lastModifiedBy>', xml_content)
                xml_content = re.sub(r'<dc:title>.*?</dc:title>', '<dc:title></dc:title>', xml_content)
                xml_content = re.sub(r'<dc:subject>.*?</dc:subject>', '<dc:subject></dc:subject>', xml_content)

                with open(core_xml_path, 'w', encoding='utf-8') as f:
                    f.write(xml_content)

            # Re-zip
            shutil.make_archive(file_path.replace('.pptx', '').replace('.xlsx', ''), 'zip', temp_dir)
            zip_out = file_path.replace('.pptx', '').replace('.xlsx', '') + '.zip'
            if os.path.exists(zip_out):
                shutil.move(zip_out, file_path)

            shutil.rmtree(temp_dir)
            return True, f"Cleared OpenXML core properties & metadata: {file_path}"
        except Exception as e:
            return False, f"Failed to sanitize Office file metadata: {str(e)}"
