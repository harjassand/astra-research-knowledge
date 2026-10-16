"""Replay the selected connected-support distance-four checks in FOLLOWUP.md."""
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / 'followup_check.py'
spec = importlib.util.spec_from_file_location('followup_check', SRC)
fc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fc)


def state_matrix(state, size):
    return [list(state[x * size:(x + 1) * size]) for x in range(size)]


def run():
    cases = []
    for size, names in ((4, ('zero', 'max_spread_reachable_height_le_3')),
                        (6, ('zero', 'all_even_tiles_fired_once', 'wrap_wavefront', 'high_gradient'))):
        torus = fc.Torus(size)
        candidates = fc.adversarial_clean_states(size)
        if size == 4:
            reachable = tuple(fc.clean_states(torus, 3))
            candidates['max_spread_reachable_height_le_3'] = max(
                reachable, key=lambda h: (max(h) - min(h), max(h), len(set(h))))
        for name in names:
            clean = candidates[name]
            result = fc.all_distance4_alternatives(size, clean)
            cases.append({
                'L': size,
                'q': fc.Q,
                'case': name,
                'clean_height_matrix': state_matrix(clean, size),
                'counter_residues_mod_q': state_matrix(tuple(x % fc.Q for x in clean), size),
                'globally_tile_valid': torus.valid(clean),
                **result,
            })
            print(f"completed L={size} {name}: {result['counts']}", flush=True)
    return {
        'scope': ('For each listed, explicitly supplied clean history: exhaust every connected changed support of size 1..4 and all q=8 substitutions, checking every tile predicate. This is not an enumeration of all clean histories.'),
        'cases': cases,
    }


if __name__ == '__main__':
    result = run()
    output = HERE / 'DISTANCE4_SELECTED_RESULTS.json'
    output.write_text(json.dumps(result, indent=2) + '\n')
    print(f'wrote {output}')
