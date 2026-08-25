#!/bin/bash
#
# Aphanis - System-wide installer (requires sudo/root)
# Installs the binary into /usr/local/bin so ALL users have access.
#
# Usage:  curl -fsSL https://aphanis.ai/install-system.sh | sudo bash
#

set -euo pipefail

REPO="sanyamk23/aphanis"
VERSION="1.4.0"
INSTALL_DIR="/usr/local/bin"

# ---- Detect platform ----
detect_platform() {
    local kernel="$(uname -s)"
    local machine="$(uname -m)"

    case "$kernel" in
        Darwin)  os="macos" ;;
        Linux)   os="linux" ;;
        MINGW*|MSYS*|CYGWIN*) os="windows" ;;
        *) echo "❌ Unsupported OS: $kernel"; exit 1 ;;
    esac

    case "$machine" in
        x86_64|amd64) arch="x86_64" ;;
        arm64|aarch64) arch="arm64" ;;
        *) echo "❌ Unsupported architecture: $machine"; exit 1 ;;
    esac

    PLATFORM_KEY="${os}-${arch}"
}

if [ "$(id -u)" -ne 0 ]; then
    echo "⚠️  System-wide install requires root. Use: sudo curl -fsSL https://aphanis.ai/install-system.sh | sudo bash"
    echo "   Or for user-only install: curl -fsSL https://aphanis.ai/install.sh | bash"
    exit 1
fi

detect_platform
echo "🔍 Detected platform: $PLATFORM_KEY"
echo "📥 Downloading Aphanis v$VERSION..."

TMP_DIR=$(mktemp -d)
trap 'rm -rf "$TMP_DIR"' EXIT

BINARY_FILE="aphanis"
if [[ "$PLATFORM_KEY" == "windows-"* ]]; then
    BINARY_FILE="aphanis.exe"
    URL="https://github.com/${REPO}/releases/download/v${VERSION}/${BINARY_FILE}-${PLATFORM_KEY}.zip"
    curl -fsSL "$URL" -o "${TMP_DIR}/win.zip" || {
        echo "❌ Download failed"; exit 1
    }
    unzip -o "${TMP_DIR}/win.zip" -d "$TMP_DIR" 2>/dev/null || true
    SOURCE_FILE="${TMP_DIR}/${BINARY_FILE}"
else
    URL="https://github.com/${REPO}/releases/download/v${VERSION}/${BINARY_FILE}-${PLATFORM_KEY}"
    curl -fsSL "$URL" -o "${TMP_DIR}/${BINARY_FILE}" || {
        echo "❌ Download failed"; exit 1
    }
    chmod +x "${TMP_DIR}/${BINARY_FILE}"
    SOURCE_FILE="${TMP_DIR}/${BINARY_FILE}"
fi

mkdir -p "$INSTALL_DIR"
cp "$SOURCE_FILE" "${INSTALL_DIR}/${BINARY_FILE}"
chmod 755 "${INSTALL_DIR}/${BINARY_FILE}"

echo "✅ Installed Aphanis to ${INSTALL_DIR}/${BINARY_FILE}"
echo ""

# Register system-wide MCP server
if [ -d "/etc/claude-desktop" ]; then
    echo "✅ System-wide Claude Desktop config directory detected"
fi

echo "🎉 Aphanis v$VERSION is now available to ALL users on this system!"
echo ""
echo "Run:  aphanis --help"