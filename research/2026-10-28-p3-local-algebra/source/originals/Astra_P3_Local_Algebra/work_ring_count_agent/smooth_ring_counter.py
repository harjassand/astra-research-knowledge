#!/usr/bin/env python3
"""Smooth homogeneous ring cubics with acquired quotient-quadratic noise.
Generic smooth cubics are fully counted when e is 0 or 2 mod 3. At e=1
mod 3 the production backend supports the explicit ordinary family stated
in the proof, at all residue degrees; other field leaves are rejected.
"""
from chain_ring_kloosterman import *
from field_descent import extract_anf,solve,polynomial_value
from itertools import product

CUBICS=tuple((i,j,3-i-j) for i in range(4) for j in range(4-i))

def fp_add(p,q):
    out=dict(p)
    for e,c in q.items(): out[e]=out.get(e,0)^c
    return {e:c for e,c in out.items() if c}

def fp_scale_shift(p,c,s,h):
    return {tuple(x+y for x,y in zip(e,s)):gf_mul(v,c,h) for e,v in p.items() if v and c}

def fp_monic(p,h):
    if not p: return p
    c=gf_pow(p[max(p)],(1<<(h.bit_length()-1))-2,h)
    return {e:gf_mul(v,c,h) for e,v in p.items()}

def fp_reduce(p,basis,h):
    p=dict(p); rem={}
    while p:
        e=max(p); c=p[e]
        match=next((g for g in basis if all(x>=y for x,y in zip(e,max(g)))),None)
        if match is None: rem[e]=c; del p[e]
        else:
            f=max(match); scale=gf_mul(c,gf_pow(match[f],(1<<(h.bit_length()-1))-2,h),h)
            p=fp_add(p,fp_scale_shift(match,scale,tuple(x-y for x,y in zip(e,f)),h))
    return rem

def affine_ideal_is_unit(polys,h):
    basis=[]; pairs=[]
    for p in polys:
        p=fp_monic(fp_reduce(p,basis,h),h)
        if p:
            if max(p)==(0,0): return True
            pairs.extend((i,len(basis)) for i in range(len(basis))); basis.append(p)
    while pairs:
        i,j=pairs.pop(); f,g=basis[i],basis[j]; ef,eg=max(f),max(g)
        L=tuple(max(a,b) for a,b in zip(ef,eg))
        s=fp_add(fp_scale_shift(f,1,tuple(a-b for a,b in zip(L,ef)),h),
                 fp_scale_shift(g,1,tuple(a-b for a,b in zip(L,eg)),h))
        s=fp_monic(fp_reduce(s,basis,h),h)
        if s:
            if max(s)==(0,0): return True
            pairs.extend((i,len(basis)) for i in range(len(basis))); basis.append(s)
    return False

def projective_smooth(H,h):
    """Buchberger in each of the three affine charts, over the coefficient field.
    Ideal=1 certifies absence of critical points over the algebraic closure.
    Only three quadratic polynomials in two variables occur in each chart.
    """
    gradients=[]
    for i in range(3):
        p={}
        for e,c in H.items():
            if e[i]&1:
                f=list(e); f[i]-=1; f=tuple(f); p[f]=p.get(f,0)^c
        gradients.append({e:c for e,c in p.items() if c})
    for chart in range(3):
        polys=[]
        for p in gradients:
            out={}
            for e,c in p.items():
                f=tuple(e[i] for i in range(3) if i!=chart)
                out[f]=out.get(f,0)^c
            polys.append({e:c for e,c in out.items() if c})
        if not affine_ideal_is_unit(polys,h): return False
    return True

def ring_polynomial_value(R,H,values):
    ans=R.zero
    for exponents,c in H.items():
        v=c
        for j,power in enumerate(exponents):
            for _ in range(power): v=R.mul(v,values[j])
        ans=R.add(ans,v)
    return ans

