"""Paid two-step observation detects within-cell memory; no hidden rank input."""
from fractions import Fraction as F
from pathlib import Path
from math import factorial
import json
import sys
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'branches'/'physical'))
from multiboundary_positive_events import binomial_interval, dumpable


def acquire(m=32,trials=32_000_000,batch=250000):
    rng=np.random.default_rng(2026102901)
    death_one=death_two=0
    denominator=m**3
    for first in range(0,trials,batch):
        size=min(batch,trials-first)
        # Each logical trial receives a fresh uniform preparation. Hidden
        # microstate is internal, never part of the returned observation.
        label=rng.integers(0,2,size=size)
        threshold=np.where(label==0,1,m*m)
        lost=rng.integers(0,denominator,size=size)<threshold
        death_one+=int(lost.sum())
        alive_threshold=threshold[~lost]
        death_two+=int((rng.integers(0,denominator,size=len(alive_threshold))<alive_threshold).sum())
    return dict(trials=trials,death_at_first_step=death_one,
                death_at_second_step=death_two,survived_both=trials-death_one-death_two,
                primitive_applications=2*trials-death_one,coarse_observations=2*trials-death_one,
                physical_preparations=trials,
                protocol='Fresh preparation; execute two steps unless irreversibly absorbed; do not restart at a coarse live report.')


def infer(receipt):
    n=receipt['trials']
    l1,u1=binomial_interval(receipt['death_at_first_step'],n,F(12))
    l2,u2=binomial_interval(receipt['death_at_second_step'],n,F(12))
    assert u1<F(1,2)
    # f1=1-r1, f2=1-r1-r2; det[[1,f1],[f1,f2]]=r1-r2-r1^2.
    lower=l1*(1-l1)-u2
    upper=u1*(1-u1)-l2
    return dict(first_death_interval=[l1,u1],second_death_interval=[l2,u2],
                hankel_determinant_interval=[lower,upper],
                one_state_time_homogeneous_model_rejected=lower>0,
                linear_realization_dimension_lower_bound=2 if lower>0 else 1,
                hidden_dimension_upper_bound=None)


def run(replay=False):
    raw=ROOT/'results'/'COARSE_MEMORY_RAW_RECEIPT.json'
    if replay:
        receipt=json.loads(raw.read_text())
    else:
        receipt=acquire()
        raw.write_text(json.dumps(receipt,indent=2)+'\n')
    certificate=infer(receipt)
    g=F(1,32)
    true_r1=(g+g**3)/2
    true_r2=((1-g)*g+(1-g**3)*g**3)/2
    determinant=(g-g**3)**2/4
    assert certificate['first_death_interval'][0]<=true_r1<=certificate['first_death_interval'][1]
    assert certificate['second_death_interval'][0]<=true_r2<=certificate['second_death_interval'][1]
    assert certificate['hankel_determinant_interval'][0]<=determinant<=certificate['hankel_determinant_interval'][1]
    assert certificate['one_state_time_homogeneous_model_rejected']
    assert 4/sum((F(12**k,factorial(k)) for k in range(60)),F(0))<F(1,1000)
    result=dict(date='2026-10-29 Australia/Brisbane',receipt=receipt,certificate=certificate,
                joint_failure_probability_upper=F(1,1000),
                true_determinant_checker_only=determinant,all_exact_checks_passed=True,
                learner_inputs='Only fresh-trial count and the two observable death counts.',
                scope='Executed software trajectories. Certifies a need for memory, not a complete two-state model or hidden-rank upper bound.')
    (ROOT/'results'/'COARSE_MEMORY_WITNESS.json').write_text(json.dumps(dumpable(result),indent=2)+'\n')
    print(json.dumps(dumpable(dict(receipt=receipt,certificate=certificate)),indent=2))


if __name__=='__main__':run('--replay' in sys.argv)
