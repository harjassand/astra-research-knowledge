"""Full-state reference checks only for small baths, independently of envelope compiler.
The 16-state closure itself never builds the hidden states used for these audits.
"""
from fractions import Fraction as F
from pathlib import Path
from time import perf_counter
import json,numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve
from conditional_envelope import compile_envelope
BASE=Path(__file__).resolve().parent

def full_reference(n,m,R,feature='all_open',speed=F(1,10**9)):
 t=perf_counter();q=F(1,26);eps=F(1,10000);N=2**n;B=2**m
 nu=[F(2)**z.bit_count()*F(3)**sum(((z>>i)&1)==((z>>(i+1))&1) for i in range(m-1)) for z in range(B)]
 mg=[q**g.bit_count()*(1-q)**(n-g.bit_count()) for g in range(N)]
 h={'all_open':lambda g:int(g==N-1),'all_closed':lambda g:int(g==0),'first_open':lambda g:g&1}[feature]
 def w(g,z):return F(1)+(R-1)*h(g)*(z.bit_count()%2)
 rows=[];ir=[];ic=[];dat=[];mass=[]
 for z in range(B):
  for g in range(N):
   x=z*N+g;row=[];diag=F(0);wx=w(g,z);mass.append(mg[g]*nu[z]*wx)
   for i in range(n):
    gg=g^(1<<i);fac=F(1) if i==0 or ((g>>(i-1))&1) else eps
    rate=(1-q if (g>>i)&1 else q)*fac*min(wx,w(gg,z))/wx
    row.append((z*N+gg,-rate));diag+=rate
   for j in range(m):
    zz=z^(1<<j);rate=speed*(j+1)*(1+F(g.bit_count(),n))*min(F(1),nu[zz]/nu[z])*min(wx,w(g,zz))/wx
    row.append((zz*N+g,-rate));diag+=rate
   diag+=q*(1 if (g>>(n-1))&1 else eps);row.append((x,diag));rows.append(row)
   for y,a in row:ir.append(x);ic.append(y);dat.append(float(a))
 A=coo_matrix((dat,(ir,ic)),shape=(N*B,N*B)).tocsr();v=spsolve(A,np.ones(N*B));vf=[F.from_float(float(a)) for a in v]
 delta=max(abs(sum(a*vf[y] for y,a in row)-1) for row in rows);assert delta<1 and min(v)>0
 mean=sum(a*b for a,b in zip(mass,vf))/sum(mass);lo=mean/(1+delta);hi=mean/(1-delta)
 return {'bath_coordinates':m,'reference_states':N*B,'R':R,'feature':feature,'speed':str(speed),'lower_exact':str(lo),'upper_exact':str(hi),'mean':float(mean),'delta':float(delta),'seconds':perf_counter()-t}

if __name__=='__main__':
 out=[];envelopes={}
 for feature,m,R in [('all_open',m,100) for m in [0,2,4,6]]+[('all_closed',4,100),('first_open',4,100)]:
  if feature not in envelopes:envelopes[feature]=compile_envelope(feature=feature,R=R)
  c=envelopes[feature];r=full_reference(4,m,R,feature)
  assert F(c['lower_exact'])<=F(r['lower_exact'])<=F(r['upper_exact'])<=F(c['upper_exact'])
  r.update({'completion_lower':c['lower'],'completion_upper':c['upper'],'covered':True});out.append(r)
 (BASE/'conditional_reference_results.json').write_text(json.dumps({'references':out,'all_passed':True,'envelopes':envelopes},indent=2));print(json.dumps([{k:r[k] for k in ['bath_coordinates','feature','mean','completion_lower','completion_upper','seconds']} for r in out],indent=2))
