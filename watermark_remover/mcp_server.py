"""Model Context Protocol (MCP) Server for Watermark Remover."""

import sys
import os

# Add package directory to path if executed directly
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from watermark_remover.cleaner import clean_text, clean_file, StatisticalPerturber


def create_mcp_server():
    """Initializes and configures the MCP server."""
    try:
        from mcp.server.fastmcp import FastMCP
        mcp = FastMCP(
            name="Watermark Remover",
            instructions="Tools to strip multi-vendor AI provenance signals, zero-width tracking marks, C2PA/EXIF metadata, and statistical watermarks."
        )

        @mcp.tool()
        def sanitize_text(text: str, perturb_statistical_watermarks: bool = False) -> str:
            """
            Strips zero-width spaces, invisible unicode characters, homoglyphs, and optionally statistical AI watermarks from text.
            
            :param text: The raw text string to sanitize.
            :param perturb_statistical_watermarks: Set to true to rephrase common AI statistical marker words.
            :return: Cleaned text free of invisible watermarks.
            """
            return clean_text(text, perturb_stats=perturb_statistical_watermarks)

        @mcp.tool()
        def sanitize_file(file_path: str) -> str:
            """
            Strips EXIF, C2PA, XMP metadata, XML/HTML comments, and invisible characters from PNG, JPEG, SVG, PDF, DOCX, HTML, or Markdown files.
            
            :param file_path: Absolute path to the file to sanitize.
            :return: Status message detailing the outcome.
            """
            success, msg = clean_file(file_path)
            return msg

        @mcp.tool()
        def perturb_text(text: str) -> str:
            """
            Rephrases statistical AI marker vocabulary (e.g. 'delve', 'testament', 'spearhead', 'crucial') to defeat statistical n-gram AI detectors.
            
            :param text: Input text string.
            :return: Rephrased text with altered statistical markers.
            """
            return StatisticalPerturber.perturb(text)

        return mcp

    except ImportError:
        # Fallback stdio server implementation if fastmcp module is missing
        import json

        class FallbackStdioMCPServer:
            def run(self):
                print("Running Stdio Fallback MCP Server", file=sys.stderr)
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
                                    "serverInfo": {"name": "Watermark Remover", "version": "0.1.0"}
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
                                                    "file_path": {"type": "string"}
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
                                _, res = clean_file(args.get("file_path", ""))
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
