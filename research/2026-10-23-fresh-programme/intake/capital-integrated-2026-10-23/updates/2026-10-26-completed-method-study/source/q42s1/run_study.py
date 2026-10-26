"""Reproduce all Q42 stage1 computations; writes only alongside this file."""
from pathlib import Path
import csv
import time
import numpy as np
from scipy.optimize import minimize_scalar
from scipy.integrate import solve_ivp
from thermal_network import (Phase, laplacian, response, shuttle_phases,
                             ideal_shuttle, leaky_shuttle, symmetric,
                             min_contrast_eigenvalue, contrast_basis, blocks,
                             nonuniform_exclusive_shuttle)

ROOT = Path(__file__).resolve().parent
SEED = 2026102642


def write_csv(name, rows):
    with (ROOT/name).open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def three_metrics(z, off_ratio, total_g=1.):
    # Fix mean total contact conductance, not just the active contact.
    on = total_g/(1+2*off_ratio)
    off = off_ratio*on
    period = 3*z/total_g  # C=1
    Y = leaky_shuttle(3, on, off, 1., period)
    forward, reverse = -Y[1, 0], -Y[0, 1]
    return dict(z=z, off_on_ratio=off_ratio, period=period,
                forward_over_total_g=forward/total_g,
                reverse_over_total_g=reverse/total_g,
                forward_reverse_ratio=forward/reverse,
                directional_excess_over_total_g=(forward-reverse)/total_g,
                hot_port_extraction_over_static=Y[0, 0]/(2*total_g/9))


def independent_ode_response(phases, capacities, ports):
    """Adaptive DOP853 integration, repeated to a converged periodic orbit.

    Uses neither segment exponentials nor their periodic fixed point.
    """
    C = np.diag(capacities)
    m = len(capacities)
    X = np.zeros((m, ports))
    for cycle in range(500):
        initial = X.copy()
        Q = np.zeros((ports, ports))
        for phase in phases:
            A, B, D = blocks(phase.laplacian, ports)
            def rhs(t, y):
                x = y[:m*ports].reshape(m, ports)
                return np.r_[np.linalg.solve(C, -A@x+B).ravel(), (D-B.T@x).ravel()]
            y0 = np.r_[X.ravel(), Q.ravel()]
            sol = solve_ivp(rhs, (0., phase.duration), y0,
                            method='DOP853', rtol=2.e-12, atol=2.e-14)
            if not sol.success:
                raise RuntimeError(sol.message)
            X = sol.y[:m*ports, -1].reshape(m, ports)
            Q = sol.y[m*ports:, -1].reshape(ports, ports)
        residual = np.linalg.norm(X-initial)
        if residual < 1.e-12:
            return Q/sum(p.duration for p in phases), cycle+1, residual
    raise RuntimeError('Independent integration did not converge')


