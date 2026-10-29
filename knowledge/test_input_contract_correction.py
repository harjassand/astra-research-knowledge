"""Protect immutable checkpoint history while correcting a wrong input field."""
import copy
import unittest
from knowledge.operations import compile_current_consumers, consumer_contract, operation_frame, statement_view


class InputContractCorrectionTests(unittest.TestCase):
    def record(self):
        record = {"id": "N1-compiler", "content_version": "1" * 64,
                  "kind": "result", "title": "Finite compiler", "authority": "old.txt",
                  "body": "Historical source\n\nEXACT CLAIM\nThe conditional finite bound.\n\nINTERFACE\nOld duplicated output.\n",
                  "statement": "Historical source-derived status", "review": {"acceptance": "not_assessed_by_normalizer"},
                  "contract": {"requires": "The returned bound", "provides": "The returned bound",
                               "assumptions": "Same finite source", "costs": "Paid acquisition", "units": "seconds", "obstruction": "No free calibration"}}
        record["notices"] = [{"kind": "source_input_contract_correction", "notice_id": "SN-input",
            "subject": {"id": record["id"], "content_version": record["content_version"]}, "field": "requires",
            "value": ["Actual finite source and fresh independent keys"],
            "clarification": "Input-field transcription only; no statement, output or review change.",
            "source_refs": [{"path": "proof.txt", "sha256": "2" * 64, "lines": [1, 2], "quote": "Actual finite source"}]}]
        return record

    def test_changes_only_current_input_and_keeps_visible_statement_and_history(self):
        record = self.record();before = copy.deepcopy(record)
        visible = statement_view(record, operation_frame(record))["statement"]
        compile_current_consumers([record])
        for key in before:
            self.assertEqual(record[key], before[key], key)
        self.assertNotIn("current_acceptance", record)
        current = consumer_contract(record)
        self.assertNotEqual(current["requires"], before["contract"]["requires"])
        self.assertEqual({k:v for k,v in current.items()if k!="requires"},
                         {k:v for k,v in before["contract"].items()if k!="requires"})
        self.assertEqual(statement_view(record, operation_frame(record))["statement"], visible)
        self.assertFalse(statement_view(record, operation_frame(record))["acceptance"])
        self.assertEqual(operation_frame(record)["consumer_origin"]["authority_notice"], "SN-input")
        self.assertEqual(record["current_consumer"]["source_correction_notice"], "SN-input")
        expected = copy.deepcopy(record);compile_current_consumers([record]);self.assertEqual(record, expected)
        record["notices"] = [];compile_current_consumers([record]);self.assertNotIn("current_consumer", record)

    def test_missing_support_stale_version_wrong_field_and_empty_input_fail(self):
        for issue in ("no_source", "empty_ref", "stale", "provides", "blank", "wrong_type"):
            record = self.record();notice = record["notices"][0]
            if issue == "no_source":notice["source_refs"] = []
            elif issue == "empty_ref":notice["source_refs"] = [{}]
            elif issue == "stale":notice["subject"]["content_version"] = "3" * 64
            elif issue == "provides":notice["field"] = "provides"
            elif issue == "blank":notice["value"] = "  "
            else:notice["value"] = {"guessed": "input"}
            with self.subTest(issue=issue),self.assertRaisesRegex(ValueError,"INGESTION FAILED"):
                compile_current_consumers([record])

    def test_conflicting_input_corrections_fail(self):
        record = self.record();second = copy.deepcopy(record["notices"][0]);second["value"] = "Different source"
        record["notices"].append(second)
        with self.assertRaisesRegex(ValueError,"conflicting source input"):
            compile_current_consumers([record])

    def test_parent_notice_context_does_not_change_or_promote_the_child(self):
        record = self.record();child = copy.deepcopy(record)
        child.update(id="U1-child", content_version="4" * 64)
        child["notices"][0].update(parent_context_card=record["id"], context_only_notice=True)
        before = copy.deepcopy(child)
        compile_current_consumers([record, child])
        self.assertEqual(child, before)
        self.assertNotIn("current_acceptance", child)
        self.assertNotIn("current_consumer", child)
