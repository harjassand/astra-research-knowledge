"""Exact branch-register algebra, not an asymptotic or hardware validation.

The three Pauli-write outcomes have exclusive source projectors and a
common target. This detects replacing their separate records by a coherent
sum. All identities are checked on a basis of the full data operator space.
"""
from __future__ import annotations
import hashlib
import itertools
import json
import math
from pathlib import Path
import sympy as s

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'outputs/tanner_controller_20261101'


def unit(d, a, b):
    v = s.zeros(d)
    v[a, b] = 1
    return v


def adj(a):
    return a.conjugate().T


def diss(j, x):
    a = adj(j) * j
    return adj(j) * x * j - (a * x + x * a) / 2


def poisson_entry(c, f, spectator, nu):
    """Integral exp((-|F|/2+i nu |F|)t)(1-exp(-t))^|spectator| dt."""
    w = f.bit_count()
    k = spectator.bit_count()
    return sum((-1)**j * math.comb(k, j) /
               (s.Rational(w, 2) + j-s.I*nu*w) for j in range(k + 1))


def check(nu):
    c = 2
    d = 4
    ident = s.eye(d)
    zero = s.zeros(d*d)
    # The order [11, 01, 10] selects a distinct write on each nonzero
    # syndrome of U = Hamming weight. Q_F is the corresponding X write.
    js = {f: unit(d, 0, f) for f in range(1, d)}
    source = {f: adj(j) * j for f, j in js.items()}
    assert all(source[f]*source[h] == s.zeros(d)
               for f, h in itertools.permutations(js, 2))
    a = {f: s.sqrt(s.Rational(f.bit_count(), c)) for f in js}
    t = zero.copy()
    g = zero.copy()
    for f, j in js.items():
        raise_f = unit(d, f, 0)
        term = a[f] * s.kronecker_product(j, raise_f)
        t += term + adj(term)
        gf = s.zeros(d)
        for spectator in range(d):
            if not (spectator & f):
                gf += poisson_entry(c, f, spectator,nu) * unit(d, f | spectator, spectator)
        term_g = a[f] * s.kronecker_product(j, gf)
        g += term_g + adj(term_g)
    # Independent single-qubit loss, including loss from intermediate flags.
    losses = []
    for bit in range(c):
        loss = s.zeros(d)
        for f in range(d):
            if f & (1 << bit):
                loss[f ^ (1 << bit), f] = 1
        losses.append(s.kronecker_product(ident, loss))
    number = s.kronecker_product(ident,s.diag(*(f.bit_count() for f in range(d))))
    def fast(x):
        return sum((diss(j, x) for j in losses), zero.copy())+s.I*nu*(number*x-x*number)
    def aa(x):
        return s.I*(g*x-x*g)
    def hh(x):
        return s.I*(t*x-x*t)
    assert s.simplify(fast(g)+t) == zero
    isometry = s.kronecker_product(ident, s.Matrix([1,0,0,0]))
    assert adj(isometry)*g*isometry == s.zeros(d)
    # Ad_W L Ad_W^dagger, W=exp(-i eps G): the first coefficient
    # vanishes on every data observable, on ALL controller states.
    checked = 0
    for u in range(d):
        for v in range(d):
            x = unit(d, u, v)
            xx = s.kronecker_product(x, ident)
            first = fast(aa(xx)) + hh(xx)
            assert s.simplify(first) == zero
            second = fast(aa(aa(xx)))/2 + hh(aa(xx))
            ground_second = adj(isometry)*second*isometry
            rate = s.Rational(4,c)/(1+4*nu**2)
            active = sum(source.values(),s.zeros(d))
            wanted = rate*(sum((diss(j, x) for j in js.values()), s.zeros(d))
                           -s.I*nu*(active*x-x*active))
            assert s.simplify(ground_second-wanted) == s.zeros(d)
            checked += 1
    # The actual coupler is bounded by one, not by the number of labels.
    esc = sum((a[f]**2*source[f] for f in js), s.zeros(d))
    assert esc == s.diag(0,s.Rational(1,2),s.Rational(1,2),1)
    # Coherently merging outcome labels changes escape and data dynamics.
    coherent = sum(js.values(), s.zeros(d))
    separate_escape = sum((adj(j)*j for j in js.values()), s.zeros(d))
    assert adj(coherent)*coherent != separate_escape
    assert diss(coherent, unit(d,0,1)) != sum((diss(j,unit(d,0,1)) for j in js.values()), s.zeros(d))
    # A single coherent reset has a dark vector. Independent bit loss has
    # only |00> in its simultaneous kernel, so no excited dark flag remains.
    coherent_reset = sum((unit(d,0,f) for f in js), s.zeros(d))
    dark = s.Matrix([0,1,-1,0])
    assert coherent_reset*dark == s.zeros(d,1)
    bit_losses = [j[0:d,0:d] for j in losses]
    common_kernel_dim = d-s.Matrix.vstack(*bit_losses).rank()
    assert common_kernel_dim == 1
    # The ground-to-F Poisson matrix element and all spectator terms are
    # independently checked above, rather than assuming just 2/|F|.
    out = {
        'controller_qubits':c, 'data_dimension':d,
        'data_operator_basis_size':checked,
        'exact_poisson_identity':True,
        'first_order_cancellation_on_all_controller_states':True,
        'dimensionless_detuning':str(nu),
        'ground_second_order_generator':'4/[c(1+4nu^2)] * (sum_F D[J_F] - i[-nu sum_F Pi_F, .])',
        'ground_second_order_rate':str(rate),
        'three_separate_outcomes':True,
        'exclusive_source_escape':str(esc),
        'coherent_sum_changes_generator':True,
        'coherent_reset_has_excited_dark_flag':True,
        'independent_bit_loss_common_kernel_dimension':int(common_kernel_dim),
        'scope':'Exact finite symbolic transducer identities; not an all-size theorem, novelty claim, or physical implementation',
        'program_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    return out


def main():
    out={'cases':[check(nu) for nu in (s.S(0),s.Rational(1,2))],
         'program_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    OUT.mkdir(parents=True,exist_ok=True)
    path = OUT/'transducer_algebra.json'
    path.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'output':str(path),'exact_basis_checks':sum(x['data_operator_basis_size'] for x in out['cases']),'passed':True}))


if __name__ == '__main__':
    main()
