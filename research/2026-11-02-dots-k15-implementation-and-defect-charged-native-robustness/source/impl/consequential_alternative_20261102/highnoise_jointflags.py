import json,sys,numpy as np
from scipy.special import xlogy
sys.path.insert(0,'producer-workspace/consequential_alternative_20261102')
from flagged_repetition import cluster,grid_channel,rep_data,evaluate
out=[]
for v in [.38,.4]:
 for r in [1.,2.,3.]:
  for K in [2,3]:
   initial=cluster(v,K,N=96,starts=40,ratio=r)
   centers=np.array(initial['pauli']);w,p,s=grid_channel(v,N=256,ratio=r)
   for it in range(100):
    labels=np.argmin(-p@np.log(centers).T,axis=1)
    mass=np.bincount(labels,weights=w,minlength=K)
    new=np.array([(w[labels==k,None]*p[labels==k]).sum(0)/mass[k] for k in range(K)])
    if np.max(abs(new-centers))<1e-14:centers=new;break
    centers=new
   entropy=-np.sum(mass[:,None]*xlogy(centers,centers))/np.log(2)
   continuum=-np.sum(w[:,None]*xlogy(p,p))/np.log(2)
   rec={'v':v,'r':r,'K':K,'w':mass.tolist(),'pauli':centers.tolist(),'Ic1':float(1-entropy),'Ic1_continuous':float(1-continuum),'quantization_loss':float(entropy-continuum),'partition':'argmin_f cross_entropy(P(sq,sp),pauli_f), normalized sq,sp in [0,sqrtpi/2]; physical coordinates scaled by sqrt(r),1/sqrt(r)','gridN':256,'quadrature_status':'diagnostic Gauss-Legendre, not interval certificate','repetition':[]}
   for n in [1,2,3,6,9,12,18]:
    vals=[evaluate(rep_data(n,mass,centers,o)) for o in [1,2,3]]
    rec['repetition'].append({'n':n,'Ic_XYZ':vals})
   out.append(rec)
   json.dump(out,open('producer-workspace/highnoise_jointflags_results.json','w'),indent=2)
   print(json.dumps({k:rec[k] for k in ['v','r','K','Ic1','Ic1_continuous','quantization_loss','w','pauli']}),flush=True)
