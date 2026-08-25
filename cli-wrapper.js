#!/usr/bin/env node
"""Wrapper that invokes the bundled Python module or standalone binary."""

const { spawnSync } = require('child_process');
const path = require('path');
const fs = require('fs');

const binDir = path.join(__dirname, 'bin');
const platform = process.platform;
const arch = process.arch;

let binaryName;
if (platform === 'darwin') {
  binaryName = arch === 'arm64' ? 'aphanis-darwin-arm64' : 'aphanis-darwin-x64';
} else if (platform === 'linux') {
  binaryName = arch === 'arm64' ? 'aphanis-linux-arm64' : 'aphanis-linux-x64';
} else if (platform === 'win32') {
  binaryName = 'aphanis-windows-x64.exe';
} else {
  binaryName = 'aphanis';
}

const binaryPath = path.join(binDir, binaryName);

// If standalone binary exists, use it
if (fs.existsSync(binaryPath)) {
  const result = spawnSync(binaryPath, process.argv.slice(2), { stdio: 'inherit' });
  process.exit(result.status || 0);
}

// Fallback: use system python with aphanis package
const pyResult = spawnSync('python3', ['-m', 'aphanis.cli', ...process.argv.slice(2)], { stdio: 'inherit' });
if (pyResult.status !== 0) {
  console.error('❌ Aphanis: No standalone binary found and Python aphanis package not installed.');
  console.error('   Install with: curl -fsSL https://aphanis.ai/install.sh | bash');
  process.exit(1);
}
process.exit(pyResult.status || 0);
