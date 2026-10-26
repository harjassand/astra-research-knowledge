"""Attempt stronger fixed-capacity contact-routing mechanisms.

Three internal stores share total C=1. Mean sum of all conductances is one.
Three modulated contacts have off/on=.001. Three additional fixed contacts are
explicitly counted. They use more connectors than the one-body architecture,
so even a numerical gain would need a physical cost comparison.
"""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent/'stage1'))
from thermal_network import Phase, laplacian, response, leaky_shuttle
import numpy as np
from scipy.optimize import differential_evolution
import csv


def phases_for(kind, fixed_share, period, eps=.001):
    h = fixed_share/3
    g = (1-fixed_share)/(1+2*eps)
    ring = [(3, 4), (4, 5), (5, 3)]
    phases = []
    for active in range(3):
        if kind == 'gated_internal_ring':
            edges = [(j, j+3, h) for j in range(3)]
            edges += [(a, b, g if k == active else eps*g) for k, (a, b) in enumerate(ring)]
        elif kind == 'gated_ports_fixed_ring':
            edges = [(a, b, h) for a, b in ring]
            edges += [(j, j+3, g if j == active else eps*g) for j in range(3)]
        else:
            raise ValueError(kind)
        phases.append(Phase(period/3, laplacian(6, edges)))
    return phases


def metrics(Y):
    f = np.array([-Y[(i+1) % 3, i] for i in range(3)])
    b = np.array([-Y[(i-1) % 3, i] for i in range(3)])
    if np.mean(f-b) < 0:
        return metrics(Y.T)
    return float(np.min(f-b)), float(np.min(f/b)), float(np.min(f)), float(np.max(b))


def main():
    rows = []
    kinds = ['gated_internal_ring', 'gated_ports_fixed_ring']
    for k, kind in enumerate(kinds):
        for s, objective in enumerate(['directional_excess', 'isolation']):
            def loss(x):
                share, period = x[0], np.exp(x[1])
                Y = response(phases_for(kind, share, period), np.ones(3)/3, 3)['Y']
                value = metrics(Y)[s]
                return -value if s == 0 else -np.log(value)
            sol = differential_evolution(loss, [(.001, .999), (-4., 5.)],
                    seed=(202610264300+2*k+s) % (2**32-1), popsize=10, maxiter=100,
                    tol=2.e-8, polish=True)
            share, P = sol.x[0], np.exp(sol.x[1])
            phases = phases_for(kind, share, P)
            out = response(phases, np.ones(3)/3, 3, 64)
            excess, isolation, forward, reverse = metrics(out['Y'])
            assert abs(sum(np.trace(p.laplacian)/2*p.duration for p in phases)/P-1) < 1.e-12
            installed = share+3*(1-share)/1.002
            rows.append(dict(architecture=kind, objective=objective,
                fixed_conductance_share=share, period=P, capacity_total=1.,
                mean_conductance_total=1., installed_conductance_sum=installed,
                modulated_contacts=3, additional_fixed_contacts=3,
                directional_excess=excess, isolation=isolation, forward=forward, reverse=reverse,
                worst_hot_port_cooling=np.min(np.diag(out['Y'])),
                cooling_over_own_static=np.min(np.diag(out['Y'])/np.diag(out['Ybar'])),
                search_evaluations=sol.nfev, search_converged=bool(sol.success)))
            np.savez(ROOT/f'{kind}_{objective}.npz', **out)
    for objective, z in [('directional_excess', 1.8725571729707948), ('isolation', 6.247198140239216)]:
        Y = leaky_shuttle(3, 1/1.002, .001/1.002, 1., 3*z)
        excess, isolation, forward, reverse = metrics(Y)
        rows.append(dict(architecture='ordinary_one_body_control', objective=objective,
            fixed_conductance_share=0., period=3*z, capacity_total=1.,
            mean_conductance_total=1., installed_conductance_sum=3/1.002,
            modulated_contacts=3, additional_fixed_contacts=0,
            directional_excess=excess, isolation=isolation, forward=forward, reverse=reverse,
            worst_hot_port_cooling=np.min(np.diag(Y)),
            cooling_over_own_static=np.min(np.diag(Y))/(2/9),
            search_evaluations=0, search_converged=True))
    with (ROOT/'architecture_comparison.csv').open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    report = '\n'.join(str(r) for r in rows)+'\n'
    (ROOT/'ARCHITECTURE_RESULTS.txt').write_text(report)
    print(report)


if __name__ == '__main__':
    main()
