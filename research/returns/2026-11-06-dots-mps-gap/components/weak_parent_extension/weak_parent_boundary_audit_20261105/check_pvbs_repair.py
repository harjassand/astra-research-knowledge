"""Independent finite-matrix audit of a weak-parent PVBS boundary repair.

Floating tests support the separate algebraic proof; they are not gap certificates.
No code from the proper-parent MPS implementation is imported.
"""
import os
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import json
import time
from pathlib import Path
import numpy as np
import scipy.linalg as la

OUT = Path(__file__).resolve().parent


def particle(L, lam):
    v = np.zeros(2**L, complex)
    for j in range(L):
        v[1 << (L - 1 - j)] = lam**j
    return v


def code(L, lam):
    p = particle(L, lam)
    z = np.zeros_like(p)
    z[0] = 1
    return np.column_stack((z, p / la.norm(p)))


def interaction(lam, B):
    e = np.array([0, 1, -lam, 0], complex) / np.sqrt(1 + lam**2)
    f = np.array([0, 0, 0, 1], complex)
    U = np.column_stack((e, f))
    return U @ B @ U.conj().T


def local_apply(Y, h, i, N):
    tail = Y.shape[1:]
    T = Y.reshape(*([2] * N), *tail)
    axes = [i, i + 1]
    order = axes + [j for j in range(T.ndim) if j not in axes]
    T = T.transpose(order)
    shape = T.shape
    T = (h @ T.reshape(4, -1)).reshape(shape)
    return T.transpose(np.argsort(order)).reshape(Y.shape)


def open_h(h, N):
    I = np.eye(2**N, dtype=complex)
    return sum(local_apply(I, h, i, N) for i in range(N-1))


def construct(L, lam):
    V = code(L, lam)
    VN = code(L+1, lam)
    W = code(2*L, lam)
    # Input order L-buffer, s, t, R-buffer. Output order t, R+L, s.
    # The entire old L-buffer is retained as Stinespring environment p.
    Y = np.einsum('psa,tqb,uq,ju->tjspab',
                  VN.reshape(2**L, 2, 2), VN.reshape(2, 2**L, 2),
                  V.conj().T, W, optimize=True)
    Y = Y.reshape(2**(2*L+2), 2**L, 4)
    nL = la.norm(particle(L, lam))
    nN = la.norm(particle(L+1, lam))
    n2 = la.norm(particle(2*L, lam))
    alpha = nL/nN
    beta = lam**L/nN
    z = np.zeros(2**(2*L+2), complex)
    z[0] = 1
    p = particle(2*L+2, lam)/nN
    Y0 = np.zeros_like(Y)
    for a in (0, 1):
        env = V[:, a] * (alpha if a else 1)
        for b in (0, 1):
            Y0[:, :, 2*a+b] = np.outer(p if b else z, env)
    delta2 = (lam**2 * (nL-n2)**2 + lam**(4*L+2))/nN**2
    exact_frobenius2 = 2*beta**2 + (1+alpha**2)*delta2
    return Y, Y0, exact_frobenius2


def buffer_kraus(L, lam):
    """Full-input Kraus family, with an actual nonzero reset branch."""
    V = code(L, lam)
    W = code(2*L, lam)
    bad = la.null_space(V.conj().T)
    right = [W @ V.conj().T]
    right += [np.outer(W[:, 0], bad[:, j].conj()) for j in range(bad.shape[1])]
    E = np.eye(2**L)
    return [np.kron(E[j:j+1], A) for j in range(2**L) for A in right]


def audit_case(lam, L, B, label):
    h = interaction(lam, B)
    M = la.norm(h, 2)
    Y, Y0, fbound = construct(L, lam)
    N = 2*L+2
    HY = local_apply(Y, h, 0, N) + local_apply(Y, h, N-2, N)
    H0 = local_apply(Y0, h, 0, N) + local_apply(Y0, h, N-2, N)
    A = Y.reshape(-1, 4)
    D = (Y-Y0).reshape(-1, 4)
    F = HY.reshape(-1, 4).conj().T @ HY.reshape(-1, 4)
    actual_frob = float(la.norm(D, 'fro')**2)
    distance = float(la.norm(D, 2))
    boundary = float(la.eigvalsh(F).max())
    ideal_resid = float(la.norm(H0.reshape(-1, 4), 2))
    isometry = float(la.norm(A.conj().T @ A-np.eye(4), 2))
    assert isometry < 1e-12
    assert ideal_resid < 1e-12
    assert abs(actual_frob-fbound) < 1e-12
    assert boundary <= 4*M*M*distance**2 + 1e-12
    return dict(lam=lam, buffer=L, interaction=label, M=float(M),
                actual_ideal_operator_distance=distance,
                actual_ideal_frobenius_squared=actual_frob,
                algebraic_frobenius_squared=fbound,
                compressed_boundary_square_norm=boundary,
                isometry_defect=isometry, ideal_seam_residual=ideal_resid,
                naive_vacuum_reset_square_lower_bound=(lam*lam/(1+lam*lam)) /
                    la.norm(particle(L+1, lam))**2 if label == 'PVBS projector' else None)


def main():
    t = time.perf_counter()
    B = np.array([[1.3, .24+.17j], [.24-.17j, .8]], complex)
    rows = []
    for lam in (.25, .7, .95):
        for L in (1, 2, 3, 4):
            for b, label in ((np.eye(2), 'PVBS projector'),
                             (B, 'complex kernel-equivalent positive interaction')):
                rows.append(audit_case(lam, L, b, label))
    spectra = []
    for lam in (.25, .7, .95, 1.4):
        for N in (2, 3, 4, 5, 6):
            h = interaction(lam, np.eye(2))
            H = open_h(h, N)
            e = la.eigvalsh(H)
            gap = float(e[e > 1e-10].min())
            formula = 1-2*lam/(1+lam*lam)*np.cos(np.pi/N)
            assert sum(abs(e)<1e-10) == 2
            assert abs(gap-formula) < 2e-12
            assert la.norm(H @ code(N, lam), 2) < 1e-12
            spectra.append(dict(lam=lam, length=N, kernel_dimension=2,
                                open_gap=gap, free_particle_formula=float(formula)))
    kraus_checks = []
    for lam in (.25, .7, .95):
        L=2
        K=buffer_kraus(L, lam)
        tp=la.norm(sum(A.conj().T @ A for A in K)-np.eye(2**(2*L)),2)
        H=open_h(interaction(lam, B), 2*L)
        joined=max(la.norm(H @ A, 2) for A in K)
        assert tp < 1e-12 and joined < 1e-12
        kraus_checks.append(dict(lam=lam, buffer=L, kraus_count=len(K),
                                 trace_preservation_defect=float(tp),
                                 joined_ground_residual=float(joined)))
    result=dict(description='Full good-subspace and full-input Kraus checks; floating sanity tests, not SDP certificates',
                cases=rows, open_spectra=spectra, full_input_kraus_checks=kraus_checks,
                elapsed_seconds=time.perf_counter()-t)
    (OUT/'pvbs_repair_results.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(cases=len(rows), open_spectra=len(spectra),
                         full_input_kraus_checks=len(kraus_checks),
                         max_isometry_defect=max(x['isometry_defect'] for x in rows),
                         max_ideal_residual=max(x['ideal_seam_residual'] for x in rows),
                         elapsed_seconds=result['elapsed_seconds']), indent=2))


if __name__ == '__main__':
    main()
