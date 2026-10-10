#!/usr/bin/env python3
"""One-port acquisition diagnostic; numpy only, no supplied hidden quantities.

Generation/evaluation may inspect truth. fit() receives only controls, scalar
noisy responses, alpha, n, dt, and common data-independent starts.
"""
import argparse
import itertools
import json
import math
import os
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent


def basis(n):
    mats = []
    for i in range(n):
        for j in range(i, n):
            m = np.zeros((n, n))
            m[i, j] = m[j, i] = 1 if i == j else 1 / np.sqrt(2)
            mats.append(m)
    return np.asarray(mats)


def encode(K, E):
    return np.einsum('pij,ij->p', E, K)


def decode(theta, E):
    return np.einsum('p,pij->ij', theta, E)


def simulate(K, controls, dt, alpha, mode='full', jac=False, substeps=1):
    r, steps = controls.shape
    n = K.shape[0]
    E = basis(n)
    p = len(E)
    # state axes: traces, linear/cubic blocks (full has one block), coordinates
    blocks = 2 if mode == 'cubic' else 1
    x = np.zeros((r, blocks, n))
    S = np.zeros((r, blocks, n, p)) if jac else None
    ys = np.empty((r, steps))
    Js = np.empty((r, steps, p)) if jac else None

    def rhs(v, W, u):
        vdot = -np.einsum('ij,rbj->rbi', K, v)
        if mode == 'cubic':
            vdot[:, 1] -= alpha * v[:, 0] ** 3
        else:
            vdot[:, 0] -= alpha * v[:, 0] ** 3
        vdot[:, 0, 0] += u
        if not jac:
            return vdot, None
        Wdot = -np.einsum('ij,rbjp->rbip', K, W)
        Wdot -= np.einsum('pij,rbj->rbip', E, v)
        if mode == 'cubic':
            Wdot[:, 1] -= 3 * alpha * v[:, 0, :, None] ** 2 * W[:, 0]
        else:
            Wdot[:, 0] -= 3 * alpha * v[:, 0, :, None] ** 2 * W[:, 0]
        return vdot, Wdot

    h = dt / substeps
    with np.errstate(over='ignore', invalid='ignore'):
        for t in range(steps):
            u = controls[:, t]
            for _ in range(substeps):
                k1, q1 = rhs(x, S, u)
                k2, q2 = rhs(x + h * k1 / 2, S + h * q1 / 2 if jac else None, u)
                k3, q3 = rhs(x + h * k2 / 2, S + h * q2 / 2 if jac else None, u)
                k4, q4 = rhs(x + h * k3, S + h * q3 if jac else None, u)
                x += h * (k1 + 2*k2 + 2*k3 + k4) / 6
                if jac:
                    S += h * (q1 + 2*q2 + 2*q3 + q4) / 6
            ys[:, t] = x[:, :, 0].sum(axis=1)
            if jac:
                Js[:, t] = S[:, :, 0].sum(axis=1)
            if not np.isfinite(x).all() or np.max(np.abs(x)) > 1e6:
                return None, None
    return ys, Js


def make_controls(seed, amplitude, traces=5, steps=240, dt=.05):
    rng = np.random.default_rng(seed)
    u = np.empty((traces, steps))
    t = np.arange(steps)*dt
    for r in range(traces):
        if r < traces - 2:
            lengths = [7, 13, 23][r % 3]
            signs = rng.choice([-1., -.5, .25, .7, 1.], math.ceil(steps/lengths))
            u[r] = np.repeat(signs, lengths)[:steps]
        else:
            phases = rng.uniform(0, 2*np.pi, 4)
            freqs = np.array([.07, .23, .61, 1.13])
            u[r] = np.sin(2*np.pi*freqs[:, None]*t + phases[:, None]).sum(axis=0)
            u[r] /= max(abs(u[r]))
    return amplitude * u


