import os
import tempfile
import unittest

from untrace.cert import AuditCertificateGenerator
from untrace.heatmap import HeatmapRenderer
from untrace.hooks import HookInstaller
from untrace.office import OfficeSanitizer
from untrace.humanizer import HumanizerEngine


class TestEnterpriseFeatures(unittest.TestCase):

    def test_audit_certificate_generation(self):
        raw_text = "Delve\u200b into crucial matters — today."
        clean_text = "Explore into important matters - today."
        cert = AuditCertificateGenerator.generate_certificate(raw_text, clean_text)

        self.assertIn("certificate_id", cert)
        self.assertTrue(cert["certificate_id"].startswith("UNTRACE-CERT-"))
        self.assertIn("sha256_raw_input", cert["hashes"])
        self.assertIn("sha256_clean_output", cert["hashes"])

    def test_heatmap_rendering(self):
        dirty_text = "Delve\u200b into crucial matters — today."
        html_out = HeatmapRenderer.render_html_heatmap(dirty_text)

        self.assertIn("[ZERO-WIDTH BYTE]", html_out)
        self.assertIn("[EM-DASH: —]", html_out)

    def test_git_hook_script_generation(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            os.makedirs(os.path.join(tmpdir, ".git", "hooks"))
            msg = HookInstaller.install_git_hook(tmpdir)
            self.assertIn("Successfully installed", msg)
            self.assertTrue(os.path.exists(os.path.join(tmpdir, ".git", "hooks", "pre-commit")))

    def test_github_action_generation(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            msg = HookInstaller.generate_github_action(tmpdir)
            self.assertIn("Successfully generated", msg)
            self.assertTrue(os.path.exists(os.path.join(tmpdir, ".github", "workflows", "untrace-hygiene.yml")))

    def test_tone_personas(self):
        text = "Utilize this tool in order to build."
        tech_lead = HumanizerEngine.humanize(text, tone="tech-lead")
        self.assertIn("use", tech_lead)
        self.assertNotIn("utilize", tech_lead)


if __name__ == "__main__":
    unittest.main()
