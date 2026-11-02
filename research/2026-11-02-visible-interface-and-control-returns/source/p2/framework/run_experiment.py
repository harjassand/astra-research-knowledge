#!/usr/bin/env python3
"""Independent experiment: drift-free learning and empirical optimality certificates.

Target is a specific nonlinear, discretized diffusion; none of its b(x) formula is
passed to the learned committor or the fitted-drift baseline. The simulator uses
its formula solely to generate experimental trajectories.

Not a proof of practical performance, continuous-time attainability, novelty, or
reliable out-of-distribution scientific control.
"""
import json
from pathlib import Path
import numpy as np
from scipy.ndimage import gaussian_filter1d
from scipy.stats import beta
from scipy.special import roots_hermitenorm

OUT = Path(__file__).parent
SEED = 20261102
T = 2.0
DT = .01
STEPS = round(T / DT)
SIGMA = .9
LAMBDA = .4
X0 = -1.
GOAL = .5
UMAX = 3.0
XGRID = np.linspace(-2.5, 2.5, 501)
DX = XGRID[1]-XGRID[0]
W = np.exp(1. / LAMBDA)

# Hidden simulator mechanism, never used for fitting or controller construction.
def hidden_physical_drift(x):
    return 2.0*(x-x*x*x)

def sim(n, seed, policy=None, save_path=True, save_increments=False):
    rng=np.random.default_rng(seed)
    x=np.full(n, X0, dtype=float)
    hist=np.empty((STEPS+1,n),dtype=np.float32) if save_path else None
    if save_path: hist[0]=x
    c=np.zeros(n)
    bytime = []
    for j in range(STEPS):
        u=np.zeros_like(x) if policy is None else np.clip(policy(j,x),-UMAX,UMAX)
        c += u*u*DT
        x = x + (hidden_physical_drift(x)+SIGMA*u)*DT+SIGMA*np.sqrt(DT)*rng.normal(size=n)
        if save_path: hist[j+1]=x
        if save_increments: bytime.append(u.astype(np.float32))
    success=(x>GOAL).astype(float)
    perf=success-(LAMBDA/2.)*c
    return {'hist':hist,'x':x,'success':success,'energy':c,'payoff':perf,'controls':bytime}

def estimate_h_direct(hist, bandwidth=0.17, time_smooth=1.5):
    """Learns P(X_T > target | X_t=x) by binned conditional regression."""
    centers = XGRID
    ids=np.clip(np.rint((hist-centers[0])/DX).astype(np.int32),0,len(centers)-1)
    s=(hist[-1]>GOAL).astype(float)
    w=np.empty((STEPS+1,len(centers)),dtype=float)
    for t in range(STEPS+1):
        c=np.bincount(ids[t],minlength=len(centers))
        a=np.bincount(ids[t],weights=s,minlength=len(centers))
        sc=gaussian_filter1d(c.astype(float), bandwidth/DX,mode='nearest')
        sa=gaussian_filter1d(a,bandwidth/DX,mode='nearest')
        # Smooth estimate of conditional success probability with conservative
        # no-effect prior in regions with no observed training trajectories.
        w[t]=np.divide(sa,sc+1e-9,out=np.zeros_like(sa),where=sc>0)
    # one normalized prediction for all terminal states is available by definition
    h=1+(W-1)*w
    h[-1]=np.where(centers>GOAL,W,1.)
    # Derivative of log h gives the matched-noise Doob feedback.
    logh=np.log(h)
    if time_smooth:
        logh[:-1]=gaussian_filter1d(logh[:-1],time_smooth,axis=0,mode='nearest')
    grad=np.gradient(logh,DX,axis=1,edge_order=2)
    return SIGMA*np.clip(grad[:-1],-UMAX/SIGMA,UMAX/SIGMA),h

