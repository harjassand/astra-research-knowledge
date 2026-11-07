from pathlib import Path
import itertools, math, json
import numpy as np

def cell(L,a,rho):
 n=L+1;states=list(itertools.product([0,1],repeat=n));lookup={x:i for i,x in enumerate(states)};m=len(states)
 weights=np.array([rho**sum(x)*(1-rho)**(n-sum(x)) for x in states])
 sectors=[np.array([i for i,x in enumerate(states) if sum(x)==k]) for k in range(n+1)]
 proj=np.zeros((m,m))
 for inds in sectors:proj[np.ix_(inds,inds)]=1/len(inds)
 ell=np.array([sum(i*x[i] for i in range(n)) for x in states],float);G0=np.zeros((m,m))
 for i,x in enumerate(states):
  for b in range(L):
   y=list(x);y[b],y[b+1]=y[b+1],y[b];j=lookup[tuple(y)]
   if j!=i:G0[i,i]+=1;G0[i,j]-=1
 g=G0@ell
 assert all(abs(sum(g[inds]))<1e-12 for inds in sectors)
 meanK=0.;meanEnergy=0.;avgG=np.zeros_like(G0);gaps=[]
 for gbits in itertools.product([0,1],repeat=2):
  gw=rho**sum(gbits)*(1-rho)**(2-sum(gbits));G=np.zeros_like(G0)
  for i,x in enumerate(states):
   eta={j:x[j] for j in range(n)}|{-1:gbits[0],L+1:gbits[1]}
   for b in range(L):
    y=list(x);y[b],y[b+1]=y[b+1],y[b];j=lookup[tuple(y)];rate=1+a*eta[b-1]*eta[b+2]
    if j!=i:G[i,i]+=rate;G[i,j]-=rate
  assert np.max(abs(G-G.T))<1e-12
  f=np.linalg.solve(G+proj,g);assert np.max(abs(G@f-g))<1e-11
  K=float(np.dot(weights*g,f));En=float(np.dot(weights*f,G@f));assert abs(K-En)<1e-11
  meanK+=gw*K;meanEnergy+=gw*En;avgG+=gw*G
  for inds in sectors[1:-1]:gaps.append(float(np.linalg.eigvalsh(G[np.ix_(inds,inds)])[1]))
 fwrong=np.linalg.solve(avgG+proj,g);Kwrong=float(np.dot(weights*g,fwrong));chi=rho*(1-rho)
 Dstar=chi*L/meanK;Drefresh=chi*L/Kwrong
 assert min(gaps)>=1/(L+1)**2-1e-11
 if a==0:assert abs(Dstar-1)<1e-12
 assert 1-1e-12<=Dstar<=1+a*rho*rho+1e-12
 return {'L':L,'a':a,'rho':rho,'states_diagnostic_only':m,'dual_K':meanK,'dual_energy':meanEnergy,'dual_Dstar':Dstar,'incorrect_refreshed_outside_Dstar':Drefresh,'outside_refresh_error':Drefresh-Dstar,'minimum_sector_gap':min(gaps),'explicit_safe_gap':1/(L+1)**2}
rows=[cell(L,a,rho) for L in [3,5] for a in [0.,1.,2.] for rho in [1/3,.5,2/3]]
d=.5;v=.5;eq2=d*d/(v*v);weighted=eq2-d*d*(v**-2-1);incorrect=eq2-(v**-2-1)
assert abs(weighted-d*d)<1e-15
result={'status':'PASS','dual_cells':rows,'weighted_detector':{'expected_corrected_square':weighted,'true_square':d*d,'incorrect_count_subtraction':incorrect},'scope':'Finite independent dual-support/kernel/normalization diagnostics; not infinite-volume convergence or physical data.'}
Path(__file__).with_name('check_dual_cell_result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'PASS','dual_cases':len(rows),'max_refresh_error':max(r['outside_refresh_error'] for r in rows),'max_variational_energy_error':max(abs(r['dual_K']-r['dual_energy']) for r in rows),'weighted_detector':result['weighted_detector']},indent=2))
