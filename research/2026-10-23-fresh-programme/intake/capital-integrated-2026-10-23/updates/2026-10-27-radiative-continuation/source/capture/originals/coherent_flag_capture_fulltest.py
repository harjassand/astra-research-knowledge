#!/usr/bin/env python3
"""Independent full memory/reference/photon register coherent evolution.
Uses the actual two-local four-pulse conditional-AND gadget, an exact finite
Jacobi one-photon Hamiltonian, a finite-support time-reversed input and a
locally gated phase hold. No reliance on ideal stationary scattering.
"""
import json, math
from pathlib import Path
import numpy as np
from scipy.linalg import expm, eigh_tridiagonal
from scipy.optimize import brentq
from scipy.integrate import solve_ivp
OUT=Path(__file__).resolve().parent
m=4;nreg=2*m-1;nmode=100;nref=3; g=.7
n=np.diag([0.,1.]);I=np.eye(2);X=np.array([[0,1],[1,0]])
k3=lambda A,B,C:np.kron(np.kron(A,B),C)
# Stage Hamiltonians: exactly 2-local positive, with eigenvalues 0,2.
hMinus=k3(I,n,I-X);hA=k3(n,I,I-np.diag([1,-1]));hPlus=k3(I,n,I+X)
stages=[(hMinus,math.pi/4),(hA,math.pi/2),(hPlus,math.pi/4),(hA,math.pi/2)]
for H,_ in stages:assert np.min(np.linalg.eigvalsh(H))>-1e-12

def gadget(delta):
    u=np.eye(8,dtype=complex)
    for h,t in stages:u=expm(-1j*(1+delta)*t*h)@u
    return u

gates=[(0,1,4),(2,3,5),(4,5,6)]
root=6

def gate3(state,u,abc):
    shape=state.shape[1:]
    tensor=state.reshape((2,)*nreg+shape)
    axes=list(abc)+[j for j in range(nreg) if j not in abc]+list(range(nreg,nreg+len(shape)))
    trans=tensor.transpose(axes)
    out=(u@trans.reshape(8,-1)).reshape((2,)*nreg+shape)
    return out.transpose(np.argsort(axes)).reshape(state.shape)

def compute(state,u,adjoint=False):
    seq=gates[::-1] if adjoint else gates
    for trip in seq:state=gate3(state,u.conj().T if adjoint else u,trip)
    return state

d=np.ones(nmode);off=.5*np.ones(nmode-1);off[0]=g
E,V=eigh_tridiagonal(d,off)
a=lambda t:float(np.sum((V[0]**2)*np.cos((E-1)*t)))
T=brentq(a,2.43388605,2.433886053)
U=(V*np.exp(-1j*E*T))@V.T
Uback=U.conj().T
# Analytic input time reverse from emitter, cut to first 16 lead sites.
phi0=Uback[:,0]
assert abs(phi0[0])<1e-10
L=16
phi=phi0.copy();phi[L+1:]=0;phi/=np.linalg.norm(phi)
loaded=U@phi
eta=float(np.linalg.norm(loaded[1:])**2)
# Common root=0 trajectory and conditional root=1 trajectory.
eL,vL=eigh_tridiagonal(d[1:],off[1:])
Ulead=(vL*np.exp(-1j*eL*math.pi))@vL.T

def hold1(psi,root):
    out=psi.copy()
    out[0]*=np.exp(-1j*math.pi*(1+root))
    out[1:]=Ulead@psi[1:]
    return out

out0=U@hold1(loaded,0)
out1=U@hold1(loaded,1)
assert abs(np.linalg.norm(out1+out0)-2*math.sqrt(eta))<1e-10
rng=np.random.default_rng(812022)
logical=rng.normal(size=(2**m,nref))+1j*rng.normal(size=(2**m,nref))
logical[-1]*=2.5
logical/=np.linalg.norm(logical)

