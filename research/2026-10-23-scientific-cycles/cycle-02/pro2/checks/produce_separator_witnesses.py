#!/usr/bin/env python3
"""Generate exact input-bound fixtures once; no floating proposals/optimization."""
import argparse,hashlib,json,resource,sys,time
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from separator_witness import build,unit_fixture,serializable,dot


def main(out,large):
    start=time.perf_counter();cpu=time.process_time();out.mkdir(parents=True,exist_ok=True)
    cases=[]
    specs=[(0,8),(1,12),(2,20),(3,28)]
    if large:specs.append((2,4010))
    for s,m in specs:
        t=time.perf_counter();c=time.process_time()
        result=build(unit_fixture(s,m),s)
        assert result['kind']=='flow'
        target=out/f'flow_s{s}_m{m}.json'
        payload=(json.dumps(serializable(result),indent=2)+'\n').encode();target.write_bytes(payload)
        ratios=[result['flow_ratio_squared'],result['local_ratio_squared']]
        cases.append({'filename':target.name,'bytes':len(payload),'sha256':hashlib.sha256(payload).hexdigest(),
                      's':s,'m':m,'q':s+2,'kind':result['kind'],'constraint_rank':result['constraint_rank'],
                      'max_certified_ratio_squared':str(max(ratios)),
                      'max_certified_ratio_approx':float(max(ratios))**0.5,
                      'guaranteed_ratio_fourth':str(result['guaranteed_ratio_fourth']),
                      'wall_seconds':time.perf_counter()-t,'cpu_seconds':time.process_time()-c})
    for kind in ('apex_kernel','clique_kernel'):
        s,m=2,20;X=unit_fixture(s,m)
        if kind=='apex_kernel':X[1]=X[0][:]
        else:X[s+1]=X[s][:]
        t=time.perf_counter();c=time.process_time();result=build(X,s)
        assert result['kind']==kind
        target=out/f'{kind}.json';payload=(json.dumps(serializable(result),indent=2)+'\n').encode();target.write_bytes(payload)
        cases.append({'filename':target.name,'bytes':len(payload),'sha256':hashlib.sha256(payload).hexdigest(),
                      's':s,'m':m,'q':s+2,'kind':kind,'wall_seconds':time.perf_counter()-t,'cpu_seconds':time.process_time()-c})
    ans={'status':'passed','case_count':len(cases),'cases':cases,
         'wall_seconds':time.perf_counter()-start,'cpu_seconds':time.process_time()-cpu,
         'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
         'scope':'exact rational construction; imports excluded; case timers included in body; no original-input benchmark'}
    (out/'PRODUCER_RECEIPT.json').write_text(json.dumps(ans,indent=2)+'\n');print(json.dumps(ans,indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);parser.add_argument('--large',action='store_true')
    a=parser.parse_args();main(a.output,a.large)
