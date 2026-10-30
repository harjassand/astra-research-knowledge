#!/usr/bin/env python3
"""Population verification; no acquired confidence or fitted LDP assertion."""
import hashlib
import json
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import minimize_scalar


def coefficients(g, h, b, r):
    c, s = np.cos(g*h), np.sin(g*h)
    M = np.array([[c, -s], [r*s, r*c]])
    d = np.array([s/g+b, r*(1-c)/g])
    ell = np.array([s/g+b*c, -(1-c)/g-b*s])
    d0 = (1-c)/g**2+b*s/g+b*b/2
    n = np.array([0., np.sqrt(1-r*r)])
    k = np.linalg.solve((np.eye(2)-M).T, ell)
    return M, d, ell, d0, n, k, d0+k@d


def nonlinear_train(kappa, g, r, seed):
    rng = np.random.default_rng(seed)
    N, h, b, cells = 7, .85, .25, 16
    M, d, ell, d0, n, k, mu = coefficients(g, h, b, r)
    X0 = np.arange(N, dtype=float)+rng.uniform(-.07, .07, N)/np.sqrt(kappa)
    V0, Y0 = rng.normal(size=N), rng.normal(size=N)
    incoming = rng.normal(size=(cells, N))
    histories = []
    max_identity = max_work = max_chainrule = 0.
    min_gap, max_gap = 2., 0.
    # Coupled numerical replay is not a claimed experimental copied future.
    for drive in (False, True):
        X, V, Y = X0.copy(), V0.copy(), Y0.copy()
        A = W = previous_A = 0.
        hist = []
        for j in range(cells):
            F = 0. if not drive or j < 2 else -.025*(previous_A-.15*j*(h+b))
            old_A, startX, startz = A, X.copy(), np.array([V.sum(), Y.sum()])

            def grad(x):
                nonlocal min_gap, max_gap
                gaps = np.roll(x, -1)-x
                gaps[-1] += N
                min_gap, max_gap = min(min_gap, float(gaps.min())), max(max_gap, float(gaps.max()))
                if np.any(gaps <= 0.) or np.any(gaps >= 2.):
                    raise RuntimeError('Numerical trajectory left finite-link domain')
                z = gaps-1.
                tension = kappa*z/(1-z*z)**2
                return np.roll(tension, 1)-tension

            def transport(_t, state):
                x, v, y = state[:N], state[N:2*N], state[2*N:3*N]
                return np.r_[v, -grad(x)-g*y+F, g*v,
                             F*v.sum(), np.sin(2*np.pi*x/N)@v]

            sol = solve_ivp(transport, (0, h), np.r_[X, V, Y, 0., 0.],
                            method='DOP853', rtol=3e-11, atol=2e-12)
            assert sol.success
            X, V, Y = np.split(sol.y[:3*N, -1], 3)
            actual_work, probe = sol.y[-2:, -1]

            def bath(_t, state):
                x, v = state[:N], state[N:2*N]
                return np.r_[v, -grad(x)+F, F*v.sum(), np.sin(2*np.pi*x/N)@v]

            sol = solve_ivp(bath, (0, b), np.r_[X, V, 0., 0.], method='DOP853',
                            rtol=3e-11, atol=2e-12)
            assert sol.success
            X, V = np.split(sol.y[:2*N, -1], 2)
            actual_work += sol.y[-2, -1]
            probe += sol.y[-1, -1]
            # Exact finite-frequency rotation, commuting with bath particle motion.
            Y = r*Y+np.sqrt(1-r*r)*incoming[j]
            endz, dA, source = np.array([V.sum(), Y.sum()]), (X-startX).sum(), incoming[j].sum()
            max_identity = max(max_identity,
                float(np.max(abs(endz-M@startz-N*d*F-n*source))),
                abs(dA-ell@startz-N*d0*F),
                abs(dA+k@(endz-startz)-N*mu*F-(k@n)*source))
            max_work = max(max_work, abs(actual_work-F*dA))
            primitive = lambda x: -N*np.cos(2*np.pi*x/N)/(2*np.pi)
            max_chainrule = max(max_chainrule, abs(probe-(primitive(X)-primitive(startX)).sum()))
            A, W, previous_A = A+dA, W+actual_work, old_A
            hist.append(np.r_[X-np.arange(N)-(X-np.arange(N)).mean(), V-V.mean(), Y-Y.mean()])
        histories.append((np.array(hist), A, W))
    difference = float(np.max(abs(histories[0][0]-histories[1][0])))
    assert max(max_identity, max_work, max_chainrule, difference) < 2e-7
    assert min_gap > 0 and max_gap < 2 and mu > 0
    return dict(N=N, stiffness=kappa, g=g, refresh_cosine=r, cells=cells,
        minimum_gap=min_gap, maximum_gap=max_gap,
        max_true_cell_identity_residual=float(max_identity),
        max_actual_work_integral_residual=float(max_work),
        max_current_density_chainrule_residual=float(max_chainrule),
        max_forced_vs_unforced_relative_path_difference=difference,
        unforced_true_displacement=float(histories[0][1]),
        forced_true_displacement=float(histories[1][1]), forced_actual_work=float(histories[1][2]))


