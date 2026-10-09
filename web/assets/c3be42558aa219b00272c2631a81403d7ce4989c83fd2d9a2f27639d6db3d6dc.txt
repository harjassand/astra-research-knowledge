"""Finite matrix diagnostics for section 9's flagged centralization.

This does not solve the low-energy to EB remainder or optimize any channel.
"""
from pathlib import Path
import json
import numpy as np

SEED = 707291
rng = np.random.default_rng(SEED)

def herm(a):
    return (a + a.conj().T) / 2

def power(a, exponent):
    vals, vecs = np.linalg.eigh(herm(a))
    vals = np.maximum(vals, 0.0)
    return (vecs * vals**exponent) @ vecs.conj().T

def trnorm(a):
    return float(np.linalg.svd(a, compute_uv=False).sum())

def apply_filter(z, a, sigmap, mask):
    return (a[:, None] * z * a[None, :]) * mask + np.trace(
        (1 - a*a)[:, None] * z) * sigmap

records = []
max_residuals = dict(canonical_identity=0., canonical_norm_excess=0.,
                     canonical_skew_bound_violation=0.,
                     averaged_pinching_violation=0.,
                     averaged_linear_pinching_violation=0.,
                     flatten_order_violation=0., filter_contraction_violation=0.,
                     filter_reference_error=0., filter_trace_error=0.,
                     filter_cp_negative_eigenvalue=0.,
                     central_commutator=0., sandwich_violation=0.,
                     recovery_bound_violation=0., probability_sum_error=0.)
for d in range(2, 12):
    for fixture in range(30):
        spread = [0., 2., 6., 12.][fixture % 4]
        weights = np.exp(rng.uniform(-spread, 0., d))
        weights /= weights.sum()
        s = np.sqrt(weights)
        sigma = np.diag(weights)
        sr = np.diag(s)
        z = rng.normal(size=(d,d)) + 1j*rng.normal(size=(d,d))
        h = herm(z)
        quantum_strength = [0., 1.e-7, 1.e-3, 1.][fixture % 4]
        h = np.diag(h.diagonal()) + quantum_strength * (
            h - np.diag(h.diagonal()))
        h -= np.trace(sigma @ h).real * np.eye(d)
        theta = [.1, .5, .9][fixture % 3]
        h *= theta / max(np.linalg.norm(h, 2), 1.e-15)
        rho = sr @ (np.eye(d) + h) @ sr
        x = power(sr @ rho @ sr, .5) / s[:,None] / s[None,:]
        m = np.sqrt(1 + theta)
        xi = float(np.linalg.norm(x @ sr - sr @ x))
        q = power(rho, .5)
        delta = max(0., trnorm(sr @ q) - np.trace(sr @ q).real)
        t = [.07, .2, .8][(fixture // 3) % 3]
        logs = np.log(s)
        points = sorted(set([0., t] + [float(v % t) for v in logs]))
        # Ignore intervals of zero floating-point length; boundary values have
        # measure zero. All interval weights and normalized filters are explicit.
        intervals = [(lo,hi) for lo,hi in zip(points[:-1],points[1:])
                     if hi > lo]
        averaged_sq = 0.
        averaged_pinching = 0.
        decoded = np.zeros_like(rho, dtype=complex)
        probs = []
        cmax = {key: 0. for key in max_residuals}
        cmax['canonical_identity'] = trnorm(x @ sigma @ x - rho)
        cmax['canonical_norm_excess'] = max(0.,np.linalg.norm(x,2)-m)
        cmax['canonical_skew_bound_violation'] = max(0.,xi-2*np.sqrt(2*m*delta))
        for lo, hi in intervals:
            u = (lo + hi) / 2
            p = (hi - lo) / t
            probs.append(p)
            bins = np.floor((logs - u) / t).astype(int)
            mask = bins[:,None] == bins[None,:]
            flat = np.exp(u + bins*t)
            flat /= np.linalg.norm(flat)
            sp = flat*flat
            sigmap = np.diag(sp)
            a = np.exp(-t) * flat / s
            y = x * mask
            defect = np.linalg.norm((x-y) @ sr)
            averaged_sq += p * defect**2
            pinched = rho * mask
            averaged_pinching += p * trnorm(pinched-rho)
            out = apply_filter(rho,a,sigmap,mask)
            decoded += p*out
            cmax['flatten_order_violation'] = max(
                cmax['flatten_order_violation'],
                float(np.maximum(np.exp(-2*t)*weights-sp,0.).max()),
                float(np.maximum(sp-np.exp(2*t)*weights,0.).max()))
            cmax['filter_contraction_violation'] = max(
                cmax['filter_contraction_violation'],
                float(np.maximum(a-1.,0.).max()),
                float(np.maximum(np.exp(-2*t)-a,0.).max()))
            cmax['filter_reference_error'] = max(
                cmax['filter_reference_error'],
                trnorm(apply_filter(sigma,a,sigmap,mask)-sigmap))
            cmax['filter_trace_error'] = max(cmax['filter_trace_error'],
                                            abs(np.trace(out)-1.))
            cmax['central_commutator'] = max(cmax['central_commutator'],
                                            float(np.linalg.norm(out@sigmap-sigmap@out)))
            cmax['sandwich_violation'] = max(cmax['sandwich_violation'],
                max(0.,-float(np.linalg.eigvalsh(herm(out-(1-theta)*sigmap)).min())),
                max(0.,-float(np.linalg.eigvalsh(herm((1+theta)*sigmap-out)).min())))
            if d <= 4 and fixture < 6:
                choi = np.zeros((d*d,d*d),complex)
                for i in range(d):
                    for j in range(d):
                        e = np.zeros((d,d),complex)
                        e[i,j] = 1.
                        choi[i*d:(i+1)*d,j*d:(j+1)*d] = apply_filter(e,a,sigmap,mask)
                cmax['filter_cp_negative_eigenvalue'] = max(
                    cmax['filter_cp_negative_eigenvalue'],
                    max(0.,-float(np.linalg.eigvalsh(herm(choi)).min())))
        cmax['averaged_pinching_violation'] = max(0.,averaged_sq-3*m*xi/t)
        cmax['averaged_linear_pinching_violation'] = max(
            0.,averaged_pinching-4*np.sqrt(3*m*xi/t))
        recovery = trnorm(decoded-rho)
        bound = 4*np.sqrt(3*m*xi/t)+8*t
        cmax['recovery_bound_violation'] = max(0.,recovery-bound)
        cmax['probability_sum_error'] = abs(sum(probs)-1.)
        for key,value in cmax.items():
            max_residuals[key] = max(max_residuals[key],float(value))
        records.append(dict(d=d,fixture=fixture,spread=spread,theta=theta,
                            quantum_strength=quantum_strength,t=t,xi=xi,
                            reference_pair_gap=delta,flag_count=len(intervals),
                            averaged_pinching_squared=averaged_sq,
                            recovery_full_trace_error=recovery,recovery_bound=bound))

result = dict(seed=SEED,fixture_count=len(records),max_residuals=max_residuals,
              tolerance=3e-7,all_checks_pass=all(v<3e-7 for v in max_residuals.values()),
              limitations=['No EB or broadcaster optimization.',
                           'No growing-family conclusion from finite fixtures.',
                           'Exact formula uses reference diagonalization; finite precision stability is not established.'],
              fixtures=records)
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='fixtures'},indent=2))
