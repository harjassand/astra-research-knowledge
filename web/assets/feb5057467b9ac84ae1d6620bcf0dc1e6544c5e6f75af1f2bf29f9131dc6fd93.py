#!/usr/bin/env python3
"""Small exact Fock-space diagnostics for the d-D spinless-fermion proof.

Only NumPy is required.  These fixtures check conventions and inequalities;
they are not a proof of the all-L theorem or a d-D spin/JW implementation.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np


def box_sites(L: int, d: int):
    side = L - 1
    return [tuple(x) for x in np.ndindex(*(side,) * d)]


def pairs_for(L: int, d: int, offsets):
    sites = box_sites(L, d)
    idx = {x: i for i, x in enumerate(sites)}
    pairs = set()
    for x in sites:
        for z in offsets:
            y = tuple(x[a] + z[a] for a in range(d))
            if y in idx and y != x:
                pairs.add(tuple(sorted((idx[x], idx[y]))))
    return sites, sorted(pairs)


def annihilation(n: int):
    dim = 1 << n
    cs = []
    for j in range(n):
        c = np.zeros((dim, dim), dtype=np.complex128)
        lower = (1 << j) - 1
        for state in range(dim):
            if (state >> j) & 1:
                target = state ^ (1 << j)
                sign = -1 if (state & lower).bit_count() % 2 else 1
                c[target, state] = sign
        cs.append(c)
    return cs


def fock_ops(L: int, d: int, J: float, lam: float, tau: float, offsets):
    sites, pairs = pairs_for(L, d, offsets)
    nsite = len(sites)
    idx = {x: i for i, x in enumerate(sites)}
    h = np.zeros((nsite, nsite), dtype=float)
    np.fill_diagonal(h, 4.0 * J * d)
    for i, x in enumerate(sites):
        for a in range(d):
            y = list(x)
            y[a] += 1
            y = tuple(y)
            if y in idx:
                j = idx[y]
                h[i, j] = h[j, i] = -2.0 * J
    cs = annihilation(nsite)
    cd = [c.conj().T for c in cs]
    dim = 1 << nsite
    K = np.zeros((dim, dim), dtype=np.complex128)
    for i in range(nsite):
        for j in range(nsite):
            if h[i, j] != 0.0:
                K += h[i, j] * (cd[i] @ cs[j])
    M = sum((cd[i] @ cs[i] for i in range(nsite)),
            start=np.zeros_like(K))
    H0 = K - lam / (L * L) * M
    occupations = np.array([[(s >> i) & 1 for i in range(nsite)]
                            for s in range(dim)], dtype=int)
    bad = np.zeros(dim, dtype=bool)
    for u, v in pairs:
        bad |= (occupations[:, u] * occupations[:, v]).astype(bool)
    return sites, pairs, h, K, M, H0, occupations, bad


def gibbs(H, beta):
    e, U = np.linalg.eigh(H)
    w = np.exp(-beta * (e - float(e.min())))
    Zscaled = float(w.sum())
    rho = (U * (w / Zscaled)) @ U.conj().T
    logZ = math.log(Zscaled) - beta * float(e.min())
    return rho, logZ, e, U, w / Zscaled


def trace_norm(A):
    return float(np.abs(np.linalg.eigvalsh((A + A.conj().T) / 2)).sum())


def entropy(rho):
    vals = np.linalg.eigvalsh((rho + rho.conj().T) / 2)
    vals = vals[vals > 1e-14]
    return float(-np.dot(vals, np.log(vals)))


def gaussian_constants(d, J, tau, B, cutoff=100):
    alpha = 8 * tau * J
    xs = np.arange(1, cutoff + 1, dtype=float)
    z0 = float(np.exp(-alpha * xs * xs).sum())
    z2 = float((xs * xs * np.exp(-alpha * xs * xs)).sum())
    c0 = math.exp(tau * B) * z0**d
    c2 = math.exp(tau * B) * d * z2 * z0 ** (d - 1)
    return c0, c2


def direct_sine_data(L, d, J, lam, tau):
    sites = box_sites(L, d)
    ks = list(np.ndindex(*(L - 1,) * d))
    ks = [tuple(v + 1 for v in k) for k in ks]
    phi = np.empty((len(sites), len(ks)), dtype=float)
    eps = []
    for a, x in enumerate(sites):
        x1 = tuple(v + 1 for v in x)
        for b, k in enumerate(ks):
            phi[a, b] = (2.0 / L) ** (d / 2) * np.prod(
                [math.sin(math.pi * k[q] * x1[q] / L) for q in range(d)])
    for k in ks:
        eps.append(4 * J * sum(1 - math.cos(math.pi * k[q] / L)
                               for q in range(d)))
    eps = np.asarray(eps)
    f = 1.0 / (1.0 + np.exp(tau * (L * L * eps - lam)))
    C = (phi * f) @ phi.T
    return phi, np.asarray(ks, dtype=float), eps, f, C


def h2(p):
    if p <= 0.0 or p >= 1.0:
        return 0.0
    return -p * math.log(p) - (1.0 - p) * math.log(1.0 - p)


def one_fixture(L, d, label):
    J, tau, B, lam = 1.0, 0.2, 0.1, 0.05
    offsets = [tuple(1 if j == a else 0 for j in range(d)) for a in range(d)]
    sites, pairs, h, K, M, H0, occ, bad = fock_ops(L, d, J, lam, tau, offsets)
    beta = tau * L * L
    rho0, logZ0, _, _, _ = gibbs(H0, beta)
    dim = len(rho0)
    Qdiag = bad.astype(float)
    Pdiag = 1.0 - Qdiag
    delta = float(np.real(np.diag(rho0) @ Qdiag))
    mdiag = occ.sum(axis=1).astype(float)
    qM = float(np.real(np.diag(rho0) @ (Qdiag * mdiag)))

    phi, ks, eps, f, C = direct_sine_data(L, d, J, lam, tau)
    c0, c2 = gaussian_constants(d, J, tau, B)
    S = len(sites)
    h_spectrum_error = float(np.max(np.abs(np.sort(np.linalg.eigvalsh(h)) - np.sort(eps))))
    assert h_spectrum_error < 1e-12
    m0 = float(np.real(np.trace(rho0 @ M)))
    assert abs(m0 - float(f.sum())) < 2e-12 * max(1.0, m0)
    sum_pair = 0.0
    sum_pair_fock = 0.0
    qM_pair = 0.0
    qM_pair_fock = 0.0
    wedge_max_ratio = 0.0
    for u, v in pairs:
        # Cauchy-Binet expansions avoid catastrophic cancellation in det(C)
        # for this very dilute, low-temperature fixture.
        pairdet = 0.0
        for k in range(len(ks)):
            for l in range(k + 1, len(ks)):
                wedge = phi[u, k] * phi[v, l] - phi[u, l] * phi[v, k]
                pairdet += f[k] * f[l] * wedge * wedge
        sum_pair += pairdet
        sum_pair_fock += float(np.real(np.diag(rho0) @ (occ[:, u] * occ[:, v])))
        # Wick/Cauchy-Binet sum over all triples; repeated x/y terms separately.
        weighted = 2.0 * pairdet
        for z in range(S):
            if z in (u, v):
                continue
            triple = 0.0
            for k in range(len(ks)):
                for l in range(k + 1, len(ks)):
                    for m in range(l + 1, len(ks)):
                        minor = np.linalg.det(phi[[u, v, z]][:, [k, l, m]])
                        triple += f[k] * f[l] * f[m] * minor * minor
            weighted += triple
        qM_pair += weighted
        qM_pair_fock += float(np.real(np.diag(rho0) @
                                      (occ[:, u] * occ[:, v] * mdiag)))

    a = (2 * (4**d) * math.pi**2 * c0 * c2 * sum(
        sum(vv * vv for vv in z) for z in offsets)) / (L ** (d + 2))
    q_bound = (2 + c0) * a
    assert delta <= sum_pair + 1e-12 * max(delta, sum_pair, 1e-300)
    assert abs(sum_pair - sum_pair_fock) < 2e-12 * max(sum_pair_fock, 1e-300)
    assert sum_pair <= a + 1e-12 * max(a, 1e-300)
    assert qM <= qM_pair + 1e-12 * max(qM, qM_pair, 1e-300)
    assert abs(qM_pair - qM_pair_fock) < 2e-12 * max(qM_pair_fock, 1e-300)
    assert qM_pair <= q_bound + 1e-12 * max(q_bound, 1e-300)
    assert abs(float(np.trace(C)) - float(np.dot(f, np.ones_like(f)))) < 1e-10

    # Verify all sine orbitals and the displacement wedge bound.
    ortho_err = float(np.linalg.norm(phi.T @ phi - np.eye(phi.shape[1]), ord=2))
    wedge_viol = 0.0
    for u, v in pairs:
        # Convert site index to coordinates only for the tested oriented +axis pair.
        x = sites[u]
        y = sites[v]
        z = tuple(y[a0] - x[a0] for a0 in range(d))
        z2 = sum(t * t for t in z)
        for k in range(len(ks)):
            for l in range(k + 1, len(ks)):
                wedge = phi[u, k] * phi[v, l] - phi[u, l] * phi[v, k]
                rhs = ((4**d) * math.pi**2 * z2
                       * (np.linalg.norm(ks[k]) + np.linalg.norm(ks[l]))**2
                       / L**(2 * d + 2))
                wedge_viol = max(wedge_viol, wedge * wedge - rhs)
    assert ortho_err < 1e-12
    assert wedge_viol < 2e-12

    # Projected trial state and all entropy/energy inequalities.
    p = 1.0 - delta
    P = np.diag(Pdiag)
    sigma = P @ rho0 @ P / p
    S0, Ss = entropy(rho0), entropy(sigma)
    entgap_bound = h2(delta) + qM * math.log(S) + delta
    assert S0 - Ss <= entgap_bound + 2e-10
    eK = float(np.real(np.trace(rho0 @ K)))
    projectedK = float(np.real(np.trace(rho0 @ P @ K @ P)))
    assert projectedK <= eK + 8 * J * d * qM + 2e-10
    m_sig = float(np.real(np.trace(sigma @ M)))
    assert abs(m_sig - m0) <= (c0 * delta + qM) / p + 2e-10

    # Rank-one PSD W supported in Q, chosen with superposition across number sectors.
    rng = np.random.default_rng(4000 + 100 * d + L)
    # Keep fermion parity physical while allowing number-changing pair creation.
    qidx = np.flatnonzero(bad & ((mdiag.astype(int) % 2) == 0))
    assert len(set(mdiag[qidx].astype(int))) >= 2
    v = np.zeros(dim, dtype=np.complex128)
    zrand = rng.normal(size=len(qidx)) + 1j * rng.normal(size=len(qidx))
    v[qidx] = zrand / np.linalg.norm(zrand)
    strength = 1000.0
    W = strength * np.outer(v, v.conj())
    w_kernel_error = float(np.linalg.norm(W @ P, ord=2))
    assert w_kernel_error < 1e-9
    comm = W @ M - M @ W
    commnorm = float(np.linalg.norm(comm, ord=2))
    parity = np.diag((-1.0) ** mdiag)
    parity_commnorm = float(np.linalg.norm(W @ parity - parity @ W, ord=2))
    HW = H0 + W
    rhoW, logZW, _, _, _ = gibbs(HW, beta)
    observed = trace_norm(rhoW - rho0)
    G = (h2(a) + a + (2 + c0) * a * math.log(S)
         + tau * a * (2 * J * math.pi**2 * c2
                      + 8 * J * d * L * L * (2 + c0)
                      + B * (2 + 2 * c0))) / (1 - a) if a < 1 else float("inf")
    triangle_trace_bound = 2 * math.sqrt(a) + math.sqrt(2 * G) if a <= 0.5 else 2.0
    relative_entropy = -Ss + beta * float(np.real(np.trace(sigma @ H0))) + logZW
    relative_entropy_sigma_free = (-Ss + beta * float(np.real(np.trace(sigma @ H0)))
                                   + logZ0)
    pidx = np.flatnonzero(Pdiag > 0)
    _, logZP, _, _, _ = gibbs(H0[np.ix_(pidx, pidx)], beta)
    relative_entropy_interacting_free = (
        -beta * float(np.real(np.trace(rhoW @ W))) + logZ0 - logZW)
    relative_entropy_partition_squeeze = logZ0 - logZP
    direct_trace_bound = math.sqrt(2 * G) if G >= 0 else float("nan")
    theorem_bound = direct_trace_bound
    assert logZW <= logZ0 + 1e-10
    assert logZW >= logZP - 1e-10
    assert abs(float(np.real(np.trace(sigma @ W)))) < 1e-9
    assert relative_entropy <= G + 2e-10
    assert relative_entropy_sigma_free <= G + 2e-10
    assert relative_entropy_interacting_free <= relative_entropy_partition_squeeze + 2e-10
    assert relative_entropy_partition_squeeze <= relative_entropy_sigma_free + 2e-10
    assert relative_entropy_interacting_free <= G + 2e-10
    assert observed <= theorem_bound + 2e-10
    assert observed <= direct_trace_bound + 2e-10
    assert commnorm > 1e-7
    assert parity_commnorm < 1e-9
    # The EB fixed-number decoder exactly fixes rho0 (rho0 is gauge invariant).
    decoded = np.zeros_like(rho0)
    for m in range(S + 1):
        idxm = np.flatnonzero(mdiag == m)
        probm = float(np.real(np.diag(rho0)[idxm].sum()))
        if probm > 0:
            block = np.zeros_like(rho0)
            block[np.ix_(idxm, idxm)] = rho0[np.ix_(idxm, idxm)] / probm
            decoded += probm * block
    decoder_err = trace_norm(decoded - rho0)
    assert decoder_err < 2e-10

    # Two-copy collective total-number channel: its free conditional states
    # are independent of lambda, and the channel fixes rho0 tensor rho0. The
    # direct dense product diagnostic is restricted to the 16-state fixture.
    if dim <= 16:
        rho0_2 = np.kron(rho0, rho0)
        mtotal_diag = (mdiag[:, None] + mdiag[None, :]).reshape(-1)
        decoded_2 = np.zeros_like(rho0_2)
        for t in range(2 * S + 1):
            idxt = np.flatnonzero(mtotal_diag == t)
            probt = float(np.real(np.diag(rho0_2)[idxt].sum()))
            if probt > 0:
                block = np.zeros_like(rho0_2)
                block[np.ix_(idxt, idxt)] = rho0_2[np.ix_(idxt, idxt)] / probt
                decoded_2 += probt * block
        decoder_2_err = trace_norm(decoded_2 - rho0_2)
        product_trace = trace_norm(np.kron(rhoW, rhoW) - rho0_2)
        assert decoder_2_err < 2e-10
        assert product_trace <= math.sqrt(4 * G) + 2e-10
    else:
        decoder_2_err = None
        product_trace = None

    return {
        "label": label, "d": d, "L": L, "sites": S, "fock_dim": dim,
        "forbidden_pairs": len(pairs), "sine_orthogonality_spectral_error": ortho_err,
        "one_body_spectrum_error": h_spectrum_error,
        "wedge_bound_max_violation": wedge_viol,
        "mean_M_DPP": float(np.trace(C)), "mean_M_Fock": m0,
        "pair_union_mass_delta": delta, "union_bound_sum_pair_masses": sum_pair,
        "pair_sum_DPP_vs_Fock_abs_error": abs(sum_pair - sum_pair_fock),
        "weighted_bad_mass_qM": qM, "weighted_pair_sum_qM": qM_pair,
        "weighted_pair_sum_DPP_vs_Fock_abs_error": abs(qM_pair-qM_pair_fock),
        "a_bound": a, "qM_bound": q_bound, "entropy_gap": S0 - Ss,
        "entropy_gap_bound": entgap_bound, "projected_kinetic": projectedK,
        "kinetic_rhs": eK + 8 * J * d * qM, "number_change": m_sig - m0,
        "W_strength": strength, "W_kernel_error": w_kernel_error,
        "commutator_norm_W_M": commnorm,
        "commutator_norm_W_fermion_parity": parity_commnorm,
        "relative_entropy_sigma_rhoW": relative_entropy,
        "relative_entropy_sigma_rho0": relative_entropy_sigma_free,
        "relative_entropy_rhoW_rho0": relative_entropy_interacting_free,
        "log_partition_squeeze_Z0_over_ZP": relative_entropy_partition_squeeze,
        "log_partition_order_ZW_le_Z0": logZW <= logZ0 + 1e-10,
        "log_partition_order_ZW_ge_ZP": logZW >= logZP - 1e-10,
        "trace_norm_rhoW_minus_rho0": observed,
        "relative_entropy_bound_G": G, "trace_theorem_rhs": theorem_bound,
        "older_gentle_projection_trace_rhs": triangle_trace_bound,
        "direct_reverse_KL_trace_rhs": direct_trace_bound,
        "EB_free_fixed_point_trace_error": decoder_err,
        "two_copy_collective_total_number_decoder_error": decoder_2_err,
        "two_copy_interacting_free_trace_distance": product_trace,
        "two_copy_trace_bound_sqrt_4G": math.sqrt(4 * G),
        "finite_diagnostic_only": True,
    }


def main():
    rows = [one_fixture(3, 2, "2D 2x2 open box"),
            one_fixture(3, 3, "3D 2x2x2 open box")]
    output = {
        "status": "PASS",
        "scope": "two dense float64 small spinless-fermion Fock fixtures; not proof or d-D spin result",
        "fixtures": rows,
    }
    out = Path("outputs/research/spin_statistical/cycle2/d_dimensional_fermion/evidence")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "exact_fock_checks.json"
    path.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(path)
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
