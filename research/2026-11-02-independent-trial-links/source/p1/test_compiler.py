#!/usr/bin/env python3
"""Independent research test: event-before-expiration from native local excursions.

All data are synthetic. No physical calibration, molecular simulation, or claim
of historical novelty. Standard numerical comparison has same supplied rates.
"""
import itertools, json, math
import numpy as np
from scipy.linalg import solve
from scipy.stats import beta

SEED=20261102
N=40
MU=0.30
M=20000
DELTA=0.01
rng=np.random.default_rng(SEED)
i=np.arange(N,dtype=float)
a=0.55+0.65*(0.5+0.5*np.sin(0.47*i+0.4))
t=0.65+0.65*(0.5+0.5*np.cos(0.39*i+0.3))
gamma=0.35+0.7*(0.5+0.5*np.sin(0.33*i+0.9))
d=0.10+0.18*np.sin(0.21*i+1.0)**2
d[0]=0.
h=gamma/(gamma+MU)


def compiled_kernel(a, h):
    """Boundary renewal kernel P, target vector b; interval trap return law h."""
    n=len(a)
    D=a+d+t+MU
    P=np.zeros((n,n),float)
    b=np.zeros(n,float)
    for k in range(n):
        P[k,k]+=t[k]*h[k]/D[k]
        if k+1<n:
            P[k,k+1]+=a[k]/D[k]
        else:
            b[k]=a[k]/D[k]
        if k>0:
            P[k,0]+=d[k]/D[k]
    return P,b


def solve_compiler(a, h):
    P,b=compiled_kernel(a,h)
    return solve(np.eye(N)-P,b,assume_a='gen',check_finite=False)


def solve_finite_generator(a):
    """Full model, all 40 native stage states + 40 hidden trap states.

    M=mu I-Q_UU; b=Q_U,product. Finite killed generator is not accessible to
    the learner, only the comparator.
    """
    size=2*N
    A=np.zeros((size,size),float)
    b=np.zeros(size,float)
    for k in range(N):
        rate=a[k]+d[k]+t[k]+MU
        A[k,k]=rate
        if k+1<N: A[k,k+1]-=a[k]
        else: b[k]+=a[k]
        if k>0: A[k,0]-=d[k]
        A[k,N+k]-=t[k]
        A[N+k,N+k]=gamma[k]+MU
        A[N+k,k]-=gamma[k]
    return solve(A,b,assume_a='gen',check_finite=False)


def rapid_yield(a,h):
    """Independent O(N) algebraic conventional baseline for same *stage* structure."""
    den=a+d+t+MU-t*h
    Ac=1.0
    Bc=0.0
    # u_i = Ac_i + Bc_i*u_0. Terminal exit to product has A=a_last/den.
    for k in range(N-1,-1,-1):
        if k==N-1:
            Ac=a[k]/den[k]
            Bc=d[k]/den[k]
        else:
            Ac=a[k]*Ac/den[k]
            Bc=(a[k]*Bc+d[k])/den[k]
    return Ac/(1-Bc)


# Native local experiment: prepare gateway T_i, run until its return to S_i
# or independent chemical death Exp(MU). The sufficient count is binomial.
# Time exposure is simulated separately, to charge actual local physical time.
k=rng.binomial(M,h)
exposure=sum(float(np.sum(rng.exponential(scale=1/(gamma[v]+MU),size=M))) for v in range(N))
h_hat=k/M
alpha=DELTA/(2*N)
h_lo=np.array([beta.ppf(alpha,int(kk),M-int(kk)+1) if kk else 0 for kk in k])
h_hi=np.array([beta.ppf(1-alpha,int(kk)+1,M-int(kk)) if kk<M else 1 for kk in k])
assert np.all(h_lo<=h) and np.all(h<=h_hi), 'This seeded run must satisfy its simultaneous confidence event'

p_true=solve_compiler(a,h)
p_hat=solve_compiler(a,h_hat)
p_lo=solve_compiler(a,h_lo)
p_hi=solve_compiler(a,h_hi)
p_full=solve_finite_generator(a)
p_standard=rapid_yield(a,h)
assert np.all(p_lo<=p_true*(1+1e-12)) and np.all(p_true<=p_hi*(1+1e-12))
assert np.allclose(p_true,p_full[:N],rtol=1e-11,atol=1e-60)
assert np.isclose(p_true[0],p_standard,rtol=1e-11)

