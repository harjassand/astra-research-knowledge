#!/usr/bin/env python3
"""Forward scalar-trajectory high-opposite H3 extraction and noise accounting.

Exact K is used ONLY to evaluate truth and give deliberately favorable oracle
linear-port subtraction. This is not an end-to-end K acquisition claim.
"""
import itertools
import json
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
K = np.array([[1.8,-.65,.42],[-.65,1.25,.27],[.42,.27,1.7]])
ALPHA = .3


def resolvent(z, model='first', gamma=.08):
    denominator = z if model == 'first' else z*z+gamma*z
    return np.linalg.solve(denominator*np.eye(3)+K, np.array([1.,0,0]))


def truths(omega, model='first', gamma=.08, slow_in=1., slow_out=2.):
    s, t = 1j*slow_out, 1j*slow_in
    c = (s-t)/2
    r = 1j*omega
    qs, qt = resolvent(s,model,gamma),resolvent(t,model,gamma)
    qp,qm = resolvent(r+c,model,gamma),resolvent(-r+c,model,gamma)
    F = ALPHA*np.sum(qs*qt*qp*qm)
    P = ALPHA*qs[0]*qt[0]*qp[0]*qm[0]
    B = ALPHA*np.sum(K[1:,0]**2*qs[1:]*qt[1:])
    exponent = 4 if model == 'first' else 8
    finite_B = omega**exponent*(F-P)
    return F,P,B,finite_B,exponent


def forward(omega, amplitude=.2, grid=4096, wash_periods=4, measure_periods=2):
    signs=np.array(list(itertools.product([-1.,1.],repeat=3)))
    weights=np.prod(signs,axis=1)
    signs=np.vstack([signs,signs])
    levels=np.array([amplitude]*8+[amplitude/2]*8)
    period=4*np.pi
    dt=period/grid
    total=grid*(wash_periods+measure_periods)
    times=np.arange(total)*dt
    freqs=np.array([omega+.5,omega-.5,1.])
    phases0=np.cos(freqs[:,None]*times)
    phasesh=np.cos(freqs[:,None]*(times+dt/2))
    phases1=np.cos(freqs[:,None]*(times+dt))
    u0=levels[:,None]*(signs@phases0)
    uh=levels[:,None]*(signs@phasesh)
    u1=levels[:,None]*(signs@phases1)
    x=np.zeros((16,3))
    samples=grid*measure_periods
    output=np.empty((16,samples))

    def rhs(v,u):
        f=-v@K.T-ALPHA*v**3
        f[:,0]+=u
        return f

    for step in range(total):
        k1=rhs(x,u0[:,step])
        k2=rhs(x+dt*k1/2,uh[:,step])
        k3=rhs(x+dt*k2/2,uh[:,step])
        k4=rhs(x+dt*k3,u1[:,step])
        x+=dt*(k1+2*k2+2*k3+k4)/6
        if step>=grid*wash_periods:
            output[:,step-grid*wash_periods]=x[:,0]
    measurement_times=(np.arange(samples)+grid*wash_periods+1)*dt
    demod=np.exp(-2j*measurement_times)

    def extract(y):
        estimates=[]
        for level,block in [(amplitude,y[:8]),(amplitude/2,y[8:])]:
            polarized=weights@block/8
            # F=-H3; cross Fourier coefficient=(3/4)*amplitude^3*H3.
            estimates.append(-4*np.mean(polarized*demod)/(3*level**3))
        return (4*estimates[1]-estimates[0])/3,estimates

    F_est,raw=extract(output)
    sigma=1e-5
    noisy=output+np.random.default_rng(327+int(omega)).normal(scale=sigma,size=output.shape)
    F_noisy,_=extract(noisy)
    # Exact RMS complex error from independent Gaussian scalar noise, including
    # 8-sign projection and the two-amplitude Richardson extrapolation.
    rms_F=np.sqrt(1025/9)*np.sqrt(2)*sigma/(3*amplitude**3*np.sqrt(samples))
    return F_est,F_noisy,dict(amplitude_per_tone=amplitude,sigma=sigma,
        total_physical_trials=16,dt=dt,measurement_samples_per_trial=samples,
        total_measured_scalar_samples=int(output.size),
        discarded_washout_samples=int(16*grid*wash_periods),
        time_per_trial=float((wash_periods+measure_periods)*period),
        total_physical_duration_excluding_resets=float(16*(wash_periods+measure_periods)*period),
        input_max=float(np.max(np.abs(u0))),input_energy=float(dt*np.sum(u0*u0)),
        rms_complex_F_noise=float(rms_F),raw_F_real_imag=[[z.real,z.imag] for z in raw])


def ascomplex(z):
    return [float(z.real),float(z.imag)]


def main():
    start=time.perf_counter()
    result=dict(model='first order',oracle_port_subtraction=True,
        warning='Oracle H1 is favorable and is not acquired; no K recovery is claimed.',forward=[])
    for omega in [3.,5.,9.,17.]:
        F,P,B,finite,exponent=truths(omega)
        estimate,noisy,ledger=forward(omega)
        acquired=omega**4*(estimate-P)
        acquired_noisy=omega**4*(noisy-P)
        rms_B=omega**4*ledger['rms_complex_F_noise']
        relative_sd=rms_B/abs(B)
        repeats_for_10pct=(relative_sd/.1)**2
        row=dict(omega=omega,true_B=ascomplex(B),true_B_abs=float(abs(B)),
            true_hidden_F_abs=float(abs(F-P)),true_port_F_abs=float(abs(P)),
            finite_frequency_B=ascomplex(finite),
            finite_frequency_relative_bias=float(abs(finite-B)/abs(B)),
            actual_noiseless_extracted_B=ascomplex(acquired),
            actual_noiseless_relative_error=float(abs(acquired-B)/abs(B)),
            actual_one_noise_draw_B=ascomplex(acquired_noisy),
            expected_rms_complex_B_noise=float(rms_B),
            rms_relative_B_noise=float(relative_sd),
            ideal_independent_protocol_repetitions_for_10pct_noise=float(repeats_for_10pct),
            ideal_scalar_measurements_for_10pct_noise=float(repeats_for_10pct*ledger['total_measured_scalar_samples']),
            physical_ledger=ledger)
        result['forward'].append(row)
        print(json.dumps(row),flush=True)
        (ROOT/'high_pair_partial.json').write_text(json.dumps(result,indent=2)+'\n')
    # Oscillator spectral truth is only a prospective best-case noise test.
    # No oscillator trajectories or acquired matrix are represented here.
    result['oscillator_spectral_only']=[]
    for omega in [3.,5.,9.,17.]:
        F,P,B,finite,e=truths(omega,'oscillator',gamma=.08,slow_in=1.,slow_out=1.5)
        result['oscillator_spectral_only'].append(dict(omega=omega,gamma=.08,
            low_input_frequency=1.,low_output_frequency=1.5,
            B_abs=float(abs(B)),hidden_H3_abs=float(abs(F-P)),port_H3_abs=float(abs(P)),
            finite_frequency_relative_bias=float(abs(finite-B)/abs(B)),
            output_complex_cross_amplitude_at_tone_amplitude_003=float(.75*.03**3*abs(F-P)),
            normalization_noise_gain=float(omega**e)))
    result['runtime_s']=time.perf_counter()-start
    (ROOT/'high_pair_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print('Runtime',result['runtime_s'],flush=True)


if __name__=='__main__':
    main()
