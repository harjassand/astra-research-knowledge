"""Independent exact algebra and finite controller checks; no supplied code execution.

Only this worker directory is written. SymPy is an already installed runtime.
The finite counter sampling supplements, and does not replace, the proof.
"""
from __future__ import annotations

import hashlib
import json
import platform
import random
from collections import Counter
from itertools import combinations, product
from pathlib import Path

import sympy as s

HERE = Path(__file__).resolve().parent
C = HERE.parents[2] / "2026-10-16-convergence-genesis-v1"
I = s.eye(2)
X = s.Matrix([[0, 1], [1, 0]])
Y = s.Matrix([[0, -s.I], [s.I, 0]])
Z = s.diag(1, -1)
PAULIS = {"I": I, "X": X, "Y": Y, "Z": Z}


def tensor(mats):
    out = s.ones(1)
    for m in mats:
        out = s.kronecker_product(out, m)
    return out


def word(w):
    return tensor(PAULIS[p] for p in w)


def jindex(digits, radix):
    z = 0
    for digit in digits:
        z = radix * z + digit
    return z


def exact_quantum():
    # Independent construction directly from the four stabilizer words.
    gs = [word(w) for w in ("XZZXI", "IXZZX", "XIXZZ", "ZXIXZ")]
    p = s.eye(32)
    for g in gs:
        p = p * (s.eye(32) + g) / 2
    zero = 4 * p[:, 0]
    v = s.Matrix.hstack(zero, word("XXXXX") * zero)
    assert v.H * v == I
    assert all(g * v == v for g in gs)
    assert word("ZZZZZ") * v == v * Z
    cyclic = (I - s.I * (X + Y + Z)) / 2
    assert s.simplify(cyclic.H * cyclic) == I
    assert all(s.simplify(cyclic * a * cyclic.H) == b for a, b in ((X, Y), (Y, Z), (Z, X)))
    ct = tensor([cyclic] * 5)
    cl = s.simplify(v.H * ct * v)
    assert s.simplify(ct * v - v * cl) == s.zeros(32, 2)
    mapping = ((2, 3), (0, 1, 2), (1, 2, 3), (0, 1))
    for g, inds in zip(gs, mapping):
        rhs = s.eye(32)
        for k in inds:
            rhs = rhs * gs[k]
        assert s.simplify(ct * g * ct.H - rhs) == s.zeros(32)
    forward, reverse = cl * X, X * cl
    relative = s.simplify(forward.H * reverse)
    assert s.trace(relative) == 0
    super_diff = tensor([forward, s.conjugate(forward)]) - tensor([reverse, s.conjugate(reverse)])
    norm_squared = s.simplify(s.trace(super_diff.H * super_diff))
    assert norm_squared == 8

    bitwords = list(product((0, 1), repeat=5))
    code = s.MutableSparseMatrix(243, 2, {})
    for b, bits in enumerate(bitwords):
        for c in range(2):
            if v[b, c] != 0:
                code[jindex(bits, 3), c] = v[b, c]
    code = s.ImmutableSparseMatrix(code)

    def image_at(site, output, incoming):
        out = s.MutableSparseMatrix(243, 2, {})
        for b, bits in enumerate(bitwords):
            if bits[site] == incoming:
                destination = list(bits)
                destination[site] = output
                for c in range(2):
                    if v[b, c] != 0:
                        out[jindex(destination, 3), c] = v[b, c]
        return s.ImmutableSparseMatrix(out)

    images = [code] + [image_at(i, r, t) for i in range(5) for r in range(3) for t in range(2)]
    gram = s.zeros(31)
    for a, ma in enumerate(images):
        for b, mb in enumerate(images):
            block = ma.H * mb
            scalar = s.trace(block) / 2
            assert block == scalar * I
            gram[a, b] = scalar
    expected_eigenvalues = {s.Rational(7, 2): 1, s.Rational(1, 2): 25, s.Integer(0): 5}
    assert gram.eigenvals() == expected_eigenvalues

    # The following 26 errors already diagonalize the correctable error space.
    orthogonal = [code]
    weights = [s.Integer(1)]
    labels = ["I"]
    for i in range(5):
        e00, e01, e10, e11 = (image_at(i, r, t) for r, t in ((0, 0), (0, 1), (1, 0), (1, 1)))
        orthogonal.extend([e01 + e10, -s.I * e01 + s.I * e10, e00 - e11])
        weights.extend([s.Integer(1)] * 3)
        labels.extend([f"{p}{i+1}" for p in "XYZ"])
    for i in range(5):
        for t in range(2):
            orthogonal.append(image_at(i, 2, t))
            weights.append(s.Rational(1, 2))
            labels.append(f"leak{i+1}:{t}")
    fixed_branch_tests = 0
    for a, ma in enumerate(orthogonal):
        for b, mb in enumerate(orthogonal):
            assert ma.H * mb == (weights[a] * I if a == b else s.zeros(2))
        # Decoder branch is code * ma.H / sqrt(weight[a]). Scalarity is exact
        # before normalization, which does not affect the zero-error test.
        for mb in images:
            block = ma.H * mb
            assert block == s.trace(block) / 2 * I
            fixed_branch_tests += 1
    assert len(orthogonal) == 26 and fixed_branch_tests == 806
    return {
        "arithmetic": "exact Gaussian rationals, with analytic sqrt(2) normalization of leakage branches",
        "encoding_isometry": True,
        "cyclic_clifford_code_preservation_and_stabilizer_products": True,
        "logical_cyclic_matrix": [[str(x) for x in cl.row(i)] for i in range(2)],
        "logical_order_relative_unitary": [[str(x) for x in relative.row(i)] for i in range(2)],
        "order_swap_superoperator_Frobenius_norm_squared": str(norm_squared),
        "order_swap_diamond_norm": "2, since relative logical unitary has trace zero",
        "qutrit_error_images": 31,
        "all_961_cross_Grams_exactly_scalar": True,
        "Gram_eigenvalues_with_multiplicity": {str(k): n for k, n in expected_eigenvalues.items()},
        "explicit_orthogonal_recovery_branches": labels,
        "explicit_good_space_dimension": 52,
        "complement_dimension_requiring_CPTP_extension": 191,
        "fixed_decoder_branch_image_tests": fixed_branch_tests,
    }


