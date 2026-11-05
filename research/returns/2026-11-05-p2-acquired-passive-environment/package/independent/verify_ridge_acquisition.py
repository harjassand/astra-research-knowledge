"""Numerical checks accompany, and do not replace, the analytic proofs.
Run: python verify_ridge_acquisition.py
Only numpy/scipy used; seed fixed. No external interaction.
"""
from pathlib import Path
from itertools import product
import json, math
import numpy as np
from scipy.optimize import minimize_scalar

HERE = Path(__file__).resolve().parent
rng = np.random.default_rng(20261105)

def binary_kl(p, q):
    return (p * math.log(p / q) if p else 0.0) + ((1-p) * math.log((1-p)/(1-q)) if p<1 else 0.0)

checks = []
for d in range(1, 13):
    signs = np.array(list(product((-1., 1.), repeat=d)))
    gamma = 1.
    q = (1 + math.exp(-4*gamma))/2
    xs = [rng.uniform(-1,1,d) for _ in range(16)] + [np.ones(d), np.zeros(d)]
    ratios = []
    equality_errors = []
    for x in xs:
        f = np.exp(-gamma*(d-signs@x))
        empirical_second = np.mean(f*f)
        formula = math.exp(-2*gamma*d)*np.prod(np.cosh(2*gamma*x))
        ratios.append(empirical_second/q**d)
        equality_errors.append(abs(empirical_second-formula)/max(formula,1e-300))
    assert max(ratios) <= 1+1e-12
    assert max(equality_errors) < 1e-12
    checks.append({"d":d,"max_second_moment_ratio":max(ratios),"max_relative_identity_error":max(equality_errors)})

pair_checks = []
for d in range(2,10):
    for _ in range(100):
        a = rng.choice([-1.,1.],d); b=rng.choice([-1.,1.],d)
        h = int(np.count_nonzero(a!=b))
        if not h: continue
        x = rng.uniform(-1,1,d)
        log_product = -2*(d)+float((a+b)@x)
        assert log_product <= -2*h+1e-12
        x_star = np.where(a==b,a,0.)
        assert abs((-2*d+float((a+b)@x_star))-(-2*h))<1e-12
        pair_checks.append(True)

bounds=[]
for d in [17,32,64,128]:
    gamma=math.log(d)/4
    q=(1+math.exp(-4*gamma))/2
    p=2.**(-d); delta=.05
    kl=binary_kl(p,1-delta)
    lower=2*q**(-d)*kl
    simpler=2/math.e*2.**d*kl
    upper=32*2.**d*math.log(2*2.**d/delta)
    bounds.append({"d":d,"gamma":gamma,"threshold_condition_exp_minus_gamma_lt_half":math.exp(-gamma)<.5,"lower_exposure_per_sigma_squared":lower,"simple_lower_per_sigma_squared":simpler,"exhaustive_upper_per_sigma_squared":upper,"upper_lower_ratio":upper/lower})

# Positive algorithm on a nonmonotone link: the line optimization is needed.
d=24; sigma=.1; epsilon=.1; delta=.05; L=2.25

def g(t): return np.sin(2*np.asarray(t))+.25*np.asarray(t)
Delta=abs(float(g(1/d)-g(-1/d)))
tau_axis=4*sigma*sigma/(Delta*Delta)*math.log(2*d/delta)
K=math.ceil(4*L/epsilon)+1
ts=np.linspace(-1,1,K)
tau_grid=32*sigma*sigma/(epsilon*epsilon)*math.log(4*K/delta)
res=minimize_scalar(lambda t: -float(g(t)),bounds=(-1,1),method='bounded',options={'xatol':1e-14})
true_max=max(float(g(-1)),float(g(1)),-float(res.fun))
regrets=[]; sign_recoveries=0
for _ in range(300):
    a=rng.choice([-1.,1.],d)
    plus=g(a/d)+rng.normal(0,sigma/math.sqrt(tau_axis),d)
    minus=g(-a/d)+rng.normal(0,sigma/math.sqrt(tau_axis),d)
    b=np.where(plus-minus>=0,1.,-1.)
    sign_recoveries += int(np.array_equal(a,b) or np.array_equal(a,-b))
    exact=g(ts*float(a@b)/d)
    obs=exact+rng.normal(0,sigma/math.sqrt(tau_grid),K)
    value=float(exact[int(np.argmax(obs))])
    regrets.append(true_max-value)

out={"note":"Numerical identity checks and a finite synthetic demonstration; not a proof or physical validation.","seed":20261105,"second_moment_checks":checks,"pairwise_cap_checks":len(pair_checks),"bounds_delta_0_05":bounds,"positive_demo":{"d":d,"sigma":sigma,"epsilon":epsilon,"delta":delta,"L":L,"axis_contrast":Delta,"axis_exposure_each":tau_axis,"grid_K":K,"grid_exposure_each":tau_grid,"total_exposure":2*d*tau_axis+K*tau_grid,"trials":len(regrets),"sign_recoveries":sign_recoveries,"epsilon_successes":sum(r<=epsilon for r in regrets),"max_regret":max(regrets),"mean_regret":float(np.mean(regrets))}}
(HERE/'verification.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({"identity_checks_passed":True,"pairwise_checks":len(pair_checks),"positive_demo":out['positive_demo'],"bounds":bounds},indent=2))
