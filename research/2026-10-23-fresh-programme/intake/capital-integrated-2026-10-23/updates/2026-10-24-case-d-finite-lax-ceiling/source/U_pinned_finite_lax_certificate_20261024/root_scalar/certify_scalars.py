#!/usr/bin/env python3
"""Exact-rational enclosures for one prescribed Case-D SDP's scalar data.

Only the NPZ's IEEE endpoint numbers are inputs; they are converted to exact
dyadic rationals.  NumPy loads that data, but every bound below uses integers
and Fraction.  No floating quadrature or floating error estimate is used.
"""
from fractions import Fraction as F
from pathlib import Path
import json
import math
import numpy as np

HERE = Path(__file__).resolve().parent
RAW = HERE.parent / 'luna_boxcar/result/sdp_matrices_and_duals.npz'
BITS = 128
S = 1 << BITS
NSUB = 2048                # even; tighter scalar RHS enclosures for small cells
POLES = [(F(-3,4),F(1,4)),(F(-1,4),F(1,4)),(F(1,4),F(1,4)),
         (F(1,2),F(1,4)),(F(2,3),F(1,8)),(F(5,6),F(1,8)),(F(1),F(1,8))]

def floorf(x): return x.numerator // x.denominator
def ceilf(x): return -((-x.numerator) // x.denominator)
def mulq(iv,q):
    a,b=iv
    return ((floorf(a*q),ceilf(b*q)) if q>=0 else
            (floorf(b*q),ceilf(a*q)))
def add(a,b): return (a[0]+b[0],a[1]+b[1])
def neg(a): return (-a[1],-a[0])
def sq(a):
    lo,hi=a
    mn=0 if lo<=0<=hi else min(lo*lo,hi*hi)
    return (mn//S,(max(lo*lo,hi*hi)+S-1)//S)

def exp_neg(r):
    """Enclose exp(-r) at fixed scale S, for rational 0<=r<=100.

    y=r/128 lies in [0,1].  The degree-40 alternating Taylor sum is an
    upper bound and its next term bounds the remainder by 1/41! < 1/S.
    Interval term recurrence rounds outwards. Seven outward-rounded
    squarings then enclose exp(-r).
    """
    assert 0<=r<=100
    if not r: return (S,S)
    y=r/128
    yl,yh=floorf(y*S),ceilf(y*S)
    tl=th=S
    al=ah=S
    assert F(1,math.factorial(41)) < F(1,S)
    for n in range(1,41):
        den=S*n
        tl=tl*yl//den
        th=(th*yh+den-1)//den
        if n%2: al,ah=al-th,ah-tl
        else: al,ah=al+tl,ah+th
    al-=1
    assert 0<al<=ah
    for _ in range(7):
        al=al*al//S
        ah=(ah*ah+S-1)//S
    return al,ah

def g(v):
    el,eh=exp_neg(F(25,2)*(1-v)**2)
    return (floorf(F(11,100)*S)-ceilf(F(eh,2)),
            ceilf(F(11,100)*S)-floorf(F(el,2)))

def pack(iv):
    return {'lower':[iv[0].numerator,iv[0].denominator],
            'upper':[iv[1].numerator,iv[1].denominator],
            'width_preview':float(iv[1]-iv[0]),
            'midpoint_preview':float((iv[0]+iv[1])/2)}

def crossing_bracket():
    lo,hi=F(3,5),F(7,10)
    assert g(lo)[0]>0 and g(hi)[1]<0
    for _ in range(100):
        mid=(lo+hi)/2
        a,b=g(mid)
        if a>0: lo=mid
        elif b<0: hi=mid
        else: break
    return lo,hi

def integrate_cell(lo,hi,sign):
    h=hi-lo; c=(hi+lo)/2; step=h/NSUB
    # Layout: signed G, G^2, signed G*(v-c)^2, G, seven Re/Im a_u G.
    total=[(0,0) for _ in range(18)]
    for j in range(NSUB+1):
        v=lo+step*j
        gv=g(v)
        rv=mulq(gv,F(sign))
        vals=[rv,sq(gv),mulq(rv,(v-c)**2),gv]
        for a,b in POLES:
            den=(a-v)**2+b*b
            vals += [mulq(gv,v*(a-v)/den),mulq(gv,-v*b/den)]
        w=1 if j in (0,NSUB) else (4 if j%2 else 2)
        total=[add(t,mulq(x,F(w))) for t,x in zip(total,vals)]
    # Global fourth-derivative upper bounds on [-1,1].
    # |G^(j)| <= (1,25,1300,65000,3400000) for j=0..4.
    # (G^2)'''' <= .11*D4(12.5)+.25*D4(25) < 27000000,
    # D4(a)=12a^2+192a^3+256a^4. Product rule yields <4000000
    # for (v-c)^2 G since |v-c|<=1. For a_u G, |Im u|>=1/8,
    # |u|<=2: |a|<=8, |a^(n)|<=2*n!*8^(n+1), n>=1;
    # the fourth product-rule sum is <100000000.
    fourth=[3400000,27000000,4000000,3400000]+[100000000]*14
    out=[]
    for t,m4 in zip(total,fourth):
        err=h*step**4*F(m4,180)
        out.append((F(t[0],S)*step/3-err,F(t[1],S)*step/3+err))
    return out

def sumiv(xs): return (sum(x[0] for x in xs),sum(x[1] for x in xs))

def main():
    data=np.load(RAW)
    los=[F.from_float(float(x)) for x in data['cell_lo']]
    his=[F.from_float(float(x)) for x in data['cell_hi']]
    assert len(los)==36 and los[0]==-1 and his[-1]==1
    assert all(his[i]==los[i+1] for i in range(35))
    crlo,crhi=crossing_bracket()
    vc0=his[23]
    mismatch=max(abs(vc0-crlo),abs(vc0-crhi))
    cells=[]; raw=[]
    for i,(lo,hi) in enumerate(zip(los,his)):
        sign=1 if i<24 else -1
        ivs=integrate_cell(lo,hi,sign)
        # |G|<=1: integral |G| differs from signed G by at most twice
        # the sign-mismatch strip. Its second centered moment has |v-c|<=1.
        correction=2*mismatch if lo<=vc0<=hi else F(0)
        ivs[0]=(ivs[0][0],ivs[0][1]+correction)
        ivs[2]=(ivs[2][0],ivs[2][1]+correction)
        raw.append(ivs)
        cells.append({'i':i,'lo':[lo.numerator,lo.denominator],
                      'hi':[hi.numerator,hi.denominator],
                      'true_center':[(lo+hi).numerator,2*(lo+hi).denominator],
                      'r':pack(ivs[0]),'int_R2':pack(ivs[1]),'J2':pack(ivs[2])})
    q=sumiv([x[3] for x in raw])
    ap=sumiv([x[0] for x in raw[:24]])
    am=sumiv([x[0] for x in raw[24:]])
    # Sector masses also differ from the prescribed split by at most the
    # mismatch strip; this deliberately conservative padding is sufficient.
    ap=(ap[0]-mismatch,ap[1]+mismatch)
    am=(am[0]-mismatch,am[1]+mismatch)
    ell=[]
    for k,(a,b) in enumerate(POLES):
        ell.append({'pole_re':[a.numerator,a.denominator],
                    'pole_im':[b.numerator,b.denominator],
                    're':pack(sumiv([x[4+2*k] for x in raw])),
                    'im':pack(sumiv([x[5+2*k] for x in raw]))})
    out={'proof_arithmetic':'integer fixed-point and exact Fraction',
         'fixed_point_bits':BITS,'simpson_subintervals_per_cell':NSUB,
         'crossing':pack((crlo,crhi)),
         'prescribed_sign_mismatch_objective_upper':pack((F(0),mismatch)),
         'q':pack(q),'A_plus':pack(ap),'A_minus':pack(am),
         'B':pack((2*am[0],2*am[1])),'cells':cells,'ell':ell}
    HERE.mkdir(parents=True,exist_ok=True)
    (HERE/'scalar_enclosures.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'q_midpoint':out['q']['midpoint_preview'],
                     'q_width':out['q']['width_preview'],
                     'B_midpoint':out['B']['midpoint_preview'],
                     'B_width':out['B']['width_preview'],
                     'max_cell_scalar_width':max(float(x[k][1]-x[k][0]) for x in raw for k in range(3)),
                     'max_ell_component_width':max(p[c]['width_preview'] for p in ell for c in ['re','im']),
                     'mismatch_upper':float(mismatch)},indent=2))

if __name__=='__main__': main()
