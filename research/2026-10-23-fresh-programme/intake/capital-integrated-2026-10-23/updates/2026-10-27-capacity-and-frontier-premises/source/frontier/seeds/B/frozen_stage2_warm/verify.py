"""Exact rational matrix checks of certificate obstructions, not target positivity."""
from itertools import product
import json
import sympy as s


def check(ok, name):
    if not ok:
        raise RuntimeError(name)


def zero(m):
    return all(s.expand(x) == 0 for x in m)


def tr(m):
    return s.expand(s.trace(m))


def local(d):
    eye = s.eye(d*d)
    omega = s.Matrix([int(i == j) for i in range(d) for j in range(d)])
    oo = omega*omega.T
    ff = s.zeros(d*d)
    for i, j in product(range(d), repeat=2):
        ff[i*d+j, j*d+i] = 1
    pp = oo/d
    aa, tt = (eye-ff)/2, (eye+ff)/2
    return {"I": eye, "O": oo, "F": ff, "P": pp,
            "Q": eye-pp, "A": aa, "T": tt, "S": tt-pp}


def kron(a, b):
    return s.kronecker_product(a, b)


def idx(i, j, a, b):
    return ((i*3+j)*2+a)*2+b


def pt(m):
    out = s.zeros(36)
    for i, j, a, b, k, ell, c, d in product(
            range(3), range(3), range(2), range(2),
            range(3), range(3), range(2), range(2)):
        out[idx(i, ell, a, d), idx(k, j, c, b)] = m[idx(i, j, a, b), idx(k, ell, c, d)]
    return out


def sym(m):
    return (m+pt(m))/2


def frob(m):
    return s.expand(sum(s.conjugate(x)*x for x in m))


def q1(c):
    return s.expand(frob(c)-s.conjugate(tr(c))*tr(c)/2)


def q2(c):
    t0, t1 = s.zeros(3), s.zeros(3)
    for i, j, k in product(range(3), repeat=3):
        t0[i, j] += c[k*3+i, k*3+j]
        t1[i, j] += c[i*3+k, j*3+k]
    return s.expand(frob(c)-(frob(t0)+frob(t1))/2+s.conjugate(tr(c))*tr(c)/4)


