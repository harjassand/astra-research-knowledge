import itertools,json
import numpy as np
from experiment import complete,native,ROOT
rng=np.random.default_rng(619720)
results=[]
for n,k in [(5,2),(5,3),(6,2),(6,3),(6,4),(7,3)]:
 es=complete(n);m=len(es);A,K,T,f=native(n,es,np.ones(m),np.zeros(n));Ps=rng.normal(size=(n,3000));Ps-=Ps.mean(axis=0)
 # Row maps for edge (0,1); symmetry covers every monitor distribution.
 e=es.index((0,1)); a=A[:,e]; rows=[];stars=[];sets=[]
 for kk in range(k+1):
  for S in itertools.combinations([i for i in range(m) if i!=e],kk):
   SS=np.array(S,dtype=int);KS=K-A[:,SS]@A[:,SS].T
   if np.linalg.eigvalsh(KS)[0]<1e-10:continue
   row=np.linalg.solve(KS,a)
   rows.append(row);stars.append(all(0 in es[s] or 1 in es[s] for s in S));sets.append(S)
 rows=np.array(rows);star=np.array(stars);vals=rows@Ps[:-1];allmax=vals.max(axis=0);starmax=vals[star].max(axis=0);gap=allmax-starmax;gap[Ps[0]<Ps[1]]=0
 ii=int(gap.argmax());iS=int(vals[:,ii].argmax())
 r=dict(n=n,k=k,num_sets=len(sets),max_star_gap=float(gap[ii]),all_opt=float(allmax[ii]),star_opt=float(starmax[ii]),witness_p=Ps[:,ii].tolist(),witness_edges=[es[z] for z in sets[iS]],star_fraction=float(star.mean()))
 results.append(r);print(json.dumps(r),flush=True)
(ROOT/'double_star_aligned_results.json').write_text(json.dumps(results,indent=2))
