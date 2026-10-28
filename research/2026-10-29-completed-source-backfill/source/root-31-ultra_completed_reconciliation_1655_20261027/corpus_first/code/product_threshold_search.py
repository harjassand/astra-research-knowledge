import sys
sys.dont_write_bytecode=True
from product_witness_search import *

def run_threshold():
 t=time.monotonic(); rng=np.random.default_rng(172307)
 loc=[np.array(x,dtype=complex) for x in library()[0]]
 mat=np.array([hc(np.kron(a,b)) for a in loc for b in loc]).T
 norm=np.r_[np.ones(D*D),np.zeros(len(mat)-D*D)]
 results=[];worst=None
 for c in (1.4,1.55,1.6,(1+np.sqrt(5))/2,1.65,1.7,1.8,2.):
  best=1e5
  for restart in range(80):
   v=rng.normal(size=D*D)+1j*rng.normal(size=D*D);v/=np.linalg.norm(v);prev=1e10
   for iteration in range(30):
    out=local_phi(np.outer(v,v.conj()),c)
    lp=linprog(hc(out),A_ub=-mat.T,b_ub=np.zeros(mat.shape[1]),A_eq=norm[None,:],b_eq=[1.],bounds=[(None,None)]*len(mat),method='highs')
    assert lp.success
    W=unhc(lp.x); ev,vs=np.linalg.eigh(local_phi(W,c));val=float(ev[0]);v=vs[:,0]
    if val<best:
     best=val;bestw=dict(c=c,witness=lp.x.tolist(),state_real=v.real.tolist(),state_imag=v.imag.tolist(),value=val)
    if abs(prev-val)<1e-12:break
    prev=val
  results.append(dict(c=c,minimum_found=best,restarts=80,universal_certificate=False))
  print(c,best,flush=True)
  if best<0:worst=bestw
 (BASE/'results'/'PRODUCT_THRESHOLD_SEARCH.json').write_text(json.dumps(dict(results=results,elapsed_seconds=time.monotonic()-t),indent=2)+'\n')
 if worst:(BASE/'results'/'PRODUCT_THRESHOLD_FAILURE.json').write_text(json.dumps(worst,indent=2)+'\n')

if __name__=='__main__':run_threshold()
