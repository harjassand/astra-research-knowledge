"""Finite Pauli-cloner/stabilizer-design diagnostic, not a universal proof.

Requires numpy, scipy (scipy only for adaptive mode).
Examples:
  python pauli_screen.py --qubits 2 --mode subsets
  python pauli_screen.py --qubits 2 --mode random --count 15000 --seed 144
  python pauli_screen.py --qubits 3 --mode random --count 12000 --seed 294042
  python pauli_screen.py --qubits 3 --mode adaptive --count 200 --seed 435625

All reported support lower bounds are STABILIZER designs, not exact h1.
Even a positive gap would require a global h1 upper certificate.
"""
import argparse
import itertools
import json
from pathlib import Path
import time
import numpy as np


def interface(n):
    d, nn = 2**n, 4**n
    sp = lambda a, b: (((a % d) & (b // d)).bit_count()
                       + ((a // d) & (b % d)).bit_count()) % 2
    ops = []
    for v in range(1, nn):
        xx = np.zeros((nn, nn))
        xx[np.arange(nn), np.arange(nn)^v] = 1
        ops.append(np.diag([(-1)**sp(u, v) for u in range(nn)])+xx)
    # Enumerate maximal isotropic label subspaces for n<=3.
    lines = set()
    for generators in itertools.combinations(range(1, nn), n):
        if any(sp(a, b) for a, b in itertools.combinations(generators, 2)):
            continue
        span = {0}
        for a in generators:
            span |= {b ^ a for b in tuple(span)}
        if len(span) == d:
            lines.add(tuple(sorted(span-{0})))
    lineidx = np.array(sorted(lines), dtype=int)-1
    lmat = np.zeros((len(lines), nn-1))
    for i, line in enumerate(lineidx):
        lmat[i, line] = 1
    return np.array(ops), lineidx, lmat


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--qubits', type=int, choices=[1, 2, 3], default=2)
    ap.add_argument('--mode', choices=['subsets', 'random', 'adaptive'], default='random')
    ap.add_argument('--count', type=int, default=1000)
    ap.add_argument('--seed', type=int, default=144)
    ap.add_argument('--iterations', type=int, default=12)
    ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    if args.mode == 'subsets' and args.qubits != 2:
        ap.error('Exhaustive support enumeration is restricted to two qubits.')
    start = time.monotonic()
    ops, lineidx, lmat = interface(args.qubits)
    size = len(ops)
    rng = np.random.default_rng(args.seed)
    candidates = []
    bestgap = -float('inf')
    evaluated = 0
    if args.mode == 'adaptive':
        from scipy.optimize import linprog
        for run in range(args.count):
            q = rng.exponential(size=size)
            q /= np.max(lmat@q)
            for iteration in range(args.iterations):
                val, vec = np.linalg.eigh(np.einsum('v,vij->ij', q, ops))
                a = vec[:, -1]
                r = np.einsum('i,vij,j->v', a, ops, a)-1
                lp = linprog(-r, A_ub=lmat, b_ub=np.ones(len(lmat)),
                             bounds=(0, None), method='highs')
                if not lp.success:
                    raise RuntimeError(lp.message)
                q = lp.x
                gap = -lp.fun-1
                evaluated += 1
                bestgap = max(bestgap, float(gap))
                if gap > 1e-7:
                    candidates.append({'gap_against_stabilizer_lower': float(gap),
                                       'q': q.tolist(), 'a': a.tolist(),
                                       'run': run, 'iteration': iteration})
                    break
    else:
        count = 2**size-1 if args.mode == 'subsets' else args.count
        for it in range(count):
            if args.mode == 'subsets':
                bits = it+1
                q = np.array([(bits >> j) & 1 for j in range(size)], float)
            elif args.qubits == 2:
                if it % 3 == 0:
                    q = rng.exponential(size=size)
                elif it % 3 == 1:
                    q = np.maximum(0, rng.normal(size=size))
                else:
                    q = 10**rng.uniform(-3, 0, size=size)
            else:
                if it % 4 == 0:
                    q = rng.exponential(size=size)
                elif it % 4 == 1:
                    q = (rng.random(size) < rng.uniform(.08, .6)).astype(float)
                elif it % 4 == 2:
                    q = 10**rng.uniform(-3, 0, size=size)
                else:
                    q = np.maximum(0, rng.normal(size=size))
            if not q.any():
                continue
            if args.mode != 'subsets':
                q /= q.sum()
            excess = np.linalg.eigvalsh(np.einsum('v,vij->ij', q, ops))[-1]-q.sum()
            lower = np.max(q[lineidx].sum(axis=1))
            gap = float(excess-lower)
            bestgap = max(bestgap, gap)
            evaluated += 1
            if gap > 1e-7:
                candidates.append({'gap_against_stabilizer_lower': gap,
                                   'cloner_excess': float(excess),
                                   'stabilizer_design_lower': float(lower),
                                   'q': q.tolist(), 'iteration': it})
    candidates.sort(key=lambda a: -a['gap_against_stabilizer_lower'])
    out = {'status': 'FINITE_NUMERICAL_SCREEN_ONLY',
           'warning': 'Stabilizer support is a lower bound on h1; no exact theorem or counterexample.',
           'dimension': 2**args.qubits, 'qubits': args.qubits,
           'mode': args.mode, 'seed': args.seed, 'requested_count': args.count,
           'evaluated': evaluated, 'Lagrangian_designs': len(lineidx),
           'threshold': 1e-7, 'best_gap_against_stabilizer_lower': bestgap,
           'candidate_count': len(candidates), 'candidates': candidates[:100],
           'elapsed_seconds': time.monotonic()-start}
    target = args.output or Path(__file__).with_name(
        f'pauli_screen_n{args.qubits}_{args.mode}.json')
    target.write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps({k: v for k, v in out.items() if k != 'candidates'}, indent=2))


if __name__ == '__main__':
    main()
