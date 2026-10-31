"""Native two-photon checker with always-on dispersive coupling.

Exact +G,-G,+G common BS calibration, full N=2 x {g,f} six-dimensional
no-jump propagator, loss derivatives, phase randomization and opposite-pass
echo. C maps, helper phases and middle-frame conventions are explicit.
"""
from pathlib import Path
import json
import numpy as np
from scipy.linalg import expm,norm

ROOT=Path(__file__).resolve().parent
I3=np.eye(3);I2=np.eye(2)
Jx=np.array([[0,1,0],[1,0,1],[0,1,0]],complex)/np.sqrt(2)
Jy=np.array([[0,-1j,0],[1j,0,-1j],[0,1j,0]],complex)/np.sqrt(2)
Jz=np.diag([1.,0.,-1.]);n=I3+Jz;nb=2*I3-n
Pf=np.diag([0.,1.]);plus=np.array([1.,1.])/np.sqrt(2)
v=np.column_stack([np.array([0,1,0]),np.array([1,0,1])/np.sqrt(2)]).astype(complex)
qv=np.array([1,0,-1],complex)/np.sqrt(2)
P=v@v.conj().T;Q=I3-P
D=np.diag([1.,-1.,1.])
X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]],complex);Z=np.diag([1.,-1.])
target=-1j*X

def parameters(G,chi=1.,angle=np.pi/2):
    assert abs(angle-np.pi/2)<1e-14
    d=chi/2;r=np.hypot(G,d);s=G/r;c=d/r;k=c*c-s*s
    sb=1/(2*np.sqrt(2)*s)
    if sb>1+1e-12:raise ValueError('G must be at least chi/(2sqrt7)')
    sb=min(1.,sb);beta=np.pi-np.arcsin(sb);cb=np.cos(beta)
    w=-1/np.sqrt(2);rhs=-(1-k)*sb;den=cb*cb+k*k*sb*sb
    ca=(cb*w+k*sb*rhs)/den;sa=(-k*sb*w+cb*rhs)/den
    a=np.arctan2(sa,ca)%(2*np.pi)
    return dict(G=G,chi=chi,d=d,r=r,outer_duration=a/r,middle_duration=2*beta/r,
                total_BS_duration=(2*a+2*beta)/r,C_duration=np.pi/chi)

def checker(G,kappas=(0.,0.),helper_gamma=0.,sign=1.,chi_error=0.,
            amplitude_error=0.,pump_phase_error=0.,read_phase_error=0.,return_schedule=False):
    par=parameters(G);a=par['outer_duration'];b=par['middle_duration'];tc=par['C_duration']
    chi=1+chi_error;d=.5
    bsaxis=np.cos(pump_phase_error)*Jx+np.sin(pump_phase_error)*Jy
    hc=chi*np.kron(n,Pf)
    hb0=hc-d*np.kron(Jz,I2)
    schedule=[(hc,tc),(hb0+sign*G*(1+amplitude_error)*np.kron(bsaxis,I2),a),
              (hb0-sign*G*(1+amplitude_error)*np.kron(bsaxis,I2),b),
              (hb0+sign*G*(1+amplitude_error)*np.kron(bsaxis,I2),a),(hc,tc)]
    rr=np.asarray(kappas)
    if rr.shape==(2,):rr=np.tile(rr,(5,1))
    U=np.eye(6,dtype=complex)
    for (H,t),kk in zip(schedule,rr):
        gam=np.kron(kk[0]*n+kk[1]*nb,I2)+helper_gamma*np.kron(I3,Pf)
        U=expm((-1j*H-gam/2)*t)@U
    # Nominal chi*N/2 phase, with N=2, is paid as a helper read-frame phase.
    phase=np.exp(1j*(par['total_BS_duration']+read_phase_error))
    km=np.kron(I3,np.array([1,-phase])[None,:]/np.sqrt(2))@U@np.kron(I3,plus[:,None])
    kp=np.kron(I3,np.array([1,+phase])[None,:]/np.sqrt(2))@U@np.kron(I3,plus[:,None])
    if return_schedule:return km,kp,par,schedule
    return km,kp,par

