"""Exact small-bond trial and a cold-Gibbs physical-product-frame barrier.

The ordinary spin-two AKLT tensor is only a variational trial for the
Heisenberg Hamiltonian.  No AKLT gap or thermodynamic-limit energy is used.
"""
import sys
sys.dont_write_bytecode = True
import sympy as S
import json, time
from fractions import Fraction
from positive_gate import BASE, spin


def aklt_tensors():
    # Clebsch-Gordan map virtual spin1 x spin1 -> physical spin2,
    # composed on the right with the virtual spin1 singlet matrix.
    A = [S.zeros(3) for _ in range(5)]
    entries = {
        -2: [(-1, -1, 1)],
        -1: [(-1, 0, 1/S.sqrt(2)), (0, -1, 1/S.sqrt(2))],
        0: [(-1, 1, 1/S.sqrt(6)), (0, 0, 2/S.sqrt(6)),
            (1, -1, 1/S.sqrt(6))],
        1: [(0, 1, 1/S.sqrt(2)), (1, 0, 1/S.sqrt(2))],
        2: [(1, 1, 1)]}
    for m, values in entries.items():
        for a, b, c in values:
            A[m+2][a+1, -b+1] = (-1)**(1-b)*c
    return A


def transfer_operators():
    A = aklt_tensors(); ms, z, plus, minus, _ = spin()
    h = S.kronecker_product(z, z)+(S.kronecker_product(plus, minus)+
                                  S.kronecker_product(minus, plus))/2
    E = sum((S.kronecker_product(a, a) for a in A), S.zeros(9))
    two = [a*b for a in A for b in A]
    F = S.zeros(9)
    for i in range(25):
        for j in range(25):
            if h[i, j]:
                F += h[i, j]*S.kronecker_product(two[i], two[j])
    E, F = E.applyfunc(S.simplify), F.applyfunc(S.simplify)
    assert all(x.is_Rational for x in list(E)+list(F))
    return A, h, E, F


def finite_trial(n):
    A, h, E, F = transfer_operators()
    norm = S.trace(E**n); energy = S.factor(S.trace(F*E**(n-2))/norm)
    assert norm > 0 and energy < -4
    # Independent physical-vector check of the same transfer ordering at n4.
    if n == 4:
        import itertools
        v = S.Matrix([S.trace(A[a]*A[b]*A[c]*A[d])
                      for a, b, c, d in itertools.product(range(5), repeat=4)])
        assert (v.T*v)[0] == norm
        # Applying each pair to the vector avoids another dense symbolic H.
        states = list(itertools.product(range(5), repeat=4))
        lookup = {q: i for i, q in enumerate(states)}
        Hv = S.zeros(625, 1)
        for col, q in enumerate(states):
            if v[col] == 0:
                continue
            for site in range(4):
                other = (site+1) % 4; pair = 5*q[site]+q[other]
                for out in range(25):
                    if h[out, pair]:
                        p = list(q); p[site], p[other] = divmod(out, 5)
                        Hv[lookup[tuple(p)]] += h[out, pair]*v[col]
        direct = S.simplify((v.T*Hv)[0]/norm/4)
        assert S.simplify(direct-energy) == 0
    return dict(n=n, norm=str(norm), energy_per_bond=str(energy),
                energy_per_bond_float=float(energy)), energy


def run():
    start = time.monotonic(); small, _ = finite_trial(4)
    block, energy = finite_trial(16)
    _, _, E, F = transfer_operators()
    assert E*F == F*E
    eigenvalues = E.eigenvals()
    assert eigenvalues == {S.Rational(5, 3): 1, S.Rational(-5, 6): 3,
                          S.Rational(1, 6): 5}
    weights = []
    for value, multiplicity in eigenvalues.items():
        P = S.eye(9)
        for other in eigenvalues:
            if other != value:
                P = P*(E-other*S.eye(9))/(value-other)
        assert P*P == P and S.trace(P) == multiplicity
        weights.append(dict(eigenvalue=str(value), multiplicity=multiplicity,
                            energy_insertion_trace=str(S.trace(P*F))))
    assert {r['eigenvalue']:r['energy_insertion_trace'] for r in weights} == {
        '5/3':'-25/2', '-5/6':'-15', '1/6':'-5/2'}
    def exact_energy(n):
        a, b = S.Rational(1, 2)**n, S.Rational(1, 10)**n
        return -S.Rational(9, 2)*(1+S.Rational(24, 5)*a+20*b)/(1+3*a+5*b)
    assert exact_energy(4) == S.Rational(small['energy_per_bond'])
    assert exact_energy(16) == energy
    # Translation-average the finite periodic trial before cutting one bond.
    # SO3-twirl each block: all one-spin means vanish and each internal bond
    # energy is unchanged.  Independently twirled blocks have zero cross energy.
    tiled = S.Rational(15, 16)*energy
    log5_upper = S.Rational(161, 100)
    # A finite positive Taylor partial sum proves exp(1.61)>5 exactly.
    partial = sum(log5_upper**k/S.factorial(k) for k in range(13))
    assert partial > 5
    rows = []
    for n, beta in ((64, 64), (128, 64), (256, 96)):
        assert n % 16 == 0
        # Exact finite-ring transfer formula is stronger than block tiling.
        direct_energy = exact_energy(n)
        assert direct_energy < -S.Rational(9, 2)
        upper = -S.Rational(9, 2)+log5_upper/beta
        gap = -4-upper; assert gap > 0
        rows.append(dict(ring_sites=n, beta=beta,
            legitimate_block_tiled_trial_energy_per_bond=str(tiled),
            direct_finite_ring_AKLT_trial_energy_per_bond=str(direct_energy),
            Gibbs_energy_per_bond_upper=str(upper),
            Gibbs_energy_per_bond_upper_float=float(upper),
            trace_distance_from_every_fully_separable_state_lower=str(gap/10),
            trace_distance_lower_float=float(gap/10)))
    result = dict(status='EXACT_FINITE_TRIAL_AND_COLD_GIBBS_PRODUCT_PHYSICAL_FRAME_BARRIER',
        ordinary_trial='Spin2 AKLT Clebsch-Gordan MPS, virtual dimension3; not a Heisenberg Gibbs representation.',
        independent_four_site_replay=small, finite_periodic_block=block,
        exact_transfer_spectral_weights=weights,
        all_even_ring_variational_energy_formula='-(9/2)*(1+(24/5)*2^(-n)+20*10^(-n))/(1+3*2^(-n)+5*10^(-n)) < -9/2 for every even n>=4',
        log5_rational_upper=str(log5_upper), exp_lower_Taylor_terms=13,
        rows=rows,
        derivation='Free-energy variational principle gives U_beta/n <= E_trial/n + log(5)/beta. Every fully separable spin2 state has H/n >= -4. The energy spectral interval [-6n,4n] converts the separation to trace distance divided by10.',
        excluded='Any compression that reconstructs the normalized cold Gibbs state as a nonnegative mixture of one-spin PSD product states to smaller trace distance.',
        not_excluded='Entangled block frames, MPOs, nonphysical matrix-unit worldline tensors, or a task-specific representation that computes only scalar traces.',
        scope='Every even periodic ring n>=4 has the same simple energy and trace-distance bounds at the indicated beta. The listed direct finite-ring trials and the weaker block-tiling construction are also acquired. No zero-temperature gap, cold partition function, or bootstrap purity is acquired.',
        elapsed_seconds=time.monotonic()-start)
    (BASE/'results/PHYSICAL_FRAME_BARRIER.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    run()