def main():
    t0 = time.perf_counter()
    rng = np.random.default_rng(SEED)
    notes = [f'Seed: {SEED}', 'All data are local exact-linear-model calculations.']

    # Abandoned two-phase commutator route: nonsymmetric evolution is real,
    # but does not imply a nonreciprocal period-averaged DC port response.
    LA = laplacian(5, [(3, 4, 3.), (0, 3, 2.), (1, 4, .4), (2, 4, 1.)])
    LB = laplacian(5, [(3, 4, .2), (0, 4, 1.5), (1, 3, .7), (2, 3, .3)])
    two = response([Phase(.7, LA), Phase(1.3, LB)], np.ones(2), 3, 32)
    np.savez(ROOT/'two_phase_counterexample.npz', **two, LA=LA, LB=LB)
    notes += [f'Two-phase monodromy antisymmetry Frobenius norm: '
              f'{np.linalg.norm(two["monodromy"]-two["monodromy"].T):.16g}',
              f'Two-phase DC antisymmetry Frobenius norm: '
              f'{np.linalg.norm(two["Y"]-two["Y"].T):.16g}']

    # Independent augmented-exponential calculation vs closed forms.
    formula_rows = []
    for n in [3, 4, 5, 8]:
        for z in [.02, .2, 1., 4., 12.]:
            for eps in [0., .001, .01, .1]:
                on, off, C = 1.7, 1.7*eps, .8
                G = on+(n-1)*off
                period = n*C*z/G
                exact = response(shuttle_phases(n, on, off, period), [C], n)
                formula = leaky_shuttle(n, on, off, C, period)
                formula_rows.append(dict(ports=n, z=z, off_on_ratio=eps,
                    maximum_absolute_error=np.max(np.abs(exact['Y']-formula)),
                    periodic_residual=exact['periodic_residual']))
    write_csv('closed_form_checks.csv', formula_rows)
    notes += [f'Closed form checks: {len(formula_rows)}; maximum absolute error: '
              f'{max(r["maximum_absolute_error"] for r in formula_rows):.16g}']

    # Exact nonuniform construction: wide, independently drawn contacts/durations.
    nonuniform_rows = []
    contact_rng = np.random.default_rng(SEED+1)
    for trial in range(60):
        n = [3, 4, 5, 8][trial % 4]
        g = np.exp(contact_rng.uniform(-2., 2., n))
        tau = np.exp(contact_rng.uniform(-2., 1., n))
        C = np.exp(contact_rng.uniform(-1., 1.))
        phases = [Phase(tau[i], laplacian(n+1, [(i, n, g[i])])) for i in range(n)]
        Y = response(phases, [C], n)['Y']
        form = nonuniform_exclusive_shuttle(g, tau, C)
        nonuniform_rows.append(dict(trial=trial, ports=n,
            maximum_absolute_error=np.max(np.abs(Y-form))))
    write_csv('nonuniform_contact_checks.csv', nonuniform_rows)
    notes += [f'Nonuniform contact checks: {len(nonuniform_rows)}; max absolute error: '
              f'{max(r["maximum_absolute_error"] for r in nonuniform_rows):.16g}']

    # Diverse held-out graph diagnostics.  Equations and proof precede sampling;
    # these do not substitute for the universal proof.
    graph_rows = []
    for trial in range(120):
        ports = [3, 4, 6][trial % 3]
        internal = [1, 2, 4, 7][(trial//3) % 4]
        count = [2, 3, 5, 8][(trial//12) % 4]
        N = ports+internal
        C = np.exp(rng.uniform(-1.5, 1.5, internal))
        phases = []
        for _ in range(count):
            # A positive spanning chain guarantees grounded coercivity in each
            # phase. Extra edges include internal, boundary and direct contacts.
            edges = [(i, i+1, np.exp(rng.uniform(-2., 1.))) for i in range(N-1)]
            for i in range(N):
                for j in range(i+2, N):
                    if rng.random() < .3:
                        edges.append((i, j, np.exp(rng.uniform(-2., 1.))))
            phases.append(Phase(np.exp(rng.uniform(-2., .7)), laplacian(N, edges)))
        out = response(phases, C, ports, 40)
        back = response(list(reversed(phases)), C, ports)
        Y, Ybar = out['Y'], out['Ybar']
        scale = max(np.linalg.norm(Ybar), 1.)
        diff = Ybar-symmetric(Y)
        U = contrast_basis(ports)
        Yc, Ybarc = U.T@Y@U, U.T@Ybar@U
        circle = symmetric(Yc)-Yc.T@np.linalg.solve(Ybarc, Yc)
        graph_rows.append(dict(trial=trial, ports=ports, internal=internal,
            phases=count, period=out['period'],
            reversal_transpose_error=np.linalg.norm(Y-back['Y'].T)/scale,
            dissipation_identity_error=np.linalg.norm(diff-out['gap_integral'])/scale,
            minimum_dominance_contrast_eigenvalue=min_contrast_eigenvalue(diff),
            minimum_passivity_contrast_eigenvalue=min_contrast_eigenvalue(Y),
            minimum_circle_bound_eigenvalue=np.linalg.eigvalsh(symmetric(circle))[0],
            row_sum_error=np.max(np.abs(Y.sum(axis=1)))/scale,
            column_sum_error=np.max(np.abs(Y.sum(axis=0)))/scale,
            periodic_residual=out['periodic_residual'],
            dc_antisymmetry=np.linalg.norm(Y-Y.T)/scale))
    write_csv('network_checks.csv', graph_rows)
    notes += [f'Random network cases: {len(graph_rows)}',
              f'Max reversal-transpose relative error: '
              f'{max(r["reversal_transpose_error"] for r in graph_rows):.16g}',
              f'Max gap-identity relative error: '
              f'{max(r["dissipation_identity_error"] for r in graph_rows):.16g}',
              f'Min dominance eigenvalue on temperature-contrast space: '
              f'{min(r["minimum_dominance_contrast_eigenvalue"] for r in graph_rows):.16g}',
              f'Min passivity eigenvalue on temperature-contrast space: '
              f'{min(r["minimum_passivity_contrast_eigenvalue"] for r in graph_rows):.16g}',
              f'Min circle-bound eigenvalue on temperature-contrast space: '
              f'{min(r["minimum_circle_bound_eigenvalue"] for r in graph_rows):.16g}',
              f'Max two-phase DC antisymmetry relative norm: '
              f'{max(r["dc_antisymmetry"] for r in graph_rows if r["phases"] == 2):.16g}']

    grid = np.geomspace(1.e-3, 40., 600)
    ratios = [0., 1.e-4, 1.e-3, 1.e-2, .1]
    frontier = [three_metrics(z, eps) for eps in ratios for z in grid]
    write_csv('three_port_frontier.csv', frontier)
    optimum = []
    for eps in ratios:
        # Ideal ratio is unbounded only as throughput tends to zero.
        if eps > 0:
            sol = minimize_scalar(lambda z: -np.log(three_metrics(z, eps)['forward_reverse_ratio']),
                                  bounds=(.00001, 80.), method='bounded',
                                  options={'xatol': 1.e-12})
            row = three_metrics(sol.x, eps)
            row['optimized_objective'] = 'maximum_isolation_ratio'
            optimum.append(row)
        sol = minimize_scalar(lambda z: -three_metrics(z, eps)['directional_excess_over_total_g'],
                              bounds=(.00001, 80.), method='bounded',
                              options={'xatol': 1.e-12})
        row = three_metrics(sol.x, eps)
        row['optimized_objective'] = 'maximum_directional_excess'
        optimum.append(row)
    write_csv('three_port_optima.csv', optimum)

    # Save inspectable actual matrices at a specified, non-selected setting.
    specimen = response(shuttle_phases(3, 1/1.002, .001/1.002, 9.), [1.], 3, 40)
    np.savez(ROOT/'three_port_example.npz', **specimen)
    notes += ['Representative three-port example: C=1, total active+leak conductance=1, '
              'off/on=.001, period=9 (z=3).', 'Y =', np.array2string(specimen['Y'], precision=10),
              'Matched mean-conductance static Y =', np.array2string(specimen['Ybar'], precision=10),
              'Finite leakage optima:', str(optimum)]

    ode_rows = []
    for name, phases, capacities, target in [
        ('two_phase', [Phase(.7, LA), Phase(1.3, LB)], [1., 1.], two['Y']),
        ('three_port_leaky', shuttle_phases(3, 1/1.002, .001/1.002, 9.), [1.], specimen['Y'])]:
        Yode, cycles, residual = independent_ode_response(phases, capacities, 3)
        ode_rows.append(dict(case=name, cycles=cycles, periodic_residual=residual,
            maximum_absolute_error=np.max(np.abs(Yode-target))))
    write_csv('independent_ode_checks.csv', ode_rows)
    notes += ['Independent adaptive ODE integration:', str(ode_rows)]

    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.0), constrained_layout=True)
    for eps in ratios:
        rows = [r for r in frontier if r['off_on_ratio'] == eps]
        label = 'ideal, zero leak' if eps == 0 else f'off/on = {eps:g}'
        axes[0].plot(grid, [r['forward_reverse_ratio'] for r in rows], label=label)
        axes[1].plot(grid, [r['directional_excess_over_total_g'] for r in rows], label=label)
        axes[2].plot(grid, [r['hot_port_extraction_over_static'] for r in rows], label=label)
    axes[0].set(xscale='log', yscale='log', ylim=(1, 1.e4),
                xlabel='Contact relaxation per phase z = G P / (3 C)',
                ylabel='Forward / reverse DC transfer', title='Finite leakage caps isolation')
    axes[1].set(xscale='log', xlabel='Contact relaxation per phase z',
                ylabel='(Forward - reverse) / G', title='Directional throughput has an optimum')
    axes[2].set(xscale='log', xlabel='Contact relaxation per phase z',
                ylabel='Hot-port extraction / matched static extraction',
                title='Cooling stays below the static comparator')
    axes[2].axhline(1, color='black', linestyle=':', linewidth=1)
    for ax in axes:
        ax.grid(True, alpha=.25)
    axes[0].legend(fontsize=8)
    fig.savefig(ROOT/'thermal_tradeoff.svg')
    fig.savefig(ROOT/'thermal_tradeoff.png', dpi=170)
    plt.close(fig)

    # Assertions detect an implementation error rather than establishing theory.
    assert max(r['maximum_absolute_error'] for r in formula_rows) < 2.e-11
    assert max(r['maximum_absolute_error'] for r in nonuniform_rows) < 2.e-11
    assert max(r['reversal_transpose_error'] for r in graph_rows) < 2.e-10
    assert max(r['dissipation_identity_error'] for r in graph_rows) < 2.e-9
    assert min(r['minimum_dominance_contrast_eigenvalue'] for r in graph_rows) > -2.e-10
    assert min(r['minimum_passivity_contrast_eigenvalue'] for r in graph_rows) > -2.e-10
    assert min(r['minimum_circle_bound_eigenvalue'] for r in graph_rows) > -2.e-10
    assert max(r['maximum_absolute_error'] for r in ode_rows) < 2.e-10
    notes += [f'Runtime seconds: {time.perf_counter()-t0:.3f}', 'All numerical checks passed.']
    (ROOT/'NUMERICAL_RESULTS.txt').write_text('\n'.join(notes)+'\n')
    print('\n'.join(notes[:13]))
    print('All numerical checks passed.')


if __name__ == '__main__':
    main()
