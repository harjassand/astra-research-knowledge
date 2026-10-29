import numpy as np, json, math
from fractions import Fraction as F
from pathlib import Path
rng=np.random.default_rng(1247); rows=[]
for k,r,D in [(2,2,7),(2,3,9),(3,2,8)]:
 for eta in [0,.2,.95]:
  d=k*r; z=rng.normal(size=(D,D))+1j*rng.normal(size=(D,D));U=np.linalg.qr(z)[0];V=U[:,:d]
  sig=np.arange(1,r+1,dtype=float);sig/=sig.sum();eig=np.r_[(1-eta)*np.tile(sig,k)/k+eta/D,np.repeat(eta/D,D-d)]
  # Explicit QPE amplitudes, arbitrary threshold in the signal to test transition-band junk reweighting.
  M=64;phase=eig/2;y=np.arange(M);a=np.mean(np.exp(2j*np.pi*np.arange(M)[:,None,None]*(phase[None,None,:]-y[None,:,None]/M)),axis=0)
  rep=np.where(y/M>=.75,y/M-1,y/M); accept=rep>=.1
  Ks=[(U*a[j])@U.conj().T for j in range(M) if accept[j]]
  f=np.sum(abs(a[accept])**2,axis=0);fp=f[:r];fout=f[-1] if D>d else 0
  t=(1-eta)*sum(sig*fp);b=eta*k*sum(fp)/D;c=eta*(D-d)*fout/D
  residual=0
  for i in range(k):
   for j in range(k):
    E=np.zeros((k,k));E[i,j]=1
    signal=V@np.kron(E,np.diag(sig))@V.conj().T
    source=(1-eta)*signal+eta*np.trace(E)*np.eye(D)/D
    got=sum(K@source@K.conj().T for K in Ks)
    expected=(1-eta)*V@np.kron(E,np.diag(sig*fp))@V.conj().T+eta*np.trace(E)*(U*f)@U.conj().T/D
    residual=max(residual,float(np.linalg.norm(got-expected)),float(abs(np.trace(got)-(t+b+c)*np.trace(E))))
  assert residual<1e-12;rows.append(dict(k=k,r=r,D=D,eta=eta,all_matrix_unit_residual=residual))
# Exact readiness cap bounds and flags/success-state factorization witness.
capchecks=[]
for p in [F(1,8),F(1,2),F(3,4)]:
 for n in [1,2,4]:
  Delta=2*p if p<=F(1,2) else F(1)
  L=math.ceil(4*n/Delta)
  fail=sum(F(math.comb(L,j))*p**j*(1-p)**(L-j) for j in range(n))
  assert fail<=F(1,2);capchecks.append(str(fail))
# Universal conservative budget coefficient with Delta<1 and n>=1.
coef=F(1,64)+F(1,256)+F(3,64)+F(1,64)+F(1,64)+F(1,512)+F(1,16)+F(1,16)
assert coef<1
res=dict(physical_QPE_transfer=rows,exact_batch_cap_checks=capchecks,universal_overhead_coefficient_upper=str(coef),scope='All operator-basis transfer and exact cap/budget diagnostics; no physical DME+recovery end-to-end execution')
Path(__file__).with_suffix('.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res,indent=2))
