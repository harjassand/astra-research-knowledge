"""Independent exact rational audit; subgroup enumeration is ONLY for tiny tests.

No worker sampler is imported. Forward transitions and backward absorption use
separate code paths. All arithmetic in laws is fractions.Fraction.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path

M = 4
STATES = tuple(product(range(M), repeat=2))
RHO = (1, 2)


def forward_gate(x):
    return ((2*x[0]+1) % M, (2*x[1]+x[0]*x[0]+1) % M)


def forward_category(law, category):
    out = defaultdict(F)
    if category == 'H':
        return {x: F(1, len(STATES)) for x in STATES}
    if category == 'R':
        return {RHO: F(1)}
    for x, mass in law.items():
        out[forward_gate(x)] += mass
    return dict(out)


def add(v, w):
    return tuple((a+b) % M for a, b in zip(v, w))


def scale(v, x):
    return tuple(a*x % M for a in v)


def cyclic_extend(subgroup, vector):
    return {add(w, scale(vector, a)) for w in subgroup for a in range(M)}


def plan(layer, times, categories):
    size = len(times)
    zero = (0,)*size
    pending = {}
    for index, time in enumerate(times):
        vector = tuple(int(j == index) for j in range(size))
        pending[time] = add(pending.get(time, zero), vector)
    subgroup = {zero}
    offset = zero
    forces = []
    exposed = []
    while pending:
        time = max(pending)
        vector = pending.pop(time)
        if vector in subgroup:
            continue
        category = categories[time]
        exposed.append((layer, time, category))
        if category == 'H':
            subgroup = cyclic_extend(subgroup, vector)
        elif category == 'R':
            offset = add(offset, scale(vector, RHO[layer]))
        else:
            if layer == 0:
                offset = add(offset, vector)
            else:
                forces.append((vector, time-1))
            parent = scale(vector, 2)
            pending[time-1] = add(pending.get(time-1, zero), parent)
    return subgroup, offset, forces, exposed


def backward_joint(categories, top_times=(0,)):
    top_v, top_b, forces, top_exposed = plan(1, top_times, categories)
    lower_times = tuple(sorted({0, *(time for _, time in forces)}, reverse=True))
    low_v, low_b, _, low_exposed = plan(0, lower_times, categories)
    out = defaultdict(F)
    weight = F(1, len(top_v)*len(low_v))
    for low_noise in low_v:
        lower = dict(zip(lower_times, add(low_b, low_noise)))
        top_offset = top_b
        for vector, time in forces:
            top_offset = add(top_offset, scale(vector, lower[time]**2+1))
        for top_noise in top_v:
            out[(lower[0], *add(top_offset, top_noise))] += weight
    return dict(out), top_exposed, low_exposed


def mixture_step(law):
    out = defaultdict(F)
    for category in 'HRG':
        for state, mass in forward_category(law, category).items():
            out[state] += mass/3
    return dict(out)


def nonunit_image_check():
    # Correct propagation at a node carrying vector (1,2) through A(x)=2x.
    vector = (1, 2)
    propagated = scale(vector, 2)
    direct = {scale(vector, (2*x) % M) for x in range(M)}
    symbolic = {scale(propagated, x) for x in range(M)}
    assert direct == symbolic == {(0, 0), (2, 0)}
    # A field-rank shortcut would falsely regard 2 as invertible modulo 4.
    assert len({2*x % M for x in range(M)}) == 2
    return {'vector': vector, 'propagated': propagated,
            'image': sorted(direct), 'image_order': len(direct)}


def correlated_uniform_counterexample():
    # U uniform is insufficient if discarded Z=U; U+Z=2U is not uniform.
    law = defaultdict(F)
    for u in range(M):
        law[(u+u) % M] += F(1, M)
    assert dict(law) == {0: F(1, 2), 2: F(1, 2)}
    return {str(x): str(p) for x, p in law.items()}


def memo_counterexample():
    # Gate sets (0,0), Haar sets two independent uniforms. One shared event
    # creates category dependence; independent layer category draws lose it.
    shared = F(1, 2) + F(1, 2)*F(1, M*M)
    independent = (F(1, 2)+F(1, 2)*F(1, M))**2
    assert shared == F(17, 32) and independent == F(25, 64)
    return {'P_both_zero_shared': str(shared),
            'P_both_zero_independent_categories': str(independent)}


def run():
    stationary = defaultdict(F)
    mismatches = []
    cases = 0
    for cats in product('HRG', repeat=4):
        categories = dict(zip(range(-3, 1), cats))
        backward, top_exposed, low_exposed = backward_joint(categories)
        for initial in STATES:
            forward = {initial: F(1)}
            for category in cats:
                forward = forward_category(forward, category)
            cases += 1
            if forward != backward:
                mismatches.append((cats, initial))
        for state, mass in backward.items():
            stationary[state] += mass/F(3**4)
    stationary = dict(stationary)
    assert not mismatches
    assert sum(stationary.values()) == 1
    assert mixture_step(stationary) == stationary
    multi_cases = 0
    for cats in product('HRG', repeat=5):
        categories = dict(zip(range(-4, 1), cats))
        backward, _, _ = backward_joint(categories, top_times=(0, -1))
        for initial in STATES:
            previous = {initial: F(1)}
            for category in cats[:-1]:
                previous = forward_category(previous, category)
            forward = defaultdict(F)
            for past, p in previous.items():
                for now, q in forward_category({past: F(1)}, cats[-1]).items():
                    forward[(now[0], now[1], past[1])] += p*q
            assert dict(forward) == backward, (cats, initial)
            multi_cases += 1
    result = {
        'model': {'M': M, 'N': 1, 'c': 2, 's': '1/3', 'r': '1/3',
                  'residual': RHO,
                  'gate': ['2*x0+1 mod4', '2*x1+x0^2+1 mod4']},
        'comparison': 'exact rational, all 81 four-step category strings and all 16 initial states',
        'conditional_cases': cases,
        'mismatches': len(mismatches),
        'stationarity_exact': True,
        'multitime_comparison': 'exact rational X0^(0), X0^(1), X-1^(1); all 243 five-step category strings and 16 initial states',
        'multitime_conditional_cases': multi_cases,
        'multitime_mismatches': 0,
        'stationary_law': {str(x): str(stationary.get(x, F(0))) for x in STATES},
        'nonunit_image_check': nonunit_image_check(),
        'correlated_uniform_counterexample': correlated_uniform_counterexample(),
        'shared_category_counterexample': memo_counterexample(),
        'scope': 'finite exact test; no statistical acceptance, no universal proof or novelty claim',
    }
    path = Path(__file__).with_name('exact_results.json')
    path.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'stationary_law'}, indent=2))


if __name__ == '__main__':
    run()
