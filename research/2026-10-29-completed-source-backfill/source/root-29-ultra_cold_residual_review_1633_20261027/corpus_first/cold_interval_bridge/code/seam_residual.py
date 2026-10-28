"""Actual spin-two local expansional seam residual; numerical discovery stage."""
import sys
sys.dont_write_bytecode = True
import itertools, json, time
from pathlib import Path
import numpy as np
from scipy.sparse import csr_matrix
from scipy.linalg import eigh, svdvals
BASE = Path(__file__).resolve().parents[1]


def sector(n, magnetization):
    states = [q for q in itertools.product(range(-2, 3), repeat=n)
              if sum(q) == magnetization]
    lookup = {q:i for i, q in enumerate(states)}
    return states, lookup


def bond(states, lookup, i, j):
    rows, cols, values = [], [], []
    for col, q in enumerate(states):
        rows.append(col); cols.append(col); values.append(q[i]*q[j])
        for sign in (-1, 1):
            a, b = q[i], q[j]
            if -2 <= a+sign <= 2 and -2 <= b-sign <= 2:
                p = list(q); p[i] += sign; p[j] -= sign
                weight = np.sqrt((6-a*(a+sign))*(6-b*(b-sign)))/2
                rows.append(lookup[tuple(p)]); cols.append(col); values.append(weight)
    return csr_matrix((values, (rows, cols)), shape=(len(states), len(states)))


class LocalSeam:
    def __init__(self, ell):
        self.ell = ell; self.n = 2*ell; self.spectra = {}; self.orders = {}
        for m in range(-2, 3):
            states, lookup = sector(self.n, m); self.orders[m] = lookup
            h = sum((bond(states, lookup, i, i+1) for i in range(self.n-1)),
                    csr_matrix((len(states), len(states))))
            h0 = h-bond(states, lookup, ell-1, ell)
            self.spectra[m] = (eigh(h.toarray()), eigh(h0.toarray()))
        states, lookup = sector(self.n+1, 0); self.states = states
        self.hout = bond(states, lookup, 0, 1)
        self.blocks = []
        for a in range(-2, 3):
            indices = [i for i, q in enumerate(states) if q[0] == a]
            order = [self.orders[-a][states[i][1:]] for i in indices]
            self.blocks.append((np.array(indices), np.array(order), -a))

    def local(self, s):
        out = {}
        for m, ((w, u), (w0, u0)) in self.spectra.items():
            out[m] = ((u*np.exp(-s*w/2))@u.T)@((u0*np.exp(s*w0/2))@u0.T)
        return out

    def residual(self, s):
        local = self.local(s); E = np.zeros((len(self.states), len(self.states)))
        for ix, order, m in self.blocks:
            E[np.ix_(ix, ix)] = local[m][np.ix_(order, order)]
        R = self.hout@E-(self.hout@E.T).T
        norm = float(svdvals(R)[0])
        schur = float(np.sqrt(np.max(np.sum(np.abs(R), axis=0))*
                              np.max(np.sum(np.abs(R), axis=1))))
        e_norm = max(float(svdvals(e)[0]) for e in local.values())
        return dict(s=s, one_boundary_commutator_norm=norm,
                    Schur_upper_numeric=schur, local_expansional_norm=e_norm)


def run():
    start = time.monotonic(); rows = []
    for ell in (1, 2):
        source = LocalSeam(ell)
        samples = [source.residual(s) for s in (0, .125, .25, .5, .75, 1., 1.5, 2., 3.)]
        row = dict(ell=ell, maximum_local_sector=max(len(w[0][0]) for w in source.spectra.values()),
                   residual_M0_dimension=len(source.states), samples=samples)
        rows.append(row)
        print('ell', ell, 'dim', len(source.states), 'beta1.5 commutator', samples[6], flush=True)
    result = dict(status='NUMERICAL_SOURCE_SPECIFIC_RESIDUAL_DISCOVERY_NOT_CERTIFICATE',
        rows=rows, elapsed_seconds=time.monotonic()-start,
        symmetry='The commutator is SU2 invariant. Its norm occurs in total M0, which contains every integer-spin irrep.',
        bound_to_be_acquired='eta_ell(beta)<= integral_0^beta exp(2s)||[h_out,E_ell(s)]|| ds for an interior join with two boundaries; one seam with truncated two-end neighborhoods has the same two-boundary estimate.')
    (BASE/'results/SEAM_RESIDUAL_DISCOVERY.json').write_text(json.dumps(result, indent=2)+'\n')
    print('elapsed', result['elapsed_seconds'])


if __name__ == '__main__':
    run()
