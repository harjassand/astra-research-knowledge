import numpy as np,json
from pathlib import Path
rng=np.random.default_rng(28102026);Z=np.diag([1.,-1.]);phi=np.array([1,0,0,1])/np.sqrt(2)
def U(t):return np.diag(np.exp(-1j*t*np.array([1.,-1.])))
def infid(K,t):return 1-sum(abs(np.trace(k@U(t)))**2 for k in K)/4
minslack=1.;checks=0
for J in [1,2,4,16]:
 for N in [1,8,128,4096]:
  d=1/(4*max(J,np.sqrt(N)))
  lower=(1/(8*np.pi**2))*min(1,J*J/N)
  exact_bound=(1-np.sqrt(N)*np.sin(2*d))*np.sin(J*d)**2
  assert exact_bound>=lower-1e-14
  for _ in range(50):
   x=rng.normal(size=(8,2))+1j*rng.normal(size=(8,2));q,_=np.linalg.qr(x);K=[q[2*i:2*i+2] for i in range(4)]
   slack=infid(K,J*d)+infid(K,-J*d)-(1-abs(np.cos(2*J*d)))
   assert slack>=-1e-12;minslack=min(minslack,slack);checks+=1
rows=[];sums={};calls=0;banks=2048
for p in [0.,.25]:
 a=1-2*p
 for N in [256,1024]:
  Jmax=16;K=2**int(np.ceil(np.log2(max(4,(22/7)*N*(np.ceil(np.sqrt(N))+Jmax)))))
  # theta=0 is a genuine grid world. Each bank is independently acquired.
  L=rng.integers(0,K,size=(banks,N));angles=2*np.pi*L/K
  Y=np.where(rng.random((banks,N))<(1+a*np.cos(angles))/2,1.,-1.)
  S=(Y*np.exp(1j*angles)).sum(axis=1);t=np.angle(S)
  assert np.min(np.abs(S))>1e-12
  sums[f'p{p}_N{N}']=S;calls+=banks*N
  for J in [1,2,4,8,16]:
   losses=np.sin(J*t/2)**2
   rows.append({'p':p,'N':N,'K':K,'J':J,'banks':banks,'mean_reused_phase_loss':float(losses.mean()),'standard_error':float(losses.std(ddof=1)/np.sqrt(banks)),'one_use_loss':float(np.sin(t/2).dot(np.sin(t/2))/banks)})
path=Path(__file__);np.savez_compressed(path.with_suffix('.npz'),**sums)
out={'status':'PASS_AUTHOR_CHECKS_AND_FLOATING_SAMPLED_FIXTURE','CPTP_decoder_checks':checks,'minimum_projector_slack':float(minslack),'source_calls_individually_simulated':calls,'independent_banks':4*banks,'seed':28102026,'scope':'Ordinary finite-root outcomes simulated; same-bank phase reused for all J. Summary S stored; seed/program reproduce every generated record. No hardware or confidence certification.','rows':rows}
path.with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='rows'},indent=2));print(rows)
