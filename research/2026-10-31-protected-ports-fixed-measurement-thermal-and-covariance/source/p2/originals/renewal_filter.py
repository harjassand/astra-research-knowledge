"""Passive cold-port spectral separation: gauge renewal vs gate dephasing.

The central electrode sees a parallel RLC impedance, compared with an
RC port at the same R,C,lever arm,temperature. Rates are the explicitly
stated weak-coupling secular model. This is not a complete microscopic
finite-coupling error bound or a full spin-bus gate simulation.
"""
import json
import math
import sys
from pathlib import Path
from functools import lru_cache
import numpy as np
from scipy.linalg import eigh, eigvals, expm
from scipy.optimize import brentq

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'source_physics'))
from star_cooling import exact_gauge

HBAR_EV_S=6.582119569e-16
R_K=25812.80745


def spectrum(w,beta,kind,omega0=None,Q=None,wc=None):
    w=np.asarray(w,float); x=abs(w)
    if kind=='RLC':
        ratio=np.zeros_like(w)
        nz=x>1e-14
        ratio[nz]=1/(1+Q**2*(x[nz]/omega0-omega0/x[nz])**2)
    else:
        ratio=1/(1+(x/wc)**2)
    out=np.zeros_like(w)
    zero=x<1e-14; out[zero]=ratio[zero]/beta
    pos=w>1e-14
    out[pos]=w[pos]/(-np.expm1(-beta*w[pos]))*ratio[pos]
    neg=w < -1e-14
    wn=-w[neg]
    out[neg]=wn*np.exp(-beta*wn)/(-np.expm1(-beta*wn))*ratio[neg]
    return out


def model(beta=200.,kind='RLC',omega0=.8,Q=1.,wc=1.,epsilon=.4):
    B,D,T,N,_=exact_gauge()
    H=D+.1*T+epsilon*(N-np.eye(7))
    e,v=eigh(H); n=v.T@N@v
    args=dict(beta=beta,kind=kind,omega0=omega0,Q=Q,wc=wc)
    W=abs(n)**2*spectrum(e[None,:]-e[:,None],**args)
    np.fill_diagonal(W,0)
    exits=W.sum(axis=0); rate=W-np.diag(exits)
    weights=np.exp(-beta*(e-e[0])); peq=weights/sum(weights)
    coh=(exits[:,None]+exits[None,:])/2
    coh+=float(spectrum(np.array([0.]),**args)[0])*(np.diag(n)[:,None]-np.diag(n)[None,:])**2/2
    cohgap=float(np.min(coh[np.triu_indices(7,1)]))
    pgap=float(-np.sort(eigvals(rate).real)[-2])
    def bound(s):
        pt=expm(rate*s)
        tv=np.max(np.sum(abs(pt-peq[:,None]),axis=0)/2)
        return float(tv+3*np.exp(-cohgap*s))
    s_hi=1.
    while bound(s_hi)>1e-6: s_hi*=2
    mixing=brentq(lambda s:bound(s)-1e-6,0.,s_hi)
    return dict(epsilon_over_U=epsilon,population_gap=pgap,coherence_gap=cohgap,
                scaled_mixing_time=mixing,mixing_bound=bound(mixing),
                max_exit=float(max(exits)),thermal_excitation=float(sum(weights[1:])/sum(weights)))


@lru_cache(None)
def full_density_harmonics():
    sys.path.insert(0,str(HERE/'alternatives'))
    from star_floquet_force import force
    d=force(steps=2048,return_waveform=True)
    samples=np.array(d['density_difference_samples'])
    amplitudes=np.fft.fft(samples)/len(samples)
    harmonics=np.fft.fftfreq(len(samples),d=1/len(samples))
    return d,harmonics,abs(amplitudes)**2


