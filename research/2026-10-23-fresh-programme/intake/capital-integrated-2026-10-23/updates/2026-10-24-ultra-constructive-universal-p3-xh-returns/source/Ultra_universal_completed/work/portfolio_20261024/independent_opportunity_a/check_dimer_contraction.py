#!/usr/bin/env python3
"""Exact finite replay of signs, acquired gauge, polymer gas and filtered norms.

Small-fixture matching enumeration is exhaustive. The generic acquisition proof
uses a polynomial weighted-perfect-matching routine instead. This is not a
materials benchmark or execution of an unrestricted projected-state sampler.
"""
from collections import defaultdict
from decimal import Decimal, localcontext
from fractions import Fraction as Q
from functools import lru_cache
from itertools import combinations, product
import json
from pathlib import Path

from check_phase_identity import det


def pmatch(f, sites):
    sites = tuple(sorted(sites))
    if not sites:
        yield ()
        return
    i = sites[0]
    for j in sites[1:]:
        if f[i][j]:
            for rest in pmatch(f, [v for v in sites if v not in (i, j)]):
                yield ((i, j),) + rest


def coeff(f, matching):
    out = Q(1)
    for i, j in matching:
        out *= f[i][j]
    return out


def create(mask, index):
    if mask >> index & 1:
        return None
    return mask | (1 << index), (-1) ** ((mask & ((1 << index) - 1)).bit_count())


@lru_cache(None)
def bond_state(matching):
    state = {0: 1}
    for i, j in matching:
        new = defaultdict(int)
        for mask, value in state.items():
            for a, b, sign in ((2*i, 2*j+1, 1), (2*i+1, 2*j, -1)):
                right = create(mask, b)
                if right is None:
                    continue
                left = create(right[0], a)
                if left is not None:
                    new[left[0]] += value * sign * right[1] * left[1]
        state = dict(new)
    sites = sorted(v for edge in matching for v in edge)
    answer = {}
    for fermion, value in state.items():
        assert all(((fermion >> (2*i)) & 3) in (1, 2) for i in sites)
        spin = sum(((fermion >> (2*i)) & 1) << i for i in sites)
        answer[spin] = value
    assert sum(x*x for x in answer.values()) == 2 ** len(matching)
    return answer


def inner(a, b):
    return sum((value * b.get(mask, 0) for mask, value in a.items()), Q(0))


def apply_pauli(state, site, pauli):
    if pauli == 'X':
        return {mask ^ (1 << site): value for mask, value in state.items()}
    if pauli == 'Z':
        return {mask: value * (1 if mask >> site & 1 else -1)
                for mask, value in state.items()}
    raise ValueError('finite exact real checker supports X/Z only')


def filtered(state, filters):
    out = dict(state)
    for site, pauli, strength in filters:
        changed = apply_pauli(out, site, pauli)
        new = defaultdict(Q)
        for mask, value in out.items():
            new[mask] += value
        for mask, value in changed.items():
            new[mask] += strength * value
        out = {mask: value for mask, value in new.items() if value}
    return out


def state(f):
    out = defaultdict(Q)
    for matching in pmatch(f, range(len(f))):
        weight = coeff(f, matching)
        for mask, value in bond_state(matching).items():
            out[mask] += weight * value
    return {mask: value for mask, value in out.items() if value}


def pairing_graph(f, reference):
    owner = {v: a for a, edge in enumerate(reference) for v in edge}
    ref = {tuple(sorted(edge)) for edge in reference}
    graph = [set() for _ in reference]
    for i in range(len(f)):
        for j in range(i+1, len(f)):
            if f[i][j] and (i, j) not in ref:
                assert owner[i] != owner[j]
                graph[owner[i]].add(owner[j])
                graph[owner[j]].add(owner[i])
    return owner, ref, graph


