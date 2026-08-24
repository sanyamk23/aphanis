# typed: false
# frozen_string_literal: true

class UntraceAi < Formula
  desc "Enterprise Zero-Trust AI Provenance Firewall & Humanizer Engine"
  homepage "https://github.com/sanyamk23/untrace-ai"
  license "MIT"
  version "1.4.0"

  if OS.mac? && Hardware::CPU.intel?
    url "https://github.com/sanyamk23/untrace-ai/releases/download/v1.4.0/untrace-macos-x86_64"
    sha256 "REPLACE_WITH_INTEL_HASH"
  elsif OS.mac? && Hardware::CPU.arm?
    url "https://github.com/sanyamk23/untrace-ai/releases/download/v1.4.0/untrace-macos-arm64"
    sha256 "REPLACE_WITH_ARM_HASH"
  elsif OS.linux?
    url "https://github.com/sanyamk23/untrace-ai/releases/download/v1.4.0/untrace-linux-x86_64"
    sha256 "REPLACE_WITH_LINUX_HASH"
  end

  def install
    binary_name = "untrace"
    if OS.mac? && Hardware::CPU.intel?
      binary_url = "https://github.com/sanyamk23/untrace-ai/releases/download/v1.4.0/untrace-macos-x86_64"
    elsif OS.mac? && Hardware::CPU.arm?
      binary_url = "https://github.com/sanyamk23/untrace-ai/releases/download/v1.4.0/untrace-macos-arm64"
    elsif OS.linux?
      binary_url = "https://github.com/sanyamk23/untrace-ai/releases/download/v1.4.0/untrace-linux-x86_64"
    end

    system "curl", "-L", binary_url, "-o", binary_name
    chmod 0755, binary_name
    bin.install binary_name
  end

  test do
    system bin/"untrace", "--help"
  end
end