#!/usr/bin/env python3
"""Exact small-case audit of ROOT SYMMETRIC_WHITEBALL_COMPILER.txt.

Covers (d,N)=(2,2),(2,3),(3,2),(3,3), with only Python's standard library.
All matrix arithmetic is over Q(i); all probability/weight decisions are over Q.
No peer script is imported or executed.
"""
from fractions import Fraction as F
from itertools import combinations, permutations, product
import json
from math import comb, factorial
from pathlib import Path


class QI:
    """Gaussian rational with immutable Fraction components."""
    __slots__ = ("r", "i")

    def __init__(self, r=0, i=0):
        self.r = F(r)
        self.i = F(i)

    @staticmethod
    def coerce(x):
        return x if isinstance(x, QI) else QI(x)

    def __add__(self, other):
        o = QI.coerce(other)
        return QI(self.r + o.r, self.i + o.i)

    __radd__ = __add__

    def __neg__(self):
        return QI(-self.r, -self.i)

    def __sub__(self, other):
        return self + (-QI.coerce(other))

    def __rsub__(self, other):
        return QI.coerce(other) - self

    def __mul__(self, other):
        o = QI.coerce(other)
        return QI(self.r * o.r - self.i * o.i,
                  self.r * o.i + self.i * o.r)

    __rmul__ = __mul__

    def __truediv__(self, other):
        o = QI.coerce(other)
        den = o.r * o.r + o.i * o.i
        if den == 0:
            raise ZeroDivisionError
        return QI((self.r * o.r + self.i * o.i) / den,
                  (self.i * o.r - self.r * o.i) / den)

    def __rtruediv__(self, other):
        return QI.coerce(other) / self

    def conj(self):
        return QI(self.r, -self.i)

    def __eq__(self, other):
        try:
            o = QI.coerce(other)
        except Exception:
            return False
        return self.r == o.r and self.i == o.i

    def is_zero(self):
        return self.r == 0 and self.i == 0

    def __repr__(self):
        return f"QI({self.r},{self.i})"


def q(x=0):
    return QI(x)


def zeros(n, m):
    return [[q() for _ in range(m)] for _ in range(n)]


def eye(n):
    out = zeros(n, n)
    for k in range(n):
        out[k][k] = q(1)
    return out


