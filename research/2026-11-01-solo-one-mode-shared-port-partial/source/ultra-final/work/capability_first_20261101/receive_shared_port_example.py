"""Receive the emitted certificate directly; import no constructor module."""
from fractions import Fraction as F
from math import prod
from pathlib import Path
import json


def parse(x):
    if isinstance(x,dict):
        if set(x)=={'numerator','denominator'}:return F(int(x['numerator']),int(x['denominator']))
        return {k:parse(v) for k,v in x.items()}
    if isinstance(x,list):return [parse(v) for v in x]
    return x


def fall(n,k):return prod(range(n-k+1,n+1)) if n>=k else 0


def main():
    root=Path('outputs/capability_first_20261101')
    c=parse(json.loads((root/'shared_port_example.json').read_text()))
    def h(a):
        return 1+c['epsilon']/((a+c['shift'])**c['p'])+c['delta']*(c['head_values'][a] if a<c['M'] else 0)
    def actual(a,qq):
        x=c['x0'].copy();x[0]=a;n=a
        for m,q in zip(c['modules'],qq):
            n+=m['r']*q
            for j,i in enumerate(m['indices'][1:],1):x[i]=m['offset'][j]+m['v'][j]*q
        assert sum(x)<=c['count_offset']+c['count_slope']*n
        value=c['lam']*(c['t']*h(a+1)-h(a))
        if a:value+=c['mu']*a*(h(a-1)/c['t']-h(a))
        for src,dst,rate in c['raw']:
            intensity=rate*prod(fall(xx,yy) for xx,yy in zip(x,src))
            if intensity:value+=intensity*(h(a+dst[0]-src[0])-h(a))
        if n>=c['head']:assert value<=-c['nu']
        return value
    assert c['rho']>1 and c['rho']**c['count_slope']<=c['t']
    for src,dst,rate in c['raw']:
        change=dst[0]-src[0]
        for m in c['modules']:
            pivot=next(i for i in range(1,len(m['v'])) if m['v'][i])
            gi=m['indices'][pivot];dq=F(dst[gi]-src[gi],m['v'][pivot]);assert dq.denominator==1
            for j,index in enumerate(m['indices'][1:],1):assert dst[index]-src[index]==dq*m['v'][j]
            change+=m['r']*dq
        assert change==0
    ratebound=c['lam']+c['mu']*c['head']+sum(rate*prod(xx**yy for xx,yy in zip(c['head_count_bounds'],src)) for src,dst,rate in c['raw'])
    assert ratebound==c['head_rate_bound']
    assert c['head_drift_bound']==dict(coefficient=F(3,2)*(c['zeta']+ratebound),base=c['t'],exponent=c['head']+1)
    assert c['stationary_total_moment_bound']==dict(coefficient=c['head_drift_bound']['coefficient']/c['zeta'],powers=[[c['rho'],c['count_offset']],[c['t'],c['head']+1]])
    count=0
    for i in range(len(c['modules'])):
        for q in [c['head'],10**100+c['head']]:
            coords=[0]*len(c['modules']);coords[i]=q
            for a in [0,c['M']-1,c['M'],c['Acut']-1,c['Acut'],c['head']]:
                actual(a,coords);count+=1
    for a in [c['head'],c['head']+1]:actual(a,[0]*len(c['modules']));count+=1
    result=dict(serialized_raw_certificate_received=True,actual_generator_states=count,
                head_rate_and_factored_moment_reconstructed=True,
                no_constructor_import=True,
                scope='Independent arithmetic receiving of this concrete certificate; not an independent whole mathematical audit.')
    (root/'shared_port_example_receiving.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
