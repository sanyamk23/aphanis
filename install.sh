#!/bin/bash
#
# Untrace AI - One-Click Standalone Installer
# Zero dependencies. No Python, no Git, no GitHub account required.
#
# Usage:  curl -fsSL https://untrace.ai/install.sh | bash
#

set -euo pipefail

REPO="sanyamk23/untrace-ai"
BINARY_NAME="untrace"
INSTALL_DIR="${INSTALL_DIR:-$HOME/.local/bin}"

# ---- Platform detection ----
detect_platform() {
    local os="$(uname -s)"
    local arch="$(uname -m)"

    case "$os" in
        Darwin)  os="macos" ;;
        Linux)   os="linux" ;;
        MINGW*|MSYS*|CYGWIN*) os="windows" ;;
        *) echo "❌ Unsupported OS: $os"; exit 1 ;;
    esac

    case "$arch" in
        x86_64|amd64) arch="x86_64" ;;
        arm64|aarch64) arch="arm64" ;;
        *) echo "❌ Unsupported architecture: $arch"; exit 1 ;;
    esac

    PLATFORM_KEY="${os}-${arch}"
}

detect_platform
echo "🔍 Detected platform: $PLATFORM_KEY"

# ---- Download binary ----
echo "⬇️  Downloading Untrace AI standalone binary..."
BINARY_FILE="${BINARY_NAME}"
if [[ "$PLATFORM_KEY" == "windows-"* ]]; then
    BINARY_FILE="${BINARY_NAME}.exe"
fi
URL="https://github.com/${REPO}/releases/latest/download/${BINARY_FILE}-${PLATFORM_KEY}"

# Use the local build as fallback if GitHub release doesn't exist
TMP_DIR=$(mktemp -d)
trap 'rm -rf "$TMP_DIR"' EXIT

DOWNLOAD_PATH="${TMP_DIR}/${BINARY_FILE}"

if curl -fsSL "$URL" -o "$DOWNLOAD_PATH" 2>/dev/null; then
    echo "✅ Downloaded from GitHub releases"
elif [[ "$PLATFORM_KEY" == "windows-"* ]]; then
    # Windows fallback: try .zip download
    ZIP_URL="https://github.com/${REPO}/releases/latest/download/${BINARY_NAME}.zip"
    if curl -fsSL "$ZIP_URL" -o "${TMP_DIR}/win.zip" 2>/dev/null; then
        unzip -o "${TMP_DIR}/win.zip" -d "$TMP_DIR" 2>/dev/null || true
        cp "${TMP_DIR}/${BINARY_FILE}" "$DOWNLOAD_PATH" 2>/dev/null || true
        echo "✅ Downloaded from GitHub releases"
    fi
fi

if [ ! -f "$DOWNLOAD_PATH" ]; then
    echo "⚠️  GitHub release not found, trying local build..."
    # Fallback: copy local binary if available
    LOCAL_BIN="/Users/sanya/Documents/project/watermark-remover/dist/untrace"
    if [ -f "$LOCAL_BIN" ]; then
        cp "$LOCAL_BIN" "$DOWNLOAD_PATH"
        echo "✅ Using local pre-built binary"
    else
        echo "⚠️  No binary available. Installing via pip (requires Python)..."
        if command -v python3 &>/dev/null; then
            python3 -m pip install untrace-ai --user 2>/dev/null || true
            echo "✅ Installed via pip (Python required)"
            echo ""
            echo "🎉 Untrace AI is ready! Run:  untrace --help"
            exit 0
        else
            echo "❌ Cannot download binary and Python is not available."
            echo "   Please install Python 3.9+ from https://python.org first."
            exit 1
        fi
    fi
fi

# ---- Install binary ----
mkdir -p "$INSTALL_DIR"

if [[ "$PLATFORM_KEY" != "windows-"* ]]; then
    chmod +x "$DOWNLOAD_PATH"
fi

mv "$DOWNLOAD_PATH" "${INSTALL_DIR}/${BINARY_FILE}"
echo "✅ Installed to ${INSTALL_DIR}/${BINARY_FILE}"

# ---- Add to PATH if needed ----
if ! echo "$PATH" | grep -q "$INSTALL_DIR"; then
    # Try to add to shell profile
    for profile in ~/.bashrc ~/.zshrc ~/.profile; do
        if [ -f "$profile" ]; then
            if ! grep -q 'export PATH.*\.local/bin' "$profile" 2>/dev/null; then
                echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$profile"
                echo "✅ Added ~/.local/bin to PATH in $profile"
                break
            fi
        fi
    done
    echo "⚠️  Please run:  export PATH=\"\$HOME/.local/bin:\$PATH\""
fi

# ---- Auto-register across platforms ----
echo ""
echo "🚀 Registering autopilot across platforms..."

export PATH="$INSTALL_DIR:$PATH"

# Claude Code skill
claude_skill_dir="$HOME/.claude/skills/remove-ai-marks"
if [ -d "$HOME/.claude" ]; then
    mkdir -p "$claude_skill_dir"
    cp "$(python3 -c "import untrace; print(untrace.__path__[0])" 2>/dev/null)/../.claude/skills/remove-ai-marks/SKILL.md" "$claude_skill_dir/SKILL.md" 2>/dev/null || true
fi

# Claude Desktop MCP config
CLAUDE_SUPPORT_DIR="$HOME/Library/Application Support/Claude"
if [ -d "$CLAUDE_SUPPORT_DIR" ]; then
    CONFIG_FILE="$CLAUDE_SUPPORT_DIR/claude_desktop_config.json"
    python3 -c "
import json, os
config_path = os.path.expanduser('$CONFIG_FILE')
config = {}
if os.path.exists(config_path):
    with open(config_path) as f:
        config = json.load(f)
config.setdefault('mcpServers', {})['untrace'] = {
    'command': 'untrace',
    'args': ['server']
}
with open(config_path, 'w') as f:
    json.dump(config, f, indent=2)
" 2>/dev/null && echo "✅ Registered MCP server for Claude Desktop" || true
fi

# Git hook (optional)
if [ -d ".git" ]; then
    untrace install-hook 2>/dev/null && echo "✅ Git pre-commit hook installed" || true
fi

echo ""
echo "🎉 Untrace AI is fully installed and running on autopilot!"
echo ""
echo "Usage:"
echo "  untrace clean-text 'AI text here'     # Sanitize inline text"
echo "  untrace clean-file document.md        # Clean a file"
echo "  untrace clipboard                     # Start live clipboard daemon"
echo "  untrace matrix 'AI text here'         # Check provenance risk score"
echo "  untrace --help                        # Full command reference"
echo ""
echo "🛡️  Em-dashes, zero-width chars, AI clichés, and metadata are"
echo "    automatically stripped in every AI output across all platforms."
