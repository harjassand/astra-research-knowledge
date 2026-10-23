"""Independent bounded point calculation. No producer imports, resampling, or fitting changes.
Streams original counts; float64 log representation (producer uses float32 log storage).
Re-derives FWL means, NNLS via Cholesky, direct-normal-equation ridge,
and SVD projection. Only descriptive point outputs are checked.
"""
import argparse,hashlib,json,time,resource,sys,platform
from pathlib import Path
import numpy as np,h5py
from scipy import sparse,optimize

def col(g,k):
 x=g[k]
 if isinstance(x,h5py.Group):return np.asarray(x['categories'].asstr()[:])[x['codes'][:]]
 return x.asstr()[:] if x.dtype.kind in 'OSU' else x[:]
def sha(p):
 with open(p,'rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--input',required=True);ap.add_argument('--producer',required=True);ap.add_argument('--output',required=True);a=ap.parse_args();t=time.monotonic()
 assert sha(a.input)=='5da0485aed81b23bda57b4a7b4510a394682d54911416db89b4846ff6dd34732'
 root=Path(a.producer);design=json.loads((root/'results/DESIGN_MAP.json').read_text());expected=json.loads((root/'results/POINT_RESULT.json').read_text())
 with h5py.File(a.input) as f:
  arr=col(f['obs'],'CRISPRcas13_Array');classes=col(f['obs'],'Guide.Class');arms,arm=np.unique(arr,return_inverse=True);N=len(arms);nc=len(arr);G=int(f['X'].attrs['shape'][1]);n=np.bincount(arm,minlength=N).astype(float);reference=np.isin(classes,['Single','NT']);ref=np.array([np.all(reference[arm==i]) for i in range(N)])
  z=np.concatenate([(col(f['obs'],k)[:,None]==np.unique(col(f['obs'],k))[None,:]).astype(float) for k in ['10X_lane','HTO']],axis=1);K=z.shape[1]
  sums={s:np.zeros((N,G)) for s in ['log','rate','Lx']};sq=np.zeros((N,2));L2=np.zeros(N);lib=np.zeros(nc);crosslog=np.zeros((K,G));crossrate=np.zeros((K,G));ptr=f['X/indptr'][:]
  for lo in range(0,nc,256):
   hi=min(nc,lo+256);start,stop=int(ptr[lo]),int(ptr[hi]);values=f['X/data'][start:stop].astype(float);assert np.isfinite(values).all() and (values>=0).all() and (values==np.floor(values)).all()
   x=sparse.csr_matrix((values,f['X/indices'][start:stop],ptr[lo:hi+1]-start),shape=(hi-lo,G));l=np.asarray(x.sum(1)).ravel();assert (l>0).all();lib[lo:hi]=l;y=x.copy();y.data=np.log1p(y.data*np.repeat(10000/l,np.diff(y.indptr)))
   ag=sparse.csr_matrix((np.ones(hi-lo),(arm[lo:hi],np.arange(hi-lo))),shape=(N,hi-lo))
   sums['log']+=(ag@y).toarray();sums['rate']+=(ag@x).toarray();sums['Lx']+=(ag@x.multiply(l[:,None])).toarray()
   np.add.at(sq[:,0],arm[lo:hi],np.asarray(y.multiply(y).sum(1)).ravel());np.add.at(sq[:,1],arm[lo:hi],np.asarray(x.multiply(x).sum(1)).ravel());np.add.at(L2,arm[lo:hi],l*l)
   rz=sparse.csr_matrix((z[lo:hi]*reference[lo:hi,None]).T);crosslog+=(rz@y).toarray();crossrate+=10000*(rz@x).toarray()
 totals=np.bincount(arm,weights=lib,minlength=N);raw={'log':sums['log']/n[:,None],'rate':10000*sums['rate']/totals[:,None]};noise={'log':np.maximum(0,sq[:,0]-n*np.sum(raw['log']**2,1))/(n*np.maximum(n-1,1))}
 m=raw['rate'];noise['rate']=np.maximum(0,1e8*sq[:,1]-20000*np.sum(m*sums['Lx'],1)+L2*np.sum(m*m,1))*n/np.maximum(n-1,1)/(totals**2)
 del sums
 adj={};tech={}
 for scale in ['log','rate']:
  w=np.ones(nc) if scale=='log' else lib;den=n if scale=='log' else totals;zs=np.zeros((N,K));np.add.at(zs,arm,z*w[:,None]);rw=w*reference
  mat=z.T@(z*rw[:,None])-zs[ref].T@(zs[ref]/den[ref,None]);rhs=(crosslog if scale=='log' else crossrate)-zs[ref].T@raw[scale][ref]
  coef=np.linalg.pinv(mat,rcond=1e-10,hermitian=True)@rhs;z0=np.average(z[reference],axis=0,weights=w[reference]);adj[scale]=raw[scale]-(zs/den[:,None]-z0)@coef;tech[scale]={'rank':int(np.linalg.matrix_rank(mat,tol=max(np.linalg.eigvalsh(mat).max(),1)*1e-10))}
 fam=[f for f in design['families'] if f['eligible']];lookup={v:i for i,v in enumerate(arms)};ix=np.array([[lookup[x] for x in f['arms']] for f in fam]);c=lookup[design['matching_control']];targets=sorted({f[k] for f in fam for k in ['a','b']});inc=np.array([[float(target in [f['a'],f['b']]) for target in targets] for f in fam]);nf=len(fam);out=[]
 for scale in ['log','rate']:
  m=adj[scale];C=m[c];upper=np.log(10001) if scale=='log' else np.inf;guard=lambda x:np.clip(x,0,upper)
  for direction in [0,1]:
   src=ix[:,direction];dst=ix[:,1-direction];sa,sb,ta,tb=(ix[:,2],ix[:,3],ix[:,5],ix[:,4]) if direction==0 else (ix[:,5],ix[:,4],ix[:,2],ix[:,3]);A=m[sa]-C;B=m[sb]-C;T=m[src]-C;betas=[]
   for j in range(nf):
    S=np.stack([A[j],B[j]],1);gram=S.T@S;pen=np.array([noise[scale][sa[j]]+noise[scale][c],noise[scale][sb[j]]+noise[scale][c]])+1e-8*max(np.trace(gram),1e-12);normal=gram+np.diag(pen);rhs=S.T@T[j]+pen;R=np.linalg.cholesky(normal).T;betas.append(optimize.nnls(R,np.linalg.solve(R.T,rhs))[0])
   beta=np.array(betas);fit=C+beta[:,0,None]*A+beta[:,1,None]*B;res=m[src]-guard(fit);w=n[src]/np.mean(n[src]);center=np.average(inc,axis=0,weights=w);Z=inc-center;Z/=np.maximum(np.sqrt(np.sum(w[:,None]*Z**2,axis=0)),1e-15);X=np.column_stack([np.ones(nf),Z]);hs=[];cvs=[]
   for lam in [.01,.1,1,10,100]:
    pen=np.diag([0]+[lam]*len(targets));H=X@np.linalg.solve(X.T@(X*w[:,None])+pen,X.T*w);den=1-np.diag(H);errors=(res-H@res)/den[:,None];cvs.append(float(np.average(np.mean(errors**2,1),weights=w)));loo=H/den[:,None];np.fill_diagonal(loo,0);hs.append(loo)
   choice=int(np.argmin(cvs));offset=hs[choice]@res;predsrc=guard(fit+offset);unguard=C+beta[:,0,None]*(m[ta]-C)+beta[:,1,None]*(m[tb]-C)+offset;pred=guard(unguard);u=[]
   for j in range(nf):
    S=(m[ix[j,[2,3,5,4]]]-C).T;U,s,V=np.linalg.svd(S,full_matrices=False);keep=s*s>max(s[0]*s[0],1e-30)*1e-10;v=m[src[j]]-predsrc[j];u.append(v-U[:,keep]@(U[:,keep].T@v))
   u=np.array(u);transfer=guard(pred+.5*u);vals={'ordinary_mse':np.mean((m[dst]-pred)**2,1),'transfer_mse':np.mean((m[dst]-transfer)**2,1),'additive_mse':np.mean((m[dst]-guard(m[ta]+m[tb]-C))**2,1)};vals['gain']=vals['ordinary_mse']-vals['transfer_mse'];ev=expected['point'][scale][direction];errors={k:float(np.max(np.abs(v-np.array(ev[k])))) for k,v in vals.items()};assert choice==ev['lambda_index'];assert max(errors.values())<2e-7,(scale,errors)
   out.append({'scale':scale,'direction':direction,'lambda_index':choice,'means':{k:float(v.mean()) for k,v in vals.items()},'maximum_absolute_family_discrepancy':errors,'positive_gain_count':int((vals['gain']>0).sum()),'beta_max_abs_discrepancy':float(np.max(np.abs(beta-np.array(ev['beta'])))),'representative_first_family':{k:float(v[0]) for k,v in vals.items()},'clipped_ordinary':int((pred!=unguard).sum()),'clipped_transfer':int((transfer!=pred+.5*u).sum())})
 receipt={'status':'PASS_POINT_ONLY','independent_implementation':True,'producer_source_imported':False,'uncertainty_draws_executed':0,'loco_executed':False,'input_sha256':sha(a.input),'representation_difference':'float64 log normalization versus producer float32 stored log values; acceptance tolerance 2e-7 absolute per-family MSE/gain, set in source before execution','families':nf,'point_rows':out,'technical':tech,'wall_seconds':time.monotonic()-t,'peak_rss_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'python':sys.version,'platform':platform.platform()}
 Path(a.output).write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt))
if __name__=='__main__':main()