def connected(mask, graph):
    if not mask:
        return False
    start = (mask & -mask).bit_length()-1
    seen, queue = {start}, [start]
    for v in queue:
        for w in graph[v]:
            if mask >> w & 1 and w not in seen:
                seen.add(w)
                queue.append(w)
    return len(seen) == mask.bit_count()


def local_activity(f, reference, support, filters=()):
    owner, ref, _ = pairing_graph(f, reference)
    cells = [a for a in range(len(reference)) if support >> a & 1]
    sites = {v for a in cells for v in reference[a]}
    local_filters = tuple(item for item in filters if item[0] in sites)
    base_match = tuple(reference[a] for a in cells)
    base = filtered(bond_state(base_match), local_filters)
    z0 = inner(base, base)
    matchings = list(pmatch(f, sites))
    spin = {p: filtered(bond_state(p), local_filters) for p in matchings}
    weights = {p: coeff(f, p) for p in matchings}
    answer = Q(0)
    for p in matchings:
        for q in matchings:
            graph = [set() for _ in reference]
            active = 0
            for i, j in p+q:
                if (i, j) not in ref:
                    a, b = owner[i], owner[j]
                    graph[a].add(b)
                    graph[b].add(a)
                    active |= (1 << a) | (1 << b)
            if active == support and connected(support, graph):
                answer += weights[p] * weights[q] * inner(spin[p], spin[q]) / z0
    return answer


def poly_mul(a, b, degree):
    out = [Q(0)] * (degree+1)
    for i, ai in enumerate(a):
        for j, bj in enumerate(b[:degree+1-i]):
            out[i+j] += ai*bj
    return out


def log_poly(a, degree):
    assert a[0] == 1
    b = list(a)
    b[0] = 0
    power = [Q(1)] + [Q(0)]*degree
    out = [Q(0)] * (degree+1)
    for j in range(1, degree+1):
        power = poly_mul(power, b, degree)
        for k, value in enumerate(power):
            out[k] += Q((-1)**(j+1), j) * value
    return out


def submasks(mask):
    sub = mask
    while True:
        yield sub
        if not sub:
            break
        sub = (sub-1) & mask


def polymer_data(f, reference, filters=(), degree=6):
    m = len(reference)
    _, _, graph = pairing_graph(f, reference)
    weights = {mask: local_activity(f, reference, mask, filters)
               for mask in range(1, 1 << m)
               if 2 <= mask.bit_count() <= degree and connected(mask, graph)}
    base = filtered(bond_state(tuple(reference)), filters)
    z0 = inner(base, base)

    @lru_cache(None)
    def gas(mask):
        if not mask:
            return [Q(1)] + [Q(0)]*degree
        v = mask & -mask
        out = list(gas(mask ^ v))
        for component, weight in weights.items():
            if component & v and component & mask == component:
                size = component.bit_count()
                rest = gas(mask ^ component)
                for j in range(degree+1-size):
                    out[j+size] += weight*rest[j]
        return out

    # The whole-gas and connected-set computations are separate exact routes.
    full = gas((1 << m)-1)
    full_log = log_poly(full, degree)
    connected_log = [Q(0)]*(degree+1)
    for support in range(1, 1 << m):
        if support.bit_count() > degree or not connected(support, graph):
            continue
        for sub in submasks(support):
            sign = (-1)**(support.bit_count()-sub.bit_count())
            lp = log_poly(gas(sub), degree)
            for j, value in enumerate(lp):
                connected_log[j] += sign*value
    assert connected_log == full_log
    return z0, weights, full, full_log


def norm_from_polymer(f, reference, filters=()):
    m = len(reference)
    z0, weights, polynomial, _ = polymer_data(f, reference, filters, degree=max(m, 1))
    answer = z0*sum(polynomial)
    direct = filtered(state(f), filters)
    assert answer == inner(direct, direct)
    return answer, weights


def power2(k):
    return Q(2**k) if k >= 0 else Q(1, 2**(-k))


