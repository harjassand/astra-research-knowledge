"""Explicit polynomial-size LP for the selected signed enclosure; no subset oracle."""
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
from experiment import top,native,complete,ring,ROOT,certificate,exhaustive
import json,time

def solve_lp(T,f,k):
 m=len(f);r=k-1;d=1-np.diag(T);nvar=4*m+2*m*(m-1)
 rr=[];cc=[];vv=[];rhs=[]
 def row(xs,b):
  ix=len(rhs);rhs.append(b)
  for j,v in xs:rr.append(ix);cc.append(j);vv.append(v)
 for i in range(m):
  pairs=[j for j in range(m) if j!=i];zp=[4*m+i*(m-1)+l for l in range(m-1)];zn=[x+m*(m-1) for x in zp]
  row([(i,-d[i]),(2*m+i,r)]+[(z,1) for z in zp],-f[i])
  row([(m+i,-d[i]),(3*m+i,r)]+[(z,1) for z in zn],f[i])
  row([(i,-1),(m+i,-1)],0)
  for j,zpij,znij in zip(pairs,zp,zn):
   q=T[i,j]
   row([(j,q),(2*m+i,-1),(zpij,-1)],0)
   row([(m+j,-q),(2*m+i,-1),(zpij,-1)],0)
   row([(j,-q),(3*m+i,-1),(znij,-1)],0)
   row([(m+j,q),(3*m+i,-1),(znij,-1)],0)
 c=np.zeros(nvar);c[:2*m]=1
 res=linprog(c,A_ub=coo_matrix((vv,(rr,cc)),shape=(len(rhs),nvar)).tocsr(),b_ub=rhs,bounds=[(None,None)]*(2*m)+[(0,None)]*(nvar-2*m),method='highs')
 if not res.success:return dict(status='UNKNOWN',message=res.message,n_variables=nvar,n_constraints=len(rhs))
 U=res.x[:m];L=-res.x[m:2*m];TT=T.copy();np.fill_diagonal(TT,0)
 pu=np.maximum(np.maximum(TT*L[None,:],TT*U[None,:]),0);pl=np.maximum(np.maximum(-TT*L[None,:],-TT*U[None,:]),0)
 hi=f+top(pu,k);lo=f-top(pl,k)
 return dict(status='FLOAT_CANDIDATE',L=L,U=U,lo=lo,hi=hi,residual=max(float(max((f+top(pu,k-1))-d*U)),float(max(d*L-(f-top(pl,k-1))))),n_variables=nvar,n_constraints=len(rhs))

if __name__=='__main__':
 cases=[]
 for eps in [1.,.05,.001,1e-6]:
  es=complete(4)+[(i+4,j+4)for i,j in complete(4)]+[(i,i+4)for i in range(4)];w=np.r_[np.ones(12),np.full(4,eps)];p=np.r_[np.ones(4),-np.ones(4)];cases.append((f'weak_cut_{eps}',8,es,w,p,3))
 rng=np.random.default_rng(993102)
 n=7;es=complete(n);w=np.exp(rng.uniform(-2,2,len(es)));p=rng.normal(size=n);p-=p.mean();cases.append(('heterogeneous7',n,es,w,p,3))
 out=[]
 for name,n,es,w,p,k in cases:
  A,K,T,f=native(n,es,w,p);st=time.perf_counter();lp=solve_lp(T,f,k);dt=time.perf_counter()-st;actual=exhaustive(A,K,w,p,T,f,k)
  row=dict(name=name,status=lp['status'],variables=lp['n_variables'],constraints=lp['n_constraints'],lp_seconds=dt,actual_worst=float(max(np.max(abs(actual['lo'])),np.max(abs(actual['hi'])))),true_margin=actual['min_spectral_margin'])
  if lp['status']=='FLOAT_CANDIDATE':row.update(bound=float(max(np.max(abs(lp['lo'])),np.max(abs(lp['hi'])))),residual=lp['residual'],violation=float(max(np.max(actual['hi']-lp['hi']),np.max(lp['lo']-actual['lo']))))
  out.append(row);print(json.dumps(row),flush=True)
 (ROOT/'lp_results.json').write_text(json.dumps(out,indent=2))
