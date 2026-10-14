import os,sys,time,json
from pathlib import Path
import numpy as np
from fractions import Fraction as F
from model import fixture,acquire,discover_partition,Compiler
from solve import solve
from certify import certify,cross_certificate,product_term
from tt_ops import product as ttproduct
ROOT=Path(__file__).parent

def run(name,**kw):
    rank=kw.pop('rank',8);its=kw.pop('iterations',7);maxbits=kw.pop('max_local_bits',6)
    start=time.perf_counter();truth=fixture(**kw);learn,trans=acquire(truth);groups,part=discover_partition(learn,maxbits);c=Compiler(learn,groups);comp=time.perf_counter()-start
    print('START',name,truth['metadata'],'groupsizes',list(map(len,groups)),'R',str(c.R),flush=True)
    v,log=solve(c,rank=rank,iterations=its);proptime=time.perf_counter()-start-comp
    cert=certify(c,v);cert.update(name=name,metadata=truth['metadata'],n=learn['n'],full_state_count=2**learn['n'],local_state_count=sum(len(p) for p in c.mass),groups=groups,partition=part,energy_queries=trans['energy_queries'],clock_queries=trans['balanced_clock_queries'],raw_operator_terms=len(c.rawterms),source_product_terms=len(c.wterms),R=str(c.R),compile_seconds=comp,proposal_seconds=proptime,total_seconds=time.perf_counter()-start,log=log)
    np.savez(ROOT/(name+'.npz'),**{str(i):a for i,a in enumerate(v)})
    json.dump(cert,open(ROOT/(name+'.json'),'w'),indent=2);json.dump(trans,open(ROOT/(name+'_transcript.json'),'w'),indent=2)
    print('DONE',name,cert['lower_float'],cert['upper_float'],cert['ratio_float'],'time',cert['total_seconds'],flush=True)
    return c,v,cert

if __name__=='__main__':
    group=sys.argv[1] if len(sys.argv)>1 else 'primary'
    if group=='primary':
        for r in [1,2,3,4]:
            try:run('primary_r'+str(r),B=3,m=6,rarity=r)
            except Exception as e:
                json.dump({'name':'primary_r'+str(r),'failure':repr(e)},open(ROOT/('primary_r'+str(r)+'_failure.json'),'w'));print('FAIL',r,repr(e),flush=True)
    elif group=='coupling':
        for t in [F(11,10),F(19,10),F(3),F(6)]:
            run('coupling_'+str(t).replace('/','_'),B=3,m=6,rarity=2,cross=t)
    elif group=='rank':
        for rank in [2,4,12]:run('rank_'+str(rank),B=3,m=6,rarity=3,rank=rank)
    elif group=='field_clock':
        for f in [0,2]:run('field_'+str(f),B=3,m=6,rarity=2,field_scale=f)
        for nu in [F(1,10),F(10)]:run('clock_'+str(nu).replace('/','_'),B=3,m=6,rarity=2,clock_scale=nu)
    elif group=='prepared':
        c,v,res=run('prepared_base',B=3,m=6,rarity=2)
        _,d1=certify(c,v,return_data=True)
        # A point preparation with every elementary coordinate zero; no equilibrium sample.
        vs=[]
        for p in c.prob:
            x=np.full(len(p),F(0),dtype=object);x[0]=1/p[0];vs.append(x)
        be=ttproduct([np.array(x,float)*p for x,p in zip(vs,c.rootprob)])
        u,log=solve(c,rank=8,iterations=7,source=be)
        _,d2=certify(c,u,source_vectors=[vs],return_data=True)
        cc=cross_certificate(c,d1,d2);cc.update(preparation='all microscopic bits zero',n=c.model['n'],log_second_load=log)
        json.dump(cc,open(ROOT/'prepared_point.json','w'),indent=2);np.savez(ROOT/'prepared_point.npz',**{str(i):a for i,a in enumerate(u)})
        print('PREPARED',cc['lower_float'],cc['upper_float'],cc['ratio_float'],flush=True)
