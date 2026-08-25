"use strict";

const https = require("https");
const { execSync } = require("child_process");
const fs = require("fs");
const path = require("path");

const REPO = "sanyamk23/aphanis";
const VERSION = "1.4.0";
const GITHUB_API = `https://api.github.com/repos/${REPO}/releases/tags/v${VERSION}`;

function detectPlatform() {
  const platform = process.platform;
  const arch = process.arch;
  let osName, archName;

  if (platform === "darwin") osName = "macos";
  else if (platform === "linux") osName = "linux";
  else if (platform === "win32") osName = "windows";
  else throw new Error(`Unsupported platform: ${platform}`);

  if (arch === "arm64" || arch === "aarch64") archName = "arm64";
  else if (arch === "x64" || arch === "amd64") archName = "x86_64";
  else throw new Error(`Unsupported architecture: ${arch}`);

  return { osName, archName, platformKey: `${osName}-${archName}` };
}

function download(url, dest) {
  return new Promise((resolve, reject) => {
    const file = fs.createWriteStream(dest);
    https.get(url, (response) => {
      if (response.statusCode !== 200) {
        reject(new Error(`Request failed: ${response.statusCode}`));
        return;
      }
      response.pipe(file);
      file.on("finish", () => file.close(resolve));
    }).on("error", (err) => {
      fs.unlink(dest, () => {});
      reject(err);
    });
  });
}

async function main() {
  const { osName, archName, platformKey } = detectPlatform();
  const binDir = path.join(__dirname, "bin");
  fs.mkdirSync(binDir, { recursive: true });

  const binaryName = platformKey === "windows-x86_64" ? "aphanis.exe" : "aphanis";
  const url = `https://github.com/${REPO}/releases/download/v${VERSION}/${binaryName}-${platformKey}`;
  const dest = path.join(binDir, binaryName);

  console.log(`📥 Downloading Aphanis v${VERSION} for ${platformKey}...`);

  try {
    await download(url, dest);
    if (platformKey !== "windows-x86_64") {
      fs.chmodSync(dest, 0o755);
    }
    console.log(`✅ Installed to ${dest}`);
  } catch (err) {
    console.error(`❌ Download failed: ${err.message}`);
    console.error("   Falling back to Python package...");
    try {
      execSync("pip3 install aphanis", { stdio: "inherit" });
      console.log("✅ Installed via pip (Python required)");
    } catch (e) {
      console.error("❌ Python fallback also failed.");
      console.error("   Manual install: curl -fsSL https://aphanis.ai/install.sh | bash");
      process.exit(1);
    }
  }
}

main();
