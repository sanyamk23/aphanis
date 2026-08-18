"""Command Line Interface for Watermark Remover."""

import argparse
import sys
from watermark_remover.cleaner import clean_text, clean_file, StatisticalPerturber
from watermark_remover.mcp_server import main as run_server


def main():
    parser = argparse.ArgumentParser(description="Watermark Remover - Provenance Hygiene Toolkit for Claude & General Use")
    subparsers = parser.add_subparsers(dest="command", help="Sub-command help")

    # clean-text subcommand
    clean_text_parser = subparsers.add_parser("clean-text", help="Sanitize inline text string or stdin")
    clean_text_parser.add_argument("text", nargs="?", help="Text string to clean. If empty, reads from stdin.")
    clean_text_parser.add_argument("--perturb", action="store_true", help="Perturb statistical AI marker vocabulary")

    # clean-file subcommand
    clean_file_parser = subparsers.add_parser("clean-file", help="Sanitize file metadata and zero-width watermarks")
    clean_file_parser.add_argument("path", help="Path to file (PNG, JPEG, SVG, PDF, DOCX, HTML, MD)")

    # server subcommand
    subparsers.add_parser("server", help="Launch Model Context Protocol (MCP) server for Claude Desktop")

    args = parser.parse_args()

    if args.command == "clean-text":
        if args.text:
            input_text = args.text
        else:
            input_text = sys.stdin.read()
        cleaned = clean_text(input_text, perturb_stats=args.perturb)
        sys.stdout.write(cleaned)

    elif args.command == "clean-file":
        success, msg = clean_file(args.path)
        print(msg)
        sys.exit(0 if success else 1)

    elif args.command == "server":
        run_server()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
