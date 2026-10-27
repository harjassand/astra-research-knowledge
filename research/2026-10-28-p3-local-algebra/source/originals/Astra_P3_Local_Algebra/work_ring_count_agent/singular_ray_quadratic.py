#!/usr/bin/env python3
"""Coefficient-input arbitrary homogeneous unit-XYZ ring cubic + quotient Q.
No smoothness, low-rank promise, or field/ring enumeration. Terminal depth1
is deliberately delegated; depths0,2 mod3 need no terminal point counter.
"""
from smooth_ring_counter import *
from field_descent import kernel_columns,span
from itertools import combinations


def pack(R,a): return sum(c<<(R.d*i) for i,c in enumerate(a))

def ring_gradient(R,H,values,direction):
    ans=R.zero
    for ex,c in H.items():
        if ex[direction]&1:
            ee=list(ex); ee[direction]-=1
            ans=R.add(ans,ring_polynomial_value(R,{tuple(ee):c},values))
    return ans

def chart_centers(R,H,pivot):
    rest=[i for i in range(3) if i!=pivot]; width=R.d*R.e
    def values(bits):
        v=[R.zero]*3; v[pivot]=R.one
        for j,i in enumerate(rest): v[i]=R.packed((bits>>(j*width))&((1<<width)-1))
        return v
    def gradients(bits):
        v=values(bits)
        return sum(pack(R,ring_gradient(R,H,v,i))<<(j*width) for j,i in enumerate(rest))
    offset=gradients(0); columns=[gradients(1<<i)^offset for i in range(2*width)]
    particular=solve(columns,offset)
    if particular is None: return []
    kernel=kernel_columns(columns)
    if len(kernel)>2: raise AssertionError('unit-XYZ chart critical fiber exceeds Bezout bound')
    roots=[]
    for mask in range(1<<len(kernel)):
        bits=particular
        for j,k in enumerate(kernel):
            if mask>>j&1: bits^=k
        assert gradients(bits)==0
        v=values(bits)
        if any(v[i][0] for i in range(pivot+1,3)): continue
        c=ring_polynomial_value(R,H,v)
        if c[0]: continue
        roots.append((v,c))
    return roots

def hasse_square(R,H,v,i):
    ans=0
    for ex,c in H.items():
        if ex[i] not in (2,3): continue
        ee=list(ex); ee[i]-=2; val=c[0]
        for x,k in zip(v,ee): val=gf_mul(val,gf_pow(x[0],k,R.h),R.h)
        ans^=val
    return ans

def ray_weight(R,c,v,Q):
    width=R.d*R.e
    def phase(bits):
        r=R.packed(bits); cube=R.mul(R.mul(r,r),r)
        x=sum(pack(R,R.mul(r,a))<<(j*width) for j,a in enumerate(v))
        return R.bit(R.mul(c,cube))^polynomial_value(Q,x)
    all_sum=quadratic_sum(phase,width)
    nil_sum=quadratic_sum(lambda x:phase(x<<R.d),width-R.d)
    return all_sum-nil_sum,dict(all_quadratic_sum=all_sum,nonunit_quadratic_sum=nil_sum)

def origin_restriction(Q,R):
    oldw=R.d*R.e; neww=R.d*(R.e-3); out=set()
    for mask in Q:
        new=0; killed=False
        for i in range(3):
            block=(mask>>(i*oldw))&((1<<oldw)-1)
            if block&((1<<R.d)-1): killed=True; break
            reduced=block>>R.d
            if reduced>>neww: raise ValueError('perturbation uses a discarded high digit')
            new|=reduced<<(i*neww)
        if not killed: out.symmetric_difference_update({new})
    return out

def homogeneous_quotient_sum(R,H,Q,depth=None,*,terminal=None,details=False):
    depth=(R.e+1)//3 if depth is None else depth
    if not 0<=depth<=(R.e+1)//3: raise ValueError('unsupported quotient depth')
    H={m:R.element(c) for m,c in H.items() if any(c)}
    if any(m not in CUBICS for m in H) or not H.get((1,1,1),R.zero)[0]:
        raise ValueError('homogeneous cubic with unit XYZ coefficient required')
    n=3*R.d*R.e; low=quotient_bitmask(R,depth)
    if any(mask<0 or mask>>n or mask.bit_count()>2 or mask&~low for mask in Q):
        raise ValueError('quadratic perturbation must descend to stated quotient')
    if R.e==1:
        if terminal is None: raise ValueError('generic finite-field terminal not implemented')
        result=terminal({m:c[0] for m,c in H.items()},R.h)*(-1 if 0 in Q else 1)
        evidence=dict(length=1,signed_count=result,terminal=True)
        return (result,evidence) if details else result
    if R.e<=3:
        origin=pow(R.q,3*(R.e-1))*(-1 if 0 in Q else 1); child=None
    else:
        small=ChainRing(R.h,R.e-3); Hsmall={m:c[:R.e-3] for m,c in H.items()}
        Qsmall=origin_restriction(Q,R)
        inner,child=homogeneous_quotient_sum(small,Hsmall,Qsmall,max(0,depth-1),terminal=terminal,details=True)
        origin=pow(R.q,6)*inner
    total=origin; rays=[]; mu=H[(1,1,1)][0]
    mu2inv=gf_pow(gf_mul(mu,mu,R.h),R.q-2,R.h)
    for pivot in range(3):
        rest=[i for i in range(3) if i!=pivot]
        for v,c in chart_centers(R,H,pivot):
            A=hasse_square(R,H,v,rest[0]); B=hasse_square(R,H,v,rest[1])
            arf=gf_trace(gf_mul(gf_mul(A,B,R.h),mu2inv,R.h),R.h)
            U,quad=ray_weight(R,c,v,Q)
            contribution=pow(R.q,R.e)*(-1 if R.e%2 and arf else 1)*U
            total+=contribution
            rays.append(dict(pivot=pivot,center=v,critical_value=c,arf_bit=arf,
                             radial_sum=U,contribution=contribution,**quad))
    if len(rays)>3: raise AssertionError('reduced plane cubic has more than three singularpoints')
    evidence=dict(length=R.e,quotient_depth=depth,origin=origin,rays=rays,child=child,signed_count=total)
    return (total,evidence) if details else total
