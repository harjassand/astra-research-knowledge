"""Finite-bandwidth Gaussian audit of imperfect continuous parity sensing.

Exact coherent-state dynamics for H=lambda*(ZZ+u*Zc+v*Za)*(m+m^dag),
ordinary meter damping, and optional joint-X toggling of the two data cats.
Does not model the physical cost of the X pulses; that cost must be added.
"""
from pathlib import Path
import json
import numpy as np
from scipy.special import erfc


def run_case(omega, dt=0.0005):
    kappa, lam, u, v, T, tr, eta = 1.0, 0.5, 0.05, 0.03, 20.0, 20.0, 0.8
    zc = np.array([1.,1.,-1.,-1.])
    za = np.array([1.,-1.,1.,-1.])
    parity = zc * za
    beta = np.zeros(4, dtype=complex)
    beta_ideal = 0j
    integrals_diff = np.zeros((4,4))
    integrals_n = np.zeros(4)
    ideal_n_integral = 0.0
    toggles = 0
    previous_sign = 1.0
    steps = int(round((T+tr)/dt))
    decay = np.exp(-kappa * dt/2)
    for j in range(steps):
        t = (j+0.5)*dt
        on = t < T
        sign = 1.0 if omega == 0 else (1.0 if np.sin(omega*t)>=0 else -1.0)
        if on and sign != previous_sign:
            toggles += 1
            previous_sign = sign
        force = lam*(parity + sign*(u*zc+v*za)) if on else np.zeros(4)
        force_i = lam if on else 0.0
        beta_next = beta*decay - 2j*force/kappa*(1-decay)
        ideal_next = beta_ideal*decay - 2j*force_i/kappa*(1-decay)
        mid = (beta+beta_next)/2
        mid_i = (beta_ideal+ideal_next)/2
        integrals_diff += abs(mid[:,None]-mid[None,:])**2*dt
        integrals_n += abs(mid)**2*dt
        ideal_n_integral += abs(mid_i)**2*dt
        beta, beta_ideal = beta_next, ideal_next
    coherence = np.exp(-0.5*kappa*integrals_diff-
                       0.5*abs(beta[:,None]-beta[None,:])**2)
    amplitudes = np.exp(-0.5*kappa*integrals_n)
    nojump = {}
    sector_errors = {}
    for name, pair in {"plus":(0,3),"minus":(1,2)}.items():
        i,j=pair
        sector_errors[name]=float((1-coherence[i,j])/2)
        ai,aj=amplitudes[i],amplitudes[j]
        # Residual meter state is negligible after the specified ringdown,
        # but include its coherent overlap in the conditional fidelity.
        inner=float(np.exp(-0.5*abs(beta[i]-beta[j])**2))
        fid=(ai*ai+aj*aj+2*ai*aj*inner)/(2*(ai*ai+aj*aj))
        nojump[name]={"probability_for_equal_sector_superposition":float((ai*ai+aj*aj)/2),
                      "conditional_infidelity":float(1-fid),
                      "log_amplitude_ratio":float(np.log(ai/aj))}
    E=kappa*ideal_n_integral
    return {"parameters":{"kappa":kappa,"lambda":lam,"u":u,"v":v,"eta":eta,
                          "gate_duration":T,"ringdown":tr,"omega":omega,"dt":dt},
            "ideal_parity_readout_error":float(0.5*erfc(np.sqrt(2*eta*E))),
            "ideal_total_emitted_photons":float(E),
            "within_parity_sector_dephasing_error":sector_errors,
            "no_click_branch":nojump,
            "joint_X_toggles":toggles,
            "physical_single_cat_X_pulses":2*toggles,
            "max_residual_meter_population":float(np.max(abs(beta)**2))}


if __name__ == "__main__":
    # T=20 contains an integer number of periods in the modulated cases.
    result={"scope":"Exact Gaussian effective meter, ideal toggling pulses; finite sensing/reset.",
            "cases":[run_case(w) for w in (0.0,np.pi,4*np.pi)]}
    path=Path(__file__).with_name("parity_meter_results.json")
    path.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))
