#!/usr/bin/env python3
"""Population checks of the actual local realization, not an acquisition trial.

Independent full-state resolvents check the hidden-impedance reduction and FDT.
Small mode matrices check the selected two-ring common-current law and DC work.
No trajectory simulation is used as a substitute for the path proofs.
"""
from pathlib import Path
import json
import math
import platform
import numpy as np
import scipy
import scipy.linalg as la

HERE = Path(__file__).resolve().parent


def incidence(n):
    b = -np.eye(n)
    for i in range(n):
        b[i, (i - 1) % n] += 1.0
    return b


def ladder(n):
    b = incidence(n)
    z = np.zeros_like(b)
    big_b = la.block_diag(b, b)
    a = np.block([[b, z], [z, -b], [np.eye(n), np.eye(n)]])
    h = np.r_[np.ones(n), -np.ones(n)] / np.sqrt(2 * n)
    return big_b, a, h


def hidden_native_case(n, seed):
    rng = np.random.default_rng(seed)
    b, a, h = ladder(n)
    m = 2 * n
    p_dim = a.shape[0]
    tau, speed, gamma = 0.7, 1.3, 0.05
    r0 = np.diag(rng.uniform(0.8, 1.6, m))
    shift = la.block_diag(np.roll(np.eye(n), 1, axis=0),
                         np.roll(np.eye(n), -1, axis=0))
    cs = [np.diag(rng.uniform(0.10, 0.25, m)) + 0.06 * shift,
          np.diag(rng.uniform(0.06, 0.18, m)) - 0.04 * shift.T]
    nus = [0.4, 1.1]
    lap = a.T @ a
    positive = la.eigvalsh(lap)
    gap = float(positive[positive > 1e-10][0])
    kappa = 0.15 * np.sqrt(gap)
    g = np.sqrt(kappa)
    omega_max = 0.0001 * gap
    rmin = float(np.min(np.diag(r0)))
    rmax = (float(la.norm(r0, 2)) + tau * omega_max
            + sum(float(la.norm(c, 2)) ** 2 / nu for c, nu in zip(cs, nus)))
    assert omega_max ** 2 <= speed ** 2 * gap / 2
    assert rmax * omega_max / kappa <= 0.5
    eps = 2 * omega_max / kappa
    dd = 2 * kappa / speed ** 2 * (gamma + omega_max / gap)
    bound = (dd / rmin ** 2 + eps * (1 + rmax / rmin) ** 2
             + rmax ** 2 * eps ** 2 / rmin)

    sizes = [m, m, p_dim, m, m, m]
    starts = np.cumsum([0] + sizes)
    sx, sq, sp, su, sh1, sh2 = [slice(starts[i], starts[i+1]) for i in range(6)]
    dim = int(starts[-1])
    drift = np.zeros((dim, dim))
    drift[sx, su] = b / np.sqrt(tau)
    drift[sq, su] = g * np.eye(m) / np.sqrt(tau)
    drift[sq, sp] = -speed * a.T
    drift[sp, sq] = speed * a
    drift[sp, sp] = -gamma * a @ a.T
    drift[su, sx] = -b.T / np.sqrt(tau)
    drift[su, sq] = -g * np.eye(m) / np.sqrt(tau)
    drift[su, su] = -r0 / tau
    for sl, c, nu in zip([sh1, sh2], cs, nus):
        drift[sl, su] = c / np.sqrt(tau)
        drift[su, sl] = -c.T / np.sqrt(tau)
        drift[sl, sl] = -nu * np.eye(m)
    noise = np.zeros((dim, 4*m))
    noise[su, :m] = np.diag(np.sqrt(2 * np.diag(r0) / tau))
    noise[sp, m:2*m] = np.sqrt(2*gamma) * a
    noise[sh1, 2*m:3*m] = np.sqrt(2*nus[0]) * np.eye(m)
    noise[sh2, 3*m:] = np.sqrt(2*nus[1]) * np.eye(m)
    force = np.zeros((dim, m))
    force[su] = np.eye(m) / np.sqrt(tau)
    output = force.T.copy()
    q_counter = np.zeros(dim)
    q_counter[sq] = h
    counter_error = la.norm(q_counter @ drift - g*h @ output)
    counter_noise_error = la.norm(q_counter @ noise)
    gibbs_error = la.norm(drift + drift.T + noise @ noise.T, 2)
    q_basis = la.null_space(h[None, :])
    kval = b.T @ b
    commutator = la.norm(r0 @ lap - lap @ r0, 2)
    rows = []
    for fraction in [0.05, 0.3, 1.0]:
        omega = fraction * omega_max
        zz = 1j * omega
        native = r0.astype(complex) + tau * zz * np.eye(m)
        for c, nu in zip(cs, nus):
            native += c.T @ c / (nu + zz)
        controller = kappa * la.solve(
            zz*zz*np.eye(m) + gamma*zz*lap + speed**2*lap,
            zz*np.eye(m) + gamma*lap)
        impedance = native + kval / zz + controller
        reduced_y = la.solve(impedance, np.eye(m))
        full_y = output @ la.solve(zz*np.eye(dim) - drift, force)
        full_noise_transfer = output @ la.solve(zz*np.eye(dim) - drift, noise)
        full_spectrum = full_noise_transfer @ full_noise_transfer.conj().T
        target = q_basis @ la.solve(
            q_basis.T @ (native + kval/zz) @ q_basis,
            q_basis.T)
        y_error = float(la.norm(full_y - reduced_y, 2))
        fdt_error = float(la.norm(full_spectrum - full_y - full_y.conj().T, 2))
        target_error = float(la.norm(full_y - target, 2))
        assert y_error < 2e-7
        assert fdt_error < 2e-7
        assert target_error <= bound + 2e-7
        rows.append(dict(omega=omega, full_vs_eliminated=y_error,
                         full_noise_vs_fdt=fdt_error, actual_target_error=target_error,
                         proved_band_bound=bound))
    assert gibbs_error < 1e-12
    assert counter_error < 1e-12 and counter_noise_error < 1e-12
    return dict(n=n, hidden_relaxation_rates=nus, gap=gap, kappa=kappa,
                omega_max=omega_max, rmin=rmin, rmax=rmax,
                noncommuting_native_norm=float(commutator),
                gibbs_residual=float(gibbs_error), counter_residual=float(counter_error),
                counter_noise_residual=float(counter_noise_error), frequency_cases=rows)


