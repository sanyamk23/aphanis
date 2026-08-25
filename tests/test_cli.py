import sys
import unittest
from unittest.mock import patch
from io import StringIO
from aphanis.cli import main


class TestCLI(unittest.TestCase):

    def test_cli_help(self):
        with patch.object(sys, 'argv', ['aphanis', '--help']):
            with self.assertRaises(SystemExit) as cm:
                with patch('sys.stdout', new=StringIO()) as fake_out:
                    main()
            self.assertEqual(cm.exception.code, 0)

    def test_cli_clean_text_inline(self):
        with patch.object(sys, 'argv', ['aphanis', 'clean-text', 'Delve\u200b into crucial matters', '--perturb']):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                main()
                output = fake_out.getvalue()
                self.assertNotIn('\u200b', output)
                self.assertNotIn('delve', output.lower())
                self.assertIn('explore', output.lower())

    def test_cli_check(self):
        with patch.object(sys, 'argv', ['aphanis', 'check', 'Delve\u200b into crucial matters — today.']):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                main()
                output = fake_out.getvalue()
                self.assertIn("4-VECTOR STEGO RISK MATRIX REPORT", output)
                self.assertIn("STATISTICAL ENTROPY READOUT", output)

    def test_cli_entropy(self):
        with patch.object(sys, 'argv', ['aphanis', 'entropy', 'This is a sample text for testing entropy calculation.']):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                main()
                output = fake_out.getvalue()
                self.assertIn("STATISTICAL ENTROPY REPORT", output)
                self.assertIn("Shannon Entropy:", output)


if __name__ == "__main__":
    unittest.main()
