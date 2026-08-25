import os
import unittest
from pathlib import Path

from aphanis.autoinstall import AutoInstaller, auto_install_all


class TestAutoInstall(unittest.TestCase):

    def test_auto_installer(self):
        res = AutoInstaller.install_all()
        self.assertIn("claude_code", res)
        self.assertIn("antigravity_ide", res)
        self.assertIn("cursor_ide", res)

        self.assertTrue(Path(res["claude_code"]).exists())
        self.assertTrue(Path(res["antigravity_ide"]).exists())
        self.assertTrue(Path(res["cursor_ide"]).exists())


if __name__ == "__main__":
    unittest.main()
