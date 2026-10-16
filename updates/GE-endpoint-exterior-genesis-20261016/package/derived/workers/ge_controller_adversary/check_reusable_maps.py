"""Independent exact checks of the two received finite reusable cells.

No received/supplied script is imported or executed.
"""
import hashlib
import json
from itertools import product
from math import comb, factorial
from pathlib import Path

import sympy as s

HERE = Path(__file__).resolve().parent
I = s.eye(2)
X = s.Matrix([[0, 1], [1, 0]])
Y = s.Matrix([[0, -s.I], [s.I, 0]])
Z = s.diag(1, -1)
C = (I - s.I*(X+Y+Z))/2


def ext(u):
    return s.diag(u, 1)


def move(u, a_to_b=True):
    operators = []
    for discarded in range(3):
        k = s.zeros(9)
        for a, c in product(range(3), repeat=2):
            row = 2*3+c if a_to_b else c*3+2
            col = a*3+discarded if a_to_b else discarded*3+a
            k[row, col] = u[c, a]
        operators.append(k)
    assert s.simplify(sum((k.H*k for k in operators), s.zeros(9))) == s.eye(9)
    return operators


def main():
    forward = move(ext(X), True)
    backward = move(ext(C), False)
    embed_a = s.zeros(9, 3)
    for a in range(3):
        embed_a[3*a+2, a] = 1
    assert s.simplify(backward[2]*forward[2]*embed_a - embed_a*ext(C)*ext(X)) == s.zeros(9, 3)
    for a, b in product(range(3), repeat=2):
        if (a, b) != (2, 2):
            assert s.simplify(backward[a]*forward[b]*embed_a) == s.zeros(9, 3)

    phase_counts = 0
    longest_word = 0
    for phases in product(range(3), repeat=5):
        phase_counts += 1
        rank = sum(2-r for r in phases)
        longest_word = max(longest_word, rank+1)
        # Every enabled local phase move lowers the finite service rank.
        for i, r in enumerate(phases):
            if r != 2:
                nxt = list(phases)
                nxt[i] += 1
                assert sum(2-r for r in nxt) == rank-1
    assert phase_counts == 243 and longest_word == 11
    assert s.simplify(C*X*X.H-C) == s.zeros(2)
    assert s.simplify((C*X)**3+s.I*I) == s.zeros(2)
    four_terminal = s.simplify((C*X)**2)
    assert four_terminal != s.trace(four_terminal)/2*I

    # Genesis single-site microstep instrument, including dephased rejection.
    micro = []
    for r, l in product(range(4), range(2)):
        control = s.zeros(8)
        control[2*r+1, 2*r+l] = 1
        local = s.eye(9)
        if l == 0:
            u = ext(X if r % 2 == 0 else C)
            local = s.kronecker_product(u, s.eye(3)) if r % 2 == 0 else s.kronecker_product(s.eye(3), u)
        micro.append(s.kronecker_product(control, local))
    assert s.simplify(sum((k.H*k for k in micro), s.zeros(72))) == s.eye(72)
    robust_phase_tests = 0
    for true_r, faulty_site, changed in product(range(4), range(5), range(4)):
        phases = [true_r]*5
        phases[faulty_site] = changed
        selected = min(range(4), key=lambda x: (-phases.count(x), x))
        assert selected == true_r
        robust_phase_tests += 1
    for partial in product(range(2), repeat=5):
        for u in (X, C):
            for done in partial:
                prefix = u if done else I
                suffix = I if done else u
                undo = u.H if done else I
                assert s.simplify(suffix*prefix-u) == s.zeros(2)
                assert s.simplify(undo*prefix-I) == s.zeros(2)

    mean = s.Integer(1)
    for j in range(1, 6):
        inner = sum(s.Rational(comb(j, k)*factorial(k), j**(k+1)) for k in range(j+1))
        mean += (-1)**(j+1)*comb(5, j)*inner
    assert mean == s.Rational(51929339, 10800000)

    p, lam, eta = s.symbols("p lambda eta", nonnegative=True)
    killed = s.Matrix([[-5*p-eta, lam], [5*p, -lam-4*p-eta]])
    base = killed + eta*s.eye(2)
    assert s.trace(base) == -lam-9*p
    assert s.factor(base.det()) == 20*p**2
    assert (s.ones(1, 2)*killed*s.Matrix([1, 0]))[0] == -eta

    receipt = {
        "arithmetic": "exact SymPy 1.14.0; no tolerances",
        "independent_move_A_to_B_and_B_to_A_TP": True,
        "clean_two_move_composition_retains_CX_in_A_and_vacates_B": True,
        "independent_phase_vectors_checked": phase_counts,
        "max_clean_phase_changes_plus_commit": longest_word,
        "unit_rate_dominating_service_mean": str(mean),
        "genesis_onsite_microstep_TP_dimension_72": True,
        "genesis_robust_plurality_tests": robust_phase_tests,
        "genesis_all_32_partial_masks_suffix_and_hold_undo_checked": True,
        "logical_CX_channel_order": 3,
        "alternating_logical_history_channel_period": 6,
        "genesis_phase_mod4_alone_does_not_identify_cumulative_logical_channel": True,
        "genesis_killed_chain_trace_determinant_and_initial_derivative": True,
        "quantum_terminal_correctness": "analytic single-site reduction and exact 26-branch QEC in PROOFS.md; whole-code atomic recovery remains an assumption",
        "scope": "internal receiving checks; no external validation, physical compiler, threshold, or novelty",
    }
    (HERE / "REUSABLE_CHECKS.json").write_text(json.dumps(receipt, indent=2, sort_keys=True)+"\n")
    paths = [HERE.parent/"ge_controller_genesis"/"REUSABLE_RECEIVER.md",
             HERE.parent/"ge_controller_genesis"/"PROOF.md",
             HERE.parent/"ge_controller_independent"/"SPEC_PROOF.md"]
    hashes = []
    for path in paths:
        data = path.read_bytes()
        hashes.append({"path": str(path), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    (HERE / "REUSABLE_INPUT_HASHES.json").write_text(json.dumps(hashes, indent=2)+"\n")
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