def checks():
    l3, l2 = local(3), local(2)
    ii = kron(l3["I"], l2["I"])
    kk = l3["I"]-l3["O"]/2
    ww = kron(kk, l2["O"])
    wr = sym(ww)

    sigma_c = (4*kron(l3["P"], l2["P"])+kron(l3["Q"], l2["Q"]))/28
    check(tr(sigma_c) == 1, "complex separator trace")
    # Exact positive decomposition after the partial transpose.
    eig_c = [s.Integer(1), s.Rational(1, 3), 0, s.Rational(8, 3)]
    pt_decomp = s.zeros(36)
    for coefficient, (a, b) in zip(eig_c, product(("T", "A"), repeat=2)):
        check(coefficient >= 0, "complex separator PT sector nonnegative")
        pt_decomp += coefficient*kron(l3[a], l2[b])/28
    check(zero(pt(sigma_c)-pt_decomp), "complex separator PPT decomposition")
    margin_c = tr(sigma_c*ww)
    check(margin_c == -s.Rational(1, 7), "complex separator margin")

    positive = s.Rational(3, 7)*kron(l3["P"], l2["Q"])+s.Rational(12, 7)*kron(l3["Q"], l2["P"])
    copositive = s.Rational(4, 7)*kron(l3["A"], l2["T"])
    check(zero(ww+ii/7-positive-pt(copositive)), "attaining decomposable identity")

    sigma_r = (9*ii
               -3*kron(l3["I"], l2["F"]+l2["O"])
               -kron(l3["F"]+l3["O"], l2["I"])
               +7*(kron(l3["F"], l2["F"])+kron(l3["O"], l2["O"]))
               -3*(kron(l3["F"], l2["O"])+kron(l3["O"], l2["F"])))/240
    check(tr(sigma_r) == 1, "real separator trace")
    check(zero(pt(sigma_r)-sigma_r), "real separator PT invariance")
    eig_r = [s.Rational(1, 8), 0, s.Rational(1, 24),
             0, s.Rational(1, 20), s.Rational(1, 60),
             0, 0, s.Rational(1, 12)]
    real_decomp = s.zeros(36)
    for coefficient, (a, b) in zip(eig_r, product(("P", "S", "A"), repeat=2)):
        check(coefficient >= 0, "real separator sector nonnegative")
        real_decomp += coefficient*kron(l3[a], l2[b])
    check(zero(sigma_r-real_decomp), "real separator positive sector decomposition")
    margin_r = tr(sigma_r*wr)
    check(margin_r == -s.Rational(1, 8), "real separator margin")

    gram = (s.Rational(3, 4)*kron(l3["P"], l2["S"])
            +s.Rational(3, 2)*kron(l3["S"], l2["P"])
            +s.Rational(5, 2)*kron(l3["A"], l2["P"])
            +s.Rational(1, 2)*kron(l3["A"], l2["S"]))
    check(zero(sym(gram)-wr-ii/8), "attaining real SOS Gram identity")

    parameter = s.Symbol("t", real=True)
    wt = kron(l3["I"]-parameter*l3["O"], l2["O"])
    pc = (6*(3*parameter-1)*kron(l3["P"], l2["Q"])
          +6*(3-2*parameter)*kron(l3["Q"], l2["P"]))/7
    qc = 8*(3*parameter-1)*kron(l3["A"], l2["T"])/7
    check(zero(wt+2*(3*parameter-1)*ii/7-pc-pt(qc)),
          "parameterized complex attaining identity")
    gr = (s.Rational(3, 2)*(3*parameter-1)*kron(l3["P"], l2["S"])
          +3*(1-parameter)*kron(l3["S"], l2["P"])
          +(1+3*parameter)*kron(l3["A"], l2["P"])
          +(3*parameter-1)*kron(l3["A"], l2["S"]))
    check(zero(sym(gr)-sym(wt)-(3*parameter-1)*ii/4),
          "parameterized real attaining identity")
    check(s.expand(tr(sigma_c*wt)-2*(1-3*parameter)/7) == 0,
          "parameterized complex lower certificate")
    check(s.expand(tr(sigma_r*wt)-(1-3*parameter)/4) == 0,
          "parameterized real lower certificate")

    # Explicit Bell-link activation calculation. The input PPT state is
    # alpha = sigma_c^Gamma, not sigma_c.
    alpha = pt(sigma_c)
    rho = (2*l3["I"]-l3["F"])/15
    tau = s.zeros(4)
    for a, b, r, q in product(range(4), range(4), range(9), range(9)):
        tau[a, b] += rho[r, q]*alpha[r*4+a, q*4+b]/9
    expected_tau = (8*l2["I"]-5*l2["F"])/1890
    check(zero(tau-expected_tau), "explicit Bell-link activation state")
    check(tr(tau) == s.Rational(11, 945), "activation success probability")
    rho_t = (l3["I"]-parameter*l3["F"])/(9-3*parameter)
    tau_t = s.zeros(4)
    for a, b, r, q in product(range(4), range(4), range(9), range(9)):
        tau_t[a, b] += rho_t[r, q]*alpha[r*4+a, q*4+b]/9
    expected_t = (4*l2["I"]-(1+3*parameter)*l2["F"])/(378*(3-parameter))
    check(all(s.cancel(x) == 0 for x in tau_t-expected_t),
          "fixed activator whole-parameter identity")

    # Independent physical factorization check, with complex, nonorthogonal frames.
    u = s.Matrix([[1, s.I], [2, -1], [s.I, 1+s.I]])
    v = s.Matrix([[s.I, 2], [1-s.I, 1], [0, -s.I]])
    c = u*v.conjugate().T
    ab = s.zeros(36, 1)
    for i, j, a, b in product(range(3), range(3), range(2), range(2)):
        ab[idx(i, j, a, b)] = u[i, a]*s.conjugate(v[j, b])
    physical = s.expand((ab.conjugate().T*ww*ab)[0])
    check(s.expand(physical-q1(c)) == 0, "full rank-two quartic representation")
    flag = s.zeros(3); flag[0, 1] = 1
    check(q2(kron(c, flag)) == q1(c), "exact spectator partial-trace identity")

    # Constrained SOS check to prevent overstatement of the obstruction.
    uu = s.Matrix([[1, 0], [0, s.Rational(3, 5)], [0, s.I*s.Rational(4, 5)]])
    check(zero(uu.conjugate().T*uu-s.eye(2)), "Stiefel control")
    aa, bb = list(uu), list(v)
    lagrange = sum(s.conjugate(aa[i]*bb[j]-aa[j]*bb[i])*(aa[i]*bb[j]-aa[j]*bb[i])
                   for i in range(6) for j in range(i+1, 6))/2
    check(s.expand(q1(uu*v.conjugate().T)-lagrange) == 0, "valid constrained SOS control")

    return {"complex_margin": str(margin_c), "real_margin": str(margin_r),
            "complex_PT_sector_eigenvalues_times_28": [str(x) for x in eig_c],
            "real_sector_eigenvalues": [str(x) for x in eig_r],
            "complex_factorization_q": str(physical),
            "attaining_decomposable_identity": "PASS",
            "attaining_real_SOS_identity": "PASS",
            "parameterized_noise_threshold_identities": "PASS",
            "activation_success_probability": str(tr(tau)),
            "normalized_activation_PT_min_eigenvalue": "-1/11",
            "fixed_activator_parameter_identity": "PASS",
            "spectator_embedding": "PASS",
            "constrained_SOS_control": "PASS",
            "scope": "Exact finite algebra for certificate obstructions; no negative endpoint rank-two witness and no all-copy proof."}


if __name__ == "__main__":
    print(json.dumps(checks(), indent=2))
