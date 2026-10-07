"""Exact hard-BCS canonical/prefix counts at charged input-order bandwidth.

The algorithm contracts a density matrix on at most w+1 physical sites.
It permits holes and complex rational amplitudes. Runtime is exponential
in w, polynomial in n and coefficient bit size; it does not implement a
quantum circuit or infer an optimal-width ordering.
"""
from representation_compiler import C,Q,matrix


def recognize_bandwidth(f, cap=None):
    f=matrix(f); n=len(f)
    if any(len(row) != n for row in f): raise ValueError('F must be square')
    width=0; edge=None
    for i in range(n):
        for j in range(n):
            if i != j and f[i][j] and abs(i-j) > width:
                width=abs(i-j); edge=[i,j]
    return {'status':'ACCEPTED' if cap is None or width <= cap else 'REJECTED_WIDTH',
            'width':width,'widest_nonzero_edge':edge,'n':n,'F':f}


def creation_product(state, left_mode, right_mode):
    """Action of c_left^dagger c_right^dagger on a Fock basis mask."""
    sign=1
    for mode in (right_mode,left_mode):
        if state & (1 << mode): return None
        if (state & ((1 << mode)-1)).bit_count() & 1: sign=-sign
        state |= 1 << mode
    return state,sign


def add(out,key,value):
    if not value: return
    value=out.get(key,C(0))+value
    if value: out[key]=value
    else: out.pop(key,None)


def pair_gate(rho, coefficient, left_mode, right_mode):
    """rho -> (I+a c_l^+ c_r^+) rho (I+a c_l^+ c_r^+)^*."""
    coefficient=C.make(coefficient)
    if not coefficient: return rho
    out={}
    for (a,b,q),weight in rho.items():
        add(out,(a,b,q),weight)
        ca=creation_product(a,left_mode,right_mode)
        cb=creation_product(b,left_mode,right_mode)
        if ca:
            aa,sa=ca; add(out,(aa,b,q),coefficient*sa*weight)
        if cb:
            bb,sb=cb; add(out,(a,bb,q),coefficient.conjugate()*sb*weight)
        if ca and cb:
            add(out,(aa,bb,q),coefficient.abs2()*sa*sb*weight)
    return out


def local_masks(n, mode_constraints=None, site_constraints=None):
    allowed=[{0,1,2} for _ in range(n)]  # 3 is hard-excluded double occupation.
    if mode_constraints:
        for (site,spin),bit in mode_constraints.items():
            if site not in range(n) or spin not in ('U','D') or bit not in (0,1):
                raise ValueError('invalid mode constraint')
            shift=0 if spin == 'U' else 1
            allowed[site]={s for s in allowed[site] if ((s >> shift)&1) == bit}
    if site_constraints:
        for site,occupations in site_constraints.items():
            if site not in range(n) or not set(occupations) <= {0,1,2}:
                raise ValueError('invalid site constraint')
            allowed[site] &= set(occupations)
    return allowed


