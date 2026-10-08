#!/usr/bin/env python3
"""Exact finite-state audit of CLE-matched, pulse-order-observable hidden memory.

States for the observable reduction are (H,P) in Z_3 x Z_2. Column generators
use Q[destination,source]. X is a four-species count vector in N^4 and P is
sum_i X_i mod 2. A/B pulses have Poisson burst events at rate lambda=2r; their
mask stoichiometries have identical jump moments through order 3 at every x,h,
but differ at the fourth-order joint inclusion.
"""
from __future__ import annotations
import itertools, json, math
from pathlib import Path
import numpy as np


def expm(A: np.ndarray) -> np.ndarray:
    """NumPy-only scaling/squaring Taylor exponential for tiny matrices."""
    A = np.asarray(A, float)
    norm1 = float(np.linalg.norm(A, 1))
    s = max(0, int(math.ceil(math.log2(norm1 / 0.5)))) if norm1 > 0.5 else 0
    X = A / (2**s)
    term = np.eye(A.shape[0]); total = term.copy()
    for k in range(1, 300):
        term = term @ X / k
        total += term
        if np.linalg.norm(term, 1) <= 2e-16 * max(1., np.linalg.norm(total, 1)):
            break
    else:
        raise ArithmeticError('Taylor exponential did not converge')
    for _ in range(s): total = total @ total
    return total



def uniformization(Q: np.ndarray, t: float, tol: float=1e-15) -> np.ndarray:
    """Independent CTMC exponential check via Poisson uniformization."""
    Q=np.asarray(Q,float); nu=float(max(-np.diag(Q)))
    if nu==0 or t==0: return np.eye(Q.shape[0])
    mu=nu*t; R=np.eye(Q.shape[0])+Q/nu
    w=math.exp(-mu); power=np.eye(Q.shape[0]); total=w*power; cdf=w; k=0
    while True:
        next_w=w*mu/(k+1)
        # Geometric upper bound on the remaining Poisson mass.
        ratio=mu/(k+2)
        tail_bound=next_w/(1-ratio) if ratio<1 else math.inf
        if tail_bound<tol: break
        k+=1; w=next_w; power=power@R; total+=w*power; cdf+=w
        if k>10000: raise ArithmeticError('uniformization failed to converge')
    return total

def idx(h: int, p: int) -> int: return 2*(h % 3) + (p % 2)


def generator(kappa: float, r: float, active_h: int | None) -> np.ndarray:
    """H clockwise cycle at kappa; parity toggles at r in active_h only."""
    Q = np.zeros((6,6), float)
    for h in range(3):
        for p in range(2):
            s = idx(h,p)
            d = idx((h+1)%3,p)
            Q[d,s] += kappa; Q[s,s] -= kappa
            if active_h == h:
                d = idx(h,1-p)
                Q[d,s] += r; Q[s,s] -= r
    return Q


def endpoint_law(order: str, tau: float, kappa: float, r: float,
                 model: str, gap: float=0.) -> np.ndarray:
    """2x2 law of (P after first, P after second) from P0=0, H0~Unif."""
    active = {'plus': {'A':0,'B':0}, 'minus': {'A':0,'B':2}}[model]
    mu = np.zeros(6); mu[[idx(h,0) for h in range(3)]] = 1/3
    first, second = order
    K1 = expm(generator(kappa,r,active[first])*tau)
    K0 = expm(generator(kappa,0.,None)*gap) if gap else np.eye(6)
    K2 = expm(generator(kappa,r,active[second])*tau)
    D = []
    for p in range(2):
        Dp = np.zeros((6,6))
        for h in range(3): Dp[idx(h,p),idx(h,p)] = 1.
        D.append(Dp)
    out = np.zeros((2,2))
    z = K1 @ mu
    for p1 in range(2):
        mid = K2 @ K0 @ D[p1] @ z
        for p2 in range(2): out[p1,p2] = np.sum(D[p2] @ mid)
    return out


def increment_law_from_endpoints(E: np.ndarray) -> np.ndarray:
    """J[u,v], where u=P1 xor P0=P1 and v=P2 xor P1."""
    J = np.zeros((2,2))
    for u in range(2):
        for v in range(2): J[u,v] = E[u,u^v]
    return J


