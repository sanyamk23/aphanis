"""
Untrace AI - Automatic Natural Humanizer Engine with Tone Personas.
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

        return result


def humanize_text(text: str, apply_contractions: bool = True, reduce_fillers: bool = True, tone: str = "conversational") -> str:
    """Helper function to convert text into natural human tone."""
    return HumanizerEngine.humanize(text, apply_contractions=apply_contractions, reduce_fillers=reduce_fillers, tone=tone)
