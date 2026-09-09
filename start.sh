#!/usr/bin/env bash
# Render build + deploy script for the Aphanis full-stack dashboard.
# 1. Build the React frontend into aphanis/dashboard_static/
# 2. Install the aphanis package (which ships the static dir via package-data)
set -euo pipefail

echo "🔧 Building React frontend..."
cd webapp
npm ci
npm run build
cd ..

echo "📦 Installing aphanis package..."
PYTHON="${PYTHON:-python3}"
"$PYTHON" -m pip install --upgrade pip
"$PYTHON" -m pip install .

echo "✅ Build complete. Static frontend:"
ls -la aphanis/dashboard_static/
