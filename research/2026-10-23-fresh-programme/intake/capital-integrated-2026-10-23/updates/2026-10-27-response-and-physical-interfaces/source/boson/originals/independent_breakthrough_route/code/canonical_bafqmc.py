#!/usr/bin/env python3
"""Balanced canonical BAFQMC for a number-conserving conjugate-flavor model.

Scientific replay, not a production QMC implementation. NumPy only. The exact
canonical and exact finite-step Trotter references use a separate Fock basis.
"""
from __future__ import annotations

import argparse
import json
import math
import time
from pathlib import Path

import numpy as np


def occupations(n: int, m: int):
    if m == 1:
        yield (n,)
        return
    for k in range(n + 1):
        for rest in occupations(n-k, m-1):
            yield (k,) + rest


def fock_one_body(a: np.ndarray, n: int):
    m = len(a)
    basis = list(occupations(n, m))
    index = {v: i for i, v in enumerate(basis)}
    result = np.zeros((len(basis), len(basis)), dtype=complex)
    for column, occ in enumerate(basis):
        for i in range(m):
            result[column, column] += a[i, i] * occ[i]
            for j in range(m):
                if i == j or not occ[j] or not a[i, j]:
                    continue
                new = list(occ)
                new[i] += 1
                new[j] -= 1
                result[index[tuple(new)], column] += (
                    a[i, j] * math.sqrt((occ[i]+1)*occ[j])
                )
    return result, np.asarray(basis, dtype=int)


def hermitian_exp(a: np.ndarray, coefficient: float):
    vals, vecs = np.linalg.eigh(a)
    return (vecs * np.exp(coefficient*vals)) @ vecs.conj().T


def model_matrices(m: int, n: int, u1: float, u2: float, t: float=1.):
    if m != 3:
        raise ValueError("Exact reference is the three-site frustrated triangle.")
    k = t * (np.ones((m, m)) - np.eye(m))
    # This is the real part of the K=(+/- 2 pi/3) structure factor.
    phase = 2*np.pi*np.arange(m)/m
    sf = np.cos(phase[:, None] - phase[None, :]) / m**2
    kf, occ = fock_one_body(k, n)
    sff, _ = fock_one_body(sf, n)
    dim = len(occ)
    ident = np.eye(dim)
    ktot = np.kron(kf, ident) + np.kron(ident, kf)
    sftot = np.kron(sff, ident) + np.kron(ident, sff)
    nb = np.repeat(occ, dim, axis=0)
    nc = np.tile(occ, (dim, 1))
    v1 = np.sum((nb-nc)**2, axis=1)
    v2 = np.sum((nb+nc)**2, axis=1)
    v = u1*v1 + u2*v2
    h = ktot + np.diag(v)
    return k, sf, ktot, sftot, v, h, v1, v2


def exact_reference(n: int, beta: float, u1: float, u2: float, steps: int):
    k, sf, ktot, sftot, v, h, v1, v2 = model_matrices(3, n, u1, u2)
    e, q = np.linalg.eigh(h)
    weights = np.exp(-beta*e)
    z = float(weights.sum())
    rho_diagonal = np.sum(np.abs(q)**2*weights[None, :], axis=1)/z
    exact = {
        "partition": z,
        "energy": float(np.dot(weights, e)/z),
        "kinetic": float(np.dot(weights, np.diag(q.conj().T@ktot@q).real)/z),
        "sf": float(np.dot(weights, np.diag(q.conj().T@sftot@q).real)/z),
        "relative_density_square": float(np.dot(rho_diagonal, v1)),
        "total_density_square": float(np.dot(rho_diagonal, v2)),
        "fock_dimension": len(h),
        "ground_energy": float(e[0]),
    }
    dt = beta/steps
    kh = hermitian_exp(ktot, -dt/2)
    dkh = -ktot@kh/(2*steps)
    vd = np.exp(-dt*v)
    dvd = -v*vd/steps
    transfer = (kh*vd[None, :])@kh
    dtransfer = ((dkh*vd[None, :])@kh +
                 (kh*dvd[None, :])@kh + (kh*vd[None, :])@dkh)
    lam, vec = np.linalg.eigh(transfer)
    dl = np.diag(vec.conj().T@dtransfer@vec).real
    terms = lam**steps
    zdt = float(terms.sum())
    edt = float(-steps*np.dot(lam**(steps-1), dl)/zdt)
    return exact, {"partition": zdt, "energy": edt, "steps": steps,
                   "delta_tau": dt}


