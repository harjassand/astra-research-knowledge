"""Exact three-cut exclusion of one specified rational normal profile.

Stdlib only. Rebuilds the literal F,p6 polynomials and exact directional
Hessians. Positive rational weights cancel BOTH free parameters, leaving
a strictly negative curvature. No finite-grid infeasibility premise.
"""
from fractions import Fraction as Q
from pathlib import Path
import json
import math
import time

OUT=Path(__file__).resolve().parent
ZERO=(0,0,0,0,0)


def pvar(i):
    e=[0]*5
    e[i]=1
    return {tuple(e):Q(1)}


def add(*ps):
    ans={}
    for p in ps:
        for e,v in p.items():
            ans[e]=ans.get(e,Q(0))+v
    return {e:v for e,v in ans.items() if v}


def scale(k,p):
    return {e:k*v for e,v in p.items() if k*v}


def mul(p,r):
    ans={}
    for e,v in p.items():
        for f,w in r.items():
            g=tuple(x+y for x,y in zip(e,f))
            ans[g]=ans.get(g,Q(0))+v*w
    return {e:v for e,v in ans.items() if v}


def sq(p):
    return mul(p,p)


def dd(p,direction):
    ans={}
    for e,v in p.items():
        for j in range(5):
            if e[j] and direction[j]:
                g=list(e)
                g[j]-=1
                g=tuple(g)
                ans[g]=ans.get(g,Q(0))+v*e[j]*direction[j]
    return {e:v for e,v in ans.items() if v}


def ev(p,point):
    return sum((v*math.prod(x**n for x,n in zip(point,e)) for e,v in p.items()),Q(0))


aa,bb,cc,dd0,ss=[pvar(j) for j in range(5)]
u=add(sq(aa),sq(cc))
v=add(sq(bb),sq(dd0))
w=add(mul(aa,bb),mul(cc,dd0))
q=add(mul(aa,dd0),scale(-1,mul(bb,cc)))
T=add(u,v)
x=add(u,scale(-1,v))
y=scale(2,w)
z=scale(2,q)
F=add(scale(Q(55220381,10**10),add(sq(u),sq(v))),
      scale(Q(114430029,625000000),mul(u,v)),
      scale(-Q(801761987,5000000000),sq(w)),
      scale(Q(118849817,4000000000),mul(q,x)))
p=add(scale(Q(6222019,200000000),mul(sq(x),x)),
      scale(Q(1686519911,10**10),mul(sq(x),z)),
      scale(Q(81172813,2000000000),mul(x,sq(z))),
      scale(Q(1726116771,10**10),mul(sq(z),z)),
      scale(Q(128626163,5000000000),mul(x,sq(y))),
      scale(Q(373321239,2000000000),mul(sq(y),z)))
delta=add(ss,scale(-1,q))
D=add(sq(T),sq(delta))
N0=add(mul(F,sq(T)),mul(p,delta))
Nalpha=mul(sq(T),sq(delta))
Nc=mul(sq(delta),add(sq(ss),sq(T)))


def curvature(num,point,direction):
    den=ev(D,point)
    assert den>0
    den1=ev(dd(D,direction),point)
    den2=ev(dd(dd(D,direction),direction),point)
    n=ev(num,point)
    n1=ev(dd(num,direction),point)
    n2=ev(dd(dd(num,direction),direction),point)
    return (den*den*n2-den*(2*n1*den1+n*den2)+2*n*den1*den1)/den**3


def solve(mat,rhs):
    # Exact Gaussian elimination; matrices are only3 by3.
    m=[list(row)+[value] for row,value in zip(mat,rhs)]
    n=len(m)
    for i in range(n):
        pivot=next(j for j in range(i,n) if m[j][i])
        m[i],m[pivot]=m[pivot],m[i]
        div=m[i][i]
        m[i]=[x/div for x in m[i]]
        for j in range(n):
            if j!=i:
                factor=m[j][i]
                m[j]=[x-factor*y for x,y in zip(m[j],m[i])]
    return [row[-1] for row in m]


def main():
    start=time.monotonic()
    inputs=[
        (['-.57','.29','.28','.72','-1.18'],['.90','.01','-.41','.07','-.13']),
        (['1','0','0','0','-2'],['1','0','0','.04','.04']),
        (['.89','-.04','-.39','-.25','-1.74'],['.92','-.03','-.39','.05','.04']),
    ]
    rows=[]
    for point,direction in inputs:
        pp,ddir=list(map(Q,point)),list(map(Q,direction))
        hh=[curvature(num,pp,ddir) for num in [N0,Nalpha,Nc]]
        rows.append({'point':list(map(str,pp)),'direction':list(map(str,ddir)),
                     'curvatures':list(map(str,hh)),
                     'display_curvatures':list(map(float,hh))})
    h=[list(map(Q,r['curvatures'])) for r in rows]
    weights=solve([[Q(1)]*3,[r[1] for r in h],[r[2] for r in h]],
                  [Q(1),Q(0),Q(0)])
    assert all(w>0 for w in weights)
    sums=[sum((w*r[j] for w,r in zip(weights,h)),Q(0)) for j in range(3)]
    assert sums[1:]==[Q(0),Q(0)]
    assert sums[0]<-Q(3,20)
    out={'status':'EXACT_THREE_CUT_RATIONAL_PROFILE_OBSTRUCTION',
         'rows':rows,'positive_weights':list(map(str,weights)),
         'display_weights':list(map(float,weights)),
         'weighted_curvature_coefficients':list(map(str,sums)),
         'display_constant':float(sums[0]),'seconds':time.monotonic()-start,
         'scope':'Rules out this fixed rational profile for ALL real alpha,c, '
                 'ALL sigma>0 and ALL epsilon>=0, by a necessary homogeneous limit. '
                 'Does not rule out general rational convex smooth lifts with s-dependent denominators.'}
    (OUT/'EXACT_PROFILE_OBSTRUCTION.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['status','display_weights','display_constant','seconds']},indent=2))


if __name__=='__main__':
    main()
