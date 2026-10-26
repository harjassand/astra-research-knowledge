#!/usr/bin/env python3
"""Complete unconditional state-vector loss audit for finite-time captured photon.
An independent Markovian emitter decay channel is included; jump trajectories
remain orthogonal environmental states. No postselection on successful capture.
"""
import json,math
from pathlib import Path
import numpy as np
from scipy.linalg import eigh_tridiagonal, expm
from scipy.optimize import brentq
from scipy.integrate import quad
OUT=Path(__file__).resolve().parent
N=90; g=.7; d=np.ones(N); off=np.r_[g,np.full(N-2,.5)]
e,V=eigh_tridiagonal(d,off)
w=V[0]**2
survival=lambda t:float(np.sum(w*np.cos((e-1)*t)))
T=brentq(survival,2.43388605,2.433886053)
U=(V*np.exp(-1j*e*T))@V.T
phi=U.conj().T[:,0].copy();phi[16+1:]=0;phi/=np.linalg.norm(phi)
lead_e,lead_v=eigh_tridiagonal(d[1:],off[1:])
lead_U=(lead_v*np.exp(-1j*lead_e*math.pi))@lead_v.T

def hold(psi,r,kappa):
    out=psi.copy()
    out[0]*=np.exp(-1j*math.pi*(1+r))*np.exp(-kappa*math.pi/2)
    out[1:]=lead_U@psi[1:]
    return out

rho=np.zeros((N,N),complex);rho[0,0]=1
h=np.diag(d)+np.diag(off,1)+np.diag(off,-1)
ideal0=U@hold(U@phi,0,0)
Icapture=float(quad(lambda t:survival(t)**2,0,T,epsabs=1e-13)[0]);Iexposure=math.pi+2*Icapture
scans=[]
for kappa in (0,1e-7,1e-6,5e-6,1e-5,2e-5,5e-5,1e-4):
    Ueff=expm((-1j*h-.5*kappa*rho)*T)
    photon_capture=Ueff@phi
    row={'independent_local_loss_rate_over_B':kappa,
         'hold_only_strict_full_state_error_lower_bound':math.sqrt(max(0,2*(1-math.exp(-kappa*math.pi/2))))}
    for r in (0,1):
        out=Ueff@hold(photon_capture,r,kappa)
        normsq=float(np.linalg.norm(out)**2)
        target=ideal0 if r==0 else -ideal0
        overlap=np.vdot(target,out)
        # Since emitted environment photons are orthogonal, pure state error
        # = sqrt(||out_nojump-target||^2 + p_emission) =sqrt(2-2Re overlap)
        full_error=math.sqrt(max(0,2-2*overlap.real))
        row[f'root{r}_no_jump_survival_probability']=normsq
        row[f'root{r}_independent_radiation_probability']=1-normsq
        row[f'root{r}_full_environment_state_error']=full_error
        if kappa>0:row[f'root{r}_error_div_sqrt_kappaI']=full_error/math.sqrt(kappa*Iexposure)
        assert normsq<=1+1e-10
        if kappa>0:assert full_error>=row['hold_only_strict_full_state_error_lower_bound']-1e-8
    scans.append(row)
limit=-2*math.log1p(-.01**2/2)/math.pi
result={'hamiltonian':'positive full bosonic Jacobi with boundary g=0.7 and independent Markov loss only on boundary',
 'finite_site_modes':N,'input_source_sites':16,'capture_time':T,
 'ideal_one_transfer_emitter_exposure_integral':Icapture,
 'ideal_full_capture_hold_release_emitter_exposure_integral':Iexposure,
 'small_kappa_error_asymptote':'epsilon^2/kappa -> integral dt p_e(t)=%.13g'%Iexposure,
 'hold_only_no_go':'epsilon_hold>=sqrt(2*(1-exp(-kappa*pi/(2U)))) for fixed local phase pi at strength U',
 'necessary_kappa_over_U_for_1percent_hold_only':limit,
 'complete_finite_photon_env_scans':scans,
 'physical_caveats':['Markov bath is unbounded in frequency and not itself a positive-Fock-sector completion; the loss audit is an effective open-system test of the positive signal Hamiltonian',
                     'Original non-Hermitian no-jump propagation includes emission from capture and release, not only hold',
                     'The exact single-photon environmental purification is included through normalized jump norm',
                     'No finite-time microscopic independent-radiation Hamiltonian is supplied',
                     'No calibration noise or preparation error beyond finite 16-site packet']}
(OUT/'capture_independent_loss_results.json').write_text(json.dumps(result,indent=2))
print('ideal emitter exposure',Iexposure,'capture each',Icapture, 'needed kappa/U<',limit)
for r in scans:print('loss',r['independent_local_loss_rate_over_B'],'err r1',r['root1_full_environment_state_error'],'r0',r['root0_full_environment_state_error'],'no jump',r['root1_no_jump_survival_probability'])