# Boundary-only intervention: double exactly two forward rates, all other
# rates untouched, including unseen hidden trap kinetics.
options=[]
for v,w in itertools.combinations(range(N),2):
    anew=a.copy();anew[v]*=2;anew[w]*=2
    zlo=rapid_yield(anew,h_lo)
    zhi=rapid_yield(anew,h_hi)
    ztrue=rapid_yield(anew,h)
    options.append((zlo,zhi,ztrue,v,w))
selected=max(options,key=lambda z:z[0])
optimal=max(options,key=lambda z:z[2])
max_U=max(o[1] for o in options)
R=max_U/selected[0]
assert selected[2] <= optimal[2]*(1+1e-12)
assert selected[2]+1e-40 >= optimal[2]/R

# Doob transform of measured Markov renewal chain gives successful skeletons.
P,b=compiled_kernel(a,h)
Kstar=P*p_true[None,:]/p_true[:,None]
bstar=b/p_true
assert np.max(abs(np.sum(Kstar,axis=1)+bstar-1)) <1e-12
counts=[]
for trial in range(1000):
    s=0
    for tick in range(200000):
        weights=np.append(Kstar[s],bstar[s])
        nxt=rng.choice(N+1,p=weights/weights.sum())
        if nxt==N:
            counts.append(tick+1);break
        s=nxt
    else: raise AssertionError('conditioned path exceeded bound')

# Falsifiers: (i) hidden memory across stages; (ii) unseen direct shortcut.
eta=1.0
correlated=0.5*(np.exp(-2*eta)+np.exp(-6*eta))
anticorrelated=np.exp(-4*eta)
shortcut=1e-7
# exact change from new direct S0->product rate shortcut in full generator:
new_a=a.copy()
# Cannot treat shortcut as merely forward rate: add direct b_0 and denominator.
P0,b0=compiled_kernel(a,h)
D0=a[0]+d[0]+t[0]+MU
P0[0,:]*=D0/(D0+shortcut)
b0[0]+=shortcut/(D0+shortcut)
p_short=solve(np.eye(N)-P0,b0,assume_a='gen',check_finite=False)[0]

res={
'git_source_revision':'5489b118101275c81500d823361592c670ec77bb',
'synthetic_seed':SEED,'n_stages':N,'n_hidden_traps':N,'independent_death_rate':MU,
'gateway_experiments_per_stage':M,'total_gateway_experiments':N*M,
'physical_time_units_in_gateway_experiments':exposure,
'expected_gateway_time_if_rates_known':float(M*np.sum(1/(gamma+MU))),
'confidence_level':1-DELTA,
'all_true_h_inside_CP_intervals':True,
'baseline_true_probability':float(p_true[0]),
'baseline_full_generator_probability':float(p_full[0]),
'baseline_conventional_O_N_probability':float(p_standard),
'baseline_learned_probability':float(p_hat[0]),
'baseline_confidence_low':float(p_lo[0]),
'baseline_confidence_high':float(p_hi[0]),
'baseline_relative_interval_high_over_low':float(p_hi[0]/p_lo[0]),
'candidate_designs_2_of_40':len(options),
'selected_worstcase_two_stages':[int(selected[3]),int(selected[4])],
'selected_true_probability':float(selected[2]),
'selected_confidence_low':float(selected[0]),
'selected_confidence_high':float(selected[1]),
'selected_true_improvement':float(selected[2]/p_true[0]),
'actual_optimal_two_stages':[int(optimal[3]),int(optimal[4])],
'actual_optimal_probability':float(optimal[2]),
'actual_selected_over_optimal':float(selected[2]/optimal[2]),
'certified_selected_over_optimal_lower_bound':float(1/R),
'doob_sample_paths':len(counts),'doob_mean_steps':float(np.mean(counts)),
'doob_max_steps':max(counts),
'direct_monte_carlo_mean_runs_per_success':float(1/p_true[0]),
'correlated_two_stage_duration_laplace':float(correlated),
'anticorrelated_two_stage_duration_laplace':float(anticorrelated),
'correlated_over_anticorrelated':float(correlated/anticorrelated),
'unseen_shortcut_rate':shortcut,
'probability_with_shortcut':float(p_short),
'shortcut_over_no_shortcut':float(p_short/p_true[0]),
'per_stage_gateway_successes':[int(x) for x in k],
'per_stage_true_gateway_discounted':[float(x) for x in h],
'per_stage_lower':[float(x) for x in h_lo],
'per_stage_upper':[float(x) for x in h_hi]
}
with open('producer-workspace/results.json','w') as f:json.dump(res,f,indent=2)
for kk,v in res.items():
    if kk.startswith('per_stage_'):continue
    print(kk,':',v)
