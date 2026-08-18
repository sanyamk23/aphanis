"""
Untrace AI - Model Context Protocol (MCP) Server for Claude Desktop & Agents.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from untrace.cleaner import clean_text, clean_file, StatisticalPerturber


def create_mcp_server():
    """Initializes and configures the MCP server."""
    try:
        from mcp.server.fastmcp import FastMCP
        mcp = FastMCP(
            name="Untrace AI",
            instructions="Provenance & AI Watermark Sanitizer: Strips zero-width tracking marks, C2PA/EXIF metadata, and statistical LLM watermarks."
        )

        @mcp.tool()
        def sanitize_text(text: str, perturb_statistical_watermarks: bool = False) -> str:
            """
            Strips zero-width spaces, invisible unicode characters, tag characters, homoglyphs, and optionally statistical AI watermarks from text.
            
            :param text: Raw input text to sanitize.
            :param perturb_statistical_watermarks: Set to true to rephrase common AI statistical vocabulary markers.
            :return: Cleaned text free of invisible watermarks.
            """
            return clean_text(text, perturb_stats=perturb_statistical_watermarks)

        @mcp.tool()
        def sanitize_file(file_path: str, disrupt_image_pixels: bool = False) -> str:
            """
            Strips EXIF, C2PA, XMP metadata, XML/HTML comments, and zero-width characters from PNG, JPEG, SVG, PDF, DOCX, HTML, or Markdown files.
            
            :param file_path: Absolute path to the file to sanitize.
            :param disrupt_image_pixels: Apply sub-pixel LSB noise jitter to disrupt spatial image watermarks.
            :return: Outcome status message.
            """
            success, msg = clean_file(file_path, disrupt_image_pixels=disrupt_image_pixels)
            return msg

        @mcp.tool()
        def perturb_text(text: str) -> str:
            """
            Rephrases statistical AI marker vocabulary (e.g. 'delve', 'testament', 'spearhead', 'crucial', 'tapestry') to defeat statistical n-gram AI detectors.
            
            :param text: Input text string.
            :return: Rephrased text.
            """
            return StatisticalPerturber.perturb(text)

        return mcp

    except ImportError:
        import json

        class FallbackStdioMCPServer:
            def run(self):
                print("Running Stdio Fallback MCP Server for Untrace AI", file=sys.stderr)
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
                                    "serverInfo": {"name": "Untrace AI", "version": "1.0.0"}
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
                                            "description": "Strip zero-width spaces & invisible watermarks from text",
                                            "inputSchema": {
                                                "type": "object",
                                                "properties": {
                                                    "text": {"type": "string"},
                                                    "perturb_statistical_watermarks": {"type": "boolean"}
                                                },
                                                "required": ["text"]
                                            }
                                        },
                                        {
                                            "name": "sanitize_file",
                                            "description": "Strip metadata and watermarks from files",
                                            "inputSchema": {
                                                "type": "object",
                                                "properties": {
                                                    "file_path": {"type": "string"},
                                                    "disrupt_image_pixels": {"type": "boolean"}
                                                },
                                                "required": ["file_path"]
                                            }
                                        }
                                    ]
                                }
                            }
                        elif method == "tools/call":
                            name = params.get("name")
                            args = params.get("arguments", {})
                            if name == "sanitize_text":
                                res = clean_text(args.get("text", ""), args.get("perturb_statistical_watermarks", False))
                            elif name == "sanitize_file":
                                _, res = clean_file(args.get("file_path", ""), args.get("disrupt_image_pixels", False))
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
