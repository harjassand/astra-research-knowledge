"""Ordinary exact variable elimination with a retained contraction plan.
No knowledge is withheld: the plan and all projection indices persist.
"""
from fractions import Fraction as Q
import itertools
import json
import random
import time
from pathlib import Path
from acquire import cube_graph, make_hidden, generate_task, apply_certificate
from strong_retained_comparison import one_instance_acquire
from all_weights_pfaffian import contract


def compile_plan(incidence, edges):
    active = {i: tuple(es) for i, es in enumerate(incidence)}
    variables = set(range(len(edges)))
    steps, next_id, max_bag, stored_indices = [], len(active), 0, 0
    while variables:
        def bag(x):
            return set().union(*(set(s) for s in active.values() if x in s))
        x = min(variables, key=lambda x: (len(bag(x)), x))
        ids = [i for i, scope in active.items() if x in scope]
        union = (x,)+tuple(sorted(bag(x)-{x}))
        max_bag = max(max_bag, len(union))
        projections = []
        for i in ids:
            positions = [union.index(e) for e in active[i]]
            mapping = []
            for bits in itertools.product((0, 1), repeat=len(union)):
                val = 0
                for pos in positions:
                    val = 2*val+bits[pos]
                mapping.append(val)
            projections.append(mapping)
            stored_indices += len(mapping)
        steps.append((ids, projections, next_id, 1 << (len(union)-1)))
        for i in ids:
            del active[i]
        active[next_id] = union[1:]
        next_id += 1
        variables.remove(x)
    return dict(steps=steps, final_ids=list(active), max_bag=max_bag,
                stored_projection_indices=stored_indices)


def execute(plan, tensors):
    values = {i: [Q(x) for x in t] for i, t in enumerate(tensors)}
    for ids, maps, outid, half in plan['steps']:
        out = [Q(0)]*half
        for assignment in range(2*half):
            product = Q(1)
            for i, projection in zip(ids, maps):
                product *= values[i][projection[assignment]]
            out[assignment % half] += product
        for i in ids:
            del values[i]
        values[outid] = out
    ans = Q(1)
    for i in plan['final_ids']:
        ans *= values[i][0]
    return ans


def main():
    inc, edges, _ = cube_graph()
    hidden = make_hidden(inc, edges)
    rng = random.Random(110)
    initial, _ = generate_task(hidden, rng)
    certificate = one_instance_acquire(inc, edges, initial)
    start = time.perf_counter()
    plan = compile_plan(inc, edges)
    setup = time.perf_counter()-start
    rows = []
    for task in range(8):
        raw, _ = generate_task(hidden, rng)
        start = time.perf_counter()
        z1 = execute(plan, raw)
        ordinary = time.perf_counter()-start
        start = time.perf_counter()
        z2 = contract(apply_certificate(certificate, raw), inc, edges)
        learned = time.perf_counter()-start
        assert z1 == z2
        rows.append(dict(task=task, retained_elimination_seconds=ordinary,
                         retained_chart_pfaffian_seconds=learned, partition=str(z1)))
    result = dict(plan_setup_seconds=setup, chart_acquisition_seconds=certificate['acquired_seconds'],
                  plan_max_bag=plan['max_bag'],
                  plan_stored_projection_indices=plan['stored_projection_indices'], rows=rows,
                  conclusion='Retained elimination wins on this small low-width fixture; no practical speedup established')
    Path('execution_comparison_results.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
