"""Small exact and floating fixtures for RESULT.txt; not a formal proof.

Run with system Python (numpy, sympy) or the local research venv.
No optimization solver is needed for these fixtures.
"""
import json
from pathlib import Path
import numpy as np
import sympy as s


def exact_qubit_fixture():
    eye = s.eye(2)
    x = s.Matrix([[0, 1], [1, 0]])
    y = s.Matrix([[0, -s.I], [s.I, 0]])
    z = s.diag(1, -1)
    tau = lambda a: s.simplify(s.trace(a) / 2)
    eq = lambda a, b: all(s.simplify(v) == 0 for v in a-b)
    kraus = []
    for b in range(2):
        k = s.zeros(4, 2)
        for i in range(2):
            k[2*i+b, i] += 1/s.sqrt(6)
            k[2*b+i, i] += 1/s.sqrt(6)
        kraus.append(k)
    assert eq(sum((k.adjoint()*k for k in kraus), s.zeros(2)), eye)
    pull = lambda a: s.simplify(sum((k.adjoint()*a*k for k in kraus), s.zeros(2)))
    phi = lambda a: pull(s.kronecker_product(a, eye))
    for a in [x, y, z]:
        assert eq(phi(a), 2*a/3)
        assert eq(pull(s.kronecker_product(eye, a)), 2*a/3)
    design = []
    for ax in [-1, 1]:
        for bz in [-1, 1]:
            fx = (eye+ax*x)/2
            gz = (eye+bz*z)/2
            effect = pull(s.kronecker_product(fx, gz))
            assert eq(effect, (eye+s.Rational(2, 3)*(ax*x+bz*z))/4)
            refined = s.zeros(2)
            for sign in [-1, 1]:
                p = (1+sign*2*s.sqrt(2)/3)/8
                proj = (eye+sign*(ax*x+bz*z)/s.sqrt(2))/2
                assert eq(proj*proj, proj)
                assert s.trace(proj) == 1
                assert p > 0
                design.append((p, proj))
                refined += 2*p*proj
            assert eq(refined, effect)
    barycenter = sum((p*proj for p, proj in design), s.zeros(2))
    assert eq(barycenter, eye/2)
    variance = s.simplify(sum(p*sum(s.trace(proj*a*a)-s.trace(proj*a)**2
                                  for a in [x, z]) for p, proj in design))
    energy = s.simplify(sum(tau(a*(a-phi(a))) for a in [x, z]))
    assert variance == 1 and energy == s.Rational(2, 3)
    assert variance <= 2*energy
    # h1 for X,Z is exactly 1 by the unit-Bloch-sphere calculation in RESULT.
    target_left = s.simplify(2*sum(tau(a*phi(a)) for a in [x, z])-2)
    assert target_left == s.Rational(2, 3)
    # Full qubit selector for the universal cloner: six axis states.
    axis_design = [(s.Rational(1, 6), (eye+sign*a)/2)
                   for a in [x, y, z] for sign in [-1, 1]]
    psi = lambda a: s.simplify(sum((2*p*s.trace(proj*a)*proj
                                   for p, proj in axis_design), s.zeros(2)))
    for a in [x, y, z]:
        assert eq(psi(a), a/3)
        assert eq(a-psi(a), 2*(a-phi(a)))
    return {"status": "EXACT_SYMBOLIC_FIXTURE_PASSED",
            "dimension": 2, "rank_two_design_outcomes": len(design),
            "average_variance": str(variance), "twice_energy": str(2*energy),
            "h1_XZ_exact": "1", "target_left": str(target_left),
            "full_cloner_comparator": "six axis states, moment I_3/3"}


def cloner_kraus(d):
    out = []
    for b in range(d):
        k = np.zeros((d*d, d), complex)
        for i in range(d):
            k[i*d+b, i] += 1/np.sqrt(2*(d+1))
            k[b*d+i, i] += 1/np.sqrt(2*(d+1))
        out.append(k)
    return out


