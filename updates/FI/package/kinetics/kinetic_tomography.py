"""Synthetic balanced-clock tomography with unknown supports.
Global assumption: each attempt prefactor is a positive Boolean polynomial of
degree at most two in the other elementary coordinates. This class is assumed,
not proven from the finite transcript. Energy remains globally pairwise.
"""
from fractions import Fraction as F
from itertools import combinations
from model import weight, fsqrt

def physical_clock(truth,i,x):
    if 'clock_tables' not in truth:return truth['nu'][i]
    z=sum(((x>>j)&1)<<k for k,j in enumerate(truth['clock_contexts'][i]))
    return truth['clock_tables'][i][z]

def recover(n,weights,rates,target=0,kappa=F(1)):
    data={int(k):F(v) for k,v in weights.items()};base=data[0]
    single=[data[1<<i] for i in range(n)];edges={}
    for i,j in combinations(range(n),2):
        t=fsqrt(data[(1<<i)|(1<<j)]*base/(single[i]*single[j]))
        if t!=1:edges[i,j]=t
    fields=[]
    for i in range(n):
        h=single[i]/base
        for (a,b),t in edges.items():
            if i==a or i==b:h*=t
        fields.append(h)
    clocks={str(k):F(v)*2 for k,v in rates.items()};ctx={};tables={};coefs={};nu=[]
    for i in range(n):
        others=[j for j in range(n) if j!=i]
        c={():clocks[f'{i}:0']};nu.append(c[()])
        for j in others:
            v=clocks[f'{i}:{1<<j}']-c[()]
            if v:c[j,]=v
        for j,k in combinations(others,2):
            v=clocks[f'{i}:{(1<<j)|(1<<k)}']-c[()]-c.get((j,),0)-c.get((k,),0)
            if v:c[j,k]=v
        support=sorted(set(j for S in c for j in S))
        if len(support)>10:raise ValueError('Acquired support too large for this table compiler')
        tab=[]
        for z in range(1<<len(support)):
            x=sum(((z>>k)&1)<<j for k,j in enumerate(support))
            val=sum(v for S,v in c.items() if all((x>>j)&1 for j in S))
            if val<=0:raise ValueError('Acquired prefactor not positive')
            tab.append(val)
        ctx[i]=support;tables[i]=tab;coefs[str(i)]={','.join(map(str,S)):str(v) for S,v in c.items()}
    return dict(n=n,edges=edges,fields=fields,nu=nu,target=target,kappa=kappa,clock_contexts=ctx,clock_tables=tables),coefs

def acquire_unknown_support(truth):
    n=truth['n'];weights={};rates={}
    for S in [()]+[(i,) for i in range(n)]+list(combinations(range(n),2)):
        x=sum(1<<i for i in S);weights[str(x)]=str(weight(truth,x))
    for i in range(n):
        others=[j for j in range(n) if j!=i]
        for S in [()]+[(j,) for j in others]+list(combinations(others,2)):
            x=sum(1<<j for j in S);rates[f'{i}:{x}']=str(physical_clock(truth,i,x)/2)
    model,coefs=recover(n,weights,rates,truth['target'],truth['kappa'])
    transcript={'energy_queries':len(weights),'balanced_clock_queries':len(rates),'weights':weights,'balanced_rates':rates,'clock_interface':'unknown-support-degree-two','coefficients':coefs,'scope':'exact synthetic balancing interventions under assumed global pairwise energy and positive degree-two attempt law'}
    return model,transcript

if __name__=='__main__':
    from model import fixture,add_context_clock
    m,t=acquire_unknown_support(add_context_clock(fixture(B=3,m=6,rarity=3),F(1,100)))
    print(t['energy_queries'],t['balanced_clock_queries'],sum(len(v) for v in m['clock_tables'].values()))
