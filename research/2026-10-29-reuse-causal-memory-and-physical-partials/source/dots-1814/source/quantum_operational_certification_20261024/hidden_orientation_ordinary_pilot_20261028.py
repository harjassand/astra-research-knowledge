"""Individually simulated ordinary labelled calls; floating Procrustes diagnostic."""
import numpy as np,json
from pathlib import Path
rng=np.random.default_rng(281047)
u=np.array([1,2,3,4.],float);u/=np.linalg.norm(u)
w,x,y,z=u
R=np.array([[1-2*(y*y+z*z),2*(x*y-w*z),2*(x*z+w*y)],[2*(x*y+w*z),1-2*(x*x+z*z),2*(y*z-w*x)],[2*(x*z-w*y),2*(y*z+w*x),1-2*(x*x+y*y)]])
rows=[]
for p in [.001,.01,.1,1.]:
 for N in [128,512,2048]:
  for rep in range(64):
   # Every call has an input label, flag and actual one-copy output measurement.
   j=rng.integers(0,3,N);a=rng.integers(0,3,N);s=2*rng.integers(0,2,N)-1;f=rng.random(N)<p
   mean=s*np.where(f,R[a,j],(a==j).astype(float));b=np.where(rng.random(N)<(1+mean)/2,1,-1)
   M=np.zeros((3,3));np.add.at(M,(a,j),9*f*s*b/N)
   A,sv,B=np.linalg.svd(M);D=np.eye(3);D[-1,-1]=np.linalg.det(A@B);fit=A@D@B
   loss=p*np.sum((fit-R)**2)/8
   rows.append({'p':p,'N':N,'rep':rep,'leakage_count':int(f.sum()),'loss':float(loss),'orthogonality_residual':float(np.max(abs(fit.T@fit-np.eye(3))))})
summary=[]
for p in [.001,.01,.1,1.]:
 for N in [128,512,2048]:
  rr=[r for r in rows if r['p']==p and r['N']==N]
  summary.append({'p':p,'N':N,'mean_loss':float(np.mean([r['loss'] for r in rr])),'se_loss':float(np.std([r['loss'] for r in rr],ddof=1)/8),'mean_leakage':float(np.mean([r['leakage_count'] for r in rr])),'theoretical_expected_cap':min(p,41/N)})
out={'scope':'ordinary independently reset flagged qubit source; actual per-call RNG simulation, not physical source','seed':281047,'simulated_calls':sum(r['N'] for r in rows),'independent_runs':len(rows),'fit':'binary64 SVD proper Procrustes; NOT executed rational Jacobi compiler or rigorous finite control','learned_source_parameters':'learner uses only a,j,s,f,b; R,p only generate and score','summary':summary,'runs':rows}
root=Path(__file__).resolve().parent;(root/'hidden_orientation_ordinary_pilot_20261028.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='runs'},indent=2))
