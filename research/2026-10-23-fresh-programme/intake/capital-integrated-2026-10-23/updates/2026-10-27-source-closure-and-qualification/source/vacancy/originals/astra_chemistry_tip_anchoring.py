"""Astra Chemistry: exact active-tip docking/undocking model.

A rooted product's last covalently attached PNA/DNA adapter can be reversibly
bound at its cognate template address. Both bound B and unbound U preserve the
correct chemical parent. Correct incorporation occurs in B with hazard a; other
reactions may damage either state. U rebinds with rate v and can suffer wrong
stable chemistry with rate w_U. All rates are hypothetical until measured.
"""
import math
import numpy as np
from scipy.stats import binomtest


def correct_first_passage(a,u,v,w_U,d=0.,w_B=0.):
    """P(correct amide before any irreversible error | starting docked B).

    B --a--> correct; B --u--> U; B --w_B+d--> dead.
    U --v--> B; U --w_U+d--> dead.
    Returns exact a/[a+w_B+d+u(w_U+d)/(v+w_U+d)] if U's total exit >0.
    """
    assert a>0 and min(u,v,w_U,d,w_B)>=0
    if v+w_U+d==0:
        return a/(a+w_B+d+u)
    return a/(a+w_B+d+u*(w_U+d)/(v+w_U+d))


def linear_solver(a,u,v,w_U,d=0.,w_B=0.):
    Q=np.array([[-(a+u+w_B+d),u],
                [v,-(v+w_U+d)]],float)
    # Absorption probability solves (-Q) h=[a,0].
    if abs(np.linalg.det(Q))<1e-14: return float('nan')
    return float(np.linalg.solve(-Q,[a,0])[0])


def simulate(a,u,v,w_U,d,w_B,n=100000,seed=12):
    """Independent Gillespie event simulation, finite-state until absorption."""
    rng=np.random.default_rng(seed)
    success=0
    for _ in range(n):
        state=0
        while True:
            if state==0:
                rates=[a,u,w_B+d]
                choice=rng.choice(3,p=np.array(rates)/sum(rates))
                if choice==0:
                    success+=1;break
                if choice==2:break
                state=1
            else:
                rates=[v,w_U+d]
                total=sum(rates)
                if total==0:break
                if rng.random()<v/total:state=0
                else:break
    return success/n


def expected_time_without_damage(a,u,v):
    """Correct incorporation time when both wrong/damage rates are zero."""
    if v==0 and u>0:return math.inf
    return (1+u/v)/a if v>0 else 1/a


def check():
    rng=np.random.default_rng(20261027)
    worst=0
    for _ in range(600):
        a=10**rng.uniform(-3,0)
        u=10**rng.uniform(-4,0)
        v=10**rng.uniform(-3,1)
        wU=10**rng.uniform(-6,-2)
        d=10**rng.uniform(-8,-4)
        wB=10**rng.uniform(-8,-4)
        x=correct_first_passage(a,u,v,wU,d,wB)
        y=linear_solver(a,u,v,wU,d,wB)
        worst=max(worst,abs(x-y))
        assert abs(x-y)<2e-12
    # Event-driven cross-check with representative non-negligible failure.
    rates=(.05,.02,.08,.008,.00001,.00002)
    exact=correct_first_passage(*rates)
    observed=simulate(*rates,n=55000,seed=7121)
    assert abs(observed-exact)<.01,(observed,exact)
    # No irreversible event => eventual success certain as long as redocking possible.
    assert abs(correct_first_passage(.05,.2,.01,0,0,0)-1)<1e-12
    # If redocking impossible, undocking irreversibly forfeits competent orientation.
    assert abs(correct_first_passage(.05,.2,0,0,0,0)-.05/.25)<1e-12
    print('600 independent CTMC linear solves: max discrepancy',worst)
    print('55000 Gillespie histories: observed',observed,'exact',exact)


if __name__=='__main__':
    check()
    for v in (.01,.1,1,10):
        p=correct_first_passage(a=.05,u=.01,v=v,w_U=1e-4,d=1e-7)
        print('rebind rate',v,'correct/stage',p,
              'F64',p**64,'F1024',p**1024,'mean stage time if zero hazards',expected_time_without_damage(.05,.01,v))
