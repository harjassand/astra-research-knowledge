"""Generate exact rational data for the single Hodge-cancelling cube target."""
import json,sys
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).parent.parent))
from exact_separability import rounded
from verify_cube_stdlib import K
from gram_sdp import gram_model

def build():
    base=Path(__file__).parent;z=np.load(base/'gram_candidate.npz')
    x=z['x'];y=z['y'];vec=z['vec'];bs=z['bs']
    scale=np.linalg.norm(x)/np.sqrt(10);x/=scale;y*=scale
    qx=10**8;qv=10**6;qb=10**10
    xi=rounded(x,qx);yi=rounded(y,qx);vi=rounded(vec,qv)
    bi=np.array([rounded((b+b.T)/(4 if 10<=n<100 else 2),qb)
                 for n,b in enumerate(bs)],dtype=object)
    vi[:100,:]=0
    for i in range(10):vi[i,i]=qv
    at=10
    for sign in (1,-1):
        for i in range(10):
            for j in range(i+1,10):vi[at,i]=qv;vi[at,j]=sign*qv;at+=1
    j=gram_model();trace=int(np.trace(j));local=np.kron(xi,yi)
    target=local@j@local.T;targetden=trace*qx**4
    approx=sum(np.kron(np.outer(v,v),b) for v,b in zip(vi,bi));approxden=qv*qv*qb
    denominator=targetden*approxden;res=target*approxden-approx*targetden
    r=res.reshape(10,6,10,6);cor=[r[i,:,i,:].copy() for i in range(10)]
    for i in range(10):
        for j0 in range(i+1,10):
            c=r[i,:,j0,:].copy();assert np.array_equal(c,c.T)
            cor.append(c);cor[i]-=c;cor[j0]-=c
    final=bi*(denominator//qb)
    for n,c in enumerate(cor):final[n]+=c
    u=[[int(i==j) for j in range(21)] for i in range(21)]
    for i in range(6):
        for j0 in range(6):u[10+i][10+j0]=K[i][j0]
    payload={'schema':'family272_hodge_cancelled_cube_separable_v1','boundary_dim':[10,6],
      'amendment_U':u,
      'x_numerator':xi.tolist(),'y_numerator':yi.tolist(),'filter_denominator':qx,
      'input_numerators':vi.tolist(),'input_denominator':qv,
      'output_numerators':final.tolist(),'output_denominator':denominator,
      'rational_target_trace':trace}
    p=base/'gram_cube_separable_certificate.json'
    p.write_text(json.dumps(payload,separators=(',',':'))+'\n')
    print('Frozen',p,'trace',trace)

if __name__=='__main__':build()
