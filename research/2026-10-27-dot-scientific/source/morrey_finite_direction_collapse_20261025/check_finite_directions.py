#!/usr/bin/env python3
"""Exact algebra checks for the independent finite-direction audit."""
from fractions import Fraction as F
from itertools import product
import json
import sympy as s

u,v,w=s.symbols('u v w'); z=s.Matrix([u,v,w])
q=u*v+u*w+v*w
D=s.Matrix([[-1,2,2],[2,-1,2],[2,2,-1]])
axes=[s.eye(3)[:,i] for i in range(3)]
dirs=axes+[D[:,i] for i in range(3)]
P=s.expand(s.prod(D*z))
assert D.T*D==9*s.eye(3)
assert s.expand(q.subs(dict(zip((u,v,w),D*z/3)), simultaneous=True)-q)==0
assert P.coeff(u,1).coeff(v,1).coeff(w,1)==3
for d in dirs[3:]:
    op=lambda p:sum(d[i]*s.diff(p,z[i]) for i in range(3))
    assert s.expand(op(op(P)))==0
assert s.expand(u*u+v*v+w*w-s.Rational(3,4)*(v-w)**2-q-s.Rational(1,4)*(2*u-v-w)**2)==0
assert s.expand(u*u+v*v+w*w-s.Rational(9,4)*u*v+s.Rational(1,2)*q-s.Rational(15,16)*(u-v)**2-s.Rational(1,16)*(u+v+4*w)**2)==0
assert s.expand(u*u+v*v+w*w+4*v*w-2*q-(u-v-w)**2)==0

# Exact four-point phase quadrature in each phase.
xc=[F(3,5),F(-4,5),F(-3,5),F(4,5)]
xs=[F(4,5),F(3,5),F(-4,5),F(-3,5)]
yc=[F(5,13),F(-12,13),F(-5,13),F(12,13)]
ys=[F(12,13),F(5,13),F(-12,13),F(-5,13)]
points=[(xc[k],yc[l],xc[k]*yc[l]-xs[k]*ys[l]) for k,l in product(range(4),repeat=2)]
assert len(set(points))==16
for p in points:
    a,b,c=p
    assert 1-a*a-b*b-c*c+2*a*b*c==0
for d in dirs:
    dd=tuple(int(x) for x in d)
    for i in range(16):
        for j in range(i):
            delta=tuple(points[i][k]-points[j][k] for k in range(3))
            cross=(delta[1]*dd[2]-delta[2]*dd[1],delta[2]*dd[0]-delta[0]*dd[2],delta[0]*dd[1]-delta[1]*dd[0])
            assert any(cross), (i,j,dd)
moments={}
for degree in range(4):
    for a,b,c in product(range(degree+1),repeat=3):
        if a+b+c!=degree:continue
        val=sum((p[0]**a*p[1]**b*p[2]**c for p in points),F(0))/16
        expected=(F(1) if degree==0 else F(1,2) if degree==2 and 2 in (a,b,c) else F(1,4) if (a,b,c)==(1,1,1) else F(0))
        assert val==expected,((a,b,c),val,expected)
        moments[str((a,b,c))]=str(val)
mat=s.Matrix([[d[0]**2,d[1]**2,d[2]**2,d[0]*d[1],d[0]*d[2],d[1]*d[2]] for d in dirs[:5]])
assert mat.rank()==5
# D6 covariance exhaustion parameterization.
ss,rr,t=s.symbols('s r t')
a=[s.Rational(1,2)-rr-9*t,s.Rational(1,2)-9*t,s.Rational(1,2)-9*t]
b=[t-ss,t,t]
future=sum((a[i]*axes[i]*axes[i].T+b[i]*D[:,i]*D[:,i].T for i in range(3)),s.zeros(3))
assert s.simplify(future-(s.eye(3)/2-ss*D[:,0]*D[:,0].T-rr*axes[0]*axes[0].T))==s.zeros(3)
print(json.dumps({'status':'all exact checks passed','D5_rank':mat.rank(),'P_D':str(P),'source_moments_through_degree_3':moments,'fixed_points_scaled_by_65':[[str(65*x) for x in p] for p in points]},indent=2))
