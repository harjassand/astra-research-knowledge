#!/usr/bin/env python3
"""Exact rational seeded inverse-mass constructor; no floating point or external solver.

The receiving routine re-derives the mathematical certificate from raw reactions.
It does NOT independently certify search-accounting transcripts. That distinction
is deliberate. A profile cap limits profile evaluations, not input/bit/memory cost.
"""
from fractions import Fraction as F
from itertools import product, permutations
from math import prod, isqrt
import hashlib
import json


def rat(x):
    if type(x) is int or type(x) is F:
        return F(x)
    raise TypeError('exact int or Fraction required; bool/float/string rejected')


def positive_int(x):
    if type(x) is not int or x < 1:
        raise ValueError('positive integer required')
    return x


def ceilq(x):
    return -(-x.numerator // x.denominator)


def ceilsqrt(x):
    k = isqrt(x.numerator // x.denominator)
    return k if k*k*x.denominator >= x.numerator else k+1


def encode(x):
    if type(x) is F:
        return str(x)
    if isinstance(x, dict):
        return {str(k): encode(v) for k, v in x.items()}
    if isinstance(x, (tuple, list)):
        return [encode(v) for v in x]
    return x


def canonical(x):
    return json.dumps(encode(x), sort_keys=True, separators=(',', ':'))


def peak_bits(x):
    if type(x) is F:
        return max(abs(x.numerator).bit_length(), x.denominator.bit_length())
    if type(x) is int:
        return abs(x).bit_length()
    if isinstance(x, dict):
        return max([0]+[peak_bits(v) for v in x.values()])
    if isinstance(x, (list, tuple)):
        return max([0]+[peak_bits(v) for v in x])
    return 0


def recognize(raw):
    """Acquire the unique open species; aggregate positive channels; check WR.

    No source record, decomposition, or good weight is accepted on trust.
    Null reactions are discarded after strict input validation.
    """
    if type(raw) not in (list, tuple) or not raw:
        raise ValueError('nonempty reaction list required')
    n = None
    aggregate = {}
    for row in raw:
        if type(row) not in (tuple, list) or len(row) != 3:
            raise ValueError('reaction must be (source,target,rate)')
        u, v, k = row
        if type(u) not in (list, tuple) or type(v) not in (list, tuple):
            raise TypeError('complexes must be lists or tuples')
        if n is None:
            n = len(u)
        if n < 2 or len(u) != n or len(v) != n:
            raise ValueError('consistent dimension n>=2 required')
        if any(type(a) is not int or a < 0 for a in tuple(u)+tuple(v)):
            raise ValueError('nonnegative integer complexes required')
        k = rat(k)
        if k <= 0:
            raise ValueError('strictly positive rates required')
        u, v = tuple(u), tuple(v)
        if u != v:
            aggregate[u, v] = aggregate.get((u, v), F(0))+k
    channels = tuple((u, v, k) for (u, v), k in sorted(aggregate.items()))
    zero = (0,)*n
    nonconservative = [(u, v, k) for u, v, k in channels if sum(u) != sum(v)]
    opens = []
    for a in range(n):
        e = tuple(int(i == a) for i in range(n))
        if len(nonconservative) == 2 and set((u,v) for u,v,k in nonconservative) == {(zero,e),(e,zero)}:
            opens.append(a)
    if len(opens) != 1:
        raise ValueError('exactly one immigration/death open coordinate required')
    a = opens[0]
    e = tuple(int(i == a) for i in range(n))
    lam, mu = aggregate[zero,e], aggregate[e,zero]
    internals = []
    for u, v, k in channels:
        if sum(u) != sum(v):
            continue
        if u[a] < 1 or v[a] < 1 or not 2 <= sum(u) <= 3:
            raise ValueError('internals must share one A and leave unary/binary conservative channels')
        us = tuple(z-int(i == a) for i,z in enumerate(u))
        vs = tuple(z-int(i == a) for i,z in enumerate(v))
        internals.append((us,vs,k))
    graph = {}
    for u,v,k in channels:
        graph.setdefault(u,set()).add(v)
        graph.setdefault(v,set())
    edge_visits = 0
    for u,v,k in channels:
        seen, todo = {v}, [v]
        while todo:
            z = todo.pop()
            for q in sorted(graph[z]):
                edge_visits += 1
                if q not in seen:
                    seen.add(q)
                    todo.append(q)
        if u not in seen:
            raise ValueError('raw graph is not weakly reversible')
    raw_hash = hashlib.sha256(canonical(channels).encode()).hexdigest()
    return dict(n=n, a=a, satellites=tuple(i for i in range(n) if i != a),
                lam=lam, mu=mu, channels=channels, internals=tuple(internals),
                raw_sha256=raw_hash, input_rows=len(raw), graph_edge_visits=edge_visits)


def derive(rec, t, weights):
    """Private working-record constructor. Public receive re-recognizes raw input."""
    t = rat(t)
    if t <= 1:
        raise ValueError('t>1 required')
    weights = tuple(map(rat, weights))
    if len(weights) != rec['n']-1 or any(not 0 <= w <= 1 for w in weights):
        raise ValueError('one weight in [0,1] per satellite required')
    n, a, js = rec['n'], rec['a'], rec['satellites']
    v = [F(0)]*n
    v[a] = F(1)
    for j,w in zip(js,weights):
        v[j] = w
    deltas = [sum(v[i]*(q[i]-u[i]) for i in range(n)) for u,q,k in rec['internals']]
    ell = 1+max([F(0)]+list(map(abs,deltas)))
    gamma = {}
    for (u,q,k),d in zip(rec['internals'],deltas):
        gamma[u] = gamma.get(u,F(0))+k*(d/ell if d >= 0 else ell*d)
    unit = lambda j, c=1: tuple(c*int(i == j) for i in range(n))
    us = tuple(gamma.get(unit(j,2),F(0)) for j in js)
    reasons = []
    if any(u <= 0 for u in us):
        reasons.append('nonpositive pure satellite effective coefficient')
    for j,k in [(j,k) for j in js for k in js if j < k]:
        z = tuple(int(i == j)+int(i == k) for i in range(n))
        if gamma.get(z,F(0)) < 0:
            reasons.append('negative mixed satellite effective coefficient')
    base = dict(t=t, weights=weights, ell=ell,
                source_coefficients=tuple((u,gamma[u]) for u in sorted(gamma)), pure=us)
    if reasons:
        return dict(status='PROFILE_REJECTED', reasons=reasons, **base)
    K1 = max([F(0)]+[-g for u,g in gamma.items() if sum(u) == 1])
    K2 = max([F(0)]+[-g for u,g in gamma.items() if sum(u) == 2 and u[a] > 0])
    K0 = K1+K2
    K = K0+sum((u+K0)**2/(2*u) for u in us)
    D = rec['mu']*(1-1/t)
    c = min(F(1),D/(4*K))
    C = rec['lam']*(t-1)+3*rec['mu']+D
    zeta = min(rec['lam']/4,D/4,F(1))
    S = sum(w*w/u for w,u in zip(weights,us))
    strength = c/(4*(1+c)*S) if S else None
    derived = dict(K1=K1,K2=K2,K=K,D=D,c=c,C=C,zeta=zeta,S=S,head_strength=strength)
    if S and strength < C+zeta:
        return dict(status='PROFILE_REJECTED', reasons=['finite-head compatibility failed'], **base, **derived)
    Acut = max(2,ceilq(4*(C+zeta)/(3*D)))
    Ttail = 9*Acut*Acut/S if S else 2*(1+c)*(C+zeta)*Acut*Acut/c
    Bcuts = tuple(max(1,ceilsqrt(Ttail/u)) for u in us)
    exception_states = (Acut-1)*prod(Bcuts)
    Nmax = Acut-1+sum(b-1 for b in Bcuts)
    h0 = 2*t*(1+c)
    prefactor = (C+zeta)*h0
    # Conservative binary bit bounds for the unexpanded rational Foster constant.
    num_bits = abs(prefactor.numerator).bit_length()+Nmax*t.numerator.bit_length()
    den_bits = prefactor.denominator.bit_length()+Nmax*t.denominator.bit_length()
    return dict(status='CERTIFIED_REQUESTED_T_MOMENT', raw_sha256=rec['raw_sha256'],
                dimension=n, open_coordinate=a, satellite_coordinates=js,
                **base, **derived, A_cut=Acut, B_cuts=Bcuts, tail_threshold=Ttail,
                exception_states_not_enumerated=exception_states, N_max=Nmax, h0=h0,
                foster_constant_factored=dict(prefactor=prefactor,base=t,exponent=Nmax,
                    expanded_numerator_bits_upper=num_bits,expanded_denominator_bits_upper=den_bits),
                guarantee='classwise positive recurrence and stationary t^N moment; not automatically all t')


def receive(raw, t, weights, certificate):
    """Strict semantic equality against raw re-derivation, not an acquisition audit."""
    expected = encode(derive(recognize(raw),t,weights))
    if expected['status'] != 'CERTIFIED_REQUESTED_T_MOMENT':
        return False
    return type(certificate) is dict and canonical(certificate) == canonical(expected)


def generic_search(raw, t, max_profiles):
    positive_int(max_profiles)
    rec = recognize(raw)
    t = rat(t)
    if t <= 1:
        raise ValueError('t>1 required')
    m, count, q, bits = rec['n']-1,0,1,peak_bits(rec)
    while True:
        for ks in product(range(q+1),repeat=m):
            if count == max_profiles:
                return dict(status='UNKNOWN', reason='profile cap; not a stability or certificate nonexistence conclusion',
                    acquisition=dict(route='rational grid', profiles=count, source_term_evaluations=count*len(rec['internals']),
                                     repeated_profiles_charged=True, last_denominator=q, retained_rational_peak_bits=bits,
                                     cap_scope='profile count only; not total bit/preprocessing/memory cost'))
            ws = tuple(F(k,q) for k in ks)
            cert = derive(rec,t,ws)
            count += 1
            bits = max(bits,peak_bits(cert))
            if cert['status'] == 'CERTIFIED_REQUESTED_T_MOMENT':
                return dict(status='CERTIFIED',certificate=cert,
                    acquisition=dict(route='rational grid',profiles=count,source_term_evaluations=count*len(rec['internals']),
                        repeated_profiles_charged=True,last_denominator=q,retained_rational_peak_bits=bits,
                        recognition_input_rows=rec['input_rows'],recognition_graph_edge_visits=rec['graph_edge_visits'],
                        cap_scope='profile count only; not total bit/preprocessing/memory cost'))
        q += 1


def hard_match(rec):
    if rec['n'] != 3 or len(rec['internals']) != 6:
        return None
    a = rec['a']
    mapping = {(u,v):k for u,v,k in rec['internals']}
    for b,c in permutations(rec['satellites']):
        def vec(aa,bb,cc):
            out = [0]*3
            out[a],out[b],out[c] = aa,bb,cc
            return tuple(out)
        pairs = [(vec(1,1,0),vec(0,1,1)),(vec(1,0,1),vec(0,2,0)),(vec(0,1,1),vec(0,0,2))]
        keys = [z for u,v in pairs for z in [(u,v),(v,u)]]
        if set(keys) == set(mapping):
            return b,c,tuple(mapping[z] for z in keys)
    return None


def hard_search(raw, t, max_profiles):
    """Raw-skeleton acquired halving, with proved finite all-positive-rate termination."""
    positive_int(max_profiles)
    rec = recognize(raw)
    t = rat(t)
    if t <= 1:
        raise ValueError('t>1 required')
    match = hard_match(rec)
    if match is None:
        return dict(status='UNKNOWN',reason='not the proved halving skeleton')
    b,cc,rates = match
    a1,b1,a2,b2,a3,b3 = rates
    eta0 = min(F(1,4),b1/(4*a3))
    Kmax, umin, umax, v0 = 2*max(a1,a2),b2/4,b2/2,b3/2
    Kbar = eta0*(Kmax+(umax+Kmax)**2/(2*umin))+Kmax*Kmax/(2*v0)+Kmax*eta0+v0*eta0*eta0/2
    D = rec['mu']*(1-1/t)
    C = rec['lam']*(t-1)+3*rec['mu']+D
    zeta = min(rec['lam']/4,D/4,F(1))
    c0 = min(F(1),D/(4*Kbar))
    eta_req = c0*umin/(8*(C+zeta))
    # Proved trial bound is acquired as exact rational halvings; this is separate
    # charged preprocessing, NOT covered by the candidate profile cap.
    guaranteed_trials, z = 1,eta0
    while z > eta_req:
        guaranteed_trials += 1
        z /= 2
    eta, trials, bits = eta0,[],peak_bits([rec,Kbar,c0,eta_req,z])
    for trial in range(1,max_profiles+1):
        ws = tuple(eta if j == b else F(0) for j in rec['satellites'])
        cert = derive(rec,t,ws)
        if cert.get('K',F(0)) > Kbar/eta:
            raise AssertionError('proved K bound violated')
        trials.append(dict(eta=eta,certificate_status=cert['status'],head_strength=cert.get('head_strength')))
        bits = max(bits,peak_bits(cert))
        acquisition = dict(route='recognized mediated triangle halving',profiles=trial,
            source_term_evaluations=trial*len(rec['internals']),trials=trials,
            guaranteed_trials=guaranteed_trials,guarantee_bound_halvings=guaranteed_trials-1,
            eta0=eta0,eta_required_sufficient=eta_req,Kbar=Kbar,c0=c0,
            retained_rational_peak_bits=bits,recognition_input_rows=rec['input_rows'],
            recognition_graph_edge_visits=rec['graph_edge_visits'],
            cap_scope='profile count only; does not cap termination-bound preprocessing or bit/memory cost',
            all_t_qualitative='proved termination for every rational t>1; hence every finite exponential stationary moment')
        if cert['status'] == 'CERTIFIED_REQUESTED_T_MOMENT':
            return dict(status='CERTIFIED',certificate=cert,acquisition=acquisition,
                        qualitative=_hard_structural_rec(rec,match))
        if eta <= eta_req:
            raise AssertionError('proved halving termination failed')
        eta /= 2
    return dict(status='UNKNOWN',reason='quantitative profile cap before certified head compatibility',
                acquisition=acquisition,qualitative=_hard_structural_rec(rec,match))


def hard_structural(raw):
    """Qualitative theorem receiver: no eta, t, Foster constants, or tail box.

    The reusable theorem proves all-rate halving termination. Per-instance
    qualitative acquisition therefore needs only exact recognition, not its
    potentially enormous quantitative witness. Failure means UNKNOWN.
    """
    rec = recognize(raw)
    match = hard_match(rec)
    if match is None:
        return dict(status='UNKNOWN',reason='not the proved halving skeleton')
    return _hard_structural_rec(rec,match)


def _hard_structural_rec(rec,match):
    b,c,rates = match
    return dict(status='CERTIFIED_ALL_FINITE_EXPONENTIAL_MOMENTS',
        raw_sha256=rec['raw_sha256'],open_coordinate=rec['a'],mediator_coordinate=b,
        other_satellite_coordinate=c,dimension=rec['n'],
        guarantee='every closed communicating class positive recurrent; every stationary exp(theta*N) moment finite, theta>0',
        numerical_foster_constants_provided=False,profile_evaluations=0,
        recognition_input_rows=rec['input_rows'],recognition_graph_edge_visits=rec['graph_edge_visits'],
        candidate_orientations_upper_bound=2)


def receive_structural(raw, certificate):
    expected = encode(hard_structural(raw))
    return (expected['status'] == 'CERTIFIED_ALL_FINITE_EXPONENTIAL_MOMENTS'
            and type(certificate) is dict and canonical(certificate) == canonical(expected))


def ff(x,u):
    if any(a < b for a,b in zip(x,u)):
        return 0
    return prod(prod(range(a-b+1,a+1)) for a,b in zip(x,u))


def check_state(raw, certificate, x):
    """Exact original generator and analytical upper bound; no large t^N expansion."""
    rec = recognize(raw)
    a,js = rec['a'],rec['satellites']
    t,c = certificate['t'],certificate['c']
    ws = certificate['weights']
    if len(x) != rec['n'] or any(type(z) is not int or z < 0 for z in x):
        raise ValueError('invalid state')
    def h(z):
        return certificate['h0'] if z[a] == 0 else 1+c/(z[a]+sum(w*z[j] for w,j in zip(ws,js)))
    hx = h(x)
    quotient, internal = F(0),F(0)
    for u,v,k in rec['channels']:
        rate = k*ff(x,u)
        if not rate:
            continue
        xp = tuple(xx-uu+vv for xx,uu,vv in zip(x,u,v))
        term = rate*(t**(sum(v)-sum(u))*h(xp)/hx-1)
        quotient += term
        if sum(v) == sum(u):
            internal += term
    A = x[a]
    if A == 0:
        assert internal == 0 and quotient <= -rec['lam']/2
        upper = -rec['lam']/2
    else:
        R = A+sum(w*x[j] for w,j in zip(ws,js))
        Q = sum(u*x[j]**2 for u,j in zip(certificate['pure'],js))
        negative = c*A*Q/(2*(1+c)*R*R)
        assert internal <= c*certificate['K']*A-negative
        upper = certificate['C']-3*certificate['D']*A/4-negative
        assert quotient <= upper
    outside = (A == 0 or A >= certificate['A_cut'] or any(x[j] >= cut for j,cut in zip(js,certificate['B_cuts'])))
    if outside:
        assert quotient <= -certificate['zeta']
    return quotient,upper,outside


def hard_raw(rates=(1,1,1,1,1,1,2,1)):
    lam,mu,a1,b1,a2,b2,a3,b3 = map(rat,rates)
    return [((0,0,0),(1,0,0),lam),((1,0,0),(0,0,0),mu),
            ((2,1,0),(1,1,1),a1),((1,1,1),(2,1,0),b1),
            ((2,0,1),(1,2,0),a2),((1,2,0),(2,0,1),b2),
            ((1,1,1),(1,0,2),a3),((1,0,2),(1,1,1),b3)]


if __name__ == '__main__':
    print(json.dumps(encode(hard_search(hard_raw(),F(2),100)),indent=2,sort_keys=True))
