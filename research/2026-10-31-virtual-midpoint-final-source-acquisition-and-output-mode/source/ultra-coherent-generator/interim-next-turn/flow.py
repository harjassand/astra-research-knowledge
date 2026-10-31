"""Exact finite outer-flow semantics for one bounded physical generator."""
from fractions import Fraction as Q
from pathlib import Path
import json
import sys

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'predictive_flow'))
sys.path.insert(0,str(HERE.parent/'entropy_witnesses'))
from flow_grid import geometry,prefix,word_feature
from entropy_cone import conjugate_bounds


def prepare(data,max_states=200):
    s,L,k=data['alphabet_size'],data['depth'],data['mesh']
    cap,clock=Q(data['kinetic_cap']),Q(data['inspection_rate'])
    if cap<=0 or clock<=0:raise ValueError('positive supplied physical cap and independent inspection rate required')
    leaves,nodes,descriptors,words=geometry(s,L,k,max_states);n,d=len(nodes),len(descriptors)
    a=list(map(Q,data['word_coefficients']));potential=list(map(Q,data['state_potential']));y=list(map(Q,data['row_duals']))
    if len(a)!=len(words) or len(potential)!=n or len(y)!=n*d or any(v>0 for v in y):
        raise ValueError('invalid coherent-generator dual shape or signs')
    D=[sum((a0*word_feature(node,w,leaves,L,k) for a0,w in zip(a,words)),Q(0)) for node in nodes]
    cache={}
    for i,node in enumerate(nodes):
        for side,b,w,sign in descriptors:
            cache[i,side,w]=prefix(node,side,w,leaves,k)
            cache[i,side,(b,)+w]=prefix(node,side,(b,)+w,leaves,k)
    active=[[(v,desc) for v,desc in zip(y[i*d:(i+1)*d],descriptors) if v] for i in range(n)]
    def row(i,j,side):
        value=Q(0)
        for coefficient,(q,b,w,sign) in active[i]:
            if q!=side:continue
            delta=(cap+clock+(clock if w else 0))/k
            residual=cap*cache[j,q,(b,)+w]-(cap+clock)*cache[i,q,(b,)+w]
            if nodes[i][0]==b:residual+=clock*cache[i,q,w]
            value+=coefficient*(sign*residual-delta)
        return value
    def without_z(i,j):return D[i]+potential[i]-potential[j]+row(i,j,0)+row(j,i,1)
    return {'nodes':nodes,'descriptors':descriptors,'words':words,'cap':cap,'clock':clock,
            'a':a,'y':y,'potential':potential,'without_z':without_z}


def normalization(cert,bits=24):
    n=len(cert['nodes']);cap=cert['cap'];cache={};worst=None;count=0
    for i in range(n):
        for j in range(i,n):
            hij,hji=cert['without_z'](i,j),cert['without_z'](j,i)
            hs,ha=(hij+hji)/2,(hij-hji)/2;argument=abs(ha/cap)
            if argument not in cache:cache[argument]=conjugate_bounds(argument,bits)[1]
            upper=hs+cap*cache[argument]
            worst=upper if worst is None else max(worst,upper);count+=1
    return {'z':-worst,'columns':count,'distinct_conjugates':len(cache)}


def verify(data,max_states=200):
    cert=prepare(data,max_states);check=normalization(cert,data.get('conjugate_bits',24))
    z=Q(data['normalization_dual'])
    if z>check['z']:raise ValueError('coherent-generator entropy cone failed')
    p=list(map(Q,data['input_probabilities']))
    if len(p)!=len(cert['words']) or min(p)<0 or sum(p)!=1:raise ValueError('invalid supplied word law')
    lower=z+sum((a*x for a,x in zip(cert['a'],p)),Q(0))
    return {**cert,'z':z,'lower':lower,'columns_checked':check['columns'],
            'largest_checked_cone_upper':z-check['z']}


def load(path,max_states=200):return verify(json.loads(Path(path).read_text()),max_states)