def exact_tree_fixture():
    """Two actual splitter levels; finite fixture for the C.2 marginal rule."""
    eye = s.eye(2)
    paul = [s.Matrix([[0, 1], [1, 0]]),
            s.Matrix([[0, -s.I], [s.I, 0]]), s.diag(1, -1)]
    eq = lambda a, b: all(s.simplify(v) == 0 for v in a-b)
    primitive = []
    for b in range(2):
        k = s.zeros(4, 2)
        for i in range(2):
            k[2*i+b, i] += 1/s.sqrt(6)
            k[2*b+i, i] += 1/s.sqrt(6)
        primitive.append(k)
    tree = [s.kronecker_product(a, b)*c
            for a in primitive for b in primitive for c in primitive]
    pull = lambda a: sum((k.adjoint()*a*k for k in tree), s.zeros(2))
    assert eq(sum((k.adjoint()*k for k in tree), s.zeros(2)), eye)
    for leaf in range(4):
        for a in paul:
            factors = [a if i == leaf else eye for i in range(4)]
            assert eq(pull(s.kronecker_product(*factors)), 4*a/9)
    effect_sum = s.zeros(2)
    meter = 0
    for sx in [-1, 1]:
        for sy in [-1, 1]:
            for sz in [-1, 1]:
                signs = [sx, sy, sz]
                factors = [(eye+sgn*a)/2 for sgn, a in zip(signs, paul)]+[eye]
                effect = pull(s.kronecker_product(*factors))
                effect_sum += effect
                for a, sign in zip(paul, signs):
                    error = a-sign*eye
                    meter += s.trace(error*effect*error)/2
    assert eq(effect_sum, eye)
    assert s.simplify(meter) == s.Rational(10, 3)
    # Exact samples support, but do not replace, the signed scalar proof.
    for lam in [s.Rational(t, 4) for t in range(-4, 5)]:
        for m in range(1, 8):
            assert 0 <= 1-lam**m <= m*(1-lam)
    return {"status": "EXACT_SYMBOLIC_TREE_FIXTURE_PASSED",
            "levels": 2, "receivers": 4, "primitive_splitter_calls": 3,
            "tree_Kraus_count": len(tree), "leaf_Pauli_multiplier": "4/9",
            "three_factor_meter_error": "10/3",
            "signed_scalar_grid": "9 rational eigenvalues x 7 powers"}


def bounded_capacity_span_fixture():
    """Exact d=4 instance of C.3; the dimension-uniform proof is in RESULT."""
    d = 4
    eye = s.eye(d)
    x = s.Matrix([[0, 1], [1, 0]])
    y = s.Matrix([[0, -s.I], [s.I, 0]])
    z = s.diag(1, -1)
    operators = [s.kronecker_product(a, b)
                 for a in [s.eye(2), x, y, z]
                 for b in [s.eye(2), x, y, z]][1:]
    assert len(operators) == 15
    for i, a in enumerate(operators):
        assert s.trace(a) == 0 and a*a == eye
        for j, b in enumerate(operators):
            assert s.trace(a*b)/d == int(i == j)
    amplitude = s.Rational(1, 2)
    states = [(eye+sign*amplitude*a)/d
              for a in operators for sign in [-1, 1]]
    assert sum(states, s.zeros(d))/len(states) == eye/d
    for rho in states:
        assert rho.eigenvals() == {s.Rational(1, 8): 2, s.Rational(3, 8): 2}
    deficit = s.simplify(((1+amplitude)*s.log(1+amplitude)
                         +(1-amplitude)*s.log(1-amplitude))/2)
    assert s.simplify(deficit-(3*s.log(3)/4-s.log(2))) == 0
    return {"status": "EXACT_SYMBOLIC_CAPACITY_SPAN_FIXTURE_PASSED",
            "dimension": d, "state_count": len(states), "score_span_dimension": 15,
            "Holevo_capacity_nats_exact": str(deficit),
            "Holevo_capacity_nats_decimal": float(deficit),
            "uniform_tail_lower_bound": "(1/2) sqrt(1-r/15)"}


def rank_two_fixture(d, rng):
    eye = np.eye(d)
    kk = cloner_kraus(d)
    pull = lambda a: sum((k.conj().T@a@k for k in kk), np.zeros((d, d), complex))
    aa = []
    for _ in range(2):
        a = rng.normal(size=(d, d))+1j*rng.normal(size=(d, d))
        a = (a+a.conj().T)/2
        a -= np.trace(a)*eye/d
        a /= np.sqrt(np.trace(a@a).real/d)
        aa.append(a)
    av, au = np.linalg.eigh(aa[0])
    bv, bu = np.linalg.eigh(aa[1])
    design = []
    meter = 0.0
    for a in range(d):
        f = np.outer(au[:, a], au[:, a].conj())
        for b in range(d):
            g = np.outer(bu[:, b], bu[:, b].conj())
            effect = pull(np.kron(f, g))
            ew, ev = np.linalg.eigh(effect)
            assert ew[0] > -1e-12
            for j in range(d):
                if ew[j] > 1e-14:
                    proj = np.outer(ev[:, j], ev[:, j].conj())
                    design.append((ew[j]/d, proj))
            for ai, ci in zip(aa, [av[a], bv[b]]):
                e = ai-ci*eye
                meter += np.trace(e@effect@e).real/d
    barycenter = sum((p*proj for p, proj in design), np.zeros((d, d), complex))
    var = sum(p*sum((np.trace(proj@a@a)-np.trace(proj@a)**2).real for a in aa)
              for p, proj in design)
    energy = sum(np.trace(a@(a-pull(np.kron(a, eye)))).real/d for a in aa)
    residue = float(np.max(np.abs(barycenter-eye/d)))
    assert residue < 2e-12 and abs(meter-2*energy) < 2e-11
    assert var <= 2*energy+2e-11
    return {"status": "FLOATING_FIXTURE_PASSED", "dimension": d,
            "pure_outcomes": len(design), "barycenter_max_residual": residue,
            "average_variance": float(var), "twice_energy": float(2*energy),
            "meter_error_identity_residual": float(abs(meter-2*energy))}


