"""Compare the implemented loop with a closed loop at the ACTUAL passive pole.

The comparison waveform is a mathematical reference, not a secretly available
calibration/control oracle. Uniform interval bounds can be taken over actual
poles. The actual pulse, its finite ramps and its physical damping are unchanged.
Only a small linear-force difference is charged to joint noise admission.
The projected reference forces are also Gram-Schmidt orthogonalized in the
FULL output displacement inner product. Closure alone does not preserve the
orthogonal radiation modes needed by the exact parity CP instrument.
"""
from pathlib import Path
import json
import numpy as np
from scipy.integrate import simpson, cumulative_simpson

HERE=Path(__file__).resolve().parent
PULSE=json.loads((HERE.parent/'physical_mechanisms/one_bus_parity_results.json').read_text())['optimized_safe']

def pulse(points=16001):
    T=PULSE['T'];k=PULSE['kappa'];A,B,c=PULSE['coefficients']
    t=np.linspace(0,T,points);q=np.pi*t/T;dq=np.pi/T;s=np.sin(q);co=np.cos(q)
    X=s*s*np.sin(2*q);Xp=dq*(2*s*co*np.sin(2*q)+2*s*s*np.cos(2*q))
    Y=s*s*(np.cos(2*q)+.5);Yp=dq*(2*s*co*(np.cos(2*q)+.5)-2*s*s*np.sin(2*q))
    ef=np.exp(k*t/2);x=ef*X;xp=ef*(Xp+k*X/2);y=ef*Y;yp=ef*(Yp+k*Y/2)
    y-=c*x;yp-=c*xp;x*=A;xp*=A;y*=B;yp*=B
    return t,np.array([1j*(xp+k*x/2),-(yp+k*y/2)])

