#!/usr/bin/env python3
"""Independent exact-arithmetic audit of the eight-site overflow certificate.

Uses Python's standard library only. No SSA, SMC, matrix exponential, or producer
code is executed. The universal steps are proved in AUDIT.txt; this checks their
finite rational obligations and their mapping to the hashed source expressions.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import math
import platform
import sys
import time
from decimal import Decimal, localcontext
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
PIN = "3dde9ce74d829a93388e64032d27351b36dd2221"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def trim(p):
    p = list(p)
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return tuple(p)


def add(p, q):
    return trim([sum((z[i] if i < len(z) else F(0)) for z in (p, q))
                 for i in range(max(len(p), len(q)))])


def scale(p, c):
    return trim([c * a for a in p])


def multiply(p, q):
    out = [F(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            out[i + j] += a * b
    return trim(out)


def polynomial(node, source, constants, variable="n"):
    """Interpret a rate AST over Q[n], not by floating-point evaluations."""
    if isinstance(node, ast.Name):
        if node.id == variable:
            return (F(0), F(1))
        return (constants[node.id],)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return (F(ast.get_source_segment(source, node)),)
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        return scale(polynomial(node.operand, source, constants, variable), -1)
    if isinstance(node, ast.BinOp):
        left = polynomial(node.left, source, constants, variable)
        right = polynomial(node.right, source, constants, variable)
        if isinstance(node.op, ast.Add):
            return add(left, right)
        if isinstance(node.op, ast.Sub):
            return add(left, scale(right, -1))
        if isinstance(node.op, ast.Mult):
            return multiply(left, right)
        if isinstance(node.op, ast.Div) and len(right) == 1:
            return scale(left, 1 / right[0])
    raise ValueError(f"Unsupported rate expression: {ast.dump(node)}")


def value(p, n):
    return sum(c * n ** i for i, c in enumerate(p))


def shifted_coefficients(p, origin):
    return tuple(sum(p[i] * math.comb(i, k) * origin ** (i - k)
                     for i in range(k, len(p))) for k in range(len(p)))


def exact(x):
    with localcontext() as ctx:
        ctx.prec = 55
        decimal = str(Decimal(x.numerator) / Decimal(x.denominator))
    return {"rational": str(x), "decimal_descriptive_only": decimal}


def ast_equal(a, b):
    return ast.dump(a, include_attributes=False) == ast.dump(b, include_attributes=False)


EXPECTED_GRID_FUNCTION = '''
def grid_edges(rows:int, cols:int)->np.ndarray:
    out=[]
    for i in range(rows):
        for j in range(cols):
            a=i*cols+j
            for di,dj in [(-1,0),(1,0),(0,-1),(0,1)]:
                ni,nj=i+di,j+dj
                if 0<=ni<rows and 0<=nj<cols:
                    out.append((a,ni*cols+nj))
    return np.asarray(out,dtype=np.int64).reshape(-1,2)
'''


def source_model():
    receipt = json.loads((HERE / "INPUT_RECEIPT.json").read_text())
    for entry in receipt["files"]:
        assert digest(HERE / entry["local_snapshot"]) == entry["sha256"]
    assert receipt["worktree_pin"] == PIN
    contract = json.loads((HERE / "inputs/input_contract.json").read_text())
    source = (HERE / "inputs/kinetics.py").read_text()
    tree = ast.parse(source)
    names = ["C1", "C2", "C3", "C4", "D"]
    constants = None
    for node in tree.body:
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Tuple):
            if [z.id for z in node.targets[0].elts] == names:
                constants = dict(zip(names, [F(ast.get_source_segment(source, z))
                                              for z in node.value.elts]))
    assert constants == dict(zip(names, map(F, ["2.676", "0.040", "108.102", "37.881", "8.2207"])))
    evolve = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "evolve")
    rate_nodes = {}
    for node in ast.walk(evolve):
        if (isinstance(node, ast.Assign) and len(node.targets) == 1
                and isinstance(node.targets[0], ast.Name)
                and node.targets[0].id in ("a", "b")
                and any(isinstance(z, ast.Name) and z.id == "n" for z in ast.walk(node.value))):
            rate_nodes[node.targets[0].id] = node.value
    birth = polynomial(rate_nodes["b"], source, constants)
    death = polynomial(rate_nodes["a"], source, constants)
    assert birth == (constants["C3"], -constants["C1"], constants["C1"])
    assert death == (F(0), 2 * constants["C2"] + constants["C4"], -3 * constants["C2"], constants["C2"])
    for key, expected in (("birth", birth), ("death", death)):
        expression = contract["local_rates"][key]
        assert polynomial(ast.parse(expression, mode="eval").body, expression, {}) == expected
    expression = contract["local_rates"]["diffusion_per_directed_edge"]
    assert polynomial(ast.parse(expression, mode="eval").body, expression, {}, "n_source") == (F(0), constants["D"])
    grid = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "grid_edges")
    assert ast_equal(grid, ast.parse(EXPECTED_GRID_FUNCTION).body[0])
    # Independent characterization: two distinct sites are adjacent exactly
    # when the Manhattan distance of their (row, column) coordinates is one.
    coordinates = [(i, j) for i in range(2) for j in range(4)]
    edges = [(a, b) for a, x in enumerate(coordinates) for b, y in enumerate(coordinates)
             if abs(x[0] - y[0]) + abs(x[1] - y[1]) == 1]
    assert len(edges) == len(set(edges)) == 20
    assert all((b, a) in edges for a, b in edges)
    degrees = [sum(a == i for a, _ in edges) for i in range(8)]
    assert degrees == [2, 3, 3, 2, 2, 3, 3, 2]
    assert contract["grid"] == {"rows": 2, "cols": 4, "boundary": "open", "directed_neighbor_edges": 20}
    assert contract["initial_counts"] == [50] * 8
    assert F(contract["deadline"]) == 1
    assert contract["target"] == "max(n_i)<=15"
    assert contract["count_cap"] is None
    # Exact static checks of the source's suppressed-transition cap semantics.
    for statement in ("if cap>=0 and n>=cap: b=0.0", "if cap>=0 and x[b]>=cap: rate=0.0"):
        expected = ast.parse(statement).body[0]
        assert any(ast_equal(node, expected) for node in ast.walk(evolve))
    # The reference FSP is a two-site diagnostic, not the eight-site solver.
    fsp_source = (HERE / "inputs/fsp_reference.py").read_text()
    fsp_tree = ast.parse(fsp_source)
    assert any(ast_equal(node, ast.parse("range(2)", mode="eval").body) for node in ast.walk(fsp_tree))
    for expr in ("C1*a*(a-1)+C3", "C2*a*(a-1)*(a-2)+C4*a", "D*a"):
        expected = ast.parse(expr, mode="eval").body
        assert any(ast_equal(node, expected) for node in ast.walk(fsp_tree))
    return contract, constants, birth, death, edges, degrees


def run():
    start = time.perf_counter()
    contract, constants, birth, death, edges, degrees = source_model()
    r = F(161, 100)
    c = r + 1 / r - 2
    assert c == (r - 1) ** 2 / r > 0
    q = add(add(scale(birth, r - 1), scale(death, 1 / r - 1)),
            (F(0), 3 * constants["D"] * c))
    assert q == (F(3297111, 50000), F(-1660754219, 161000000),
                 F(6753249, 4025000), F(-61, 4025))
    tail = shifted_coefficients(q, 111)
    assert tail == (F(-182475423729, 161000000), F(-31881623099, 161000000),
                    F(-13559751, 4025000), F(-61, 4025))
    assert all(coefficient < 0 for coefficient in tail)
    # The sign proof above covers every real k>=0, hence every integer m>=111.
    # Since r^m>0 and K>0, none of those infinitely many states can maximize.
    finite_values = [r ** m * value(q, m) for m in range(111)]
    K = max(finite_values)
    maximizers = [m for m, z in enumerate(finite_values) if z == K]
    assert maximizers == [103]
    assert K > 0
    V0 = 8 * r ** 50
    epsilon = (V0 + 8 * K) / r ** 163
    epsilon_162 = (V0 + 8 * K) / r ** 162
    assert epsilon < F(1, 10 ** 9)
    assert epsilon < F(757, 10 ** 12)  # Safe outward decimal 7.57e-10.
    assert epsilon_162 > F(1, 10 ** 9)
    producer = json.loads((HERE / "candidate_frozen/diagnostics.json").read_text())
    candidate = producer["benchmark"]["global_overflow_certificate"]
    assert F(candidate["r"]["rational"]) == r
    assert candidate["scalar_max_attained_at"] == maximizers[0]
    assert F(candidate["scalar_global_upper_drift"]["rational"]) == K
    assert F(candidate["exact_probability_upper_bound"]["rational"]) == epsilon
    assert candidate["full_box_state_count"] == 163 ** 8
    result = {
        "status": "PASS_EXACT_DECIMAL_GENERATOR_GLOBAL_CUTOFF_CERTIFICATE",
        "scope": "Section 6 overflow theorem and its cap/FSP consequences only; no audit of Sections 1-5 or 7",
        "pinned_worktree": PIN,
        "source_mapping": {
            "coefficients": {key: exact(z) for key, z in constants.items()},
            "birth_coefficients_low_to_high": [exact(z) for z in birth],
            "death_coefficients_low_to_high": [exact(z) for z in death],
            "normalization": "Published coefficients multiply falling factorials; no additional 2! or 3! division",
            "directed_edges": edges, "undirected_edges": 10, "degrees": degrees,
            "reaction_channels": 36, "actual_reference_fsp_sites": 2,
            "cap_implementation": "Birth at n>=cap and incoming diffusion to destination>=cap are suppressed",
            "source_numerical_arithmetic": contract["numerical_arithmetic"],
        },
        "certificate": {
            "r": exact(r), "q_coefficients_low_to_high": [exact(z) for z in q],
            "q_of_111_plus_k_coefficients_low_to_high": [exact(z) for z in tail],
            "tail_all_coefficients_strictly_negative": True,
            "tail_universal_domain": "All real k>=0, hence every integer m>=111",
            "finite_maximization_domain": "Integer m=0,...,110", "maximizers": maximizers,
            "K": exact(K), "global_LV_upper_bound": exact(8 * K),
            "initial_V": exact(V0), "horizon": 1, "first_overflow_count": 163,
            "epsilon": exact(epsilon), "strictly_below_one_billionth": True,
            "first_overflow_162_same_r_bound": exact(epsilon_162),
            "retained_site_counts_inclusive": [0, 162], "full_box_states": 163 ** 8,
            "target_absorbed_fsp_states_including_target_and_overflow": 163 ** 8 - 16 ** 8 + 2,
            "candidate_exact_numbers_match_independent_derivation": True,
        },
        "analytic_steps_proved_in_AUDIT_txt": [
            "Symmetric diffusion inequality holds for every nonnegative integer count pair",
            "Localized finite stopped-chain Dynkin identity avoids assuming unbounded-domain Dynkin",
            "Coercive exit bounds and bounded rates inside finite boxes imply nonexplosion",
            "Suppressed-cap common-path coupling proves absolute path-event probability bias",
            "Absorbing target and overflow give a one-sided first-hit bracket",
        ],
        "not_certified": [
            "IEEE arithmetic, PRNG, logarithm, categorical selection, int64 overflow, or full SSA law",
            "A value or relative-error bound for the first-entry probability",
            "Numerical integration or compressed-state approximation error of an eight-site solve",
            "A novel algorithm, historical priority, physical calibration, or practical advantage",
        ],
        "cost": {"scalar_states_enumerated": 111, "SSA_events": 0, "splitting_runs": 0,
                 "full_lattice_states_enumerated": 0, "producer_script_executed": False,
                 "arithmetic": "Exact fractions for all decisive comparisons; Decimal strings descriptive",
                 "wall_seconds": time.perf_counter() - start},
        "environment": {"python": sys.version, "executable": sys.executable, "platform": platform.platform()},
        "classical_prior_method_reference": "https://cnls.lanl.gov/~munsky/JChemPhys_124_044104.pdf",
    }
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=HERE / "EXACT_AUDIT.json")
    args = parser.parse_args()
    result = run()
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"],
                      "epsilon": result["certificate"]["epsilon"]["decimal_descriptive_only"],
                      "maximizer": result["certificate"]["maximizers"],
                      "scalar_states_enumerated": 111, "SSA_events": 0,
                      "output": str(args.output)}, indent=2))