class Surface:
    def __init__(self, side, modulus=8):
        self.l, self.q = side, modulus
        self.tiles = []
        for p in (0, 1):
            for x in range(p, side, 2):
                for y in range(p, side, 2):
                    self.tiles.append((p, tuple(((x+a) % side) * side + (y+b) % side for a in range(2) for b in range(2))))
        self.incident = [[j for j, (_, tile) in enumerate(self.tiles) if v in tile] for v in range(side**2)]
        self.moats = []
        for j in range(len(self.tiles)):
            seen = {j}
            for _ in range(2):
                seen |= {b for a in seen for v in self.tiles[a][1] for b in self.incident[v]}
            self.moats.append(tuple(seen))

    def valid(self, c, j):
        p, tile = self.tiles[j]
        residues = {c[v] % self.q for v in tile}
        return len(residues) == 1 or any(residues <= {a, (a+1) % self.q} for a in range(self.q) if a % 2 != p)

    def r_value(self, c, v):
        options = []
        old = c[v]
        for z in range(self.q):
            c[v] = z
            if all(self.valid(c, j) for j in self.incident[v]):
                options.append(z)
        c[v] = old
        return options[0] if len(options) == 1 and options[0] != old else None

    def gates(self, c):
        return [j for j, (p, tile) in enumerate(self.tiles)
                if len({c[v] % self.q for v in tile}) == 1 and c[tile[0]] % 2 == p
                and all(self.valid(c, k) for v in tile for k in self.incident[v])]

    def b_outputs(self, c, j):
        _, tile = self.tiles[j]
        if self.valid(c, j) or any(self.r_value(c, v) is not None for v in tile):
            return []
        outputs = []
        for size in (1, 2):
            for positions in combinations(tile, size):
                for zs in product(range(self.q), repeat=size):
                    if any(c[v] == z for v, z in zip(positions, zs)):
                        continue
                    t = c.copy()
                    for v, z in zip(positions, zs):
                        t[v] = z
                    if all(self.valid(t, k) for k in self.moats[j]):
                        outputs.append(t)
        return outputs

    def clean_invariant(self, h):
        for v, k in enumerate(h):
            for j in self.incident[v]:
                p, tile = self.tiles[j]
                allowed = {k-1, k} if p == k % 2 else {k, k+1}
                assert all(h[w] in allowed for w in tile if w != v)

    def endpoint_class(self, t, h):
        changed = {v for v in range(self.l**2) if t[v] != h[v] % self.q}
        if not changed:
            return "clean"
        assert len(changed) == 4
        for p, tile in self.tiles:
            if set(tile) != changed:
                continue
            assert len({h[v] for v in tile}) == 1
            shift = {(t[v] - h[v]) % self.q for v in tile}
            assert shift in ({1}, {self.q-1})
            return "forward" if shift == {1} else "backward"
        raise AssertionError("non-tile endpoint")


