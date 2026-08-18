"""
Untrace AI - Zero-Touch Autoinstaller.
Automatically registers Untrace AI skills, rules, and hooks into Claude Code,
Antigravity IDE, Cursor IDE, and Git repositories so everything runs 100% on autopilot.
"""

import os
import shutil
from pathlib import Path
from typing import Dict, List


class AutoInstaller:
    """Installs Untrace AI skills and rules globally across all AI coding environments."""

    @classmethod
    def install_all(cls) -> Dict[str, str]:
        """Installs Untrace AI into Claude Code, Antigravity IDE, and Cursor IDE."""
        results = {}
        home = Path.home()

        curr_dir = Path(__file__).parent.parent
        skill_src = curr_dir / "skills" / "remove-ai-marks" / "SKILL.md"

        if not skill_src.exists():
            results["status"] = "Error: Could not locate skills/remove-ai-marks/SKILL.md"
            return results

        with open(skill_src, "r", encoding="utf-8") as f:
            skill_content = f.read()

        # 1. Claude Code (~/.claude/skills/remove-ai-marks/SKILL.md)
        claude_dir = home / ".claude" / "skills" / "remove-ai-marks"
        claude_dir.mkdir(parents=True, exist_ok=True)
        with open(claude_dir / "SKILL.md", "w", encoding="utf-8") as f:
            f.write(skill_content)
        results["claude_code"] = str(claude_dir / "SKILL.md")

        # 2. Antigravity IDE (~/.gemini/config/skills/remove-ai-marks/SKILL.md)
        gemini_dir = home / ".gemini" / "config" / "skills" / "remove-ai-marks"
        gemini_dir.mkdir(parents=True, exist_ok=True)
        with open(gemini_dir / "SKILL.md", "w", encoding="utf-8") as f:
            f.write(skill_content)
        results["antigravity_ide"] = str(gemini_dir / "SKILL.md")

        # 3. Cursor IDE (~/.cursor/rules/remove-ai-marks.mdc)
        cursor_dir = home / ".cursor" / "rules"
        cursor_dir.mkdir(parents=True, exist_ok=True)
        with open(cursor_dir / "remove-ai-marks.mdc", "w", encoding="utf-8") as f:
            f.write(skill_content)
        results["cursor_ide"] = str(cursor_dir / "remove-ai-marks.mdc")

        # 4. Local Git Pre-commit hook if inside a git repo
        if (Path(".") / ".git").exists():
            from untrace.hooks import HookInstaller
            hook_msg = HookInstaller.install_git_hook(".")
            results["git_hook"] = hook_msg

        return results


def auto_install_all() -> Dict[str, str]:
    """Helper function to run 1-click zero-touch installation."""
    return AutoInstaller.install_all()
