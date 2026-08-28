import unittest
from aphanis.humanizer import HumanizerEngine, humanize_text
from aphanis.cleaner import clean_text


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


class TestSmmPillarsFolding(unittest.TestCase):
    """Regression tests for the SMM / numbered-pillars / common-goals bypass case.

    The detector screenshots the user shared showed three things in assistant
    prose that needed to fold into a flowing paragraph before sentence split:
      - "4 Core Pillars of X" heading + "1. Y — descr" / "2. Z — descr" blocks
      - "Common Goals of X:" + bullet list
      - generic heading + numbered list (without the "Core Pillars" trigger)
    """

    def test_pillars_at_start_of_text_fold(self):
        text = (
            "4 Core Pillars of SMM\n"
            "1. Strategy — picking goals and the right channels to reach them.\n"
            "2. Content — making posts, videos, and graphics people actually want to see.\n"
            "3. Engagement — replying to comments, DMs, and joining the conversation.\n"
            "4. Analytics — watching what works and tweaking what doesn't.\n"
        )
        out = HumanizerEngine.humanize(text, tone="conversational")
        # The "1. ", "2. " list markers must be gone.
        self.assertNotIn("1. ", out)
        self.assertNotIn("2. ", out)
        self.assertNotIn("3. ", out)
        self.assertNotIn("4. ", out)
        # The pillar titles must survive as a joined list.
        self.assertIn("Strategy", out)
        self.assertIn("Content", out)
        self.assertIn("Engagement", out)
        self.assertIn("Analytics", out)
        # Sub-descriptions (after the em-dash) must be stripped so the join reads clean.
        self.assertNotIn("picking goals", out)
        self.assertNotIn("replying to comments", out)

    def test_common_goals_fold(self):
        text = (
            "Common Goals of SMM:\n"
            "- Build brand awareness\n"
            "- Drive website traffic\n"
            "- Generate leads and sales\n"
            "- Foster community and loyalty\n"
        )
        out = HumanizerEngine.humanize(text, tone="conversational")
        # The bullet markers must be gone.
        self.assertNotIn("- Build", out)
        self.assertNotIn("- Drive", out)
        # Items should be folded into a single sentence — "going for ...".
        self.assertIn("going for", out)
        # Items should be lowercased at start of each so the prose reads as a list, not a heading.
        self.assertIn("build brand awareness", out)
        self.assertIn("drive website traffic", out)
        self.assertIn("generate leads", out)
        self.assertIn("foster community and loyalty", out)  # humanizer only folds structure; vocab swap is StatisticalPerturber's job

    def test_full_smm_sample_audits_clean(self):
        from aphanis.cleaner import AuditTool
        text = (
            "Social media marketing is about connecting with people where they already hang out online.\n"
            "\n"
            "4 Core Pillars of SMM\n"
            "1. Strategy — picking goals and the right channels to reach them.\n"
            "2. Content — making posts, videos, and graphics people actually want to see.\n"
            "3. Engagement — replying to comments, DMs, and joining the conversation.\n"
            "4. Analytics — watching what works and tweaking what doesn't.\n"
            "\n"
            "Common Goals of SMM:\n"
            "- Build brand awareness\n"
            "- Drive website traffic\n"
            "- Generate leads and sales\n"
            "- Foster community and loyalty\n"
        )
        out = clean_text(text, mode="paranoid")
        audit = AuditTool.audit_text(out)
        self.assertEqual(audit["status"], "CLEAN", f"Audit failed: {audit['issues']}")
        self.assertEqual(audit["score"], 100)

    def test_no_em_dash_in_pillar_intro(self):
        # The em-dash was a Claude signature telltale. The humanizer used to
        # introduce it via "It usually comes down to a handful of things — ".
        text = (
            "4 Core Pillars of X\n"
            "1. A\n"
            "2. B\n"
            "3. C\n"
        )
        out = HumanizerEngine.humanize(text, tone="conversational")
        self.assertNotIn(" — ", out)

    def test_generic_heading_numbered_fold(self):
        # The "Core Pillars" pattern is one specific trigger; we also need to
        # fold a generic heading + numbered block.
        text = (
            "Key Components of Email Marketing\n"
            "1. List Building\n"
            "2. Segmentation\n"
            "3. Copywriting\n"
            "4. Analytics\n"
        )
        out = HumanizerEngine.humanize(text, tone="conversational")
        self.assertNotIn("1. ", out)
        self.assertNotIn("2. ", out)
        self.assertIn("List Building", out)
        self.assertIn("Segmentation", out)
        self.assertIn("Copywriting", out)
        self.assertIn("Analytics", out)

    def test_hyphen_in_compound_word_preserved(self):
        # Regression: an earlier version of the title-strip split on any
        # hyphen, which truncated "high-quality content" to "high".
        text = (
            "5 Steps of Building a Product\n"
            "1. Find a real problem\n"
            "2. Talk to real users\n"
            "3. Build a low-cost prototype\n"
            "4. Run small experiments\n"
            "5. Ship a paid beta version\n"
        )
        out = HumanizerEngine.humanize(text, tone="conversational")
        self.assertIn("low-cost prototype", out)
        self.assertIn("paid beta version", out)
        self.assertNotIn("low and cost", out)
        self.assertNotIn("paid and beta", out)

    def test_pillar_subtitles_stripped_after_emdash_normalization(self):
        # Regression: UnicodeSanitizer replaces em-dash with " - " before the
        # humanizer runs, so the title-strip pattern must also accept the
        # " - " form. Otherwise "Strategy - picking goals" leaks into the
        # folded list.
        text = (
            "4 Core Pillars of SMM\n"
            "1. Strategy — picking goals and the right channels\n"
            "2. Content — making posts people want to see\n"
            "3. Engagement — replying to comments\n"
            "4. Analytics — watching what works\n"
        )
        out = HumanizerEngine.humanize(text, tone="conversational")
        self.assertNotIn("picking goals", out)
        self.assertNotIn("making posts", out)
        self.assertNotIn("replying to comments", out)
        self.assertIn("Strategy", out)
        self.assertIn("Content", out)
        self.assertIn("Engagement", out)
        self.assertIn("Analytics", out)


if __name__ == "__main__":
    unittest.main()
