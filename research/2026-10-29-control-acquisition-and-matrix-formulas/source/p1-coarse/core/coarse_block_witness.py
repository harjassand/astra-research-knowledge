"""A separately paid pilot chooses long probes that reveal coarse hidden memory."""
from fractions import Fraction as F
from pathlib import Path
from math import ceil, factorial
import json
import sys
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'branches'/'physical'))
from multiboundary_positive_events import binomial_interval,dumpable


def run(replay=False):
    raw_path=ROOT/'results'/'COARSE_BLOCK_RAW_RECEIPT.json'
    if replay:
        receipt=json.loads(raw_path.read_text())
    else:
        rng=np.random.default_rng(2026102902)
        m,den=32,32**3
        pilot_n=2048
        hidden=rng.integers(0,2,size=pilot_n)
        threshold=np.where(hidden==0,1,m*m)
        pilot_deaths=int((rng.integers(0,den,size=pilot_n)<threshold).sum())
        # Pilot is for design only. Any resulting finite L leaves the fresh
        # main confidence statement valid; no accurate pilot estimate is assumed.
        length=max(1,ceil(F(pilot_n,2*max(1,pilot_deaths))))
        n=10000
        hidden=rng.integers(0,2,size=n)
        threshold=np.where(hidden==0,1,m*m)
        alive=np.ones(n,dtype=bool)
        survivor_counts=[]
        for block in range(2):
            for _ in range(length):
                active=np.flatnonzero(alive)
                survive=rng.integers(0,den,size=len(active))>=threshold[active]
                alive[active[~survive]]=False
            survivor_counts.append(int(alive.sum()))
        n1,n2=survivor_counts
        receipt=dict(pilot_trials=pilot_n,pilot_deaths=pilot_deaths,chosen_block_length=length,
            main_trials=n,survived_first_block=n1,survived_both_blocks=n2,
            primitive_applications=pilot_n+length*(n+n1),
            coarse_observations=pilot_n+n+n1,physical_preparations=pilot_n+n,
            cost_rule='Read only at each block endpoint. Charge the whole block even when backend absorption occurs earlier. Every trial is freshly prepared.')
        raw_path.write_text(json.dumps(receipt,indent=2)+'\n')
    n,length=receipt['main_trials'],receipt['chosen_block_length']
    l1,u1=binomial_interval(receipt['survived_first_block'],n,F(12))
    l2,u2=binomial_interval(receipt['survived_both_blocks'],n,F(12))
    determinant_interval=[l2-u1*u1,u2-l1*l1]
    assert determinant_interval[0]>0
    g=F(1,32)
    true_f1=((1-g**3)**length+(1-g)**length)/2
    true_f2=((1-g**3)**(2*length)+(1-g)**(2*length))/2
    true_det=true_f2-true_f1*true_f1
    assert l1<=true_f1<=u1 and l2<=true_f2<=u2
    assert determinant_interval[0]<=true_det<=determinant_interval[1]
    assert 4/sum((F(12**k,factorial(k)) for k in range(60)),F(0))<F(1,1000)
    result=dict(receipt=receipt,first_block_survival_interval=[l1,u1],
        second_block_survival_interval=[l2,u2],hankel_determinant_interval=determinant_interval,
        linear_realization_dimension_lower_bound=2,hidden_dimension_upper_bound=None,
        joint_failure_probability_upper=F(1,1000),true_determinant_checker_only=true_det,
        all_exact_checks_passed=True,
        scope='Fresh software trajectories on the same source and observation interface as the short witness; pilot cost included; no precision oracle or hidden-rank promise.')
    (ROOT/'results'/'COARSE_BLOCK_WITNESS.json').write_text(json.dumps(dumpable(result),indent=2)+'\n')
    print(json.dumps(dumpable(result),indent=2))


if __name__=='__main__':run('--replay' in sys.argv)
