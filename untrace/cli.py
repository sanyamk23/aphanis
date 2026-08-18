"""
Untrace AI - Command Line Interface.
"""

import argparse
import sys
import os
import shutil
from pathlib import Path

from untrace.cleaner import clean_text, clean_file, StatisticalPerturber
from untrace.mcp_server import main as run_server


def install_claude_code():
    """Installs the untrace skill into user's global ~/.claude/skills/ directory."""
    home = Path.home()
    target_dir = home / ".claude" / "skills" / "remove-ai-marks"
    target_dir.mkdir(parents=True, exist_ok=True)

    # Path to SKILL.md inside current package/repo
    curr_dir = Path(__file__).parent.parent
    skill_src = curr_dir / ".claude" / "skills" / "remove-ai-marks" / "SKILL.md"

    if not skill_src.exists():
        skill_src = curr_dir / "skills" / "remove-ai-marks" / "SKILL.md"

    if skill_src.exists():
        shutil.copy(skill_src, target_dir / "SKILL.md")
        print(f"✅ Successfully installed Untrace Skill to {target_dir / 'SKILL.md'}")
    else:
        print("❌ Could not locate SKILL.md template.")


def install_claude_desktop():
    """Prints or writes the Claude Desktop JSON configuration."""
    config_snippet = """{
  "mcpServers": {
    "untrace": {
      "command": "python3",
      "args": [
        "-m",
        "untrace.cli",
        "server"
      ]
    }
  }
}"""
    print("\n📋 Add the following snippet to your `claude_desktop_config.json`:\n")
    print(config_snippet)
    print("\n(Path on macOS: ~/Library/Application Support/Claude/claude_desktop_config.json)\n")


def main():
    parser = argparse.ArgumentParser(
        prog="untrace",
        description="Untrace AI - Ultimate AI Provenance, Watermark & Metadata Sanitizer"
    )
    subparsers = parser.add_subparsers(dest="command", help="Sub-command help")

    # clean-text
    clean_text_parser = subparsers.add_parser("clean-text", help="Sanitize inline text string or stdin")
    clean_text_parser.add_argument("text", nargs="?", help="Text string to clean. If empty, reads from stdin.")
    clean_text_parser.add_argument("--perturb", action="store_true", help="Rephrase statistical AI vocabulary markers")

    # clean-file
    clean_file_parser = subparsers.add_parser("clean-file", help="Sanitize file metadata and zero-width watermarks")
    clean_file_parser.add_argument("path", help="Path to file (PNG, JPEG, SVG, PDF, DOCX, HTML, MD)")
    clean_file_parser.add_argument("--jitter", action="store_true", help="Apply sub-pixel LSB noise jitter to images")

    # server
    subparsers.add_parser("server", help="Launch Model Context Protocol (MCP) server for Claude Desktop")

    # install commands
    subparsers.add_parser("install-claude-code", help="Install Untrace skill to global ~/.claude/skills/")
    subparsers.add_parser("install-claude-desktop", help="Show configuration snippet for Claude Desktop")

    args = parser.parse_args()

    if args.command == "clean-text":
        if args.text:
            input_text = args.text
        else:
            input_text = sys.stdin.read()
        cleaned = clean_text(input_text, perturb_stats=args.perturb)
        sys.stdout.write(cleaned)

    elif args.command == "clean-file":
        success, msg = clean_file(args.path, disrupt_image_pixels=args.jitter)
        print(msg)
        sys.exit(0 if success else 1)

    elif args.command == "server":
        run_server()

    elif args.command == "install-claude-code":
        install_claude_code()

    elif args.command == "install-claude-desktop":
        install_claude_desktop()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
