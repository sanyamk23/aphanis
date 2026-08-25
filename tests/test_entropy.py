import unittest
from aphanis.entropy import EntropyAnalyzer


class TestEntropyAnalyzer(unittest.TestCase):

    def test_shannon_entropy_calculation(self):
        text = "Hello world! This is a test string."
        entropy = EntropyAnalyzer.calculate_shannon_entropy(text)
        self.assertIsInstance(entropy, float)
        self.assertGreater(entropy, 3.0)

    def test_ttr_calculation(self):
        repetitive = "the the the the word word"
        ttr_rep = EntropyAnalyzer.calculate_ttr(repetitive)
        self.assertEqual(ttr_rep, round(2 / 6, 4))

        varied = "The quick brown fox jumps over a lazy dog"
        ttr_var = EntropyAnalyzer.calculate_ttr(varied)
        self.assertEqual(ttr_var, 1.0)

    def test_analyze_report(self):
        sample_text = "Furthermore, we must delve into this crucial testament. It is paramount to note that tapestry of ideas."
        report = EntropyAnalyzer.analyze(sample_text)
        self.assertIn("shannon_entropy", report)
        self.assertIn("ttr", report)
        self.assertIn("predictability_score", report)
        self.assertIn("ai_likelihood", report)
        self.assertGreaterEqual(report["predictability_score"], 0.0)

    def test_empty_text_entropy(self):
        report = EntropyAnalyzer.analyze("")
        self.assertEqual(report["shannon_entropy"], 0.0)
        self.assertEqual(report["ai_likelihood"], "UNKNOWN")


if __name__ == "__main__":
    unittest.main()
