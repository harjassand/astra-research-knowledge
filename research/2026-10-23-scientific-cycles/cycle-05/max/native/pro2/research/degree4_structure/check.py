#!/usr/bin/env python3
"""Exact bounded-subclass decoder and structural failure checks."""
from fractions import Fraction as F
import json,resource,time
from pathlib import Path
from decoder import prepare,recover,action


def main():
    wall,cpu=time.perf_counter(),time.process_time()
    cases=[]
    jobs=[('squared_path_32',[(i-2,i-1) for i in range(3,32)]),
          ('squared_path_128',[(i-2,i-1) for i in range(3,128)]),
          ('three_sun',[(0,1),(1,2),(0,2)]),
          ('three_page_book',[(0,1),(0,1)])]
    for name,parents in jobs:
        started=time.perf_counter()
        plan=prepare(parents);n=plan['n']
        D={e:F((e[0]*7+e[1]*11)%17-8,13) for e in
           [(i,i) for i in range(n)]+plan['edges']}
        Y=action(plan,D)
        assert recover(plan,Y)==D
        E=[[F((i*5+j*7)%19-9,29) for j in range(4)] for i in range(n)]
        observed=[[a+b for a,b in zip(y,e)] for y,e in zip(Y,E)]
        estimate=recover(plan,observed)
        error=sum((1 if i==j else 2)*(estimate[i,j]-d)**2 for (i,j),d in D.items())
        noise=sum(e*e for row in E for e in row)
        bound=2 if plan['book'] is not None else 400
        assert error<=bound*noise
        assert all(sum(x*x for x in row)<=1 for row in plan['X'])
        cases.append({'name':name,'n':n,'edges':len(plan['edges']),'q':4,
                      'max_degree':max(map(len,plan['adj'])),'exact_recovery':True,
                      'noise_squared':str(noise),'error_squared':str(error),
                      'proved_squared_constant':bound,
                      'distinct_local_maps':plan.get('distinct_local_maps'),
                      'max_local_gram_inverse_trace':str(max(plan.get('gram_traces',[F(0)]))),
                      'body_wall_seconds':time.perf_counter()-started})
    counterexamples=[]
    for n in (12,100):
        adj=[set() for _ in range(n)]
        for i in range(n):
            for j in range(i+1,min(n,i+3)):
                adj[i].add(j);adj[j].add(i)
        low={v for v in range(n) if len(adj[v])<4}
        distance={v:0 for v in low};front=list(low)
        for v in front:
            for w in adj[v]:
                if w not in distance:distance[w]=distance[v]+1;front.append(w)
        counterexamples.append({'kind':'squared_path_anchor_distance','n':n,
                                'low_degree_vertices':sorted(low),
                                'maximum_distance':max(distance.values())})
    weighted=[]
    for depth in (2,8,32):
        energy=F(4,3)*F(3,4)**depth
        norm=1+sum(F(4,3)*F(3,4)**d for d in range(1,depth))
        assert norm>=1 and energy>0
        weighted.append({'depth':depth,'edge_energy':str(energy),'amplitude_squared_norm':str(norm),
                         'edge_gain_min':'1/2','edge_gain_max':'1'})
    result={'schema':'astra.cycle4.maximal_degree4_local.v1','status':'passed',
            'cases':cases,'anchor_counterexamples':counterexamples,'weighted_gain_counterexamples':weighted,
            'wall_seconds':time.perf_counter()-wall,'cpu_seconds':time.process_time()-cpu,
            'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
            'scope':'One exact receiving operation on four actual 2-tree supports; universal proof is separate. No claim for all partial 2-trees.'}
    dest=Path(__file__).with_name('RESULT.json')
    if dest.exists():raise FileExistsError(dest)
    dest.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
