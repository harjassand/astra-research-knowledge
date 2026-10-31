"""Minimum target L2 cost of unbiased finite-future feature estimators.

This is a floating point acquisition diagnostic for the supplied N541 seed.
It neither proves a null inequality nor implements an equilibrium test.
Every source file is read without mutation.
"""
from pathlib import Path
from fractions import Fraction
import json
import time
import numpy as np

BASE = Path('producer-workspace/evidence')


def main():
    start = time.perf_counter()
    source = json.loads((BASE / 'work/hidden_equilibrium/certificate.txt').read_text())
    array = lambda key: np.array([[float(Fraction(x)) for x in row] for row in source[key]])
    P = np.eye(10) + array('Q') / 2
    points = array('points')
    labels = np.array([0] * 5 + list(range(1, 6)))
    words = np.ones((10, 1))
    rows = []
    for depth in range(1, 8):
        words = np.concatenate([P @ ((labels == a)[:, None] * words) for a in range(6)], axis=1)
        A = words[:5]
        mass = A.mean(axis=0)
        keep = mass > 0
        weighted = A[:, keep] / np.sqrt(mass[keep])
        information = weighted @ weighted.T
        eig, vec = np.linalg.eigh(information)
        good = eig > eig[-1] * 1e-10
        inv = (vec[:, good] / eig[good]) @ vec[:, good].T
        residual = np.linalg.norm(information @ inv @ points - points)
        cost = float(np.trace(points.T @ inv @ points))
        assert residual < 1e-8
        row = {'future_letters': depth, 'all_words': words.shape[1], 'positive_target_words': int(keep.sum()), 'observable_rank': int(good.sum()), 'minimum_conditional_internal_L2_cost': cost, 'unbiasedness_projection_residual': float(residual)}
        rows.append(row)
        print(json.dumps(row), flush=True)
    result = {'scope': __doc__, 'model': 'P=I+Q/2; initial output=0; five internal states equiprobable', 'rows': rows, 'seconds': time.perf_counter() - start}
    Path(__file__).with_suffix('.json').write_text(json.dumps(result, indent=2) + '\n')


if __name__ == '__main__':
    main()
