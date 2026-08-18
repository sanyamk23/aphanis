import os
import tempfile
import unittest
from untrace.cleaner import UnicodeSanitizer, StatisticalPerturber, FileMetadataSanitizer, clean_text, clean_file


class TestUntraceAI(unittest.TestCase):

    def test_unicode_sanitizer_zero_width(self):
        # Text with embedded zero-width space (\u200b), soft hyphen (\u00ad), non-breaking space (\u00a0), variation selector (\ufe0f)
        dirty_text = "This\u200bis\u00ad a\u00a0test\ufeff string\ufe0f."
        cleaned = UnicodeSanitizer.clean(dirty_text)
        self.assertNotIn("\u200b", cleaned)
        self.assertNotIn("\u00ad", cleaned)
        self.assertNotIn("\ufeff", cleaned)
        self.assertNotIn("\ufe0f", cleaned)
        self.assertNotIn("\u00a0", cleaned)
        self.assertEqual(cleaned, "Thisis a test string.")

    def test_statistical_perturber(self):
        ai_text = "Furthermore, we must delve into this crucial testament and tapestry of ideas."
        perturbed = StatisticalPerturber.perturb(ai_text)
        self.assertNotIn("delve", perturbed.lower())
        self.assertNotIn("crucial", perturbed.lower())
        self.assertNotIn("testament", perturbed.lower())
        self.assertNotIn("tapestry", perturbed.lower())
        self.assertIn("explore", perturbed.lower())
        self.assertIn("important", perturbed.lower())

    def test_clean_text_helper(self):
        dirty_text = "Delve\u200b into crucial\ufeff matters."
        cleaned = clean_text(dirty_text, perturb_stats=True)
        self.assertNotIn("\u200b", cleaned)
        self.assertNotIn("\ufeff", cleaned)
        self.assertNotIn("delve", cleaned.lower())
        self.assertIn("explore", cleaned.lower())

    def test_file_cleaner_markdown(self):
        with tempfile.NamedTemporaryFile(suffix=".md", mode="w+", delete=False) as f:
            f.write("<!-- AI comment watermark -->\n# Title\u200b\nDelve into details.")
            temp_path = f.name

        try:
            success, msg = clean_file(temp_path)
            self.assertTrue(success)
            with open(temp_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertNotIn("<!-- AI comment watermark -->", content)
            self.assertNotIn("\u200b", content)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def test_file_cleaner_svg(self):
        svg_content = '<svg><metadata>C2PA Signature</metadata><!-- Comment --><g data-c2pa="true"></g></svg>'
        with tempfile.NamedTemporaryFile(suffix=".svg", mode="w+", delete=False) as f:
            f.write(svg_content)
            temp_path = f.name

        try:
            success, msg = clean_file(temp_path)
            self.assertTrue(success)
            with open(temp_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertNotIn("<metadata>", content)
            self.assertNotIn("<!-- Comment -->", content)
            self.assertNotIn('data-c2pa="true"', content)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)


if __name__ == "__main__":
    unittest.main()
