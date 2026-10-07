#!/usr/bin/env python3
"""Reproduce the inline exact diagnostics for the global population drift."""
from common_nonlinear import generator
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import time


def main():
    started = time.perf_counter()
    checks = 0
    for a, b, c, k in product(range(7), range(11), range(11), (F(1), F(2))):
        if not a + b:
            continue
        assert generator(a, b, c, k) <= 1945 - F(a, 2) - F(b + c, 32)
        checks += 1
    states = [(10**9, 1, 10**8), (0, 10**9, 10**8), (1, 10**9, 0),
              (10**9, 0, 1), (10**9, 0, 0)]
    for (a, b, c), k in product(states, (F(1), F(2))):
        assert generator(a, b, c, k) <= 1945 - F(a, 2) - F(b + c, 32)
        checks += 1
    assert 16 * 11**2 + 9 == 1945
    assert 32 * F(13, 12)**2 == F(338, 9) < 38
    result = {'status': 'PASS', 'scope': 'finite diagnostics, not an all-state proof',
              'states_checked': checks, 'normlike_drift_constant': 1945,
              'stationary_population_upper': 62240,
              'seconds': time.perf_counter() - started}
    # Preserve the original inline-run evidence; replays write a separate file.
    Path(__file__).with_name('global_cost_replay.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
