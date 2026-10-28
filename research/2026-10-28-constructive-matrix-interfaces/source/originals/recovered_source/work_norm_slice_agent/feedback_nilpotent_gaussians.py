#!/usr/bin/env python3
"""Closed Gaussian source formula on an arbitrary nilpotent Jordan type.

No matrices, field elements, subspaces, or Jordan partitions are enumerated.
The input tuple is the supplied nilpotent Jordan type, not a guessed type.
"""
from invariant_quadratic_scalar_gauss import (
    Field, polynomial_value, quadratic_sum, two_scalar_matrix_gaussians)
from functools import lru_cache

def nilpotent_gauss(lengths,h,beta,phi,eta=0):
    lengths=tuple(lengths); phi=frozenset(phi); F=Field(h); b=sum(lengths)
    if any(type(x) is not int or x<=0 for x in lengths):
        raise ValueError('positive explicit nilpotent block lengths required')
    if not 0<=beta<F.q or not 0<=eta<F.q: raise ValueError('field coefficient out of range')
    if any(type(x) is not int or x<0 or x.bit_length()>F.a or x.bit_count()>2 for x in phi):
        raise ValueError('Boolean quadratic ANF on field coordinates required')
    if beta:
        return two_scalar_matrix_gaussians(b,h,beta,phi)[0][b]
    z=sum(min(i,j) for i in lengths for j in lengths)
    exponent=(b*b+z)//2
    if (b*b+z)%2: raise AssertionError('alternating commutator has odd rank')
    if not any(x%2 for x in lengths):
        return (1-2*polynomial_value(phi,eta if (b//2)%2 else 0))*F.q**exponent
    scalar=quadratic_sum(lambda x:polynomial_value(phi,x),F.a)
    return F.q**(exponent-1)*scalar

@lru_cache(None)
def qbinom(n,k,q):
    if not 0<=k<=n: return 0
    value=1
    for j in range(k):
        value,rem=divmod(value*(q**(n-j)-1),q**(j+1)-1)
        if rem: raise ArithmeticError('Gaussian coefficient was not integral')
    return value

def regular_chain_gap(t,h,beta,phi):
    """Independent implementation of the parent's regular-chain profile DP.

    Returns the gap for tr(XYZ)+beta e2(X)+tr(J_t X^2)+phi(tr X),
    with the absolute field trace applied to the field-valued terms.
    """
    F=Field(h);q=F.q
    if type(t) is not int or t<1:raise ValueError('positive explicit matrix size required')
    H=[[0]*(t+1) for _ in range(t+1)];H[0][0]=1
    for c in range(1,t+1):
        for k in range(1,c+1):
            H[c][k]=sum(q**(j*(j+1)//2)*qbinom(k,j,q)*H[c-k][j]
                        for j in range(min(k,c-k)+1))
    products=[1]
    for k in range(t):products.append(products[-1]*(q**(t-k)-1))
    T=[sum(products[k]*H[c][k] for k in range(c+1)) for c in range(t+1)]
    G=[nilpotent_gauss((b,) if b else (),h,beta,phi) for b in range(t+1)]
    gap=q**(t*t)*sum(q**(c*(c-1)//2+c*(t-c))*T[c]*G[t-c] for c in range(t+1))
    return gap,dict(H=H,T=T,residual_gaussians=G)

def shifted_trace_polynomial(phi,F,delta,beta):
    """ANF of p(s+delta)+Tr(beta*delta*s); known quadratic expression."""
    value=lambda s:polynomial_value(phi,s^delta)^F.trace(F.mul(F.mul(beta,delta),s))
    constant=value(0);out={0} if constant else set();linear=[]
    for i in range(F.a):
        coefficient=value(1<<i)^constant;linear.append(coefficient)
        if coefficient:out.add(1<<i)
    for i in range(F.a):
        for j in range(i+1,F.a):
            if value((1<<i)|(1<<j))^linear[i]^linear[j]^constant:
                out.add((1<<i)|(1<<j))
    return out

def regular_chain_gap_linear(t,h,beta,phi,eta):
    """All beta,eta extension, retaining the even-level height sum mod four."""
    F=Field(h);q=F.q;phi=frozenset(phi)
    if type(t) is not int or t<1 or not 0<=beta<q or not 0<=eta<q:
        raise ValueError('invalid explicit dimension or field coefficient')
    # Validate phi even in branches that would otherwise only evaluate a point.
    nilpotent_gauss((),h,beta,phi,eta)
    tail=[[[[0]*4 for _ in range(2)] for _ in range(t+1)] for _ in range(t+1)]
    for k in range(t+1):
        for e in range(2):tail[0][k][e][0]=1
    for remaining in range(1,t+1):
        for previous in range(1,t+1):
            for height in range(1,min(previous,remaining)+1):
                weight=q**(height*(height+1)//2)*qbinom(previous,height,q)
                for level in range(2):
                    for residue in range(4):
                        tail[remaining][previous][level][(residue+level*height)%4]+=\
                            weight*tail[remaining-height][height][1-level][residue]
    products=[1]
    for k in range(t):products.append(products[-1]*(q**(t-k)-1))
    profiles=[[0]*4 for _ in range(t+1)];profiles[0][0]=1
    for c in range(1,t+1):
        for k in range(1,c+1):
            for residue in range(4):
                profiles[c][residue]+=products[k]*tail[c-k][k][1][residue]
    if beta:
        J=[two_scalar_matrix_gaussians(t,h,beta,shifted_trace_polynomial(phi,F,delta,beta))[0]
           for delta in [0,eta]]
        phases=[1-2*(F.trace(F.mul(beta,F.mul(eta,eta))) * (r*(r-1)//2%2)) for r in range(4)]
        gaussians=[[phases[r]*J[r%2][b] for r in range(4)] for b in range(t+1)]
    else:
        scalar=quadratic_sum(lambda s:polynomial_value(phi,s),F.a)
        gaussians=[]
        for b in range(t+1):
            if b%2:gaussians.append([q**(b*(b+1)//2-1)*scalar]*4)
            else:gaussians.append([(1-2*polynomial_value(phi,eta if (r+b//2)%2 else 0))*
                                  q**(b*(b+1)//2) for r in range(4)])
    gap=q**(t*t)*sum(q**(c*(c-1)//2+c*(t-c))*sum(profiles[c][r]*gaussians[t-c][r] for r in range(4))
                    for c in range(t+1))
    return gap,dict(profile_residues_mod4=profiles,residual_gaussians=gaussians)
