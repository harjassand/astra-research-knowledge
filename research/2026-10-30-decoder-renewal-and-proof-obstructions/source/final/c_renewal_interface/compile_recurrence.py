#!/usr/bin/env python3
"""Exact logical-tensor consumer, not a source/circuit/trajectory simulation.

Only stdlib integers/Fractions are used.  The all-r junk contraction is
computed symbolically by equality classes, not by testing selected ranks.
The canonical isometry is checked on EVERY input matrix unit.  The
arbitrary-isometry/all-memory theorem is analytic in PROOF.md; this finite
consumer does not purport to certify a general diamond norm by examples.
"""
from collections import defaultdict
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import json
import time

HERE = Path(__file__).resolve().parent


def bits(i, n):
    return tuple((i >> (n - 1 - j)) & 1 for j in range(n))


def integer(bs):
    ans = 0
    for b in bs:
        ans = 2 * ans + b
    return ans


def clean(a):
    return {k: v for k, v in a.items() if v}


def add_entry(a, ij, v):
    a[ij] += v


def outer(a, b, factor=F(1)):
    ans = defaultdict(F)
    for i, x in a.items():
        for j, y in b.items():
            # All literal tensor coefficients here are real integers.
            add_entry(ans, (i, j), factor * x * y)
    return clean(ans)


def plus(*aa):
    out = defaultdict(F)
    for a in aa:
        for ij, v in a.items():
            add_entry(out, ij, v)
    return clean(out)


def partial_trace(a, n, keep):
    out = defaultdict(F)
    discard = tuple(i for i in range(n) if i not in keep)
    for (i, j), v in a.items():
        bi, bj = bits(i, n), bits(j, n)
        if any(bi[t] != bj[t] for t in discard):
            continue
        ii = integer(tuple(bi[t] for t in keep))
        jj = integer(tuple(bj[t] for t in keep))
        add_entry(out, (ii, jj), v)
    return clean(out)


def trace(a):
    return sum(v for (i, j), v in a.items() if i == j)


def inner(a, b):
    return sum(v * b.get(i, 0) for i, v in a.items())


def raw_columns():
    """Columns sqrt(2) VA and sqrt(2) VB0 in order L0,M,Lp,R,Lnew.

    VA appends Phi_(R,Lnew). VB0=SWAP_(L0,Lp)(I-2SWAP_(M,R)) VA.
    No floating sqrt or trigonometric parameter enters these columns.
    """
    aa, bb = [], []
    for i in range(8):
        l, m, p = bits(i, 3)
        a, b = defaultdict(int), defaultdict(int)
        for rr in (0, 1):
            a[integer((l, m, p, rr, rr))] += 1
            b[integer((p, m, l, rr, rr))] += 1
            b[integer((p, rr, l, m, rr))] -= 2
        aa.append(clean(a))
        bb.append(clean(b))
    return aa, bb


def image(a, b, i, j):
    return partial_trace(outer(a[i], b[j], F(1, 2)), 5, (0, 1, 3, 4))


def expected_A(i, j):
    l, m, p = bits(i, 3)
    ll, mm, pp = bits(j, 3)
    if p != pp:
        return {}
    ans = defaultdict(F)
    for r in (0, 1):
        for rr in (0, 1):
            ans[(integer((l, m, r, r)), integer((ll, mm, rr, rr)))] += F(1, 2)
    return clean(ans)


def junk_symbolic(u, v):
    # Two diagonal maximally mixed input labels j,k, remaining ket/bra a,b.
    # The spent ket and bra indices are identified by partial trace.
    parent = {x: x for x in ("j", "k", "a", "b")}

    def find(x):
        while parent[x] != x:
            x = parent[x]
        return x

    def union(x, y):
        parent[find(x)] = find(y)

    ket_target, ket_spent = (("j", "k") if u == 0 else ("k", "j"))
    bra_target, bra_spent = (("j", "k") if v == 0 else ("k", "j"))
    union(ket_target, "a")
    union(bra_target, "b")
    union(ket_spent, bra_spent)
    assert find("a") == find("b")
    fixed = find("a")
    free = len({find(x) for x in ("j", "k")} - {fixed})
    power = free - 2
    assert power == (-1 if u == v else -2)
    return {"left_swap": u, "right_swap": v, "remaining_is_identity": True,
            "free_summed_labels": free, "coefficient_of_I": f"r^{power}",
            "relative_to_I_over_r": ("1" if u == v else "1/r")}


def general_AB_algebra():
    # Coefficients of V_s^* V_t; denominators include the two factors 1/2.
    A = {"+": F(1, 2), "-": F(1, 2)}
    B = {"+": F(1, 2), "-": F(-1, 2)}

    def product(x, y):
        return {(s, t): x[s] * y[t] for s in A for t in A}

    aa, bb, ab, ba = product(A, A), product(B, B), product(A, B), product(B, A)
    norm = {st: aa[st] + bb[st] for st in aa}
    cross = {st: ab[st] + ba[st] for st in aa}
    assert norm == {("+", "+"): F(1, 2), ("+", "-"): 0,
                    ("-", "+"): 0, ("-", "-"): F(1, 2)}
    assert cross == {("+", "+"): F(1, 2), ("+", "-"): 0,
                     ("-", "+"): 0, ("-", "-"): F(-1, 2)}
    # Substitution V_+^*V_+=V_-^*V_-=I gives I and 0 respectively.
    return {"AA_plus_BB": {str(k): str(v) for k, v in norm.items()},
            "AB_plus_BA": {str(k): str(v) for k, v in cross.items()},
            "isometry_substitution": ["I", "0"]}


