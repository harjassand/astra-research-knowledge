"""Native quantum erasure of a finite Toom island, and its driven response.

The healthy exterior is an explicit local diagnostic, not an assumption made
about the continually driven torus. Exact checks and floating controls are
kept separate. This program neither installs packages nor edits old work.
"""
from __future__ import annotations

import hashlib
import itertools
import json
from collections import deque
from fractions import Fraction
from pathlib import Path

import numpy as np
import sympy as s
from scipy.linalg import expm, eigvalsh
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import expm_multiply

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs/logical_phase_20261101"


def geometry(a, b):
    return [(y*a+x, y*a+x-1 if x else None,
             (y-1)*a+x if y else None)
            for y in range(b) for x in range(a)]


def bit(state, i):
    return 0 if i is None else (state >> i) & 1


def update(state, loc):
    i, left, down = loc
    active = bit(state, i) != bit(state, left) and bit(state, i) != bit(state, down)
    return state ^ (1 << i) if active else state


def matrices(a, b):
    dm = 1 << (a*b)
    Q = np.zeros((dm, dm), dtype=int)
    jumps = []
    flips = []
    for loc in geometry(a, b):
        J = np.zeros((dm, dm), dtype=int)
        P = np.zeros((dm, dm), dtype=int)
        F = np.zeros((dm, dm), dtype=int)
        for state in range(dm):
            F[state ^ (1 << loc[0]), state] = 1
            nxt = update(state, loc)
            if nxt != state:
                J[nxt, state] = 1
                P[state, state] = 1
                Q[nxt, state] += 1
                Q[state, state] -= 1
        jumps.append((J, P))
        flips.append(F)
    return Q, jumps, flips


def exact_structure():
    cases = []
    for a, b in [(1, 1), (2, 1), (2, 2)]:
        Q, jumps, _ = matrices(a, b)
        dm = Q.shape[0]
        assert np.all(Q.sum(axis=0) == 0)
        assert np.all(Q[:, 0] == 0)
        # Exact integer adjoint: every diagonal observable stays diagonal,
        # for both native generators. The inactive adjoint is exactly zero.
        for target in range(dm):
            F = np.zeros((dm, dm), dtype=int)
            F[target, target] = 1
            D2 = np.zeros_like(F)
            for J, P in jumps:
                D2 += 2*J.T@F@J - P@F - F@P
                R = np.eye(dm, dtype=int)-P
                assert np.array_equal(2*R@F@R-R@F-F@R, np.zeros_like(F))
            assert np.array_equal(D2, 2*np.diag(Q[target, :]))

        # Exhaust the finite joint process: the universal permanent-zero
        # clock certificate dominates every initial configuration.
        initial = [(state, dm-1) for state in range(dm)]
        seen = set(initial)
        todo = deque(initial)
        transitions = 0
        while todo:
            state, cert = todo.popleft()
            assert state & ~cert == 0
            for loc in geometry(a, b):
                i, left, down = loc
                nc = cert
                if not bit(cert, left) and not bit(cert, down):
                    nc &= ~(1 << i)
                ns = update(state, loc)
                assert ns & ~nc == 0
                transitions += 1
                pair = (ns, nc)
                if pair not in seen:
                    seen.add(pair)
                    todo.append(pair)
        cases.append(dict(a=a, b=b, initial_configurations=dm,
                          reachable_joint_states=len(seen),
                          exact_clock_transitions=transitions))

    # A rational upper bound ln(2)<7/10, used in the driven certificate.
    assert sum(s.Rational(7, 10)**j/s.factorial(j) for j in range(4)) > 2
    return dict(cases=cases, diagonal_population_closure="exact integer identity",
                quantum_return="diamond distance to vacuum reset <= min(2,2 sqrt(p)+2 p)",
                classical_tail="p <= min(1,4^(a+b-1) exp(-kappa t/2))",
                integrated_return_upper="8 ((a+b) ln(2)+1)/kappa",
                scope="All-size proof is in ISLAND_RETURN.txt; finite exact checks do not establish a global driven phase")


def stationary_one_site():
    h = s.Rational(1, 1024)
    X = s.Matrix([[0, 1], [1, 0]])
    J = s.Matrix([[0, 1], [0, 0]])
    R = s.diag(1, 0)
    x, y, z = s.symbols("x y z", real=True)
    rho = s.Matrix([[1-z, x+s.I*y], [x-s.I*y, z]])
    results = []
    for model in ["active", "completed"]:
        L = -s.I*h*(X*rho-rho*X)
        for A in ([J] if model == "active" else [J, R]):
            D = A.T.conjugate()*A
            L += A*rho*A.T.conjugate()-(D*rho+rho*D)/2
        sol = s.solve([s.re(L[0, 1]), s.im(L[0, 1]), L[1, 1]], [x, y, z])
        stationary = s.simplify(rho.subs(sol))
        assert s.simplify(L.subs(sol)) == s.zeros(2)
        assert stationary.det() >= 0
        distance_squared = s.simplify(4*(sol[z]**2+sol[x]**2+sol[y]**2))
        expected_population = 4*h*h/(1+8*h*h) if model == "active" else 2*h*h/(1+4*h*h)
        assert sol[z] == expected_population
        results.append(dict(model=model, h_over_kappa=str(h),
                            exact_excited_probability=str(sol[z]),
                            exact_reset_distance_squared=str(distance_squared),
                            reset_distance_preview=float(s.sqrt(distance_squared))))
    return results


