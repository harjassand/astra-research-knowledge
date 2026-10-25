#!/usr/bin/env python3
"""Independent exhaustive-subset audit of the ordinary-valve comparator."""
from pathlib import Path
import itertools
import json
import numpy as np
import phase_valve_model as v


def main():
    rng=np.random.default_rng(112358)
    worst=0.0
    for trial in range(100):
        n=8
        r=np.exp(rng.normal(0,1,n))
        m=np.exp(rng.normal(0,.3,n))
        qmax=1.25*m.sum()
        gm=float(v.aperture_conductance(np.full((1,v.NPHASE),v.U0/(1+v.BETA)))[0])
        gf=float(v.aperture_conductance(np.zeros((1,v.NPHASE)))[0])
        re=r+1/gm
        p0=qmax/np.sum(1/re)
        pmax=5*p0
        wmax=p0*qmax*rng.uniform(.4,3)
        got=v.benchmark(r,m,qmax,pmax,wmax,'ordinary_individual_valves_max_adequate_count')['adequate_fraction']
        best=0.0
        for mask in itertools.product([False,True],repeat=n):
            chosen=np.array(mask)
            if not chosen.any():
                continue
            pp=float(np.max(re[chosen]*m[chosen]*(1+1e-9)))
            qq=pp/(r+1/gf)
            qq=np.maximum(qq,chosen*m*(1+1e-9))
            if pp<=pmax+1e-9 and qq.sum()<=qmax+1e-9 and pp*qq.sum()<=wmax+1e-9:
                best=max(best,float(np.mean(qq>=m)))
        worst=max(worst,abs(got-best))
        assert abs(got-best)<1e-12,(trial,got,best)
    doc=dict(cases=100,branches=8,subsets_each=256,maximum_fraction_difference=worst,
             scope='steady supplied-geometry/demand bounded-conductance common-pressure allocation only',
             repair='product-based critical-pressure eligibility, 1e-12 relative roundoff tolerance')
    (Path(__file__).resolve().parent/'allocation_comparator_check.json').write_text(json.dumps(doc,indent=2)+'\n')
    print(json.dumps(doc,indent=2))


if __name__=='__main__':
    main()
