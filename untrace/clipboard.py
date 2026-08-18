"""
Untrace AI - Clipboard Hygiene Daemon.
Monitors system clipboard in real time, automatically stripping zero-width spaces,
C2PA traces, and applying natural humanization to copied text.
"""

import sys
import time
import subprocess
from typing import Optional

from untrace.cleaner import clean_text


class ClipboardDaemon:
    """Monitors system clipboard and sanitizes copied text in real time."""

    @staticmethod
    def get_clipboard() -> str:
        """Reads text from system clipboard."""
        try:
            if sys.platform == 'darwin':
                return subprocess.check_output(['pbpaste'], text=True)
            elif sys.platform.startswith('linux'):
                return subprocess.check_output(['xclip', '-selection', 'clipboard', '-o'], text=True)
            elif sys.platform == 'win32':
                return subprocess.check_output(['powershell', '-command', 'Get-Clipboard'], text=True)
        except Exception:
            pass
        return ""

    @staticmethod
    def set_clipboard(text: str):
        """Writes text to system clipboard."""
        try:
            if sys.platform == 'darwin':
                p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE, text=True)
                p.communicate(input=text)
            elif sys.platform.startswith('linux'):
                p = subprocess.Popen(['xclip', '-selection', 'clipboard'], stdin=subprocess.PIPE, text=True)
                p.communicate(input=text)
            elif sys.platform == 'win32':
                p = subprocess.Popen(['powershell', '-command', 'Set-Clipboard'], stdin=subprocess.PIPE, text=True)
                p.communicate(input=text)
        except Exception:
            pass

    def start(self, poll_interval: float = 0.8, mode: str = "paranoid"):
        """Starts real-time background clipboard monitoring loop."""
        print(f"📋 Untrace AI Clipboard Hygiene Daemon Active... [Mode: {mode.upper()}]")
        print("Press Ctrl+C to stop.\n")

        last_text = ""
        try:
            while True:
                curr_text = self.get_clipboard()
                if curr_text and curr_text != last_text:
                    cleaned = clean_text(curr_text, mode=mode, humanize=True)
                    if cleaned != curr_text:
                        self.set_clipboard(cleaned)
                        print("✨ Sanitized and humanized copied text on clipboard!")
                    last_text = cleaned
                time.sleep(poll_interval)
        except KeyboardInterrupt:
            print("\n🛑 Clipboard Daemon stopped.")