def noisy_endpoint_law(E: np.ndarray, eps: float) -> np.ndarray:
    """Distribution of two independent noisy parity snapshots (Y1,Y2)."""
    Y = np.zeros((2,2))
    for p1,p2,y1,y2 in itertools.product(range(2), repeat=4):
        e1 = (1-eps) if y1==p1 else eps
        e2 = (1-eps) if y2==p2 else eps
        Y[y1,y2] += E[p1,p2]*e1*e2
    return Y


def tv(P: np.ndarray, Q: np.ndarray) -> float:
    return float(.5*np.abs(P-Q).sum())


def bernoulli_kl(p: float, q: float) -> float:
    p=min(max(p,1e-300),1-1e-16); q=min(max(q,1e-300),1-1e-16)
    return p*math.log(p/q)+(1-p)*math.log((1-p)/(1-q))


def mask_moment_audit() -> dict:
    masks = list(itertools.product((0,1), repeat=4))
    ind = masks
    even = [m for m in masks if sum(m)%2==0]
    def inclusion(kernel, subset): return sum(all(m[i] for i in subset) for m in kernel)/len(kernel)
    checks = {}
    for k in range(4):
        vals_i=[]; vals_e=[]
        for subset in itertools.combinations(range(4),k):
            vals_i.append(inclusion(ind,subset)); vals_e.append(inclusion(even,subset))
        checks[str(k)] = {'ind_values': sorted(set(vals_i)), 'even_values':sorted(set(vals_e)), 'equal': all(a==b for a,b in zip(vals_i,vals_e))}
    return checks