def counter_checks():
    rng = random.Random(20261016)
    n = Counter()
    endpoints = Counter()
    for side in (6, 8):
        surf = Surface(side)
        h = [0] * side**2
        for trial in range(120):
            # Generate reachable integer surfaces, including wrap.
            for _ in range(20):
                j = rng.choice(surf.gates(h))
                for v in surf.tiles[j][1]:
                    h[v] += 1
            surf.clean_invariant(h)
            c = [v % surf.q for v in h]
            ghost = h.copy()
            for fault in range(2):
                v = rng.randrange(side**2)
                c[v] = rng.choice([z for z in range(surf.q) if z != c[v]])
                # Separated faults: legal exterior gates may occur in between.
                for _ in range(3):
                    gates = surf.gates(c)
                    if not gates:
                        break
                    j = rng.choice(gates)
                    p, tile = surf.tiles[j]
                    assert all(c[w] == ghost[w] % surf.q for w in tile)
                    assert len({ghost[w] for w in tile}) == 1 and ghost[tile[0]] % 2 == p
                    for w in tile:
                        c[w] = (c[w]+1) % surf.q
                        ghost[w] += 1
                    surf.clean_invariant(ghost)
                    n["verified_clean_ghost_interleaved_gates"] += 1
            repairs = 0
            while c != [z % surf.q for z in ghost] and not all(surf.valid(c, j) for j in range(len(surf.tiles))):
                rs = [(v, surf.r_value(c, v)) for v in range(side**2)]
                rs = [(v, z) for v, z in rs if z is not None]
                assert all(z == ghost[v] % surf.q for v, z in rs)
                bs = []
                for j in range(len(surf.tiles)):
                    for out in surf.b_outputs(c, j):
                        assert all(surf.valid(out, k) for k in range(len(surf.tiles)))
                        endpoints[surf.endpoint_class(out, ghost)] += 1
                        n["all_enabled_B_candidates_checked"] += 1
                        bs.append(out)
                assert rs or bs
                if rs and (not bs or rng.randrange(2)):
                    v, z = rng.choice(rs)
                    c[v] = z
                else:
                    # Choice need not equal producer's deterministic tie break:
                    # theorem claims every valid candidate has the same bound.
                    c = rng.choice(bs)
                repairs += 1
                assert repairs <= 2
            assert all(surf.valid(c, j) for j in range(len(surf.tiles)))
            endpoints["retired_" + surf.endpoint_class(c, ghost)] += 1
            n["sampled_episodes"] += 1
            n[f"sampled_episodes_L{side}"] += 1
            n["effective_repair_events"] += repairs
        n[f"maximum_integer_height_L{side}"] = max(h)
    # Explicit two-history fork and the stated three-fault local trap.
    surf = Surface(6)
    _, tile = surf.tiles[4]
    fork = [0] * 36
    fork[tile[0]] = fork[tile[1]] = 1
    assert not any(surf.r_value(fork, v) is not None for v in range(36))
    outputs = surf.b_outputs(fork, 4)
    assert len(outputs) == 2
    assert {surf.endpoint_class(out, [0]*36) for out in outputs} == {"clean", "forward"}
    trap = [0] * 36
    for v, z in zip(tile, (1, 2, 3)):
        trap[v] = z
    assert not any(surf.r_value(trap, v) is not None for v in range(36))
    assert not any(surf.b_outputs(trap, j) for j in range(len(surf.tiles)))
    assert not any(set(tile) & set(surf.tiles[j][1]) for j in surf.gates(trap))
    return {"scope": "finite deterministic-seed samples, not a size-uniform proof",
            "counts": dict(n), "endpoint_counts": dict(endpoints),
            "two_history_fork": "exactly two B endpoints: clean or forward tile debt",
            "three_counter_fault_trap": "no R or B; every G touching the damaged tile blocked"}