def coeffs(k):
    rel=target.conj().T@k
    return np.array([np.trace(pa@rel)/2 for pa in [I2,X,Y,Z]])

def encode_complex(xs):
    return [[float(z.real),float(z.imag)] for z in np.asarray(xs).flat]

def loss_kernel(G,weights=(1.,1.,1.)):
    # Pointwise first-order Jz no-jump insertion in the middle pulse.
    par=parameters(G);d=.5
    schedule=[(G,par['outer_duration']),(-G,par['middle_duration']),(G,par['outer_duration'])]
    U=np.eye(3,dtype=complex);time=0.;samples=[]
    for g,t in schedule:
        H=g*Jx-d*Jz
        for x in np.linspace(0,t,121,endpoint=False):
            ut=expm(-1j*H*x)@U
            r=ut.conj().T@Jz@ut
            vx=float(np.trace(Jx@r).real/2)
            samples.append((time+x,vx))
        U=expm(-1j*H*t)@U;time+=t
    samples.append((time,float(np.trace(Jx@U.conj().T@Jz@U).real/2)))
    # Exact integral via block exponentiation, independent of sampling.
    integ=np.zeros((3,3),complex);U=np.eye(3,dtype=complex)
    for (g,t),weight in zip(schedule,weights):
        H=g*Jx-d*Jz
        # derivative of exp[(-i H + eps Jz)t] at eps=0.
        z=np.zeros((3,3),complex);B=np.block([[-1j*H,Jz],[z,-1j*H]])
        eb=expm(B*t);piece=eb[:3,:3].conj().T@eb[:3,3:]
        integ+=weight*(U.conj().T@piece@U)
        U=expm(-1j*H*t)@U
    intvx=float(np.trace(Jx@integ).real/2)
    intvy=float(np.trace(Jy@integ).real/2)
    intvz=float(np.trace(Jz@integ).real/2)
    return dict(integral_vx=intvx,integral_vy=intvy,integral_vz=intvz,
                loss_relative_X_coefficient=-intvx/2,
                accepted_Q_coefficient=(np.pi+intvy)/2,
                rejected_Q_coefficient=-(np.pi+intvz)/2,
                sampled_max_abs_vx=max(abs(x[1]) for x in samples),
                arbitrary_time_profile_vx_bound=min(1.,d*par['total_BS_duration']),
                arbitrary_time_profile_code_amplitude_bound_per_max_differential_kappa=d*par['total_BS_duration']**2/4,
                large_drive_scaled_coefficient=(-intvx/2)*G*G)

