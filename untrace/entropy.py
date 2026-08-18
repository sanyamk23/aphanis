"""
Untrace AI - Statistical Entropy & Text Uniformity Analyzer.
Calculates Shannon entropy, Type-Token Ratio (TTR), and text predictability metrics
to detect AI-generated token distribution patterns vs natural human writing.
"""

import math
import re
from typing import Dict, Any, List


class EntropyAnalyzer:
    """Calculates statistical entropy, lexical diversity, and predictability heuristics."""

    @staticmethod
    def calculate_shannon_entropy(text: str) -> float:
        """
        Calculates Shannon entropy in bits per character.
        Human language typically ranges between 3.8 and 4.8 bits/char for English text.
        """
        if not text:
            return 0.0

        char_counts: Dict[str, int] = {}
        for char in text:
            char_counts[char] = char_counts.get(char, 0) + 1

        length = len(text)
        entropy = 0.0
        for count in char_counts.values():
            probability = count / length
            entropy -= probability * math.log2(probability)

        return round(entropy, 4)

    @staticmethod
    def calculate_ttr(text: str) -> float:
        """
        Calculates Type-Token Ratio (TTR): Unique words / Total words.
        Higher TTR indicates higher lexical diversity (common in natural human text).
        Lower TTR indicates vocabulary repetition or low diversity.
        """
        words = re.findall(r'\b\w+\b', text.lower())
        if not words:
            return 0.0

        unique_words = set(words)
        return round(len(unique_words) / len(words), 4)

    @classmethod
    def analyze(cls, text: str) -> Dict[str, Any]:
        """
        Performs a full statistical entropy and uniformity analysis on the text.
        Returns metrics including Shannon entropy, TTR, sentence length variance, and AI likelihood assessment.
        """
        if not text or not text.strip():
            return {
                "shannon_entropy": 0.0,
                "ttr": 0.0,
                "predictability_score": 0.0,
                "ai_likelihood": "UNKNOWN",
                "word_count": 0,
                "unique_word_count": 0,
                "avg_sentence_length": 0.0,
                "sentence_length_std": 0.0,
                "details": "Empty text provided."
            }

        shannon = cls.calculate_shannon_entropy(text)
        ttr = cls.calculate_ttr(text)

        words = re.findall(r'\b\w+\b', text)
        word_count = len(words)
        unique_words = set(w.lower() for w in words)

        # Sentence length statistics
        sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
        sentence_lengths = [len(re.findall(r'\b\w+\b', s)) for s in sentences if len(re.findall(r'\b\w+\b', s)) > 0]

        if sentence_lengths:
            avg_sent_len = sum(sentence_lengths) / len(sentence_lengths)
            variance = sum((l - avg_sent_len) ** 2 for l in sentence_lengths) / len(sentence_lengths)
            std_sent_len = math.sqrt(variance)
        else:
            avg_sent_len = 0.0
            std_sent_len = 0.0

        # Predictability heuristic: LLMs tend to produce low sentence-length variance (uniformity)
        # and moderate-to-low TTR along with high Shannon entropy consistency.
        predictability = 0.0
        
        # 1. Low sentence length variance (overly uniform structure)
        if std_sent_len < 3.5 and len(sentence_lengths) > 3:
            predictability += 35.0
        elif std_sent_len < 5.0 and len(sentence_lengths) > 2:
            predictability += 20.0

        # 2. Moderate TTR range typical of LLMs (0.35 to 0.55 for medium texts)
        if 0.35 <= ttr <= 0.60 and word_count > 50:
            predictability += 35.0

        # 3. High character entropy (between 4.0 and 4.6 bits/char)
        if 4.0 <= shannon <= 4.6:
            predictability += 30.0

        predictability_score = min(100.0, round(predictability, 1))

        if predictability_score >= 70:
            likelihood = "HIGH"
        elif predictability_score >= 40:
            likelihood = "MODERATE"
        else:
            likelihood = "LOW"

        return {
            "shannon_entropy": shannon,
            "ttr": ttr,
            "predictability_score": predictability_score,
            "ai_likelihood": likelihood,
            "word_count": word_count,
            "unique_word_count": len(unique_words),
            "avg_sentence_length": round(avg_sent_len, 2),
            "sentence_length_std": round(std_sent_len, 2),
            "details": f"Analyzed {word_count} words across {len(sentences)} sentences. Shannon entropy: {shannon} bits/char."
        }
