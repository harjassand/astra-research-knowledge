"""Unknown-support kinetic recovery from fast reverse-relaxation interrogations.
An exact computational experiment, not a laboratory calibration. Physical use
requires local state/context preparation and access to the original conditional
clock after preparation; preparation, resets and statistical errors are not free.
"""
from fractions import Fraction as F
from itertools import combinations
from model import weight,fsqrt
from kinetic_tomography import recover,physical_clock

def energy_model(n,weights):
    data={int(k):F(v) for k,v in weights.items()};w0=data[0];ss=[data[1<<i] for i in range(n)];edges={};fields=[]
    for i,j in combinations(range(n),2):
        t=fsqrt(data[(1<<i)|(1<<j)]*w0/(ss[i]*ss[j]))
        if t!=1:edges[i,j]=t
    for i in range(n):
        h=ss[i]/w0
        for (a,b),t in edges.items():
            if i==a or i==b:h*=t
        fields.append(h)
    return dict(n=n,fields=fields,edges=edges)

def ratio_on(model,i,x):
    # m(x with bit i=1)/m(x with bit i=0); x is a context with bit i zero.
    r=model['fields'][i]
    for (a,b),t in model['edges'].items():
        if i==a or i==b:
            j=b if i==a else a;r*=t if (x>>j)&1 else 1/t
    return r

def recover_reverse(n,tr,target=0,kappa=F(1)):
    energy=energy_model(n,tr['weights']);derived={}
    for key,raw in tr['reverse_rates'].items():
        i,x=map(int,key.split(':'));r=ratio_on(energy,i,x)
        downhill_probability=max(F(1),r)/(1+r)
        derived[key]=str(F(raw)/downhill_probability/2)
        assert int(tr['prepared_bit'][key])==(0 if r>=1 else 1)
    model,coefs=recover(n,tr['weights'],derived,target,kappa)
    return model,coefs,derived

def acquire_reverse(truth):
    n=truth['n'];weights={}
    for S in [()]+[(i,) for i in range(n)]+list(combinations(range(n),2)):
        x=sum(1<<i for i in S);weights[str(x)]=str(weight(truth,x))
    energy=energy_model(n,weights);rates={};prep={};workratios=[]
    for i in range(n):
        others=[j for j in range(n) if j!=i]
        for S in [()]+[(j,) for j in others]+list(combinations(others,2)):
            x=sum(1<<j for j in S);r=ratio_on(energy,i,x);xi=0 if r>=1 else 1
            # Oracle returns original elementary rate after resetting local bit.
            # It is NOT a metastable escape rate and no bias is applied during readout.
            xx=x|(xi<<i);xp=xx^(1<<i)
            raw=physical_clock(truth,i,xx)*weight(truth,xp)/(weight(truth,xx)+weight(truth,xp))
            rates[f'{i}:{x}']=str(raw);prep[f'{i}:{x}']=xi;workratios.append(max(r,1/r))
    tr=dict(energy_queries=len(weights),reverse_clock_queries=len(rates),weights=weights,reverse_rates=rates,prepared_bit=prep,clock_interface='unknown-support-degree-two-reverse',maximum_local_excitation_weight_ratio=str(max(workratios)),scope='exact synthetic original-law downhill rates after local/context preparation; no physical measurement performed')
    model,coefs,derived=recover_reverse(n,tr,truth['target'],truth['kappa']);tr['coefficients']=coefs
    return model,tr

if __name__=='__main__':
    from model import fixture,add_context_clock
    m,t=acquire_reverse(add_context_clock(fixture(B=3,m=6,rarity=3),F(1,100)))
    print(t['energy_queries'],t['reverse_clock_queries'],t['maximum_local_excitation_weight_ratio'])
