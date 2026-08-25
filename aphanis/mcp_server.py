"""
Aphanis :: Zero-Trust AI Provenance Firewall & Automatic Humanizer - MCP Server.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aphanis.cleaner import clean_text, clean_file, StatisticalPerturber
from aphanis.entropy import EntropyAnalyzer
from aphanis.stealth import StegoRiskMatrix
from aphanis.humanizer import HumanizerEngine
from aphanis.cert import AuditCertificateGenerator


def create_mcp_server():
    """Initializes and configures the MCP server."""
    try:
        from mcp.server.fastmcp import FastMCP
        mcp = FastMCP(
            name="Aphanis Firewall & Humanizer",
            instructions="Zero-Trust AI Provenance Firewall & Humanizer Engine: Strips zero-width watermarks, C2PA metadata, and automatically converts AI text into a natural human tone."
        )

        @mcp.tool()
        def sanitize_text(text: str, mode: str = "paranoid", perturb_statistical_watermarks: bool = False, humanize: bool = True, tone: str = "conversational") -> str:
            """
            Sanitizes text and automatically humanizes tone using Stealth Engine profiles.
            
            :param text: Raw input text to sanitize.
            :param mode: Stealth profile preset (paranoid, aggressive, standard, minimal).
            :param perturb_statistical_watermarks: Rephrase common AI statistical vocabulary markers.
            :param humanize: Synthesize contractions and eliminate robotic filler phrases for a human tone.
            :param tone: Humanizer tone persona (conversational, casual, tech-lead, academic, executive).
            :return: Cleaned and humanized text free of invisible watermarks.
            """
            return clean_text(text, perturb_stats=perturb_statistical_watermarks, mode=mode, humanize=humanize, tone=tone)

        @mcp.tool()
        def humanize_text_tool(text: str, tone: str = "conversational") -> str:
            """
            Transforms formal robotic AI output into natural conversational human text (contractions, phrase reduction).
            
            :param text: Input text.
            :param tone: Humanizer tone persona (conversational, casual, tech-lead, academic, executive).
            :return: Humanized text.
            """
            return HumanizerEngine.humanize(text, tone=tone)

        @mcp.tool()
        def sanitize_file(file_path: str, mode: str = "paranoid", disrupt_image_pixels: bool = False) -> str:
            """
            Sanitizes file metadata, C2PA manifests, comments, and humanizes text content.
            
            :param file_path: Absolute path to file.
            :param mode: Stealth profile preset.
            :param disrupt_image_pixels: Apply sub-pixel LSB noise jitter to disrupt spatial image watermarks.
            :return: Status message.
            """
            success, msg = clean_file(file_path, disrupt_image_pixels=disrupt_image_pixels, mode=mode)
            return msg

        @mcp.tool()
        def evaluate_risk_matrix(text: str) -> str:
            """
            Evaluates the 4-Vector Stego Risk Matrix (Unicode, Statistical Model, Metadata, Spatial Frequency).
            
            :param text: Input text string.
            :return: JSON formatted 4-Vector Risk Assessment report.
            """
            import json
            matrix = StegoRiskMatrix.evaluate(text)
            return json.dumps(matrix, indent=2)

        @mcp.tool()
        def generate_audit_certificate(text: str) -> str:
            """
            Generates a signed SHA-256 Zero-Trust Clean Certificate JSON.
            
            :param text: Input text string.
            :return: JSON formatted Audit Certificate.
            """
            import json
            cleaned = clean_text(text)
            cert = AuditCertificateGenerator.generate_certificate(text, cleaned)
            return json.dumps(cert, indent=2)

        return mcp

    except ImportError:
        import json

        class FallbackStdioMCPServer:
            def run(self):
                print("Running Stdio Fallback MCP Server for Aphanis Firewall", file=sys.stderr)
                while True:
                    line = sys.stdin.readline()
                    if not line:
                        break
                    try:
                        req = json.loads(line)
                        req_id = req.get("id")
                        method = req.get("method")
                        params = req.get("params", {})

                        if method == "initialize":
                            resp = {
                                "jsonrpc": "2.0",
                                "id": req_id,
                                "result": {
                                    "protocolVersion": "2024-11-05",
                                    "capabilities": {"tools": {}},
                                    "serverInfo": {"name": "Aphanis Firewall & Humanizer", "version": "1.4.0"}
                                }
                            }
                        elif method == "tools/list":
                            resp = {
                                "jsonrpc": "2.0",
                                "id": req_id,
                                "result": {
                                    "tools": [
                                        {
                                            "name": "sanitize_text",
                                            "description": "Sanitize and humanize text using Stealth Engine presets",
                                            "inputSchema": {
                                                "type": "object",
                                                "properties": {
                                                    "text": {"type": "string"},
                                                    "mode": {"type": "string"}
                                                },
                                                "required": ["text"]
                                            }
                                        },
                                        {
                                            "name": "humanize_text_tool",
                                            "description": "Transform text into conversational human tone",
                                            "inputSchema": {
                                                "type": "object",
                                                "properties": {
                                                    "text": {"type": "string"},
                                                    "tone": {"type": "string"}
                                                },
                                                "required": ["text"]
                                            }
                                        },
                                        {
                                            "name": "evaluate_risk_matrix",
                                            "description": "Evaluate 4-Vector Stego Risk Matrix",
                                            "inputSchema": {
                                                "type": "object",
                                                "properties": {
                                                    "text": {"type": "string"}
                                                },
                                                "required": ["text"]
                                            }
                                        }
                                    ]
                                }
                            }
                        elif method == "tools/call":
                            name = params.get("name")
                            args = params.get("arguments", {})
                            if name == "sanitize_text":
                                res = clean_text(args.get("text", ""), mode=args.get("mode", "paranoid"))
                            elif name == "humanize_text_tool":
                                res = HumanizerEngine.humanize(args.get("text", ""), tone=args.get("tone", "conversational"))
                            elif name == "evaluate_risk_matrix":
                                res = json.dumps(StegoRiskMatrix.evaluate(args.get("text", "")), indent=2)
                            else:
                                res = "Unknown tool"

                            resp = {
                                "jsonrpc": "2.0",
                                "id": req_id,
                                "result": {
                                    "content": [{"type": "text", "text": res}]
                                }
                            }
                        else:
                            resp = {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

                        sys.stdout.write(json.dumps(resp) + "\n")
                        sys.stdout.flush()
                    except Exception as e:
                        sys.stderr.write(f"Error handling MCP request: {e}\n")

        return FallbackStdioMCPServer()


def main():
    """Runs the MCP server over stdio."""
    server = create_mcp_server()
    server.run()


if __name__ == "__main__":
    main()
