"""Actual detector JSON must retain its output and assumption boundary."""
import json
import unittest

from knowledge.model import scientific_text


class ScientificJsonCells(unittest.TestCase):
    def test_detector_partition_is_not_a_notebook(self):
        raw = json.dumps({"cells": ["[0,1]", "(1,2]", "(2,infinity)"],
                          "status": "FLOATING_DIAGNOSTIC_not_exact_bit_output",
                          "continuous_full_velocity_law_acquired": False})
        text, selection = scientific_text(raw)
        self.assertIn("FLOATING_DIAGNOSTIC_not_exact_bit_output", text)
        self.assertIn("(2,infinity)", text)
        self.assertIn("False", text)
        self.assertIn("raw JSON remains authoritative", selection)

    def test_nonnotebook_cell_objects_keep_surrounding_conditions(self):
        text, selection = scientific_text(json.dumps({
            "cells": [{"radius": "1", "mass": "1/2"}],
            "condition": "exact Gaussian cell masses must be acquired"}))
        self.assertIn("exact Gaussian cell masses must be acquired", text)
        self.assertNotIn("notebook", selection)

    def test_real_notebook_keeps_sources_without_saved_outputs(self):
        text, selection = scientific_text(json.dumps({"nbformat": 4, "cells": [
            {"cell_type": "markdown", "source": ["Conditional construction\n"]},
            {"cell_type": "code", "source": "x = 1", "outputs": ["private plot payload"]}]}))
        self.assertEqual(text, "Conditional construction\n\n\nx = 1")
        self.assertNotIn("private plot payload", text)
        self.assertIn("outputs not indexed", selection)

    def test_empty_nonnotebook_cells_do_not_erase_conditions(self):
        text, _ = scientific_text('{"cells": [], "condition": "no admitted detector"}')
        self.assertIn("no admitted detector", text)


if __name__ == "__main__":
    unittest.main()
