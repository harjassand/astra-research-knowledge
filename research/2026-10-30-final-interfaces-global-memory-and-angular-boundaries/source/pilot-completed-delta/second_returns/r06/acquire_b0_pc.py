"""Construct a genuine global minor-support candidate and its acoustic lift.

The polynomial support rule is lambda(A)=L X(A)+(216/13-8L/11)det A.
No positivity follows from imposing the forced acoustic value; positivity is
acquired and checked separately on the actual matrices.
"""
from pathlib import Path
import json,time,sys
import sympy as S
import numpy as np

HERE=Path(__file__).resolve().parent;start=time.time()
a,b,c,d,L=S.symbols('a b c d L',real=True);A=(a,b,c,d)
T=sum(x*x for x in A);q=a*d-b*c;X=a*a+c*c-b*b-d*d
F=T*T+S.Rational(60,13)*q*q+S.Rational(44,13)*q*X
grad=S.Matrix([S.diff(F,x) for x in A]);HF=S.hessian(F,A)
E=S.Matrix([[0,0,0,1],[0,0,-1,0],[0,-1,0,0],[1,0,0,0]])
DD=S.diag(1,-1,1,-1)
B=L*DD+(S.Rational(216,13)-S.Rational(8,11)*L)*E/2
C=(2*F*HF-grad*grad.T-4*F*q*B).subs({a:1,c:0}).applyfunc(S.expand)
u=S.Rational(1,6);bb=1-3*u*u;hh=1+3*u*u
g=S.Poly(bb*bb*(1-b*b)**2-(1-4*u+3*u*u)*hh*(1+b*b)**2,b).monic().as_expr()
K=[-bb*(u*(1-b*b)+hh*b*b)*(1+b*b),bb*b*(hh-u*(1-b*b))*(1+b*b),
   bb*bb*b*(1-b*b)-u*hh*b*(1+b*b)**2,bb*bb*b*b*(1-b*b)+u*hh*(1+b*b)**2]
K=[S.rem(x,g,b) for x in K]
kinv=S.invert(K[0],g,b);k=S.Matrix([S.rem(x*kinv,g,b) for x in K]);assert k[0]==1
cp00=S.expand((k.T*C*k)[0]);poly=S.Poly(cp00,d)
c0=poly.nth(0);c1=poly.nth(1)
M=S.zeros(5)
M[1,1],rem=S.div(c0,g*g,b);assert rem==0
M[0,1],rem=S.div(c1,2*g,b);assert rem==0;M[1,0]=M[0,1]
M[0,0]=S.cancel((cp00-c0-d*c1)/(d*d)).expand()
for j in range(1,4):
    cross=S.expand((k.T*C)[j]);v0=S.Poly(cross,d).nth(0)
    M[0,j+1]=M[j+1,0]=S.cancel((cross-v0)/d).expand()
    M[1,j+1],rem=S.div(v0,g,b);assert rem==0;M[j+1,1]=M[1,j+1]
    for i in range(1,4):M[i+1,j+1]=C[i,j]
Q=S.eye(4);Q[:,0]=k
liftD=S.zeros(5,4);liftD[0,0]=d;liftD[1,0]=g
for j in range(1,4):liftD[j+1,j]=1
assert all(S.expand(x)==0 for x in Q.T*C*Q-liftD.T*M*liftD)
fn=S.lambdify((b,d,L),M,'numpy')
cc=-S.Poly(g,b).nth(2);bzero=float(S.sqrt((cc-S.sqrt(cc*cc-4))/2))
stats=[]
for ll in (3,3.5,4,4.5,4.6,5,5.5,6):
    eig=np.linalg.eigvalsh(np.array(fn(bzero,0,ll),float))
    stats.append({'L':ll,'lift_eigenvalues_at_zero':list(map(float,eig))})
print(json.dumps({'g':str(g),'kernel':[str(x) for x in k],'bzero':bzero,'local_lift_tests':stats,'seconds':time.time()-start},indent=2),flush=True)
chosen=S.Rational(sys.argv[1]) if len(sys.argv)>1 else S.Rational(23,5)
CC=C.subs(L,chosen);MM=M.subs(L,chosen)
def literal(pp):return [[ib,id_,int(co.p),int(co.q)] for (ib,id_),co in S.Poly(pp,b,d).terms()]
out={'beta':'11/13','r':'28/13','L':str(chosen),'M_lambda':str(S.Rational(216,13)-S.Rational(8,11)*chosen),
     'g':literal(g),'w':literal(d),'kernel':[literal(x) for x in k],
     'C':[[literal(x) for x in row] for row in CC.tolist()],
     'M':[[literal(x) for x in row] for row in MM.tolist()],
     'acoustic_b_approx':bzero,'lift_identity_exact':True,
     'local_tests_L':stats,'seconds':time.time()-start}
(HERE/'b0_pc_candidate.json').write_text(json.dumps(out,indent=2)+'\n')
