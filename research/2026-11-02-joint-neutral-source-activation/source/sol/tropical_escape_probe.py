#!/usr/bin/env python3
"""Finite valuation diagnostic, never a full asymptotic or return certificate."""
from fractions import Fraction as F
from itertools import product
from math import prod
from collections import Counter
from pathlib import Path
import json
from max_source_envelope import adjacent, ordered, ff

P=Path(__file__).resolve().parent
def activity(source,weights,base,offset,coeff):
    deg=0;c=F(1)
    for y,w,b,o,k in zip(source,weights,base,offset,coeff):
        if w:
            deg+=w*y;c*=k**y
        else:
            f=ff(b+o,y)
            if not f:return None
            c*=f
    return deg,c
def escape(raw,weights,base,coeff=None,horizon=10):
    d=len(weights);sources={y for y,z,k in raw};coeff=tuple(coeff or [F(1)]*d)
    root=(0,)*d
    def maximal(offset):
        aa={y:activity(y,weights,base,offset,coeff) for y in sources}
        aa={y:v for y,v in aa.items() if v is not None};mx=max(aa.values())
        return mx,{y for y,v in aa.items() if v==mx}
    first,unused=maximal(root);seen={root};front={root:[]}
    for depth in range(horizon+1):
        nxt={}
        for off,path in front.items():
            mx,ss=maximal(off)
            degree=sum(w*o for w,o in zip(weights,off))+first[0]-mx[0]
            if degree<0:return {'escape_depth':depth,'degree':degree,'word':path,'states':len(seen)}
            if depth==horizon:continue
            for i,(y,z,k) in enumerate(raw):
                if y not in ss:continue
                dest=tuple(o+b-a for o,a,b in zip(off,y,z))
                if dest not in seen:
                    seen.add(dest);nxt[dest]=path+[i]
        front=nxt
        if not front:break
    return {'escape_depth':None,'states':len(seen)}

def main():
    raw=adjacent(3);hist=Counter();fails=[];count=0;maxstates=0
    # Each coordinate is either exactly 0,1,2,3,4, or n,n^2,n^3.
    modes=[('b',j) for j in range(5)]+[('w',j) for j in range(1,4)]
    for spec in product(modes,repeat=4):
        weights=tuple(v if k=='w' else 0 for k,v in spec)
        if not any(weights):continue
        base=tuple(v if k=='b' else 0 for k,v in spec)
        ans=escape(raw,weights,base);count+=1;maxstates=max(maxstates,ans['states'])
        if ans['escape_depth'] is None:
            fails.append({'weights':weights,'bounded_coordinates':base,**ans})
        else:hist[ans['escape_depth']]+=1
    controls=[]
    for label,net,w,b in [('single_ordered_axis',ordered(3,[1,1,1,2]),(1,0,0),(0,0,0)),
        ('conservative_fast_angular',[( (2,0),(1,1),F(100)),((1,1),(2,0),F(1)),((0,0),(1,0),F(1)),((1,0),(0,0),F(1)),((0,0),(0,1),F(1)),((0,1),(0,0),F(1))],(1,1),(0,0))]:
        controls.append({'label':label,**escape(net,w,b,horizon=10)})
    result={'scope':'Finite leading-power fixtures only; no coefficient-uniform, complete valuation-flag or paid-return certificate.',
            'fixtures':count,'escape_depth_histogram':dict(sorted(hist.items())),'failed_fixtures':fails,
            'largest_search_state_count':maxstates,'negative_controls':controls}
    (P/'results'/'tropical_escape_probe.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
