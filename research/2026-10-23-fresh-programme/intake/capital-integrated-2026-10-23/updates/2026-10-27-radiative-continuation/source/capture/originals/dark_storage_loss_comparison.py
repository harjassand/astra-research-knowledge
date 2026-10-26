#!/usr/bin/env python3
"""Loss-inclusive local dark-storage variant of the finite-time photon phase gate.
A second localized storage oscillator takes the photon off the radiatively
coupled boundary emitter during the conditional phase. All instantaneous
one-body Hamiltonians are positive: capture h>=0; swap block [[J+1,J],[J,J+1]]>=I;
hold e,d onsite 1 and 1+U r; ordinary gapless lead remains.
"""
import json,math
from pathlib import Path
import numpy as np
from scipy.linalg import expm,eigh_tridiagonal
from scipy.optimize import brentq
from scipy.integrate import quad
OUT=Path(__file__).resolve().parent
N=90;g=.7;J=10.;U=1.;tau=math.pi/(2*J);holdtime=math.pi/U
lead=np.diag(np.ones(N-1))+np.diag(.5*np.ones(N-2),1)+np.diag(.5*np.ones(N-2),-1)
le,lv=eigh_tridiagonal(np.ones(N-1),.5*np.ones(N-2))
e,v=eigh_tridiagonal(np.ones(N),np.r_[g,.5*np.ones(N-2)])
a=lambda t:float(np.dot(v[0]**2,np.cos((e-1)*t)))
T=brentq(a,2.43388605,2.433886053)
Ucap=(v*np.exp(-1j*e*T))@v.T
initial=Ucap.conj().T[:,0].copy();initial[17:]=0;initial/=np.linalg.norm(initial)
# The input is only supported on lead sites 1..16; extra storage orbital 90 empty.
Icapture=quad(lambda t:a(t)**2,0,T,epsabs=1e-13)[0]
Ie=2*Icapture+math.pi/(2*J)
Id=math.pi/U+math.pi/(2*J)

def process(kappa_e,kappa_d,r):
    # Matrix-time ordering as controlled finite stages; environmental emission
    # is retained by the norm deficit of the no-jump trajectory.
    h=np.diag(np.ones(N))+np.diag(np.r_[g,.5*np.ones(N-2)],1)+np.diag(np.r_[g,.5*np.ones(N-2)],-1)
    proj=np.zeros((N,N),complex);proj[0,0]=1
    Ucap_eff=expm((-1j*h-kappa_e/2*proj)*T)
    D_swap=np.array([[J+1.,J],[J,J+1.]],complex)
    D_eff=expm((-1j*D_swap-.5*np.diag([kappa_e,kappa_d]))*tau)
    Lswap=(lv*np.exp(-1j*le*tau))@lv.T
    Lhold=(lv*np.exp(-1j*le*holdtime))@lv.T
    v0=Ucap_eff@initial
    total=np.r_[v0,0j]
    def swap(t):
        z=t.copy();z[np.r_[0,N]]=D_eff@t[np.r_[0,N]]
        z[1:N]=Lswap@t[1:N]
        return z
    total=swap(total)
    total[0]*=np.exp((-1j-kappa_e/2)*holdtime)
    total[N]*=np.exp((-1j*(1+U*r)-kappa_d/2)*holdtime)
    total[1:N]=Lhold@total[1:N]
    total=swap(total)
    total[:N]=Ucap_eff@total[:N]
    total[N]*=np.exp((-1j-kappa_d/2)*T)
    return total

ideal0=process(0,0,0)
ideal1=process(0,0,1)
ideal_error=float(np.linalg.norm(ideal1+ideal0))
assert ideal_error<1e-9
scans=[]
for ke,kd in [(0.,0.),(1e-6,0.),(1e-5,0.),(2e-5,0.),(2e-5,1e-6),(2e-5,1e-5),(5e-5,1e-6)]:
    v0=process(ke,kd,0);v1=process(ke,kd,1)
    row={'emitter_decay_rate_over_B':ke,'storage_decay_rate_over_B':kd,
         'leading_loss_only_error_estimate':math.sqrt(ke*Ie+kd*Id)}
    for r,z in ((0,v0),(1,v1)):
        target=ideal0 if r==0 else -ideal0
        # Full environment output error squared = 2 -2Re overlap of
        # target with no-jump component; jump wavefunctions orthogonal.
        err=math.sqrt(max(0,2-2*np.vdot(target,z).real))
        row[f'root{r}_full_environment_state_error']=err
        row[f'root{r}_probability_emitted_to_unwanted_bath']=1-float(np.linalg.norm(z)**2)
    scans.append(row)

out={'model':'positive Jacobi boundary plus local dark storage oscillator, root-conditioned onsite U on dark store',
     'capture_time':T,'capture_each_emitter_population_integral':Icapture,
     'local_swap_strength_J_over_B':J,'maximum_swap_onsite_energy_over_B':J+1,
     'root_conditional_interaction_U_over_B':U,'local_swap_time_each_B_inverse':tau,
     'conditional_hold_duration_B_inverse':holdtime,
     'emitter_integrated_population_exact_lossless':Ie,
     'dark_storage_integrated_population_exact_lossless':Id,
     'previous_direct_hold_emitter_exposure':2*Icapture+math.pi,
     'lossless_selected_plus_unselected_photon_error':ideal_error,
     'scans':scans,
     'positive_hamiltonian_stages':['capture half-line Schur margin 0.02',
         'swap emitter/storage pair eigenvalues 1 and 21',
         'hold isolated emitter=1 and storage onsite >=1; lead >=0',
         'all energies nonnegative in every photon Fock sector'],
     'limitations':['Independent Markovian emitter/storage channels effective, not microscopic positive-frequency completion',
         'Two more actively switched hopping edges are required: emitter-to-lead and emitter-to-store',
         'Photon source shape and lossless flag computation are external resources',
         'This is conventional auxiliary dark-memory architecture, not historical novelty']}
(OUT/'dark_storage_loss_results.json').write_text(json.dumps(out,indent=2))
print('photon capture',T,'exposures e',Ie,'d',Id,'direct hold e',2*Icapture+math.pi,'idealerror',ideal_error)
for x in scans:print(x)