def receiving_boundaries():
    # Jump-only closure of start --I--> accept passes prescribed identity.
    # For rate lambda=1 and H=Z, timed acceptance has off-diagonal multiplier
    # int_0^infinity exp(-t) exp(-2 i t) dt = 1/(1+2i).
    multiplier = s.simplify(1 / (1+2*s.I))
    g = -I/2 - s.I*Z
    assert g != s.trace(g)/2 * I
    assert multiplier != 1
    # A scalar no-jump generator preserves every span; this covers the source
    # Poisson-CPTP model, with sum_e L_e^dagger L_e = total_rate * I.
    return {
        "omitted_no_jump_counterexample": {
            "logical_and_physical_dimension": 2, "encoding_and_decoder": "I_2",
            "accepting_jump": "L=I_2, rate 1", "Hamiltonian": "Z",
            "jump_only_terminal_span": "span{I_2}, passes fixed identity decoder",
            "actual_accepted_offdiagonal_multiplier": str(multiplier),
            "actual_accepted_channel_is_identity": False,
            "augmented_generator_closure": "span{I_2,Z}, rejects fixed identity decoder",
            "applies_to_supplied_Poisson_CPTP_model": False,
        },
        "empty_terminal_span": "KL and fixed-decoder universal conditions are vacuously true; no liveness follows",
        "zero_decoder_family": "scalar branch check passes but sum D_r^dagger D_r=0; receiving CPTP precondition is necessary",
        "budget_and_absorption": "absorption for unaugmented graph is not absorption of a fault-budget-truncated subinstrument",
    }


def input_hashes():
    inputs = [
        "MANIFEST.json", "CLAIM_LEDGER.json", "CONTINUATION_HANDOFF.md",
        "root/ALL_HISTORY_CHANNEL_CONTRACT.md",
        "workers/s01_controller_repair/REPORT.md",
        "workers/s01_controller_repair/TRANSITION_TABLE.md",
        "workers/s01_controller_repair/check_radius2_decoder.py",
        "workers/s03_history_interface/FINITE_DISCHARGE.md",
        "workers/s03_history_interface/REPORT.md",
        "workers/s03_history_interface/finite_discharge_check.py",
        "workers/s03_history_interface/quantum_recovery_check.py",
        "workers/s06_controller_adversary/REPORT.md",
        "workers/s06_controller_adversary/S03_BANK_CLEAR_AUDIT.md",
        "workers/s06_controller_adversary/FINAL_AUDIT_ADDENDUM.md",
        "workers/l02_history_algebra/REPORT.md",
        "workers/l02_history_algebra/history_closure.py",
        "workers/l03_counter_repair/REPORT.md",
        "workers/l03_counter_repair/FOLLOWUP.md",
        "sources/l01/2601.20818v3/source/SM.tex",
        "sources/l01/2610.05589v1/source/submission.tex",
        "sources/l01/astra-capital/github_commit.json",
    ]
    manifest = {x["path"]: x["sha256"] for x in json.loads((C / "MANIFEST.json").read_text())["files"]}
    rows = []
    for rel in inputs:
        b = (C / rel).read_bytes()
        digest = hashlib.sha256(b).hexdigest()
        rows.append({"path": str(C / rel), "bytes": len(b), "sha256": digest,
                     "matches_supplied_manifest": digest == manifest[rel] if rel in manifest else None})
    return rows


if __name__ == "__main__":
    result = {
        "worker": "ge_controller_adversary", "source_handling": "DATA; no supplied/acquired code executed",
        "environment": {"python": platform.python_version(), "sympy": s.__version__},
        "quantum": exact_quantum(), "counter": counter_checks(), "receiving_boundaries": receiving_boundaries(),
        "scientific_scope": "Internal exact/finite checks only. No external validation, novelty, threshold, or physical capability established.",
    }
    (HERE / "CHECKS.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    (HERE / "INPUT_HASHES.json").write_text(json.dumps(input_hashes(), indent=2) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
