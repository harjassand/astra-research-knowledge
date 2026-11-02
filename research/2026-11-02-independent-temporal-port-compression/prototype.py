#!/usr/bin/env python3
"""Independent fixed-revision Astra research: acquired passive dynamic port responses.
No internal A, B or pole data is exposed to the learner.  The synthetic physical
oracle has this information exclusively for generating scalar port measurements
and for withheld validation. All bounds are analytic, not inferred from holdout.
"""
from __future__ import annotations
import json, math, time, os
from pathlib import Path
import numpy as np
from scipy.linalg import eigh
from scipy.interpolate import BarycentricInterpolator, AAA, CubicSpline

SEED=742086
rng=np.random.default_rng(SEED)
N=180; m=24; target_r=4
T=5.0; t0=0.004; degree=22; eta=float(os.getenv("ETA", "1e-7"))

# Physical passive resistor-capacitor network: C dx/dt=-Gx+Bphys u.
# Grounded conductances and symmetric edges yield positive G; C is positive diagonal.
C=10**rng.uniform(-0.7,0.7,size=N)
G=np.diag(0.075+0.075*rng.random(N))
for i in range(N):
    j=(i+1)%N
    g=10**rng.uniform(-1,1)
    G[i,i]+=g;G[j,j]+=g;G[i,j]-=g;G[j,i]-=g
for _ in range(2*N):
    i,j=rng.choice(N,2,replace=False)
    g=10**rng.uniform(-1.5,0.7)
    G[i,i]+=g;G[j,j]+=g;G[i,j]-=g;G[j,i]-=g
