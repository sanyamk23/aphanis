import os
import tempfile
import unittest
from untrace.rules import RuleEngine


class TestRuleEngine(unittest.TestCase):

    def test_starter_rules_file_creation(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            rules_path = os.path.join(tmpdir, ".untracerules.json")
            msg = RuleEngine.create_starter_rules_file(rules_path)
            self.assertTrue(os.path.exists(rules_path))
            self.assertIn("Created starter rules", msg)

            engine = RuleEngine.from_file(rules_path)
            self.assertIn("custom_word_swaps", engine.rules_data)

    def test_custom_rule_application(self):
        rules_data = {
            "custom_zero_width_chars": ["\\u200B"],
            "custom_word_swaps": {
                "spearhead": "lead",
                "testament": "proof"
            },
            "custom_regex_replacements": [
                {
                    "pattern": "\\bIn summary,",
                    "replacement": "Overall,"
                }
            ],
            "custom_ai_comment_patterns": [
                "#\\s*AI-generated.*"
            ]
        }

        engine = RuleEngine(rules_data)
        dirty = "# AI-generated comment\nIn summary, we must spearhead this testament\u200b."
        cleaned = engine.apply_rules(dirty)

        self.assertNotIn("AI-generated comment", cleaned)
        self.assertNotIn("In summary,", cleaned)
        self.assertIn("Overall,", cleaned)
        self.assertNotIn("spearhead", cleaned)
        self.assertIn("lead", cleaned)
        self.assertNotIn("testament", cleaned)
        self.assertIn("proof", cleaned)
        self.assertNotIn("\u200b", cleaned)


if __name__ == "__main__":
    unittest.main()
