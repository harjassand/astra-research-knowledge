"""Checks of a restricted ONE-WELL-MIXED-SOURCE kinetic separation frontier.

No physical kinetics are inferred. Multistage countercurrent cascades are excluded.
Use the pre-existing /usr/local/bin/python3; outputs stay beside this script.
"""
import json
import math
import platform
import time
from pathlib import Path

import mpmath as mp
import numpy as np
import scipy
from scipy.integrate import solve_ivp
from scipy.optimize import brentq, minimize

ROOT=Path(__file__).resolve().parent
mp.mp.dps=80


def frontier(al,an,l0,n0,r,pn):
    rho=an/al; gamma=1/(rho-1)
    x=-mp.log1p(-r);v=-mp.log1p(-pn/n0)/rho
    integral=gamma/rho*mp.expm1(rho*v/gamma)
    w0=x/integral
    assert w0>=1
    cost=rho*n0*mp.exp((gamma+1)*mp.log(x)-gamma*mp.log(integral))
    constant=pn*mp.exp((gamma+1)*mp.log(x/v))
    return rho,gamma,x,v,integral,w0,cost,constant


def numerical_ode_check(al,an,l0,n0,r,pn):
    vals=frontier(*map(mp.mpf,[al,an,l0,n0,r,pn]))
    rho,gamma,x,v,integral,w0,cost,constant=map(float,vals)
    gain=math.expm1(rho*v/gamma)
    def rhs(z,y):
        u=(integral/x)/(1+(z/x)*gain)
        l,n,scaled_cost=y
        return [-l,-rho*n*u,rho*n*u**(-gamma)/cost]
    sol=solve_ivp(rhs,[0,x],[l0,n0,0.],method='DOP853',rtol=2e-11,atol=1e-12)
    l,n,c=sol.y[:,-1]
    expected_l=l0*(1-r);expected_n=n0-pn
    errors=dict(L_relative=l/expected_l-1,N_relative=n/expected_n-1,
                cost_relative=c-1)
    assert sol.success and max(map(abs,errors.values()))<1e-8
    return dict(inputs=dict(a_L=al,a_N=an,L0=l0,N0=n0,recovery=r,N_product=pn),
                success=bool(sol.success),function_evaluations=sol.nfev,
                final_L=l,final_N=n,scaled_cost=c,relative_errors=errors)


def convex_check():
    rho,gamma,x,v,integral,w0,cost,_=map(float,frontier(*map(mp.mpf,[.6,1.,1.,1.,.8,.5])))
    n=64;edges=np.linspace(0,v,n+1);dv=v/n
    weights=(np.exp(-rho*edges[:-1])-np.exp(-rho*edges[1:]))/rho
    mean_w=x/v
    fun=lambda z: float(weights @ z**(gamma+1))
    jac=lambda z: weights*(gamma+1)*z**gamma
    res=minimize(fun,np.ones(n),jac=jac,method='SLSQP',
                 constraints=[dict(type='eq',fun=lambda z:z.mean()-1,
                                   jac=lambda z:np.ones(n)/n)],
                 bounds=[(1/mean_w,None)]*n,
                 options=dict(ftol=1e-13,maxiter=300))
    finite_w=weights**(-1/gamma);finite_w*=x/(dv*finite_w.sum())
    finite_cost=rho*float(weights @ finite_w**(gamma+1))
    numerical_cost=rho*mean_w**(gamma+1)*res.fun
    assert res.success and abs(numerical_cost/finite_cost-1)<1e-8
    assert finite_cost>=cost*(1-1e-12)
    return dict(cells=n,success=bool(res.success),message=str(res.message),
                numerical_cost=numerical_cost,finite_cell_optimum=finite_cost,
                continuum_optimum=cost,relative_optimizer_error=numerical_cost/finite_cost-1,
                discretization_excess=finite_cost/cost-1)


def nonlinear_cohort_check():
    rng=np.random.default_rng(20261027)
    al,an,l0,n0,b=.6,1.,1.,5.,.25
    l,n=l0,n0;pl=pn=an_gross=0.
    for _ in range(80):
        wanted=min(b*rng.uniform(.02,.95),.95*(l+n))
        loaded=lambda z:l*(-np.expm1(-al*z))+n*(-np.expm1(-an*z))
        hi=1.
        while loaded(hi)<wanted:hi*=2
        z=brentq(lambda z:loaded(z)-wanted,0,hi,xtol=1e-14)
        cl=l*(-np.expm1(-al*z));cn=n*(-np.expm1(-an*z))
        h=rng.uniform(0,8)
        outl=cl*np.exp(-al*h);outn=cn*np.exp(-an*h)
        l-=outl;n-=outn;pl+=outl;pn+=outn;an_gross+=cn
    floor=(an/al)*max(0,n0-pn-b)*(-math.log1p(-pl/l0))
    mass_error=max(abs(l+pl-l0),abs(n+pn-n0))
    assert mass_error<1e-12 and an_gross>=floor
    return dict(seed=20261027,cycles=80,L0=l0,N0=n0,bed_capacity=b,
                recovery=pl/l0,product_purity=pl/(pl+pn),gross_N_captures=an_gross,
                general_N_capture_floor=floor,mass_balance_error=mass_error,
                scope='Finite nonlinear loading with wash recycling into ONE source; synthetic kinetics.')


start=time.perf_counter()
rows=[]
al,an=mp.mpf(103)/133,mp.mpf(1)
r,p=mp.mpf('.9'),mp.mpf('.99')
for qtext in ['.1','.01','.0001','.00005']:
    q=mp.mpf(qtext);l0=mp.mpf(1);n0=1/q;pn=r*(1-p)/p
    rho,g,x,v,i,w0,cost,constant=frontier(al,an,l0,n0,r,pn)
    rows.append(dict(initial_L_over_N=qtext,kinetic_ratio=str(al),
                     recovery=str(r),purity=str(p),
                     status='ILLUSTRATIVE_MOBILITY_RATIO_IS_NOT_ACQUIRED_BINDING_KINETICS',
                     single_wash_max_recovery_of_initially_loaded_L=str(mp.exp(g*mp.log(q*(1-p)/p))),
                     optimal_N_captures_per_L=str(cost/r),
                     constant_N_captures_per_L=str(constant/r),
                     constant_relative_excess=str(constant/cost-1),
                     starting_wash_dose=str(mp.log(w0)/(an-al)),
                     general_floor_B_equals_100_L0=str(rho*max(0,n0-pn-100)*x/r)))
result=dict(status='SCOPED_MODEL_CHECKS_ONLY',mission='NOT_ACHIEVED',historical_novelty='UNKNOWN',
            crucial_scope='ONE well-mixed recycle source. No countercurrent intermediate inventories. No ion-specific equilibrium affinity. No physical rate/material qualification.',
            illustrative_rows=rows,
            ode_checks=[numerical_ode_check(.6,1.,1.,1.,.8,.5),
                        numerical_ode_check(103/133,1.,1.,1e4,.9,.9*.01/.99)],
            convex_check=convex_check(),nonlinear_finite_source=nonlinear_cohort_check(),
            execution=dict(python=platform.python_version(),numpy=np.__version__,
                           scipy=scipy.__version__,mpmath=mp.__version__,
                           decimal_digits=mp.mp.dps,elapsed_seconds=time.perf_counter()-start))
(ROOT/'COMPUTATIONAL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
