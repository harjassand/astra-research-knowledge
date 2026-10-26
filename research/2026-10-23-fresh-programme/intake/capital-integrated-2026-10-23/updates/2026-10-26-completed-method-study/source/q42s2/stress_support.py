"""Withheld support/topology and underflow stress; stage1 is read only."""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent/'stage1'))
from thermal_network import Phase, laplacian, response, ideal_shuttle
import csv
import numpy as np
import mpmath as mp


def save_csv(name, rows):
    with (ROOT/name).open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def avoiding_path(W, ports, i, j):
    # Other fixed-temperature terminals absorb the perturbation and cannot be
    # treated as hidden transit nodes.
    todo = [[i]]
    seen = {i}
    while todo:
        path = todo.pop(0)
        for k in np.flatnonzero(W[path[-1]] > 0):
            if k == j:
                return path+[int(k)]
            if k >= ports and k not in seen:
                seen.add(int(k))
                todo.append(path+[int(k)])
    return None


def main():
    rng = np.random.default_rng(202610264201)
    rows = []
    # Sparse sequential trees differ from the dense grounded phases in stage1.
    # Each individual phase can be disconnected; only the union must connect.
    for case in range(80):
        ports = [3, 4, 5, 6][case % 4]
        internal = [1, 2, 3, 5][(case//4) % 4]
        N = ports+internal
        order = rng.permutation(N)
        edges = [(int(order[k]), int(order[int(rng.integers(k))])) for k in range(1, N)]
        capacities = np.exp(rng.uniform(-.7, .7, internal))
        phases = [Phase(float(np.exp(rng.uniform(-1., .7))),
                        laplacian(N, [(i, j, float(np.exp(rng.uniform(-1., .7))))]))
                  for i, j in edges]
        rng.shuffle(phases)
        out = response(phases, capacities, ports, 48)
        P = out['period']
        Lint = sum(p.duration*p.laplacian for p in phases)
        W = -Lint
        np.fill_diagonal(W, 0.)
        delta = max(np.max(np.diag(p.laplacian)[ports:]/capacities) for p in phases)
        for i in range(ports):
            for j in range(i+1, ports):
                path = avoiding_path(W, ports, i, j)
                forward, reverse = -out['Y'][j, i], -out['Y'][i, j]
                if path is None:
                    logbound = float('-inf')
                    assert abs(forward) < 2.e-12 and abs(reverse) < 2.e-12
                else:
                    hidden = path[1:-1]
                    k = len(hidden)
                    logbound = (-k*delta*P - np.log(P)
                        +sum(np.log(W[a, b]) for a, b in zip(path[:-1], path[1:]))
                        -sum(np.log(capacities[v-ports]) for v in hidden))
                    assert forward > 0 and reverse > 0
                    assert np.log(min(forward, reverse)) >= logbound-2.e-10
                rows.append(dict(case=case, ports=ports, internal=internal,
                    phases=len(phases), pair=f'{i}-{j}', connected_without_other_ports=path is not None,
                    path='' if path is None else '-'.join(map(str, path)),
                    forward=forward, reverse=reverse,
                    log_reverse_floor=logbound,
                    static_gap_error=np.linalg.norm(out['Ybar']-(out['Y']+out['Y'].T)/2-out['gap_integral'])))
    save_csv('withheld_support_cases.csv', rows)

    mp.mp.dps = 100
    underflow = []
    for z0 in [12, 40, 100, 500, 800]:
        z = mp.mpf(z0)
        r = mp.exp(-z)
        a = (1-r)/(3*z*(1+r+r*r))  # C=G=1, P=3*z
        Yfloat = ideal_shuttle(3, 1., 1., 3*z0)
        reverse_float = -Yfloat[0, 1]
        underflow.append(dict(z=z0, period=3*z0,
            float64_reverse=reverse_float,
            high_precision_reverse=mp.nstr(a*r, 80),
            high_precision_isolation=mp.nstr(1/r, 80),
            log_lower_bound=mp.nstr(mp.log(z/3)-3*z, 80),
            hot_port_cooling_over_static=mp.nstr((a*(1+r))/(mp.mpf(2)/9), 25)))
    save_csv('underflow_stress.csv', underflow)
    connected = [r for r in rows if r['connected_without_other_ports']]
    absent = [r for r in rows if not r['connected_without_other_ports']]
    report = (f'Withheld sparse phase schedules: 80\nPort pairs: {len(rows)}\n'
              f'Pairs linked without another terminal: {len(connected)}\n'
              f'Pairs separated by terminal cuts: {len(absent)}\n'
              f'Min nonzero reverse/forward coefficient: '
              f'{min(min(r["forward"],r["reverse"]) for r in connected):.16g}\n'
              f'Max static gap identity error: {max(r["static_gap_error"] for r in rows):.16g}\n'
              'Every predicted support relation and quantitative reverse floor passed.\n'
              'At z=800, Float64 reports zero reverse transfer, while 100-digit '
              'arithmetic gives a strictly positive coefficient.\n')
    (ROOT/'STRESS_RESULTS.txt').write_text(report)
    print(report)


if __name__ == '__main__':
    main()
