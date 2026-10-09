#!/usr/bin/env python3
"""One prescribed exact noncommuting p=4 replay and sharpness-Hessian check.

All arithmetic is rational or Gaussian rational; no floating arithmetic,
numerical search, transcendental evaluation, or eigenvalue sampling. This
checks identities at a single fixture, not the general positivity theorem.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import sys


@dataclass(frozen=True)
class C:
    r: F = F(0)
    i: F = F(0)

    def __post_init__(self):
        object.__setattr__(self, "r", F(self.r))
        object.__setattr__(self, "i", F(self.i))

    @staticmethod
    def of(x):
        return x if isinstance(x, C) else C(x)

    def __add__(self, x):
        x = C.of(x)
        return C(self.r+x.r, self.i+x.i)

    __radd__ = __add__

    def __neg__(self):
        return C(-self.r, -self.i)

    def __sub__(self, x):
        return self + -C.of(x)

    def __rsub__(self, x):
        return C.of(x) + -self

    def __mul__(self, x):
        x = C.of(x)
        return C(self.r*x.r-self.i*x.i, self.r*x.i+self.i*x.r)

    __rmul__ = __mul__

    def __truediv__(self, x):
        return self * (1/F(x))

    def star(self):
        return C(self.r, -self.i)


def diag(xs):
    return [[C(x) if i == j else C() for j in range(len(xs))]
            for i, x in enumerate(xs)]


def add(a, b):
    return [[x+y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def scale(a, r):
    return [[r*x for x in ar] for ar in a]


def mul(a, b):
    return [[sum((a[i][k]*b[k][j] for k in range(len(b))), C())
             for j in range(len(b[0]))] for i in range(len(a))]


def adj(a):
    return [[a[j][i].star() for j in range(len(a))]
            for i in range(len(a[0]))]


def tr(a):
    return sum((a[i][i] for i in range(len(a))), C())


def comm(a, b):
    return add(mul(a, b), scale(mul(b, a), -1))


def ch(exp_x):
    return (exp_x+1/exp_x)/2


def sh(exp_x):
    return (exp_x-1/exp_x)/2


def record_rational(x):
    return str(x)


def run():
    # Faithful raw s; normalizing sigma rescales coordinates covariantly.
    svals = [F(1), F(16), F(256)]
    s = diag(svals)
    sr = diag([1, 2, 4])  # s^(1/4), p=4, mu=1/2
    sri = diag([F(1), F(1, 2), F(1, 4)])
    v = [F(1), F(2), F(3)]
    O = [[C((1 if i == j else 0)-v[i]*v[j]/7)
          for j in range(3)] for i in range(3)]
    phases = [C(1), C(0, 1), C(F(3, 5), F(4, 5))]
    U = [[phases[i]*O[i][j] for j in range(3)] for i in range(3)]
    assert mul(adj(U), U) == diag([1, 1, 1])
    B = [[C(1), C(2, 3), C(-1, 2)],
         [C(2, -3), C(-2), C(3, -1)],
         [C(-1, -2), C(3, 1), C(F(1, 2))]]
    assert adj(B) == B
    BsB = mul(mul(B, s), B)
    V = [[2*BsB[i][j]/(svals[i]+svals[j]) for j in range(3)]
         for i in range(3)]
    assert adj(V) == V

    def H(X):
        return add(scale(add(mul(V, X), mul(X, V)), F(1, 2)),
                   scale(mul(mul(B, X), B), -1))

    assert H(s) == diag([0, 0, 0])
    qs = [F(1), F(4), F(9)]
    roots = [F(1), F(2), F(3)]

    def spectral(vals):
        return mul(mul(U, diag(vals)), adj(U))

    q = spectral(qs)
    qhalf = spectral(roots)
    qthreehalf = spectral([F(1), F(8), F(27)])
    assert mul(qhalf, qhalf) == q
    assert comm(q, s) != diag([0, 0, 0])
    assert any(x.i for row in q for x in row)
    physical_F = tr(mul(mul(mul(qthreehalf, sri),
                           H(mul(mul(sr, qhalf), sr))), sri))
    physical_E = tr(mul(q, H(q)))
    assert physical_F.i == physical_E.i == 0

    # Frequencies are n log16; no logarithms need evaluation.
    positions = [0, 1, 2]
    Bf = {}
    for n in range(-2, 3):
        Bn = [[B[i][j] if positions[i]-positions[j] == n else C()
               for j in range(3)] for i in range(3)]
        Bf[n] = mul(mul(adj(U), Bn), U)
    for n in Bf:
        assert Bf[-n] == adj(Bf[n])

    gram_F = C()
    gram_E = C()
    pairs_F, pairs_E = [], []
    for i in range(3):
        row_F, row_E = [], []
        for j in range(3):
            term_F, term_E = C(), C()
            for n in Bf:
                for m in Bf:
                    exp_mid = (qs[i]/qs[j]) / (F(4)**(n+m))
                    exp_halfdiff = F(4)**(m-n)
                    exp_mu_halfdiff = F(2)**(m-n)
                    exp_mu_mid = (roots[i]/roots[j])/(F(2)**(n+m))
                    Lmu = (ch(exp_mid)*ch(exp_mu_halfdiff)
                           /ch(exp_halfdiff)-ch(exp_mu_mid))
                    Lzero = ch(exp_mid)/ch(exp_halfdiff)-1
                    amp = Bf[n][i][j].star()*Bf[m][i][j]
                    term_F += qs[i]*qs[j]*amp*Lmu
                    term_E += qs[i]*qs[j]*amp*Lzero
            assert term_F.i == term_E.i == 0
            row_F.append(record_rational(term_F.r))
            row_E.append(record_rational(term_E.r))
            gram_F += term_F
            gram_E += term_E
        pairs_F.append(row_F)
        pairs_E.append(row_E)
    assert gram_F == physical_F
    assert gram_E == physical_E
    assert all(pairs_F[i][i] != "0" for i in range(3))

    # Independently check every entry of the physical sharpness congruence
    # at nonzero real nodes x_i=4 log a_i, p=4, r=1/4.
    aa = [F(2), F(3), F(5)]
    leaf_s = [a**-4 for a in aa]  # unnormalized s0=1
    A0 = sum(leaf_s, F())
    congruence = []
    for i, ai in enumerate(aa):
        row = []
        for j, aj in enumerate(aa):
            vi = 2*A0/(leaf_s[i]+leaf_s[j])
            Di, Dj = sh(ai**3)/sh(ai), sh(aj**3)/sh(aj)
            Ci, Cj = sh(ai**2)/sh(ai), sh(aj**2)/sh(aj)
            di, dj = ai**2/sh(ai), aj**2/sh(aj)
            Lmu = ch(ai**2*aj**2)*ch(ai/aj)/ch(ai**2/aj**2)-ch(ai*aj)
            Lzero = ch(ai**2*aj**2)/ch(ai**2/aj**2)-1
            lhs_const, lhs_eta = vi*(Di+Dj)/2, -vi*Ci*Cj
            rhs_const, rhs_eta = A0*di*dj*Lmu/2, -A0*di*dj*Lzero/2
            assert lhs_const == rhs_const and lhs_eta == rhs_eta
            # Exact power divided differences at stationary node x_i=4 log ai.
            direct_D = ai**2*(1-ai**-6)/(1-ai**-2)
            direct_C = ai*(1-ai**-4)/(1-ai**-2)
            assert Di == direct_D == ai**2+1+ai**-2
            assert Ci == direct_C == ai+ai**-1
            row.append({"constant":str(lhs_const),"eta_coefficient":str(lhs_eta)})
        congruence.append(row)

    return {
        "status":"PASS",
        "arithmetic":"Python stdlib Gaussian rational and Fraction; no floating point",
        "profile_fixture":{"p":4,"mu":"1/2","local_dimension":3,
                           "raw_s":[str(x) for x in svals],
                           "q_eigenvalues":[str(x) for x in qs],
                           "full_complex_noncommuting_input":True},
        "physical_raw_KT_pairing_F":str(physical_F.r),
        "physical_root_energy_E":str(physical_E.r),
        "ordered_state_pair_F":pairs_F,
        "ordered_state_pair_E":pairs_E,
        "factor_one_full_complex_Gram":True,
        "nonzero_diagonal_pairs":True,
        "physical_sharpness_Hessian_congruence_all_entries":congruence,
        "scan_count":0,
        "scope":"Exact identity diagnostics only; all-p positivity and sharpness are proved analytically in separate reports."
    }


def main():
    here = Path(__file__).resolve().parent
    output = here/"EXPOSED_P4_EXACT_REPLAY.json"
    result = run()
    if sys.argv[1:] == ["--verify"]:
        assert json.loads(output.read_text()) == result
        print("PASS: frozen exact complex Gram and physical Hessian replay match.")
    elif not sys.argv[1:]:
        with output.open("x") as file:
            json.dump(result, file, indent=2, sort_keys=True)
            file.write("\n")
        print("PASS: wrote exact prescribed p4 replay.")
    else:
        raise SystemExit("Usage: verify_exposed_p4_exact.py [--verify]")
    print("replay_sha256", hashlib.sha256(output.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
