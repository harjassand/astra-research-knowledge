#!/usr/bin/env python3
"""Exact all-horizon qualification for ONE actual uniform staged controller.

No selected source rank, trajectory, fidelity optimizer, parameter scan or
physical circuit is executed.  A 78-variable rational Lyapunov equation
qualifies the complete12-dimensional coherent distinct-tag walk.
"""
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import json
import time

from staged_family import (
    DIM, ARRANGEMENTS, linear_kraus, qualify_symbolic_normalization,
    substitute, symmetric_lyapunov_system, solve_bareiss, dual_apply,
    identity, exact_ldl,
)

HERE = Path(__file__).resolve().parent


def main():
    start = time.perf_counter()
    linear = linear_kraus()
    assert qualify_symbolic_normalization(linear)
    a, b = F(11, 14), F(5, 14)
    kk = substitute(a, b, linear)
    assert dual_apply(kk, identity(), survival=False) == identity()
    basis, system, rhs, den = symmetric_lyapunov_system(kk)
    solution, work = solve_bareiss(system, rhs)
    gg = {}
    for (i, j), value in zip(basis, solution):
        if value:
            gg[i, j] = value
            gg[j, i] = value
    image = dual_apply(kk, gg)
    for i in range(DIM):
        for j in range(DIM):
            assert gg.get((i, j), 0) - image.get((i, j), 0) == (1 if i == j else 0)
    pivots = exact_ldl(gg)
    # PSD G and G-S*G=I imply G>=I. Uniform upper is exact Gershgorin/trace.
    trace_bound = sum(gg.get((i, i), 0) for i in range(DIM))
    row_bound = max(sum(abs(gg.get((i, j), 0)) for j in range(DIM)) for i in range(DIM))
    bound = min(trace_bound, row_bound)
    assert bound >= 1
    # Initial arrangement e, known M=+, independent of logical input.
    initial_bound = sum(gg.get((i, j), 0) for i in (0, 1) for j in (0, 1)) / 2
    assert 0 <= initial_bound <= bound
    integer_ceiling = (bound.numerator + bound.denominator - 1) // bound.denominator
    initial_ceiling = (initial_bound.numerator + initial_bound.denominator - 1) // initial_bound.denominator
    result = {
        "scope": "Exact uniform-all-horizons tag-loss certificate for staged FIRST_OPERATION, fixed a11/14,b5/14; not a source/quantum run",
        "source_rank_substitutions": 0,
        "port": {"a": str(a), "b": str(b), "a_squared_plus_3b_squared": str(a*a+3*b*b),
                 "source_input_transpose_coefficient": str(4*b*b-1)},
        "tag_basis": [list(x) for x in ARRANGEMENTS],
        "walk_dimension": DIM,
        "kraus": [{"source_logical_traced": label[0], "R_discarded": label[1],
                    "discarded_tag": label[2], "target_lost": label[2] == 0,
                    "entries": [[i,j,str(v)] for (i,j),v in sorted(mat.items())]}
                   for label,mat in sorted(kk.items())],
        "symbolic_normalization": "sum K* K=(a^2+3b^2)I for every a,b; all144 polynomial entries checked",
        "lyapunov_G": [[str(gg.get((i,j),0)) for j in range(DIM)] for i in range(DIM)],
        "G_strict_LDL_pivots": [str(x) for x in pivots],
        "exact_dual_residual": "G-S*(G)=I, all144 entries checked",
        "uniform_lifetime_bound": str(bound), "uniform_integer_bound": integer_ceiling,
        "initial_plus_lifetime_bound": str(initial_bound), "initial_plus_integer_bound": initial_ceiling,
        "lifetime_formula": "E(no-collision live steps)<=Tr(G rho0); survival<=L*(1-1/L)^m uniformly",
        "intended_collision_consequence_pending_full_proof": "initial collisions<=3/r; first live collision before loss<=3*E(lifetime)/r; fixed-controller high fidelity cannot persist for arbitrarily large r at any horizon",
        "fixed_parameter_warning": "G belongs ONLY to this fixed(a,b). No uniformity toward a=+/-b or rank-dependent tuning is inferred.",
        "arithmetic": {**work, "kraus_common_denominator": den},
        "elapsed_seconds_after_imports": time.perf_counter()-start,
        "producer_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "family_sha256": sha256((HERE/'staged_family.py').read_bytes()).hexdigest(),
    }
    (HERE/'LIFETIME_CERTIFICATE.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({"dimension":DIM,"port":result['port'],
                      "uniform_integer_bound":integer_ceiling,
                      "initial_plus_integer_bound":initial_ceiling,
                      "arithmetic":work,"elapsed_seconds_after_imports":result['elapsed_seconds_after_imports']},indent=2))


if __name__=='__main__':
    main()
