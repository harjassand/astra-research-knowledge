#!/usr/bin/env python3
"""Exact rational compiler for the easy-plane XXZ Euler-gate lift.

This is a bounded diagnostic and certificate generator, not an FPRAS.  It
compiles a finite chronological list of rational gates F_i = I + s_i A_i into
the homogeneous coefficient instance described in the accompanying report.
The exact contraction is compared with an independent dense Fraction matrix
product on small instances.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import json
import random
from pathlib import Path
from typing import Iterable, Sequence


F = Fraction


def qstr(x: Fraction) -> str:
    return f"{x.numerator}/{x.denominator}"


@dataclass(frozen=True)
class Gate:
    kind: str
    qubits: tuple[int, ...]
    step: Fraction
    alpha: Fraction = F(0)
    gamma: Fraction = F(0)
    field_x: Fraction = F(0)
    field_z: Fraction = F(0)

    @staticmethod
    def pair(q0: int, q1: int, alpha, gamma, step) -> "Gate":
        return Gate("pair", (q0, q1), F(step), F(alpha), F(gamma))

    @staticmethod
    def field(q, field_x, field_z, step) -> "Gate":
        return Gate("field", (q,), F(step), field_x=F(field_x),
                    field_z=F(field_z))

    def validate(self, nqubits: int) -> None:
        if self.kind not in {"pair", "field"}:
            raise ValueError(f"unknown gate kind: {self.kind}")
        expected = 2 if self.kind == "pair" else 1
        if len(self.qubits) != expected or len(set(self.qubits)) != expected:
            raise ValueError(f"invalid qubits for {self.kind} gate: {self.qubits}")
        if any(q < 0 or q >= nqubits for q in self.qubits):
            raise ValueError(f"qubit index outside [0,{nqubits}): {self.qubits}")
        if self.step < 0:
            raise ValueError("Euler step must be nonnegative")
        if self.kind == "pair" and (self.alpha < 0 or abs(self.gamma) > self.alpha):
            raise ValueError("pair gate requires alpha >= |gamma| >= 0")
        if self.kind == "field" and self.field_x < 0:
            raise ValueError("field gate requires a nonnegative X field")


@dataclass
class LocalFactor:
    gate_index: int
    kind: str
    variables: tuple[int, ...]
    terms: dict[frozenset[int], Fraction]
    seed: frozenset[int]
    seed_coefficient: Fraction


def gate_matrix(g: Gate) -> list[list[Fraction]]:
    """Return the exact local matrix of I + s A for a supported gate."""
    s = g.step
    if g.kind == "pair":
        a = 1 + s * (3 * g.alpha + g.gamma)
        b = 1 + s * (3 * g.alpha - g.gamma)
        c = 2 * s * g.alpha
        return [[a, 0, 0, 0],
                [0, b, c, 0],
                [0, c, b, 0],
                [0, 0, 0, a]]
    b, c = g.field_x, g.field_z
    r = b + abs(c)
    u = 1 + s * (r + c)
    v = 1 + s * (r - c)
    d = s * b
    return [[v, d], [d, u]]


class ExactBudgetExceeded(RuntimeError):
    pass


class HomogeneousCompiler:
    """Compile a finite gate trace into two homogeneous coefficient measures."""

    def __init__(self, nqubits: int, gates: Sequence[Gate]):
        if nqubits < 0:
            raise ValueError("nqubits must be nonnegative")
        self.nqubits = nqubits
        self.gates = tuple(gates)
        for g in self.gates:
            g.validate(nqubits)

        self.names: list[str] = []
        self.legs: list[dict[int, tuple[int, int]]] = []
        self.dummies: list[tuple[int, int] | None] = []
        self.factors: list[LocalFactor] = []
        occurrences: dict[int, list[int]] = {q: [] for q in range(nqubits)}

        for gi, g in enumerate(self.gates):
            leg_map: dict[int, tuple[int, int]] = {}
            for q in g.qubits:
                row = self._new_var(f"g{gi}.q{q}.row")
                colbar = self._new_var(f"g{gi}.q{q}.colbar")
                leg_map[q] = (row, colbar)
                occurrences[q].append(gi)
            self.legs.append(leg_map)

            dummy_pair = None
            if g.kind == "field":
                z0 = self._new_var(f"g{gi}.z0")
                z1 = self._new_var(f"g{gi}.z1")
                dummy_pair = (z0, z1)
            self.dummies.append(dummy_pair)
            self.factors.append(self._make_factor(gi, g, leg_map, dummy_pair))

        self.dummy_vars = tuple(v for pair in self.dummies if pair is not None
                                for v in pair)
        self.field_count = sum(g.kind == "field" for g in self.gates)
        self.wires: list[tuple[int, int]] = []
        touched = 0
        for q, order in occurrences.items():
            if order:
                touched += 1
                for j, gi in enumerate(order):
                    gj = order[(j + 1) % len(order)]
                    # The row output of occurrence j is identified with the
                    # input column of its successor; complementing that column
                    # turns equality into a one-of-two constraint.
                    self.wires.append((self.legs[gi][q][0],
                                       self.legs[gj][q][1]))
        self.inactive_qubits = nqubits - touched
        self.ground_size = len(self.names)
        self.target_degree = self.ground_size // 2
        self.mu_degree = 2 * len(self.gates)
        self.nu_degree = len(self.wires) + self.field_count
        if self.ground_size % 2 or self.mu_degree != self.nu_degree:
            raise AssertionError("homogeneous degree accounting failed")
        if self.mu_degree != self.target_degree:
            raise AssertionError("each measure must have degree |U|/2")

        self.local_maps = [factor.terms for factor in self.factors]
        self.lc_certificates = [self._lc_certificate(g) for g in self.gates]
        self.wire_of_var: dict[int, int] = {}
        for wi, (u, v) in enumerate(self.wires):
            if u == v:
                raise AssertionError("a row and complemented column must be distinct")
            for var in (u, v):
                if var in self.wire_of_var:
                    raise AssertionError("a physical half-edge belongs to two wires")
                self.wire_of_var[var] = wi
        physical_vars = {v for leg in self.legs for pair in leg.values() for v in pair}
        if set(self.wire_of_var) != physical_vars:
            raise AssertionError("wire system does not cover all physical half-edges")

        self.mu_seed = frozenset(v for f in self.factors for v in f.seed)
        self.nu_seed = frozenset([u for u, _ in self.wires] + list(self.dummy_vars[:self.field_count]))
        if len(self.mu_seed) != self.mu_degree or len(self.nu_seed) != self.nu_degree:
            raise AssertionError("support seeds have the wrong homogeneous degree")
        if not self.mu_query(self.mu_seed) or not self.nu_query(self.nu_seed):
            raise AssertionError("constructed support seed failed exact oracle check")

    @staticmethod
    def _lc_certificate(g: Gate) -> dict:
        s = g.step
        if g.kind == "pair":
            a = 1 + s * (3 * g.alpha + g.gamma)
            b = 1 + s * (3 * g.alpha - g.gamma)
            c = 2 * s * g.alpha
            bad_eigs = (a - b - c, -a + b - c, -a - b + c)
            if min(a, b, c) < 0 or max(bad_eigs) > 0:
                raise AssertionError("pair gate missed its exact quadratic LC certificate")
            return {
                "gate_index": None,
                "kind": "pair_quadratic",
                "a": qstr(a), "b": qstr(b), "c": qstr(c),
                "three_nonpositive_hessian_eigenvalues": [qstr(x) for x in bad_eigs],
                "fourth_hessian_eigenvalue": qstr(a + b + c),
                "certificate": "all three displayed eigenvalues <= 0; nonnegative homogeneous quadratic then has log-concave logarithm",
            }
        b, c = g.field_x, g.field_z
        r = b + abs(c)
        u = 1 + s * (r + c)
        v = 1 + s * (r - c)
        d = s * b
        margin = u * v - d * d
        if u <= 0 or v <= 0 or d < 0 or margin < 0:
            raise AssertionError("field gate missed its exact homogeneous-lift LC certificate")
        return {
            "gate_index": None,
            "kind": "field_homogeneous_lift",
            "u": qstr(u), "v": qstr(v), "d": qstr(d),
            "uv_minus_d_squared": qstr(margin),
            "certificate": "positive-rescaling gives pair weights d,sqrt(uv)/2,sqrt(uv)/2; d^2 <= uv implies at most one positive Hessian eigenvalue",
        }

    def _new_var(self, name: str) -> int:
        idx = len(self.names)
        self.names.append(name)
        return idx

    @staticmethod
    def _combine_terms(raw: Iterable[tuple[Fraction, Iterable[int]]]) -> dict[frozenset[int], Fraction]:
        result: dict[frozenset[int], Fraction] = {}
        for coefficient, variables in raw:
            coefficient = F(coefficient)
            if coefficient == 0:
                continue
            subset = frozenset(variables)
            result[subset] = result.get(subset, F(0)) + coefficient
        return {s: c for s, c in result.items() if c > 0}

    def _make_factor(self, gi: int, g: Gate, leg_map: dict[int, tuple[int, int]],
                     dummy_pair: tuple[int, int] | None) -> LocalFactor:
        if g.kind == "pair":
            q0, q1 = g.qubits
            r0, c0 = leg_map[q0]
            r1, c1 = leg_map[q1]
            s = g.step
            a = 1 + s * (3 * g.alpha + g.gamma)
            b = 1 + s * (3 * g.alpha - g.gamma)
            c = 2 * s * g.alpha
            raw = [(a, (r0, r1)), (a, (c0, c1)),
                   (b, (r0, c1)), (b, (r1, c0)),
                   (c, (r0, c0)), (c, (r1, c1))]
            # A positive diagonal pair entry always supplies a local seed.
            seed = frozenset((r0, r1))
            owned = (r0, c0, r1, c1)
        else:
            (q,) = g.qubits
            row, colbar = leg_map[q]
            assert dummy_pair is not None
            z0, z1 = dummy_pair
            b, c = g.field_x, g.field_z
            r = b + abs(c)
            s = g.step
            u = 1 + s * (r + c)
            v = 1 + s * (r - c)
            d = s * b
            raw = [(d, (z0, z1)), (u / 2, (row, z0)),
                   (u / 2, (row, z1)), (v / 2, (colbar, z0)),
                   (v / 2, (colbar, z1)), (d, (row, colbar))]
            seed = frozenset((row, z0))
            owned = (row, colbar, z0, z1)
        terms = self._combine_terms(raw)
        if not terms or seed not in terms:
            raise AssertionError(f"positive seed missing for gate {gi}")
        return LocalFactor(gi, g.kind, tuple(owned), terms, seed, terms[seed])

    def mu_query(self, subset: Iterable[int]) -> Fraction:
        chosen = frozenset(subset)
        if any(v < 0 or v >= self.ground_size for v in chosen):
            return F(0)
        value = F(1)
        for factor in self.factors:
            local = frozenset(v for v in factor.variables if v in chosen)
            coeff = factor.terms.get(local, F(0))
            if coeff == 0:
                return F(0)
            value *= coeff
        return value

    def nu_query(self, subset: Iterable[int]) -> int:
        chosen = frozenset(subset)
        if any(v < 0 or v >= self.ground_size for v in chosen):
            return 0
        if sum(v in chosen for v in self.dummy_vars) != self.field_count:
            return 0
        if any((u in chosen) + (v in chosen) != 1 for u, v in self.wires):
            return 0
        return 1

    @property
    def coefficient_range_mu(self) -> Fraction:
        ratio = F(1)
        for factor in self.factors:
            vals = tuple(factor.terms.values())
            ratio *= max(vals) / min(vals)
        return ratio

    def support_certificate(self) -> dict:
        mu_seed_value = self.mu_query(self.mu_seed)
        nu_seed_value = self.nu_query(self.nu_seed)
        return {
            "ground_size": self.ground_size,
            "target": "all-ones exponent vector",
            "mu_degree": self.mu_degree,
            "nu_degree": self.nu_degree,
            "mu_seed": [self.names[v] for v in sorted(self.mu_seed)],
            "mu_seed_value": qstr(mu_seed_value),
            "nu_seed": [self.names[v] for v in sorted(self.nu_seed)],
            "nu_seed_value": nu_seed_value,
            "coefficient_range_mu_exact": qstr(self.coefficient_range_mu),
            "coefficient_range_nu_exact": "1/1",
            "factor_certificates": [
                {
                    "gate_index": f.gate_index,
                    "kind": f.kind,
                    "support_size": len(f.terms),
                    "minimum_positive_coefficient": qstr(min(f.terms.values())),
                    "maximum_positive_coefficient": qstr(max(f.terms.values())),
                    "seed": [self.names[v] for v in sorted(f.seed)],
                    "seed_coefficient": qstr(f.seed_coefficient),
                }
                for f in self.factors
            ],
            "local_log_concavity_certificates": [
                {**cert, "gate_index": i} for i, cert in enumerate(self.lc_certificates)
            ],
            "wire_count": len(self.wires),
            "field_gate_count": self.field_count,
            "inactive_qubits": self.inactive_qubits,
            "mu_oracle": "product of exact local rational table lookups",
            "nu_oracle": "one selected endpoint per wire and exactly f selected dummies; coefficient 1",
        }

    def exact_contraction(self, max_combinations: int = 2_000_000) -> tuple[Fraction, dict]:
        """Enumerate supported local monomials and exactly contract Q."""
        branch_count = 1
        for factor in self.factors:
            branch_count *= len(factor.terms)
        if branch_count > max_combinations:
            raise ExactBudgetExceeded(
                f"exact local-term product {branch_count} exceeds cap {max_combinations}")
        term_lists = [tuple(f.terms.items()) for f in self.factors]
        wire_counts = [0] * len(self.wires)
        dummy_set = set(self.dummy_vars)
        total = F(0)
        accepted = 0
        examined = 0

        def visit(i: int, coeff: Fraction, dummy_count: int) -> None:
            nonlocal total, accepted, examined
            if dummy_count > self.field_count:
                return
            if i == len(self.factors):
                examined += 1
                if dummy_count == self.field_count and all(c == 1 for c in wire_counts):
                    total += coeff
                    accepted += 1
                return
            for local_set, local_coeff in term_lists[i]:
                touched_wires: list[int] = []
                valid = True
                add_dummies = 0
                for var in local_set:
                    if var in dummy_set:
                        add_dummies += 1
                    else:
                        wi = self.wire_of_var[var]
                        wire_counts[wi] += 1
                        touched_wires.append(wi)
                        if wire_counts[wi] > 1:
                            valid = False
                if valid:
                    visit(i + 1, coeff * local_coeff, dummy_count + add_dummies)
                for wi in touched_wires:
                    wire_counts[wi] -= 1

        visit(0, F(1), 0)
        return total, {
            "local_term_product_upper_bound": branch_count,
            "complete_feasible_or_infeasible_leaves_examined": examined,
            "accepted_local_term_combinations": accepted,
            "max_combinations": max_combinations,
        }

    def coefficient_by_subset_sum(self) -> Fraction:
        """Independent tiny-instance check of [x^U](g_mu g_nu)."""
        if self.ground_size > 24:
            raise ExactBudgetExceeded("subset-sum cross-check is capped at 24 variables")
        all_vars = frozenset(range(self.ground_size))
        value = F(0)
        for mask in range(1 << self.ground_size):
            s = frozenset(i for i in range(self.ground_size) if mask >> i & 1)
            m = self.mu_query(s)
            if m:
                value += m * self.nu_query(all_vars - s)
        return value


def matmul(a: Sequence[Sequence[Fraction]], b: Sequence[Sequence[Fraction]]) -> list[list[Fraction]]:
    n, inner, m = len(a), len(b), len(b[0]) if b else 0
    if len(a[0]) != inner:
        raise ValueError("matrix dimensions do not match")
    out = [[F(0) for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for k in range(inner):
            if a[i][k] == 0:
                continue
            aik = a[i][k]
            for j in range(m):
                if b[k][j]:
                    out[i][j] += aik * b[k][j]
    return out


def identity(d: int) -> list[list[Fraction]]:
    return [[F(i == j) for j in range(d)] for i in range(d)]


def embed_gate(nqubits: int, g: Gate) -> list[list[Fraction]]:
    local = gate_matrix(g)
    dim = 1 << nqubits
    qs = g.qubits
    out = [[F(0) for _ in range(dim)] for _ in range(dim)]
    for row in range(dim):
        row_local = 0
        for q in qs:
            row_local = (row_local << 1) | ((row >> (nqubits - q - 1)) & 1)
        for col in range(dim):
            if any(((row >> (nqubits - q - 1)) & 1) !=
                   ((col >> (nqubits - q - 1)) & 1)
                   for q in range(nqubits) if q not in qs):
                continue
            col_local = 0
            for q in qs:
                col_local = (col_local << 1) | ((col >> (nqubits - q - 1)) & 1)
            out[row][col] = local[row_local][col_local]
    return out


def dense_trace(nqubits: int, gates: Sequence[Gate]) -> Fraction:
    """Exact trace of chronological gate action, using a dense independent route."""
    d = 1 << nqubits
    running = identity(d)
    for g in gates:
        running = matmul(embed_gate(nqubits, g), running)
    return sum((running[i][i] for i in range(d)), F(0))


def symmetric_euler_block(base: Sequence[Gate], repetitions: int) -> tuple[Gate, ...]:
    """Build chronological gates whose matrix product is (W W^T)^repetitions.

    If base is [F_1,...,F_p], chronological application has product
    W=F_p...F_1.  Every local gate is symmetric, so reversing the operation
    order inside each block gives W W^T.
    """
    if repetitions < 1:
        raise ValueError("repetitions must be positive")
    one_block = tuple(reversed(base)) + tuple(base)
    return one_block * repetitions


def check_case(name: str, nqubits: int, gates: Sequence[Gate],
               max_combinations: int = 2_000_000,
               do_subset_sum: bool = False) -> dict:
    compiler = HomogeneousCompiler(nqubits, gates)
    contraction, contraction_stats = compiler.exact_contraction(max_combinations)
    dense = dense_trace(nqubits, gates)
    compiled_total = contraction * (2 ** compiler.inactive_qubits)
    if compiled_total != dense:
        raise AssertionError(f"{name}: coefficient {compiled_total} != dense trace {dense}")
    if do_subset_sum and compiler.ground_size <= 24:
        subset_sum = compiler.coefficient_by_subset_sum()
        if subset_sum != contraction:
            raise AssertionError(f"{name}: subset sum {subset_sum} != local contraction {contraction}")
    else:
        subset_sum = None
    return {
        "case": name,
        "qubits": nqubits,
        "gate_count": len(gates),
        "ground_size": compiler.ground_size,
        "inactive_qubits": compiler.inactive_qubits,
        "wire_count": len(compiler.wires),
        "field_gate_count": compiler.field_count,
        "local_contraction_exact": qstr(contraction),
        "inactive_factor": 2 ** compiler.inactive_qubits,
        "compiled_trace_exact": qstr(compiled_total),
        "dense_trace_exact": qstr(dense),
        "subset_sum_crosscheck_exact": qstr(subset_sum) if subset_sum is not None else "SKIPPED_SIZE_CAP",
        "support_certificate": compiler.support_certificate(),
        "contraction_stats": contraction_stats,
        "status": "PASS",
    }


def deterministic_cases() -> list[tuple[str, int, tuple[Gate, ...]]]:
    return [
        ("empty_two_qubit_trace", 2, ()),
        ("single_field_zero_x_boundary", 1,
         (Gate.field(0, 0, F(-2, 3), F(1, 5)),)),
        ("single_field_nonzero_x", 2,
         (Gate.field(0, F(2, 3), F(-1, 4), F(3, 7)),)),
        ("single_pair_gamma_equals_alpha", 2,
         (Gate.pair(0, 1, F(3, 5), F(3, 5), F(2, 9)),)),
        ("single_pair_gamma_equals_minus_alpha", 2,
         (Gate.pair(0, 1, F(2, 3), F(-2, 3), F(1, 7)),)),
        ("triangle_with_spatially_varying_fields", 3,
         (Gate.pair(0, 1, F(1, 2), F(1, 2), F(1, 5)),
          Gate.field(1, F(1, 3), F(-1, 4), F(2, 7)),
          Gate.pair(1, 2, F(2, 5), F(-1, 5), F(1, 6)),
          Gate.field(2, F(0), F(2, 7), F(1, 8)),
          Gate.pair(2, 0, F(3, 4), F(-3, 4), F(1, 9)),
          Gate.field(0, F(2, 5), F(1, 6), F(1, 10)))),
        ("same_qubit_repeated_fields", 1,
         (Gate.field(0, F(1, 2), F(1, 3), F(1, 4)),
          Gate.field(0, F(2, 3), F(-1, 5), F(1, 7)),
          Gate.field(0, F(0), F(-1, 2), F(1, 9)))),
    ]


def random_cases(seed: int = 6107, count: int = 12) -> list[tuple[str, int, tuple[Gate, ...]]]:
    rng = random.Random(seed)
    out = []
    for case_i in range(count):
        n = rng.randint(1, 3)
        ngates = rng.randint(1, 4)
        gates: list[Gate] = []
        for _ in range(ngates):
            step = F(rng.randint(1, 3), rng.randint(2, 9))
            if n >= 2 and rng.random() < 0.5:
                q0, q1 = rng.sample(range(n), 2)
                alpha = F(rng.randint(0, 3), rng.randint(1, 5))
                gamma = alpha * F(rng.choice([-1, 0, 1]) * rng.randint(0, 3), 3)
                gates.append(Gate.pair(q0, q1, alpha, gamma, step))
            else:
                q = rng.randrange(n)
                bx = F(rng.randint(0, 3), rng.randint(1, 5))
                bz = F(rng.choice([-1, 1]) * rng.randint(0, 3), rng.randint(1, 5))
                gates.append(Gate.field(q, bx, bz, step))
        out.append((f"seed{seed}_case{case_i:02d}", n, tuple(gates)))
    return out


def run_self_check() -> dict:
    cases = deterministic_cases() + random_cases()
    results = [check_case(name, n, gates, do_subset_sum=(i < 5))
               for i, (name, n, gates) in enumerate(cases)]

    # Verify the same compiler on repeated symmetric Euler blocks, which are
    # the exact rational partition traces used by the thermal transfer.
    base = (Gate.pair(0, 1, F(1, 2), F(-1, 4), F(1, 7)),
            Gate.field(1, F(1, 3), F(1, 5), F(1, 9)))
    for repetitions in (1, 2):
        seq = symmetric_euler_block(base, repetitions)
        results.append(check_case(f"symmetric_euler_block_m{repetitions}", 2, seq,
                                  max_combinations=2_000_000,
                                  do_subset_sum=(repetitions == 1)))

    return {
        "worker_id": "c06_l07",
        "compiler": "work/cycle6/c06_l07/xxz_homogeneous_compiler.py",
        "arithmetic": "Python standard-library Fraction only",
        "test_count": len(results),
        "passed": sum(r["status"] == "PASS" for r in results),
        "results": results,
        "scope": "exact finite rational gate traces, local coefficient contraction, support seeds, and one tiny subset-sum cross-check; no FPRAS or many-body runtime",
    }


def main() -> None:
    report = run_self_check()
    path = Path(__file__).with_name("diagnostics.json")
    path.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: report[k] for k in ("test_count", "passed", "scope")}, indent=2))
    print(f"saved: {path}")


if __name__ == "__main__":
    main()
