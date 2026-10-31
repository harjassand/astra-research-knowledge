"""Stronger comparator: recover and retain rational parity axes from ONE
generic network using the already-established N1077 CP/quadratic predicate.

N1077 files are exact read-only copies of the pinned source. This adapter only
extracts the rational projective parity axis and retains its edgewise chart.
"""
import json
import random
import statistics
import sys
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent/'prior_n1077'))
import sympy as sp
from fields import Rational, Quadratic, Degenerate
from local_recognition import pencil, cp, determinant_quadratic, inv, mm
from acquire import (I, assemble_certificate, cube_graph, make_hidden,
                     generate_task, acquire, apply_certificate, brute_contract, validate_graph)


def one_instance_acquire(incidence, edges, tensors):
    start = time.perf_counter()
    validate_graph(incidence, edges)
    B = Rational()
    axes = {}
    for v, tensor in enumerate(tensors):
        pen = pencil(tensor, B)
        F = Quadratic(pen[3])
        factors = cp(tensor, B, F, pen)
        axes[v] = []
        for leg, e in enumerate(incidence[v]):
            u, w = edges[e]
            w = w if u == v else u
            other_leg = incidence[w].index(e)
            mat = factors[leg]
            qs = [determinant_quadratic(tensors[w], other_leg,
                                       [mat[i][s] for i in range(2)], F)
                  for s in range(2)]
            if any(not F.norm(q) for q in qs):
                raise Degenerate('zero CP-edge entry: outside generic recognition scope')
            r2 = F.div(qs[1], qs[0])
            scaled_involution = mm(mm(mat, [[F.zero, r2], [F.one, F.zero]], F), inv(mat, F), F)
            pivot = next(x for row in scaled_involution for x in row if F.norm(x))
            ratios = [F.div(x, pivot) for row in scaled_involution for x in row]
            if any(x[1] for x in ratios):
                raise ValueError('one-instance parity axis is not rational')
            j = sp.Matrix(2, 2, [sp.Rational(x[0].numerator, x[0].denominator) for x in ratios])
            root = sp.sqrt(-j.det())
            if not root.is_Rational or not root:
                raise ValueError('one-instance rational axis does not split over Q')
            j /= root
            assert j*j == I and sp.trace(j) == 0
            axes[v].append(j)
    bases = {v: sp.Matrix(t) for v, t in enumerate(tensors)}
    certificate = assemble_certificate(incidence, edges, axes, bases)
    certificate['acquired_seconds'] = time.perf_counter()-start
    return certificate


def same_admitted_subspaces(a, b):
    # Compare the four-dimensional accepted subspaces, not just sampled answers.
    even = [0, 3, 5, 6]
    for ta, tb in zip(a['transforms'], b['transforms']):
        ba = ta.inv()[:, even]
        bb = tb.inv()[:, even]
        if sp.Matrix.hstack(ba, bb).rank() != 4:
            return False
    return True


def main():
    inc, edges, points = cube_graph()
    rows = []
    for seed in range(5):
        hidden = make_hidden(inc, edges, 17+seed)
        rng = random.Random(110+seed)
        observations = [generate_task(hidden, rng)[0] for _ in range(4)]
        multi = acquire(inc, edges, observations)
        single_start = time.perf_counter()
        failed_trials = []
        for candidate_index, candidate in enumerate(observations):
            try:
                single = one_instance_acquire(inc, edges, candidate)
                break
            except (ValueError, Degenerate) as exc:
                failed_trials.append(str(exc))
        else:
            raise AssertionError('all four generic-member attempts failed; no completion claim')
        one_acquisition_all_trials_seconds = time.perf_counter()-single_start
        assert same_admitted_subspaces(multi, single)
        query_times = []
        for task in range(10):
            raw, canonical = generate_task(hidden, rng)
            # Include arbitrarily degenerate later tensors, outside N1077's
            # fresh one-instance generic-input interface.
            if task >= 5:
                for v, x in enumerate(canonical):
                    x = sp.MutableDenseMatrix(x)
                    x[[0, 3, 5, 6][(v+task) % 4]] = 0
                    canonical[v] = x
                    raw[v] = hidden[v]*x
            start = time.perf_counter()
            out_single = apply_certificate(single, raw)
            query_times.append(time.perf_counter()-start)
            out_multi = apply_certificate(multi, raw)
            if task in (0, 5):
                truth = brute_contract(raw, inc, edges)
                assert brute_contract(out_single, inc, edges) == truth
                assert brute_contract(out_multi, inc, edges) == truth
        rows.append(dict(seed=seed, multi_task_seconds=multi['acquired_seconds'],
                         one_generic_task_seconds=one_acquisition_all_trials_seconds,
                         failed_generic_trials=failed_trials,
                         first_successful_observation=candidate_index,
                         retained_query_median_seconds=statistics.median(query_times),
                         accepted_subspaces_identical=True,
                         independent_new_queries=10, singular_new_queries=5))
    summary = dict(rows=rows, conclusion='Same learned family; one-instance retained comparator is stronger',
                   source_commit='cb87e72296824ae2a677ccd337025d02d20cbb0a')
    Path('strong_comparison_results.json').write_text(json.dumps(summary, indent=2)+'\n')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