def native_exclusion_samples(N, times, seed):
    """Exact bounded-rate Poisson-attempt 2D interacting exclusion realization."""
    rng = np.random.default_rng(seed)
    flat = rng.permutation(np.r_[np.ones(N*N//2, dtype=np.int8), np.zeros(N*N-N*N//2, dtype=np.int8)])
    initial = flat.reshape(N, N).copy()
    starts, ends, rates, increments, rows = [], [], [], [], []
    for y in range(N):
        for x in range(N):
            for dy, dx, D in ((0, 1, .7), (0, -1, .7), (1, 0, 1.1), (-1, 0, 1.1)):
                force = (1.+.8*np.sin(2*np.pi*y/N)) if dx else 0.
                starts.append(y*N+x)
                ends.append(((y+dy)%N)*N+(x+dx)%N)
                rates.append(D*np.exp((dx if dx else dy)*force/(2*N)))
                increments.append(dx)
                rows.append(y)
    starts, ends, increments, rows = map(np.array, (starts, ends, increments, rows))
    cumulative = np.cumsum(rates)
    rate = cumulative[-1]
    B, samples = np.zeros(N, dtype=np.int64), []
    attempts = accepted = vertical = 0
    digest = hashlib.sha256(initial.tobytes())
    clock = float(rng.exponential(1/rate))
    for target in times:
        while clock <= target:
            edge = int(np.searchsorted(cumulative, rng.random()*rate))
            i, j = starts[edge], ends[edge]
            attempts += 1
            if flat[i] and not flat[j]:
                flat[i], flat[j] = 0, 1
                accepted += 1
                if increments[edge]:
                    B[rows[edge]] += increments[edge]
                else:
                    vertical += 1
                digest.update(np.array([i, j], dtype=np.int32).tobytes())
            clock += rng.exponential(1/rate)
        samples.append(B.copy())
    assert int(flat.sum()) == int(initial.sum())
    return np.array(samples), dict(attempts=attempts, accepted=accepted,
        vertical_native_moves=vertical, horizon=float(times[-1]), native_event_hash=digest.hexdigest(),
        initial_row_masses=initial.sum(axis=1).tolist(),
        final_row_masses=flat.reshape(N, N).sum(axis=1).tolist(), total_mass=int(flat.sum()))


def spatial_execution(seed=113017):
    N, h, b, L, blocks, K = 32, 1., .2, 27, 31, 1.5
    p = h+b
    cells = L*blocks
    times = np.arange(cells+1)*p
    native, native_meta = native_exclusion_samples(N, times, seed)
    y = np.arange(N)/N
    kernel = (1-.4**2)/(1-2*.4*np.cos(2*np.pi*y)+.4**2)
    kernel /= kernel.sum()
    S = np.array([np.roll(kernel, i) for i in range(N)])
    g, r = .9+.15*(1+np.sin(2*np.pi*y))/2, .2+.08*np.cos(2*np.pi*y)
    coeff = [coefficients(g[i], h, b, r[i]) for i in range(N)]
    Ms, ds, ells, d0s, ns, ks, mus = [np.array(v) for v in zip(*coeff)]
    rng = np.random.default_rng(seed+1)
    z0 = rng.normal(size=(N, N, 2)).sum(axis=1)
    sources = rng.normal(size=(cells, N, N)).sum(axis=2)

    def target(j):
        t, hh = times[j]/N**2, native[j]/N**2
        smooth = S@hh
        psi = .08*np.sin(2*np.pi*y)*t+.25*smooth/(1+smooth*smooth)
        return psi-hh, psi

    runs = []
    for controlled in (False, True):
        z, A, work = z0.copy(), np.zeros(N), np.zeros(N)
        corrected_work, correction_work = np.zeros(N), np.zeros(N)
        records, forces = [np.zeros(N)], []
        max_error = max_cell_residual = 0.
        clipped = 0
        for block in range(blocks):
            proposed = -K*records[block-1]/N if controlled and block >= 1 else np.zeros(N)
            F = np.clip(proposed, -N**(-.25), N**(-.25))
            clipped += int(np.count_nonzero(F != proposed))
            forces.append(F.copy())
            for j in range(block*L, (block+1)*L):
                dA = np.einsum('ij,ij->i', ells, z)+N*d0s*F
                nextz = np.einsum('ijk,ik->ij', Ms, z)+N*ds*F[:, None]+ns*sources[j, :, None]
                analytic = N*mus*F+np.einsum('ij,ij->i', ks, ns)*sources[j]
                corr = np.einsum('ij,ij->i', ks, nextz-z)
                max_cell_residual = max(max_cell_residual, float(np.max(abs(dA+corr-analytic))))
                A += dA
                work += F*dA
                corrected_work += F*analytic
                correction_work += F*corr
                z = nextz
                q, _ = target(j+1)
                max_error = max(max_error, float(np.sqrt(np.mean((A/N**2-q)**2))))
            q, psi = target((block+1)*L)
            records.append(A/N**2-q)
        output = native[-1]/N**2+A/N**2
        residual = float(np.max(abs(work-corrected_work+correction_work)))
        assert residual < 2e-9 and max_cell_residual < 2e-11
        runs.append(dict(controlled=controlled, final_output_row_current=output.tolist(),
            final_target=psi.tolist(), final_spatial_rms_error=float(np.sqrt(np.mean((output-psi)**2))),
            maximum_sampled_spatial_rms_error=max_error, actual_carrier_work=float(work.sum()),
            corrector_work=float(correction_work.sum()), actual_work_identity_residual=residual,
            cell_identity_residual=max_cell_residual, clipped_commands=clipped,
            max_applied_force=float(np.max(np.abs(np.asarray(forces))))))
    return dict(N=N, T=float(times[-1]/N**2), cell_period=p, held_cells=L,
        one_block_delay=L*p, feedback_gain=K,
        max_actual_loop_gain=float(max(mus)*K*L/N**2), native=native_meta, programs=runs,
        scope='Exact interacting native realization with finite-cell real auxiliary current and ideal readout. Finite errors are reported; no local electronics are simulated.')


def action_and_weak_failure():
    n = 160
    x, y = np.meshgrid(np.arange(n)/n, np.arange(n)/n, indexing='ij')
    tau = 2*np.pi
    rho = .43+.12*np.sin(tau*x)*(.4+.6*np.cos(tau*y))
    rx = .12*tau*np.cos(tau*x)*(.4+.6*np.cos(tau*y))
    ry = -.12*.6*tau*np.sin(tau*x)*np.sin(tau*y)
    jx, jy = .05*tau*np.sin(tau*x)*np.cos(tau*y), -.05*tau*np.cos(tau*x)*np.sin(tau*y)
    Dx, Dy = .7, 1.4
    chi = rho*(1-rho)
    ax, ay = jx+Dx*rx, jy+Dy*ry
    resistance, ell = np.mean(1/(Dx*chi), axis=0), np.mean(ax/(Dx*chi), axis=0)
    u = -ell/resistance
    restricted = float(np.mean(ax*ax/(Dx*chi)+ay*ay/(Dy*chi))/4)
    contracted = restricted-float(np.mean(ell*ell/resistance))/4
    direct = float(np.mean((ax+u[None, :])**2/(Dx*chi)+ay*ay/(Dy*chi))/4)
    errors = []
    for col in (0, 13, 41, 77, 120):
        f = lambda q: float(np.mean((ax[:, col]+q)**2/(Dx*chi[:, col]))/4)
        sol = minimize_scalar(f, bracket=(-.3, .3), method='brent', options={'xtol':1e-12})
        errors.append(abs(sol.fun-f(u[col])))
    assert abs(contracted-direct) < 1e-12 and max(errors) < 1e-12
    weak = []
    yy = np.arange(8192)/8192
    for frequency in (1, 4, 16, 64):
        hh = np.sin(tau*frequency*yy)
        ss = .5**frequency*hh
        weak.append(dict(frequency=frequency, native_mean=float(hh.mean()),
            unsmoothed_nonlinear_mean=float(np.mean(hh*hh/(1+hh*hh))),
            physically_smoothed_nonlinear_mean=float(np.mean(ss*ss/(1+ss*ss)))))
    return dict(grid=n, native_density_range=[float(rho.min()), float(rho.max())],
        passive_restriction_action=restricted, physical_pushforward_action=contracted,
        actual_subtracted_cost=restricted-contracted, direct_vs_contracted_error=abs(contracted-direct),
        numerical_scalar_minimization_error=max(errors), unsmoothed_weak_continuity_failure=weak)


def joint_kernel_check():
    result = []
    for N in (256, 1024, 4096):
        K, delta = np.log(np.log(N+np.e**np.e)), np.log(N)/N
        alpha = 1.3*K*delta
        assert alpha < 1/8
        rp, rm = (1+np.sqrt(1-4*alpha))/2, (1-np.sqrt(1-4*alpha))/2
        j = np.arange(int(np.ceil(40/alpha)))
        kernel = (rp**(j+1)-rm**(j+1))/(rp-rm)
        assert np.all(kernel >= 0)
        result.append(dict(N=N, gain=float(K), actual_loop_gain=float(alpha),
            alpha_times_sum_kernel=float(alpha*kernel.sum()),
            alpha_times_sum_squared_kernel=float(alpha*(kernel*kernel).sum()),
            single_row_exponent_divided_by_volume=float(K/N),
            joint_exponent_divided_by_volume=float(K)))
    return result


def main():
    result = dict(schema='astra_p1.elastic_spatial_program.v1',
        nonlinear_actual_carriers=[nonlinear_train(2., .9, .35, 113101),
                                   nonlinear_train(7., 1.1, -.25, 113102),
                                   nonlinear_train(23., 1., .65, 113103)],
        executed_spatial_program=spatial_execution(),
        spatial_action_and_failed_unsmoothed_map=action_and_weak_failure(),
        delayed_joint_kernel_checks=joint_kernel_check(),
        scope='Population ODE/algebra/exact-event checks. No acquired end-to-end confidence, fitted LDP tail, total apparatus energy, or built device.')
    Path(__file__).with_name('ELASTIC_SPATIAL_CHECK_RESULTS.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
