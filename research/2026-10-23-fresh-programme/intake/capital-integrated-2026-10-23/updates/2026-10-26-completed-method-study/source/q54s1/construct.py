#!/usr/local/bin/python3
"""Reproduce the Q54 mathematical construction and model-only comparisons.

No device data are used. All laws are explicit, dimensionless model laws.
Outputs are written beside this file. Requires NumPy and SciPy only.
"""
from pathlib import Path
import csv
import json
import math
import numpy as np
from scipy.special import expit, ndtr, ndtri
from scipy.optimize import root

OUT = Path(__file__).resolve().parent
M_LOWER, M_UPPER = 1.0, 5.0
AMPLITUDE = M_UPPER - M_LOWER
SAFE, TARGET, CENTER, SIGMA = 0.5, 1.0, 0.65, 1e-3


def hidden(x, delta, center=CENTER):
    x = np.asarray(x, dtype=float)
    return AMPLITUDE * delta * (
        np.logaddexp(0.0, (x-center)/delta)
        - np.logaddexp(0.0, -center/delta)
    )


def stiffness(x, delta, center=CENTER):
    return M_LOWER + AMPLITUDE * expit((np.asarray(x)-center)/delta)


def risk(n, signal, sigma=SIGMA):
    return float(ndtr(-np.sqrt(n)*signal/(2*sigma)))


def required_count(signal, p=0.05, sigma=SIGMA):
    # Floating evaluation of the exact symbolic threshold. Large integer
    # ceilings are approximate at double precision, not unit-resolved counts.
    val = 4*sigma*sigma*float(ndtri(1-p))**2/signal**2
    return val, math.ceil(val)


def csv_write(name, rows):
    with (OUT/name).open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def check_laws_and_rates():
    rows = []
    for delta in [0.1, 0.05, 0.025, 0.0125, 0.01, 0.00625, 0.003125]:
        grid = np.linspace(0, SAFE, 10001)
        sig = float(hidden(SAFE, delta))
        db = float(hidden(TARGET, delta))
        upper = AMPLITUDE*delta*math.exp(-(CENTER-SAFE)/delta)
        nreal, nint = required_count(sig)
        k = stiffness(np.linspace(-2, 2, 20001), delta)
        assert hidden(0, delta) == 0
        assert np.all(np.diff(hidden(grid, delta)) >= 0)
        assert np.all(k >= M_LOWER) and np.all(k <= M_UPPER)
        assert sig <= upper*(1+1e-12)
        assert db >= AMPLITUDE*(TARGET-CENTER) - AMPLITUDE*delta*math.exp(-CENTER/delta) - 1e-13
        rows.append(dict(delta=delta, safe_signal=sig, safe_signal_upper=upper,
                         target_gap=db, endpoint_error_n_1e6=risk(10**6, sig),
                         n_for_5pct_error_real=nreal, n_for_5pct_error_rounded_float=nint,
                         minimum_stiffness=float(k.min()), maximum_stiffness=float(k.max())))
    csv_write('rate_sweep.csv', rows)
    return rows


def check_sharp_modulus():
    rows = []
    d = TARGET-SAFE
    for delta in [0.02, 0.005, 0.001, 0.0002, 0.00005]:
        c = SAFE+math.sqrt(delta*d)
        sig = float(hidden(SAFE, delta, c))
        db = float(hidden(TARGET, delta, c))
        rows.append(dict(delta=delta, center=c, safe_signature=sig,
                         target_gap=db, limiting_gap=AMPLITUDE*d,
                         gap_fraction=db/(AMPLITUDE*d)))
    assert rows[-1]['safe_signature'] < rows[0]['safe_signature']
    assert rows[-1]['target_gap'] > rows[0]['target_gap']
    csv_write('sharp_modulus.csv', rows)
    return rows


