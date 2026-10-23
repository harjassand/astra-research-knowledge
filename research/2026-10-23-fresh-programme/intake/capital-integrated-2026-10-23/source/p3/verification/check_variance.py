"""Independent finite checks, not replacements for the proof.

Run: python check_variance.py
The first three checks use exact rational arithmetic. The nonlinear trajectory
check uses floating point and is explicitly a finite diagnostic.
"""
from fractions import Fraction as F
from itertools import product
import json
import math
from pathlib import Path


def exact_moments(values, probabilities):
    mean = sum((p*w for p,w in zip(probabilities,values)), F(0))
    second = sum((p*w*w for p,w in zip(probabilities,values)), F(0))
    return mean,second,second/(mean*mean)


def K(r):
    return (1+r)**2/(4*r)


def run():
    out={}
    rs=[F(3,2),F(5,3),F(7,4),F(11,5)]
    ps=[1/(1+r) for r in rs]
    values=[];probs=[]
    for bits in product([0,1],repeat=len(rs)):
        w=F(1);p=F(1)
        for r,q,b in zip(rs,ps,bits):
            w*=r**b;p*=q if b else 1-q
        values.append(w);probs.append(p)
    _,_,ratio=exact_moments(values,probs)
    bound=math.prod(K(r) for r in rs)
    assert ratio==bound
    out['sharp_product']={'R_exact':str(ratio),'bound_exact':str(bound),'pass':True}

    # Interacting weights: fibers still obey product ratio upper bounds.
    n=6;r=F(6,5);s=F(11,10)
    values=[];probs=[]
    for bits in product([0,1],repeat=n):
        w=r**sum(bits)*s**sum(bits[i]*bits[(i+1)%n] for i in range(n))
        values.append(w);probs.append(F(1,2**n))
    _,_,ratio=exact_moments(values,probs)
    bound=K(r*s*s)**n
    assert ratio<=bound
    out['interacting_weight']={'R_exact':str(ratio),'bound_exact':str(bound),
                               'R':float(ratio),'bound':float(bound),'pass':True}

    r=F(2);T=20;q=1/(1+r**T)
    _,_,ratio=exact_moments([F(1),r**T],[1-q,q])
    correct=K(r**T);incorrect=K(r)**T
    assert ratio==correct and ratio>incorrect
    out['persistent_mode']={'R':float(ratio),'correct_bound':float(correct),
                            'incorrect_independence_bound':float(incorrect),
                            'unsound_bound_factor':float(ratio/incorrect),'pass':True}

    # Nonlinear contractive dynamics: X_{t+1}=rho*tanh(X_t)+sigma*U_t.
    T=12;rho=.61;sigma=.3;eta=.4
    logw=[]
    for bits in product([0,1],repeat=T):
        x=0.;g=0.
        for u in bits:
            x=rho*math.tanh(x)+sigma*u
            g-=eta*x
        logw.append(g)
    cs=[eta*sigma*(1-rho**(T-t))/(1-rho) for t in range(T)]
    observed=[]
    for t in range(T):
        mask=1<<(T-1-t)
        observed.append(max(abs(logw[i]-logw[i^mask]) for i in range(2**T)))
    assert all(o<=c+1e-12 for o,c in zip(observed,cs))
    weights=[math.exp(v) for v in logw]
    mean=sum(weights)/len(weights)
    ratio=(sum(w*w for w in weights)/len(weights))/mean**2
    bound=math.prod(math.cosh(c/2)**2 for c in cs)
    assert ratio<=bound+1e-12
    out['nonlinear_contracting']={'R':ratio,'bound':bound,
                                  'c_max':max(cs),'observed_c_max':max(observed),
                                  'all_coordinate_bounds_hold':True,
                                  'arithmetic':'float diagnostic','pass':True}
    eta=.7;T=100
    local=2*(1+math.exp(-2*eta))/(1+math.exp(-eta))**2
    out['rho_zero_horizon_failure']={'T':T,'eta':eta,'R':local**T,
                                     'message':'R grows exponentially even at rho=0'}
    path=Path(__file__).with_name('check_results.json')
    path.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':
    run()
