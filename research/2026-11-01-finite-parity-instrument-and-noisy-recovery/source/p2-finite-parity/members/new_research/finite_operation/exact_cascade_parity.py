"""Finite-strength, finite-window parity emission by two conditional drives.

This is the root's two-mode inverse-design construction, implemented and
checked here. It retains every outlet and terminal oscillator. Main results
are analytic conditional coherent-state solutions, not Fock truncations.

Physical model (one ideal unidirectional cascade):
 b' = -ae b - i u(t) Z2
 c' = -(ac+i chi Z1)c - sqrt(ke kc)b - i w(t) Z2
 L_main = sqrt(ke)b+sqrt(kc)c,
 L_bypass=sqrt(kb)b, L_internal=sqrt(ki)c.
 ae=(ke+kb)/2, ac=(kc+ki)/2.

Choose a real target A with A,A',A'' zero at endpoints, and set
 B=-(A'+ac A)/chi,
 u=-(B'+ae B)/sqrt(ke),
 w=(B'-(kc-ac)B-chi A)/sqrt(kc).
 Then b=iB Z2/sqrt(ke), c=(A Z1 Z2-iB Z2)/sqrt(kc), so
 L_main(t)=A(t) Z1 Z2 exactly throughout the finite operation.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, asdict
from pathlib import Path
import numpy as np
from scipy.integrate import simpson, solve_ivp
from scipy.special import ndtri, ndtr


@dataclass
class Model:
    T: float = 8.0
    ke: float = 1.0
    kc: float = 10.0
    kb: float = 0.0
    ki: float = 0.0
    chi: float = 5.0
    eta: float = 0.5
    assignment_error: float = 1e-3
    photons: float | None = None

    @property
    def N(self):
        if self.photons is not None:
            return self.photons
        return ndtri(self.assignment_error)**2/(4*self.eta)


def waveforms(m: Model, t):
    t = np.asarray(t)
    k=np.pi/m.T
    a0=np.sqrt(m.N*128/(35*m.T))
    ss,cc=np.sin(k*t),np.cos(k*t)
    A=a0*ss**4
    dA=4*a0*k*ss**3*cc
    ddA=4*a0*k*k*(3*ss**2*cc**2-ss**4)
    ae=(m.ke+m.kb)/2
    ac=(m.kc+m.ki)/2
    B=-(dA+ac*A)/m.chi
    dB=-(ddA+ac*dA)/m.chi
    u=-(dB+ae*B)/np.sqrt(m.ke)
    w=(dB-(m.kc-ac)*B-m.chi*A)/np.sqrt(m.kc)
    b=1j*B/np.sqrt(m.ke)
    # Representative ++ branch; -- has conjugate c, -b.
    c=(A-1j*B)/np.sqrt(m.kc)
    return dict(A=A,dA=dA,ddA=ddA,B=B,dB=dB,u=u,w=w,b=b,c=c)


def solve(m: Model, samples=12001):
    t=np.linspace(0,m.T,samples)
    f=waveforms(m,t)
    I=lambda v: float(simpson(v,x=t))
    N=I(f['A']**2)
    NB=I(f['B']**2)
    C=I(f['A']*f['B'])
    phase=-I(f['w']*f['A']/np.sqrt(m.kc))
    ri2=m.ki/m.kc
    D=(m.kb/m.ke+ri2)*NB
    r={
        'model':asdict(m),'target_photons_N':N,'source_output_photons_NB':NB,
        'AB_integral_C':C,'dynamical_local_z1_phase':phase,
        'same_sector_correcting_z1_phase':phase-ri2*C,
        'assignment_error':float(ndtr(-2*np.sqrt(m.eta*N))),
        'same_sector_dephasing_D':D,
        'same_sector_coherence_after_local_correction':float(np.exp(-2*D)),
        'same_sector_phase_flip_probability':float(-np.expm1(-2*D)/2),
        'peak_source_drive_u':float(np.max(abs(f['u']))),
        'peak_corrector_drive_w':float(np.max(abs(f['w']))),
        'source_drive_squared_action':I(f['u']**2),
        'corrector_drive_squared_action':I(f['w']**2),
        'peak_source_photons':float(np.max(abs(f['b'])**2)),
        'peak_corrector_photons':float(np.max(abs(f['c'])**2)),
        'source_photon_exposure':NB/m.ke,
        'corrector_photon_exposure':(N+NB)/m.kc,
        'source_bypass_emitted_photons':m.kb/m.ke*NB,
        'corrector_internal_emitted_photons':m.ki/m.kc*(N+NB),
        'terminal_oscillator_photons':float(abs(f['b'][-1])**2+abs(f['c'][-1])**2),
        'start_drive_u':float(f['u'][0]),'end_drive_u':float(f['u'][-1]),
        'start_drive_w':float(f['w'][0]),'end_drive_w':float(f['w'][-1]),
        'analytic_NB':m.N*((m.kc+m.ki)**2/4+16*np.pi**2/(7*m.T**2))/m.chi**2,
    }
    return r,t,f


Z1=np.array([1,1,-1,-1])
Z2=np.array([1,-1,1,-1])
S=Z1*Z2


def instrument_gram(result, reported_parity=1, correct_local_phase=True):
    """Exact 4x4 Schur matrix for each coarse homodyne instrument outcome.

    The main output has a real ±A waveform, so its measurement has no
    stochastic within-sector phase. The optional single-qubit Z1 correction
    removes the deterministic dynamical and hidden-output same-sector phase.
    Internal and bypass ports remain unobserved. Initial state is vacuum.
    """
    m=result['model']; N=result['target_photons_N']; NB=result['source_output_photons_NB']
    C=result['AB_integral_C']; eta=m['eta']; ri2=m['ki']/m['kc']; rb2=m['kb']/m['ke']
    phi=result['dynamical_local_z1_phase']
    if correct_local_phase:
        phi-=result['same_sector_correcting_z1_phase']
    out=np.zeros((4,4),complex)
    for i in range(4):
        for j in range(4):
            collected_overlap=np.exp(-eta*(S[i]-S[j])**2*N/2)
            region=ndtr(reported_parity*(S[i]+S[j])*np.sqrt(eta*N))
            expo=-(1-eta+ri2)*(S[i]-S[j])**2*N/2-(rb2+ri2)*(Z2[i]-Z2[j])**2*NB/2
            expo+=1j*(phi*(Z1[i]-Z1[j])+ri2*C*(S[i]*Z2[j]-S[j]*Z2[i]))
            out[i,j]=collected_overlap*region*np.exp(expo)
    return out


def checks(result):
    P,M=[instrument_gram(result,s) for s in (1,-1)]
    return {
        'min_eigenvalue_positive_outcome':float(np.linalg.eigvalsh(P).min()),
        'min_eigenvalue_negative_outcome':float(np.linalg.eigvalsh(M).min()),
        'trace_preservation_error':float(np.max(abs(np.diag(P+M)-1))),
        'positive_assignment_error':float(1-P[0,0].real),
        'negative_assignment_error':float(1-M[1,1].real),
        'NB_analytic_error':abs(result['source_output_photons_NB']-result['analytic_NB']),
    }


def check_classical_ode(m: Model):
    """Independent ODE integration versus the inverse-designed trajectories."""
    def rhs(t,v):
        f=waveforms(m,t)
        b,c=v
        return np.array([-(m.ke+m.kb)*b/2-1j*f['u'],
                         -((m.kc+m.ki)/2+1j*m.chi)*c-np.sqrt(m.ke*m.kc)*b-1j*f['w']])
    t=np.linspace(0,m.T,2001)
    sol=solve_ivp(rhs,[0,m.T],np.zeros(2,complex),t_eval=t,method='DOP853',rtol=2e-12,atol=2e-13)
    f=waveforms(m,t)
    output=np.sqrt(m.ke)*sol.y[0]+np.sqrt(m.kc)*sol.y[1]
    return {
        'max_source_amplitude_error':float(np.max(abs(sol.y[0]-f['b']))),
        'max_corrector_amplitude_error':float(np.max(abs(sol.y[1]-f['c']))),
        'max_main_field_error':float(np.max(abs(output-f['A']))),
        'terminal_photons_from_ode':float(np.sum(abs(sol.y[:,-1])**2)),
        'solver_success':bool(sol.success),
    }


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',default=str(Path(__file__).with_name('exact_cascade_results.json')))
    args=parser.parse_args()
    cases=[]
    for T in (2,4,8,16):
        for loss in (0.,1e-5,1e-4,1e-3):
            m=Model(T=T,kb=loss,ki=10*loss)
            r,_,_=solve(m)
            r['checks']=checks(r)
            cases.append(r)
            print(f"T={T:2}, loss={loss:.0e}: pZ={r['same_sector_phase_flip_probability']:.7g}, "
                  f"u={r['peak_source_drive_u']:.5g}, w={r['peak_corrector_drive_w']:.5g}, "
                  f"n_b={r['peak_source_photons']:.5g}, n_c={r['peak_corrector_photons']:.5g}")
    ode_checks=[]
    for loss in (0.,1e-3):
        m=Model(T=4,kb=loss,ki=10*loss)
        ode_checks.append({'model':asdict(m),**check_classical_ode(m)})
    Path(args.output).write_text(json.dumps({'cases':cases,'independent_ode_checks':ode_checks},indent=2))


if __name__=='__main__':
    main()
