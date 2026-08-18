"""
Untrace AI - Command Line Interface.
"""

import argparse
import sys
import os
import shutil
from pathlib import Path

from untrace.cleaner import clean_text, clean_file, StatisticalPerturber, FileMetadataSanitizer
from untrace.watcher import DirectoryWatcher
from untrace.mcp_server import main as run_server


def install_claude_code():
    """Installs the untrace skill into user's global ~/.claude/skills/ directory."""
    home = Path.home()
    target_dir = home / ".claude" / "skills" / "remove-ai-marks"
    target_dir.mkdir(parents=True, exist_ok=True)

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


def clean_directory(dir_path: str, perturb: bool = True):
    """Recursively cleans all files in a directory."""
    target_path = Path(dir_path).resolve()
    if not target_path.exists():
        print(f"❌ Path not found: {dir_path}")
        sys.exit(1)

    watcher = DirectoryWatcher(str(target_path), perturb_stats=perturb)
    count = watcher.scan_and_clean()
    print(f"\n🎉 Finished recursively sanitizing {count} files in {target_path}")


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
    clean_file_parser = subparsers.add_parser("clean-file", help="Sanitize file metadata, AI comments, and zero-width watermarks")
    clean_file_parser.add_argument("path", help="Path to file (PNG, JPEG, SVG, PDF, DOCX, HTML, MD, PY, JS, TS)")
    clean_file_parser.add_argument("--jitter", action="store_true", help="Apply sub-pixel LSB noise jitter to images")
    clean_file_parser.add_argument("--perturb", action="store_true", help="Rephrase statistical AI vocabulary")

    # clean-dir
    clean_dir_parser = subparsers.add_parser("clean-dir", help="Recursively sanitize all files in a directory")
    clean_dir_parser.add_argument("path", nargs="?", default=".", help="Directory path to clean (default: current directory)")
    clean_dir_parser.add_argument("--no-perturb", action="store_true", help="Disable vocabulary rephrasing")

    # watch
    watch_parser = subparsers.add_parser("watch", help="Watch directory in real time and automatically sanitize created/edited files")
    watch_parser.add_argument("path", nargs="?", default=".", help="Directory path to watch (default: current directory)")

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
        success, msg = clean_file(args.path, disrupt_image_pixels=args.jitter, perturb_stats=args.perturb)
        print(msg)
        sys.exit(0 if success else 1)

    elif args.command == "clean-dir":
        clean_directory(args.path, perturb=not args.no_perturb)

    elif args.command == "watch":
        watcher = DirectoryWatcher(args.path)
        watcher.start()

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
