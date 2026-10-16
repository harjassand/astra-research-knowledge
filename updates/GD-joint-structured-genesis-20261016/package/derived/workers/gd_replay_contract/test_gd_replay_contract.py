"""Bounded contract tests; all checker commands use tiny stdlib snippets."""
from __future__ import annotations

import importlib.util
import json
import os
import shlex
import sys
import tempfile
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("gd_replay_contract", HERE / "gd_replay_contract.py")
runner = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(runner)


class ReplayContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="gd-replay-contract-")
        self.root = Path(self.temp.name)
        self.plan_path = self.root / "plan.json"

    def tearDown(self) -> None:
        self.temp.cleanup()

    def plan(self, mandatory: list[dict], optional: list[dict] | None = None) -> dict:
        value = {"schema": runner.PLAN_SCHEMA, "mandatory": mandatory, "optional": optional or []}
        self.plan_path.write_text(json.dumps(value), encoding="utf-8")
        return value

    def check(self, code: str, *, modules: list[str] | None = None,
              accept: dict | None = None, **extra: object) -> dict:
        row = {"id": "bounded-check", "argv": [runner.PYTHON_TOKEN, "-c", code],
               "required_modules": modules or [], "accept": accept or {"stdout_contains": ["accepted"]}}
        row.update(extra)
        return row

    def execute(self, selected: str = sys.executable) -> dict:
        return runner.run_plan(self.plan_path, selected)

    def test_selected_interpreter_is_used_and_provenance_is_separate(self) -> None:
        spy = self.root / "selected-python"
        log = self.root / "invocations.txt"
        wrapper = "#!/bin/sh\nprintf 'selected\\n' >> " + shlex.quote(str(log)) + "\nexec " + shlex.quote(sys.executable) + " \"$@\"\n"
        spy.write_text(wrapper, encoding="utf-8")
        spy.chmod(0o755)
        self.plan([self.check("print('accepted')")])

        result = self.execute(str(spy))

        checker = result["provenance"]["checker_interpreter"]
        self.assertEqual(result["aggregate"], "PASS")
        self.assertNotEqual(result["provenance"]["launcher"]["executable"], checker["invocation"])
        self.assertEqual(result["mandatory"][0]["argv"][0], checker["invocation"])
        self.assertEqual(checker["requested"], str(spy))
        self.assertEqual(log.read_text(encoding="utf-8").splitlines(), ["selected", "selected"])
        self.assertEqual(checker["status"], "OK")

    def test_missing_mandatory_dependency_blocks_and_does_not_run(self) -> None:
        marker = self.root / "must-not-exist"
        code = f"from pathlib import Path; Path({str(marker)!r}).write_text('ran')"
        self.plan([self.check(code, modules=["gd_replay_missing_dependency_xyz"])])

        result = self.execute()

        self.assertEqual(result["aggregate"], "INCOMPLETE")
        self.assertEqual(result["mandatory"][0]["status"], "BLOCKED")
        self.assertFalse(marker.exists())
        self.assertFalse(result["mandatory"][0].get("argv"))

    def test_omitted_optional_row_stays_not_run_with_present_and_missing_dependencies(self) -> None:
        self.plan([], optional=[
            {"id": "optional-producer", "reason": "intentionally omitted",
             "required_modules": ["sys", "gd_replay_missing_dependency_xyz"]}
        ])

        result = self.execute()

        optional = result["optional"][0]
        self.assertEqual(optional["status"], "NOT_RUN")
        self.assertIsNone(optional["command"])
        self.assertTrue(optional["dependency_diagnostics"]["sys"]["available"])
        self.assertFalse(optional["dependency_diagnostics"]["gd_replay_missing_dependency_xyz"]["available"])
        self.assertEqual(result["aggregate"], "INCOMPLETE")

    def test_assertion_failure_is_fail_even_if_output_text_matches(self) -> None:
        self.plan([self.check("print('accepted'); raise AssertionError('expected failure')")])

        result = self.execute()

        self.assertEqual(result["aggregate"], "FAIL")
        self.assertEqual(result["mandatory"][0]["status"], "FAIL")
        self.assertNotEqual(result["mandatory"][0]["exit_code"], 0)

    def test_stale_json_receipt_cannot_be_accepted(self) -> None:
        receipt = self.root / "receipt.json"
        receipt.write_text('{"status":"PASS"}\n', encoding="utf-8")
        self.plan([self.check("print('accepted')", accept={
            "stdout_contains": ["accepted"],
            "json_files": [{"path": "receipt.json", "fields": {"status": "PASS"}}],
        })])

        result = self.execute()

        self.assertEqual(result["aggregate"], "FAIL")
        self.assertEqual(result["mandatory"][0]["status"], "FAIL")
        self.assertIn("fresh output 'receipt.json' was not changed by this run",
                      result["mandatory"][0]["acceptance_errors"])


if __name__ == "__main__":
    unittest.main()
