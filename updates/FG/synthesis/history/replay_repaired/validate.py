"""Algebra, resource, and finite-duration reference checks. No experimental data."""
import json,itertools,math,time
from pathlib import Path
import numpy as np
from scipy.linalg import expm
from scipy import constants as c
from rotor_exact import build_model,signal,free,theta_from_fluence,pulse_parts,fourier_map
from rotor_probe import rotor_blocks,NU,B,sigma_t,d

rng=np.random.default_rng(721104)
report={'status':'theoretical checks; no laboratory validation'}

def pair(z): return [float(np.real(z)),float(np.imag(z))]

def split_unitary(U,ng):
    n=len(U);p={m:np.zeros((n,n),complex) for m in (-1,0,1)}
    p[0][:ng,:ng]=U[:ng,:ng];p[0][ng:,ng:]=U[ng:,ng:]
    p[1][ng:,:ng]=U[ng:,:ng];p[-1][:ng,ng:]=U[:ng,ng:]
    return p

# Strong pulses, multiple states in each band, mixed preparation.
ng=3;ne=2;n=ng+ne
parts=[]
for j in range(4):
    a=rng.normal(size=(n,n))+1j*rng.normal(size=(n,n))
    h=(a+a.conj().T)/3
    parts.append(split_unitary(expm(-1j*h),ng))
rho=np.diag([.2,.3,.5,0,0]).astype(complex)
ell=[-1,1,1,-1];s=.702;a=s/2

def calc(q2):
    K=fourier_map(rho,parts[0],-1,1,s)
    K=fourier_map(K,parts[1],1,q2,s)
    K=fourier_map(K,parts[2],1,1,s)
    return np.trace(fourier_map(K,parts[3],-1,1,s))
Sp,Sm,S0=calc(1),calc(-1),calc(0)
XL=(np.exp(1j*a)*Sp-np.exp(-1j*a)*Sm)/(2j*np.sin(s))
XR=(-np.exp(-1j*a)*Sp+np.exp(1j*a)*Sm)/(2j*np.sin(s))
K1=fourier_map(rho,parts[0],-1,1,s)
Ks=[parts[1][1]@K1@parts[1][0].conj().T,
    parts[1][0]@K1@parts[1][-1].conj().T]
# The second-pulse contributions land in E-E and G-G respectively.
assert np.linalg.norm(Ks[0][:ng,:])+np.linalg.norm(Ks[0][:,:ng])<1e-12
assert np.linalg.norm(Ks[1][ng:,:])+np.linalg.norm(Ks[1][:,ng:])<1e-12
truth=[]
for K in Ks:
    truth.append(np.trace(fourier_map(fourier_map(K,parts[2],1,1,s),parts[3],-1,1,s)))
assert np.max(abs(np.array([XL,XR])-truth))<1e-12
assert abs(Sp+Sm-2*np.cos(a)*S0)<1e-12
# Actual 5x5x5 phase cycling of full unitaries, including strong pulse terms.
coeff=0j
for phis in itertools.product(2*np.pi*np.arange(5)/5,repeat=3):
    K=rho.copy()
    phases=list(phis)+[0.]
    for j,phi in enumerate(phases):
        UA=sum(np.exp(1j*m*(phi+a))*parts[j][m] for m in (-1,0,1))
        UB=sum(np.exp(1j*m*(phi-a))*parts[j][m] for m in (-1,0,1))
        K=UA@K@UB.conj().T
    coeff+=np.trace(K)*np.exp(-1j*np.dot(ell,phases))/125
assert abs(coeff-Sp)<1e-12
report['multilevel_strong_pulse']={'inversion_error':float(np.max(abs(np.array([XL,XR])-truth))),
 'phase_cycle_error':float(abs(coeff-Sp)),'zero_port_residual':float(abs(Sp+Sm-2*np.cos(a)*S0)),
 'condition_number':float(1/np.tan(a)),'XL':pair(XL),'XR':pair(XR)}

# Ancilla parking: original optical +/- labels -> ground Zeeman states.
plus=np.array([1,1,0])/np.sqrt(2);minus=np.array([1,-1,0])/np.sqrt(2)
unused=np.array([0,0,1.])
W=np.outer([1,0,0],plus)+np.outer([0,0,1],minus)+np.outer([0,1,0],unused)
assert np.linalg.norm(W.conj().T@W-np.eye(3))<1e-12
for phase in np.linspace(-20,20,41):
    Uir=np.diag([np.exp(-1j*.31),np.exp(-1j*phase),np.exp(-1j*.31)])
    for v in [plus,minus]:
        assert np.linalg.norm(W.conj().T@Uir@W@v-np.exp(-1j*.31)*v)<1e-12
