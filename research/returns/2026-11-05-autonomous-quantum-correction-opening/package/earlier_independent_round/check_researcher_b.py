#!/usr/bin/env python3
"""Finite exact contraction/flux tests and illustrative strip correlations."""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
import numpy as np


def port_contractions():
    count = 0
    correlations = [F(1, 2), F(2, 3), F(3, 5), F(4, 7)]
    for degree in range(1, 5):
        cs, check = correlations[:degree], F(5, 7)
        for data in product((-1, 1), repeat=degree):
            actual = F()
            for ports in product((-1, 1), repeat=degree):
                parity = 1
                for t in ports: parity *= t
                weight = 1 + check * parity
                for c, s, t in zip(cs, data, ports): weight *= 1 + c*s*t
                actual += weight
            coeff, parity = check, 1
            for c, s in zip(cs, data): coeff, parity = coeff*c, parity*s
            assert actual == 2**degree * (1 + coeff*parity)
            count += 1
    return count


def small_rectangle():
    vertices = tuple(product(range(3), repeat=2))
    idx = {p: i for i, p in enumerate(vertices)}
    edges = [(idx[x,y],idx[x+dx,y+dy]) for x,y in vertices
             for dx,dy in ((1,0),(0,1)) if (x+dx,y+dy) in idx]
    u,v = idx[0,1],idx[2,1]
    zs = {(s,t):0 for s,t in product((-1,1),repeat=2)}
    for spins in product((-1,1),repeat=9):
        w = 3**sum(spins[a]==spins[b] for a,b in edges)
        zs[spins[u],spins[v]] += w
    assert zs[1,1]==zs[-1,-1] and zs[1,-1]==zs[-1,1]
    same,opp = zs[1,1],zs[1,-1]
    a,c = F(same+opp,2),F(same-opp,same+opp)
    for s,t in zs: assert zs[s,t] == a*(1+c*s*t)
    return {'vertices':9,'edges':len(edges),'endpoint_correlation':str(c)}


def ribbon_correlation(width,length,j=1.0):
    spins = np.asarray(tuple(product((-1,1),repeat=width)),dtype=float)
    vertical = j*np.sum(spins[:,:-1]*spins[:,1:],axis=1)
    logs = j*(spins@spins.T)+(vertical[:,None]+vertical[None,:])/2
    transfer = np.exp(logs-logs.max())
    boundary = np.exp((vertical-vertical.max())/2)
    sign = spins[:,width//2]
    den,num = boundary.copy(),boundary*sign
    for _ in range(length):
        den,num = transfer@den,transfer@num
        scale=den.max();den/=scale;num/=scale
    return float((boundary*sign)@num/(boundary@den))


def flux_check():
    states = tuple(product((-1,1),repeat=7))
    edges = ((0,3),(1,4),(1,5),(2,6),(3,4),(5,6))
    weights = {s:101**sum(s[a]==s[b] for a,b in edges) for s in states}
    errors = lambda s:sum(v==-1 for v in s[:3])
    code_z = sum(w for s,w in weights.items() if errors(s)==0)
    shell_z = sum(w for s,w in weights.items() if errors(s)==1)
    kernel,flux,balance = {},F(),0
    for s in states:
        transitions=[];off=F()
        for bit in range(7):
            y=list(s);y[bit]*=-1;y=tuple(y)
            p=F(weights[y],7*(weights[s]+weights[y]))
            rev=F(weights[s],7*(weights[s]+weights[y]))
            assert weights[s]*p==weights[y]*rev
            balance+=1;transitions.append((y,p));off+=p
            if errors(s)<=1<errors(y):flux+=weights[s]*p
        transitions.append((s,1-off));kernel[s]=transitions
    flux/=code_z
    coarse=F(3,7)*F(shell_z,code_z)
    assert flux<=coarse
    alive={s:F(w,code_z) for s,w in weights.items() if errors(s)==0}
    records=[]
    for t in range(1,13):
        nxt={}
        for s,mass in alive.items():
            for y,p in kernel[s]:
                if errors(y)<=1:nxt[y]=nxt.get(y,F())+mass*p
        alive=nxt;failed=1-sum(alive.values(),F())
        assert failed<=t*flux and failed<=t*coarse
        records.append({'steps':t,'exit_probability':float(failed),'stationary_flux_bound':float(t*flux)})
    return {'physical_states':len(states),'detailed_balance_checks':balance,
            'flux_over_code_mass':str(flux),'coarse_bound_per_step':str(coarse),
            'exit_bounds_checked':len(records),'records':records}


def parity_mask_repair():
    u=F(3,5);records=[]
    for width in range(1,6):
        fields=[F(1,10+i) for i in range(width)]
        zs={};corrs={}
        for endpoint in (-1,1):
            z=F();z0=F();cor=F()
            for masks in product((-1,1),repeat=width):
                for interior in product((-1,1),repeat=width-1):
                    chain=(1,)+interior+(endpoint,)
                    value=F(1)
                    for i,mask in enumerate(masks):value*=1+u*chain[i]*mask*chain[i+1]
                    z0+=value
                    parity=endpoint
                    for mask in masks:parity*=mask
                    cor+=value*parity
                    for field,mask in zip(fields,masks):value*=1+field*mask
                    z+=value
            zs[endpoint]=z;corrs[endpoint]=cor/z0
            assert cor/z0==u**width
        expected=u**width
        for field in fields:expected*=field
        bias=(zs[1]-zs[-1])/(zs[1]+zs[-1])
        assert bias==expected
        records.append({'width':width,'zero_field_readout_correlation':str(u**width),
                        'masked_field_bias':str(bias)})
    return {'widths_checked':5,'records':records}


def main():
    numerical=[]
    for width in (1,3,5,7):
        for length in (8,32,128,512):
            value=ribbon_correlation(width,length)
            if width==1:
                expected=float(np.tanh(1.0)**length)
                assert abs(value-expected)<=1e-11*max(expected,1e-100)
            numerical.append({'coupling':1.0,'width':width,'length':length,'endpoint_correlation':value})
    result={'scope':'Finite exact identities and flux checks; numerical ribbons are illustrative only, not asymptotic or physical validation.',
            'exact_port_contractions':port_contractions(),'exact_small_rectangle':small_rectangle(),
            'exact_flux_test':flux_check(),'parity_mask_repair':parity_mask_repair(),
            'illustrative_ribbons':numerical}
    target=Path(__file__).with_name('researcher_b_checks.json')
    target.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
