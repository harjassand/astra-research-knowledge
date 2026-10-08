"""Exact 2D all-face geometry diagnostic; proof is in frozen derivations."""
from functools import cmp_to_key
from math import gcd
import json
from pathlib import Path

NETWORKS = {
    'order5': [((0,0),(2,0)),((2,0),(1,1)),((3,1),(0,1)),((3,2),(0,-2)),((3,2),(-1,-2))],
    'order6': [((0,0),(2,0)),((2,0),(2,1)),((4,1),(0,1)),((4,2),(-1,-2))],
    'order7': [((0,0),(2,0)),((2,0),(2,1)),((4,1),(1,1)),((4,1),(0,1)),((5,2),(-2,-2))],
    'order8': [((0,0),(2,0)),((2,0),(2,1)),((4,1),(1,2)),((5,3),(-2,-3))],
    'failed_order7_chain': [((0,0),(2,0)),((2,0),(1,1)),((3,1),(1,2)),((4,3),(-1,-3))],
    'failed_order4_split': [((0,0),(2,0)),((2,0),(1,1)),((3,1),(0,-1)),((3,1),(-1,-1))],
}

def check(edges):
    normals=[v for _,v in edges]
    normals += [(s[0]-t[0],s[1]-t[1]) for s,_ in edges for t,_ in edges]
    rays=set()
    for u,v in normals:
        if u==v==0: continue
        g=gcd(abs(u),abs(v));r=(-v//g,u//g)
        rays.update((r,(-r[0],-r[1])))
    def half(r):return 0 if r[1]>0 or (r[1]==0 and r[0]>=0) else 1
    def compare(r,s):
        if half(r)!=half(s):return half(r)-half(s)
        c=r[0]*s[1]-r[1]*s[0]
        return -1 if c>0 else 1 if c<0 else 0
    rays=sorted(rays,key=cmp_to_key(compare));directions=[]
    for j,r in enumerate(rays):
        directions.append(r);t=rays[(j+1)%len(rays)]
        middle=(r[0]+t[0],r[1]+t[1]);assert middle!=(0,0)
        directions.append(middle)
    certificates=[];strong=True;endo=True
    for w in directions:
        levels=[w[0]*s[0]+w[1]*s[1] for s,_ in edges]
        projections=[w[0]*v[0]+w[1]*v[1] for _,v in edges]
        ix=[j for j,l in enumerate(levels) if l==max(levels)]
        relevant=[j for j,p in enumerate(projections) if p]
        active=[j for j in relevant if levels[j]==max(levels[k] for k in relevant)] if relevant else []
        ok_endo=all(projections[j]<0 for j in active)
        ok_strong=ok_endo and all(projections[j]<=0 for j in ix) and any(projections[j]<0 for j in ix)
        strong &=ok_strong;endo &=ok_endo
        certificates.append(dict(w=w,levels=levels,projections=projections,max_sources=ix,essential_max=active,strong=ok_strong,endotactic=ok_endo))
    return dict(strong=strong,endotactic=endo,directions=len(directions),max_source_degree=max(sum(s) for s,_ in edges),certificate=certificates)

if __name__=='__main__':
    result={k:check(e) for k,e in NETWORKS.items()}
    Path(__file__).with_name('geometry_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:{f:v[f] for f in ('strong','endotactic','directions','max_source_degree')} for k,v in result.items()},indent=2))
