"""Independent Kraus replay of the reconstructed full two-site state."""
import sys
sys.dont_write_bytecode=True
import json,time
import numpy as np
from werner_unraveling import nonnegative_factor,prime_at_least,CSTAR,BASE

def kraus(d,c):
 s=c*d-1;out=[]
 for i in range(d):
  K=np.zeros((d,d),complex);K[i,i]=np.sqrt((c-1)/s);out.append(K)
 for i in range(d):
  for j in range(i+1,d):
   K=np.zeros((d,d),complex);K[i,j]=K[j,i]=np.sqrt((c-1)/(2*s));out.append(K)
   K=np.zeros((d,d),complex);K[i,j]=np.sqrt((c+1)/(2*s));K[j,i]=-K[i,j];out.append(K)
 assert np.max(abs(sum((K.conj().T@K for K in out))-np.eye(d)))<1e-13
 return out

def reconstruction(v,d,c):
 U,x,Vh=np.linalg.svd(v.reshape(d,d));B=Vh.T;lam=x*x
 factors,A=nonnegative_factor(lam,c);p=prime_at_least(d);omega=np.exp(2j*np.pi/p)
 out=np.zeros((d*d,d*d),complex)
 for k in range(factors.shape[1]):
  r=np.sqrt(factors[:,k])
  for a in range(p):
   for b in range(p):
    z=np.array([omega**((a*i+b*i*i)%p) for i in range(d)])
    left=U.conj()@(r*z);right=B.conj()@(r*z.conj());product=np.kron(left,right)
    out+=np.outer(product,product.conj())/(p*p)
 for i in range(d):
  for j in range(d):
   if i!=j:
    weight=c*c-c*(lam[i]+lam[j])-x[i]*x[j]
    assert weight>=-1e-11
    w=np.kron(U[:,i].conj(),B[:,j].conj());out+=weight*np.outer(w,w.conj())
 return out/(c*d-1)**2

def run():
 start=time.monotonic();rng=np.random.default_rng(870237);records=[]
 for d in (2,3,4,5):
  for c in (CSTAR,1.4,1.8):
   errors=[]
   for trial in range(8):
    v=rng.normal(size=d*d)+1j*rng.normal(size=d*d);v/=np.linalg.norm(v)
    actual=np.zeros((d*d,d*d),complex)
    Ks=kraus(d,c)
    for K in Ks:
     for L in Ks:
      w=np.kron(K,L)@v;actual+=np.outer(w,w.conj())
    predicted=reconstruction(v,d,c)
    errors.append(float(np.max(abs(actual-predicted))))
   assert max(errors)<1e-11
   records.append(dict(d=d,c=float(c),random_pure_inputs=8,max_full_matrix_error=max(errors)))
 result=dict(cases=records,total_inputs=96,verification='direct local Kraus action versus complete rotated phase-mixture state',
  elapsed_seconds=time.monotonic()-start)
 (BASE/'results'/'FULL_UNRAVELING_VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(dict(total_inputs=96,max_error=max(r['max_full_matrix_error'] for r in records),elapsed_seconds=result['elapsed_seconds']),indent=2))

if __name__=='__main__':run()
