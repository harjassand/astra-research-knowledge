"""Finite model of copying a structural reference under load.

This is theoretical/executable evidence, not a fabricated material.  Controller
functions receive sensor records, never the pristine rest-length target.
Run: python reference_turnover.py
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import os
from pathlib import Path

import numpy as np
from scipy.integrate import quad
from scipy.linalg import expm, null_space

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "results"
OUT.mkdir(exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(OUT / "mpl-cache"))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

KB = 1.380649e-23


def equilibrium_length(rest, stiffness, force):
    return (force + np.dot(rest, stiffness)) / np.sum(stiffness)


def rocker(rest1, rest2, stiffness, pivot_stiffness, temperature):
    h = 2 * stiffness + pivot_stiffness
    return {
        "mean": stiffness * (rest2 - rest1) / h,
        "variance": KB * temperature / h,
        "natural_length_gain": h / stiffness,
        "terminal_stiffness": 2 * stiffness,
    }


def ou_average_factor(duration_over_tau):
    z = duration_over_tau
    if z < 1e-3:
        return 1 - z / 3 + z * z / 12 - z**3 / 60
    return 2 * (z + math.expm1(-z)) / z**2


def observer_checks():
    k, kap, temp, tau = 1.0, 0.2, 300.0, 1e-3
    d = 2e-9
    records = []
    maximum_equilibrium_residual = 0.0
    for L in np.linspace(-1e-3, 1e-3, 31):
        r1, r2 = 0.0, d
        state = rocker(r1, r2, k, kap, temp)
        x = state["mean"]
        derivative = -k * (L - r1 - x) + k * (L - r2 + x) + kap * x
        maximum_equilibrium_residual = max(maximum_equilibrium_residual, abs(derivative))
        assert abs(k * (L-r1-x) + k * (L-r2+x) - k*(2*L-r1-r2)) < 1e-17
    for T in [1e-4, 1e-3, 1e-2, 1e-1, 1.0]:
        v = state["variance"] * state["natural_length_gain"]**2 * ou_average_factor(T/tau)
        direct = 2 * quad(lambda t: (T-t)*math.exp(-t/tau), 0, T,
                         epsabs=1e-20)[0] / T**2
        assert abs(direct-ou_average_factor(T/tau)) < 1e-8
        records.append({"window_s": T, "rest_difference_sd_m": math.sqrt(v)})
    # Exact series piezo reduction, checked by minimizing its internal displacement.
    kb, kp, h, beta, Q, extension = 3.0, 5.0, 0.7, 2.0, 0.13, 0.27
    xp = (kb*extension+h*Q)/(kb+kp)
    raw = 0.5*kb*(extension-xp)**2+0.5*kp*xp*xp-h*Q*xp+0.5*beta*Q*Q
    ke = kb*kp/(kb+kp)
    he = kb*h/(kb+kp)
    be = beta-h*h/(kb+kp)
    reduced = 0.5*ke*extension**2-he*Q*extension+0.5*be*Q*Q
    assert abs(raw-reduced) < 1e-14
    return {"model": "equilibrium rocker; stationary overdamped Gaussian meter",
            "stiffness_N_per_m": k, "pivot_stiffness_N_per_m": kap,
            "temperature_K": temp, "relaxation_time_s": tau,
            "maximum_equilibrium_residual_N": maximum_equilibrium_residual,
            "finite_windows": records, "series_piezo_energy_residual": abs(raw-reduced)}


class FiniteOUReadout:
    """Exact joint OU endpoint and finite-window average for independent channels."""
    def __init__(self, sigma, tau, rng, channels=3):
        self.sigma,self.tau,self.rng=sigma,tau,rng
        self.state=rng.normal(0,sigma,channels)
        self.elapsed=0.0
        self.windows=0

    def average_noise(self, duration):
        t=self.tau; s2=self.sigma**2
        a=math.exp(-duration/t); z=1-a
        v_end=s2*(1-a*a)
        v_avg=s2*(2*t/duration-4*t*t*z/duration**2
                  +t*t*(1-a*a)/duration**2)
        cov=s2*t*z*z/duration
        endpoint=self.rng.normal(0,math.sqrt(v_end),self.state.size)
        residual=self.rng.normal(0,math.sqrt(max(0,v_avg-cov*cov/v_end)),self.state.size)
        average=t*z/duration*self.state+cov/v_end*endpoint+residual
        self.state=a*self.state+endpoint
        self.elapsed+=duration;self.windows+=1
        return average


def relative_calibration(k, gain, offsets, rest, lengths, readout, duration=0.5):
    """The calibration output contains no length, force or target reference.

    Each offset is obtained from a physically force-free branch.  Two subsequent
    common-gap states provide relative slopes.  The controller receives only
    records and the known sign of the test motion, not its amplitude.
    """
    zeros=np.zeros(3)
    # Three separate force-free episodes, not simultaneous removal of all paths.
    for i in range(3):
        zeros[i]=offsets[i]+readout.average_noise(duration)[i]
    z = np.array([gain*k*(L-rest)+offsets+readout.average_noise(duration)
                  for L in lengths])
    slopes = z[1]-z[0]
    assert np.all(slopes > 0)
    return zeros, slopes


def finite_controller(seed=1927, biased_zero=False):
    """A sensor-only controller copies two healthy references into one newcomer."""
    rng = np.random.default_rng(seed)
    k = np.array([0.86, 1.12, 1.03])
    gain = np.array([0.8, 1.3, 1.1])
    offsets = np.array([0.02, -0.013, 0.01])*1e-6
    target = 10e-6                 # used ONLY in environment and final evaluation
    rest = np.array([target, target, target+120e-9])
    sigma = 0.02e-9                # record noise in calibrated arbitrary signal units
    readout=FiniteOUReadout(sigma,1e-3,rng)
    zeros, slopes = relative_calibration(k, gain, offsets, rest,
                                        [target+0.1e-6, target+0.3e-6], readout)
    calibration_time=readout.elapsed
    if biased_zero:
        zeros[2] += gain[2]*k[2]*8e-9
    gain_ratio_true = gain*k/(gain[0]*k[0])
    gain_ratio_est = slopes/slopes[0]
    dt, steps, servo_gain, vmax = 0.002, 900, 1.0e-6, 2e-6
    trace=[]
    initial=rest.copy()
    work=0.0
    for it in range(steps):
        t=it*dt
        F=(0.3+0.17*math.sin(13*t)+0.07*math.sin(41*t))*1e-6
        L=equilibrium_length(rest, k, F)
        f=k*(L-rest)
        # Rest length is latched during each finite observation interval. Shared
        # load contributions cancel; no 64 independent reads are granted in 2ms.
        z=gain*f+offsets+readout.average_noise(dt)
        normalized=(z-zeros)/slopes
        error_signal=normalized[2]-(normalized[0]+normalized[1])/2
        change=np.clip(servo_gain*error_signal, -vmax, vmax)*dt
        # Exact change of constant-load potential, including load re-equilibration.
        delta_G=-f[2]*change+0.5*k[2]*(1-k[2]/sum(k))*change*change
        work += max(0.0, delta_G)   # does not count possible energy recovery
        rest[2] += change
        if it%5==0:
            trace.append([t, F, L, rest[2], error_signal])
    trace=np.asarray(trace)
    return {
        "noise_is_illustrative_not_measured": True,
        "initial_rest_lengths_m": initial.tolist(), "final_rest_lengths_m": rest.tolist(),
        "final_copy_error_m": float(rest[2]-target),
        "relative_slope_max_fraction_error": float(np.max(abs(gain_ratio_est/gain_ratio_true-1))),
        "positive_quasistatic_mechanical_work_J": work,
        "calibration_observation_time_s":calibration_time,
        "control_observation_time_s":steps*dt,
        "total_observation_time_s":readout.elapsed,
        "number_of_finite_readout_windows":readout.windows,
        "readout_correlation_time_s":readout.tau,
        "readout_equilibrium_sd":readout.sigma,
        "additional_unmodeled_time":"mechanical unload/reload, probe motion, settling, latching and physical part delivery",
        "controller": "two current force references; zero-state records; two unknown-amplitude shared probe states",
        "biased_zero": biased_zero,
    }, trace


def renewal_matrices(n=3):
    updates=[]
    for i in range(n):
        a=np.eye(n)
        a[i,:]=1/(n-1)
        a[i,i]=0
        updates.append(a)
    a=np.eye(n)
    noise=np.zeros((n,n))
    for i, ai in enumerate(updates):
        a=ai@a
        noise=ai@noise
        noise[i,i]+=1
    w=null_space((a.T-np.eye(n)))[:,0]
    w=w/w.sum()
    return a, noise, w


def repeated_copying(seed=472, rounds=1500, samples=5000, copy_sd=1e-9):
    rng=np.random.default_rng(seed)
    a,b,w=renewal_matrices(3)
    expected_D=float(np.sum((w@b)**2)*copy_sd**2)
    assert np.max(abs(w@a-w))<1e-14
    assert abs(expected_D/copy_sd**2-4/3)<1e-13
    x=np.zeros((samples,3))
    digital=np.zeros((samples,3))
    history=[]
    theory_cov=np.zeros((3,3))
    for t in range(1,rounds+1):
        eta=rng.normal(0,copy_sd,(samples,3))
        x=x@a.T+eta@b.T
        # Strong ordinary reference: each replacement is independently calibrated
        # against a retained target code plus an absolute dimensional standard.
        digital=rng.normal(0,copy_sd,(samples,3))
        theory_cov=a@theory_cov@a.T+copy_sd**2*(b@b.T)
        if t in [1,3,10,30,100,300,1000,rounds]:
            history.append({"rounds":t,
                "comparison_only_reference_sd_m":float(np.std(x@w,ddof=1)),
                "exact_reference_sd_m":math.sqrt(t*expected_D),
                "mean_rest_length_sd_m":float(np.std(x.mean(1),ddof=1)),
                "exact_mean_rest_length_sd_m":math.sqrt(float(np.ones(3)@theory_cov@np.ones(3))/9),
                "coded_reference_mean_sd_m":float(np.std(digital.mean(1),ddof=1))})
    empirical=float(np.var(x@w,ddof=1))
    assert abs(empirical/(rounds*expected_D)-1)<0.08
    return {"copy_sd_m":copy_sd,"samples":samples,"rounds":rounds,
            "round_transition":a.tolist(),"round_noise_map":b.tolist(),
            "conserved_left_reference":w.tolist(),
            "variance_added_per_round_m2":expected_D,
            "empirical_to_exact_variance_ratio":empirical/(rounds*expected_D),
            "history":history}


def repair_lifetime():
    out=[]
    lam=1e-5
    for repair_time in [0.01, 0.1, 1.0, 10, 100, 1000]:
        mean_det=1/(3*lam*(-math.expm1(-2*lam*repair_time)))+1/(2*lam)
        mu=1/repair_time
        Q=np.array([[-3*lam,3*lam],[mu,-mu-2*lam]])
        exact=-np.linalg.solve(Q,np.ones(2))[0]
        formula=(mu+5*lam)/(6*lam*lam)
        # Very separated rates make this 2x2 generator ill-conditioned.
        assert abs(exact/formula-1)<1e-8
        out.append({"repair_time_s":repair_time,"mean_deterministic_repair_lifetime_s":mean_det,
                    "mean_exponential_repair_lifetime_s":exact,
                    "single_member_lifetime_s":1/lam,
                    "generator_solve_relative_error":exact/formula-1,
                    "generator_condition_number":float(np.linalg.cond(Q))})
    # This is a TWO-fault overlap calculation, not a complete reliability prediction.
    return {"independent_fault_rate_per_member_per_s":lam,"rows":out,
            "excluded": ["wrong diagnosis", "reference diffusion", "common-mode faults",
                         "controller, junction and delivery failures", "finite consumables"]}


def energy_checks():
    k, F, r0 = 1.0, 1e-6, 10e-6
    rows=[]
    for delta in [1e-9,1e-8,1e-7,1e-6,2e-6]:
        old=np.array([r0,r0,r0+delta])
        new=np.ones(3)*r0
        def G(r):
            L=equilibrium_length(r,np.ones(3)*k,F)
            return 0.5*k*np.sum((L-r)**2)-F*L
        numeric=G(new)-G(old)
        formula=F*delta/3-k*delta*delta/3
        assert abs(numeric-formula)<1e-26
        rows.append({"overlength_m":delta,"repair_free_energy_change_J":numeric,
                     "formula_J":formula})
    return {"stiffness_per_member_N_per_m":k,"load_N":F,"rows":rows,
            "temporary_extension_if_one_of_three_removed_m":F/(6*k)}


def global_geometry_failure():
    # Explicit reflection ambiguity: two valid K5 rest metrics differ in two edges.
    pts=np.array([[0.,0.],[2.,0.],[0.3,1.1],[1.6,1.7],[0.9,-0.8]])
    other=pts.copy(); other[4,1]*=-1
    edges=list(itertools.combinations(range(5),2))
    def lengths(p): return np.array([np.linalg.norm(p[i]-p[j]) for i,j in edges])
    a,b=lengths(pts),lengths(other)
    changed=np.flatnonzero(abs(a-b)>1e-10)
    assert len(changed)==2
    received=a.copy(); received[changed[0]]=b[changed[0]]
    assert np.count_nonzero(abs(received-a)>1e-10)==1
    assert np.count_nonzero(abs(received-b)>1e-10)==1
    return {"changed_edges":[edges[j] for j in changed],
            "embedding_a":pts.tolist(),"embedding_b":other.tolist(),
            "received_natural_lengths":received.tolist(),
            "conclusion":"one faulty distance is globally ambiguous in this K5 example"}


def compatibility_distance_check():
    pts=np.array([[0.,0.],[2.,0.],[0.3,1.1],[1.6,1.7],[0.9,-0.8]])
    edges=list(itertools.combinations(range(5),2)); rows=[]
    for i,j in edges:
        row=np.zeros(10);v=pts[i]-pts[j];v=v/np.linalg.norm(v)
        row[2*i:2*i+2]=v;row[2*j:2*j+2]=-v;rows.append(row)
    B=np.asarray(rows);r=np.linalg.matrix_rank(B)
    min_delete=None
    for z in range(1,5):
        for subset in itertools.combinations(range(10),z):
            if np.linalg.matrix_rank(np.delete(B,subset,axis=0))<r:
                min_delete=z;break
        if min_delete is not None:break
    H=null_space(B.T).T
    max_decode_error=0.
    for j in range(10):
        d=np.zeros(10);d[j]=1.
        y=H@d
        candidates=[]
        for h in range(10):
            amp=float(H[:,h]@y/(H[:,h]@H[:,h]))
            candidates.append((np.linalg.norm(y-H[:,h]*amp),h,amp))
        residual,loc,amp=min(candidates)
        assert loc==j
        max_decode_error=max(max_decode_error,residual,abs(amp-1))
    assert min_delete==3
    return {"rank":int(r),"linear_compatibility_code_distance":min_delete,
            "exact_single_error_decode_max_residual":max_decode_error,
            "warning":"local tangent result; global nonlinear ambiguity tested separately"}


def make_figure(results,trace,biased_trace):
    plt.rcParams.update({"font.size":10,"axes.spines.top":False,"axes.spines.right":False})
    fig,axs=plt.subplots(2,2,figsize=(11,8),layout="constrained")
    axs[0,0].plot(trace[:,0],(trace[:,3]-1e-5)*1e9,label="finite calibrated feedback")
    axs[0,0].plot(biased_trace[:,0],(biased_trace[:,3]-1e-5)*1e9,
                   label="8 nm equivalent sensor-zero bias",ls="--")
    axs[0,0].set(xlabel="Time (s)",ylabel="Copied rest-length error (nm)",
                   title="Copying from two current load paths")
    axs[0,0].legend(fontsize=8)
    axs[0,1].plot(trace[:,0],trace[:,1]*1e6)
    axs[0,1].set(xlabel="Time (s)",ylabel="External load (µN)",
                   title="Changing load is not supplied to the controller")
    h=results["repeated_copying"]["history"]
    x=np.array([a["rounds"] for a in h])
    axs[1,0].loglog(x,[a["comparison_only_reference_sd_m"]*1e9 for a in h],"o",label="Monte Carlo")
    axs[1,0].loglog(x,[a["exact_reference_sd_m"]*1e9 for a in h],label="exact comparison-only diffusion")
    axs[1,0].loglog(x,[a["coded_reference_mean_sd_m"]*1e9 for a in h],label="stored specification + dimensional standard")
    axs[1,0].set(xlabel="Complete three-member renewal rounds",ylabel="Reference uncertainty (nm)",
                   title="Agreement does not stop common reference drift")
    axs[1,0].legend(fontsize=8)
    rr=results["energy"]["rows"]
    axs[1,1].semilogx([a["overlength_m"]*1e9 for a in rr],
                     [a["repair_free_energy_change_J"]*1e15 for a in rr],"o-")
    axs[1,1].axhline(0,color="0.6",lw=0.7)
    axs[1,1].set(xlabel="Faulty member overlength (nm)",ylabel="Minimum quasistatic work (fJ)",
                   title="Repair can require work despite releasing mismatch")
    fig.suptitle("Renewing a material's geometric reference — model predictions, not device data",fontsize=13)
    fig.savefig(OUT/"reference_turnover.png",dpi=180)
    plt.close(fig)


def main():
    good,tr=finite_controller()
    bad,btr=finite_controller(biased_zero=True)
    assert abs(good["final_copy_error_m"])<1e-9
    assert abs(bad["final_copy_error_m"])>5e-9
    results={"scope":"conditional models only; no fabricated material or demonstrated resource advantage",
             "observer":observer_checks(),"finite_controller":good,"biased_sensor_control":bad,
             "repeated_copying":repeated_copying(),"overlap_lifetime":repair_lifetime(),
             "energy":energy_checks(),"linear_geometry":compatibility_distance_check(),
             "nonlinear_geometry_failure":global_geometry_failure()}
    (OUT/"reference_turnover_results.json").write_text(json.dumps(results,indent=2)+"\n")
    make_figure(results,tr,btr)
    print(json.dumps({"finite_controller":good,"biased_sensor_error_m":bad["final_copy_error_m"],
          "reference_variance_per_round_m2":results["repeated_copying"]["variance_added_per_round_m2"],
          "monte_carlo_exact_variance_ratio":results["repeated_copying"]["empirical_to_exact_variance_ratio"],
          "linear_geometry":results["linear_geometry"],
          "nonlinear_ambiguity_edges":results["nonlinear_geometry_failure"]["changed_edges"]},indent=2))


if __name__=="__main__":main()
