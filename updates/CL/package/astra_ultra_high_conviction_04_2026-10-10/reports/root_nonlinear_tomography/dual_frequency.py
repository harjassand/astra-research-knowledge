"""Target-functional recovery from third-order kernels: spectral-oracle diagnostic.
H1 spectral data and H3 values are supplied here; this is NOT acquisition or an
end-to-end physical capability. Coefficients are tested by numerical row-span
residual and actual recovery of a sampled physical quartic tensor.
"""
import itertools,json,math
from pathlib import Path
import numpy as np

def run(n,gamma,kind='resonant'):
 rng=np.random.default_rng(417+n)
 lam=np.linspace(1,4,n)
 a=np.ones(n)/math.sqrt(n)
 # Orthogonal hidden basis, with first column a.
 Q=np.linalg.qr(np.column_stack([a,np.eye(n)[:,:n-1]]))[0]
 if Q[:,0]@a<0:Q[:,0]*=-1
 C=Q[:,1:];m=n-1
 inds=list(itertools.combinations_with_replacement(range(m),4))
 perms=[np.asarray(list(set(itertools.permutations(i)))) for i in inds]
 D=len(inds)+1
 z=C.T@(lam*a)
 pairs=list(itertools.combinations_with_replacement(range(m),2))
 index={x:i+1 for i,x in enumerate(inds)}
 L=np.zeros((len(pairs),D))
 for ri,(i,j) in enumerate(pairs):
  for k in range(m):
   for l in range(m):L[ri,index[tuple(sorted([i,j,k,l]))]]+=z[k]*z[l]
 rows=[]
 for q in range(3*D+50):
  if kind=='resonant':
   freqs=np.sqrt(lam[rng.integers(n,size=3)])*rng.choice([-1,1],3)
   freqs+=gamma*rng.uniform(-.25,.25,3)
  else:freqs=rng.uniform(-6,6,3)
  ss=1j*np.concatenate(([sum(freqs)],freqs))
  modal=a[None,:]/(ss[:,None]**2+gamma*ss[:,None]+lam[None,:])
  port=modal@a;hidden=modal@C
  row=[np.prod(port)]
  for pr in perms:row.append(np.sum(np.prod(hidden[np.arange(4)[None,:],pr],axis=1)))
  rows.append(row)
 A=np.asarray(rows);F=np.concatenate([A.real,A.imag])
 U,s,Vh=np.linalg.svd(F,full_matrices=False)
 keep=s>s[0]*1e-11
 pinv=(Vh[keep].T/s[keep])@U[:,keep].T
 W=L@pinv
 residual=np.linalg.norm(W@F-L)/np.linalg.norm(L)
 # Independent physically valid hidden rotation and coefficients.
 O=np.linalg.qr(rng.normal(size=(m,m)))[0]
 alphas=rng.uniform(.2,.7,n)
 t=np.asarray([alphas[0]]+[sum(alphas[r+1]*np.prod(O[r,list(i)]) for r in range(m)) for i in inds])
 true=L@t; recovered=W@(F@t)
 return {'n':n,'gamma':gamma,'design':kind,'unknowns':D,'complex_queries':len(rows),'numerical_rank':int(sum(keep)),'target_row_span_residual':float(residual),'target_noise_amplification_op':float(np.linalg.norm(W,2)),'kernel_full_inverse_norm':float(1/s[keep][-1]),'physical_target_relative_error':float(np.linalg.norm(recovered-true)/np.linalg.norm(true)),'sigma_max':float(s[0]),'sigma_min_kept':float(s[keep][-1])}
if __name__=='__main__':
 results=[run(n,g) for n in [3,4,5,6,8] for g in [.1,.03,.01]]
 results += [run(6,.01,'uniform')]
 Path(__file__).with_suffix('.json').write_text(json.dumps(results,indent=2)+'\n')
 print(json.dumps(results,indent=2))