def propagate(delta):
    gate=gadget(delta)
    state=np.zeros((2**nreg,nref,nmode),complex)
    ideal=np.zeros_like(state)
    for word in range(2**m):
        idx=word<<(nreg-m)
        state[idx]=logical[word,:,None]*phi[None,:]
        sign=-1 if word==2**m-1 else 1
        ideal[idx]=sign*logical[word,:,None]*out0[None,:]
    # Compute + transit are allowed to overlap: their Hamiltonians commute
    state=compute(state,gate)
    state=state@U.T
    # Hold: photon boundary is isolated and gains local root-dependent phase;
    # all residual lead branches remain present and evolve exactly.
    state[:,:,1:]=state[:,:,1:]@Ulead.T
    r=((np.arange(2**nreg)>>(nreg-1-root))&1)
    state[:,:,0]*=np.exp(-1j*math.pi*(1+r))[:,None]
    # Uncompute + release commute and can overlap.
    state=state@U.T
    state=compute(state,gate,adjoint=True)
    err=float(np.linalg.norm(state-ideal))
    # Independent computation of the logical root mistakes.
    wrong=[]
    for word in range(2**m):
        v=np.zeros((2**nreg,1,1),complex)
        v[word<<(nreg-m),0,0]=1
        v=compute(v,gate)
        f=int(word==2**m-1)
        bad=(r!=f)
        wrong.append(float(np.linalg.norm(v[bad])**2))
    rooterr=2*math.sqrt(float(np.sum(abs(logical)**2* np.asarray(wrong)[:,None])))
    bound=2*math.sqrt(eta)+rooterr
    assert err<=bound+1e-9,(err,bound)
    return {'relative_calibration_error':delta,'full_memory_reference_photon_error':err,
            'root_error_exact_ideal_photon':rooterr,
            'coherent_composition_bound':bound,
            'worst_root_wrong_probability':max(wrong),
            'photon_probability_after_full':float(np.linalg.norm(state)**2),
            'decoded_bad_flag_probability':float(sum(np.linalg.norm(state[k])**2 for k in range(2**nreg) if k%(2**(nreg-m))!=0))}

runs=[propagate(delta) for delta in (0.,.0001,.0003,.001)]
# Off-ramp and capture-time jitter are tested independently in the full one-photon
# matrix, not inserted artificially as amplitude noise.
def leakage_with_offramp(jitter,ramp_duration):
    # h_on acts through an extra jitter; off ramp g(u)=g*(1-u/tau), onsite stays 1.
    start=(V*np.exp(-1j*E*(T+jitter)))@V.T@phi
    if ramp_duration>0:
        def rhs(t,y):
            v=y.view(np.complex128)
            z= d.astype(complex)*v
            strength=g*max(0,1-t/ramp_duration)
            z[0]+=strength*v[1];z[1]+=strength*v[0]
            z[1:-1]+=.5*v[2:];z[2:]+=.5*v[1:-1]
            return -1j*z
        sol=solve_ivp(rhs,[0,ramp_duration],start,rtol=2e-11,atol=2e-13)
        assert sol.success
        end=sol.y[:,-1]
    else:end=start
    eta_actual=float(np.linalg.norm(end[1:]))
    analytical_upper=math.sqrt(eta)+g*abs(jitter)+g*ramp_duration/2
    assert eta_actual<=analytical_upper+1e-9
    return {'capture_timing_error_B_inverse':jitter,
            'linear_off_ramp_duration_B_inverse':ramp_duration,
            'actual_full_state_sign_error':2*eta_actual,
            'analytic_sign_error_upper':2*analytical_upper}
robust=[leakage_with_offramp(dt,ds) for dt,ds in ((0.,0.),(.001,0.),(0.,.002),(.001,.002),(.003,.005))]
# Time overlap: per-depth flag compute 3*pi/2, capture 2.433...
# both can run simultaneously whenever the root-photon phase is OFF.
depth=math.ceil(math.log2(m));tflag=1.5*math.pi*depth
assert tflag>T
out={'model':'Jacobi g=0.7, bulk 0.5, onsite 1; branch-off during transport; one root-conditioned hold with +1 energy',
     'memory_size':m,'auxiliary_registers':m-1,'reference_dim':nref,
     'initial_photon_source_sites':L,'photon_modes_for_validation':nmode,
     'certified_capture_time_diagnostic':T,
     'capture_photon_leak_norm':math.sqrt(eta),
     'ideal_full_protocol_duration_sequential':2*tflag+2*T+math.pi,
     'ideal_full_protocol_duration_overlap':2*max(tflag,T)+math.pi,
     'flag_pulse_time_per_depth_single_pass':1.5*math.pi,
     'coherent_runs':runs,
     'timing_and_off_ramp_audit':robust,
     'caveats':['The two-local control pulses are exact ideal Hamiltonian propagators and the decoder is the exact adjoint of the actual encoder',
                'The internal photon transfer is controlled by bond modulation, requiring an actual finite switching interface',
                'The photon input mode is supplied as an explicit prepared resource, not manufactured by the Hamiltonian',
                'Full unitary bosonic dynamics is tested in the single-photon sector; multi-photon operator positivity follows separately',
                'No independent radiation, hardware dephasing or control work statistics']}
(OUT/'coherent_flag_capture_fulltest_results.json').write_text(json.dumps(out,indent=2))
print('capture t',T,'L',L,'leak',math.sqrt(eta),'total parallel',out['ideal_full_protocol_duration_overlap'])
for z in runs:print('delta',z['relative_calibration_error'],'joint coherent err',z['full_memory_reference_photon_error'],'root-only',z['root_error_exact_ideal_photon'],'bound',z['coherent_composition_bound'])
for z in robust: print('timing',z)
