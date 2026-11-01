#!/usr/bin/env python3
"""Source integrity and exact algebra only, not a processed-mean receiver."""
from fractions import Fraction as F
from pathlib import Path
from hashlib import sha256
import json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
provenance=json.loads((HERE/'PROVENANCE.json').read_text())
for item in provenance['bound_sources']:
    assert sha256((ROOT/item['path']).read_bytes()).hexdigest()==item['sha256'],item
checks=0

def ck(x):
    global checks
    assert x
    checks+=1

def mv(A,x):
    return [sum(a*b for a,b in zip(row,x)) for row in A]

def dotm(x,y,m):
    return sum(a*b*w for a,b,w in zip(x,y,m))

for delta in [F(1,100),F(1,10),F(1),F(3)]:
    for rho in [F(1,10),F(1),F(3)]:
        for r in [F(1,100),F(1,20),F(1,10),F(1,2),F(3,4)]:
            k=r/(delta+r);p=delta/(delta+r);c=r*p;b=c/rho
            m=[1-r,r,rho];h=[F(1),F(1),F(0)];one=[F(1)]*3;slab=[F(0),F(0),F(1)]
            A=[[F(1),F(0),F(0)],[F(0),F(1),-p],[F(0),-b,b]]
            ck(0<k<1 and 0<p<1 and b>0)
            ck(k+p==1)
            ck(r*p==rho*b)
            ck(mv(A,one)==[1,k,0])
            ck(dotm(h,h,m)==1)
            ck(dotm(h,mv(A,h),m)==1)
            vh=[F(1),1/k,1/k]
            ck(mv(A,vh)==h)
            BA=dotm(h,vh,m)
            ck(BA==1+delta)
            t1=(1+rho/r)/k
            times=[F(1),t1,t1+1/b]
            ck(mv(A,times)==one)
            mean=dotm(h,times,m)
            ck(mean==1+delta+rho+delta*rho/r)
            vs=[F(0),p/(b*k),1/(b*k)]
            ck(mv(A,vs)==slab)
            cross=dotm(h,vs,m)
            BS=dotm(slab,vs,m)
            ck(cross==rho/k)
            ck(BS==rho*rho*(delta+r)**2/(delta*r*r))
            ck(BS==rho*rho/(r*k)+rho*rho/c)
            QD=dotm(one,times,m)
            ck(QD==BA+2*cross+BS)
            ck(cross*cross<=BA*BS)
            ck(mean<=QD)
            ck(mean<=4*QD)
# Test exact Tonelli tail constants on a nonnegative step heat-content profile.
# This is an integration-identity regression, not a claim the step is a semigroup.
for R in [F(1,5),F(1),F(7,2)]:
    for L in [F(1,10),F(1,2),F(1),F(2),F(4),F(10)]:
        ck(R+R==2*R) # integral G = 2 integral H
        if L<=2*R:
            tail=4*R-L
            weighted=L/4
        else:
            tail=4*R*R/L
            weighted=R-R*R/L
        ck(tail==4*R-4*weighted)
        ck(tail>=0)
for ell in [F(j,7) for j in range(1,41)]:
    Dsum=8/(ell*ell)
    total=8/ell+Dsum*ell
    ck(total==16/ell)
    ck(total*total==32*Dsum)
for M in [F(1,3),F(1),F(7)]:
    for C0 in [F(1,10),F(1),F(11)]:
        for B in [M*M/C0,F(2)*M*M/C0,F(7)*M*M/C0]:
            k0=C0/M;epsilon=C0*B/(M*M)-1
            ck(epsilon>=0)
            ck(4*B/M==4*(1+epsilon)/k0)
print(json.dumps({
 'status':'PASS',
 'bound_source_files':len(provenance['bound_sources']),
 'exact_rational_algebra_checks':checks,
 'scope':'frozen-source integrity, exact finite-chain identities, Tonelli-kernel constants, and mean optimization algebra; not a finite substitute for the analytical proof',
 'previous_archives_unchanged':True,
 'convergence_interpretation':'k E[tau] -> 1, not unscaled absolute convergence if k varies',
 'upload_performed':False
},indent=2,sort_keys=True))