def paulis(n):
    d = 2**n
    x = np.array([[0, 1], [1, 0]], complex)
    z = np.diag([1, -1]).astype(complex)
    eye = np.eye(2)
    pp = []
    for label in range(d*d):
        xp, zp = label % d, label // d
        p = np.ones((1, 1), complex)
        for bit in range(n):
            p = np.kron(p, (x if (xp >> bit) & 1 else eye)
                        @ (z if (zp >> bit) & 1 else eye))
        p *= 1j**((xp & zp).bit_count())
        assert np.max(np.abs(p-p.conj().T)) < 1e-12
        pp.append(p)
    return pp


def pauli_cloner_fixture(n, rng):
    d, nn = 2**n, 4**n
    sp = lambda a, b: (((a % d) & (b // d)).bit_count()
                       + ((a // d) & (b % d)).bit_count()) % 2
    ff = np.array([[(-1)**sp(a, b)/d for b in range(nn)] for a in range(nn)])
    q = rng.exponential(size=nn-1)
    q /= q.sum()
    hh = np.zeros((nn, nn))
    for v in range(1, nn):
        xx = np.zeros((nn, nn)); xx[np.arange(nn), np.arange(nn)^v] = 1
        dd = np.diag([(-1)**sp(u, v) for u in range(nn)])
        hh += q[v-1]*(dd+xx)/2
    vals, vecs = np.linalg.eigh(hh)
    a = vecs[:, -1]
    if a[0] < 0:
        a = -a
    assert a.min() > 0 and np.max(np.abs(ff@a-a)) < 3e-12
    pp = paulis(n)
    bell0 = np.eye(d).reshape(d*d)/np.sqrt(d)
    bell = [(np.kron(np.eye(d), p)@bell0).reshape(d, d) for p in pp]
    omega = sum(av*np.einsum('ra,be->rabe', bb, bb.conj()) for av, bb in zip(a, bell))
    rec = np.array([np.vdot(np.einsum('rb,ae->rabe', bb, bb.conj()), omega)
                    for bb in bell])
    assert np.max(np.abs(rec-ff@a)) < 3e-12
    jjra = omega.reshape(nn, nn)@omega.reshape(nn, nn).conj().T
    rbx = omega.transpose(0, 2, 1, 3).reshape(nn, nn)
    jjrb = rbx@rbx.conj().T
    assert np.max(np.abs(jjra-jjrb)) < 3e-12
    lam = np.array([np.trace(jjra@np.kron(p.T, p)).real for p in pp])
    predicted = np.array([sum((-1)**sp(v, u)*a[u]**2 for u in range(nn))
                          for v in range(nn)])
    assert np.max(np.abs(lam-predicted)) < 3e-12
    assert lam.min() > -3e-12
    objective_residual = abs(float(q@lam[1:])-vals[-1])
    assert objective_residual < 3e-12
    return {"status": "FLOATING_ACTUAL_CHANNEL_FIXTURE_PASSED", "qubits": n,
            "dimension": d, "recoupling_max_residual": float(np.max(np.abs(rec-ff@a))),
            "equal_Choi_marginal_max_residual": float(np.max(np.abs(jjra-jjrb))),
            "Phi_min_L2_eigenvalue": float(lam[1:].min()),
            "weighted_correlation_spectral_residual": float(objective_residual)}


def main():
    rng = np.random.default_rng(9346712)
    out = {"warning": "Fixtures verify explicit instances and conventions, not the universal theorem.",
           "exact": exact_qubit_fixture(),
           "tree": exact_tree_fixture(),
           "capacity_span": bounded_capacity_span_fixture(),
           "rank_two": [rank_two_fixture(d, rng) for d in [2, 3, 4]],
           "Pauli": [pauli_cloner_fixture(n, rng) for n in [1, 2]]}
    target = Path(__file__).with_suffix('.json')
    target.write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
