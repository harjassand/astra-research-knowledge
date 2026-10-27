"""Rational certificates for a tighter-cap infimum and sharp small-C slope.

An interval sign bracket proves existence of each exact transcendental root.
The analytic root-count argument, not the numerical brackets, owns the
all-frequency dual signs. This script never treats the H=infinity limit as
a finite legal fixed-backbone network.
"""
from fractions import Fraction as Q
from pathlib import Path
from intervals import I,sqrt,sinh,cosh,bose,full_conductance

HERE=Path(__file__).resolve().parent

def interpolate(edges):
    nodes=[w*w for w in edges]
    vals=[w**3*bose(w) for w in edges]
    c=[I(0),I(0),I(0)]
    for i in range(3):
        j,k=[a for a in range(3) if a!=i]
        v=vals[i]/((nodes[i]-nodes[j])*(nodes[i]-nodes[k]))
        c[0]+=v*nodes[j]*nodes[k]
        c[1]-=v*(nodes[j]+nodes[k]);c[2]+=v
    return -c[1],-c[2]/2,c[0]

def at_A(A,C):
    A,C=I(A) if not isinstance(A,I) else A,iv_C(C)
    r=sqrt((A-2)/C)
    delta=sqrt((r*r+A)**2-8*r*r)
    s=sqrt((r*r+A+delta)/2);p=sqrt(2*r*r/(s*s))
    return [p,r,s],interpolate([p,r,s])

def iv_C(C):return C if isinstance(C,I) else I(C)

def slope_data(r):
    r=iv_C(r);g=bose(r)
    lam=r*g*(r*cosh(r)/sinh(r)-Q(5,2))
    eta=r**3*g+lam*r*r
    a=sqrt(2)
    E=a**3*bose(a)+2*lam-eta
    return E,lam,eta

def main():
    # A root of mu(A,C)=0 at fixed C=1/20; its active trace is below 4.
    C=Q(1,20)
    lo=Q('3.39813033676949568');hi=Q('3.39813033676949570')
    _,(_,mu_lo,_)=at_A(lo,C)
    _,(_,mu_hi,_)=at_A(hi,C)
    assert mu_lo.lo>0>mu_hi.hi
    A=I(lo,hi)
    edges,(lam,mu,eta)=at_A(A,C)
    assert 2<A.lo<A.hi<4 and lam.lo>0 and eta.lo>0
    m=4/A;h=m-1;b=2-m;k=b*b/C
    Jinf=full_conductance(edges)

    # An exact root r0 of E(r)=0 makes F0(sqrt2)=F0(r0)=F0'(r0)=0.
    rlo=Q('5.2916003633454644313334084015605480943466')
    rhi=Q('5.2916003633454644313334084015605480943467')
    Elo,_,_=slope_data(rlo);Ehi,_,_=slope_data(rhi)
    assert Elo.hi<0<Ehi.lo
    r0=I(rlo,rhi);_,lam0,eta0=slope_data(r0)
    assert lam0.lo>0 and eta0.lo>0
    slope=eta0/4;ordinary_slope=bose(sqrt(2))/sqrt(2)
    ratio=slope/ordinary_slope
    lines=[
        'PASS: exact rational sign brackets + analytic root-count dual.',
        'At C=1/20, an exact mu=0 effective-trace root exists in:',
        'A '+A.decimal(),
        'mu(A_lo) '+mu_lo.decimal(32),
        'mu(A_hi) '+mu_hi.decimal(32),
        'lambda '+lam.decimal(), 'eta '+eta.decimal(),
        'effective backbone mass '+m.decimal(),
        'hard side mass in finite approximants '+h.decimal(),
        'soft side mass '+b.decimal(),'limiting soft spring '+k.decimal(),
        'J_infimum '+Jinf.decimal(),
        'This is a bound and a limit; no legal fixed-m=1 finite network attains it.',
        'Finite actual stars use k_H=b^2/(C-h^2/H), H>h^2/C.',
        '',
        'Sharp small-C supporting dual:',
        'r0 '+r0.decimal(42),
        'E(r_lo) '+Elo.decimal(45),
        'E(r_hi) '+Ehi.decimal(45),
        'lambda0 '+lam0.decimal(), 'eta0 '+eta0.decimal(),
        'sharp slope eta0/4 '+slope.decimal(),
        'ordinary one-pendant slope '+ordinary_slope.decimal(),
        'ratio of leading conductance savings '+ratio.decimal(),
        'For every legal finite network: J_rigid-J <= (eta0/4)*C.',
        'A legal 2-pendant sequence reaches this slope as C tends to 0,',
        'using H=C^(-2) and b=2*C*r0^2/(2+C*r0^2).',
    ]
    text='\n'.join(lines)+'\n'
    (HERE/'CERTIFIED_ENVELOPE.txt').write_text(text)
    print(text)

if __name__=='__main__':main()