def madd(a, b):
    return [[x + y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def mscale(s, a):
    return [[s * x for x in row] for row in a]


def msub(a, b):
    return madd(a, mscale(-1, b))


def mkron(a, b):
    return [[a[i][j] * b[r][s]
             for j in range(len(a[0])) for s in range(len(b[0]))]
            for i in range(len(a)) for r in range(len(b))]


def tensor_many(mats):
    out = [[q(1)]]
    for mat in mats:
        out = mkron(out, mat)
    return out


def mtrace(a):
    return sum((a[i][i] for i in range(min(len(a), len(a[0])))), q())


def trace_product(a, b):
    n = len(a)
    return sum((a[i][j] * b[j][i]
                for i in range(n) for j in range(n)), q())


def frobenius_sq(a):
    return sum((x.conj() * x for row in a for x in row), q())


def meq(a, b):
    return len(a) == len(b) and all(
        len(ra) == len(rb) and all(x == y for x, y in zip(ra, rb))
        for ra, rb in zip(a, b)
    )


def det(a):
    """Exact determinant over Q(i), using Gaussian elimination."""
    n = len(a)
    if n == 0:
        return q(1)
    b = [row[:] for row in a]
    out = q(1)
    for col in range(n):
        pivot = next((r for r in range(col, n) if not b[r][col].is_zero()), None)
        if pivot is None:
            return q(0)
        if pivot != col:
            b[col], b[pivot] = b[pivot], b[col]
            out = -out
        p = b[col][col]
        out = out * p
        for r in range(col + 1, n):
            if b[r][col].is_zero():
                continue
            f = b[r][col] / p
            for c in range(col + 1, n):
                b[r][c] = b[r][c] - f * b[col][c]
            b[r][col] = q(0)
    return out


def is_hermitian(a):
    n = len(a)
    return all(a[i][j] == a[j][i].conj()
               for i in range(n) for j in range(n))


def all_principal_minors(a, strict=False):
    """Exact PSD/PD test for the tiny (at most 3x3) Hermitian local matrices."""
    n = len(a)
    vals = []
    for size in range(1, n + 1):
        for idx in combinations(range(n), size):
            sub = [[a[i][j] for j in idx] for i in idx]
            value = det(sub)
            if value.i != 0:
                return False, vals + ["nonreal principal minor"]
            if strict and value.r <= 0:
                return False, vals + [str(value.r)]
            if not strict and value.r < 0:
                return False, vals + [str(value.r)]
            vals.append(value.r)
    return True, vals


def compositions(total, qlen):
    if qlen == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for tail in compositions(total - first, qlen - 1):
            yield (first,) + tail


def orbit_size(m):
    n = sum(m)
    out = factorial(n)
    for k in m:
        out //= factorial(k)
    return out


def make_local_basis(d):
    mats = [eye(d)]
    names = ["I"]
    for a in range(d):
        for b in range(a + 1, d):
            x = zeros(d, d)
            x[a][b] = q(1)
            x[b][a] = q(1)
            mats.append(x)
            names.append(f"X{a}{b}")
            y = zeros(d, d)
            y[a][b] = QI(0, 1)
            y[b][a] = QI(0, -1)
            mats.append(y)
            names.append(f"Y{a}{b}")
    for ell in range(1, d):
        h = zeros(d, d)
        for k in range(ell):
            h[k][k] = q(F(1, ell))
        h[ell][ell] = q(-1)
        mats.append(h)
        names.append(f"H{ell}")
    return mats, names


def sequential_mask_probability(mask, pwhite):
    """Probability of a mask under the sequential not-all-white sampler."""
    remaining = len(mask)
    seen_nonwhite = False
    probability = F(1)
    transitions = []
    for white in mask:
        if seen_nonwhite:
            p_w, p_n = pwhite, 1 - pwhite
        else:
            # Given that the prefix was white, forbid the event that all
            # remaining sites are white.  If one site remains, white is
            # outside the valid support and is assigned probability zero.
            denom = 1 - pwhite ** remaining
            p_w = (pwhite * (1 - pwhite ** (remaining - 1)) / denom
                   if remaining > 1 else F(0))
            p_n = (1 - pwhite) / denom
        transitions.append((p_w, p_n))
        probability *= p_w if white else p_n
        if not white:
            seen_nonwhite = True
        remaining -= 1
    return probability, transitions


def perm_invariant(a, d, n):
    basis = list(product(range(d), repeat=n))
    idx = {v: k for k, v in enumerate(basis)}
    for perm in permutations(range(n)):
        image = [idx[tuple(v[k] for k in perm)] for v in basis]
        for r in range(len(basis)):
            for c in range(len(basis)):
                if a[r][c] != a[image[r]][image[c]]:
                    return False
    return True


def run_case(d, n):
    T, names = make_local_basis(d)
    qlen = d * d
    assert len(T) == qlen
    name_index = {name: i for i, name in enumerate(names)}
    h = []
    for a in range(qlen):
        assert is_hermitian(T[a])
        if a > 0:
            assert mtrace(T[a]) == 0
        for b in range(qlen):
            inner = trace_product(T[a], T[b])
            if a != b:
                assert inner == 0
            elif inner.i == 0:
                h.append(inner.r)
            else:
                raise AssertionError("nonreal local Hilbert-Schmidt norm")
    assert h[0] == d and all(F(1) <= x <= F(2) for x in h[1:])
    hs_inv_sum = sum((1 / x for x in h), F(0))
    assert hs_inv_sum <= d * d

    # Exact operator-norm certificate: I +/- T is PSD for every nonidentity
    # basis matrix, by all principal minors over Q(i).
    local_psd_checks = 0
    for a in range(1, qlen):
        for sign in (-1, 1):
            ok, _ = all_principal_minors(madd(eye(d), mscale(sign, T[a])))
            assert ok, (d, names[a], sign)
            local_psd_checks += 1

    groups = {m: [] for m in compositions(n, qlen)}
    for word in product(range(qlen), repeat=n):
        m = tuple(word.count(a) for a in range(qlen))
        groups[m].append(word)
    expected_D = comb(n + qlen - 1, qlen - 1)
    assert len(groups) == expected_D
    dim = d ** n
    Sbasis = {}
    for m, words in groups.items():
        assert len(words) == orbit_size(m)
        smat = zeros(dim, dim)
        for word in words:
            smat = madd(smat, tensor_many([T[a] for a in word]))
        assert mtrace(smat) == 0 if m != (n,) + (0,) * (qlen - 1) else mtrace(smat) == dim
        norm2 = trace_product(smat, smat)
        hprod = F(1)
        for a, multiplicity in enumerate(m):
            hprod *= h[a] ** multiplicity
        expected_norm2 = F(orbit_size(m)) * hprod
        assert norm2 == expected_norm2
        Sbasis[m] = smat

    identity_m = (n,) + (0,) * (qlen - 1)
    selected = [m for m in groups if m != identity_m]
    kterms = len(selected)
    zeta = F(1, 2 * d)
    pwhite = d * zeta
    w = pwhite ** n
    assert pwhite == F(1, 2)
    raw_weights = {m: F(i + 1) for i, m in enumerate(selected)}
    raw_total = sum(raw_weights.values(), F(0))
    A_by_m = {}
    c_by_m = {}
    for i, m in enumerate(selected):
        eps = 1 if i % 2 == 0 else -1
        sm = orbit_size(m)
        A_m = (w / 4) * raw_weights[m] / raw_total
        a_m = eps * A_m / sm
        c_m = a_m / dim
        A_by_m[m] = F(sm) * abs(a_m)
        c_by_m[m] = c_m
        assert A_by_m[m] == A_m

    A_total = sum(A_by_m.values(), F(0))
    assert A_total == w / 4 and 0 <= A_total <= w

    # Build a rational full-rank two-atom iid mixture S.
    Tprobe = T[name_index["X01"]]
    I_d = eye(d)
    sigma_plus = madd(mscale(F(1, d), I_d), mscale(F(1, 4 * d), Tprobe))
    sigma_minus = madd(mscale(F(1, d), I_d), mscale(F(-1, 4 * d), Tprobe))
    sigma_list = (sigma_plus, sigma_minus)
    local_floor_checks = 0
    tau_list = []
    for sigma in sigma_list:
        assert is_hermitian(sigma)
        ok, _ = all_principal_minors(sigma, strict=True)
        assert ok
        diff = msub(sigma, mscale(zeta, I_d))
        ok, _ = all_principal_minors(diff, strict=True)
        assert ok
        tau = mscale(F(1, 1) / (1 - pwhite), diff)
        assert mtrace(tau) == 1
        ok, _ = all_principal_minors(tau, strict=True)
        assert ok
        assert meq(sigma, madd(mscale(pwhite, mscale(F(1, d), I_d)),
                               mscale(1 - pwhite, tau)))
        tau_list.append(tau)
        local_floor_checks += 1

    sigma_tensors = [tensor_many([sigma] * n) for sigma in sigma_list]
    S = mscale(F(1, 2), madd(sigma_tensors[0], sigma_tensors[1]))
    Id_over_D = mscale(F(1, dim), eye(dim))
    floor_scalar = zeta ** n
    assert w / dim == floor_scalar

    # Independent exact basis analysis of E and coefficient/multiplicity data.
    E = zeros(dim, dim)
    for m, cm in c_by_m.items():
        E = madd(E, mscale(cm, Sbasis[m]))
    assert mtrace(E) == 0
    coefficients = {}
    for m, smat in Sbasis.items():
        numer = trace_product(smat, E)
        den = trace_product(smat, smat)
        cm = numer / den
        assert cm.i == 0
        coefficients[m] = cm.r
        assert cm.r == c_by_m.get(m, F(0))
    assert len(coefficients) == expected_D
    assert perm_invariant(E, d, n)

    # Verify A_m=s_m |a_m|, a_m=d^N c_m, and the exact h-weighted Cauchy bound.
    word_l1 = sum((F(orbit_size(m)) * abs(coefficients[m])
                   for m in coefficients), F(0))
    A_from_coeffs = F(dim) * word_l1
    assert A_from_coeffs == A_total
    for m in selected:
        a_m = F(dim) * coefficients[m]
        assert A_by_m[m] == orbit_size(m) * abs(a_m)
    E2_sq = frobenius_sq(E)
    assert E2_sq.i == 0 and E2_sq.r >= 0
    Hsum = hs_inv_sum ** n
    assert word_l1 ** 2 <= E2_sq.r * Hsum
    assert Hsum <= F(d ** (2 * n))
    assert A_total ** 2 <= F(d ** (4 * n)) * E2_sq.r

    # Exact parity-orbit correction states and their conditional atom laws.
    Omegas = {}
    orbit_details = []
    for m in selected:
        eps = 1 if c_by_m[m] > 0 else -1
        words = groups[m]
        active_count = sum(m[1:])
        sign_vectors = [ss for ss in product((-1, 1), repeat=active_count)
                        if _prod(ss) == eps]
        assert len(sign_vectors) == 2 ** (active_count - 1)
        atom_probability = F(1, len(words) * len(sign_vectors))
        assert atom_probability * len(words) * len(sign_vectors) == 1
        omega = zeros(dim, dim)
        for word in words:
            active_positions = [pos for pos, lab in enumerate(word) if lab != 0]
            for svec in sign_vectors:
                signs_at = dict(zip(active_positions, svec))
                factors = []
                for pos, lab in enumerate(word):
                    if lab == 0:
                        factors.append(mscale(F(1, d), I_d))
                    else:
                        factor = madd(I_d, mscale(signs_at[pos], T[lab]))
                        factor = mscale(F(1, d), factor)
                        ok, _ = all_principal_minors(factor)
                        assert ok
                        factors.append(factor)
                state = tensor_many(factors)
                omega = madd(omega, mscale(atom_probability, state))
        expected_omega = madd(Id_over_D,
                              mscale(F(eps, orbit_size(m) * dim), Sbasis[m]))
        assert meq(omega, expected_omega)
        assert mtrace(omega) == 1
        Omegas[m] = omega
        orbit_details.append({
            "count_vector": list(m),
            "orbit_size": len(words),
            "active_sites": active_count,
            "parity_sign": eps,
            "sign_patterns_per_word": len(sign_vectors),
            "conditional_atom_probability": str(atom_probability),
            "top_level_branch_weight_A_m": str(A_by_m[m]),
        })

    first = msub(S, mscale(w / dim, eye(dim)))
    middle_weight = w - A_total
    middle = mscale(middle_weight / dim, eye(dim))
    rhs = madd(first, middle)
    for m in selected:
        rhs = madd(rhs, mscale(A_by_m[m], Omegas[m]))
    R = madd(S, E)
    assert meq(R, rhs)
    assert mtrace(first) == 1 - w
    assert mtrace(middle) == middle_weight
    assert all(mtrace(mscale(A_by_m[m], Omegas[m])) == A_by_m[m]
               for m in selected)
    branch_weights = [1 - w, middle_weight] + [A_by_m[m] for m in selected]
    assert all(x >= 0 for x in branch_weights)
    assert sum(branch_weights, F(0)) == 1
    assert mtrace(R) == 1 and perm_invariant(R, d, n)

    # Positive first branch: exact tensor-floor identity, with each local
    # sigma-zeta I positive definite.  Every summand is a tensor product of
    # PSD local factors, so no floating-point eigenvalue test is used.
    first_from_atoms = zeros(dim, dim)
    for sigmat in sigma_tensors:
        first_from_atoms = madd(first_from_atoms,
                                mscale(F(1, 2), msub(sigmat,
                                                   mscale(floor_scalar, eye(dim)))))
    assert meq(first, first_from_atoms)
    floor_terms_checked = 0
    for sigma in sigma_list:
        delta = msub(sigma, mscale(zeta, I_d))
        telescoped = zeros(dim, dim)
        for mask in range(1, 1 << n):
            factors = []
            card = 0
            for pos in range(n):
                if (mask >> pos) & 1:
                    factors.append(delta)
                    card += 1
                else:
                    factors.append(I_d)
            telescoped = madd(telescoped,
                              mscale(zeta ** (n - card), tensor_many(factors)))
            floor_terms_checked += 1
        assert meq(tensor_many([sigma] * n),
                   madd(mscale(floor_scalar, eye(dim)), telescoped))

    # Conditional white/nonwhite branch: enumerate every allowed mask and
    # verify the exact conditioned iid law and its probability normalization.
    cond_probabilities = []
    global_conditional = zeros(dim, dim)
    conditional_transition_table = []
    for sigma, tau in zip(sigma_list, tau_list):
        cond_j = zeros(dim, dim)
        for mask in product((0, 1), repeat=n):  # 1 = white
            white_count = sum(mask)
            if white_count == n:
                continue
            direct_prob = (pwhite ** white_count * (1 - pwhite) ** (n - white_count)
                           / (1 - w))
            prob, transitions = sequential_mask_probability(mask, pwhite)
            assert prob == direct_prob
            cond_probabilities.append(prob)
            factors = [mscale(F(1, d), I_d) if white else tau
                       for white in mask]
            cond_j = madd(cond_j,
                          mscale(prob, tensor_many(factors)))
            if sigma is sigma_list[0]:
                conditional_transition_table.append({
                    "mask_white_bits": "".join(str(bit) for bit in mask),
                    "direct_conditional_probability": str(direct_prob),
                    "sequential_conditional_probability": str(prob),
                    "step_transitions_white_nonwhite": [
                        [str(pw), str(pn)] for pw, pn in transitions
                    ],
                })
        assert sum((pwhite ** sum(mask) * (1 - pwhite) ** (n - sum(mask))
                    / (1 - w)
                    for mask in product((0, 1), repeat=n) if sum(mask) < n),
                   F(0)) == 1
        target_j = mscale(F(1, 1) / (1 - w),
                          msub(tensor_many([sigma] * n),
                               mscale(w / dim, eye(dim))))
        assert meq(cond_j, target_j)
        global_conditional = madd(global_conditional, mscale(F(1, 2), cond_j))
    target_conditional = mscale(F(1, 1) / (1 - w), first)
    assert meq(global_conditional, target_conditional)
    assert sum(cond_probabilities, F(0)) == 2

    return {
        "d": d,
        "N": n,
        "local_basis_names": names,
        "local_hs_squared": [str(x) for x in h],
        "sum_inverse_h": str(hs_inv_sum),
        "sum_inverse_h_le_d_squared": True,
        "exact_I_plus_minus_T_PSD_checks": local_psd_checks,
        "orbit_count_D": expected_D,
        "ambient_dimension_d_pow_N": dim,
        "orbit_details": orbit_details,
        "nonidentity_orbit_count": kterms,
        "all_nonidentity_orbit_coefficients_nonzero": len(c_by_m) == expected_D - 1,
        "correction_weight_rule": "A_m=(w/4)*(orbit_index+1)/sum_{r=1}^{D-1} r; signs alternate in exact count-vector order",
        "zeta": str(zeta),
        "p_white_d_zeta": str(pwhite),
        "w": str(w),
        "A_m_total": str(A_total),
        "w_minus_A": str(middle_weight),
        "top_level_probabilities": [str(x) for x in branch_weights],
        "orbit_coefficients_nonzero": [
            {"count_vector": list(m), "c_m": str(coefficients[m]),
             "s_m": orbit_size(m), "a_m": str(dim * coefficients[m]),
             "A_m": str(A_by_m[m])}
            for m in selected
        ],
        "trace_zero_E": True,
        "permutation_invariant_E_and_R": True,
        "exact_h_weighted_Cauchy_check": True,
        "exact_coefficient_ball_check_A_le_w": True,
        "correction_state_identity_exact": True,
        "first_branch_tensor_floor_identity_exact": True,
        "floor_telescoping_terms_checked": floor_terms_checked,
        "conditional_white_mask_probabilities_sum_per_atom_family": "1 (for each j)",
        "conditional_white_sequential_transition_formula": "after all-white prefix with r remaining: white=p(1-p^(r-1))/(1-p^r), nonwhite=(1-p)/(1-p^r); after a nonwhite: (p,1-p); at r=1 white has probability 0",
        "conditional_white_sequential_mask_checks": conditional_transition_table,
        "conditional_white_branch_law_exact": True,
        "parity_orbit_atom_probabilities_exact": True,
        "all_local_factors_exact_PSD": True,
        "R_trace": str(mtrace(R).r),
        "R_positive_certificate": "exact sum of nonnegative-weight PSD product terms; all local PSD checks by principal minors over Q(i)",
        "arithmetic": "all exact Q(i) matrices and Q weights; no floating PSD test",
    }


def _prod(values):
    out = 1
    for x in values:
        out *= x
    return out


results = [run_case(d, n) for d, n in ((2, 2), (2, 3), (3, 2), (3, 3))]
output = {
    "status": "PASS",
    "source_audited": "work/cycle6/control/SYMMETRIC_WHITEBALL_COMPILER.txt",
    "cases": results,
}
out_path = Path(__file__).with_name("whiteball_exact_checks.json")
out_path.write_text(json.dumps(output, indent=2) + "\n")
print(json.dumps(output, indent=2))