def field_hesse_sum(H,h):
    """H=X²Y+XY²+Z³+aXYZ; a³!=1. Odd d uses the fast Kloosterman form."""
    d=h.bit_length()-1; q=1<<d
    a=H.get((1,1,1),0)
    expected={(2,1,0):1,(1,2,0):1,(0,0,3):1}
    if a: expected[(1,1,1)]=a
    if {e:c for e,c in H.items() if c}!=expected:
        raise ValueError('unimplemented finite-field leaf: cubic outside the explicit family')
    a3=gf_pow(a,3,h)
    if a3==1: raise ValueError('singular residue cubic')
    if d%2==0 or not a:
        from laurent_field_counter import shifted_hesse_sum
        return shifted_hesse_sum(h,a)
    u=gf_pow(a3,q-2,h); c=gf_mul(a3^1,gf_pow(gf_pow(a,12,h),q-2,h),h)
    K,_=kloosterman_dwork(c,h,use_hasse=True)
    return q*(1-2*gf_trace(u,h))*K

def smooth_homogeneous_sum(R,H):
    if any(e not in CUBICS for e in H): raise ValueError('ordinary homogeneous cubic required')
    H={e:R.element(c) for e,c in H.items() if any(c)}
    residue={e:c[0] for e,c in H.items() if c[0]}
    if not projective_smooth(residue,R.h): raise ValueError('residue cubic is singular')
    if R.e%3==0: return pow(R.q,2*R.e)
    if R.e%3==2: return pow(R.q,2*R.e-1)
    return pow(R.q,2*R.e-2)*field_hesse_sum(residue,R.h)

def quotient_bitmask(R,depth):
    return sum(((1<<(R.d*depth))-1)<<(R.d*R.e*i) for i in range(3))

def acquire_quotient_quadratic(poly,R,depth=None):
    """Given raw ANF in acquired ring coordinates, fit H+Q by binary algebra.
    H is homogeneous ordinary ring cubic. Q may be an arbitrary binary
    quadratic on V/t^depth V. This stage receives neither H nor Q.
    """
    if R.e<2: raise ValueError('positive nilpotent depth required')
    depth=(R.e+1)//3 if depth is None else depth
    if not 0<=depth<=(R.e+1)//3: raise ValueError('quotient exceeds invisible depth')
    n=3*R.d*R.e; lowmask=quotient_bitmask(R,depth)
    if any(m<0 or m>>n or m.bit_count()>3 for m in poly): raise ValueError('invalid cubic ANF')
    def protected(m): return m.bit_count()==3 or bool(m&~lowmask)
    all_masks=[sum(1<<i for i in S) for k in range(1,4)
               for S in __import__('itertools').combinations(range(n),k)]
    rows=[m for m in all_masks if protected(m)]; pos={m:i for i,m in enumerate(rows)}
    def vector(p): return sum(1<<pos[m] for m in p if m in pos)
    columns=[]; models=[]; keys=[]; width=R.d*R.e
    for monomial in CUBICS:
        for k in range(R.e):
            for bit in range(R.d):
                c=tuple((1<<bit) if j==k else 0 for j in range(R.e))
                def value(x):
                    vals=[R.packed((x>>(i*width))&((1<<width)-1)) for i in range(3)]
                    return R.bit(ring_polynomial_value(R,{monomial:c},vals))
                model=extract_anf(value,n)
                models.append(model); keys.append((monomial,k,bit)); columns.append(vector(model))
    answer=solve(columns,vector(poly))
    if answer is None: raise ValueError('raw polynomial has no admissible cubic plus quotient quadratic fit')
    H={}; remainder=set(poly)
    for i,(monomial,k,bit) in enumerate(keys):
        if answer>>i&1:
            remainder.symmetric_difference_update(models[i])
            c=H.setdefault(monomial,[0]*R.e); c[k]^=1<<bit
    H={m:tuple(c) for m,c in H.items() if any(c)}
    if any(m.bit_count()>2 or m&~lowmask for m in remainder): raise AssertionError('invalid fitted quotient remainder')
    residue={e:c[0] for e,c in H.items() if c[0]}
    if not projective_smooth(residue,R.h): raise ValueError('acquired residue cubic is singular')
    Z=smooth_homogeneous_sum(R,H)*(-1 if 0 in remainder else 1)
    return dict(H=H,Q=remainder,depth=depth,signed_count=Z,zero_count=((1<<n)+Z)//2,
                original_bits=n,quotient_bits=3*R.d*depth,linear_fit_columns=len(columns),
                linear_fit_rows=len(rows))
