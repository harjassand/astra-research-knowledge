"""Conventional conditional averaging + product Poincare/coloring certificate.

The averaged rates and sources are the exact ordinary conditional averages.
This comparator imports their implementation from root and independently
constructs a deliberately conventional dimension-free coupling estimate:
two-color the dependence path of slow rate residuals, then use the conditional
fast spectral gap. No fast-monomial expansion or acquired slow gap is needed.
"""
import json
import math
from pathlib import Path
import sys
import time

import numpy as np
from scipy.special import expit

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/"interacting"))
from conditional_decimation import SP, initial_model, one_decimation, prefactors
from audit_local_schur import local_theta


def coloring_theta(bonds, rates):
    n = len(rates)
    gamma = float(prefactors(rates)[0::2].min())
    answer = 0.
    for i in range(1, n, 2):
        for L in SP:
            for s,S in enumerate(SP):
                for R in SP:
                    pl = np.array([expit(2*x*(bonds[i-1]*L+bonds[i]*S)) for x in SP])
                    pr = np.array([expit(2*x*(bonds[i+1]*S+bonds[i+2]*R)) for x in SP])
                    prob = pl[:,None]*pr[None,:]
                    rr = rates[i,:,s,:]
                    mean = float(np.sum(prob*rr))
                    var = float(np.sum(prob*(rr-mean)**2))
                    answer = max(answer, 4*var/(gamma*mean))
    return answer


def response(n, J, alpha):
    bonds,rates,weights,clocks=initial_model(n,J,alpha)
    begin=time.perf_counter()
    levels=[]
    while len(weights)>1:
        theta=coloring_theta(bonds,rates)
        sharp=local_theta(bonds,rates,True)
        bonds,rates,weights,record=one_decimation(bonds,rates,weights)
        record['coloring_theta']=theta
        record['root_monomial_theta']=sharp
        levels.append(record)
    variance=1-math.tanh(float(bonds.sum()))**2
    last=weights[0]**2*variance/float(prefactors(rates)[0,1,1])
    lower=upper=center=float(last)
    for rec in reversed(levels):
        b,theta=rec['fast_response'],rec['coloring_theta']
        # Standard variational lower bound from the lifted slow trial alone.
        upper=(1+theta)*upper+b+2*math.sqrt(theta*upper*b)
        center+=b
    return {'n':n,'J':J,'alpha':alpha,'lower':lower,'upper':upper,
            'center':center,'relative_width':(upper-lower)/lower,
            'seconds':time.perf_counter()-begin,'levels':levels,
            'arithmetic':'float64 evaluations of exact-arithmetic inequalities'}


def main():
    out=[]
    for n in [31,127,511,2047]:
        row=response(n,.5*math.log(n+1),1e-5)
        out.append(row)
        print(json.dumps({k:v for k,v in row.items() if k!='levels'}),flush=True)
    Path(__file__).with_name('coloring_averaging_results.json').write_text(json.dumps(out,indent=2)+'\n')


if __name__=='__main__':main()