def reference(kappa,detuning,points=16001,two_sided=True,number_cap=320,nb=.1):
    t,f=pulse(points);T=t[-1];s=t-T/2;a=kappa/2
    # Stable independent constraint rows. sinh(a*s)/a avoids an ill-conditioned
    # difference of nearly equal exponentials at weak intrinsic damping.
    phase=np.exp(1j*detuning*s)
    if two_sided:
        rows=np.array([phase*np.cosh(a*s),phase*(np.sinh(a*s)/a if a else s)])
    else:rows=np.array([phase*np.exp(-a*s)])
    window=np.sin(np.pi*t/T)**2
    gram=np.array([[simpson(window*r*np.conj(v),x=t) for v in rows] for r in rows])
    target=np.array([[simpson(r*fj,x=t) for r in rows] for fj in f])
    coeff=np.array([np.linalg.solve(gram,z) for z in target])
    df=np.array([window*np.sum(c[:,None]*np.conj(rows),axis=0) for c in coeff])
    ref=f-df
    # No approximation of actual bosonic damping is made in either channel.
    lam=a+1j*detuning
    def cint(y):
        return cumulative_simpson(y.real,x=t,initial=0)+1j*cumulative_simpson(y.imag,x=t,initial=0)
    beta=np.array([-1j*np.exp(-lam*t)*cint(np.exp(lam*t)*fj) for fj in ref])
    def displacement_inner(left,right):
        return np.conj(left[-1])*right[-1]+kappa*simpson(np.conj(left)*right,x=t)
    # Both null constraints are linear, so subtracting a multiple of the first
    # reference force from the second preserves them. At exact two-sided
    # closure the endpoint term vanishes and this is the radiation Gram matrix.
    # Use the full inner product also in the numerical construction, rather
    # than silently losing a retained-mode component to quadrature residuals.
    pre_gram=np.array([[displacement_inner(bj,bk) for bk in beta] for bj in beta])
    orthogonalization=pre_gram[0,1]/pre_gram[0,0]
    ref[1]-=orthogonalization*ref[0]
    beta[1]-=orthogonalization*beta[0]
    # Recompute the actual comparison force and every derived action/phase
    # after orthogonalization. beta changes by the same linear combination.
    df=f-ref
    residual=np.array([[simpson(r*fj,x=t) for r in rows] for fj in ref])
    # JD has norm 2 and ZA norm 1. This force-envelope bound can also be used
    # in a time-domain perturbation argument. The exact dilation calculation
    # below assumes the declared commuting-Z force window; additional faults
    # inside that window need their own physical fault-path admission.
    difference_envelope=2*abs(df[0])+abs(df[1])
    action=float(simpson(difference_envelope,x=t))
    G=np.array([[displacement_inner(bj,bk) for bk in beta] for bj in beta])
    theta=-float(np.real(simpson(ref[0]*np.conj(beta[1])+ref[1]*np.conj(beta[0]),x=t)))
    # Small diagonal self phases multiply JD^2 and ZA^2. The ZA term is scalar;
    # JD^2=2I+2S is gauge in the parity consumer but not a free logical CZ phase.
    self_phase=[-float(np.real(simpson(fj*np.conj(bj),x=t))) for fj,bj in zip(ref,beta)]
    actual_beta=np.array([-1j*np.exp(-lam*t)*cint(np.exp(lam*t)*fj) for fj in f])
    delta_beta=actual_beta-beta
    old=np.array([-1j*simpson(np.exp((-a+1j*detuning)*t)*fj,x=t) for fj in df])
    theta_actual=-float(np.real(simpson(f[0]*np.conj(actual_beta[1])+f[1]*np.conj(actual_beta[0]),x=t)))
    self_actual=[-float(np.real(simpson(fj*np.conj(bj),x=t))) for fj,bj in zip(f,actual_beta)]
    # Full one-particle inner products contain retained mode + EVERY loss photon.
    cross=np.array([[displacement_inner(bj,bk) for bk in actual_beta] for bj in beta])
    delta_gram=np.array([[displacement_inner(bj,bk) for bk in delta_beta] for bj in delta_beta])
    # Self phases in JD^2=2I+2S and ZA^2=I are an allowed gauge phase/global phase.
    # They are placed in the nominal reference, never silently dropped from a
    # nongauge target operation. The J_D*Z_A coefficient sets the parity gate.
    omega_cross=theta_actual-np.pi/4+float(np.imag(cross[0,1]+cross[1,0]))
    branch_bounds=[]
    for jd in [-2,0,2]:
        for za in [-1,1]:
            zz=np.array([jd,za]);c_old=abs(zz@old)
            total=float(np.real(zz@delta_gram@zz))
            fresh=max(0.,total-c_old*c_old)
            amplitude=(abs(jd*za*omega_cross)+c_old*(np.sqrt(number_cap)+np.sqrt(number_cap+1))
                       +np.sqrt((2*nb+1)*fresh))
            branch_bounds.append(dict(jd=jd,za=za,old_displacement=c_old,
                fresh_displacement_norm=np.sqrt(fresh),dilation_norm_bound=float(amplitude)))
    return dict(kappa=kappa,detuning=detuning,two_sided=two_sided,
       force_difference_action=action,max_force_difference=float(max(difference_envelope)),
       constraint_residual=float(np.max(abs(residual))),theta=theta,
       theta_error=theta-np.pi/4,self_phase=self_phase,
       reference_orthogonalization_coefficient=[float(np.real(orthogonalization)),float(np.imag(orthogonalization))],
       reference_cross_gram_before_orthogonalization=[float(np.real(pre_gram[0,1])),float(np.imag(pre_gram[0,1]))],
       reference_cross_gram_abs=float(abs(G[0,1])),
       reference_gram_real=G.real.tolist(),reference_gram_imag=G.imag.tolist(),
       retained_reference_displacement=abs(beta[:,-1]).tolist(),
       restricted_input_number_cap=number_cap,thermal_nb=nb,
       aligned_reference_parity_angle_error=omega_cross,
       nominal_reference_gauge_phase_coefficients=[self_actual[j]+float(np.imag(cross[j,j])) for j in range(2)],
       exact_linear_dilation_comparison=branch_bounds,
       restricted_full_channel_diamond_bound=2*max(b['dilation_norm_bound'] for b in branch_bounds),
       warning='Sampled numerical sensitivity, not an interval certificate or a physical rate measurement.')

def main():
    rows=[]
    for k in [.9e-4,1.e-4,1.1e-4]:
        for d in [0.,1.e-6,1.e-5,1.e-4,.001]:
            rows.append(reference(k,d))
    single=[reference(1.1e-4,d,two_sided=False) for d in [1.e-6,1.e-4,.001]]
    out=dict(implemented_pulse=PULSE,comparison=rows,incoming_only_comparison=single,
       scope='Two-sided references support the full retained product-channel theorem. Incoming-only references support record-inclusive semicausality when separately earned; they are not substituted into the same full-memory CP fault bound.',
       conservative_analytic_force_bound='For a detuning error the general time-domain perturbation delta_omega*n remains a valid alternative; the small comparison force must be bounded over the actual parameter domain before claiming its smaller budget.')
    (HERE/'actual_pole_reference_results.json').write_text(json.dumps(out,indent=2)+'\n')
    def compact(r):
        return {key:r[key] for key in ['kappa','detuning','two_sided',
            'constraint_residual','reference_cross_gram_abs',
            'reference_orthogonalization_coefficient','force_difference_action',
            'aligned_reference_parity_angle_error','restricted_full_channel_diamond_bound']}
    print(json.dumps({'output':str(HERE/'actual_pole_reference_results.json'),
        'max_constraint_residual':max(r['constraint_residual'] for r in rows),
        'max_reference_cross_gram_abs':max(r['reference_cross_gram_abs'] for r in rows),
        'selected_rows':[compact(r) for r in rows if r['kappa']==.00011 and r['detuning'] in [0.,1.e-6,.001]],
        'incoming_only_comparison':[compact(r) for r in single]},indent=2))

if __name__=='__main__':main()
