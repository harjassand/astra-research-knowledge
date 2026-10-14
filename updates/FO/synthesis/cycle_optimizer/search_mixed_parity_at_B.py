#!/usr/bin/env python3
"""Exact fixed-common-background cycle search for resonant carriers 1 and 2."""
from fractions import Fraction as Q
from pathlib import Path
import json,sys

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'incoming_resonant'))
from profile_algebra import add,scale,mul,cos,sin,meanprod,const,poly_terms,edge_coeffs,edge_value,r,s,p,q

LAM=Q(11,100)
WIDTHS=[Q(1,4),Q(1,2),Q(1),Q(2)]

def gap_terms(n,m,Bvec):
    a=add(scale(cos(n),p),scale(cos(m),q)); c=add(scale(sin(n),p),scale(sin(m),q))
    b=add(scale(sin(n),-n*r),scale(sin(m),-m*s)); d=add(scale(cos(n),n*r),scale(cos(m),m*s))
    X=[add(x,const(Q(Bvec[i]))) for i,x in enumerate([a,b,c,d])]
    a,b,c,d=X
    u=add(mul(a,a),mul(c,c));v=add(mul(b,b),mul(d,d));w=add(mul(a,b),mul(c,d));det=add(mul(a,d),scale(mul(b,c),-1))
    F=meanprod(u,u)+meanprod(v,v)+4*meanprod(w,w)+ (Q(7,2)-LAM)*meanprod(det,det)-Q(29,10)*meanprod(det,add(u,v))
    aa,bb,cc,dd=map(Q,Bvec); ub=aa*aa+cc*cc;vb=bb*bb+dd*dd;wb=aa*bb+cc*dd;qb=aa*dd-bb*cc
    Fbase=ub*ub+vb*vb+4*wb*wb+(Q(7,2)-LAM)*qb*qb-Q(29,10)*qb*(ub+vb)
    return poly_terms(F-Fbase)

def graph(Bvec,low=Q(-1),high=Q(1),step=Q(1,4)):
    axis=[];x=low
    while x<=high:axis.append(x);x+=step
    V=[(x,y) for x in axis for y in axis];terms=gap_terms(1,2,Bvec)
    choices=[]
    for i,a in enumerate(V):
        for j,b in enumerate(V):
            co=edge_coeffs(terms,a,b)
            for k,h in enumerate(WIDTHS): choices.append((i,j,k,edge_value(co,h)))
    best={}
    for i,j,k,cost in choices:
        if (i,j) not in best or cost<best[i,j][0]:best[i,j]=(cost,k)
    d=[Q(0)]*len(V);pred=[None]*len(V);changed=None
    for it in range(len(V)):
        changed=None
        for (i,j),(cost,k) in best.items():
            if d[i]+cost<d[j]:d[j]=d[i]+cost;pred[j]=(i,k,cost);changed=j
        if changed is None:
            slacks=[cost+d[i]-d[j] for i,j,k,cost in choices]
            assert min(slacks)>=0
            return {'kind':'NO_NEGATIVE_CYCLE_AT_FIXED_COMMON_B','passes':it+1,
                    'negative_raw_strip_edges':sum(cost<0 for i,j,k,cost in choices),
                    'min_edge':str(min(x[3] for x in choices)),
                    'min_potential_slack':str(min(slacks)),
                    'potential':[str(x) for x in d], 'tight_edge_widths':sum(x==0 for x in slacks)}
    v=changed
    for _ in V:v=pred[v][0]
    start=v;rev=[]
    while True:
        i,k,cost=pred[v];rev.append((i,v,k,cost));v=i
        if v==start:break
    cyc=list(reversed(rev));total=sum((e[3] for e in cyc),Q(0));assert total<0
    return {'kind':'EXACT_NEGATIVE_CYCLE','cycle_weight':str(total),
            'cycle':[[list(map(str,V[i])),list(map(str,V[j])),str(WIDTHS[k]),str(c)] for i,j,k,c in cyc]}

if __name__=='__main__':
    affine=json.loads((ROOT/'full_affine_loop_search.json').read_text())
    chosen=[]
    for row in affine['runs']:
        if row.get('carrier_pair')==[1,2] and row.get('cubic_nonzero'):
            if row['common_B_opt'] not in [x['B'] for x in chosen]:
                chosen.append({'name':row['path_name'],'B':row['common_B_opt']})
    chosen.insert(0,{'name':'zero-background','B':['0','0','0','0']})
    results=[]
    for item in chosen:
        out={'background_name':item['name'],'common_B':item['B'],**graph([Q(x) for x in item['B']])}
        results.append(out);print(json.dumps({k:v for k,v in out.items() if k!='potential'},indent=2),flush=True)
    result={'integrand':'Fstar-(11/100)q^2','carriers':[1,2],
            'vertices':'[-1,1]^2 intersect (1/4)Z^2','allowed_widths':[str(x) for x in WIDTHS],
            'per_background_edge_width_choices':(9*9)**2*len(WIDTHS),'backgrounds_tested':len(results),
            'results':results}
    (ROOT/'mixed_parity_fixed_background_search.json').write_text(json.dumps(result,indent=2)+'\n')
