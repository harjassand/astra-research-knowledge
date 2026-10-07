"""Independent exact Q(i) checks; use M=sqrt(2)X to avoid radicals."""
from dataclasses import dataclass
from fractions import Fraction as Q
import json
from pathlib import Path


@dataclass(frozen=True)
class C:
    re: Q = Q(0)
    im: Q = Q(0)

    @staticmethod
    def cast(z):
        return z if isinstance(z, C) else C(Q(z))

    def __add__(self, z):
        z = C.cast(z)
        return C(self.re + z.re, self.im + z.im)

    __radd__ = __add__

    def __neg__(self):
        return C(-self.re, -self.im)

    def __sub__(self, z):
        return self + -C.cast(z)

    def __mul__(self, z):
        z = C.cast(z)
        return C(self.re*z.re-self.im*z.im, self.re*z.im+self.im*z.re)

    __rmul__ = __mul__

    def conj(self):
        return C(self.re, -self.im)

    def __truediv__(self, z):
        z = C.cast(z)
        d = z.re*z.re + z.im*z.im
        n = self*z.conj()
        return C(n.re/d, n.im/d)


ZERO, ONE = C(), C(Q(1))


def phase(t):
    t = Q(t)
    return C((1-t*t)/(1+t*t), 2*t/(1+t*t))


def mul(a, b):
    return [[sum((a[i][k]*b[k][j] for k in range(len(b))), ZERO)
             for j in range(len(b[0]))] for i in range(len(a))]


def star(a):
    return [[a[j][i].conj() for j in range(len(a))] for i in range(len(a[0]))]


def scale(a, s):
    return [[z*s for z in row] for row in a]


def ident(n):
    return [[ONE if i == j else ZERO for j in range(n)] for i in range(n)]


def rank(a):
    a = [row[:] for row in a]
    n, m = len(a), len(a[0])
    k = 0
    for j in range(m):
        pivot = next((i for i in range(k, n) if a[i][j] != ZERO), None)
        if pivot is None:
            continue
        a[k], a[pivot] = a[pivot], a[k]
        p = a[k][j]
        a[k] = [x/p for x in a[k]]
        for i in range(k+1, n):
            p = a[i][j]
            if p != ZERO:
                a[i] = [x-p*y for x, y in zip(a[i], a[k])]
        k += 1
        if k == n:
            break
    return k


def run(r):
    aa = [phase(u+1) for u in range(r)]
    bb = [phase(Q(2*v+1, 2)) for v in range(r)]
    mm = [[[[a, b], [-b.conj(), a.conj()]] for b in bb] for a in aa]
    for row in mm:
        for m in row:
            assert mul(m, star(m)) == scale(ident(2), 2)
            assert m[0][0]*m[1][1]-m[0][1]*m[1][0] == C(Q(2))
    y = [[mm[u][v][j][k] for v in range(r) for k in range(2)]
         for u in range(r) for j in range(2)]
    assert rank(y) == 4
    count = 0
    for u in range(r):
        for up in range(r):
            if u == up:
                continue
            for v in range(r):
                p = scale(mul(mm[u][v], star(mm[up][v])), Q(1, 2))
                assert p[0][1] == bb[v]*(aa[up]-aa[u])/2
                for vp in range(r):
                    if v == vp:
                        continue
                    # Expand all four original factors, independently of P_v P_vp*.
                    w = scale(mul(mul(mul(mm[u][v], star(mm[up][v])),
                                      mm[up][vp]), star(mm[u][vp])), Q(1, 4))
                    da = aa[u]-aa[up]
                    db = bb[v]-bb[vp]
                    expected = ONE - da*da.conj()*db*db.conj()/8
                    assert (w[0][0]+w[1][1])/2 == expected
                    assert expected.re < 1 and expected.im == 0
                    diff = [[ident(2)[i][j]-w[i][j] for j in range(2)] for i in range(2)]
                    assert rank(diff) == 2
                    count += 1
    assert count == r*r*(r-1)*(r-1)
    return {"r": r, "D": 2, "Y_rank": 4, "nondegenerate_rectangles": count,
            "all_rectangle_difference_ranks": 2,
            "putative_trace_free_rank_lower_bound": str(Q(2*r*r, 2*r-1)),
            "counterexample_to_that_bound": 4 < Q(2*r*r, 2*r-1)}


if __name__ == "__main__":
    results = [run(r) for r in (4, 6)]
    out = {"arithmetic": "exact rational complex numbers Q(i)", "results": results}
    path = Path(__file__).with_name("checks.json")
    path.write_text(json.dumps(out, indent=2)+"\n")
    print(json.dumps(out, indent=2))
