"""
Untrace AI :: Zero-Trust AI Provenance Firewall & Enterprise Stealth Engine - CLI.
"""

import argparse
import sys
import os
import shutil
from pathlib import Path

from untrace.cleaner import clean_text, clean_file, StatisticalPerturber, FileMetadataSanitizer, audit_text
from untrace.watcher import DirectoryWatcher
from untrace.mcp_server import main as run_server
from untrace.entropy import EntropyAnalyzer
from untrace.rules import RuleEngine
from untrace.stealth import StegoRiskMatrix, StealthMode
from untrace.dashboard import launch_dashboard
from untrace.humanizer import HumanizerEngine, humanize_text
from untrace.clipboard import ClipboardDaemon
from untrace.hooks import HookInstaller
from untrace.cert import AuditCertificateGenerator
from untrace.heatmap import HeatmapRenderer


ASCII_BANNER = r"""
  _   _ _  _ _____ ___    _   ___ ___   _   ___ 
 | | | | \| |_   _| _ \  /_\ / __| __| /_\ |_ _|
 | |_| | .` | | | |   / / _ \ (__| _| / _ \ | | 
  \___/|_|\_| |_| |_|_\/_/ \_\___|___/_/ \_\___|

🛡️ UNTRACE AI :: Enterprise Zero-Trust Provenance Firewall v1.4.0
"""


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


def print_risk_matrix(matrix: dict):
    """Prints formatted 4-Vector Stego Risk Matrix to terminal."""
    score = matrix["overall_clean_score"]
    level = matrix["provenance_risk_level"]
    vectors = matrix["vectors"]

    print("\n🛡️ --- 4-VECTOR STEGO RISK MATRIX REPORT --- 🛡️")
    print(f"PROVENANCE RISK LEVEL : {level}")
    print(f"OVERALL CLEAN SCORE   : {score}/100\n")

    v1 = vectors["vector_1_unicode_steganography"]
    v2 = vectors["vector_2_statistical_model"]
    v3 = vectors["vector_3_metadata_container"]
    v4 = vectors["vector_4_spatial_frequency"]

    print(f"[VECTOR 1] Unicode Steganography  : {v1['risk_score']:5.1f}% Risk [{v1['status']}] ({v1['issues_found']} hidden bytes)")
    print(f"[VECTOR 2] Statistical Model Risk : {v2['risk_score']:5.1f}% Risk [{v2['status']}] ({v2['telltale_phrases']} clichés, {v2['em_dashes']} em-dashes)")
    print(f"[VECTOR 3] Metadata & Containers  : {v3['risk_score']:5.1f}% Risk [{v3['status']}] ({v3['ai_comments_found']} AI comments)")
    print(f"[VECTOR 4] Spatial Frequency      : {v4['risk_score']:5.1f}% Risk [{v4['status']}]")

    ent = matrix.get("entropy", {})
    if ent:
        print("\n📊 --- STATISTICAL ENTROPY READOUT ---")
        print(f" Shannon Entropy: {ent.get('shannon_entropy', 0.0)} bits/char")
        print(f" Type-Token Ratio: {ent.get('ttr', 0.0)}")
        print(f" Predictability  : {ent.get('predictability_score', 0.0)}%")
    print()


def clean_directory(dir_path: str, mode: str = "paranoid", rules_engine: RuleEngine = None, humanize: bool = True):
    """Recursively cleans all files in a directory using stealth mode."""
    target_path = Path(dir_path).resolve()
    if not target_path.exists():
        print(f"❌ Path not found: {dir_path}")
        sys.exit(1)

    watcher = DirectoryWatcher(str(target_path), perturb_stats=(mode in ["paranoid", "aggressive"]))
    count = watcher.scan_and_clean()
    print(f"\n🎉 Finished recursively sanitizing {count} files in {target_path} [Stealth Profile: {mode.upper()}, Humanized: {humanize}]")