def generator(a, b, model, h):
    Q, js, fs = matrices(a, b)
    dm = Q.shape[0]
    db = 2
    D = dm*db
    I = np.eye(D)
    ib = np.eye(db)
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    Z = np.diag([1., -1.])
    H = np.kron(np.eye(dm), X/8+Z/16)
    for i, F in enumerate(fs):
        B = [(ib+Z)/2, X, Y, Z][i % 4]
        H += h*np.kron(F, B)
    G = -1j*(np.kron(I, H)-np.kron(H.T, I))
    for J, P in js:
        for A in ([J] if model == "active" else [J, np.eye(dm)-P]):
            K = np.kron(A, ib)
            R = K.conj().T@K
            G += np.kron(K.conj(), K)-(np.kron(I, R)+np.kron(R.T, I))/2
    return Q, csr_matrix(G), dm, db, np.trace(G)


def reset_memory(A, dm, db):
    marginal = np.einsum("iaib->ab", A.reshape(dm, db, dm, db))
    result = np.zeros_like(A)
    result[:db, :db] = marginal
    return result


def driven_controls():
    rows = []
    a = b = 2
    Hdepth = a+b-1
    h = Fraction(1, 1024)
    # Fully unconditional drive at every face of this box, norm <= h per
    # term; common noncommuting bath, no resets. Healthy exterior is the
    # diagnostic's boundary condition, not a replacement of torus dynamics.
    rational_bound = min(Fraction(2), 16*(a*b*h)*((Hdepth+1)*Fraction(7, 10)+1))
    assert rational_bound == Fraction(19, 80)
    for model in ["active", "completed"]:
        for drive in [0., float(h)]:
            Q, G, dm, db, traceG = generator(a, b, model, drive)
            D = dm*db
            # Drive controls start at the island vacuum with a bath-reference
            # Bell pair. Quiet controls include a coherent island error
            # entangled with BOTH bath and reference.
            s0, s1 = (0, dm-1) if drive == 0 else (0, 0)
            vectors = []
            for rr, ss in [(0, s0), (1, s1)]:
                v = np.zeros(D);v[ss*db+rr] = 1
                vectors.append(v)
            ops = [np.outer(vectors[i], vectors[j]).reshape(-1, order="F")
                   for i in range(db) for j in range(db)]
            for T in [5., 25., 100.]:
                ev = expm_multiply(G*T, np.array(ops).T, traceA=traceG*T)
                joint = np.zeros((D*db, D*db), dtype=complex)
                comp = np.zeros_like(joint)
                for index, (i, j) in enumerate(itertools.product(range(db), repeat=2)):
                    A = ev[:, index].reshape(D, D, order="F")
                    R = np.zeros((db, db));R[i, j] = .5
                    joint += np.kron(A, R)
                    comp += np.kron(reset_memory(A, dm, db), R)
                dist = float(np.linalg.svd(joint-comp, compute_uv=False).sum())
                assert abs(np.trace(joint)-1) < 1e-10
                assert eigvalsh((joint+joint.conj().T)/2)[0] > -1e-10
                if drive == 0:
                    kernel = expm(Q*T)
                    worst = float(1-kernel[0, :].min())
                    assert worst <= min(1., 4.**Hdepth*np.exp(-T/2))+1e-12
                    bound = min(2., 2*np.sqrt(max(0., worst))+2*worst)
                else:
                    worst = None
                    bound = float(rational_bound)
                assert dist <= bound+1e-10
                rows.append(dict(model=model, T=T, h_over_kappa=str(h) if drive else "0",
                                 worst_population_survival_preview=worst,
                                 entangled_input_trace_distance_preview=dist,
                                 proved_uniform_diamond_upper=str(rational_bound) if drive else
                                 "min(2,2 sqrt(p(t))+2 p(t))",
                                 evaluated_upper_preview=bound))
    return dict(cases=rows, drive_certificate=str(rational_bound),
                persistent_bath_dimension=2,
                scope="Finite floating semigroup controls with an exact analytic 19/80 driven bound; no global torus phase or logical lifetime claim")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    data = dict(exact_structure=exact_structure(),
                exact_one_site=stationary_one_site(),
                actual_native_controls=driven_controls())
    data["program_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    (OUT/"island_controls.json").write_text(json.dumps(data, indent=2)+"\n")
    print(json.dumps(dict(output=str(OUT/"island_controls.json"), checks=list(data))))


if __name__ == "__main__":
    main()
