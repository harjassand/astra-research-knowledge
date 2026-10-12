from explore import *
import scipy.sparse as ss
from scipy.sparse.linalg import lsmr

def dual_context_setup(r):
    basis,N=dual_setup(r)
    outer=tuple(x for x in range(-r,r+2) if x not in (0,1)); outerindex={x:i for i,x in enumerate(outer)}
    B=1<<len(outer); k=N.cols
    denom=sp.ilcm(*[x.q for x in N]) if N else 1
    print('N denom',denom,flush=True)
    NN=np.asarray(N*denom,dtype=np.int64)
    coeff=np.zeros((B,k),dtype=np.int64)
    for j,a in enumerate(basis):
        mask=sum(1<<outerindex[x] for x in a); coeff[mask,:]=NN[j,:]
    for j in range(len(outer)):
        step=1<<j
        for start in range(0,B,2*step):coeff[start+step:start+2*step,:]+=coeff[start:start+step,:]
    mask1=1<<outerindex[-1]; mask2=1<<outerindex[2]
    valid=np.array([not ((s&mask1) and (s&mask2)) for s in range(B)])
    coeff[~valid,:]=0
    pop=np.array([s.bit_count() for s in range(B)])
    return basis,N,outer,coeff,valid,pop

def dual_context_eval(data,p):
    basis,N,outer,G,valid,pop=data
    p=float(p);w=p**pop*(1-p)**(len(outer)-pop)
    V=np.sqrt(w)[:,None]*G
    target=np.sqrt(w)*valid
    norms=np.linalg.norm(V,axis=0); Vs=V/norms
    zz=lstsq(Vs,target,cond=1e-13)[0]/norms
    pred=G@zz
    L=float(w@(2*pred-pred**2))
    return L,zz

def fast_primal(m,p):
    basis,polys=primal_setup(m); pp=float(p);chi=pp*(1-pp)
    # Factor local c-weighted inner product into three allowed rate contexts.
    grouped={}
    for j,poly in enumerate(polys):
        for a,v in poly.items():
            outer=a-{-1,2};mask=int(-1 in a)+2*int(2 in a)
            grouped.setdefault(outer,[]).append((j,mask,v))
    grouped.setdefault(frozenset((0,)),[]);grouped.setdefault(frozenset((1,)),[])
    rows=[];cols=[];vals=[];target=[];row=0
    for outer,items in grouped.items():
        for i,j in [(0,0),(0,1),(1,0)]:
            w=((pp if i else 1-pp)*(pp if j else 1-pp))*chi**len(outer)/(2*chi)
            fac=np.sqrt(w);h=[1,i-pp,j-pp,(i-pp)*(j-pp)]
            for k,mask,v in items:rows.append(row);cols.append(k);vals.append(fac*v*h[mask])
            target.append(fac*(int(outer==frozenset((0,)))-int(outer==frozenset((1,)))))
            row+=1
    V=ss.coo_matrix((vals,(rows,cols)),shape=(row,len(basis))).tocsr();target=np.array(target)
    norms=np.sqrt(np.array(V.power(2).sum(axis=0)).ravel());norms[norms==0]=1
    Vs=V@ss.diags(1/norms)
    result=lsmr(Vs,-target,atol=1e-13,btol=1e-13,maxiter=10000)
    z=result[0]/norms
    residual=V@z+target
    return float(residual@residual),basis,z,V,target,result[1:]

if __name__=='__main__':
 for r in [4,5,6]:
  t=time.perf_counter();data=dual_context_setup(r)
  for p in [sp.Rational(1,2),sp.Rational(4,5),sp.Rational(19,20)]:
   val,z=dual_context_eval(data,p);print('LOWER',r,str(p),val,flush=True)
  print('TIME',r,time.perf_counter()-t,flush=True)
 for m in [7,8,9,10]:
  t=time.perf_counter()
  for p in [sp.Rational(1,2),sp.Rational(4,5),sp.Rational(19,20)]:
   val,*rest=fast_primal(m,p);print('UPPER',m,str(p),val,'vars',len(rest[0]),'iters',rest[-1][1],flush=True)
  print('TIME',m,time.perf_counter()-t,flush=True)
