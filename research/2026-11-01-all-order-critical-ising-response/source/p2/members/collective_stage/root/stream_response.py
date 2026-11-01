"""Fully streaming all-order sampler and exact finite-confidence response.

Only the current dual state, four sums/squares, and a bounded 512-entry score
cache are retained. No interaction histories or terminal histogram accumulate.
The supplied executable is the compiled all_order_sampler.cpp, not an oracle.
"""
import argparse
import json
import subprocess
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
from time import perf_counter
from all_order_response import potential_num,scores,dyadic_outer
from certify_all_order import certify


def run(executable,n,samples,seed,failure=F(1,20),bits=100):
    started=perf_counter();scale=1<<bits
    sums={k:0 for k in ('ul','uu','wl','wu')};squares=dict(sums)
    maxwidth=F(0);observed=0;record={}
    @lru_cache(maxsize=512)
    def endpoint(state):
        u,wl,wu=scores(n,state,potential_num(state,n),bits)
        ul,uu=dyadic_outer(u,bits);wli,_=dyadic_outer(wl,bits);_,wui=dyadic_outer(wu,bits)
        return (ul,uu,wli,wui)
    command=[str(executable),str(n),str(samples),str(seed),'-','--stream']
    with subprocess.Popen(command,stdout=subprocess.PIPE,text=True,bufsize=1) as process:
        for line in process.stdout:
            value=json.loads(line)
            if value['type']=='sample':
                values=endpoint(tuple(value['state']))
                for k,v in zip(sums,values):sums[k]+=v;squares[k]+=v*v
                maxwidth=max(maxwidth,F(values[3]-values[2],scale));observed+=1
            else:
                record.update({k:v for k,v in value.items() if k!='type'})
        code=process.wait()
    assert code==0 and observed==samples and record['samples']==samples
    result=certify(failure=failure,bits=bits,precomputed=(record,sums,squares,maxwidth))
    result['streaming']=True;result['retained_score_cache_limit']=512
    result['score_cache_info']=list(endpoint.cache_info());result['total_seconds']=perf_counter()-started
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--executable',default='producer-workspace/astra_all_order_sampler')
    p.add_argument('--n',type=int,default=128);p.add_argument('--samples',type=int,default=10000)
    p.add_argument('--seed',type=int,default=20261106);p.add_argument('--output',required=True)
    p.add_argument('--bits',type=int,default=100)
    a=p.parse_args();r=run(a.executable,a.n,a.samples,a.seed,bits=a.bits)
    Path(a.output).write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({k:v for k,v in r.items() if not k.endswith('exact') and not k.startswith('exact_endpoint')},indent=2))
