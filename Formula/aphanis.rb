# typed: false
# frozen_string_literal: true

class Aphanis < Formula
  desc "Enterprise Zero-Trust AI Provenance Firewall & Humanizer Engine"
  homepage "https://github.com/sanyamk23/aphanis"
  license "MIT"
  version "1.4.0"

  if OS.mac? && Hardware::CPU.intel?
    url "https://github.com/sanyamk23/aphanis/releases/download/v1.4.0/aphanis-macos-x86_64"
    sha256 "REPLACE_WITH_INTEL_HASH"
  elsif OS.mac? && Hardware::CPU.arm?
    url "https://github.com/sanyamk23/aphanis/releases/download/v1.4.0/aphanis-macos-arm64"
    sha256 "REPLACE_WITH_ARM_HASH"
  elsif OS.linux?
    url "https://github.com/sanyamk23/aphanis/releases/download/v1.4.0/aphanis-linux-x86_64"
    sha256 "REPLACE_WITH_LINUX_HASH"
  end

  def install
    binary_name = "aphanis"
    if OS.mac? && Hardware::CPU.intel?
      binary_url = "https://github.com/sanyamk23/aphanis/releases/download/v1.4.0/aphanis-macos-x86_64"
    elsif OS.mac? && Hardware::CPU.arm?
      binary_url = "https://github.com/sanyamk23/aphanis/releases/download/v1.4.0/aphanis-macos-arm64"
    elsif OS.linux?
      binary_url = "https://github.com/sanyamk23/aphanis/releases/download/v1.4.0/aphanis-linux-x86_64"
    end

    system "curl", "-L", binary_url, "-o", binary_name
    chmod 0755, binary_name
    bin.install binary_name
  end

  test do
    system bin/"aphanis", "--help"
  end
end