def homogeneous_with_derivatives(b: np.ndarray, db: np.ndarray, n: int,
                                 operators: list[np.ndarray]):
    """Newton recursion on traces, valid for defective/nonnormal B as well.

    Returns h_n, beta derivative, and one-body insertion numerators. It uses
    no eigenvector decomposition or assumption of positive eigenvalues.
    """
    batch, m, _ = b.shape
    powers = [np.broadcast_to(np.eye(m, dtype=complex), b.shape)]
    traces = [np.full(batch, m, dtype=complex)]
    dtraces = [np.zeros(batch, dtype=complex)]
    for j in range(1, n+1):
        previous = powers[-1]
        current = previous@b
        powers.append(current)
        traces.append(np.trace(current, axis1=-2, axis2=-1))
        dtraces.append(j*np.einsum("bij,bji->b", previous, db))
    hs = [np.ones(batch, dtype=complex)]
    dhs = [np.zeros(batch, dtype=complex)]
    for r in range(1, n+1):
        hs.append(sum(traces[j]*hs[r-j] for j in range(1, r+1))/r)
        dhs.append(sum(dtraces[j]*hs[r-j]+traces[j]*dhs[r-j]
                       for j in range(1, r+1))/r)
    inserts = []
    for op in operators:
        inserts.append(sum(hs[n-j]*np.einsum("ij,bji->b", op, powers[j])
                           for j in range(1, n+1)))
    return hs[n], dhs[n], inserts


def field_evaluate(fields: np.ndarray, *, n: int, beta: float,
                   u1: float, u2: float, k: np.ndarray, sf: np.ndarray,
                   remove_uniform: bool=True):
    """Returns weight and unnormalized energy/one-body numerators.

    fields has shape (batch, steps, 2, modes), with independent N(0,1)
    entries. Channel 0 is relative density; channel 1 is total density.
    The spatial uniform modes can be integrated exactly at fixed populations.
    """
    batch, steps, channels, m = fields.shape
    assert channels == 2 and u1 >= 0 and u2 <= 0
    if remove_uniform:
        fields = fields - fields.mean(axis=-1, keepdims=True)
    dt = beta/steps
    a1 = math.sqrt(2*dt*u1)
    a2 = math.sqrt(-2*dt*u2)
    vals, vecs = np.linalg.eigh(k)
    a = (vecs*np.exp(-dt*vals/2))@vecs.conj().T
    da = -k@a/(2*steps)
    b = np.broadcast_to(np.eye(m, dtype=complex), (batch, m, m)).copy()
    db = np.zeros_like(b)
    for ell in range(steps):
        exponent = a2*fields[:, ell, 1, :] + 1j*a1*fields[:, ell, 0, :]
        d = np.exp(exponent)
        dd = d*exponent/(2*beta)
        sliced = (a[None, :, :]*d[:, None, :])@a
        dsliced = ((da[None, :, :]*d[:, None, :])@a +
                   (a[None, :, :]*dd[:, None, :])@a +
                   (a[None, :, :]*d[:, None, :])@da)
        db = dsliced@b + sliced@db
        b = sliced@b
    h, dh, inserts = homogeneous_with_derivatives(b, db, n, [k, sf])
    w = np.abs(h)**2
    energy_num = -2*np.real(h.conj()*dh)
    uniform_energy = 4*u2*n*n/m if remove_uniform else 0.
    energy_num += uniform_energy*w
    kin_num = 2*np.real(h.conj()*inserts[0])
    sf_num = 2*np.real(h.conj()*inserts[1])
    log_prefactor = -beta*uniform_energy
    return np.stack([w, energy_num, kin_num, sf_num], axis=1), log_prefactor


