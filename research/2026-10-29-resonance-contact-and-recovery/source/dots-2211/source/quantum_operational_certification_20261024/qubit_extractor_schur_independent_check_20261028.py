"""Exact Schur certificate sharpness for physical rotated unitary channels."""
from pathlib import Path
import sympy as s,json
I=s.eye(2);P=[s.Matrix([[0,1],[1,0]]),s.Matrix([[0,-s.I],[s.I,0]]),s.diag(1,-1)];k=s.kronecker_product
PB=(s.eye(4)+sum((k(p.T,p) for p in P),s.zeros(4)))/4
rows=[]
for m in [3,5,10]:
 c=s.Rational(m*m-1,m*m+1);r=s.Rational(2*m,m*m+1);U=s.Matrix([[c,-r],[r,c]])
 C=[U*p*U.H/2 for p in P];Y=sum(((a*b+b*a)/2 for a,b in zip(C,P)),s.zeros(2));H=sum((k(p.T,a) for p,a in zip(P,C)),s.zeros(4));Q=k(I,Y)-H
 Z=(s.eye(4)-PB)*Q*PB;W=(s.eye(4)-PB)*Q*(s.eye(4)-PB);kap=2*(c*c-r*r);z2=4*c*c*r*r;lam=2*r*r
 assert PB*Q*PB==s.zeros(4)
 assert max((Z.H*Z).eigenvals())==z2
 assert all(x>=0 for x in (W-kap*(s.eye(4)-PB)).eigenvals())
 assert lam*(kap+lam)==z2 and all(x>=0 for x in (Q+lam*s.eye(4)).eigenvals())
 Fe=(1+sum(s.trace(a*b) for a,b in zip(C,P)))/4
 assert 1-Fe==2*lam/4
 rows.append({'m':m,'transverse_gap':str(kap),'stationarity_norm_squared':str(z2),'dual_shift':str(lam),'exact_regret':str(1-Fe),'Schur_bound_sharp':True})
out={'status':'PASS_EXACT_SCHUR_SHARPNESS','source_outcomes':0,'cases':rows,'scope':'Exact source-disabled proof fixture, not sampled holdout or executed SDP.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'])