def estimate_drift(hist, bandwidth=.19):
    # Same passive information as direct model-free learner.
    x=hist[:-1].ravel().astype(float)
    dx=np.diff(hist.astype(float),axis=0).ravel()/DT
    z=np.clip(np.rint((x-XGRID[0])/DX).astype(np.int32),0,len(XGRID)-1)
    c=np.bincount(z,minlength=len(XGRID)).astype(float)
    a=np.bincount(z,weights=dx,minlength=len(XGRID))
    w=bandwidth/DX
    bc=gaussian_filter1d(c,w)
    ba=gaussian_filter1d(a,w)
    out=np.divide(ba,bc+1e-12)
    # Extreme unsampled tails: no aggressive control extrapolation; flat clipping.
    return np.clip(out,-5,5)

def estimate_drift_polynomial(hist, degree=5):
    """Strong model-based comparator: fit a generic polynomial drift dictionary.

    This reconstruction sees exactly the same state/increment trajectories as
    the conditional learner, but receives a smooth polynomial inductive bias.
    No true physical coefficients are supplied.
    """
    x=hist[:-1].ravel().astype(float)
    y=np.diff(hist.astype(float),axis=0).ravel()/DT
    # Low-degree sufficient statistics; numerically stable scaled x.
    z=x/1.5
    exps=np.arange(degree+1)
    G=np.array([np.sum(z**k) for k in range(2*degree+1)])
    XTX=np.array([[G[i+j] for j in exps] for i in exps])
    XTy=np.array([np.dot(y,z**j) for j in exps])
    reg=np.diag(np.r_[1e-5,np.full(degree,1e-3)])*len(x)
    coef=np.linalg.solve(XTX+reg,XTy)
    fitted=np.polynomial.polynomial.polyval(XGRID/1.5,coef)
    return np.clip(fitted,-7.,7.),coef.tolist()

def backward_for_model(bhat, num_quadrature=16):
    """Strong conventional baseline: fit b(x), then solve backward FK equation.

    Gaussian-Hermite integration of the E-M plant, with sigma known to both
    learning strategies, and control policy u=sigma*d_x log h.
    """
    nodes,weights=roots_hermitenorm(num_quadrature)
    weights=weights/np.sqrt(2*np.pi)
    h=np.empty((STEPS+1,len(XGRID)))
    h[-1]=np.where(XGRID>GOAL,W,1.)
    shifts=(XGRID+DT*bhat)[:,None]+SIGMA*np.sqrt(DT)*nodes[None,:]
    for j in range(STEPS-1,-1,-1):
        h[j]=sum(w*np.interp(shifts[:,k],XGRID,h[j+1],left=h[j+1,0],right=h[j+1,-1])
                 for k,w in enumerate(weights))
    grad=np.gradient(np.log(h),DX,axis=1,edge_order=2)
    return SIGMA*np.clip(grad[:-1],-UMAX/SIGMA,UMAX/SIGMA),h

def discrete_dp_for_model(bhat, n_actions=121):
    """Dynamic programming for clipped discrete-time Gaussian-shift control.

    This is a stronger fair model-based comparator: b is fitted from precisely
    the same passive trajectory records; the privileged oracle gets true b.
    Numerical limitations: finite X grid, finite U grid, Gaussian convolution.
    """
    actions=np.linspace(-UMAX,UMAX,n_actions)
    value=np.zeros((STEPS+1,len(XGRID)))
    value[-1]=(XGRID>GOAL).astype(float)
    optimal_u=np.zeros((STEPS,len(XGRID)))
    mean_grid=(XGRID[:,None]+bhat[:,None]*DT+
               SIGMA*actions[None,:]*DT)
    cost=(LAMBDA/2)*DT*actions**2
    for k in range(STEPS-1,-1,-1):
        smoothed_next=gaussian_filter1d(value[k+1],SIGMA*np.sqrt(DT)/DX,mode='nearest')
        q=np.interp(mean_grid.ravel(),XGRID,smoothed_next,
                    left=smoothed_next[0],right=smoothed_next[-1]).reshape(len(XGRID),len(actions))
        q=q-cost[None,:]
        ix=np.argmax(q,axis=1)
        optimal_u[k]=actions[ix]
        value[k]=q[np.arange(len(XGRID)),ix]
    return optimal_u,value