def random_spd(n, seed):
    rng = np.random.default_rng(seed)
    Q, _ = np.linalg.qr(rng.normal(size=(n, n)))
    return (Q * np.linspace(.65, 2.7, n)) @ Q.T


def starts(n, count, seed):
    rng = np.random.default_rng(seed)
    answer = []
    for _ in range(count):
        A = rng.normal(scale=.38, size=(n, n))
        K = 1.45*np.eye(n) + (A+A.T)/2
        low = np.linalg.eigvalsh(K)[0]
        if low < .35:
            K += (.35-low)*np.eye(n)
        answer.append(K)
    return answer


def fit(controls, yobs, dt, alpha, init_Ks, mode, maxiter=100):
    n = init_Ks[0].shape[0]
    E = basis(n)
    logs = []
    best = None
    total_simulations = 0
    start_time = time.perf_counter()
    for index, init_K in enumerate(init_Ks):
        theta = encode(init_K, E)
        damping = 1e-3
        evals = 0
        accepted = 0
        last_step = None
        for iteration in range(maxiter):
            K = decode(theta, E)
            pred, J = simulate(K, controls, dt, alpha, mode, jac=True)
            evals += 1
            if pred is None:
                break
            residual = (pred-yobs).reshape(-1)
            A = J.reshape(-1, len(E))
            cost = float(residual @ residual)
            H = A.T @ A
            g = A.T @ residual
            diagonal = np.maximum(np.diag(H), 1e-12)
            improved = False
            for trial in range(12):
                try:
                    step = np.linalg.solve(H + damping*np.diag(diagonal), -g)
                except np.linalg.LinAlgError:
                    damping *= 10
                    continue
                candidate = theta + step
                Ktry = decode(candidate, E)
                eig = np.linalg.eigvalsh(Ktry)
                # Common broad search range; evaluator truth is never supplied.
                if eig[0] < .05 or eig[-1] > 12:
                    damping *= 4
                    continue
                trial_y, _ = simulate(Ktry, controls, dt, alpha, mode)
                evals += 1
                if trial_y is None:
                    damping *= 4
                    continue
                trial_cost = float(np.sum((trial_y-yobs)**2))
                if trial_cost < cost:
                    theta = candidate
                    damping = max(damping/3, 1e-12)
                    accepted += 1
                    improved = True
                    last_step = float(np.linalg.norm(step))
                    break
                damping *= 4
            if not improved:
                break
            if np.linalg.norm(step) < 1e-9*(1+np.linalg.norm(theta)):
                break
        K = decode(theta, E)
        pred, _ = simulate(K, controls, dt, alpha, mode)
        evals += 1
        cost = float(np.sum((pred-yobs)**2)) if pred is not None else float('inf')
        record = dict(start=index, iterations=iteration+1, accepted=accepted,
                      evaluations=evals, cost=cost, last_step=last_step,
                      eigvals=np.linalg.eigvalsh(K).tolist(), K=K.tolist())
        logs.append(record)
        total_simulations += evals
        if best is None or cost < best['cost']:
            best = record
    return np.asarray(best['K']), dict(mode=mode, runtime_s=time.perf_counter()-start_time,
              total_simulations=total_simulations, starts=logs,
              best_start=best['start'], best_cost=best['cost'])


def gauge_error(A, B):
    n = len(A)
    best = float('inf')
    for perm in itertools.permutations(range(1, n)):
        ix = [0]+list(perm)
        C = B[np.ix_(ix, ix)]
        for signs in itertools.product([-1, 1], repeat=n-1):
            d = np.array([1]+list(signs))
            best = min(best, np.linalg.norm(A-C*d[:, None]*d[None, :]))
    return float(best/np.linalg.norm(A))