report['ground_parking']='scalar atomic Stark phase cancels for arbitrary optical S-D differential phase; transfer errors not simulated'

# Tr of an arbitrary cross-block is conserved by a common trace-preserving channel.
K=rng.normal(size=(2,2))+1j*rng.normal(size=(2,2));p=.73
E0=np.diag([1,np.sqrt(1-p)]);E1=np.array([[0,np.sqrt(p)],[0,0]])
assert abs(np.trace(E0@K@E0.T+E1@K@E1.T)-np.trace(K))<1e-12
report['common_relaxation_trace_test']='passed; branch-dependent photon recoil is excluded from this common-channel identity'

# Physically linked inputs and cost arithmetic.
w0=2*np.pi*c.c*100*NU
Arad=w0**3*d*d/(3*np.pi*c.epsilon_0*c.hbar*c.c**3)
thcm=c.k*300/(c.h*c.c*100)
ground_vib=(1-np.exp(-747.4/thcm))*(1-np.exp(-481.2/thcm))**2*(1-np.exp(-3949.9/thcm))
alphaS=75.46*c.physical_constants['atomic unit of electric polarizability'][0]
k=w0/c.c;F=1100.
ray_cs=k**4*alphaS**2/(6*np.pi*c.epsilon_0**2)
report['derived_scales']={
 'thermal_energy_cm':thcm,'harmonic_thermal_all_modes_ground_probability':ground_vib,
 'dipole_C_m':d,'radiative_A_s_inverse':Arad,'radiative_lifetime_ms':1000/Arad,
 'grating_pitch_um':(1/(NU*100))/.9*1e6,'s':s,'eta_after_angular_dispersion':.027,
 'theta_F011_Jcm2':theta_from_fluence(1100),'theta_F00275_Jcm2':theta_from_fluence(275),
 'max_finite_packet_fourpulse_attenuation':float(np.exp(-.5*.027**2*16)),
 'static_alphaS_common_phase_rad_F011':float(alphaS*F/(2*c.epsilon_0*c.c*c.hbar)),
 'static_alphaS_Rayleigh_photons_F011':float(ray_cs*F/(c.hbar*w0)),
 'added_20us_reference_delay_factor':float(np.exp(-20e-6/.92e-3)),
 '20um_waist_energy_per_F011_pulse_uJ':float(F*np.pi*(20e-6)**2/2*1e6),
 '20um_waist_total_energy_four_F011_pulses_uJ':float(4*F*np.pi*(20e-6)**2/2*1e6)}
# Independent samples; normalized complex Fourier coefficient; conservative 5-sigma bound.
report['costs']=[]
for X in [.00036,.0018,.0077,.01,.03]:
    N=100/(.4**2*np.sin(s)**2*X**2)
    report['costs'].append({'X':X,'C_assumed':.4,'N_conservative':N,'hours_at_ASSUMED_50_trials_per_second':N/50/3600,
                          'p_loss_for_90pct_survival_one_molecule':-np.log(.9)/N})

# Convergence checks of the finite-duration two-band rotor reference.
conv=[]
for jmax,steps in [(60,160),(70,200),(70,400),(80,200)]:
    model,ps=build_model(jmax=jmax,steps=steps)
    S,X=signal(model)
    conv.append(dict(Jmax=jmax,steps=steps,single_pulse_excitation_reference=ps,XL=pair(X[0]),XR=pair(X[1])))
report['rotor_convergence']=conv
x200=np.array(conv[1]['XL']);x400=np.array(conv[2]['XL']);x80=np.array(conv[3]['XL'])
report['rotor_convergence_summary']={'relative_step_refinement_error':float(np.linalg.norm(x400-x200)/np.linalg.norm(x400)),
 'relative_J70_J80_difference':float(np.linalg.norm(x80-x200)/np.linalg.norm(x80))}
assert report['rotor_convergence_summary']['relative_step_refinement_error']<.005
assert report['rotor_convergence_summary']['relative_J70_J80_difference']<.005
Path('validation_results.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
