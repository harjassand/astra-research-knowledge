"""Replay the exhaustive L4 two-fault B(P) scan recorded in FOLLOWUP.md."""
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / 'followup_check.py'
spec = importlib.util.spec_from_file_location('followup_check', SRC)
fc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fc)


def run():
    torus = fc.Torus(4)
    states = tuple(fc.clean_states(torus, 3))
    return fc.exact_two_fault_scan(
        4, states,
        scope_note=('L=4, q=8; all clean states reachable from zero with max height <=3; '
                    'all unordered distinct-site pairs and all nontrivial residue substitutions; '
                    'exact singleton and common-invalid-tile B(P) checks.'))


if __name__ == '__main__':
    result = run()
    output = HERE / 'L4_TWO_FAULT_RESULTS.json'
    output.write_text(json.dumps(result, indent=2) + '\n')
    print(f'wrote {output}')