def iid_run(*, n: int, beta: float, u1: float, u2: float, steps: int,
            samples: int, seed: int, batch: int=4096, remove_uniform: bool=True):
    start = time.perf_counter()
    k, sf, *_ = model_matrices(3, n, u1, u2)
    rng = np.random.default_rng(seed)
    sums = np.zeros(4)
    cross = np.zeros((4, 4))
    max_w = 0.
    log_prefactor = 0.
    nblocks = 32
    block_size = max(1, samples//nblocks)
    blocks = []
    block_sum = np.zeros(4)
    block_count = 0
    done = 0
    # The final batch is shortened at a block boundary; blocks are independent.
    while done < samples:
        count = min(batch, samples-done, block_size-block_count)
        fields = rng.standard_normal((count, steps, 2, 3))
        values, log_prefactor = field_evaluate(
            fields, n=n, beta=beta, u1=u1, u2=u2, k=k, sf=sf,
            remove_uniform=remove_uniform)
        sums += values.sum(axis=0)
        cross += values.T@values
        max_w = max(max_w, float(values[:, 0].max()))
        block_sum += values.sum(axis=0)
        block_count += count
        done += count
        if block_count == block_size or done == samples:
            blocks.append((block_sum/block_count).tolist())
            block_sum[:] = 0
            block_count = 0
    means = sums/samples
    cov = (cross-samples*np.outer(means, means))/(samples-1)
    w = means[0]
    obs = means[1:]/w
    errs = []
    for j, o in enumerate(obs, 1):
        variance = max(0., cov[j, j]-2*o*cov[0, j]+o*o*cov[0, 0])
        errs.append(math.sqrt(variance/samples)/w)
    prefactor = math.exp(log_prefactor)
    return {
        "method": "independent Gaussian importance integration",
        "n_per_flavor": n, "sites": 3, "beta": beta, "t": 1.,
        "u1": u1, "u2": u2, "steps": steps,
        "samples": samples, "seed": seed,
        "uniform_fields_integrated": remove_uniform,
        "partition": prefactor*w,
        "partition_stderr": prefactor*math.sqrt(cov[0, 0]/samples),
        "energy": float(obs[0]), "energy_stderr": errs[0],
        "kinetic": float(obs[1]), "kinetic_stderr": errs[1],
        "sf": float(obs[2]), "sf_stderr": errs[2],
        "weight_cv_squared": max(0., float(cov[0, 0]/w**2)),
        "weight_ess_diagnostic": float(sums[0]**2/cross[0, 0]),
        "largest_weight": max_w,
        "independent_blocks": blocks,
        "autocorrelation": "IID Gaussian proposals; no Markov chain",
        "seconds": time.perf_counter()-start,
    }


def exact_checks():
    # A negative total-number coefficient, despite positive GC weights.
    b = 1j
    total_two = b*b + b*b.conjugate() + b.conjugate()**2
    assert total_two == -1+0j
    rng = np.random.default_rng(41731)
    max_trace_error = 0.
    max_derivative_error = 0.
    # Independent canonical evaluation by direct occupation monomials in the
    # eigenvalues, including an explicitly defective nonnormal matrix.
    cases = [np.array([[1., 8., 0.], [0., 1., 8.], [0., 0., 1.]])]
    cases += [rng.normal(size=(3, 3))+1j*rng.normal(size=(3, 3)) for _ in range(20)]
    for b in cases:
        db = rng.normal(size=(3, 3))+1j*rng.normal(size=(3, 3))
        h, dh, _ = homogeneous_with_derivatives(b[None], db[None], 4, [])
        ev = np.linalg.eigvals(b)
        independent = sum(np.prod(ev**np.asarray(o)) for o in occupations(4, 3))
        max_trace_error = max(max_trace_error, abs(h[0]-independent))
        eps = 1e-6
        hp, _, _ = homogeneous_with_derivatives((b+eps*db)[None], db[None], 4, [])
        hm, _, _ = homogeneous_with_derivatives((b-eps*db)[None], db[None], 4, [])
        max_derivative_error = max(max_derivative_error, abs(dh[0]-(hp[0]-hm[0])/(2*eps)))
    k, sf, *_ = model_matrices(3, 2, 1., -.05)
    fields = rng.standard_normal((7, 12, 2, 3))
    out, logpre = field_evaluate(fields, n=2, beta=1., u1=1., u2=-.05, k=k, sf=sf)
    plus, lp = field_evaluate(fields, n=2, beta=1.+1e-5, u1=1., u2=-.05, k=k, sf=sf)
    minus, lm = field_evaluate(fields, n=2, beta=1.-1e-5, u1=1., u2=-.05, k=k, sf=sf)
    analytic = out[:, 1]*math.exp(logpre)
    finite_difference = -(plus[:, 0]*math.exp(lp)-minus[:, 0]*math.exp(lm))/(2e-5)
    beta_error = float(np.max(np.abs(analytic-finite_difference)/np.maximum(1., np.abs(analytic))))
    assert max_trace_error < 1e-8
    assert max_derivative_error < 1e-3
    assert beta_error < 1e-7
    return {"total_N_two_counterexample_weight": total_two.real,
            "grand_canonical_weight_at_fugacity_half": 1/(1+.5**2),
            "balanced_one_one_weight": 1.,
            "max_h4_trace_error": float(max_trace_error),
            "max_h4_derivative_absolute_error": float(max_derivative_error),
            "max_pathwise_beta_derivative_relative_error": beta_error,
            "nonnormal_defective_test": "3x3 Jordan block with offdiagonal 8"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--samples", type=int, default=131072)
    parser.add_argument("--n", type=int, default=2)
    parser.add_argument("--beta", type=float, default=1.)
    parser.add_argument("--u1", type=float, default=1.)
    parser.add_argument("--u2", type=float, default=-.05)
    parser.add_argument("--steps", type=int, nargs="+", default=[10, 20, 40])
    parser.add_argument("--seed", type=int, default=20261027)
    parser.add_argument("--keep-uniform", action="store_true")
    args = parser.parse_args()
    result = {"checks": exact_checks(), "runs": []}
    for steps in args.steps:
        exact, trotter = exact_reference(args.n, args.beta, args.u1, args.u2, steps)
        result["exact_canonical"] = exact
        run = iid_run(n=args.n, beta=args.beta, u1=args.u1, u2=args.u2,
                      steps=steps, samples=args.samples, seed=args.seed+steps,
                      remove_uniform=not args.keep_uniform)
        run["exact_trotter"] = trotter
        run["energy_zscore_to_trotter"] = ((run["energy"]-trotter["energy"])/
                                              run["energy_stderr"])
        run["partition_zscore_to_trotter"] = ((run["partition"]-trotter["partition"])/
                                                 run["partition_stderr"])
        result["runs"].append(run)
        args.output.write_text(json.dumps(result, indent=2))
        print(json.dumps({k: v for k, v in run.items() if k != "independent_blocks"}), flush=True)


if __name__ == "__main__":
    main()