def projected_gate_dephasing(args,omega=.05):
    """Longitudinal Floquet diagonal model on the full numerical grid.

    This excludes off-diagonal transitions to charge Floquet bands.
    This is not an upper bound on total physical gate error.
    """
    data=json.loads((HERE/'alternatives'/'star_floquet_force_results.json').read_text())['actual_point'][-1]
    mean=data['mean_density_difference']
    rate=.5*mean**2*float(spectrum(np.array([0.]),**args)[0])
    contributions=[]
    for h in data['harmonics']:
        k=h['harmonic']; amp=h['density_difference_cosine']
        component=amp**2/8*float(sum(spectrum(np.array([k*omega,-k*omega]),**args)))
        rate+=component; contributions.append(component)
    duration=math.pi/(2*abs(data['force_real']))
    full,ks,powers=full_density_harmonics()
    complete=.5*float(np.sum(powers*spectrum(-ks*omega,**args)))
    return dict(unit_eta_rate=complete,gate_time_U=duration,
                unit_eta_gate_dephasing_exponent=complete*duration,
                harmonic_rate_contributions=contributions,
                five_harmonic_rate=rate,
                all_sampled_harmonics_minus_five=complete-rate,
                scope='Projected Floquet diagonal coupling, full 2048-point Fourier grid, no charge transitions or full gate certificate.')


def run():
    Uev=.0005; C=1e-14; alpha=.05; beta=200.; omega0=.8
    Ufreq=Uev/HBAR_EV_S; omega_physical=omega0*Ufreq
    L=1/(C*omega_physical**2)
    rows=[]
    for quality in [.25,.5,1.,2.,4.]:
        R=quality/(omega_physical*C)
        eta=4*math.pi*alpha**2*R/R_K
        wc=1/(R*C*Ufreq)
        devices=[]
        for kind in ['RC','RLC']:
            args=dict(beta=beta,kind=kind,omega0=omega0,Q=quality,wc=wc)
            cool=model(**args); gate=projected_gate_dephasing(args)
            tmix=cool['scaled_mixing_time']/(eta*Ufreq)
            devices.append(dict(kind=kind,renewal=cool,gate_diagonal_model=gate,
                renewal_time_us=tmix*1e6,
                projected_gate_dephasing_exponent=eta*gate['unit_eta_gate_dephasing_exponent'],
                max_decay_over_U=eta*cool['max_exit'],
                residual_energy_over_U_for_1e_minus3_renewal_action=1e-3/(tmix*Ufreq)))
        rows.append(dict(Q=quality,R_ohm=R,eta=eta,RC_cutoff_over_U=wc,devices=devices))
    sys.path.insert(0,str(HERE/'coulomb_leakage'))
    from star_geometry import slab_full_row_bound,gaussian_u
    selected=rows[2]['devices'][1]
    renewal_s=selected['renewal_time_us']*1e-6
    loop_s=selected['gate_diagonal_model']['gate_time_U']/Ufreq
    geometry_U=gaussian_u(.5,.2)
    geometric_rows=[]
    for d in [10.,11.,12.,13.]:
        kappa_ratio=slab_full_row_bound(d,.5,orbital_radius=.2)/geometry_U
        geometric_rows.append(dict(d_over_a=d,
            direct_action_for_renewal_plus_ideal_loop=kappa_ratio*(renewal_s+loop_s)*Ufreq,
            full_duration_us_allowed_by_direct_action_1e_minus3=1e-3/kappa_ratio/Ufreq*1e6))
    result=dict(physical_model=dict(U_eV=Uev,C_F=C,alpha=alpha,beta_U=beta,
                     resonance_over_U=omega0,resonance_GHz=omega_physical/(2*math.pi*1e9),
                     inductance_nH=L*1e9),
                rows=rows,
                direct_interaction_component_comparison=dict(
                    renewal_us=renewal_s*1e6,ideal_loop_us=loop_s*1e6,
                    rows=geometric_rows,
                    caveat='Same dimensionless component models; not a jointly established microscopic dot. Additional source, ramp, readout and routing durations must fit the full-duration bound.'),
                limitations=['The rates assume a fresh equilibrium Gaussian voltage bath and weak-coupling secular reduction.',
                             'No finite-coupling master-equation approximation bound is certified here.',
                             'Same R,C,alpha,T for RC and RLC; RLC adds a physical inductor and broad spectral tuning.',
                             'The physical capacitance counterterm must be incorporated into acquired local charge parameters.',
                             'Source/isolation errors, active charge transitions, bus loss and symmetry mismatch remain separate.'])
    Path(__file__).with_name('renewal_filter_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__': run()
