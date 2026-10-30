"""Exact rational continuation template for original N901 heat certificates.

This file prepares algebra, not a QC assertion. Parameter positivity must
be verified separately over the stated intervals.
"""
from pathlib import Path
from itertools import combinations
import sys,pickle,time,json
import numpy as np,sympy as s
from sympy.polys.matrices import DomainMatrix
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'work'));import n901_heat as m
rr=s.symbols('r');N=3*rr*rr+8*rr+4;pp=-3*N/((rr+1)**2*(2*rr+1));ww=N/(rr+1);L=s.zeros(12,14)
rows=[[(2,0,1),(0,0,-2)],[(1,0,1),(0,1,-pp)],[(2,1,1),(0,1,-2)],[(3,0,1),(0,1,-ww)]]+[[ (a,h,1)] for a,h in ((1,1),(1,2),(1,3),(2,2),(2,3),(3,1),(3,2),(3,3))]
for i,row in enumerate(rows):
 for a,h,c in row:L[i,m.features.index((a,h))]=c
gp=[(i,i) for i in range(12)]+list(combinations(range(12),2));A=s.zeros(104,len(gp)+30)
for k in range(100):
 B=s.Matrix([[int(m.gc[k,i,j]) for j in range(14)] for i in range(14)]);B=L*B*L.T
 for j,(a,b) in enumerate(gp):A[k,j]=s.cancel(B[a,b]*(1 if a==b else 2))
 for j in range(30):A[k,len(gp)+j]=-int(m.oc[k,j])
for k in range(4):
 for j in range(30):A[100+k,len(gp)+j]=int(m.closure[k,j])
p,q,w=s.symbols('p q w');sig=rr+1;kap=rr*(rr+2)/3;al=3*rr/(8*(rr+2));be=rr*(rr-1)/6
Q=(al*((sig*p-w)**2+(sig+1)**2*q*q)**2+be*(q*q+sig*sig*p*p)**2+sig*sig*(p*w-q*q)**2+rr*sig*(q*q+sig*sig*p*p)*(p*w-q*q))/(kap*sig*sig)
P=s.Poly(Q-p*p*q-q**3/sig**2+p*p,p,q,w);HH=s.hessian(P.as_expr(),(p,q,w));B=s.zeros(4)
for ids in (m.p1,m.p2):
 for i in range(3):
  for j in range(3):B[ids[i],ids[j]]+=HH[i,j]
BP=[[s.Poly(B[i,j],p,q,w) for j in range(4)] for i in range(4)];raw=s.Matrix([s.cancel(BP[i][j].coeff_monomial(pw)*(1 if i==j else 2)) for pw,i,j in m.rowkeys]+[0]*4)
if __name__=='__main__':
 start=time.perf_counter();print('built',A.shape,flush=True);T0,piv=A.subs(rr,1).row_join(raw.subs(rr,1)).rref();assert len(gp)+30 not in piv;free=[i for i in range(A.cols) if i not in piv];order=list(piv)+free;AA=A[:,order].row_join(raw);DM=DomainMatrix.from_Matrix(AA).to_field();print('field built',time.perf_counter()-start,flush=True);T,pi=DM.rref();T=T.to_Matrix();assert pi==tuple(range(len(piv)));out=[None]*A.cols
 for k,i in enumerate(piv):out[i]=[s.cancel(T[k,-1])]+[s.cancel(-T[k,len(piv)+j]) for j in range(len(free))]
 for j,i in enumerate(free):out[i]=[s.Integer(0)]+[s.Integer(j==k) for k in range(len(free))]
 path=root/'work/n901_parameter_template.pickle';path.write_bytes(pickle.dumps({'r':rr,'Gram_pairs':gp,'free':free,'solution':out,'L':L,'A':A,'raw':raw}));print(json.dumps({'rank':len(piv),'free':free,'seconds':time.perf_counter()-start,'template':str(path)}),flush=True)
