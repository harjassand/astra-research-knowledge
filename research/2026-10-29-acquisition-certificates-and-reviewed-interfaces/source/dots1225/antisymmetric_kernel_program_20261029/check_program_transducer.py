from fractions import Fraction as F
import itertools,json,math
from pathlib import Path
import numpy as np
# Quadratic polynomials in nine real rotation entries, represented on ordered two-copy basis.
def add(a,b,s=F(1)):
 c=a.copy()
 for k,v in b.items():c[k]=c.get(k,F(0))+s*v
 return {k:v for k,v in c.items() if v}
def cof(i,j):
 rr=[r for r in range(3) if r!=i];cc=[c for c in range(3) if c!=j];s=(-1)**(i+j)
 return {(3*rr[0]+cc[0],3*rr[1]+cc[1]):F(s),(3*rr[0]+cc[1],3*rr[1]+cc[0]):F(-s)}
C=[[cof(i,j) for j in range(3)] for i in range(3)];norm={(j,j):F(1,3) for j in range(9)}
Q=[[{} for j in range(4)] for i in range(4)]
signs=[[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]]
for i in range(4):
 Q[i][i]=norm.copy()
 for j in range(3):Q[i][i]=add(Q[i][i],C[j][j],F(signs[i][j]))
for i,j,a,b,s in [(0,1,(2,1),(1,2),-1),(0,2,(0,2),(2,0),-1),(0,3,(1,0),(0,1),-1),(1,2,(0,1),(1,0),1),(1,3,(0,2),(2,0),1),(2,3,(1,2),(2,1),1)]:
 Q[i][j]=add(C[a[0]][a[1]],C[b[0]][b[1]],F(s));Q[j][i]=Q[i][j]
A=[[F(0) for _ in range(81)] for __ in range(16)]
for i in range(4):
 for j in range(4):
  for (a,b),v in Q[i][j].items():A[4*i+j][9*a+b]+=v/4
fro2=sum(x*x for row in A for x in row);scale=math.isqrt(fro2.numerator//fro2.denominator)
while scale*scale<fro2:scale+=1
An=np.array(A,float);rng=np.random.default_rng(202610291020);maxerr=0.;cases=[]
for _ in range(100):
 q=rng.normal(size=4);q/=np.linalg.norm(q);w,x,y,z=q
 R=np.array([[1-2*(y*y+z*z),2*(x*y-w*z),2*(x*z+w*y)],[2*(x*y+w*z),1-2*(x*x+z*z),2*(y*z-w*x)],[2*(x*z-w*y),2*(y*z+w*x),1-2*(x*x+y*y)]])
 c=R.ravel()/np.sqrt(3);out=An@np.kron(c,c)/scale;target=np.kron(q,q)/(3*scale);err=np.linalg.norm(out-target);maxerr=max(maxerr,err);assert err<1e-14
 cases.append(float(np.vdot(out,out).real))
root=Path(__file__).parent
(root/'transducer_matrix.json').write_text(json.dumps(dict(matrix=[[str(x) for x in row] for row in A],frobenius_squared=str(fro2),coarse_frobenius_contraction_scale=scale,coarse_success_probability=str(F(1,9*scale*scale))),indent=2)+'\n')
(root/'transducer_checks.json').write_text(json.dumps(dict(cases=100,max_residual=maxerr,operator_norm_numeric=float(np.linalg.norm(An,2)),frobenius_squared=str(fro2),safe_scale=scale,exact_success=str(F(1,9*scale*scale)),observed_success_range=[min(cases),max(cases)]),indent=2)+'\n')
print(fro2,scale,F(1,9*scale*scale),maxerr,np.linalg.eigvalsh(An@An.T))