def interpolation_policy(ugrid):
    def policy(t,x):
        return np.interp(x,XGRID,ugrid[t],left=ugrid[t,0],right=ugrid[t,-1])
    return policy

def clipped_constant_policy(amp):
    return lambda t,x: np.full_like(x,amp)

def empirical_bernstein_lb(samples,lo,hi,fail_prob):
    # Maurer & Pontil (2009), bounded empirical-Bernstein inequality.
    n=len(samples);var=np.var(samples,ddof=1)
    ell=np.log(2/fail_prob)
    radius=np.sqrt(2*var*ell/n)+7*(hi-lo)*ell/(3*(n-1))
    return float(np.mean(samples)-radius),float(radius)

def hoeffding_lb(samples,lo,hi,fail_prob):
    n=len(samples)
    radius=(hi-lo)*np.sqrt(np.log(1/fail_prob)/(2*n))
    return float(np.mean(samples)-radius),float(radius)

def certify(passive_succ,controlled_payoffs,delta=.05):
    # Conservative union bound on one-sided marginal failures.
    d0=delta/2
    d1=delta/2
    n0=len(passive_succ)
    k=int(passive_succ.sum())
    # Clopper-Pearson exact one-sided upper binomial confidence limit.
    p_ub=1. if k==n0 else float(beta.ppf(1-d0,k+1,n0-k))
    Z_ub=1+(W-1)*p_ub
    J_ub=LAMBDA*np.log(Z_ub)
    lo=-LAMBDA/2*UMAX**2*T
    lb_bern,bern_rad=empirical_bernstein_lb(controlled_payoffs,lo,1.,d1)
    lb_hoeff,hoeff_rad=hoeffding_lb(controlled_payoffs,lo,1.,d1)
    return {'upper_optimal_J':float(J_ub),'lower_policy_J_bern':lb_bern,
            'lower_policy_J_hoeff':lb_hoeff,
            'gap_bound_bern':float(max(0,J_ub-lb_bern)),
            'gap_bound_hoeff':float(max(0,J_ub-lb_hoeff)),
            'p0_upper':p_ub,'p0_empirical':float(k/n0),
            'radii':{'bern':bern_rad,'hoeff':hoeff_rad}}