def validate_sensitivities():
    K = np.array([[1.8,-.65,.42],[-.65,1.25,.27],[.42,.27,1.7]])
    E = basis(3)
    rng = np.random.default_rng(782)
    direction = rng.normal(size=len(E))
    direction /= np.linalg.norm(direction)
    dK = decode(direction, E)
    u = make_controls(113, .8, traces=3, steps=70)
    answer = {}
    for mode in ['full', 'cubic']:
        y, J = simulate(K, u, .05, .3, mode, jac=True)
        plus, _ = simulate(K+1e-5*dK, u, .05, .3, mode)
        minus, _ = simulate(K-1e-5*dK, u, .05, .3, mode)
        finite_difference = (plus-minus)/2e-5
        exact = J @ direction
        error = np.linalg.norm(finite_difference-exact)/np.linalg.norm(exact)
        answer[mode] = float(error)
        if error > 1e-7:
            raise RuntimeError('sensitivity implementation failed finite difference check')
    return answer


def weak_sweep():
    alpha, dt, sigma = .3, .025, 1e-4
    u = make_controls(987, 2.5, traces=5, steps=480, dt=dt)
    all_rows = []
    for n in [3, 5]:
        B = random_spd(n-1, 817+n)
        b = np.linspace(.25, .55, n-1)
        b /= max(1., np.linalg.norm(b))
        Q, _ = np.linalg.qr(np.random.default_rng(218+n).normal(size=(n-1,n-1)))
        R = np.eye(n)
        R[1:, 1:] = Q
        rows = []
        for eps in [1., .6, .35, .2, .1, .05, .025, .0125]:
            K = np.zeros((n, n))
            K[0, 0] = 1.7
            K[1:, 1:] = B
            K[0, 1:] = K[1:, 0] = eps*b
            K2 = R.T @ K @ R
            y, _ = simulate(K, u, dt, alpha, substeps=2)
            y2, _ = simulate(K2, u, dt, alpha, substeps=2)
            rms = float(np.sqrt(np.mean((y-y2)**2)))
            maximum = float(np.max(np.abs(y-y2)))
            # Gaussian KL per scalar, true numerical difference.
            per_sample_KL = rms*rms/(2*sigma*sigma)
            _, J = simulate(K, u, dt, alpha, jac=True)
            sv = np.linalg.svd(J.reshape(-1, n*(n+1)//2), compute_uv=False)
            rows.append(dict(n=n, eps=eps, output_rms_contrast=rms,
                output_max_contrast=maximum, quotient_K_separation=gauge_error(K,K2),
                minimum_eigenvalue=float(np.linalg.eigvalsh(K)[0]),
                empirical_KL_per_scalar_at_sigma_1e4=per_sample_KL,
                scalar_samples_for_KL_half_at_same_rms=float(.5/per_sample_KL),
                jacobian_smin=float(sv[-1]), jacobian_condition=float(sv[0]/sv[-1])))
        slope = float(np.polyfit(np.log([x['eps'] for x in rows[-5:]]),
                    np.log([x['output_rms_contrast'] for x in rows[-5:]]), 1)[0])
        all_rows.append(dict(n=n, weak_limit_log_slope=slope, rows=rows))
    return dict(alpha=alpha, dt=dt, samples_per_pair=int(u.size),
                duration_per_trace=float(dt*u.shape[1]), traces=u.shape[0],
                input_max=float(np.max(abs(u))), energy=float(dt*np.sum(u*u)),
                results=all_rows)


def run_cases(maxiter=100, counts=(6, 8)):
    alpha, dt, sigma = .3, .05, 1e-5
    records = []
    for n, amplitude in [(3,.35),(3,.9),(3,2.5),(5,2.5)]:
        K = np.array([[1.8,-.65,.42],[-.65,1.25,.27],[.42,.27,1.7]]) if n == 3 else random_spd(5, 316)
        controls = make_controls(714, amplitude)
        validation = make_controls(1254, amplitude, traces=2)
        ytrue, _ = simulate(K, controls, dt, alpha, substeps=2)
        holdout, _ = simulate(K, validation, dt, alpha, substeps=2)
        noise = np.random.default_rng(436).normal(scale=sigma, size=ytrue.shape)
        yobs = ytrue+noise
        init_Ks = starts(n, counts[0 if n == 3 else 1], seed=198+n)
        linear, _ = simulate(K, controls, dt, 0.)
        cubic, _ = simulate(K, controls, dt, alpha, mode='cubic')
        coarse, J = simulate(K, controls, dt, alpha, jac=True)
        sv = np.linalg.svd(J.reshape(-1,len(basis(n))), compute_uv=False)
        case = dict(n=n, amplitude=amplitude, alpha=alpha, sigma=sigma, dt=dt,
            traces=int(controls.shape[0]), samples=int(controls.size),
            duration_per_trace=float(dt*controls.shape[1]),
            total_experiment_duration_excluding_resets=float(dt*controls.size),
            input_energy=float(dt*np.sum(controls*controls)),
            evaluator_truth_K=K.tolist(),
            linear_model_error_at_truth=float(np.sqrt(np.mean((linear-ytrue)**2))),
            cubic_model_error_at_truth=float(np.sqrt(np.mean((cubic-ytrue)**2))),
            integration_bias=float(np.sqrt(np.mean((coarse-ytrue)**2))),
            sensitivity_singular_values=sv.tolist(),
            jacobian_condition=float(sv[0]/sv[-1]),
            local_worst_1sigma_parameter_error=float(sigma/sv[-1]),
            estimators=[])
        for mode in ['full', 'cubic']:
            est, stats = fit(controls,yobs,dt,alpha,init_Ks,mode,maxiter=maxiter)
            est_y,_ = simulate(est, controls, dt, alpha, substeps=2)
            est_holdout,_ = simulate(est, validation, dt, alpha, substeps=2)
            stats.update(quotient_K_relative_error=gauge_error(K,est),
                estimated_K=est.tolist(),
                physical_train_prediction_rmse=float(np.sqrt(np.mean((est_y-ytrue)**2))),
                physical_holdout_prediction_rmse=float(np.sqrt(np.mean((est_holdout-holdout)**2))))
            case['estimators'].append(stats)
            print(json.dumps(dict(n=n,amp=amplitude,mode=mode,
                 quotient_K_relative_error=stats['quotient_K_relative_error'],
                 holdout_rmse=stats['physical_holdout_prediction_rmse'],
                 runtime_s=stats['runtime_s'],evals=stats['total_simulations'])),flush=True)
        records.append(case)
        # Save each completed case so interruption preserves evidence.
        (ROOT/'partial_recovery.json').write_text(json.dumps(records,indent=2)+'\n')
        tag=f'n{n}_a{amplitude}'
        np.savez_compressed(ROOT/f'data_{tag}.npz',controls=controls,observed=yobs,
            validation_controls=validation,alpha=alpha,dt=dt,sigma=sigma)
    return records


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--mode',choices=['all','weak','fit','check'],default='all')
    parser.add_argument('--maxiter',type=int,default=100)
    parser.add_argument('--starts3',type=int,default=6)
    parser.add_argument('--starts5',type=int,default=8)
    args=parser.parse_args()
    result=dict(platform=os.uname().sysname, numpy_version=np.__version__)
    start=time.perf_counter()
    result['sensitivity_check']=validate_sensitivities()
    if args.mode in ['weak','all']:
        result['weak_coupling']=weak_sweep()
        (ROOT/'weak_coupling.json').write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps(result['weak_coupling'],indent=2),flush=True)
    if args.mode in ['fit','all']:
        result['recovery']=run_cases(args.maxiter,(args.starts3,args.starts5))
    result['total_runtime_s']=time.perf_counter()-start
    (ROOT/f'results_{args.mode}.json').write_text(json.dumps(result,indent=2)+'\n')
    print('Completed in',result['total_runtime_s'],'seconds',flush=True)


if __name__ == '__main__':
    main()
