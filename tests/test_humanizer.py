import unittest
from untrace.humanizer import HumanizerEngine, humanize_text
from untrace.cleaner import clean_text


class TestHumanizerEngine(unittest.TestCase):

    def test_contractions_synthesis(self):
        robotic_text = "It is clear that we cannot proceed and they are not ready."
        humanized = HumanizerEngine.humanize(robotic_text)
        self.assertIn("It's", humanized)
        self.assertIn("can't", humanized)
        self.assertIn("aren't", humanized)

    def test_filler_phrase_reduction(self):
        robotic_text = "In order to succeed, it is important to note that we must act."
        humanized = HumanizerEngine.humanize(robotic_text)
        self.assertNotIn("In order to", humanized)
        self.assertIn("To succeed", humanized)
        self.assertNotIn("it is important to note that", humanized.lower())

    def test_default_clean_text_humanization(self):
        robotic = "Delve\u200b into matters. Furthermore, it is important to note that we cannot fail."
        cleaned = clean_text(robotic, perturb_stats=True, humanize=True)
        self.assertNotIn("\u200b", cleaned)
        self.assertNotIn("delve", cleaned.lower())
        self.assertIn("can't", cleaned)
        self.assertNotIn("in order to", cleaned.lower())

    def test_no_humanize_flag(self):
        robotic = "It is clear that we cannot fail."
        cleaned_raw = clean_text(robotic, humanize=False)
        self.assertIn("cannot", cleaned_raw)


if __name__ == "__main__":
    unittest.main()
