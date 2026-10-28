#!/usr/bin/env python3
"""Four-height exact counter for one cyclic irreducible-quadratic primary.

The operator has characteristic/minimal polynomial f^e, deg f=2, with e
unbounded. All beta, eta and Boolean quadratic trace sources are supported.
The matrix algebra representation is supplied to this backend. It does not
claim acquisition from an arbitrary program or arbitrary raw quadratic.
"""
from functools import lru_cache
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'work_matrix_root'))
sys.path.insert(0,str(ROOT/'work_norm_frontier_agent'))
from simple_operator_quadratic import matrix_source_anf
from krylov_square_source import Field, companion, quadratic_anf_sum, factor_polynomial
from feedback_nilpotent_gaussians import shifted_trace_polynomial
from two_invariant_quadratic_matrix import gaussian_rows

def quadratic_primary_profile_weights(t,q,maximum=None):
    """Return exact mod-four full-profile weights, without listing partitions.

    Degree n output is the coefficient of z^n in
    sum_lambda (q^t;q^-1)_ell(lambda) P_lambda[-z-z*(-1);q], refined
    by sum of the even column heights modulo four. Only even n survive.
    The plethystic negative alphabet has power sums -z^r*(1+(-1)^r).
    """
    if maximum is None:maximum=t
    if not 0<=maximum<=t:raise ValueError('0<=maximum<=ambient dimension required')
    choose=gaussian_rows(t,q);transitions=0
    @lru_cache(None)
    def local(h,g):
        h0,h1,h2,h3=h;g0,g1,g2,g3=g
        # Q'[q,-q,-1,-(-1)] branching, ordered as the two negative
        # letters followed by the two positive letters. The outer Gaussian
        # turns the Hall-Littlewood b_lambda denominator into integers.
        if not (h0>=h1>=h2>=h3>=0 and g0>=g1>=g2>=g3>=0
                and g0<=h1 and g1<=h2 and g2<=h2 and g3<=h3):return 0
        exponent=(h2-h3)*(h2-h3+1)//2+h3*(h3+1)//2
        sign=-1 if (h0-h1+h3)%2 else 1
        return sign*q**exponent*choose[h0][g0]*choose[h0-g0][h0-h1]*choose[h1-g1][h1-h2]*choose[h2-g3][h3-g3]
    @lru_cache(None)
    def tail(remaining,h,parity):
        nonlocal transitions
        h0,h1,h2,h3=h
        if not h0:return (int(remaining==0),0,0,0)
        if remaining<h0:return (0,0,0,0)
        left=remaining-h0;out=[0]*4;shift=parity*h0%4
        for g0 in range(min(h1,left)+1):
            if not g0 and left:continue
            for g1 in range(min(g0,h2)+1):
                for g2 in range(min(g1,h2)+1):
                    for g3 in range(min(g2,h3)+1):
                        g=(g0,g1,g2,g3);w=local(h,g)
                        if not w:continue
                        v=tail(left,g,1-parity);transitions+=1
                        for r in range(4):out[(r+shift)%4]+=w*v[r]
        return tuple(out)
    answers={0:(1,0,0,0)}
    for n in range(1,maximum+1):
        answer=[0]*4
        for h0 in range(1,n+1):
            initial=choose[t][h0]
            for h1 in range(h0+1):
                for h2 in range(h1+1):
                    for h3 in range(h2+1):
                        value=tail(n,(h0,h1,h2,h3),0)
                        for r in range(4):answer[r]+=initial*value[r]
        answers[n]=tuple(answer)
        if n%2 and any(answer):raise AssertionError('roots-of-unity odd-degree cancellation failed')
    return answers,dict(profile_states=tail.cache_info().currsize,
                       profile_transitions=transitions,local_transitions=local.cache_info().currsize,
                       height_coordinates=4,enumerated_partitions=0,enumerated_subspaces=0)

def polynomial_product(A,B,F):
    C=[0]*(len(A)+len(B)-1)
    for i,a in enumerate(A):
        for j,b in enumerate(B):C[i+j]^=F.mul(a,b)
    return C

def cyclic_quadratic_primary_gap(exponent,field_h,irreducible,beta,phi,eta=0):
    F=Field(field_h);q=F.q;f=list(irreducible);phi=set(phi)
    if type(exponent) is not int or exponent<1:raise ValueError('positive explicit primary exponent required')
    if len(f)!=3 or f[-1]!=1 or any(type(x) is not int or not 0<=x<q for x in f):raise ValueError('monic quadratic over F required')
    if factor_polynomial(f,F)!=[(f,1)]:raise ValueError('quadratic factor must be irreducible')
    if not 0<=beta<q or not 0<=eta<q or any(type(m) is not int or m<0 or m.bit_length()>F.a or m.bit_count()>2 for m in phi):raise ValueError('invalid field coefficient or trace quadratic')
    t=2*exponent;weights,stats=quadratic_primary_profile_weights(t,q)
    powers=[[1]]
    for _ in range(exponent):powers.append(polynomial_product(powers[-1],f,F))
    phase=F.trace(F.mul(beta,F.mul(eta,eta)));total=0;terms=[]
    for j in range(exponent+1):
        c=2*j;b=t-c;D=companion(powers[exponent-j]) if b else []
        value=0;gaussians=[]
        for residue in range(4):
            delta=eta if residue%2 else 0
            shifted=shifted_trace_polynomial(phi,F,delta,beta)
            source=matrix_source_anf(D,F,beta,shifted,eta)
            gaussian=quadratic_anf_sum(source,F.a*b*b)
            sign=-1 if phase*(residue*(residue-1)//2)%2 else 1
            value+=weights[c][residue]*sign*gaussian
            gaussians.append(gaussian)
        prefactor=q**(c*(c-1)//2+c*b);total+=prefactor*value
        terms.append(dict(controlled_dimension=c,residual_dimension=b,
                          profile_weights=list(weights[c]),residual_gaussians=gaussians,
                          contribution=prefactor*value))
    gap=q**(t*t)*total
    stats.update(route='four-height Hall-Littlewood transfer for one cyclic degree-two primary',
                 field_polynomial=field_h,field_degree=F.a,matrix_size=t,
                 irreducible_polynomial=f,primary_exponent=exponent,beta=beta,eta=eta,
                 trace_quadratic_anf=sorted(phi),terms=terms,
                 enumerated_field_elements=0,enumerated_original_assignments=0,
                 original_bits=3*F.a*t*t)
    return gap,stats
