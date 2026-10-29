import numpy as np,json
from pathlib import Path
rng=np.random.default_rng(65312)
worst=0.;cases=0
for d in [2,3,5,9]:
 for rep in range(100):
  mats=[]
  for j in range(2):
   z=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d));m=(z+z.conj().T)/2;m*=10**rng.uniform(-1,.5)/np.linalg.norm(m,2);mats.append(m)
  A,B=mats;W=np.linalg.qr(rng.normal(size=(d,min(2,d)))+1j*rng.normal(size=(d,min(2,d))))[0]
  def sign(M):
   ev,U=np.linalg.eigh(M);return (U*np.where(ev>=0,1.,-1.))@U.conj().T
  R,S=sign(A),sign(B);I=np.eye(d)
  da=np.linalg.norm((A@A-I)@W,2);db=np.linalg.norm((B@B-I)@W,2)
  ka=np.linalg.norm(A@A@B-B@A@A,2);kb=np.linalg.norm(B@B@A-A@B@B,2)
  crossa=np.linalg.norm(B,2)*da+ka;crossb=np.linalg.norm(A,2)*db+kb
  assert np.linalg.norm((R-A)@W,2)<=da+1e-10
  assert np.linalg.norm((R-A)@B@W,2)<=crossa+1e-10
  assert np.linalg.norm((S-B)@A@W,2)<=crossb+1e-10
  expected=da+db+crossa+crossb+np.linalg.norm((A@B+B@A)@W,2)
  assert np.linalg.norm((R@S+S@R)@W,2)<=expected+1e-10
  cases+=1
# Explicit scalar lift of cyclic bins: good estimates in the physically relevant window.
liftcases=0
for J in [4,8,16,64]:
 w=4/J;g=w/100
 for u in [0,w/16,w/2,15*w/16]:
  for b in np.linspace(-1,1,41):
   for error in [-g,0,g]:
    estimate=b+error;label=int(np.floor((estimate-u)/w))%J
    lifts=[u+(label+k*J+.5)*w for k in [-2,-1,0,1]]
    centers=[c for c in lifts if c+w/2>=-1-g and c-w/2<=1+g]
    assert len(centers)==1
    assert abs(centers[0]-b)<=w+1e-12
    liftcases+=1
out={'reflection_cases':cases,'canonical_bin_lift_cases':liftcases,'all_passed':True,'scope':'Independent algebra/finite lift diagnostics; no approximate decoder or native instrument execution'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