def count_coefficients(f, mode_constraints=None, site_constraints=None,
                       width_cap=None, collect_stats=False):
    """Returns every exact c_k under arbitrary physical occupation prefixes.

    F is in the supplied site ordering. No bandwidth-minimization oracle is
    called. Disjoint-minor diagonal invariance licenses omitting F_ii.
    """
    certificate=recognize_bandwidth(f,width_cap)
    if certificate['status'] != 'ACCEPTED': raise ValueError(certificate)
    f=certificate['F']; n=len(f); w=certificate['width']
    allowed=local_masks(n,mode_constraints,site_constraints)
    rho={(0,0,0):C(1)}; peak=1; gates=0; additions=0
    # Frontier at step i is sites i,...,min(n-1,i+w), with site-ordered modes.
    # New rightmost frontier sites are vacua, so their appended high bits are 0.
    for i in range(n):
        for j in range(i+1,min(n,i+w+1)):
            distance=j-i
            for coefficient,left,right in ((f[i][j],0,2*distance+1),
                                           (f[j][i],2*distance,1)):
                if coefficient:
                    additions+=4*len(rho); gates+=1
                    rho=pair_gate(rho,coefficient,left,right)
                    peak=max(peak,len(rho))
        out={}
        for (a,b,q),weight in rho.items():
            occupation=a&3
            if occupation != (b&3) or occupation not in allowed[i]: continue
            add(out,(a >> 2,b >> 2,q+occupation.bit_count()),weight)
        rho=out; peak=max(peak,len(rho))
    polynomial=[Q(0)]*(n+1)
    for (a,b,q),weight in rho.items():
        assert a == b == 0 and weight.im == 0 and weight.re >= 0
        polynomial[q] += weight.re
    assert all(not polynomial[q] for q in range(1,n+1,2))
    coefficients=[polynomial[2*k] for k in range(n//2+1)]
    result={'coefficients':coefficients,'width':w}
    if collect_stats:
        result['stats']={'peak_nonzero_density_coefficients':peak,
                         'pair_creation_gates':gates,'update_bound':additions,
                         'maximum_live_sites':min(n,w+1),
                         'scope':'exact count contraction; quantum circuit unimplemented'}
    return result


def prefix_count(f,k,mode_constraints=None,site_constraints=None,width_cap=None):
    n=len(f)
    if k < 0 or 2*k > n: return Q(0)
    return count_coefficients(f,mode_constraints,site_constraints,width_cap)['coefficients'][k]


def capped_rational_bit(p,getrandbits,attempts):
    """Exact Bernoulli(p) until a bounded rejection cap; returns None on abort.

    Correct distribution/error claims require independent uniformly fair
    getrandbits. A seeded PRNG is only a reproducible execution diagnostic.
    """
    p=Q(p)
    if not 0 <= p <= 1: raise ValueError('invalid probability')
    if p == 0 or p == 1: return int(p),0
    d=p.denominator; bits=(d-1).bit_length()
    for attempt in range(attempts):
        draw=getrandbits(bits)
        if not 0 <= draw < (1 << bits): raise ValueError('getrandbits contract violated')
        if draw < d: return int(draw < p.numerator),(attempt+1)*bits
    return None,attempts*bits


def sample_born(f,k,getrandbits,epsilon=Q(1,1000000),width_cap=None):
    """Total capped Born sampler with TV error <= epsilon under fair random bits.

    Exact prefix counts and a supported fallback eliminate inverse-sector
    costs. Arithmetic/coin budgets are finite on every execution. This is
    classical sampling; no quantum circuit is executed.
    """
    f=matrix(f); n=len(f); epsilon=Q(epsilon)
    if not 0 < epsilon <= 1: raise ValueError('epsilon must be in (0,1]')
    z=prefix_count(f,k,width_cap=width_cap)
    if not z: return {'status':'ZERO','norm':z}
    attempts=0
    while Q(2*n,1 << attempts) > epsilon: attempts+=1
    prefix={}; fallback=False; coin_bits=0; count_queries=1
    for site,spin in ([(i,'U') for i in range(n)]+[(i,'D') for i in range(n)]):
        zero=dict(prefix); zero[site,spin]=0
        one=dict(prefix); one[site,spin]=1
        z0=prefix_count(f,k,zero,width_cap=width_cap)
        z1=prefix_count(f,k,one,width_cap=width_cap); count_queries+=2
        assert z0+z1 > 0
        if fallback:
            bit=int(bool(z1))
        else:
            bit,used=capped_rational_bit(z1/(z0+z1),getrandbits,attempts)
            coin_bits+=used
            if bit is None:
                fallback=True; bit=int(bool(z1))
        prefix[site,spin]=bit
    up=[i for i in range(n) if prefix[i,'U']]
    down=[i for i in range(n) if prefix[i,'D']]
    assert len(up) == len(down) == k and not set(up)&set(down)
    return {'status':'SAMPLE','up':up,'down':down,'norm':z,
            'fallback':fallback,'coin_bits':coin_bits,'attempt_cap':attempts,
            'exact_count_queries':count_queries,
            'randomness_contract':'TV guarantee requires independent fair random bits'}
