"""
Aphanis - Automatic Natural Humanizer Engine with Tone Personas.
Transforms formal, passive, and uniform LLM outputs into natural human tone.
"""

import re
from typing import Dict, Any, List, Optional


class HumanizerEngine:
    """Transforms AI-generated text into authentic human phrasing and rhythm."""

    # Natural conversational contractions
    CONTRACTIONS_MAP: Dict[str, str] = {
        r'\bcannot\b': "can't",
        r'\bdo not\b': "don't",
        r'\bdoes not\b': "doesn't",
        r'\bdid not\b': "didn't",
        r'\bwill not\b': "won't",
        r'\bwould not\b': "wouldn't",
        r'\bshould not\b': "shouldn't",
        r'\bcould not\b': "couldn't",
        r'\bis not\b': "isn't",
        r'\bare not\b': "aren't",
        r'\bwas not\b': "wasn't",
        r'\bwere not\b': "weren't",
        r'\bhave not\b': "haven't",
        r'\bhas not\b': "hasn't",
        r'\bhad not\b': "hadn't",
        r'\bit is\b': "it's",
        r'\bthat is\b': "that's",
        r'\bthere is\b': "there's",
        r'\bwhat is\b': "what's",
        r'\bwho is\b': "who's",
        r'\bhere is\b': "here's",
        r'\bwe are\b': "we're",
        r'\byou are\b': "you're",
        r'\bthey are\b': "they're",
        r'\bwe have\b': "we've",
        r'\byou have\b': "you've",
        r'\bthey have\b': "they've",
        r'\bwe will\b': "we'll",
        r'\byou will\b': "you'll",
        r'\bthey will\b': "they'll",
        r'\bwe would\b': "we'd",
        r'\byou would\b': "you'd",
        r'\bthey would\b': "they'd",
    }

    # Wordy robotic filler phrases -> Concise active human phrases
    FILLER_PHRASES_MAP: Dict[str, str] = {
        r'\bin order to\b': 'to',
        r'\bit is important to note that\b': 'note that',
        r'\bit is worth noting that\b': 'note that',
        r'\bit is essential to\b': 'remember to',
        r'\bdue to the fact that\b': 'because',
        r'\bat this point in time\b': 'now',
        r'\bwith regard to\b': 'about',
        r'\bwith respect to\b': 'about',
        r'\bin light of the fact that\b': 'since',
        r'\ba large number of\b': 'many',
        r'\ba majority of\b': 'most',
        r'\bhas the capability of\b': 'can',
        r'\bhave the capability of\b': 'can',
        r'\bserves to improve\b': 'improves',
        r'\bserves to enhance\b': 'enhances',
        r'\bplays a crucial role in\b': 'helps',
        r'\bplays a pivotal role in\b': 'helps',
        r'\btakes into consideration\b': 'considers',
        r'\btake into consideration\b': 'consider',
        r'\bin the event that\b': 'if',
        r'\bat the end of the day\b': 'ultimately',
        r'\bfor the purpose of\b': 'for',
        r'\bhas a tendency to\b': 'tends to',
        r'\bin a position to\b': 'able to',
        r'\bmake a decision\b': 'decide',
        r'\bcome to a conclusion\b': 'conclude',
        r'\bprovide assistance to\b': 'help',
        # ── Expanded AI telltales ──────────────────────────────────────────────
        r'\bin today\'s (?:digital|modern|fast-paced|ever-evolving|interconnected) (?:landscape|world|era|environment)\b': 'today,',
        r'\bin an increasingly (?:digital|complex|interconnected) (?:world|landscape|era|environment)\b': 'today,',
        r'\bin today\'s (?:fast-)?paced world\b': 'today,',
        r'\bin today\'s (?:ever-)?evolving digital landscape\b': 'today,',
        r'\bin the modern (?:era|world|age)\b': 'today,',
        r'\bin today\'s (?:digital|modern) age\b': 'today,',
        r'\bin the (?:contemporary|current|ever-changing|ever-evolving) landscape\b': 'today,',
        r'\bthe landscape of\b': 'how',
        r'\bin recent years\b': 'lately,',
        r'\bin recent times\b': 'recently,',
        r'\bprior to (this|that)\b': 'before',
        r'\bhas the ability to\b': 'can',
        r'\bpossesses the ability to\b': 'can',
        r'\bhas the capability of\b': 'can',
        r'\bhave the capability of\b': 'can',
        r'\bhas the potential to\b': 'could',
        r'\bplays a (?:crucial|pivotal|key|central|vital|fundamental) role in\b': 'helps',
        r'\bserves as a (?:cornerstone|linchpin|vital component|key element) of\b': 'is part of',
        r'\bbrings (?:to bear|to the table)\b': 'adds',
        r'\bdelving (?:into|deeper (?:into|in))\b': 'exploring',
        r'\bdelve into\b': 'explore',
        r'\bin (?:the |a )?(?:realm|domain|arena|sphere) of\b': 'in the area of',
        r'\bharnesses the power of\b': 'uses',
        r'\bleverages the power of\b': 'uses',
        r'\butilizes\b': 'uses',
        r'\butilizes (?:the|this|these)\b': 'uses this',
        r'\bexecutes (?:the|this|these)\b': 'does this',
        r'\bconducts (?:an|a)? (?:comprehensive|thorough|detailed|systematic|in-depth|deep) analysis\b': 'analyzes',
        r'\biterates through\b': 'goes through each',
        r'\bcomputes the results of\b': 'calculates',
        r'\bensures that\b': 'makes sure',
        r'\bfacilitates the process of\b': 'helps',
        r'\boptimizes for\b': 'improves',
        r'\breminiscent of\b': 'like',
        r'\bheralds a new era of\b': 'starts a new era of',
        r'\bmarks a significant shift in\b': 'changes how',
        r'\brepresents a paradigm shift in\b': 'fundamentally changes',
        r'\bunderscores the (?:importance|significance|value|criticality)\b': 'shows how important',
        r'\bhighlights the (?:importance|significance|value|criticality)\b': 'shows how important',
        r'\bimperative that\b': 'important that',
        r'\bit is worth mentioning (?:that)?\b': 'note that',
        r'\bin essence\b': 'basically,',
        r'\bas such\b': 'therefore,',
        r'\bto that end\b': 'for that purpose,',
        r'\bin the (?:final|ultimate) analysis\b': 'in the end,',
        r'\bwhen all is said and done\b': 'in the end,',
        r'\bat the conclusion\b': 'finally,',
        r'\bit goes without saying (?:that)?\b': '',
        r'\bnotably\b': 'especially',
        r'\bindeed\b': 'actually',
        r'\bas a result\b': 'so',
        r'\bas a consequence\b': 'so',
        r'\bresulting in\b': 'causing',
        r'\bprovides (?:a|an|the) (?:comprehensive|thorough|detailed|complete|robust)\b': 'gives a',
        r'\bdemonstrates (?:the|this|these|a|an)\b': 'shows the',
        r'\bshowcases (?:the|this|these|a|an)\b': 'shows the',
        r'\billustrates (?:the|this|these|a|an)\b': 'shows the',
        r'\bexemplifies (?:the|this|these|a|an)\b': 'shows the',
        r'\bepitomizes (?:the|this|these|a|an)\b': 'represents the',
        r'\bis a testament to\b': 'proves',
        r'\bis a stark reminder of\b': 'reminds us of',
        r'\bis a vivid illustration of\b': 'illustrates',
        r'\bis a prime example of\b': 'exemplifies',
        r'\bpaves the way for\b': 'enables',
        r'\bushering in a new era of\b': 'starting a new era of',
        r'\bneedless to say\b': '',
        r'\ball things being equal\b': '',
        r'\bas a general rule\b': '',
        # ── Overconfident hedging & redundant qualifiers ──────────────────────────
        r'\bit is (?:safe to assume|worth noting|important to note|essential to|imperative to) (?:that)?\b': '',
        r'\bit goes without saying\b': '',
        r'\bit stands to reason that\b': '',
        r'\bas mentioned (?:earlier|above|previously)\b': 'as said before',
        r'\bas noted (?:above|earlier|previously)\b': 'as said before',
        r'\bas previously stated\b': 'as said before',
        r'\bas referenced (?:above|earlier)\b': 'as said before',
        r'\bit is safe to say that\b': 'note that',
        r'\bit is fair to say that\b': 'note that',
        r"\bit is clear that\b": "it's clear",
        r'\bit should be noted that\b': '',
        r'\bit bears mentioning that\b': '',
        r'\bto be fair\b': '',
        r'\bas a matter of fact\b': 'in fact',
        r'\bit is important to understand that\b': 'remember that',
        r'\bit is critical to recognize that\b': 'remember that',
        r'\bit is essential to recognize that\b': 'remember that',
        r'\bin a (?:broader|wider|larger) context\b': '',
        r'\bin the grand scheme of things\b': '',
        # ── Formulaic opening phrases ─────────────────────────────────────────────
        r'\bin today\'s (?:fast-)?paced (?:digital|business|tech|market) (?:landscape|environment|arena|world)\b': 'currently,',
        r'\bin an increasingly (?:digital|interconnected|complex|global) (?:world|landscape|era|environment|age)\b': 'currently,',
        r'\bagainst the backdrop of\b': 'amid',
        r'\bin the backdrop of\b': 'amid',
        r'\bin the wake of (?:the|this|recent|ongoing)\b': 'after',
        r'\bin the light of (?:the|recent|ongoing)\b': 'after',
        r'\bin today\'s day and age\b': 'today,',
        # ── Redundant/overly formal phrasing ───────────────────────────────────
        r'\bwith a view to\b': 'to',
        r'\bfor the purpose of doing\b': 'to',
        r'\bserves as an? (?:indication|indicator) of\b': 'shows',
        r'\bacts as an? (?:indication|indicator) of\b': 'shows',
        r'\bplays an? (?:integral|essential|vital|key|crucial|significant|major) role in\b': 'helps',
        r'\bis (?:in|under) no uncertain terms\b': '',
        r'\bis nothing short of\b': 'is',
        r'\bis at the (?:forefront|cutting edge|vanguard|leading edge) of\b': 'leads in',
        r'\bis a (?:pioneer|trailblazer|groundbreaker|leader) in\b': 'leads in',
        r'\bushering in a new era of\b': 'starting a new era of',
        r'\bheralding a new era of\b': 'starting a new era of',
        r'\bsignifies a (?:fundamental|major|significant|profound) shift\b': 'changes how',
        r'\bopens up (?:new|novel|innovative|exciting) possibilities for\b': 'creates new possibilities for',
        r'\bopens (?:new|novel|innovative|exciting) (?:avenues|horizons) for\b': 'creates new paths for',
    }

    # Formulaic LLM transitions -> Organic human connectors
    TRANSITIONS_MAP: Dict[str, str] = {
        r'\bfurthermore,\b': 'also,',
        r'\bmoreover,\b': 'plus,',
        r'\bconsequently,\b': 'so,',
        r'\bnevertheless,\b': 'still,',
        r'\bnonetheless,\b': 'still,',
        r'\bin conclusion,\b': 'overall,',
        r'\bto summarize,\b': 'in short,',
        r'\bto sum up,\b': 'in short,',
        r'\bas a matter of fact,\b': 'in fact,',
        # ── Additional organic transitions ───────────────────────────────────────
        r'\bas a consequence,\b': 'so,',
        r'\bas a result of this,\b': 'because of this,',
        r'\bin light of this,\b': 'given this,',
        r'\bin view of this,\b': 'given this,',
        r'\bto that end,\b': 'for that purpose,',
        r'\bas such,\b': 'therefore,',
        r'\bit follows that\b': 'so',
        r'\bconsequently, it is evident that\b': 'so',
        r'\bthus, it can be concluded that\b': 'so',
    }

    # ── AI uncertainty / hedge word removal ──────────────────────────────────
    HEDGE_WORDS: Dict[str, str] = {
        r'\bvery\b\s+': '',
        r'\bsomewhat\b': '',
        r'\brather\b\s+': '',
        r'\bquite\b\s+': '',
        r'\bpretty\b\s+': '',
        r'\breally\b\s+': '',
        r'\bextremely\b': 'very',
        r'\b(t?extremely) (?:important|critical|vital|essential)\b': r'\1',
        r'\b(very) (?:important|critical|vital|essential)\b': r'\1',
    }

    # Persona specific overrides
    TECH_LEAD_SWAPS: Dict[str, str] = {
        r'\butilize\b': 'use',
        r'\butilizes\b': 'uses',
        r'\butilizing\b': 'using',
        r'\barchitected\b': 'built',
        r'\bleverage\b': 'use',
    }

    ACADEMIC_SWAPS: Dict[str, str] = {
        r'\bdelve\b': 'investigate',
        r'\btestament\b': 'evidence',
        r'\bspearhead\b': 'direct',
    }

    @classmethod
    def humanize(cls, text: str, apply_contractions: bool = True, reduce_fillers: bool = True, adapt_transitions: bool = True, tone: str = "conversational") -> str:
        import random as _random
        _random.seed(42)
        """
        Transforms text into natural human tone by synthesizing contractions,
        reducing passive filler phrases, and applying tone personas (conversational, casual, tech-lead, academic, executive).
        """
        if not text or not text.strip():
            return text

        result = text
        tone = (tone or "conversational").lower()

        # Tone specific adjustments
        if tone == "tech-lead":
            for pattern, replacement in cls.TECH_LEAD_SWAPS.items():
                result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
        elif tone == "academic":
            apply_contractions = False # Academic style avoids contractions but strips LLM clichés
            for pattern, replacement in cls.ACADEMIC_SWAPS.items():
                result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)

        # 1. Reduce wordy filler phrases
        if reduce_fillers:
            for pattern, replacement in cls.FILLER_PHRASES_MAP.items():
                def _repl(m):
                    word = m.group(0)
                    if word and word[0].isupper():
                        return replacement.capitalize()
                    elif word.isupper():
                        return replacement.upper()
                    return replacement
                result = re.sub(pattern, _repl, result, flags=re.IGNORECASE)

        # 2. Adapt rigid transitions
        if adapt_transitions:
            for pattern, replacement in cls.TRANSITIONS_MAP.items():
                def _repl_trans(m):
                    word = m.group(0)
                    if word and word[0].isupper():
                        return replacement.capitalize()
                    elif word.isupper():
                        return replacement.upper()
                    return replacement
                result = re.sub(pattern, _repl_trans, result, flags=re.IGNORECASE)

        # 3. Synthesize natural contractions
        if apply_contractions:
            for pattern, replacement in cls.CONTRACTIONS_MAP.items():
                def _repl_contract(m):
                    word = m.group(0)
                    if word and word[0].isupper():
                        return replacement.capitalize()
                    elif word.isupper():
                        return replacement.upper()
                    return replacement
                result = re.sub(pattern, _repl_contract, result, flags=re.IGNORECASE)

        # 4. Clean up double spaces created by edits
        result = re.sub(r'[ \t]+', ' ', result)

        # 5. Structural humanization: vary sentence length & rhythm
        import random as _random

        # More AI-specific sentence starters and phrasing to replace/restructure
        AI_STRUCTURE_PATTERNS = [
            (r"\bIn (?:today's|the|this) (?:increasingly\s+)?(?:digital|modern|fast-paced|interconnected|evolving)\s+(?:landscape|world|era|environment|age|context)\b", "These days,"),
            (r"\bIn (?:today's|the|this)\s+(?:landscape|world|era|environment|age|context)\b", "These days,"),
            (r"\bin today's day and age\b", "these days,"),
            (r'\bstands as a cornerstone of\b', "is foundational to"),
            (r'\bstands as an? (?:cornerstone|linchpin|pillar) of\b', "is key to"),
            (r'\bsynergistically\b', "together"),
            (r'\bwork synergistically\b', "work hand in hand"),
            (r'\breduces (?:complexity|inefficiency)\b', "simplifies"),
            (r'\bprior to (?:this|that)\b', "before this"),
            (r'\bIn conclusion,?\b', "Overall,"),
            (r'\bTo summarize,?\b', "In short,"),
            (r'\bTo sum up,?\b', "In short,"),
        ]

        for pattern, replacement in AI_STRUCTURE_PATTERNS:
            result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)

        # Clean up double commas (,,  -> ,) caused by replacements that end with comma
        result = re.sub(r',\s*,', ',', result)
        result = re.sub(r',\s*([.!?])', r'\1', result)

        sentences = re.split(r'(?<=[.!?])\s+', result)
        if len(sentences) > 2:
            # Merge short consecutive sentences (AI over-splits)
            merged = []
            i = 0
            while i < len(sentences):
                curr = sentences[i]
                # Merge if this sentence is very short (< 10 words) and next exists
                while len(curr.split()) < 10 and i + 1 < len(sentences):
                    nxt = sentences[i + 1]
                    if len(nxt.split()) < 30 and len(nxt) > 1:
                        curr = curr.rstrip('.!?') + ", " + nxt[0].lower() + nxt[1:]
                        i += 1
                    else:
                        break
                merged.append(curr)
                i += 1
            sentences = merged

            # Split long sentences (>30 words) on relative clauses to simulate human overtalk
            split_result = []
            for s in sentences:
                words = s.split()
                if len(words) > 30:
                    # Split before "which", "that", "including", "such as"
                    parts = re.split(r'\s+(which|that|including|such as)\s+', s)
                    if len(parts) > 1:
                        first = parts[0]
                        rest = " ".join(parts[1:])
                        split_result.append(first.rstrip('.!?') + ".")
                        split_result.append(rest)
                    else:
                        split_result.append(s)
                else:
                    split_result.append(s)
            sentences = split_result

            # Randomly add conversational fillers to ~20% of sentences
            fillers = ["", "", "", "actually, ", "you know, ", "I mean, ", "well, ", "oh, "]
            def _add_filler(s):
                if not s or len(s) < 2:
                    return s
                if _random.random() > 0.15:
                    return s
                prefix = _random.choice(fillers)
                return prefix + s[0].lower() + s[1:]
            result = " ".join(_add_filler(s) for s in sentences)
            result = re.sub(r'\s+([.!?])', r'\1', result)
            result = re.sub(r'([.!?])\s+([a-z])', lambda m: m.group(1) + " " + m.group(2).upper(), result)
        else:
            result = " ".join(sentences) if sentences else result

        # 6. Break AI list/structured patterns: convert "- X - Y" lines into prose
        # Detectors flag perfect parallel bullet structure. Merge into flowing text.
        bullet_lines = re.findall(r'(?:^|\n)\s*[-*•]\s+([^\n]+)', result)
        if len(bullet_lines) >= 3:
            # Replace the bullet block with a single prose paragraph
            block_pattern = re.compile(r'(?:^|\n)\s*[-*•]\s+[^\n]+(?:\n\s*[-*•]\s+[^\n]+){2,}', re.MULTILINE)
            block = block_pattern.search(result)
            if block:
                items = re.findall(r'[-*•]\s+([^\n]+)', block.group())
                # Group into 2-3 sentence flowing prose with varied connectives
                if len(items) >= 4:
                    mid = len(items) // 2
                    first_chunk = items[:mid]
                    second_chunk = items[mid:]
                    connectors = [
                        "You've got things like {items}, and then there's {rest}.",
                        "It usually breaks down into {items}, plus {rest}.",
                        "Some of the main pieces here are {items}, with {rest} on top of that.",
                    ]
                    items_str_first = ", ".join(first_chunk[:-1]) + " and " + first_chunk[-1] if len(first_chunk) > 1 else first_chunk[0]
                    items_str_rest = ", ".join(second_chunk[:-1]) + " and " + second_chunk[-1] if len(second_chunk) > 1 else second_chunk[0]
                    template = _random.choice(connectors)
                    prose = template.format(items=items_str_first, rest=items_str_rest)
                else:
                    items_str = ", ".join(items[:-1]) + " and " + items[-1] if len(items) > 1 else items[0]
                    prose = "This includes " + items_str + "."
                result = block_pattern.sub(prose, result, count=1)

        # 7. Break formulaic opener "It covers:" / "These include:" / "The goal is..."
        result = re.sub(r'\bIt covers:\s*\n', "It includes things like ", result, flags=re.IGNORECASE)
        result = re.sub(r'\bThe goal is usually one of:\s*', "Most of the time you're going for ", result, flags=re.IGNORECASE)
        result = re.sub(r'\bThe goal is\s*', "What you'\''re really after is ", result, flags=re.IGNORECASE)

        # 8. Break "Most teams mix X with Y" formulaic closers
        result = re.sub(r'\bMost teams mix\s+', "A lot of teams will pair ", result, flags=re.IGNORECASE)

        result = re.sub(r'[ \t]+', ' ', result)

        return result


def humanize_text(text: str, apply_contractions: bool = True, reduce_fillers: bool = True, tone: str = "conversational") -> str:
    """Helper function to convert text into natural human tone."""
    return HumanizerEngine.humanize(text, apply_contractions=apply_contractions, reduce_fillers=reduce_fillers, tone=tone)
