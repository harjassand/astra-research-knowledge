#!/usr/bin/env python3
"""Acquire an unknown error using an acquired chain-ring uniformizer.

The annihilator kernel is larger than the ordinary-ring polynomial family.
A caller MUST verify the recovered base in its exact ordinary-ring fitter.
Only matrix acquisition is performed here; no count or base fit is asserted.
"""
from sylvester_support import *


def nilpotent_apply(x,power,d,e,b):
    if power>=e: return 0
    m=d*e; lowmask=(1<<(d*(e-power)))-1
    return sum((((x>>(m*i))&lowmask)<<(d*power))<<(m*i) for i in range(b))


def ring_gram_apply(x,local_gram,d,e,b):
    m=d*e; mask=(1<<d)-1
    return sum(linear_apply(local_gram,(x>>(m*i+d*j))&mask)<<(m*i+d*(e-1-j))
               for i in range(b) for j in range(e))


def nilpotent_operator(L,d,e,b):
    result=[]
    for i,column in enumerate(L):
        v=1<<i; N4v=nilpotent_apply(v,4,d,e,b)
        cv=nilpotent_apply(v,1,d,e,b)^nilpotent_apply(v,2,d,e,b)
        qv=nilpotent_apply(v,1,d,e,b)^nilpotent_apply(v,3,d,e,b)
        Lcv=linear_apply(L,cv); Lqv=linear_apply(L,qv)
        value=linear_apply(L,N4v)^nilpotent_apply(column,4,d,e,b)
        value^=nilpotent_apply(Lqv,1,d,e,b)^nilpotent_apply(Lqv,2,d,e,b)
        value^=nilpotent_apply(Lcv,1,d,e,b)^nilpotent_apply(Lcv,3,d,e,b)
        result.append(value)
    return result


def acquire_nilpotent_base(B,h,e,module_dimension=3):
    """Return (base_candidate, exact_defect, certificate).

    Input order is module block -> uniformizer power -> field bit.
    Uses the chain-ring top-coefficient Gram pairing, not the field-block Gram.
    Under the seven-term Krylov directness condition, the exact planted defect
    is recovered; callers then verify the ordinary-ring polynomial base.
    """
    started=time.perf_counter(); d=h.bit_length()-1; b=module_dimension; n=len(B)
    if not irreducible_binary(h): raise ValueError('reducible field modulus')
    if not isinstance(e,int) or e<7: raise ValueError('nilpotent support acquisition requires chain length at least seven')
    if not isinstance(b,int) or b<1 or n!=b*d*e: raise ValueError('incomplete free chain module')
    if any(not isinstance(x,int) or x<0 or x>>n for x in B): raise ValueError('invalid binary matrix')
    if any(x>>i&1 for i,x in enumerate(B)) or any((B[i]>>j^B[j]>>i)&1 for i in range(n) for j in range(i)):
        raise ValueError('input polar matrix must be alternating')
    gram=trace_gram(h); gram_inv=[solve(gram,1<<j) for j in range(d)]
    L=[ring_gram_apply(x,gram_inv,d,e,b) for x in B]
    H=nilpotent_operator(L,d,e,b); W=independent(H)
    certificate=dict(operator='selfadjoint nilpotent uniformizer',field_degree=d,
        chain_length=e,module_dimension=b,scalar_orbit_dimension=7,
        pairing='ring top-coefficient Frobenius pairing',
        manufactured_syndrome_rank=len(W),base_fit_required=True,
        base_certificate_scope='annihilator identity only; ordinary-ring coefficient fit must follow')
    if not W:
        certificate.update(recovered_rank=0,recovered_support=[],krylov_rank=0,
            seconds=time.perf_counter()-started)
        return B[:],[0]*n,certificate
    if len(W)%4: raise ValueError('syndrome rank is not a four-fold expansion')
    cW=[nilpotent_apply(w,1,d,e,b)^nilpotent_apply(w,2,d,e,b) for w in W]
    cpiv=span(cW)
    if len(cpiv)!=len(W): raise ValueError('uniformizer polynomial is not injective on manufactured support')
    cU=intersection(W,cW)
    preimages=[solve_with_pivots(cpiv,v) for v in cU]
    assert all(v is not None for v in preimages)
    U=independent(linear_apply(W,v) for v in preimages); r=len(U)
    if len(W)!=4*r: raise ValueError('restricted preimage has incompatible dimension')
    krylov=[nilpotent_apply(u,j,d,e,b) for j in range(7) for u in U]
    if len(span(krylov))!=7*r: raise ValueError('recovered uniformizer Krylov orbit is not direct')
    N4U=[nilpotent_apply(u,4,d,e,b) for u in U]
    cU=[nilpotent_apply(u,1,d,e,b)^nilpotent_apply(u,2,d,e,b) for u in U]
    qU=[nilpotent_apply(u,1,d,e,b)^nilpotent_apply(u,3,d,e,b) for u in U]
    CU=U+N4U+cU+qU; piv=span(CU)
    if len(piv)!=4*r: raise ValueError('recovered coefficient orbit is not direct')
    coordinates=[solve_with_pivots(piv,v) for v in H]
    if any(v is None for v in coordinates): raise ValueError('syndrome outside recovered support')
    E=[linear_apply(U,(v>>r)&((1<<r)-1)) for v in coordinates]
    defect=[ring_gram_apply(x,gram,d,e,b) for x in E]
    base=[x^y for x,y in zip(B,defect)]
    if any(defect[i]>>i&1 for i in range(n)) or any((defect[i]>>j^defect[j]>>i)&1 for i in range(n) for j in range(i)):
        raise ValueError('recovered error is not alternating')
    if len(span(defect))!=r: raise ValueError('recovered error rank inconsistent')
    if any(nilpotent_operator([x^y for x,y in zip(L,E)],d,e,b)):
        raise ValueError('base candidate is not annihilated')
    # The sum is an exact rational bound on failure for iid uniform columns.
    # Common denominator 2^n avoids floating point underflow.
    numerator=sum(((1<<((7-v)*r))-(1<<((6-v)*r)))<<(b*d*v) for v in range(7))
    certificate.update(recovered_rank=r,recovered_support=U,krylov_rank=7*r,
        iid_failure_bound_numerator=numerator,iid_failure_bound_denominator=1<<n,
        seconds=time.perf_counter()-started)
    return base,defect,certificate
