"""
Aphanis - Real-Time File System Watcher Module.
"""

import os
import sys
import time
from pathlib import Path
from typing import Set

from aphanis.cleaner import clean_file


class DirectoryWatcher:
    """Monitors a directory for file additions/modifications and automatically sanitizes them in real time."""

    IGNORE_DIRS = {'.git', '.idea', '.vscode', '__pycache__', 'node_modules', 'venv', '.venv'}
    IGNORE_EXTS = {'.pyc', '.pyo', '.png.tmp', '.log'}

    def __init__(self, watch_path: str, poll_interval: float = 1.0, perturb_stats: bool = True):
        self.watch_path = Path(watch_path).resolve()
        self.poll_interval = poll_interval
        self.perturb_stats = perturb_stats
        self._file_mtimes: dict[str, float] = {}

    def _should_ignore(self, path: Path) -> bool:
        parts = set(path.parts)
        if parts.intersection(self.IGNORE_DIRS):
            return True
        if path.suffix.lower() in self.IGNORE_EXTS:
            return True
        return False

    def scan_and_clean(self) -> int:
        cleaned_count = 0
        for root, dirs, files in os.walk(self.watch_path):
            # Exclude ignored directories in place
            dirs[:] = [d for d in dirs if d not in self.IGNORE_DIRS]

            for file_name in files:
                file_path = Path(root) / file_name
                if self._should_ignore(file_path):
                    continue

                try:
                    mtime = file_path.stat().st_mtime
                    path_str = str(file_path)

                    if path_str not in self._file_mtimes or self._file_mtimes[path_str] < mtime:
                        self._file_mtimes[path_str] = mtime
                        success, msg = clean_file(path_str, perturb_stats=self.perturb_stats)
                        if success:
                            # Update mtime after cleaning to avoid loop
                            self._file_mtimes[path_str] = file_path.stat().st_mtime
                            cleaned_count += 1
                            print(f"[Aphanis Watcher] ✨ Sanitized: {file_path.name}")

                except Exception as e:
                    pass

        return cleaned_count

    def start(self):
        print(f"[Aphanis Watcher] 🛡️ Watching {self.watch_path} for real-time AI watermark sanitization...")
        print("Press Ctrl+C to stop.\n")

        # Initial scan
        self.scan_and_clean()

        try:
            while True:
                time.sleep(self.poll_interval)
                self.scan_and_clean()
        except KeyboardInterrupt:
            print("\n[Aphanis Watcher] Stopped.")
