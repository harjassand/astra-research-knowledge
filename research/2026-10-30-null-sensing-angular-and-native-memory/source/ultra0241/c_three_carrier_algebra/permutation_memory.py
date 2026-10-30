#!/usr/bin/env python3
"""Exact sparse all-order permutation-memory interface (stdlib only).

Arithmetic is rational polynomial in q=1/r.  This implementation qualifies
real rational known controls; the governing operator identities also cover
complex controls.  No source, unknown U or quantum hardware is simulated.

State: {permutation3: {(row,col): Poly}}, row order (L0,L1,L2,E).
Control: list of Kraus dictionaries {permutation4: MemoryMap}; MemoryMap is
{(new_logical,new_memory,old_memory): rational_amplitude}.
Only terms in the SAME Kraus dictionary interfere.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import permutations


class Poly:
    """Real rational polynomial in q, with no numerical rank substituted."""
    __slots__ = ("c",)

    def __init__(self, value=0):
        if isinstance(value, Poly):
            self.c = value.c
            return
        if isinstance(value, (tuple, list)):
            cc = tuple(F(v) for v in value)
        else:
            if isinstance(value, float):
                raise TypeError("Floating coefficients are outside this exact port")
            cc = (F(value),)
        while len(cc) > 1 and cc[-1] == 0:
            cc = cc[:-1]
        self.c = cc or (F(0),)

    @classmethod
    def q(cls, degree=1):
        assert degree >= 0
        return cls([0] * degree + [1])

    def __bool__(self):
        return any(self.c)

    def __add__(self, other):
        other = Poly(other)
        return Poly([self.at(i) + other.at(i) for i in range(max(len(self.c), len(other.c)))])

    __radd__ = __add__

    def __neg__(self):
        return Poly([-x for x in self.c])

    def __sub__(self, other):
        return self + -Poly(other)

    def __rsub__(self, other):
        return Poly(other) - self

    def __mul__(self, other):
        other = Poly(other)
        cc = [F(0)] * (len(self.c) + len(other.c) - 1)
        for i, a in enumerate(self.c):
            if a:
                for j, b in enumerate(other.c):
                    if b:
                        cc[i + j] += a * b
        return Poly(cc)

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = F(other)
        assert other
        return Poly([x / other for x in self.c])

    def __eq__(self, other):
        try:
            return self.c == Poly(other).c
        except (TypeError, ValueError):
            return False

    def at(self, i):
        return self.c[i] if i < len(self.c) else F(0)

    def conjugate(self):
        return self

    def evaluate(self, r):
        assert isinstance(r, int) and r >= 1
        return sum(v / F(r) ** i for i, v in enumerate(self.c))

    def json(self):
        return [str(x) for x in self.c]

    def __repr__(self):
        return f"Poly({self.json()})"


S3 = tuple(permutations(range(3)))
S4 = tuple(permutations(range(4)))
E3 = tuple(range(3))
E4 = tuple(range(4))


def compose(g, h):
    assert len(g) == len(h)
    return tuple(g[h[i]] for i in range(len(g)))


def inverse(g):
    out = [0] * len(g)
    for i, gi in enumerate(g):
        out[gi] = i
    return tuple(out)


def cycle_count(g):
    seen, count = set(), 0
    for i in range(len(g)):
        if i not in seen:
            count += 1
            j = i
            while j not in seen:
                seen.add(j)
                j = g[j]
    return count


def parity(g):
    return -1 if (len(g) - cycle_count(g)) % 2 else 1


def embed(pi):
    assert tuple(sorted(pi)) == E3
    return tuple(pi) + (3,)


def delete_wire(kappa, erase, survivors=None):
    """Return (permutation3, q_exponent) for normalized (1/r)Tr_erase."""
    assert tuple(sorted(kappa)) == E4
    assert erase in range(4)
    survivors = tuple(i for i in range(4) if i != erase) if survivors is None else tuple(survivors)
    assert len(survivors) == 3 and set(survivors) == set(range(4)) - {erase}
    where = {wire: j for j, wire in enumerate(survivors)}
    out = []
    for wire in survivors:
        nxt = kappa[wire]
        if nxt == erase:
            nxt = kappa[erase]
        out.append(where[nxt])
    sigma = tuple(out)
    assert tuple(sorted(sigma)) == E3
    return sigma, (0 if kappa[erase] == erase else 1)


def trace_plan(branch_perms, erase=1, survivors=None):
    """Exact combinatorial plan; arbitrary complex logical backends may use it."""
    for pi in S3:
        for g in branch_perms:
            for h in branch_perms:
                kappa = compose(compose(g, embed(pi)), inverse(h))
                sigma, power = delete_wire(kappa, erase, survivors)
                yield {"input": pi, "left": g, "right": h,
                       "kappa": kappa, "output": sigma, "q_power": power}


def add(a, key, value):
    value = Poly(value)
    if value:
        a[key] = a.get(key, Poly()) + value
        if not a[key]:
            del a[key]


def add_matrix(out, a, factor=1):
    for ij, x in a.items():
        add(out, ij, x * factor)


def matrix_trace(a):
    return sum((x for (i, j), x in a.items() if i == j), Poly())


def matrix_adjoint(a):
    return {(j, i): x.conjugate() for (i, j), x in a.items()}


def decode_index(index, k, memory, wires):
    mm = index % memory
    rest = index // memory
    labels = [0] * wires
    for i in range(wires - 1, -1, -1):
        labels[i] = rest % k
        rest //= k
    assert rest == 0
    return tuple(labels), mm


def encode_index(labels, memory_index, k, memory):
    out = 0
    for x in labels:
        out = k * out + x
    return memory * out + memory_index


def permute_labels(g, labels):
    out = [None] * len(g)
    for i in range(len(g)):
        out[g[i]] = labels[i]
    return tuple(out)


def dilation_columns(g, memory_map, *, k, memory_in, memory_out):
    """Sparse columns of P_g (I_(old logical) tensor V_g)."""
    by_input = defaultdict(list)
    for (aa, ee, mm), value in memory_map.items():
        assert 0 <= aa < k and 0 <= ee < memory_out and 0 <= mm < memory_in
        value = F(value)
        if value:
            by_input[mm].append((aa, ee, value))
    columns = []
    for i in range(k ** 3 * memory_in):
        old, mm = decode_index(i, k, memory_in, 3)
        col = {}
        for aa, ee, value in by_input[mm]:
            labels = permute_labels(g, old + (aa,))
            j = encode_index(labels, ee, k, memory_out)
            col[j] = col.get(j, F(0)) + value
        columns.append({j: value for j, value in col.items() if value})
    return columns


def logical_pair(x, left, right, *, k, memory_out, erase, survivors):
    """Tr_Lerase K_left X K_right*, exact sparse rational-polynomial map."""
    out = {}
    for (i, j), value in x.items():
        for a, ca in left[i].items():
            ka, ea = decode_index(a, k, memory_out, 4)
            for b, cb in right[j].items():
                kb, eb = decode_index(b, k, memory_out, 4)
                if ka[erase] != kb[erase]:
                    continue
                ia = encode_index(tuple(ka[t] for t in survivors), ea, k, memory_out)
                ib = encode_index(tuple(kb[t] for t in survivors), eb, k, memory_out)
                add(out, (ia, ib), value * ca * cb.conjugate())
    return out


def update(coeffs, controls, *, k, memory_in, memory_out, erase=1, survivors=None):
    """Apply the exact one-call S4-to-S3 recurrence.

    This computes the algebraic map, NOT an admission test for arbitrary
    control coefficients.  Supply a literal normalized known circuit.
    check_prequery_isometry is available only for g fixing fresh wire3.
    """
    assert isinstance(k, int) and k >= 2
    assert memory_in >= 1 and memory_out >= 1 and erase in (1, 2)
    survivors = tuple(i for i in range(4) if i != erase) if survivors is None else tuple(survivors)
    assert len(survivors) == 3 and set(survivors) == set(range(4)) - {erase}
    for pi, x in coeffs.items():
        assert pi in S3
        assert all(0 <= i < k ** 3 * memory_in and 0 <= j < k ** 3 * memory_in for i, j in x)
    out = {}
    for control in controls:
        assert all(g in S4 for g in control)
        columns = {g: dilation_columns(g, v, k=k, memory_in=memory_in, memory_out=memory_out)
                   for g, v in control.items()}
        for pi, x in coeffs.items():
            for g in control:
                for h in control:
                    kappa = compose(compose(g, embed(pi)), inverse(h))
                    sigma, power = delete_wire(kappa, erase, survivors)
                    logical = logical_pair(x, columns[g], columns[h], k=k,
                                           memory_out=memory_out, erase=erase, survivors=survivors)
                    if logical:
                        target = out.setdefault(sigma, {})
                        add_matrix(target, logical, Poly.q(power))
    return {pi: x for pi, x in out.items() if x}


def check_prequery_isometry(controls, *, k, memory_in, memory_out):
    """Sufficient exact group-algebra normalization ONLY when g fixes wire3."""
    assert all(g[3] == 3 for control in controls for g in control)
    for h3 in S3:
        h = embed(h3)
        total = {}
        for control in controls:
            for g, left in control.items():
                right = control.get(compose(g, h), {})
                for (a, e, i), ci in left.items():
                    for (b, f, j), cj in right.items():
                        if a == b and e == f:
                            add(total, (i, j), F(ci).conjugate() * F(cj))
        expected = {(i, i): Poly(1) for i in range(memory_in)} if h == E4 else {}
        assert total == expected, (h, total, expected)
    return True


def logical_marginal(coeffs):
    out = {}
    for pi, x in coeffs.items():
        add_matrix(out, x, Poly.q(3 - cycle_count(pi)))
    return out


def reset_to_product_junk(coeffs):
    """UNWARRANTED physical reset, supplied only as a discriminating comparator."""
    x = logical_marginal(coeffs)
    return {E3: x} if x else {}


def moments(coeffs, *, k, memory):
    out = {}
    for pi in S3:
        moment = {}
        for sigma, x in coeffs.items():
            factor = Poly.q(3 - cycle_count(compose(sigma, pi)))
            for (i, j), value in x.items():
                li, ei = decode_index(i, k, memory, 3)
                lj, ej = decode_index(j, k, memory, 3)
                # Tr_L[X_sigma P_pi]: the second logical index is pi(first).
                if lj == permute_labels(pi, li):
                    add(moment, (ei, ej), value * factor)
        out[pi] = moment
    return out


def relational_output(coeffs, *, k, memory):
    """Actual known group-readout state, order E then G, dimension6*memory."""
    mm = moments(coeffs, k=k, memory=memory)
    out = {}
    for gi, g in enumerate(S3):
        for hi, h in enumerate(S3):
            pi = compose(h, inverse(g))
            for (e, f), value in mm[pi].items():
                add(out, (6 * e + gi, 6 * f + hi), value / 6)
    return out


def controlled_persistent_swap():
    """Known flag-controlled SWAP01, append logical |0>, leave flag intact."""
    f01 = (1, 0, 2, 3)
    return [{E4: {(0, 0, 0): F(1)}, f01: {(0, 1, 1): F(1)}}]


def pair_matrix_unit(a, b, c, d, *, flag_cross=Poly(1)):
    """E_ab(target) tensor E_cd(programme1) tensor |0><0|2 tensor flag+."""
    out = {}
    for f in (0, 1):
        for ff in (0, 1):
            i = encode_index((a, c, 0), f, 2, 2)
            j = encode_index((b, d, 0), ff, 2, 2)
            add(out, (i, j), (Poly(1) if f == ff else flag_cross) / 2)
    return out


def matrix_json(x):
    return [[i, j, value.json()] for (i, j), value in sorted(x.items())]


def coefficients_json(coeffs):
    return [{"permutation": list(pi), "matrix": matrix_json(x)} for pi, x in sorted(coeffs.items())]