A=G/np.sqrt(C[:,None]*C[None,:])
lam,E=eigh(A,check_finite=False)
assert lam[0]>0
# Four basic physically local injection patterns; each of 24 port channels is a
# distinct linear combination, with a weak independent localized component.
F=np.zeros((N,target_r))
for a in range(target_r):
    ix=(a*N//target_r+np.arange(7))%N
    F[ix,a]=rng.uniform(0.4,1.0,size=7)
F/=np.linalg.norm(F,axis=0)[None,:]
V=rng.normal(size=(target_r,m))
V/=np.linalg.norm(V,axis=0)[None,:]
Bphys=F@V
ind=np.zeros((N,m))
for j in range(m):
    ix=(j*7+3)%N
    ind[ix,j]=1
Bphys+=2e-6*ind
D=E.T@(Bphys/np.sqrt(C[:,None]))


def phi(z):
    z=np.asarray(z)
    out=np.empty_like(z,dtype=float)
    mask=np.abs(z)<1e-5
    out[mask]=1-z[mask]/2+z[mask]**2/6-z[mask]**3/24
    out[~mask]=-np.expm1(-z[~mask])/z[~mask]
    return out

def R_true(t, cols=None):
    """Forbidden to learner; used by scalar physics oracle and held-out checks."""
    if cols is None: X=D
    else:X=D[:,np.asarray(cols,dtype=int)]
    W=phi(lam*t)
    return (X*W[:,None]).T@X

experiment_times=[]

def scalar_observation(t, indices, weights, noise=True):
    """one scalar normalized step experiment q_v(t)=v^T[y_v(t)/t]."""
    experiment_times.append(float(t))
    v=np.zeros(m)
    v[list(indices)]=weights
    y=float(np.sum(phi(lam*t)*(D@v)**2))
    return y+(rng.uniform(-eta,eta) if noise else 0)

# Stage I: experimentally obtain the response Gram's diagonal at t0.
raw_count=0
diag=np.array([scalar_observation(t0,[i],[1.0]) for i in range(m)])
raw_count+=m
J=[]; sampled={}  # acquired Gram columns, only from scalar mixed-port experiments
xi=2*eta

def choose_weights():
    r=len(J)
    Z=np.zeros((r,m))
    if r:
        Chat=np.column_stack([sampled[j] for j in J])
        W=0.5*(Chat[J,:]+Chat[J,:].T)
        gamma=1e-8*max(np.trace(W)/r,1e-2)
        for i in range(m):
            if i in J:
                Z[J.index(i),i]=1.0
            else:
                Z[:,i]=np.linalg.solve(W+gamma*np.eye(r),Chat[i,:])
    else:
        W=np.empty((0,0)); Chat=np.empty((m,0))
    residuals=[]
    for i in range(m):
        if i in J:
            residuals.append(0.0)
        else:
            z=Z[:,i]
            dh=float(diag[i]-2*z@Chat[i,:]+z@W@z)
            residuals.append(max(0.0,dh+xi*(1+np.linalg.norm(z,1))**2))
    return Z,np.array(residuals)

for step in range(target_r):
    Z,res=choose_weights()
    selected=int(np.argmax(res))
    assert selected not in J
    # Pair experiments reveal the entire selected Gram column. Each (i,selected)
    # is one v=(ei+ej)/sqrt(2) scalar experiment, not a free vector readout.
    col=np.zeros(m)
    col[selected]=diag[selected]
    for i in range(m):
        if i!=selected:
            v=scalar_observation(t0,[i,selected],[1/math.sqrt(2)]*2)
            col[i]=v-(diag[i]+diag[selected])/2
            raw_count+=1
    sampled[selected]=col
    J.append(selected)
Z,res=choose_weights()
Dcert=float(res.sum())
M0=float(np.sum(diag+eta)) # measured PSD trace upper; no B bound supplied
Znorm=float(np.linalg.norm(Z,2))

# Stage II: Chebyshev sampling of time-varying r x r step responses on log blocks.
x0=math.log(t0); xT=math.log(T)
num_blocks=int(math.ceil(xT-x0))
block_edges=np.linspace(x0,xT,num_blocks+1)
model=[]
for b in range(num_blocks):
    a,c=block_edges[b:b+2]
    n=degree
    theta=(np.arange(n+1)+0.5)*math.pi/(n+1)
    xs=np.sort((a+c)/2+(c-a)/2*np.cos(theta))
    measured=[]
    for x in xs:
        t=math.exp(x)
        dd=np.array([scalar_observation(t,[j],[1]) for j in J]);raw_count+=len(J)
        RR=np.diag(dd)
        for i in range(len(J)):
            for j in range(i+1,len(J)):
                q=scalar_observation(t,[J[i],J[j]],[1/math.sqrt(2)]*2);raw_count+=1
                RR[i,j]=RR[j,i]=q-(dd[i]+dd[j])/2
        measured.append(RR)
    measured=np.array(measured)
    model.append((xs,measured,BarycentricInterpolator(xs, measured, axis=0)))

# All constants need only the acquired diagonal, a strict sensor error bound,
# degree, time endpoints and calculated Z coefficients.
C_analytic=math.exp(1/8)/math.cos(3/8)
Lambda_bound=1+(2/math.pi)*math.log(degree+1)
eta_R=4*C_analytic*M0*2.0**(-degree)+2*len(J)*Lambda_bound*eta
red_const=T*(2*math.sqrt(M0*Dcert)+Dcert)
interp_const=Znorm**2*max(T*eta_R,M0*t0)
Delta=red_const+interp_const

def approx_S(t):
    if t<=0:return np.zeros((m,m))
    if t<t0:return np.zeros((m,m))
    xx=math.log(t)
    i=min(num_blocks-1,max(0,int(np.searchsorted(block_edges,xx,side='right')-1)))
    Rr=model[i][2](xx)
    return t*(Z.T@Rr@Z)

def true_S(t):
    return t*R_true(t) if t>0 else np.zeros((m,m))

# Withheld diagnostic: global step-response bound and pulse predictions.
times=np.linspace(0,T,221)
error_steps=[];err_spatial=[];err_log=[]
for t in times:
    P=approx_S(t);S=true_S(t)
    error_steps.append(float(np.linalg.norm(S-P,2)))
    St=t*R_true(t,J) if t>0 else np.zeros((len(J),len(J)))
    Sp=Z.T@St@Z
    err_spatial.append(float(np.linalg.norm(S-Sp,2)))
    err_log.append(float(np.linalg.norm(Sp-P,2)))

jumps=[(0.0,rng.normal(size=m)/math.sqrt(m)),
       (0.9,rng.normal(size=m)/math.sqrt(m)),
       (2.1,rng.normal(size=m)/math.sqrt(m)),
       (3.35,rng.normal(size=m)/math.sqrt(m))]
Vbudget=sum(np.linalg.norm(v) for _,v in jumps)
errors=[]; signal=[]
for t in times:
    yt=np.zeros(m); yp=np.zeros(m)
    for tj,v in jumps:
        if tj<=t:
            yt+=true_S(t-tj)@v
            yp+=approx_S(t-tj)@v
    errors.append(float(np.linalg.norm(yt-yp)))
    signal.append(float(np.linalg.norm(yt)))

# Strong established alternative: ordinary AAA rational approximation of the
# same acquired r-by-r matrix curves on log t (no additional experiments).
# It is not certified passive, and no claim is made that this baseline is optimal.
all_x=np.concatenate([s[0] for s in model]); all_R=np.concatenate([s[1] for s in model]);
aaamodel={}; aaawarn=[]
for i in range(len(J)):
    for j in range(i,len(J)):
        try:
            ap=AAA(all_x,all_R[:,i,j],rtol=1e-9)
            aaamodel[(i,j)]=ap
        except Exception as e: aaawarn.append(str(e))

def aaa_S(t):
    if t<=0:return np.zeros((m,m))
    if t<t0:return np.zeros((m,m))
    logt=math.log(t)
    RR=np.zeros((len(J),len(J)))
    for (i,j),f in aaamodel.items():
        RR[i,j]=RR[j,i]=float(f(logt).real)
    return t*Z.T@RR@Z

# Strong ordinary smooth-response interpolation comparator, also from the SAME
# exact acquired port/time readings. It does not carry a model-class-robust bound.
cs_model=CubicSpline(all_x,all_R,axis=0)
def spline_S(t):
    if t<=0 or t<t0:return np.zeros((m,m))
    Rr=cs_model(math.log(t))
    return t*(Z.T@Rr@Z)
spline_max=max(float(np.linalg.norm(true_S(t)-spline_S(t),2)) for t in times)

if len(aaamodel)==len(J)*(len(J)+1)//2:
    aaa_err=[]
    for t in times:
        aaa_err.append(float(np.linalg.norm(true_S(t)-aaa_S(t),2)))
    aaa_max=float(max(aaa_err))
else:aaa_max=None

# A genuinely novel future decision (not among training experiments): rank two
# unseen current-pulse schedules by a terminal observable. Learned decisions use
# the full 24-port response and no source remeasurement.
v1=rng.uniform(0,1,size=m);v1/=np.linalg.norm(v1)
v2=rng.uniform(0,1,size=m);v2/=np.linalg.norm(v2)
obs=rng.normal(size=m);obs/=np.linalg.norm(obs)
schedules=[[(0.0,v1),(1.2,-v1)],[(2.5,v2),(3.7,-v2)]]
# pick terminal objective so two schedules are measurably different (avoid cherry pick by using both)
terminal_true=[]; terminal_hat=[]
for schedule in schedules:
    terminal_true.append(float(sum(obs@true_S(T-tj)@dv for tj,dv in schedule)))
    terminal_hat.append(float(sum(obs@approx_S(T-tj)@dv for tj,dv in schedule)))
choice_true=int(np.argmax(terminal_true)); choice_hat=int(np.argmax(terminal_hat))

# verify actual measured acquisition residuals for diagnostic only
R0=R_true(t0)
Q=np.eye(m);Q[J,:]-=Z
true_res=np.array([Q[:,i]@R0@Q[:,i] for i in range(m)])
assert np.all(true_res<=res+2e-11), (max(true_res-res))
assert max(error_steps)<=Delta+1e-8

result={
 "seed":SEED,"internal_states":N,"ports":m,"selected_ports":J,
 "rate_range":[float(lam.min()),float(lam.max())],
 "t0":t0,"T":T,"degree":degree,"number_log_panels":num_blocks,
 "physical_scalar_experiment_settings":raw_count,"dense_full_port_settings_comparator": int((m*(m+1)/2)*(degree+1)*num_blocks),
 "scalar_report_normalized_error_bound":eta,
 "total_experimental_run_time_excluding_reset":float(sum(experiment_times)),
 "earliest_raw_step_output_error_required":float(eta*min(experiment_times)),
 "M0_psd_trace_bound":M0,"Dcert_noisy_residual_trace_bound":Dcert,
 "true_residual_trace_diagnostic":float(true_res.sum()),
 "Z_operator_norm":Znorm,"uniform_log_interpolation_bound_matrix":eta_R,
 "certified_port_reduction_bound":red_const,
 "certified_time_interpolation_and_unobserved_early_bound":interp_const,
 "certified_step_kernel_uniform_operator_error":Delta,
 "observed_withheld_max_step_error":max(error_steps),
 "observed_withheld_max_spatial_error":max(err_spatial),
 "observed_withheld_max_time_interpolation_error":max(err_log),
 "AAA_same_data_max_step_error":aaa_max,
 "cubic_spline_same_data_max_step_error":spline_max,
 "AAA_fit_warnings":aaawarn[:5],
 "pulse_total_variation":float(Vbudget),
 "certified_future_pulse_output_error_bound":float(Vbudget*Delta),
 "observed_withheld_max_pulse_output_error":max(errors),
 "max_true_pulse_output_norm":max(signal),
 "future_terminal_choices":{"true_returns":terminal_true,"predicted_returns":terminal_hat,"oracle_best":choice_true,"learned_best":choice_hat,"regret":max(terminal_true)-terminal_true[choice_hat],"bound_2VDelta":2*sum(np.linalg.norm(dv) for sc in schedules for _,dv in sc)*Delta}
}
Path(__file__).with_name('results.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))

# Stage III: a task-specific certificate.  For any tau>=t0, S(tau)<=tau R(t0)
# in PSD order. Minkowski on the *observed* R0 residuals gives a much sharper
# source-safe scalar bound than a global (all-protocol) operator radius.
Chat=np.column_stack([sampled[j] for j in J])
What=0.5*(Chat[J,:]+Chat[J,:].T)

def source_energy_bound(v):
    zv=Z@v
    return max(0.0,float(zv@What@zv)+xi*np.linalg.norm(zv,1)**2)

def task_error_bound(tau, w, v):
    if tau<t0:
        # Conservative unobserved short-lag bound using acquired R0 energies.
        ew=sum(abs(w)*np.sqrt(res)); ev=sum(abs(v)*np.sqrt(res))
        aw=math.sqrt(source_energy_bound(w)); av=math.sqrt(source_energy_bound(v))
        return t0*(aw+ew)*(av+ev)
    ew=sum(abs(w)*np.sqrt(res)); ev=sum(abs(v)*np.sqrt(res))
    aw=math.sqrt(source_energy_bound(w)); av=math.sqrt(source_energy_bound(v))
    port=tau*(aw*ev+av*ew+ew*ev)
    temporal=tau*eta_R*np.linalg.norm(Z@w)*np.linalg.norm(Z@v)
    return port+temporal

cert_radii=[]
for schedule in schedules:
    cert_radii.append(sum(task_error_bound(T-tj,obs,dv) for tj,dv in schedule))
regret_pair_upper=terminal_hat[1-choice_hat]+cert_radii[1-choice_hat]-(terminal_hat[choice_hat]-cert_radii[choice_hat])
# positive => cannot distinguish; negative => certified best.
res3={"radii":cert_radii,"predicted_returns":terminal_hat,
      "source_safe_best_action_certified":bool(regret_pair_upper<0),
      "worst_alt_upper_minus_chosen_lower":float(regret_pair_upper),
      "true_best_action":choice_true,"learned_choice":choice_hat}
result['task_specific_certificate']=res3
Path(__file__).with_name('results.json').write_text(json.dumps(result,indent=2))
print('TASK_SPECIFIC_CERTIFICATE',json.dumps(res3,indent=2))

# A 24-way future allocation at a held-out target port; every candidate consumes
# the same rectangular unit-current charge for one time unit. All predictions,
# bounds and physical port choices use only frozen acquisition data.
target_port=7; goal=np.eye(m)[target_port]
scores=[]; intervals=[]; truths=[]
for i in range(m):
    curr=np.eye(m)[i]
    schedule=[(3.5,curr),(4.5,-curr)]
    score=float(sum(goal@approx_S(T-tj)@dv for tj,dv in schedule))
    rad=sum(task_error_bound(T-tj,goal,dv) for tj,dv in schedule)
    true=float(sum(goal@true_S(T-tj)@dv for tj,dv in schedule))
    scores.append(score); intervals.append([score-rad,score+rad]); truths.append(true)
chosen=int(np.argmax(scores))
other_upper=max(intervals[i][1] for i in range(m) if i!=chosen)
allocation={
  "target_port":target_port,"menu_size":m,"candidate_pulse_interval":[3.5,4.5],
  "selected_actuator":chosen,"true_best_actuator":int(np.argmax(truths)),
  "chosen_true_reward":truths[chosen],"true_optimum_reward":max(truths),
  "chosen_certificate_lower":intervals[chosen][0],
  "best_competitor_certificate_upper":other_upper,
  "certified_unique_winner":bool(intervals[chosen][0]>other_upper),
  "certified_regret_max":float(max(0,other_upper-intervals[chosen][0]))
}
result["unseen_24_action_allocation"]=allocation
Path(__file__).with_name('results.json').write_text(json.dumps(result,indent=2))
print('ALLOCATION',json.dumps(allocation,indent=2))

# Acquired-source reuse with a changed hardware price selected after all physical
# measurements are frozen. The same 24 unit-dose, one-unit-duration policies.
# Port 7 has an independently specified 0.1 charge in reward units.
pricing={"port_7_price":0.1,"other_port_prices":0.0}
priced_scores=[];priced_truth=[];priced_intervals=[]
for i in range(m):
    price=pricing['port_7_price'] if i==7 else 0.0
    curr=np.eye(m)[i]
    schedule=[(3.5,curr),(4.5,-curr)]
    score=float(sum(goal@approx_S(T-tj)@dv for tj,dv in schedule))-price
    rad=sum(task_error_bound(T-tj,goal,dv) for tj,dv in schedule)
    truth=float(sum(goal@true_S(T-tj)@dv for tj,dv in schedule))-price
    priced_scores.append(score);priced_intervals.append((score-rad,score+rad));priced_truth.append(truth)
chosen2=int(np.argmax(priced_scores))
competitor=max((priced_intervals[i][1],i) for i in range(m) if i!=chosen2)
priced_decision={
  "decision_selected_after_source_record_frozen":True,
  "prices":pricing,"selected_actuator":chosen2,
  "oracle_best_actuator":int(np.argmax(priced_truth)),
  "selected_predicted_value":priced_scores[chosen2],
  "selected_true_value":priced_truth[chosen2],
  "selected_certified_lower":priced_intervals[chosen2][0],
  "strongest_competitor":competitor[1],
  "strongest_competitor_certified_upper":competitor[0],
  "positive_certificate_gap":priced_intervals[chosen2][0]-competitor[0],
  "is_certified_best":bool(priced_intervals[chosen2][0]>competitor[0]),
  "new_source_measurements":0
}
# Because the physical response and the known prices are linear in the actuator
# mixture, every fractional v>=0, sum(v)<=1 has a convex-combination reward
# of the 24 unit vertices and the zero action. Strict vertex separation hence
# certifies a unique global optimum over the FULL CONTINUOUS simplex.
priced_decision["certificate_over_continuous_allocation_simplex"]=bool(
    priced_decision["is_certified_best"] and priced_intervals[chosen2][0]>0)
priced_decision["policy_class"]="nonnegative 24-port mixtures with sum <= 1 at fixed rectangular pulse [3.5,4.5]"
result["priced_unseen_24_action_decision"]=priced_decision
Path(__file__).with_name('results.json').write_text(json.dumps(result,indent=2))
print('PRICED_DECISION',json.dumps(priced_decision,indent=2))

# Check that every alternative's true response falls inside its certificate,
# not merely that the selected action happened to be best in the simulation.
for true, (lower,upper) in zip(priced_truth,priced_intervals):
    assert lower-1e-9<=true<=upper+1e-9
result['ordinary_rough_comparators']={
    'adaptive_Nystrom_plus_Chebyshev_experiments':raw_count,
    'adaptive_Nystrom_plus_spline_same_experiments':raw_count,
    'adaptive_Nystrom_plus_AAA_same_experiments':raw_count,
    'same_spline_menu_best':int(np.argmax([sum(goal@spline_S(T-tj)@dv for tj,dv in [(3.5,np.eye(m)[i]),(4.5,-np.eye(m)[i])])-(pricing['port_7_price'] if i==7 else 0.0) for i in range(m)])),
    'same_AAA_menu_best':int(np.argmax([sum(goal@aaa_S(T-tj)@dv for tj,dv in [(3.5,np.eye(m)[i]),(4.5,-np.eye(m)[i])])-(pricing['port_7_price'] if i==7 else 0.0) for i in range(m)]))
}
Path(__file__).with_name('results.json').write_text(json.dumps(result,indent=2))