def first_B_swap():
    # The memory is a spectator in this universal matrix-unit contraction.
    # Tr_spent [SWAP (E_ab tensor E_cd) SWAP] = delta_ab E_cd.
    count = 0
    for a in (0, 1):
        for b in (0, 1):
            for c in (0, 1):
                for d in (0, 1):
                    actual = partial_trace({(integer((c, a)), integer((d, b))): F(1)}, 2, (0,))
                    expected = {(c, d): F(1)} if a == b else {}
                    assert actual == expected
                    count += 1
    return count


def compile_all():
    start = time.perf_counter()
    aa, bb = raw_columns()
    gram_counts = {"VA": 0, "VB0": 0, "cross": 0}
    for i in range(8):
        for j in range(8):
            assert inner(aa[i], aa[j]) == (2 if i == j else 0)
            assert inner(bb[i], bb[j]) == (6 if i == j else 0)
            assert inner(aa[i], bb[j]) == 0
            for name in gram_counts:
                gram_counts[name] += 1

    A, B, X = {}, {}, {}
    counts = {"matrix_units": 0, "A_trace": 0, "Braw_trace": 0,
              "X_trace": 0, "A_literal_append": 0,
              "first_B_payload_erasure": 0, "fresh_port_trace_cross_zero": 0,
              "memory_marginal": 0}
    for i in range(8):
        for j in range(8):
            A[i, j] = image(aa, aa, i, j)
            B[i, j] = image(bb, bb, i, j)
            X[i, j] = plus(image(aa, bb, i, j), image(bb, aa, i, j))
            assert trace(A[i, j]) == (1 if i == j else 0)
            assert trace(B[i, j]) == (3 if i == j else 0)
            assert trace(X[i, j]) == 0
            assert A[i, j] == expected_A(i, j)
            assert partial_trace(X[i, j], 4, (0, 1)) == {}

            l, m, p = bits(i, 3)
            ll, mm, pp = bits(j, 3)
            ii0, jj0 = integer((0, m, p)), integer((0, mm, pp))
            base = image(bb, bb, ii0, jj0)
            assert B[i, j] == (base if l == ll else {})

            # Full M marginal: Braw(E_mm')=2 Tr(E_mm') I-E_mm'.
            ma = partial_trace(A[i, j], 4, (1,))
            mb = partial_trace(B[i, j], 4, (1,))
            mx = partial_trace(X[i, j], 4, (1,))
            expect_a, expect_b = {}, defaultdict(F)
            if l == ll and p == pp:
                expect_a = {(m, mm): F(1)}
                if m == mm:
                    for d in (0, 1):
                        expect_b[d, d] += 2
                expect_b[m, mm] -= 1
            assert ma == expect_a
            assert mb == clean(expect_b)
            assert mx == {}
            for k in counts:
                counts[k] += 1

    # Canonical input/output maps represented by all their exact matrix units.
    # Digest pins the full tensors without bloating the human receipt.
    tensor_rows = []
    for name, tensor in (("A", A), ("Braw", B), ("Xraw", X)):
        for (i, j), mat in sorted(tensor.items()):
            for (a, b), v in sorted(mat.items()):
                tensor_rows.append([name, i, j, a, b, str(v)])
    tensor_bytes = json.dumps(tensor_rows, separators=(",", ":")).encode()

    report = {
        "scope": "Exact universal logical tensor identities; no source/circuit/trajectory/RNG/solver run",
        "all_rank_junk_contractions": [junk_symbolic(u, v) for u in (0, 1) for v in (0, 1)],
        "arbitrary_sector_isometry_algebra": general_AB_algebra(),
        "first_B_swap_matrix_units": first_B_swap(),
        "canonical_raw_gram_entries": gram_counts,
        "canonical_all_input_matrix_unit_checks": counts,
        "canonical_tensor_nonzeros": len(tensor_rows),
        "canonical_tensor_sha256": sha256(tensor_bytes).hexdigest(),
        "canonical_normalization": {
            "VA": "raw/sqrt(2)", "VB_normalized": "raw/sqrt(6)",
            "X_normalized": "Xraw/sqrt(3)",
            "recurrence": "c^2 A + (s^2/3) Braw + (c*s/(r*sqrt(3))) Xraw",
            "constraint": "c^2+s^2=1",
            "memory_B_normalized": "(2 Tr(.) I-.)/3",
            "memory_Bloch_contraction": "1-4*s^2/3"},
        "theorem_not_a_finite_diagnostic": {
            "controller_class": "arbitrary known V_+,V_- on retained nonphysical memory; spent physical Bp discarded each fixed cell",
            "calls": "m feedback cells + one initial independent forward programme = m+1",
            "average_fidelity_bound": "1/4 + [p_m/4 + sum_t sqrt(p_t*(p_(t-1)-p_t))]/r",
            "simplified_bound_m_ge_1": "min(1,1/4+sqrt(m)/r)",
            "high_fidelity_necessary": "m>=r^2*(3/4-epsilon)^2 for all-U half-diamond<=epsilon<3/4",
            "proof": "PROOF.md Sections 1-4; arbitrary-size norm and one-query theorem are analytic inputs",
            "excluded": ["generic approximate-inverse lower bound", "unclosed physical-history controller", "arbitrary two-carrier interaction", "adaptive stopping-time expected cost", "hardware or source acquisition"]},
        "elapsed_seconds_after_imports": time.perf_counter() - start,
        "producer_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    return report


def main():
    result = compile_all()
    (HERE / "RECURRENCE.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"checks": result["canonical_all_input_matrix_unit_checks"],
                      "all_rank_junk_contractions": result["all_rank_junk_contractions"],
                      "elapsed_seconds_after_imports": result["elapsed_seconds_after_imports"]}, indent=2))


if __name__ == "__main__":
    main()