def compare_endpoint_and_differences():
    # A setting with nontrivial errors; policies receive exactly n scalar samples.
    delta, n, width = 0.025, 200, 0.05
    eps = float(hidden(SAFE, delta))
    signal_d = float(hidden(SAFE, delta)-hidden(SAFE-width, delta))
    rows = []
    rows.append(dict(policy='endpoint_optimal', scalar_readings=n,
                     discrimination_z=math.sqrt(n)*eps/(2*SIGMA),
                     exact_error=risk(n, eps)))
    # Optimal full-record likelihood for a fixed two-point design, a competent ordinary adaptation.
    total_signal_sq = (n//2)*(eps**2+float(hidden(SAFE-width, delta))**2)
    z_full=math.sqrt(total_signal_sq)/(2*SIGMA)
    rows.append(dict(policy='two_point_full_record_likelihood', scalar_readings=n,
                     discrimination_z=z_full, exact_error=float(ndtr(-z_full))))
    z_diff = math.sqrt(n)*signal_d/(4*SIGMA)
    rows.append(dict(policy='finite_difference_only', scalar_readings=n,
                     discrimination_z=z_diff, exact_error=float(ndtr(-z_diff))))
    assert rows[0]['exact_error'] <= rows[1]['exact_error'] <= rows[2]['exact_error']
    csv_write('matched_comparison.csv', rows)
    return rows


def adaptive_simulation():
    """Validate full likelihood risk and the exact Gaussian simulation kernel.

    Simulation is diagnostic, not the proof. Theorem 1 is the proof of optimum.
    Both hypotheses, retained raw histories, known candidate laws, same n/noise.
    """
    rng = np.random.default_rng(540026)
    delta, n, repeats = 0.025, 160, 40000
    eps = float(hidden(SAFE, delta))
    policies=['endpoint', 'uniform', 'history_feedback']
    rows=[]
    for policy in policies:
        for label in [0, 1]:
            llr=np.zeros(repeats)
            for t in range(n):
                if policy=='endpoint':
                    x=np.full(repeats, SAFE)
                elif policy=='uniform':
                    x=rng.uniform(0,SAFE,repeats)
                else:
                    # A truly history-dependent safe policy, retaining all data.
                    # This is a diagnostic example, not the strong comparator.
                    x=SAFE*(0.25+0.75*expit(llr))
                h=hidden(x,delta)
                residual=label*h+SIGMA*rng.standard_normal(repeats)
                llr += h*(residual-h/2)/(SIGMA**2)
            empirical=float(np.mean((llr>=0) != bool(label)))
            se=math.sqrt(empirical*(1-empirical)/repeats)
            rows.append(dict(policy=policy, hypothesis=label, readings=n,
                             replicates=repeats, empirical_error=empirical,
                             monte_carlo_se=se, endpoint_exact_error=risk(n,eps)))
    endpoint_rows=[r for r in rows if r['policy']=='endpoint']
    assert all(abs(r['empirical_error']-r['endpoint_exact_error']) < 5*r['monte_carlo_se']+1/repeats for r in endpoint_rows)
    csv_write('adaptive_simulation.csv',rows)

    # Test the constructive simulation kernel at a grid of selected points.
    kernel=[]
    for x in np.linspace(0, SAFE, 7):
        ratio=float(hidden(x,delta))/eps
        assert 0 <= ratio <= 1
        for label in [0,1]:
            w=M_LOWER*SAFE+label*eps+SIGMA*rng.standard_normal(repeats)
            y=M_LOWER*x+ratio*(w-M_LOWER*SAFE)+SIGMA*math.sqrt(1-ratio**2)*rng.standard_normal(repeats)
            mean_target=M_LOWER*x+label*float(hidden(x,delta))
            kernel.append(dict(x=x,hypothesis=label,ratio=ratio,
                               empirical_mean=float(y.mean()),theoretical_mean=mean_target,
                               empirical_variance=float(y.var()),theoretical_variance=SIGMA**2))
            assert abs(float(y.mean())-mean_target) < 5*SIGMA/math.sqrt(repeats)
            assert abs(float(y.var())-SIGMA**2) < 0.05*SIGMA**2
    csv_write('blackwell_kernel_check.csv',kernel)
    return rows


def passive_networks():
    # Same anchored preloaded equilibrium operation under either constitutive law.
    # Known unit anchoring ensures beta >= 1. No physical sensor advantage is inferred.
    rows=[]
    for geometry in ['parallel','chain']:
        for size in [4,16,64]:
            if geometry=='parallel':
                bmat=np.eye(size)
            else:
                bmat=np.eye(size)-np.eye(size,k=-1)
            # Explicit summations avoid spurious floating-point warning flags
            # observed in this host's BLAS matmul path. No warning suppression.
            gram=np.einsum('ei,ej->ij',bmat,bmat,optimize=False)
            for delta in [0.1,0.05,0.025]:
                prestrain=np.full(size,SAFE)
                load=M_LOWER*np.einsum('ei,e->i',bmat,prestrain,optimize=False)
                def gradient(z):
                    strain=np.einsum('ei,i->e',bmat,z,optimize=False)+prestrain
                    force=M_LOWER*strain+hidden(strain,delta)
                    return z+np.einsum('ei,e->i',bmat,force,optimize=False)-load
                def jacobian(z):
                    strain=np.einsum('ei,i->e',bmat,z,optimize=False)+prestrain
                    return np.eye(size)+np.einsum('ei,e,ej->ij',bmat,stiffness(strain,delta),bmat,optimize=False)
                sol=root(gradient,np.zeros(size),jac=jacobian,tol=1e-11)
                residual=float(np.linalg.norm(gradient(sol.x)))
                # HYBR can flag stagnation once residual is already at roundoff.
                assert residual < 1e-10
                strain=np.einsum('ei,i->e',bmat,sol.x,optimize=False)+prestrain
                assert strain.min() >= -1e-12 and strain.max() <= SAFE+1e-12
                beta=1+M_LOWER*float(np.linalg.eigvalsh(gram)[0])
                norm_b=float(np.linalg.norm(bmat,2))
                eps=float(hidden(SAFE,delta))
                bound=norm_b*math.sqrt(size)*eps/beta
                movement=float(np.linalg.norm(sol.x))
                assert movement <= bound*(1+1e-6)+1e-12
                rows.append(dict(geometry=geometry,components=size,delta=delta,
                                 displacement_gap=movement,sensitivity_bound=bound,
                                 bound_fraction=movement/bound,beta_lower=beta,
                                 coupling_norm=norm_b,residual=residual,
                                 minimum_strain=float(strain.min()),maximum_strain=float(strain.max())))
    csv_write('passive_networks.csv',rows)
    return rows


def main():
    rates=check_laws_and_rates()
    modulus=check_sharp_modulus()
    comparisons=compare_endpoint_and_differences()
    simulations=adaptive_simulation()
    networks=passive_networks()
    result=dict(
        interpretation='Mathematical model and Monte Carlo diagnostics; no physical measurements.',
        assumptions=dict(m=M_LOWER,L=M_UPPER,a=SAFE,b=TARGET,c=CENTER,sigma=SIGMA),
        selected_rate=[r for r in rates if r['delta']==0.01][0],
        sharp_modulus_last=modulus[-1],
        matched_comparison=comparisons,
        simulated_endpoint=[r for r in simulations if r['policy']=='endpoint'],
        network_cases=len(networks),
        maximum_network_bound_fraction=max(r['bound_fraction'] for r in networks),
        status='Bridge defeated in stated observation class; qualifying scientific advance not established.'
    )
    (OUT/'numerical_summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    main()
