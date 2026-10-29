"""Finite-field coordinate extractor diagnostic, not rational reconstruction certificate."""
import sys,json,time
from pathlib import Path
SRC=Path('producer-workspace/grevlex_value_oracle_20261029');sys.path.insert(0,str(SRC));from modular_quotient import *
OUT=Path(__file__).parent

def check(p):
 st=time.time();cv=lambda a:a.numerator*pow(a.denominator%p,-1,p)%p
 mats=[np.array([[cv(x) for x in c] for c in m],dtype=np.int64).T for m in raw];I=np.eye(n,dtype=np.int64);mul=lambda a,b:(a@b)%p
 powers=[[I,A,mul(A,A),mul(mul(A,A),A)] for A in mats];Q=(I+sum(a[2] for a in powers))%p;num=np.zeros_like(I)
 for e,c in terms:
  v=I
  for j,k in enumerate(e):
   if k:v=mul(v,powers[j][k])
  num=(num+cv(c)*v)%p
 L=mul(inv(Q,p),num)*pow(4,-1,p)%p;c=cp(p);B=I.copy();coeff=[[],[],[]]
 for k in range(n):
  for j,A in enumerate(mats):coeff[j].append(int(np.sum((A*B.T)%p)%p))
  B=(mul(L,B)+c[n-k-1]*I)%p
 assert not np.any(B)
 coeff=[a[::-1] for a in coeff];one=I[:,0];dp=np.zeros(n,dtype=np.int64)
 for k in range(n,0,-1):dp=(mul(L,dp)+(k*c[k]%p)*one)%p
 for A,cs in zip(mats,coeff):
  v=np.zeros(n,dtype=np.int64)
  for cc in cs[::-1]:v=(mul(L,v)+cc*one)%p
  assert np.array_equal(v,mul(A,dp))
 return {'prime':p,'seconds':time.time()-st,'coordinate_numerators_low_to_high':coeff,'all_three_quotient_identities_pass':True}
if __name__=='__main__':
 results=[check(p) for p in [10000019,10000103,10000121]]
 (OUT/'modular_coordinate_checks.json').write_text(json.dumps({'status':'MODULAR_DIAGNOSTIC_NOT_EXACT_RATIONAL_COORDINATE_CERTIFICATE','checks':results},indent=2)+'\n');print([(r['prime'],r['seconds']) for r in results])