def main():
    rows=[]
    for G in [.2,.25,.5,1.,2.,5.,10.,20.,50.,100.]:
        km,kp,par=checker(G)
        expected=-1j*Jx
        ideal_err=float(norm(km-expected,2));reject_err=float(norm(kp-Q,2))
        assert ideal_err<3e-13 and reject_err<3e-13
        eps=1e-6
        am,ap,_=checker(G,kappas=(eps,0.))
        total=2*par['C_duration']+par['total_BS_duration']
        ahat=np.exp(eps*total/2)*am
        code=v.conj().T@ahat@v
        derivative=(coeffs(code)-np.array([1.,0,0,0]))/eps
        kern=loss_kernel(G)
        assert abs(derivative[1].real-kern['loss_relative_X_coefficient'])<3e-5
        assert abs(norm(Q@ahat@v,2)/eps-abs(kern['accepted_Q_coefficient']))<3e-5
        rejected_normalized=np.exp(eps*total/2)*ap
        assert abs(norm(Q@rejected_normalized@v,2)/eps-abs(kern['rejected_Q_coefficient']))<3e-5
        row=dict(G_over_chi=G,BS_duration_chi_units=par['total_BS_duration'],
                 complete_C_BS_C_duration_chi_units=total,outer_duration=par['outer_duration'],
                 middle_duration=par['middle_duration'],ideal_accept_error=ideal_err,
                 ideal_reject_error=reject_err,first_order_relative_code_derivative=encode_complex(derivative),
                 accepted_Q_amplitude_per_differential_kappa=float(norm(Q@ahat@v,2)/eps),
                 middle_pulse_loss_kernel=kern)
        rows.append(row)
    cases=[]
    for G in [.5,1.,2.,5.,10.,20.]:
        for e in [1e-4,3e-4,1e-3,3e-3]:
            # Real positive rates: kappa_a=2e, kappa_b=e; difference=e.
            A,B,par=checker(G,kappas=(2*e,e))
            Am,Bm,_=checker(G,kappas=(2*e,e),sign=-1)
            assert norm(Am-D@A@D,2)<2e-13
            t=2*par['C_duration']+par['total_BS_duration']
            s=np.exp(3*e*t/2)
            rel=coeffs(v.conj().T@(s*A)@v)
            raw_traceless=norm(target.conj().T@(v.conj().T@(s*A)@v)-rel[0]*I2,2)
            good=target.conj().T@(v.conj().T@(s*A)@v)
            opposite=target.conj().T@(v.conj().T@(-s*Am)@v)
            ev=(good+opposite)/2;odd=(good-opposite)/2
            # Code-projected channel after discarding phase coin:
            # ev rho ev† + odd rho odd†, ev is scalar in this palindrome model.
            ev_res=norm(ev-np.trace(ev)/2*I2,2)
            echo=s*s*(Am@A)
            ecode=v.conj().T@echo@v
            ecoeff=np.array([np.trace(pa@ecode)/2 for pa in [I2,X,Y,Z]])
            pjump=float(np.linalg.eigvalsh(v.conj().T@(I3-A.conj().T@A-B.conj().T@B)@v)[-1])
            cases.append(dict(G_over_chi=G,kappa_a_over_chi=2*e,kappa_b_over_chi=e,
                duration_single=t,duration_echo=2*t,
                raw_normalized_code_traceless_amplitude=float(raw_traceless),
                discarded_phase_coin_even_nonscalar_residual=float(ev_res),
                phase_randomized_error_subchannel_norm=float(norm(odd,2)**2),
                code_relative_Pauli_weight=float(sum(abs(rel[1:])**2)/sum(abs(rel)**2)),
                accepted_Q_amplitude=float(norm(Q@A@v,2)),
                one_checker_max_photon_loss_probability=pjump,
                echo_normalized_code_traceless_amplitude=float(norm(ecode-ecoeff[0]*I2,2)),
                echo_code_relative_Pauli_weight=float(sum(abs(ecoeff[1:])**2)/sum(abs(ecoeff)**2)),
                echo_final_accepted_Q_amplitude=float(norm(Q@(Am@A)@v,2)),
                reference_idle_pauli_weight_unit_chi_time=e**4/256))
    drift=[]
    for key in ['chi_error','amplitude_error','pump_phase_error']:
        for e in [1e-5,1e-4,1e-3]:
            kw={key:e};A,B,par=checker(5.,**kw);Am,Bm,_=checker(5.,sign=-1,**kw)
            cc=coeffs(v.conj().T@A@v);echo=v.conj().T@(Am@A)@v
            drift.append(dict(parameter=key,error=e,
                phase_covariance_residual=float(norm(Am-D@A@D,2)),
                raw_in_code_traceless=float(norm(target.conj().T@(v.conj().T@A@v)-cc[0]*I2,2)),
                accepted_Q_amplitude=float(norm(Q@A@v,2)),
                opposite_pass_echo_code_traceless=float(norm(echo-np.trace(echo)/2*I2,2))))
    helper=[]
    for gam in [1e-4,1e-3,1e-2]:
        A,B,par=checker(5.,helper_gamma=gam);t=2*par['C_duration']+par['total_BS_duration']
        ac=v.conj().T@A@v;bc=v.conj().T@B@v
        known=.5*(1+np.exp(-gam*t/2));wrong=.5*(1-np.exp(-gam*t/2))
        helper.append(dict(gamma_f_over_chi=gam,duration=t,
            accept_scalar_residual=float(norm(ac-known*target,2)),
            nojump_false_flag_scalar_residual=float(norm(bc-wrong*target,2)),
            any_f_to_e_decay_probability=(1-np.exp(-gam*t))/2,
            pure_helper_dephasing_false_flag_probability=(1-np.exp(-gam*t/2))/2,
            accepted_Q_amplitude=float(norm(Q@A@v,2))))
    # Independent first-order full-operator check for a nonpalindromic loss profile.
    G=5.;eps=1e-7;profile=np.array([2.,7.,3.,11.,5.])
    A,B,par=checker(G,kappas=np.column_stack([eps*profile,np.zeros(5)]))
    A0,B0,_=checker(G)
    durations=np.array([par['C_duration'],par['outer_duration'],par['middle_duration'],par['outer_duration'],par['C_duration']])
    scalar=np.exp(eps*np.dot(profile,durations)/2)
    ker=loss_kernel(G,weights=profile[1:4]);ix=ker['integral_vx'];iy=ker['integral_vy'];iz=ker['integral_vz']
    first=profile[0]*par['C_duration'];last=profile[4]*par['C_duration']
    q0=np.outer(qv,v[:,0].conj());zq=q0.conj().T
    q1=np.outer(qv,v[:,1].conj());oq=q1.conj().T
    dA=1j/2*(ix*P+(iy+last)*q0+(iz+first)*zq)
    dB=-.5*((iz+first)*q1+(iy+last)*oq)
    ares=norm((scalar*A-A0)/eps-dA,2);bres=norm((scalar*B-B0)/eps-dB,2)
    assert ares<5e-5 and bres<5e-5
    profile_validation=dict(relative_rates=profile.tolist(),G_over_chi=G,derivative_epsilon=eps,
        full_accept_first_order_residual=float(ares),full_reject_first_order_residual=float(bres))
    result=dict(model='N=2 data spin1 x helper(g,f); exact six-dimensional no-jump evolution.',
        conventions='Known common mode frame W=exp(-i chi*T_BS*Jz/2) is retained as a frame update; helper read phase compensates nominal chi*T_BS.',
        endpoint_and_derivatives=rows,finite_loss_cases=cases,control_drift=drift,
        helper_faults=helper,arbitrary_time_profile_validation=profile_validation,
        high_drive_limits=dict(BS_duration_times_G=5*np.pi/2-4*np.arcsin(np.sqrt(2)/4),
            negative_loss_X_coefficient_times_G_squared_over_chi=3*np.pi/8+(np.sqrt(7)-1)/4,
            phase_randomized_error_weight_coefficient=(3*np.pi/8+(np.sqrt(7)-1)/4)**2,
            C_BS_C_duration_chi_floor=2*np.pi,echo_duration_chi_floor=4*np.pi,
            accepted_late_Q_amplitude_per_differential_kappa_limit=np.pi/2,
            echo_code_Pauli_quartic_coefficient=np.pi**4/64),
        physical_exclusions=['Number measurement and helper read errors/time are separate; ideal flags do not certify a detector.',
          'Every photon-loss jump must be flagged by a qualified number/parity instrument; N0 requires full number or a two-loss allowance.',
          'f->e flags require e persistence and distinguishability; e->g plus missed record is an additional fault.',
          'Self/cross Kerr, pump-induced higher nonlinearities and finite helper-drive leakage are not in this linear-mode/dispersive model.',
          'Phase randomization suppresses code-projected coherent errors after discarding the coin, not conditional on keeping its value; accepted Q remains.',
          'Opposite-pass echo needs matching slowly varying drift/loss profiles; arbitrary independent time profiles do not cancel.'])
    (ROOT/'native_palindrome_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
