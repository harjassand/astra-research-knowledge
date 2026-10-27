from pathlib import Path
import json,numpy as np
from covariance_sampler import QueryOracle,covariance_word,second_corrected_sampler,corrected_sampler,ordinary_sampler
rng=np.random.default_rng(8102723)
A=np.array([[.4,.1,0],[.1,-.6,.08],[0,.08,.7]])
v=rng.standard_normal((10000,3));q=QueryOracle(lambda x:x@A.T+np.array([2.,-1.,3.]))
word=covariance_word(q,v,2,rng)
result=dict(seed=8102723,affine_word_queries=q.queries_per_execution,
            affine_word_max_abs_error=float(np.max(np.abs(word-v@np.linalg.matrix_power(A,4).T))))
dim=16384;n=8;k=8;ell=2;trials=384;total=n+4*k+8*ell
laws={}
for name in ['second','first_same_n','first_equal_queries','ordinary_equal_queries','target']:
    shells=[]
    for start in range(0,trials,4):
        batch=min(4,trials-start);q=QueryOracle(np.sin)
        if name=='second':y=second_corrected_sampler(q,n,k,ell,batch,dim,1.,rng,True)
        elif name=='first_same_n':y=corrected_sampler(q,n,k,batch,dim,1.,rng,True)
        elif name=='first_equal_queries':y=corrected_sampler(q,n+8*ell,k,batch,dim,1.,rng,True)
        elif name=='ordinary_equal_queries':y=ordinary_sampler(q,total,batch,dim,1.,rng)
        else:y=rng.standard_normal((batch,dim))
        shells.extend((np.sum(y*y,axis=1)-dim)/np.sqrt(2*dim))
    shells=np.array(shells)
    laws[name]=dict(queries=q.queries_per_execution,radial_mean=float(shells.mean()),
                    radial_sd=float(shells.std(ddof=1)),outside_two_sd=float(np.mean(np.abs(shells)>2)))
result['law_diagnostics']=dict(dim=dim,n=n,k=k,ell=ell,trials=trials,laws=laws)
(Path(__file__).resolve().parent/'second_checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2),flush=True)