def ceil_log2(q):
    assert q > 0
    k = q.numerator.bit_length()-q.denominator.bit_length()
    while power2(k) < q:
        k += 1
    while power2(k-1) >= q:
        k -= 1
    return k


def floor_log2(q):
    k = ceil_log2(q)
    return k if power2(k) == q else k-1


def acquire_gauge(f):
    # Exact small-fixture substitute for a weighted perfect-matching algorithm.
    all_matchings = list(pmatch(f, range(len(f))))
    reference = max(all_matchings, key=lambda p: abs(coeff(f, p)))
    owner, ref, graph = pairing_graph(f, reference)
    degree = max(map(len, graph), default=0)
    delta = max(sum(bool(f[i][j]) and (min(i,j), max(i,j)) not in ref
                    for j in range(len(f))) for i in range(len(f)))
    if not degree:
        raise ValueError('product case not used in this gauge fixture')
    target = Q(1, 384*degree)
    sigma, base = {}, {}
    for i, j in reference:
        sigma[i], sigma[j] = 1, -1
        base[i], base[j] = Q(1), 1/f[i][j]
    threshold = floor_log2(target/(2*delta))
    edges = []
    literal = lambda a, s: 2*a + (s == -1)
    for i in range(len(f)):
        for j in range(i+1, len(f)):
            if not f[i][j] or (i, j) in ref:
                continue
            rhs = threshold-ceil_log2(abs(base[i]*base[j]*f[i][j]))
            a, b = owner[i], owner[j]
            edges += [(literal(b,-sigma[j]), literal(a,sigma[i]), rhs),
                      (literal(a,-sigma[i]), literal(b,sigma[j]), rhs)]
    potentials = [0]*len(f)
    for iteration in range(len(f)):
        changed = False
        for source, target_node, weight in edges:
            if potentials[target_node] > potentials[source]+weight:
                potentials[target_node] = potentials[source]+weight
                changed = True
        if not changed:
            break
    else:
        raise ValueError('UNKNOWN: negative signed-constraint cycle')
    exponents = [int((Q(potentials[2*a]-potentials[2*a+1],2)+Q(1,2))//1)
                 for a in range(len(reference))]
    diagonal = [base[i]*power2(sigma[i]*exponents[owner[i]]) for i in range(len(f))]
    transformed = [[diagonal[i]*f[i][j]*diagonal[j] for j in range(len(f))]
                   for i in range(len(f))]
    assert all(transformed[i][j] == 1 for i,j in reference)
    rho = max(sum(abs(transformed[i][j]) for j in range(len(f))
                  if (min(i,j),max(i,j)) not in ref) for i in range(len(f)))
    assert rho <= target
    return transformed, reference, diagonal, rho, degree


def validate_state_map(f):
    n, k = len(f), len(f)//2
    psi = state(f)
    z = Q(0)
    for subset in combinations(range(n), k):
        other = [i for i in range(n) if i not in subset]
        value = det([[f[i][j] for j in other] for i in subset])
        inversion = sum(j<i for i in subset for j in other)
        expected = (-1)**(k*(k-1)//2+inversion)*value
        mask = sum(1 << i for i in subset)
        assert psi.get(mask,0) == expected
        z += value*value
    assert z == inner(psi,psi)
    return z


def decimal(q):
    return Decimal(q.numerator)/Decimal(q.denominator)


def main():
    # First witness: genuinely signed connected activity, exact determinant map.
    lam = Q(1,10000)
    f = [[Q(0),1,lam,0],[1,0,0,lam],[lam,0,0,1],[0,lam,1,0]]
    f = [[Q(v) for v in row] for row in f]
    reference = ((0,1),(2,3))
    z = validate_state_map(f)
    gas_z, weights = norm_from_polymer(f,reference)
    assert z == gas_z == 4*(1-lam**2+lam**4)
    assert weights[3] == -lam**2+lam**4 < 0

    # Second witness: raw entries fail a tiny-coupling test, native gauge passes.
    raw = [[Q(0),1,1,0],[1,0,0,Q(1,10**8)],
           [1,0,0,1],[0,Q(1,10**8),1,0]]
    raw = [[Q(v) for v in row] for row in raw]
    scaled, ref, diagonal, rho, d = acquire_gauge(raw)
    scalar = Q(1)
    for value in diagonal:
        scalar *= value
    assert validate_state_map(scaled) == scalar**2*validate_state_map(raw)
    norm_from_polymer(scaled,ref)

    # Coupled square of four dimers, rather than only a disjoint product.
    n=8
    square = [[Q(0) for _ in range(n)] for _ in range(n)]
    ref_square = tuple((2*a,2*a+1) for a in range(4))
    for i,j in ref_square:
        square[i][j]=square[j][i]=Q(1)
    for a,b in ((0,1),(1,2),(2,3),(3,0)):
        for parity in (0,1):
            i,j=2*a+parity,2*b+parity
            square[i][j]=square[j][i]=lam
    exact = validate_state_map(square)
    polymer_norm, square_weights = norm_from_polymer(square,ref_square)
    assert polymer_norm == exact

    # Positive local-filter norms recover even observables whose reference
    # expectation is zero. This checks the operation, not arbitrary conditionals.
    psi=state(square)
    t=Q(1,20)
    p=2*t/(1+t*t)
    observables={}
    for sites,paulis in (((0,2),('X','X')),((0,2),('Z','Z')),((0,),('X',))):
        numerator=Q(0)
        for signs in product((-1,1),repeat=len(sites)):
            filters=tuple((i,pauli,t*sign) for i,pauli,sign in zip(sites,paulis,signs))
            norm,_=norm_from_polymer(square,ref_square,filters)
            sign_product=1
            for sign in signs:
                sign_product*=sign
            numerator+=sign_product*norm
        estimate=numerator/(2**len(sites)*(1+t*t)**len(sites)*p**len(sites)*exact)
        transformed=dict(psi)
        for i,pauli in zip(sites,paulis):
            transformed=apply_pauli(transformed,i,pauli)
        direct=inner(psi,transformed)/exact
        assert estimate==direct
        observables[str(tuple(zip(sites,paulis)))]=str(direct)

    # Repeated polymers/cumulants and actual truncated-log error.
    _,_,_,log_coeff=polymer_data(square,ref_square,degree=8)
    rho_square=2*lam
    kappa4=Q(21,19)**4
    h=(2*rho_square+rho_square**2)*kappa4
    beta=0
    while 4*2*3**(beta+2)*h <= Q(1,2):
        beta+=1
    assert beta>=1
    truncations=[]
    with localcontext() as context:
        context.prec=70
        log_exact=decimal(exact/16).ln()
        for cut in (2,3,4,5,6,7,8):
            truncated=sum(log_coeff[:cut])
            error=abs(decimal(truncated)-log_exact)
            bound=Decimal(4)*(-Decimal(beta*cut)).exp()
            assert error<=bound
            truncations.append({'cut':cut,'actual_log_error':str(error),
                                'certified_KP_bound':str(bound)})
    result={'scope':'EXACT_FINITE_MAPPING_GAUGE_POLYMER_FILTER_CHECK',
            'signed_two_dimer_activity':str(weights[3]),
            'gauge':{'reference':ref,'diagonal':[str(v) for v in diagonal],
                     'certified_rho':str(rho),'contracted_degree':d,
                     'native_row_max':'1','normalization_scalar':str(scalar)},
            'coupled_square':{'n':n,'normalizer':str(exact),
                              'nonzero_polymers':sum(bool(v) for v in square_weights.values()),
                              'observables':observables,'filtered_beta':beta,
                              'truncated_log_checks':truncations},
            'all_checks_passed':True,
            'limits':'Small exact fixtures only; no general sampler, physical experiment, or speed comparison.'}
    path=Path(__file__).with_name('DIMER_CONTRACTION_CHECK.json')
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