def main():
    parser = argparse.ArgumentParser(
        prog="untrace",
        description="Untrace AI :: Enterprise Zero-Trust AI Provenance Firewall & Automatic Humanizer Engine"
    )
    subparsers = parser.add_subparsers(dest="command", help="Sub-command help")

    # clean-text
    clean_text_parser = subparsers.add_parser("clean-text", help="Sanitize inline text string or stdin (humanized by default)")
    clean_text_parser.add_argument("text", nargs="?", help="Text string to clean. If empty, reads from stdin.")
    clean_text_parser.add_argument("--mode", choices=["paranoid", "aggressive", "standard", "minimal"], default="paranoid", help="Stealth profile preset")
    clean_text_parser.add_argument("--tone", choices=["conversational", "casual", "tech-lead", "academic", "executive"], default="conversational", help="Humanizer tone persona")
    clean_text_parser.add_argument("--perturb", action="store_true", help="Rephrase statistical AI vocabulary markers")
    clean_text_parser.add_argument("--rules", help="Path to custom rules JSON file (.untracerules.json)")
    clean_text_parser.add_argument("--no-humanize", action="store_true", help="Disable automatic natural tone humanization")

    # clean-file
    clean_file_parser = subparsers.add_parser("clean-file", help="Sanitize file metadata, AI comments, zero-width watermarks (humanized by default)")
    clean_file_parser.add_argument("path", help="Path to file (PNG, JPEG, SVG, PDF, DOCX, IPYNB, PPTX, XLSX, HTML, MD, PY, JS, TS)")
    clean_file_parser.add_argument("--mode", choices=["paranoid", "aggressive", "standard", "minimal"], default="paranoid", help="Stealth profile preset")
    clean_file_parser.add_argument("--jitter", action="store_true", help="Apply sub-pixel LSB noise jitter to images")
    clean_file_parser.add_argument("--dct-jitter", action="store_true", help="Apply 2D DCT spectral noise modulation to images")
    clean_file_parser.add_argument("--perturb", action="store_true", help="Rephrase statistical AI vocabulary")
    clean_file_parser.add_argument("--rules", help="Path to custom rules JSON file (.untracerules.json)")
    clean_file_parser.add_argument("--no-humanize", action="store_true", help="Disable automatic natural tone humanization")

    # clean-dir
    clean_dir_parser = subparsers.add_parser("clean-dir", help="Recursively sanitize all files in a directory")
    clean_dir_parser.add_argument("path", nargs="?", default=".", help="Directory path to clean (default: current directory)")
    clean_dir_parser.add_argument("--mode", choices=["paranoid", "aggressive", "standard", "minimal"], default="paranoid", help="Stealth profile preset")
    clean_dir_parser.add_argument("--no-perturb", action="store_true", help="Disable vocabulary rephrasing")
    clean_dir_parser.add_argument("--rules", help="Path to custom rules JSON file (.untracerules.json)")
    clean_dir_parser.add_argument("--no-humanize", action="store_true", help="Disable automatic natural tone humanization")

    # humanize
    humanize_parser = subparsers.add_parser("humanize", help="Transform AI text tone into conversational human phrasing")
    humanize_parser.add_argument("input", nargs="?", help="Text string or file path to humanize. If empty, reads from stdin.")
    humanize_parser.add_argument("--tone", choices=["conversational", "casual", "tech-lead", "academic", "executive"], default="conversational", help="Humanizer tone persona")

    # clipboard
    clip_parser = subparsers.add_parser("clipboard", help="Run real-time background clipboard hygiene daemon")
    clip_parser.add_argument("--mode", choices=["paranoid", "aggressive", "standard", "minimal"], default="paranoid", help="Stealth profile preset")

    # install-hook / init-github-action
    subparsers.add_parser("install-hook", help="Install .git/hooks/pre-commit provenance hygiene hook")
    subparsers.add_parser("init-github-action", help="Generate .github/workflows/untrace-hygiene.yml workflow")

    # cert
    cert_parser = subparsers.add_parser("cert", help="Generate SHA-256 Zero-Trust Clean Certificate")
    cert_parser.add_argument("input", help="Text string or file path to certify")
    cert_parser.add_argument("-o", "--output", help="Output JSON certificate file path")

    # heatmap
    heatmap_parser = subparsers.add_parser("heatmap", help="Generate visual HTML forensics heatmap")
    heatmap_parser.add_argument("input", help="Text string or file path to analyze")
    heatmap_parser.add_argument("-o", "--output", default="untrace_heatmap.html", help="Output HTML heatmap file path")

    # matrix / audit / check
    matrix_parser = subparsers.add_parser("matrix", help="Evaluate 4-Vector Stego Risk Matrix for text string or file")
    matrix_parser.add_argument("input", help="Text string or file path to evaluate")

    check_parser = subparsers.add_parser("check", help="Audit text string or file for watermarks and AI telltales")
    check_parser.add_argument("input", help="Text string or file path to audit")

    # entropy
    entropy_parser = subparsers.add_parser("entropy", help="Calculate statistical entropy & AI predictability metrics")
    entropy_parser.add_argument("input", help="Text string or file path to analyze")

    # dashboard / ui
    dash_parser = subparsers.add_parser("dashboard", help="Launch interactive Cyber-Stealth Web Dashboard visualizer")
    dash_parser.add_argument("--port", type=int, default=8080, help="Port to run dashboard server on (default: 8080)")
    dash_parser.add_argument("--no-open", action="store_true", help="Do not auto-open browser")

    ui_parser = subparsers.add_parser("ui", help="Alias for dashboard")
    ui_parser.add_argument("--port", type=int, default=8080, help="Port to run dashboard server on")
    ui_parser.add_argument("--no-open", action="store_true", help="Do not auto-open browser")

    # init-rules
    rules_parser = subparsers.add_parser("init-rules", help="Generate starter .untracerules.json rules file")
    rules_parser.add_argument("path", nargs="?", default=".untracerules.json", help="Output path for rules file")
    rules_parser.add_argument("--force", action="store_true", help="Overwrite existing rules file")

    # watch
    watch_parser = subparsers.add_parser("watch", help="Watch directory in real time and automatically sanitize created/edited files")
    watch_parser.add_argument("path", nargs="?", default=".", help="Directory path to watch (default: current directory)")

    # server
    subparsers.add_parser("server", help="Launch Model Context Protocol (MCP) server for Claude Desktop")

    # install commands
    subparsers.add_parser("auto-install", help="1-click zero-command autopilot registration across Claude Code, Antigravity IDE, Cursor & Git")
    subparsers.add_parser("install-claude-code", help="Install Untrace skill to global ~/.claude/skills/")
    subparsers.add_parser("install-claude-desktop", help="Show configuration snippet for Claude Desktop")

    args = parser.parse_args()

    # Load custom rules engine if specified
    rules_engine = None
    if hasattr(args, "rules") and args.rules:
        try:
            rules_engine = RuleEngine.from_file(args.rules)
        except Exception as e:
            print(f"❌ Error loading rules file {args.rules}: {e}")
            sys.exit(1)

    if args.command == "clean-text":
        if args.text:
            input_text = args.text
        else:
            input_text = sys.stdin.read()
        should_humanize = not args.no_humanize
        cleaned = clean_text(input_text, perturb_stats=args.perturb, rules_engine=rules_engine, mode=args.mode, humanize=should_humanize, tone=args.tone)
        sys.stdout.write(cleaned)

    elif args.command == "clean-file":
        should_humanize = not args.no_humanize
        use_jitter = args.jitter or args.dct_jitter
        success, msg = clean_file(args.path, disrupt_image_pixels=use_jitter, perturb_stats=args.perturb, rules_engine=rules_engine, mode=args.mode, humanize=should_humanize)
        print(msg)
        sys.exit(0 if success else 1)

    elif args.command == "clean-dir":
        should_humanize = not args.no_humanize
        clean_directory(args.path, mode=args.mode, rules_engine=rules_engine, humanize=should_humanize)

    elif args.command == "humanize":
        if args.input:
            target_input = args.input
            if os.path.exists(target_input):
                with open(target_input, 'r', encoding='utf-8', errors='ignore') as f:
                    target_input = f.read()
        else:
            target_input = sys.stdin.read()
        
        humanized = HumanizerEngine.humanize(target_input, tone=args.tone)
        sys.stdout.write(humanized)

    elif args.command == "clipboard":
        daemon = ClipboardDaemon()
        daemon.start(mode=args.mode)

    elif args.command == "install-hook":
        msg = HookInstaller.install_git_hook()
        print(f"✅ {msg}")

    elif args.command == "init-github-action":
        msg = HookInstaller.generate_github_action()
        print(f"✅ {msg}")

    elif args.command == "cert":
        target_input = args.input
        source_name = target_input
        if os.path.exists(target_input):
            with open(target_input, 'r', encoding='utf-8', errors='ignore') as f:
                target_input = f.read()
        
        cleaned = clean_text(target_input)
        cert_data = AuditCertificateGenerator.generate_certificate(target_input, cleaned, source_name=source_name)
        out_file = AuditCertificateGenerator.save_certificate_file(cert_data, output_path=args.output)
        print(f"✅ Generated SHA-256 Zero-Trust Clean Certificate: {out_file}")
        print(f"Certificate ID: {cert_data['certificate_id']}")

    elif args.command == "heatmap":
        target_input = args.input
        if os.path.exists(target_input):
            with open(target_input, 'r', encoding='utf-8', errors='ignore') as f:
                target_input = f.read()

        out_file = HeatmapRenderer.save_heatmap_file(target_input, output_path=args.output)
        print(f"🔥 Generated Forensics Heatmap: {out_file}")

    elif args.command in ["matrix", "check"]:
        target_input = args.input
        file_ext = None
        if os.path.exists(target_input):
            file_ext = os.path.splitext(target_input)[1].lower()
            with open(target_input, 'r', encoding='utf-8', errors='ignore') as f:
                target_input = f.read()

        matrix = StegoRiskMatrix.evaluate(target_input, file_ext=file_ext)
        print_risk_matrix(matrix)

    elif args.command == "entropy":
        target_input = args.input
        if os.path.exists(target_input):
            with open(target_input, 'r', encoding='utf-8', errors='ignore') as f:
                target_input = f.read()

        res = EntropyAnalyzer.analyze(target_input)
        print("\n📊 --- STATISTICAL ENTROPY REPORT --- 📊\n")
        print(f"Shannon Entropy: {res['shannon_entropy']} bits/char")
        print(f"Type-Token Ratio: {res['ttr']}")
        print(f"Predictability Score: {res['predictability_score']}%")
        print(f"AI Likelihood Assessment: {res['ai_likelihood']}")
        print(f"Word Count: {res['word_count']} ({res['unique_word_count']} unique)")
        print(f"Avg Sentence Length: {res['avg_sentence_length']} words (std dev: {res['sentence_length_std']})")
        print()

    elif args.command in ["dashboard", "ui"]:
        launch_dashboard(port=args.port, open_browser=not args.no_open)

    elif args.command == "init-rules":
        msg = RuleEngine.create_starter_rules_file(filepath=args.path, overwrite=args.force)
        print(f"✅ {msg}")

    elif args.command == "watch":
        watcher = DirectoryWatcher(args.path)
        watcher.start()

    elif args.command == "server":
        run_server()

    elif args.command == "auto-install":
        from untrace.autoinstall import AutoInstaller
        res = AutoInstaller.install_all()
        print("🤖 --- UNTRACE AI ZERO-COMMAND AUTOPILOT REGISTRATION --- 🤖")
        for k, v in res.items():
            print(f"  ✅ Registered {k}: {v}")
        print("\n✨ Untrace AI is now operating 100% on autopilot across your AI coding environments!")

    elif args.command == "install-claude-code":
        install_claude_code()

    elif args.command == "install-claude-desktop":
        install_claude_desktop()

    else:
        print(ASCII_BANNER)
        parser.print_help()


if __name__ == "__main__":
    main()
