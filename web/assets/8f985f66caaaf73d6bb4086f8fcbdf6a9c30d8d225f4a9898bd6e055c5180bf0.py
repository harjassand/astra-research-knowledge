"""Bounded exact search for a stronger dominant-face disconnection.

This retains negative outcomes. Connected dominant faces do not prove
polynomial mixing; they only defeat the attempted zero-leading-capacity
counterexample for these three six-site templates.
"""
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
import json
import sys
import time
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from initial_checks import det


def templates():
    n=6
    upper=[[Q(i<j<n-1) for j in range(n)] for i in range(n)]
    light=[[Q(j==n-1 and i<n-1) for j in range(n)] for i in range(n)]
    light2=[[Q((i%2)+1 if j==n-1 and i<n-1 else 0) for j in range(n)] for i in range(n)]
    triangles=[[Q(0) for _ in range(n)] for _ in range(n)]
    for offset in (0,3):
        for i in range(3):
            triangles[offset+i][offset+(i+1)%3]=Q(1)
    cross=[[Q((i<3)!=(j<3)) for j in range(n)] for i in range(n)]
    return [('upper_with_uniform_light_column',upper,light),('upper_with_alternating_light_column',upper,light2),('two_directed_triangles_with_cross_light',triangles,cross)]


def systems(a,b):
    n=len(a)
    out=[]
    for t in range(4):
        f=[[t*a[i][j]+b[i][j] for j in range(n)] for i in range(n)]
        lines=[(tuple(Q(i==k) for k in range(n)),tuple(f[i])) for i in range(n)]
        for i,j in combinations(range(n),2):
            lines.append((tuple(Q(k==i) for k in range(n)),tuple(Q(k==j) for k in range(n))))
        out.append(lines)
    return out


def components(states,max_replaced):
    parent=list(range(len(states)))
    def find(i):
        while parent[i]!=i:
            parent[i]=parent[parent[i]]
            i=parent[i]
        return i
    buckets={}
    shared=len(states[0])-max_replaced
    for i,s in enumerate(states):
        for key in combinations(s,shared):
            buckets.setdefault(key,[]).append(i)
    for ids in buckets.values():
        first=ids[0]
        for other in ids[1:]:
            x,y=find(first),find(other)
            if x!=y:
                parent[y]=x
    result={}
    for i,s in enumerate(states):
        result.setdefault(find(i),[]).append(s)
    return sorted((len(v) for v in result.values()),reverse=True)


def main():
    started=time.perf_counter()
    rows=[]
    for name,a,b in templates():
        allsystems=systems(a,b)
        polynomials={}
        for state in combinations(range(len(allsystems[0])),3):
            ds=[]
            for lines in allsystems:
                columns=[]
                for i in state:
                    columns.extend(lines[i])
                matrix=[[c[row] for c in columns] for row in range(6)]
                ds.append(det(matrix))
            cubic=(ds[3]-3*ds[2]+3*ds[1]-ds[0])/6
            quadratic=(ds[2]-2*ds[1]+ds[0])/2-3*cubic
            linear=ds[1]-ds[0]-quadratic-cubic
            coefficients=(ds[0],linear,quadratic,cubic)
            degree=max((i for i,c in enumerate(coefficients) if c),default=-1)
            if degree>=0:
                polynomials[state]=(degree,coefficients[degree])
        degree=max(p[0] for p in polynomials.values())
        high=[s for s,p in polynomials.items() if p[0]==degree]
        one=components(high,1)
        two=components(high,2)
        rows.append({'template':name,'candidate_states':1330,'nonzero_amplitude_polynomials':len(polynomials),'max_amplitude_degree':degree,'dominant_states':len(high),'one_pair_component_sizes':one,'two_pair_component_sizes':two,'attempt':'Seek dominant-face disconnection blocking two-line edits plus union swaps','verdict':'NOT_FOUND' if len(two)==1 else 'CANDIDATE_REQUIRING_VARIANCE_AND_BALANCE_AUDIT'})
    result={'status':'COMPLETE','arithmetic':'exact rational determinants; degree <=3 independently follows from three selected f-columns','templates':rows,'scope':'Finite dominant-support connectivity only, no spectral gap or energy guarantee','wall_seconds':time.perf_counter()-started}
    target=Path(__file__).with_suffix('.json')
    target.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
