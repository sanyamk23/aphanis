"""Tests for the Aphanis full-stack REST API server."""

import json
import threading
import time
import unittest
from http.client import HTTPConnection
from io import BytesIO

from aphanis.api_server import APIRequestHandler, _ThreadingHTTPServer


def _start_server(port: int = 0) -> tuple:
    server = _ThreadingHTTPServer(("127.0.0.1", port), APIRequestHandler)
    actual_port = server.server_address[1]
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()
    return server, actual_port


def _request(port: int, method: str, path: str, body: dict | bytes | None = None, headers: dict | None = None):
    conn = HTTPConnection("127.0.0.1", port, timeout=5)
    hdrs = headers or {}
    if isinstance(body, dict):
        body = json.dumps(body).encode("utf-8")
        hdrs.setdefault("Content-Type", "application/json")
    elif isinstance(body, bytes):
        hdrs.setdefault("Content-Type", "application/octet-stream")
    conn.request(method, path, body=body, headers=hdrs)
    resp = conn.getresponse()
    data = resp.read()
    conn.close()
    return resp.status, data


class TestHealthEndpoint(unittest.TestCase):
    def setUp(self):
        self.server, self.port = _start_server()

    def tearDown(self):
        self.server.shutdown()

    def test_health(self):
        status, data = _request(self.port, "GET", "/api/health")
        self.assertEqual(status, 200)
        body = json.loads(data)
        self.assertEqual(body["status"], "ok")


class TestAuditEndpoint(unittest.TestCase):
    def setUp(self):
        self.server, self.port = _start_server()

    def tearDown(self):
        self.server.shutdown()

    def test_audit_detects_ai_vocab(self):
        status, data = _request(self.port, "POST", "/api/audit", {"text": "Furthermore, it is important to note that this necessitates a paradigm shift."})
        self.assertEqual(status, 200)
        body = json.loads(data)
        self.assertIn("audit", body)
        self.assertIn("entropy", body)
        self.assertIn("risk_matrix", body)
        self.assertGreater(body["audit"]["score"], 0)

    def test_audit_clean_text(self):
        status, data = _request(self.port, "POST", "/api/audit", {"text": "hello world"})
        self.assertEqual(status, 200)
        body = json.loads(data)
        self.assertEqual(body["audit"]["status"], "CLEAN")

    def test_audit_empty_body(self):
        status, data = _request(self.port, "POST", "/api/audit", {})
        self.assertEqual(status, 200)


class TestCleanEndpoint(unittest.TestCase):
    def setUp(self):
        self.server, self.port = _start_server()

    def tearDown(self):
        self.server.shutdown()

    def test_clean_with_mode(self):
        status, data = _request(self.port, "POST", "/api/clean", {
            "text": "Furthermore, it is important to note that.",
            "mode": "paranoid",
            "tone": "conversational",
            "perturb": False,
            "humanize": True,
        })
        self.assertEqual(status, 200)
        body = json.loads(data)
        self.assertIn("cleaned", body)
        self.assertEqual(body["mode"], "paranoid")

    def test_clean_invalid_mode(self):
        status, data = _request(self.port, "POST", "/api/clean", {"text": "hi", "mode": "bogus"})
        self.assertEqual(status, 400)
        body = json.loads(data)
        self.assertIn("error", body)


class TestOtherEndpoints(unittest.TestCase):
    def setUp(self):
        self.server, self.port = _start_server()

    def tearDown(self):
        self.server.shutdown()

    def test_matrix(self):
        status, data = _request(self.port, "POST", "/api/matrix", {"text": "hello world"})
        self.assertEqual(status, 200)
        body = json.loads(data)
        self.assertIn("overall_clean_score", body)

    def test_entropy(self):
        status, data = _request(self.port, "POST", "/api/entropy", {"text": "hello world"})
        self.assertEqual(status, 200)
        body = json.loads(data)
        self.assertIn("shannon_entropy", body)

    def test_provenance(self):
        status, data = _request(self.port, "POST", "/api/provenance", {"text": "hello"})
        self.assertEqual(status, 200)
        body = json.loads(data)
        self.assertIn("verdict", body)
        self.assertIn("signature", body)

    def test_cert(self):
        status, data = _request(self.port, "POST", "/api/cert", {"text": "hello"})
        self.assertEqual(status, 200)
        body = json.loads(data)
        self.assertIn("certificate_id", body)
        self.assertIn("hashes", body)

    def test_scrub(self):
        status, data = _request(self.port, "POST", "/api/scrub", {"text": "Furthermore, it is important to note that."})
        self.assertEqual(status, 200)
        body = json.loads(data)
        self.assertIn("cleaned", body)

    def test_humanize(self):
        status, data = _request(self.port, "POST", "/api/humanize", {"text": "It is important to note that this is the case.", "tone": "casual"})
        self.assertEqual(status, 200)
        body = json.loads(data)
        self.assertIn("humanized", body)
        self.assertEqual(body["tone"], "casual")

    def test_heatmap(self):
        status, data = _request(self.port, "POST", "/api/heatmap", {"text": "hello world test"})
        self.assertEqual(status, 200)
        body = json.loads(data)
        self.assertIn("html", body)
        self.assertGreater(len(body["html"]), 100)


class TestCleanFileEndpoint(unittest.TestCase):
    def setUp(self):
        self.server, self.port = _start_server()

    def tearDown(self):
        self.server.shutdown()

    def test_clean_file_upload(self):
        boundary = "----aphanisboundary"
        body = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="file"; filename="test.txt"\r\n'
            f"Content-Type: text/plain\r\n\r\n"
            f"Furthermore, it is important to note that.\r\n"
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="mode"\r\n\r\n'
            f"paranoid\r\n"
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="perturb"\r\n\r\n'
            f"true\r\n"
            f"--{boundary}--\r\n"
        ).encode()
        status, data = _request(
            self.port, "POST", "/api/clean-file",
            body=body,
            headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        )
        self.assertEqual(status, 200)
        result = json.loads(data)
        self.assertTrue(result["success"])
        self.assertIn("data_base64", result)

    def test_clean_file_no_file(self):
        boundary = "----aphanisboundary"
        body = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="mode"\r\n\r\n'
            f"paranoid\r\n"
            f"--{boundary}--\r\n"
        ).encode()
        status, data = _request(
            self.port, "POST", "/api/clean-file",
            body=body,
            headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        )
        self.assertEqual(status, 400)


class TestNotFound(unittest.TestCase):
    def setUp(self):
        self.server, self.port = _start_server()

    def tearDown(self):
        self.server.shutdown()

    def test_unknown_endpoint(self):
        status, _ = _request(self.port, "POST", "/api/nonexistent")
        self.assertEqual(status, 404)


if __name__ == "__main__":
    unittest.main()
