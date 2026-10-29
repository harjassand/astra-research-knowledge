#!/usr/bin/env python3
"""Exact root control of current-carrying modules; no observations or RNG."""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json,time
from clock_capped_transport import solve,sub,dot,serialize

def build(w,edges,regions):
    n=len(w);lap=[[F()]*n for _ in range(n)]
    for i,j,f in edges:
        assert i!=j and f>0
        lap[i][i]+=f;lap[i][j]-=f
    assert all(sum(row)==0 for row in lap)
    assert all(sum(lap[i][j] for i in range(n))==0 for j in range(n))
    return {'w':w,'L':lap,'regions':regions}

def record(model,region,ports):
    w=model['w'];lap=model['L'];outside=set(range(len(w)))-set(region)
    local=sub(lap,region);index={v:i for i,v in enumerate(region)}
    for v in ports:
        local[index[v]][index[v]]+=sum(lap[v][j] for j in outside)
    assert all(sum(row)==0 for row in local)
    boundary=[index[x] for x in ports];hidden=[i for i in range(len(region)) if i not in boundary]
    assert all(sum(local[i][j] for i in range(len(region)))==0 for j in hidden)
    g=sub(local,hidden);wi=[w[region[i]] for i in hidden]
    h=solve(g,wi);ht=solve([list(row) for row in zip(*g)],wi)
    sr=[[local[i][j]-dot([local[i][z] for z in hidden],solve(g,[local[z][j] for z in hidden])) for j in boundary] for i in boundary]
    br=[w[region[i]]-dot([local[i][z] for z in hidden],h) for i in boundary]
    bl=[w[region[j]]-dot(ht,[local[z][j] for z in hidden]) for j in boundary]
    imbalance=[sum(local[i][j] for i in range(len(region))) for j in boundary]
    assert imbalance==[sum(sr[i][j] for i in range(len(sr))) for j in range(len(sr))]
    assert any(imbalance)
    return {'S':sr,'bR':br,'bL':bl,'c':dot(wi,h),'boundary_imbalance':imbalance,
            'region_mass':sum(w[i] for i in region)}

def hit(model,target):
    keep=[i for i in range(len(model['w'])) if i not in target]
    w=[model['w'][i] for i in keep];h=solve(sub(model['L'],keep),w)
    return dot(w,h)/sum(w)

def main():
    start=time.perf_counter();one=F(1)
    source=build([one]*4+[F(2),F(3)],[(a,b,one) for a,b in [(0,4),(4,1),(1,2),(2,5),(5,3),(3,0)]],[[0,1,4],[2,3,5]])
    edges=[(0,1,F(1,3)),(2,3,F(2,5)),(1,2,one),(3,0,one)]
    for path,f in [([0,4,5,6,1],F(2,3)),([2,7,8,9,10,11,3],F(3,5))]:
        edges.extend((i,j,f) for i,j in zip(path,path[1:]))
    prepared=build([one]*4+[F(2,3)]*3+[F(3,5)]*5,edges,[[0,1,4,5,6],[2,3,7,8,9,10,11]])
    records=[]
    for r,ports in enumerate([[0,1],[2,3]]):
        actual=record(source,source['regions'][r],ports)
        fitted=record(prepared,prepared['regions'][r],ports)
        assert actual==fitted;records.append(actual)
    means=[]
    for target,expected in [(1,F(11,4)),(0,F(18,5))]:
        a=hit(source,set(source['regions'][target]));b=hit(prepared,set(prepared['regions'][target]))
        assert a==b==expected;means.append({'target_region':target,'source_mean':a,'prepared_mean':b})
    rates=[prepared['L'][i][i]/prepared['w'][i] for i in range(12)]
    assert rates==[one]*12
    out={'status':'PASS','source_observations':0,'random_draws':0,'source_states':6,'prepared_states':12,
         'open_region_records':records,'whole_region_means':means,'all_prepared_exit_rates':rates,
         'prepared_weights':prepared['w'],'prepared_laplacian':prepared['L'],
         'wall_seconds':time.perf_counter()-start,'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'scope':'Prescribed stationary directed cycle; modules individually non-Eulerian at ports; exact supplied-flow completion.'}
    (Path(__file__).resolve().parent/'OPEN_MODULE_CHECKS.json').write_text(json.dumps(serialize(out),indent=2)+'\n')
    print(json.dumps({'status':'PASS','source_states':6,'prepared_states':12,'whole_region_means':['11/4','18/5']}))

if __name__=='__main__':main()
