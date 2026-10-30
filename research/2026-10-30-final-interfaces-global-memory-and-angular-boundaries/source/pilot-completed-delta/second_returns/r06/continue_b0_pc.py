"""Acquire and verify an actual rational PC-support/lift family through B0.

Finite strict positivity in b0_pc_certificate.json then proves a nonempty
open polyconvex arc by continuity. No interval wider than this existence
statement is inferred from samples.
"""
from pathlib import Path
import json,time
import sympy as S

HERE=Path(__file__).resolve().parent;start=time.time()
a,b,c,d,u=S.symbols('a b c d u',real=True);A=(a,b,c,d)
field=S.QQ.frac_field(u)
B=1-3*u*u;H=1+3*u*u;beta=B/H;r=4-12*u/H
T=sum(x*x for x in A);q=a*d-b*c;X=a*a+c*c-b*b-d*d
F=T*T+4*(r-1)*q*q+4*beta*q*X
grad=S.Matrix([S.diff(F,x) for x in A]);HF=S.hessian(F,A)
E=S.Matrix([[0,0,0,1],[0,0,-1,0],[0,-1,0,0],[1,0,0,0]])
L=S.Rational(23,5);mu=4*r+8-4*u*L/B
BB=L*S.diag(1,-1,1,-1)+mu*E/2
Cexpr=(2*F*HF-grad*grad.T-4*F*q*BB).subs({a:1,c:0})
C=[[S.Poly(Cexpr[i,j],b,d,domain=field) for j in range(4)] for i in range(4)]
g=S.Poly(B*B*(1-b*b)**2-(1-4*u+3*u*u)*H*(1+b*b)**2,b,domain=field).monic()
K=[-B*(u*(1-b*b)+H*b*b)*(1+b*b),B*b*(H-u*(1-b*b))*(1+b*b),
   B*B*b*(1-b*b)-u*H*b*(1+b*b)**2,B*B*b*b*(1-b*b)+u*H*(1+b*b)**2]
K=[S.Poly(x,b,domain=field).rem(g) for x in K]
kinv=S.invert(K[0],g);k=[(x*kinv).rem(g) for x in K]
k=[S.Poly(x.as_expr(),b,d,domain=field) for x in k]
assert k[0]==S.Poly(1,b,d,domain=field)
zero=S.Poly(0,b,d,domain=field);dp=S.Poly(d,b,d,domain=field);gp=S.Poly(g.as_expr(),b,d,domain=field)
cp00=sum((k[i]*C[i][j]*k[j] for i in range(4) for j in range(4)),zero)
c0=S.Poly(cp00.as_expr().subs(d,0),b,d,domain=field)
c1=S.Poly(S.diff(cp00.as_expr(),d).subs(d,0),b,d,domain=field)
MM=[[zero for _ in range(5)] for _ in range(5)]
MM[1][1],rem=c0.div(gp*gp);assert rem.is_zero
MM[0][1],rem=c1.div(gp.mul_ground(2));assert rem.is_zero;MM[1][0]=MM[0][1]
MM[0][0],rem=(cp00-c0-dp*c1).div(dp*dp);assert rem.is_zero
for j in range(1,4):
    cross=sum((k[i]*C[i][j] for i in range(4)),zero)
    v0=S.Poly(cross.as_expr().subs(d,0),b,d,domain=field)
    MM[0][j+1],rem=(cross-v0).div(dp);assert rem.is_zero;MM[j+1][0]=MM[0][j+1]
    MM[1][j+1],rem=v0.div(gp);assert rem.is_zero;MM[j+1][1]=MM[1][j+1]
    for i in range(1,4):MM[i+1][j+1]=C[i][j]
assert cp00==dp*dp*MM[0][0]+(dp*gp*MM[0][1]).mul_ground(2)+gp*gp*MM[1][1]
for j in range(1,4):
    assert sum((k[i]*C[i][j] for i in range(4)),zero)==dp*MM[0][j+1]+gp*MM[1][j+1]

seed=json.loads((HERE/'b0_pc_certificate.json').read_text());center=S.Rational(1,6)
def literal_at_center(pp):
    return {powers:S.cancel(co.subs(u,center)) for powers,co in pp.terms() if co.subs(u,center)!=0}
def actual(raw):return {(ib,id_):S.Rational(n,dd) for ib,id_,n,dd in raw if n}
for name,matrix in (('C',C),('M',MM)):
    for i,row in enumerate(matrix):
        for j,pp in enumerate(row):assert literal_at_center(pp)==actual(seed[name][i][j])
for i,pp in enumerate(k):assert literal_at_center(pp)==actual(seed['kernel'][i])
all_coeffs=[co for mat in (C,MM) for row in mat for pp in row for _,co in pp.terms()]+[co for pp in k for _,co in pp.terms()]
denominators=set()
for co in all_coeffs:
    den=S.factor(S.denom(S.cancel(co)));assert den.subs(u,center)!=0;denominators.add(str(den))

def pack(pp):return [[ib,id_,str(S.factor(co))] for (ib,id_),co in pp.terms()]
out={'parameter':'u','center':'1/6','L':'23/5','M_lambda':str(S.factor(mu)),
     'g':str(S.factor(g.as_expr())),
     'kernel': [pack(pp) for pp in k],
     'C':[[pack(pp) for pp in row] for row in C],
     'M':[[pack(pp) for pp in row] for row in MM],
     'coefficient_denominators_nonzero_at_center':sorted(denominators),
     'full_rational_family_acquired':True,'generic_lift_identity_exact':True,
     'center_matches_verified_literal_certificate':True,
     'conclusion':'An actual rational support/lift family through B0 with strict finite Bernstein inequalities at the center proves an open polyconvex boundary arc about u=1/6.',
     'seconds':time.time()-start}
(HERE/'b0_pc_continuation.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({key:out[key] for key in ('M_lambda','full_rational_family_acquired','generic_lift_identity_exact','center_matches_verified_literal_certificate','seconds')},indent=2))