def main() -> None:
    # Exact laws, both pulse orders, a finite grid in unknown switching rate.
    tau=0.38; r=1.0; eps=0.08
    ks=[0.,.05,.1,.2,.4,.8,1.5,3.,6.]
    rows=[]
    for k in ks:
        for order in ['AB','BA']:
            Em=endpoint_law(order,tau,k,r,'minus')
            Ep=endpoint_law(order,tau,k,r,'plus')
            Jm=increment_law_from_endpoints(Em); Jp=increment_law_from_endpoints(Ep)
            Ym=noisy_endpoint_law(Em,eps); Yp=noisy_endpoint_law(Ep,eps)
            rows.append({'kappa':k,'order':order,'J_plus':Jp.tolist(),'J_minus':Jm.tolist(),
                         'latent_J11_gap':float(Jp[1,1]-Jm[1,1]),
                         'endpoint_TV_noiseless':tv(Em,Ep),'endpoint_TV_noisy':tv(Ym,Yp),
                         'both_observed_increment_event_gap':float(Yp[1,0]-Ym[1,0])})
    # Continuous-parameter certificate on the unknown hidden switching rate κ∈[0,3].
    # Each noisy event probability is 4*tau-Lipschitz in κ: Duhamel gives
    # ||d exp(tQκ)/dκ||_1 <= 2t, and there are two pulse kernels.
    cert_h=1e-4
    cert_ks=np.linspace(0.,3.,int(round(3./cert_h))+1)
    cert_p={name:[] for name in ['plus','minus']}
    for k in cert_ks:
        for name in cert_p:
            E=endpoint_law('AB',tau,float(k),r,name)
            cert_p[name].append(float(noisy_endpoint_law(E,eps)[1,0]))
    Lk=4*tau
    min_plus_grid=min(cert_p['plus']); argmin_plus=cert_ks[int(np.argmin(cert_p['plus']))]
    max_minus_grid=max(cert_p['minus']); argmax_minus=cert_ks[int(np.argmax(cert_p['minus']))]
    plus_lower=min_plus_grid-Lk*cert_h/2
    minus_upper=max_minus_grid+Lk*cert_h/2
    certified_gap=plus_lower-minus_upper
    delta=.05
    n_hoeffding=math.ceil(2*math.log(1/delta)/(certified_gap**2))
    # Debit bounded pulse-timing, pulse-rate, and reporter-calibration error.
    eta_tau=1e-5; eta_r=1e-4; eta_eps=1e-4
    rmax=r+eta_r; taumax=tau+eta_tau
    nuisance_debit=2*(3.+rmax)*(2*eta_tau)+2*taumax*(2*eta_r)+2*eta_eps
    robust_gap=certified_gap-2*nuisance_debit
    robust_threshold=(plus_lower+minus_upper)/2
    n_robust=math.ceil(2*math.log(1/delta)/(robust_gap**2))
    cert={'kappa_interval':[0.,3.],'grid_step':cert_h,'grid_points':len(cert_ks),
      'per_model_lipschitz_bound_in_kappa':Lk,'plus_min_grid':min_plus_grid,'plus_argmin_grid':float(argmin_plus),
      'plus_continuous_lower_bound_nominal':plus_lower,'minus_max_grid':max_minus_grid,
      'minus_argmax_grid':float(argmax_minus),'minus_continuous_upper_bound_nominal':minus_upper,
      'nominal_continuous_range_gap_lower_bound':certified_gap,'nominal_threshold_midpoint':(plus_lower+minus_upper)/2,
      'bounded_control_and_reporter_uncertainty':{'duration_abs_each':eta_tau,'r_abs_each_action':eta_r,'epsilon_abs':eta_eps,
        'per_model_probability_debit':nuisance_debit,'robust_plus_lower':plus_lower-nuisance_debit,
        'robust_minus_upper':minus_upper+nuisance_debit,'robust_gap_lower_bound':robust_gap,
        'robust_threshold_midpoint':robust_threshold},
      'nominal_one_sided_hoeffding_n_for_delta_0_05':n_hoeffding,
      'robust_one_sided_hoeffding_n_for_delta_0_05':n_robust,
      'n_suffices_for_each_unknown_mechanism':'ceil(2 log(1/delta)/gap^2) independent AB wells; one binary event per well; robust_n includes the stated actuation and reporter uncertainty debits'}
    # Fixed-sample synthetic Bernoulli acquisitions at an interior unknown rate.
    synthetic_n=n_robust
    synthetic_threshold=robust_threshold
    synthetic_runs=[]
    for model,seed in [('plus',20261008),('minus',20261008)]:
        pz=float(noisy_endpoint_law(endpoint_law('AB',tau,1.,r,model),eps)[1,0])
        count=int(np.random.default_rng(seed).binomial(synthetic_n,pz))
        synthetic_runs.append({'true_model':model,'kappa':1.,'seed':seed,'wells':synthetic_n,
          'event_probability':pz,'event_count':count,'observed_frequency':count/synthetic_n,
          'threshold':synthetic_threshold,'decision':'plus' if count/synthetic_n>synthetic_threshold else 'minus'})
    finite_cost_ledger={'independent_wells_per_classifier':synthetic_n,'nominal_wells_without_control_uncertainty':n_hoeffding,
      'A_pulses':synthetic_n,'B_pulses':synthetic_n,'endpoint_snapshots':2*synthetic_n,
      'commanded_duration_each':tau,'actual_duration_abs_tolerance_each':eta_tau,
      'nominal_command_rate_each':2*r,'rate_abs_tolerance_parameter_r_each':eta_r,'epsilon_abs_tolerance':eta_eps,
      'worst_case_event_opportunities_per_action_per_well':2*rmax*taumax,
      'worst_case_total_event_opportunities_expected_per_well':4*rmax*taumax,
      'worst_case_total_event_opportunities_expected_across_wells':synthetic_n*4*rmax*taumax,
      'symbolic_total_cost':'N*(c_culture+c_verified_start+2*c_snapshot+lambda_max*(tauA_max+tauB_max)*c_dose_per_event+c_handling)+C_reporter_calibration+C_actuation_calibration'}
    fast_tv=[]
    for k in [3.,6.,10.,30.,100.]:
        Yp=noisy_endpoint_law(endpoint_law('AB',tau,k,r,'plus'),eps)
        Ym=noisy_endpoint_law(endpoint_law('AB',tau,k,r,'minus'),eps)
        fast_tv.append({'kappa':k,'observable_TV':tv(Yp,Ym)})
    # κ=0 closed form test and pulse-order symmetry test.
    q=(1-math.exp(-2*r*tau))/2
    kp0=endpoint_law('AB',tau,0.,r,'plus')
    km0=endpoint_law('AB',tau,0.,r,'minus')
    assert abs(increment_law_from_endpoints(kp0)[1,1]-q*q/3)<1e-13
    assert abs(increment_law_from_endpoints(km0)[1,1])<1e-13
    # Independent uniformization check for all pulse kernels used in the certificate.
    uniformization_checks=[]
    for k in [0.,.4,3.]:
        for model in ['plus','minus']:
            active={'plus':{'A':0,'B':0},'minus':{'A':0,'B':2}}[model]
            for action in ['A','B']:
                Q=generator(k,r,active[action])
                err=float(np.max(np.abs(expm(Q*tau)-uniformization(Q,tau))))
                uniformization_checks.append({'kappa':k,'model':model,'action':action,'sup_error':err})
    # Same single-action law and same-action words are exactly aliased after hiding H.
    same_word_checks=[]
    for k in [0.,.1,.4,1.,3.]:
        for word in ['AA','BB']:
            a=endpoint_law(word,tau,k,r,'plus'); b=endpoint_law(word,tau,k,r,'minus')
            same_word_checks.append({'kappa':k,'word':word,'sup_error':float(np.max(np.abs(a-b)))})
    # At all k, plus is invariant to reversing the equal-duration pulse order.
    sym=[]
    for k in ks:
        a=endpoint_law('AB',tau,k,r,'plus'); b=endpoint_law('BA',tau,k,r,'plus')
        sym.append(float(np.max(np.abs(a-b))))
    # For strict observable equivalence of all one-letter laws, compare
    # endpoint distribution under A vs B for each model (uniform hidden phase).
    solo={}
    for model in ['plus','minus']:
        active={'plus':{'A':0,'B':0},'minus':{'A':0,'B':2}}[model]
        for action in ['A','B']:
            mu=np.zeros(6); mu[[idx(h,0) for h in range(3)]]=1/3
            K=expm(generator(.37,r,active[action])*tau)
            p=K@mu
            solo[(model,action)]=[sum(p[idx(h,z)] for h in range(3)) for z in range(2)]
    # equality A-only and B-only across models is exact at the parity-marginal level;
    # with hidden H observed it is false, hence H is explicitly unobserved.
    solo_gaps={a:abs(solo[('plus',a)][1]-solo[('minus',a)][1]) for a in ['A','B']}
    result={'model':'4 binary markers X, hidden H in Z3, observed parity only',
      'parameters':{'tau_each_pulse':tau,'r':r,'lambda':2*r,'snapshot_error_epsilon':eps,'kappa_grid':ks},
      'definitions':{'initial_H':'uniform on 0,1,2','initial_X':'(0,0,0,0) in N^4; each event adds its mask stoichiometry','P':'sum_i X_i mod 2','U':'P after first pulse xor P before first pulse','V':'P after second pulse xor P before second pulse'},
      'mask_moment_audit':mask_moment_audit(),'kappa_zero_q':q,'kappa_zero_Jplus':increment_law_from_endpoints(kp0).tolist(),
      'kappa_zero_Jminus':increment_law_from_endpoints(km0).tolist(),'rows':rows,'continuous_unknown_kappa_certificate':cert,'fast_switching_observable_TV':fast_tv,'uniformization_independent_checks':uniformization_checks,'same_action_word_cross_model_checks':same_word_checks,'synthetic_finite_sample_runs':synthetic_runs,'finite_cost_ledger':finite_cost_ledger,
      'Mplus_AB_BA_endpoint_supnorm_by_kappa':sym,'one_letter_parity_flip_probabilities':{f'{m}_{a}':v[1] for (m,a),v in solo.items()},
      'one_letter_cross_model_flip_gaps':solo_gaps,
      'generator_orientation':'destination row, source column; columns sum to zero',
      'noisy_observation':'Y1=P1 xor iid Bernoulli(epsilon), Y2=P2 xor iid Bernoulli(epsilon); initial P0=0 is known exactly, and estimated increments are Uhat=Y1, Vhat=Y1 xor Y2; independent replicate unit per pulse word'}
    path=Path(__file__).with_name('CYCLE3_MODEL_OUTPUT.json')
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['kappa_zero_q','kappa_zero_Jplus','kappa_zero_Jminus','Mplus_AB_BA_endpoint_supnorm_by_kappa','one_letter_cross_model_flip_gaps']},indent=2))
    print('certificate',json.dumps(cert,indent=2))
    print('fast switching TV',fast_tv)
    print('uniformization max error',max(x['sup_error'] for x in uniformization_checks))
    print('same-action max cross-model error',max(x['sup_error'] for x in same_word_checks))
    print('synthetic finite runs',synthetic_runs)
    print('cost ledger',finite_cost_ledger)
    for row in rows: print(row['kappa'],row['order'],'latent increment J11 gap',row['latent_J11_gap'],'TVnoise',row['endpoint_TV_noisy'],'observed both-increment event gap',row['both_observed_increment_event_gap'])

if __name__=='__main__': main()
