"""Rationalize a facially reduced proposal for the original N901 gate.

The output is checked coefficient by coefficient and with exact rational
positive pivots. The independent receiver must rebuild the source itself.
"""
from pathlib import Path
from fractions import Fraction as R
from itertools import combinations
import sys,json
import sympy as s,numpy as np
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'work'));import n901_heat as m
def rat(x):return s.Rational(R(x).numerator,R(x).denominator)
def rationalize(rec):
 rr=R(rec['r']);rows=rec['face'];L=s.zeros(12,14)
 for i,row in enumerate(rows):
  for a,h,c in row:L[i,m.features.index((a,h))]=rat(c)
 gp=list(combinations(range(12),2));gp=[(i,i) for i in range(12)]+gp
 A=s.zeros(104,len(gp)+30)
 # Coefficient matching in the 14 original polynomial features.
 for k in range(100):
  B=s.Matrix([[int(m.gc[k,i,j]) for j in range(14)] for i in range(14)]);B=L*B*L.T
  for j,(a,b) in enumerate(gp):A[k,j]=B[a,b]*(1 if a==b else 2)
  for j in range(30):A[k,len(gp)+j]=-int(m.oc[k,j])
 for k in range(4):
  for j in range(30):A[100+k,len(gp)+j]=int(m.closure[k,j])
 lead,cub,quad=m.source(rr);P=m.add(lead,cub,quad);HH=[[m.diff(m.diff(P,i),j) for j in range(3)] for i in range(3)];B=[[{} for j in range(4)] for i in range(4)]
 for ids in (m.p1,m.p2):
  for i in range(3):
   for j in range(3):B[ids[i]][ids[j]]=m.add(B[ids[i]][ids[j]],HH[i][j])
 raw=[B[i][j].get(pw,R(0))*(1 if i==j else 2) for pw,i,j in m.rowkeys]+[R(0)]*4;rhs=s.Matrix(list(map(rat,raw)));T,piv=A.row_join(rhs).rref();assert len(gp)+30 not in piv
 base=np.array([rec['Gram'][i][j] for i,j in gp]+rec['closed_two_form']);free=[i for i in range(len(base)) if i not in piv];out=[s.Rational(0)]*len(base)
 for i in free:out[i]=rat(R(float(base[i])).limit_denominator(2**18))
 for k,i in enumerate(piv):out[i]=T[k,-1]-sum(T[k,j]*out[j] for j in free)
 assert A*s.Matrix(out)==rhs
 G=[[R(0)]*12 for i in range(12)]
 for (i,j),v in zip(gp,out):G[i][j]=G[j][i]=R(int(v.p),int(v.q))
 margin=R(1,10000);m.b.pd([[v-(margin if i==j else 0) for j,v in enumerate(row)] for i,row in enumerate(G)])
 return {'r':str(rr),'face':rows,'Gram':[[str(v) for v in row] for row in G],'closed_two_form':[str(v) for v in out[len(gp):]],'PD_margin':str(margin),'matching_rank':len(piv),'affine_free_parameters':len(free)}
if __name__=='__main__':
 records=json.loads((root/'work/n901_facial.json').read_text())['records'];rr=sys.argv[1] if len(sys.argv)>1 else '1';rec=next(v for v in records if v['r']==rr);out=rationalize(rec);dest=root/'outputs/n901_gate';dest.mkdir(exist_ok=True);(dest/f'certificate_r{rr.replace("/","_")}.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('face','Gram','closed_two_form')}))