def harmonic_mode(beta, g, r1, r2, tau, speed, gamma):
    # A real Fourier gauge; coordinates x(2),q(2),p(3),u(2).
    b = beta * np.eye(2)
    a = np.array([[beta, 0.], [0., -beta], [1., 1.]])
    mat = np.zeros((9, 9))
    mat[0:2, 7:9] = b / np.sqrt(tau)
    mat[2:4, 7:9] = g * np.eye(2) / np.sqrt(tau)
    mat[2:4, 4:7] = -speed * a.T
    mat[4:7, 2:4] = speed * a
    mat[4:7, 4:7] = -gamma * a @ a.T
    mat[7:9, 0:2] = -b.T / np.sqrt(tau)
    mat[7:9, 2:4] = -g * np.eye(2) / np.sqrt(tau)
    mat[7:9, 7:9] = -np.diag([r1, r2]) / tau
    return mat


def selective_mode_cases():
    r1, r2, tau, speed, gamma = 1.2, 2.1, 0.7, 1.3, 0.2
    horizon = 0.15
    rows = []
    for n in [16, 64, 256]:
        kappa = 1 / np.log(n + 1)
        g = np.sqrt(kappa)
        beta = 2 * np.sin(np.pi/n)
        mat = harmonic_mode(beta, g, r1, r2, tau, speed, gamma)
        mean = la.expm(mat * (n*n*horizon))[:2, :2]
        ideal_mean = np.diag(np.exp(-4*np.pi**2*horizon/np.array([r1,r2])))
        # At zero wave number remove decoupled x and the first two p coordinates.
        zero = harmonic_mode(0., g, r1, r2, tau, speed, gamma)
        ix = [2, 3, 6, 7, 8]
        stable = zero[np.ix_(ix, ix)]
        out = np.zeros((2, 5)); out[:, 3:5] = np.eye(2) / np.sqrt(tau)
        time = n*n*horizon
        integral = la.solve(stable, la.solve(stable,
                           la.expm(time*stable) - np.eye(5) - time*stable))
        integrated_cov = out @ (integral + integral.T) @ out.T / (n*n)
        target_cov = (2*horizon/(r1+r2))*np.ones((2,2))
        force = out.T
        dc = -out @ la.solve(stable, force)
        target_dc = np.ones((2,2))/(r1+r2+2*kappa*gamma/speed**2)
        dc_error = float(la.norm(dc-target_dc, 2))
        assert dc_error < 1e-12
        rows.append(dict(n=n, kappa=float(kappa), macro_horizon=horizon,
                         density_response=mean.tolist(), native_heat_response=ideal_mean.tolist(),
                         density_response_error=float(la.norm(mean-ideal_mean,2)),
                         harmonic_integrated_covariance=integrated_cov.tolist(),
                         target_common_covariance=target_cov.tolist(),
                         common_covariance_error=float(la.norm(integrated_cov-target_cov,2)),
                         exact_dc_response=dc.tolist(), dc_formula_error=dc_error))
    return rows


