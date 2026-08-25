"""
Aphanis - Git Hook & CI/CD Workflow Generator.
Installs .git/hooks/pre-commit and generates GitHub Action workflow configuration.
"""

import os
import stat
from pathlib import Path


GIT_HOOK_SCRIPT = r"""#!/usr/bin/env bash
# Aphanis - Zero-Trust Git Pre-Commit Provenance Hygiene Hook

echo "🛡️ Running Aphanis Pre-Commit Provenance Audit..."

# Check staged text/code files for zero-width watermarks and C2PA markers
STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.(md|txt|py|js|ts|jsx|tsx|json|html|svg|pdf|docx)$')

if [ -z "$STAGED_FILES" ]; then
    exit 0
fi

FAILED=0
for FILE in $STAGED_FILES; do
    if [ -f "$FILE" ]; then
        python3 -m aphanis.cli check "$FILE" > /dev/null 2>&1
        if [ $? -ne 0 ]; then
            echo "⚠️ Provenance risk or zero-width watermarks detected in: $FILE"
            FAILED=1
        fi
    fi
done

if [ $FAILED -ne 0 ]; then
    echo "❌ Commit rejected by Aphanis Firewall! Run 'aphanis clean-file <file>' to sanitize before committing."
    exit 1
fi

echo "✅ All staged files passed Aphanis Zero-Trust Audit!"
exit 0
"""


GITHUB_ACTION_WORKFLOW = """name: Aphanis Provenance & Hygiene Audit

on:
  push:
    branches: [ main, master, develop ]
  pull_request:
    branches: [ main, master ]

jobs:
  aphanis-audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install Aphanis
        run: |
          python -m pip install --upgrade pip
          pip install .
      - name: Run Zero-Trust Provenance Audit
        run: |
          aphanis clean-dir . --mode paranoid
"""


class HookInstaller:
    """Installs Git pre-commit hooks and generates CI/CD workflows."""

    @staticmethod
    def install_git_hook(repo_path: str = ".") -> str:
        """Installs pre-commit hook into .git/hooks/ directory."""
        git_dir = Path(repo_path).resolve() / ".git"
        if not git_dir.exists():
            return f"Error: No .git directory found at {repo_path}"

        hooks_dir = git_dir / "hooks"
        hooks_dir.mkdir(parents=True, exist_ok=True)

        hook_file = hooks_dir / "pre-commit"
        with open(hook_file, "w", encoding="utf-8") as f:
            f.write(GIT_HOOK_SCRIPT)

        # Make executable
        st = os.stat(hook_file)
        os.chmod(hook_file, st.st_mode | stat.S_IEXEC)

        return f"Successfully installed Aphanis Git pre-commit hook to {hook_file}"

    @staticmethod
    def generate_github_action(repo_path: str = ".") -> str:
        """Generates .github/workflows/aphanis-hygiene.yml file."""
        target_dir = Path(repo_path).resolve() / ".github" / "workflows"
        target_dir.mkdir(parents=True, exist_ok=True)

        workflow_file = target_dir / "aphanis-hygiene.yml"
        with open(workflow_file, "w", encoding="utf-8") as f:
            f.write(GITHUB_ACTION_WORKFLOW)

        return f"Successfully generated GitHub Action workflow at {workflow_file}"
