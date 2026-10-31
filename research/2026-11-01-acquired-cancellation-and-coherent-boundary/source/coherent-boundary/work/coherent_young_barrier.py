"""Exact combinatorics and a finite quantum control for a Young-diagram barrier.

No installation, external service, random draw, or fitted constant is used.
The all-size argument is in outputs/coherent_boundary/PROOF.txt.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import deque
from fractions import Fraction as Q
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "coherent_boundary"


def bit(s: int, x: int, y: int, L: int) -> int:
    return (s >> ((y % L) * L + (x % L))) & 1


def pattern(s: int, x: int, y: int, L: int) -> tuple[int, ...]:
    """Syndrome bits on bottom, left, top, right boundary edges of a face."""
    z = bit(s, x, y, L)
    return (z ^ bit(s, x, y - 1, L), z ^ bit(s, x - 1, y, L),
            z ^ bit(s, x, y + 1, L), z ^ bit(s, x + 1, y, L))


def add_pattern(x: int, y: int, L: int) -> tuple[int, ...]:
    return (0, 0, int(y != L - 1), int(x != L - 1))


def base_drive(s: int, x: int, y: int, L: int) -> bool:
    p = pattern(s, x, y, L)
    a = add_pattern(x, y, L)
    return p == a or p == tuple(1 - v for v in a)


def bridge_patterns(x: int, y: int, L: int) -> list[tuple[int, ...]]:
    """Extra gates at the torus cuts. They annihilate the small Young sector.

    Their purpose is to keep the global model nontrivial: the all-face logical
    membrane is accessible, rather than being excluded by a hard wall.
    """
    a = []
    if x == 0:
        a.append((0, 1, int(y != L - 1), 1))
    if y == 0:
        a.append((1, 0, 1, int(x != L - 1)))
    return a


def bridge_drive(s: int, x: int, y: int, L: int) -> bool:
    p = pattern(s, x, y, L)
    return any(p == a or p == tuple(1 - v for v in a)
               for a in bridge_patterns(x, y, L))


def mask_of(h: tuple[int, ...], L: int) -> int:
    m = len(h)
    return sum(1 << (y * L + L - m + j)
               for j, height in enumerate(h)
               for y in range(L - height, L))


def heights_of(s: int, m: int, L: int) -> tuple[int, ...] | None:
    h = tuple(sum(bit(s, L - m + j, y, L) for y in range(L))
              for j in range(m))
    if h != tuple(sorted(h)) or max(h, default=0) > m:
        return None
    return h if mask_of(h, L) == s else None


def row_widths(h: tuple[int, ...]) -> tuple[int, ...]:
    m = len(h)
    # Bottom to top, just as columns run left to right.
    return tuple(sum(a >= m - i for a in h) for i in range(m))


def potential(h: tuple[int, ...]) -> Q:
    m = len(h)
    return sum((Q(2) ** (m - 1 - j) * Q(16) ** (a - m)
                for j, a in enumerate(h)), Q(0))


def active_deaths(h: tuple[int, ...]) -> list[tuple[int, ...]]:
    ans = []
    for j, a in enumerate(h):
        if a > (h[j - 1] if j else 0):
            v = list(h)
            v[j] -= 1
            ans.append(tuple(v))
    return ans


def check_geometry(m: int) -> dict:
    L = 2 * m + 4
    states = list(itertools.combinations_with_replacement(range(m + 1), m))
    masks = {mask_of(h, L): h for h in states}
    correction_checks = drive_checks = bridges_checked = exits = 0
    gamma0 = Q(15, 32)
    f0 = Q(2**m - 1, 16**m)
    max_slack = None
    exit_faces = {(L - 1, L - m - 1), (L - m - 1, L - 1)}
    for s, h in masks.items():
        expected = {mask_of(v, L) for v in active_deaths(h)}
        actual = set()
        for y in range(L):
            for x in range(L):
                b, l, _, _ = pattern(s, x, y, L)
                t = s ^ (1 << (y * L + x))
                if b == l == 1:
                    actual.add(t)
                correction_checks += 1
                assert not bridge_drive(s, x, y, L), (m, h, x, y, "bridge")
                bridges_checked += 1
                if base_drive(s, x, y, L):
                    drive_checks += 1
                    v = masks.get(t)
                    if v is None:
                        # A true safe-domain exit, at one of two anchored tips.
                        assert (x, y) in exit_faces, (h, x, y, "unexpected exit")
                        assert heights_of(t, m + 1, L) is not None
                        exits += 1
                    else:
                        assert sum(abs(a - b) for a, b in zip(h, v)) == 1
        assert actual == expected, (h, actual, expected)
        for v in (h, row_widths(h)):
            qf = sum((potential(u) - potential(v) for u in active_deaths(v)), Q(0))
            slack = qf + gamma0 * potential(v) - gamma0 * f0
            assert slack <= 0, (m, h, "classical drift", slack)
            max_slack = slack if max_slack is None else max(max_slack, slack)
        # Exact boundary domination; no state probability is used here.
        assert potential(h) >= int(max(h) == m)
        assert potential(row_widths(h)) >= int(max(row_widths(h)) == m)
    return dict(m=m, L=L, states=len(states), correction_predicates=correction_checks,
                allowed_coherent_transitions=drive_checks, safe_exits=exits,
                bridge_predicates=bridges_checked, source_per_potential=str(f0),
                largest_classical_slack=str(max_slack))


def logical_route(L: int = 4) -> dict:
    """0/1 shortest path: correction writes cost zero, coherent writes cost one."""
    target = (1 << (L * L)) - 1
    dist = {0: 0}
    prev = {}
    todo = deque([0])
    while todo:
        s = todo.popleft()
        for y in range(L):
            for x in range(L):
                p = pattern(s, x, y, L)
                typ = None
                if p[0] == p[1] == 1:
                    typ, cost = "native_correction", 0
                elif base_drive(s, x, y, L) or bridge_drive(s, x, y, L):
                    typ, cost = "coherent_write", 1
                if typ is None:
                    continue
                t = s ^ (1 << (y * L + x))
                d = dist[s] + cost
                if d < dist.get(t, L * L + 1):
                    dist[t] = d
                    prev[t] = (s, x, y, typ)
                    (todo.appendleft if cost == 0 else todo.append)(t)
    assert target in dist, "The proposed global model has a hard topological wall"
    path = []
    s = target
    while s:
        old, x, y, typ = prev[s]
        path.append(dict(x=x, y=y, kind=typ, before=hex(old), after=hex(s)))
        s = old
    path.reverse()
    return dict(L=L, reached=len(dist), minimal_coherent_writes=dist[target],
                correction_writes=sum(a["kind"] == "native_correction" for a in path),
                path=path,
                scope="Legal native path, not an actual logical failure-rate estimate")


def exact_local_operator_blocks() -> dict:
    # r=16, sqrt(r)=4, h/kappa=1/32. Each 2x2 block is PSD by
    # equal nonnegative diagonal and zero determinant after F_j scaling.
    h, alpha, gamma0 = Q(1, 32), Q(15, 4), Q(15, 32)
    gamma = gamma0 - 2 * h * alpha
    assert gamma == Q(15, 64)
    for a in range(10):
        fs, ft = Q(16)**a, Q(16)**(a + 1)
        ds, dt = h * alpha * fs, h * alpha * ft
        off2 = (h * (ft - fs)) ** 2
        assert ds >= 0 and dt >= 0 and ds * dt == off2
    return dict(h_over_kappa=str(h), gamma0_over_kappa=str(gamma0),
                gamma_over_kappa=str(gamma), alpha=str(alpha),
                rank_one_psd_blocks_checked=10,
                bath_extension="Block [[I, iB],[-iB*,I]] is PSD for every contraction B")


def countercontrols() -> dict:
    m, L = 4, 12
    empty = 0
    # A completely ordinary single Pauli outside the anchor is an immediate
    # coherent exit. It is excluded by the corner constraint, not suppressed.
    x, y = 3, 3
    assert heights_of(empty ^ (1 << (y * L + x)), m, L) is None
    winding = sum(1 << ((L - 1) * L + x) for x in range(L))
    assert not any(pattern(winding, x, y, L)[0:2] == (1, 1)
                   for y in range(L) for x in range(L))
    return dict(unconditioned_pauli_immediate_exit=dict(face=[x, y],
                    code_boundary_susceptibility_over_h_squared=1),
                winding_strip_active_pairs=0,
                equal_column_weight_plateau_drift_fraction=str(Q(1, m)),
                geometric_column_weight_plateau_drift_fraction=str(Q(2**(m - 1), 2**m - 1)))


def quantum_control(m: int = 3) -> dict:
    """Numerical generator control; the proof is the exact operator argument."""
    import numpy as np
    from scipy.linalg import eigvalsh
    hs = list(itertools.combinations_with_replacement(range(m + 1), m))
    idx = {a: i for i, a in enumerate(hs)}
    n = len(hs)
    X = np.array([[0, 1], [1, 0]], complex)
    Y = np.array([[0, -1j], [1j, 0]], complex)
    Z = np.diag([1., -1.]).astype(complex)
    I = np.eye(2)
    bath_ops = [X, Y, Z, (X + Z) / np.sqrt(2)]
    h = 1/32
    D = n * 2
    H = np.kron(np.eye(n), X/7 + Z/11)
    jumps = []
    inactive = []
    Fv = np.kron(np.diag([float(potential(a)) for a in hs]), I)
    Fh = np.kron(np.diag([float(potential(row_widths(a))) for a in hs]), I)
    for j in range(m):
        # Group by face, not by input syndrome; both-active coherences must
        # be transported together by the actual native correction operator.
        for height in range(1, m + 1):
            A = np.zeros((n, n), complex)
            P = np.zeros((n, n), complex)
            for a in hs:
                if a[j] == height and a[j] > (a[j-1] if j else 0):
                    b = list(a)
                    b[j] -= 1
                    A[idx[tuple(b)], idx[a]] = 1
                    P[idx[a], idx[a]] = 1
            if np.any(A):
                B = bath_ops[(j + 2 * height) % len(bath_ops)]
                H += h * (np.kron(A, B) + np.kron(A.conj().T, B.conj().T))
                jumps.append(np.kron(A, I))
                inactive.append(np.kron(np.eye(n) - P, I))
    fv0 = float(potential((0,) * m))
    gamma0, gamma = 15/32, 15/64
    fsum = Fv + Fh

    def dual(F, js):
        ans = 1j * (H @ F - F @ H)
        for J in js:
            A = J.conj().T @ J
            ans += J.conj().T @ F @ J - (A @ F + F @ A)/2
        return ans

    ans = {}
    for name, js in [("active", jumps), ("completed", jumps + inactive)]:
        residual = dual(fsum, js) + gamma * fsum - gamma0 * 2 * fv0 * np.eye(D)
        largest = float(eigvalsh(residual)[-1])
        assert largest < 1e-10
        if m > 3:
            continue
        # Exact finite-dimensional GKSL generator, column-vector convention.
        eye = np.eye(D)
        G = -1j * (np.kron(eye, H) - np.kron(H.T, eye))
        for J in js:
            A = J.conj().T @ J
            G += np.kron(J.conj(), J) - (np.kron(eye, A) + np.kron(A.T, eye))/2
        from scipy.sparse import csr_matrix
        traceG = np.trace(G)
        G = csr_matrix(G)
        rho0 = np.zeros((D, D), complex)
        # Pure persistent bath state |+y>, no reset and noncommuting couplings.
        vb = np.array([1, 1j]) / np.sqrt(2)
        rho0[:2, :2] = np.outer(vb, vb.conj())
        from scipy.sparse.linalg import expm_multiply
        times = [0., 1., 10., 100.]
        data = []
        Bdiag = np.array([int(max(a) == m) + int(max(row_widths(a)) == m) for a in hs])
        boundary = np.kron(np.diag(Bdiag), I)
        for t in times:
            rho = expm_multiply(G * t, rho0.reshape(-1, order="F"),
                               traceA=traceG*t).reshape(D, D, order="F")
            f = float(np.trace(fsum @ rho).real)
            q = float(np.trace(boundary @ rho).real)
            bound = 2*fv0 * (np.exp(-gamma*t) + gamma0/gamma*(1-np.exp(-gamma*t)))
            assert q <= f + 1e-10 and f <= bound + 1e-10
            assert abs(np.trace(rho)-1) < 1e-9
            data.append(dict(t=t, boundary_sum=q, potential=f, potential_bound=bound,
                             trace_error=float(abs(np.trace(rho)-1))))
        ans[name] = dict(hilbert_dimension=D, largest_operator_residual_eigenvalue=largest,
                         samples=data)
    ans["scope"] = "Floating-point control only; no numerical threshold or diamond certification"
    return ans


def crossed_css_control(m: int = 2) -> dict:
    """Two intersecting CSS planes and one common bath, with Pauli phases.

    In the Z_S X_T frame an X write has sign (-1)^(S at its face).
    The chosen planes intersect at their seed face. Face correction operators
    still transport all both-active dyads together.
    """
    import numpy as np
    from scipy.linalg import eigvalsh
    hs = list(itertools.combinations_with_replacement(range(m + 1), m))
    idx = {a: i for i, a in enumerate(hs)}
    n = len(hs)
    Is, Ib = np.eye(n), np.eye(2)
    X = np.array([[0, 1], [1, 0]], complex)
    Y = np.array([[0, -1j], [1j, 0]], complex)
    Z = np.diag([1., -1.]).astype(complex)
    parity = np.diag([(-1)**int(a[-1] > 0) for a in hs])
    H = np.kron(np.eye(n*n), X/7 + Z/11)
    js, inactive = [], []
    hz = np.zeros_like(H)
    hx = np.zeros_like(H)
    for j in range(m):
        for height in range(1, m+1):
            A, P = np.zeros((n,n), complex), np.zeros((n,n), complex)
            for a in hs:
                if a[j] == height and a[j] > (a[j-1] if j else 0):
                    b = list(a)
                    b[j] -= 1
                    A[idx[tuple(b)], idx[a]] = 1
                    P[idx[a], idx[a]] = 1
            if not np.any(A):
                continue
            sign = parity if (j, height) == (m-1, 1) else Is
            Az = np.kron(A, Is)
            Ax = np.kron(sign, A)
            Bz, Bx = (X if j == 0 else Z), (Y if height == 1 else (X+Z)/np.sqrt(2))
            hz += (np.kron(Az, Bz) + np.kron(Az.conj().T, Bz.conj().T))/32
            hx += (np.kron(Ax, Bx) + np.kron(Ax.conj().T, Bx.conj().T))/32
            js += [np.kron(Az, Ib), np.kron(Ax, Ib)]
            inactive += [np.kron(np.kron(Is-P, Is), Ib),
                         np.kron(np.kron(Is, Is-P), Ib)]
    H += hz + hx
    Fsingle = np.diag([float(potential(a)+potential(row_widths(a))) for a in hs])
    F = np.kron(np.kron(Fsingle, Is)+np.kron(Is, Fsingle), Ib)
    f0 = 4*float(potential((0,)*m))
    ans = dict(hilbert_dimension=len(H),
               noncommuting_sector_hamiltonian_norm=float(np.linalg.norm(hz@hx-hx@hz, 2)))
    assert ans["noncommuting_sector_hamiltonian_norm"] > 0
    for name, jops in [("active", js), ("completed", js+inactive)]:
        res = 1j*(H@F-F@H)+(15/64)*F-(15/32)*f0*np.eye(len(H))
        for J in jops:
            A = J.conj().T@J
            res += J.conj().T@F@J-(A@F+F@A)/2
        maximum = float(eigvalsh(res)[-1])
        assert maximum < 1e-10
        ans[name+"_maximum_operator_residual_eigenvalue"] = maximum
    ans["scope"] = "Finite floating-point operator check, not an independent audit"
    return ans


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--quantum", action="store_true")
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    result = dict(operator_blocks=exact_local_operator_blocks(),
                  geometry=[check_geometry(m) for m in [2, 3, 4, 6]],
                  logical_route=logical_route(), countercontrols=countercontrols())
    if args.quantum:
        result["quantum"] = quantum_control()
        result["crossed_css"] = crossed_css_control()
    result["program_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    (OUT / "verification.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"geometry_states": [x["states"] for x in result["geometry"]],
                      "logical_path_coherent_writes": result["logical_route"]["minimal_coherent_writes"],
                      "quantum": args.quantum, "output": str(OUT / "verification.json")}))


if __name__ == "__main__":
    main()
