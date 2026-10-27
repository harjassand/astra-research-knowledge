"""Real SDK clients over stdio and HTTP, plus portable manifest validation."""
import asyncio
import hashlib
import json
from pathlib import Path
import socket
import subprocess
import sys
import unittest

import jsonschema
from mcp import Client
from mcp.client.stdio import StdioServerParameters

PLUGIN = Path(__file__).resolve().parents[1]
ROOT = PLUGIN.parents[1]


async def full_fetch(client, identifier):
    text, expected = [], None
    while identifier:
        result = await client.call_tool("fetch", {"id": identifier})
        assert not result.is_error, result.content
        value = result.structured_content
        assert json.loads(result.content[0].text) == value
        expected = expected or value["metadata"]["payload_sha256"]
        assert value["metadata"]["payload_sha256"] == expected
        assert value["url"].startswith("https://github.com/harjassand/")
        assert len(value["text"].encode()) <= 24000
        text.append(value["text"])
        identifier = value["metadata"]["next_id"]
    data = "".join(text).encode()
    assert hashlib.sha256(data).hexdigest() == expected
    return json.loads(data)


class SchemaTests(unittest.TestCase):
    def test_current_portable_manifests(self):
        for name in ("plugin", "mcp"):
            jsonschema.validate(json.loads((PLUGIN / (name + ".json")).read_bytes()),
                                json.loads((PLUGIN / "schemas" / (name + ".schema.json")).read_bytes()))


class ProtocolTests(unittest.IsolatedAsyncioTestCase):
    async def assert_tools(self, client):
        tools = (await client.list_tools()).tools
        self.assertEqual({t.name for t in tools}, {"search", "fetch"})
        for tool in tools:
            self.assertTrue(tool.annotations.read_only_hint)
            self.assertFalse(tool.annotations.destructive_hint)
            self.assertTrue(tool.annotations.idempotent_hint)
            self.assertIsNotNone(tool.output_schema)
            self.assertEqual(set(tool.input_schema["properties"]), {"query" if tool.name == "search" else "id"})

    async def test_real_stdio_menu_source_use_and_invalid_handle(self):
        params = StdioServerParameters(command=sys.executable,
            args=[str(PLUGIN / "server.py"), "--root", str(ROOT)])
        async with Client(params, read_timeout_seconds=60) as client:
            await self.assert_tools(client)
            result = await client.call_tool("search", {"query": "ordered-word inverse-Jordan compiler"})
            self.assertFalse(result.is_error, result.content)
            self.assertEqual(json.loads(result.content[0].text), result.structured_content)
            self.assertTrue(result.structured_content["results"])
            packet = await full_fetch(client, "U675-ordered-word-compiler")
            source = await full_fetch(client, packet["evidence"][0]["fetch_id"])
            self.assertIn("Suffix closure", source["text"])
            self.assertIn("lines", source["source"])
            self.assertEqual(packet["id"], "U675-ordered-word-compiler")
            bad = await client.call_tool("fetch", {"id": "../../private"})
            self.assertTrue(bad.is_error)

    async def test_real_http_current_correction_and_review_scope(self):
        with socket.socket() as sock:
            sock.bind(("127.0.0.1", 0))
            port = sock.getsockname()[1]
        process = subprocess.Popen([sys.executable, str(PLUGIN / "server.py"), "--root", str(ROOT),
            "--transport", "streamable-http", "--port", str(port)],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        url = "http://127.0.0.1:%d/mcp" % port
        try:
            for _ in range(120):
                self.assertIsNone(process.poll(), "HTTP server exited before readiness")
                try:
                    _, writer = await asyncio.open_connection("127.0.0.1", port)
                    writer.close()
                    await writer.wait_closed()
                    break
                except OSError:
                    await asyncio.sleep(0.1)
            else:
                self.fail("HTTP server did not become ready")
            async with Client(url, read_timeout_seconds=60, mode="legacy") as client:
                await self.assert_tools(client)
                packet = await full_fetch(client, "N557")
                accepted = next(r for r in packet["review_overlays"] if r["id"] == "A557-completed-internal-cfdb")
                self.assertEqual(accepted["decision"], "accepted_internally_verified")
                self.assertEqual(accepted["subjects"][0]["content_version"], packet["content_version"])
                self.assertTrue(packet["notices"])
                self.assertIn("W49", " ".join(accepted["remaining_gaps"]))
        finally:
            process.terminate()
            try:
                process.wait(timeout=5)

    async def test_real_stdio_exposed_task_miss_reaches_exact_witnesses_through_typed_routes(self):
        params = StdioServerParameters(command=sys.executable,
            args=[str(PLUGIN / "server.py"), "--root", str(ROOT)])
        async with Client(params, read_timeout_seconds=60) as client:
            result = await client.call_tool("search", {"query":
                "An extra measurement sharply narrows the uncertainty of a hidden model parameter. "
                "Could it still be worthless for the particular signed combination I need to decide? "
                "I want a worked exact example rather than a general slogan."})
            self.assertFalse(result.is_error, result.content)
            navigation = next(r["metadata"]["shared_consumer_navigation"]
                for r in result.structured_content["results"]
                if r.get("metadata", {}).get("shared_consumer_navigation", {}).get("total_candidates"))
            self.assertEqual(navigation["relation"], "COMMON CONSUMER; NAVIGATION ONLY")
            route = (navigation["routes"] or navigation["consumers"])[0]
            consumer = await full_fetch(client, route["consumer_fetch_id"])
            target = next(b for b in consumer["consumer_bindings"]
                if b["provider"] == "U1069-signed-task-dual-and-no-value-observation")
            mapping = next(t for t in consumer["transfers"] if t["id"] == target["binding_ref"]["id"])
            self.assertEqual(mapping["slot_binding"]["lower"], "63/1024")
            self.assertEqual(mapping["slot_binding"]["upper"], "33/512")
            packet = await full_fetch(client, target["provider_fetch_id"])
            source = await full_fetch(client, packet["evidence"][0]["fetch_id"])
            self.assertIn("both signed-task extremizers", source["text"])
            self.assertIn("q_-(x)", source["text"])
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)


if __name__ == "__main__":
    unittest.main()