def marked_particle_balance():
    # Exact algebra is in the proof; these floating evaluations catch sign/update mistakes.
    maximum = 0.
    count = 0
    for g in [0.07, 0.3, 0.8]:
        for q in [-2., -0.2, 0., 0.5, 2.4]:
            for delta in [-1., 1.]:
                qp = q + g*delta
                energy = g*delta*q + g*g/2
                reverse_energy = g*(-delta)*qp + g*g/2
                forward = np.exp(-q*q/2)*min(1., np.exp(-energy))
                reverse = np.exp(-qp*qp/2)*min(1., np.exp(-reverse_energy))
                maximum = max(maximum, abs(forward-reverse), abs(energy+reverse_energy))
                count += 1
    assert maximum < 1e-14
    return dict(marked_pairs=count, max_balance_or_energy_reversal_error=float(maximum),
                scope='Only local marked balance; no nonlinear heat/action validation.')


def main():
    result = dict(
        scope='Executed population linear-port and marked-event checks; no acquired confidence budget.',
        python=platform.python_version(), numpy=np.__version__, scipy=scipy.__version__,
        hidden_impedance_cases=[hidden_native_case(8, 1009), hidden_native_case(12, 1013)],
        selective_modes=selective_mode_cases(), nonlinear_marked_balance=marked_particle_balance())
    path = HERE / 'LOCAL_TRANSPORT_LAW_CHECK.json'
    path.write_text(json.dumps(result, indent=2)+'\n')
    frequency_rows=[r for case in result['hidden_impedance_cases'] for r in case['frequency_cases']]
    print(json.dumps(dict(output=str(path),
        max_full_resolvent_error=max(r['full_vs_eliminated'] for r in frequency_rows),
        max_full_noise_fdt_error=max(r['full_noise_vs_fdt'] for r in frequency_rows),
        max_bound_ratio=max(r['actual_target_error']/r['proved_band_bound'] for r in frequency_rows),
        max_dc_formula_error=max(r['dc_formula_error'] for r in result['selective_modes']),
        marked_pairs=result['nonlinear_marked_balance']['marked_pairs']), indent=2))


if __name__ == '__main__':
    main()