def main():
    print('Simulate training passive trajectories',flush=True)
    n_train=25000
    train=sim(n_train,SEED+1,save_path=True)
    print('Passive training p0=',train['success'].mean(),flush=True)
    h_policy,h_direct=estimate_h_direct(train['hist'])
    b_hat=estimate_drift(train['hist'])
    model_policy,h_model=backward_for_model(b_hat)
    b_poly3,poly3coef=estimate_drift_polynomial(train['hist'],degree=3)
    poly3_policy,h_poly3=backward_for_model(b_poly3)
    b_poly5,poly5coef=estimate_drift_polynomial(train['hist'],degree=5)
    poly5_policy,h_poly5=backward_for_model(b_poly5)
    oracle_policy,h_oracle=backward_for_model(hidden_physical_drift(XGRID))
    dp3_policy,dp3_value=discrete_dp_for_model(b_poly3)
    dp5_policy,dp5_value=discrete_dp_for_model(b_poly5)
    dp_oracle_policy,dp_oracle_value=discrete_dp_for_model(hidden_physical_drift(XGRID))
    print('Simulate held-out passive & policy test',flush=True)
    passive_test=sim(25000,SEED+2,save_path=False)
    # Physical controllers are applied to black-box plant. Same n=25000
    # on-policy episodes for every candidate; no baseline gets extra data.
    direct_test=sim(25000,SEED+3,policy=interpolation_policy(h_policy),save_path=False)
    model_test=sim(25000,SEED+4,policy=interpolation_policy(model_policy),save_path=False)
    poly3_test=sim(25000,SEED+7,policy=interpolation_policy(poly3_policy),save_path=False)
    poly5_test=sim(25000,SEED+8,policy=interpolation_policy(poly5_policy),save_path=False)
    oracle_test=sim(25000,SEED+9,policy=interpolation_policy(oracle_policy),save_path=False)
    dp3_test=sim(25000,SEED+10,policy=interpolation_policy(dp3_policy),save_path=False)
    dp5_test=sim(25000,SEED+11,policy=interpolation_policy(dp5_policy),save_path=False)
    dp_oracle_test=sim(25000,SEED+12,policy=interpolation_policy(dp_oracle_policy),save_path=False)
    null_test=sim(25000,SEED+5,save_path=False)
    const_test=sim(25000,SEED+6,policy=clipped_constant_policy(.8),save_path=False)
    tests={'direct_conditional':direct_test,'model_based_smooth_drift':model_test,
           'model_based_polynomial_3':poly3_test,
           'model_based_polynomial_5':poly5_test,
           'privileged_oracle_drift':oracle_test,
           'model_based_dp_poly3':dp3_test,
           'model_based_dp_poly5':dp5_test,
           'privileged_oracle_discrete_dp':dp_oracle_test,
           'no_control':null_test,'constant_u_0.8':const_test}
    result={
       'scenario':{'T':T,'dt':DT,'steps':STEPS,'sigma':SIGMA,'lambda':LAMBDA,
                   'x0':X0,'goal_gt':GOAL,'umax':UMAX,
                   'hidden_drift':'2*(x-x^3) hidden from learners',
                   'reward':'indicator(X_T > 0.5)',
                   'training_passive_episodes':n_train,
                   'heldout_passive_episodes':len(passive_test['success']),
                   'evaluation_episodes_per_candidate':25000,
                   'total_simulated_episodes':n_train+25000+25000*len(tests)},
       'reference':{'estimated_optimal_J':float(LAMBDA*np.log(np.mean(1+(W-1)*passive_test['success']))),
                    'estimated_p0':float(passive_test['success'].mean())},
       'drift_fit':{'smooth_rmse':float(np.sqrt(np.mean((b_hat[np.abs(XGRID)<1.5]-hidden_physical_drift(XGRID[np.abs(XGRID)<1.5]))**2))),
                    'polynomial3_rmse':float(np.sqrt(np.mean((b_poly3[np.abs(XGRID)<1.5]-hidden_physical_drift(XGRID[np.abs(XGRID)<1.5]))**2))),
                    'polynomial5_rmse':float(np.sqrt(np.mean((b_poly5[np.abs(XGRID)<1.5]-hidden_physical_drift(XGRID[np.abs(XGRID)<1.5]))**2))),
                    'poly3coef':poly3coef,'poly5coef':poly5coef},
       'policies':{}
    }
    for name,v in tests.items():
        result['policies'][name]={
            'empirical_J':float(v['payoff'].mean()),
            'success_frequency':float(v['success'].mean()),
            'energy_mean':float(v['energy'].mean()),
            'cost_mean':float(LAMBDA/2*v['energy'].mean()),
            'certification_95pct':certify(passive_test['success'],v['payoff'])}
        print(name, result['policies'][name],flush=True)
    with open(OUT/'results.json','w') as f:json.dump(result,f,indent=2)
    np.savez_compressed(OUT/'diagnostics.npz',xgrid=XGRID,h_direct=h_direct,
        h_model=h_model,u_direct=h_policy,u_model=model_policy,b_fitted=b_hat,
        b_actual_plot_only=hidden_physical_drift(XGRID),b_polynomial3=b_poly3,
        b_polynomial5=b_poly5,u_poly3=poly3_policy,u_poly5=poly5_policy,
        u_oracle=oracle_policy,h_poly3=h_poly3,h_poly5=h_poly5,
        u_dp3=dp3_policy,u_dp5=dp5_policy,u_dp_oracle=dp_oracle_policy,
        v_dp3=dp3_value,v_dp5=dp5_value,v_dp_oracle=dp_oracle_value)
    print('wrote results.json and diagnostics.npz')

if __name__=='__main__': main()
