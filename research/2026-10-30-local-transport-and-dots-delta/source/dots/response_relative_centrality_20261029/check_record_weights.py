import numpy as np,json
from pathlib import Path
rng=np.random.default_rng(32940);rows=[]
for d in [2,3,5,8]:
 for case in range(12):
  z=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d));X=(z+z.conj().T)/2
  Bs=[]
  for j in range(2):
   z=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d));B=(z+z.conj().T)/2;Bs.append(B)
  projections=[]
  for B in Bs:
   e,u=np.linalg.eigh(B);mask=e>=np.median(e);Q=(u*mask)@u.conj().T;projections.append([Q,np.eye(d)-Q])
  ms=[q@p for p in projections[0] for q in projections[1]];hs=[m@m.conj().T for m in ms]
  assert np.linalg.norm(sum(hs)-np.eye(d))<1e-10
  es=[m@X-X@m for m in ms];a=np.sqrt(max(0,np.linalg.eigvalsh(sum(e.conj().T@e for e in es)).max()))
  loss=sum(np.linalg.norm(m@X@m.conj().T-X@h,'nuc') for m,h in zip(ms,hs));comm=sum(np.linalg.norm(h@X-X@h,'nuc') for h in hs)
  assert loss<=d*a+1e-10 and comm<=2*d*a+1e-10
  rows.append(dict(d=d,case=case,intertwining=a,response_error=loss,weight_commutator=comm))
Path(__file__).with_suffix('.json').write_text(json.dumps({'scope':'48 ideal unital record-weight checks, no approximate decoder','cases':rows},indent=2)+'\n');print('PASS',len(rows))
