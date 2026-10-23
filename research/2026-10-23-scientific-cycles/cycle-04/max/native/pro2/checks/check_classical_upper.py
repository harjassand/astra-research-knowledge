#!/usr/bin/env python3
"""Test the actual classical comparator on the same saved support graphs."""
from fractions import Fraction as F
import json,resource,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from classical_star import prepare,recover


def run():
    wall=time.perf_counter();cpu=time.process_time();cases=[]
    for name in ('core_t2_large','core_t3'):
        data=json.loads((ROOT/'witnesses'/(name+'.json')).read_text())
        n=data['n'];t=data['parameters']['t'];edges=[tuple(e) for e in data['edges']]
        start=time.perf_counter();plan=prepare(n,edges,t);q=plan['q']
        D={(i,i):F((i%13)-6,7) for i in range(n)}
        D.update({(i,j):F((i*19+j*7)%17-8,11) for i,j in edges})
        Y=[[F(0)]*q for _ in range(n)]
        for (i,j),a in D.items():
            Y[i][plan['colors'][j]]+=a
            if i!=j:Y[j][plan['colors'][i]]+=a
        assert recover(plan,Y)==D
        E=[[F((i*11+j*13)%19-9,23) for j in range(q)] for i in range(n)]
        Z=[[a+b for a,b in zip(y,e)] for y,e in zip(Y,E)]
        out=recover(plan,Z)
        err=sum((1 if i==j else 2)*(out[i,j]-a)**2 for (i,j),a in D.items())
        noise=sum(x*x for row in E for x in row)
        assert err<=2*noise
        cases.append({'name':name,'n':n,'t':t,'actual_queries':q,'upper_K_t':plan['cap'],
          'exact_recovery':True,'noise_squared':str(noise),'frobenius_error_squared':str(err),
          'wall_seconds':time.perf_counter()-start})
    result={'cases':cases,'wall_seconds':time.perf_counter()-wall,'cpu_seconds':time.process_time()-cpu,
      'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
      'scope':'Explicit sparse action simulation and preparation/decoder; no implicit-action performance benchmark.'}
    print(json.dumps(result,indent=2))
    return result

if __name__=='__main__':
    result=run()
    if len(sys.argv)>1:Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
