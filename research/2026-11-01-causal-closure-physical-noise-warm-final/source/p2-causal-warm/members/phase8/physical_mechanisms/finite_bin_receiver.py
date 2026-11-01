"""512-bin finite homodyne receiver, quantized digital coefficients, ADC budget.
No adaptive calibration is performed. Piecewise constant physical filter is
constructed by projecting integrated nominal derivative columns in bin space.
"""
from pathlib import Path
import json
import numpy as np
from scipy.integrate import solve_ivp
from scipy.special import ndtr,log_ndtr
from numpy.polynomial.legendre import leggauss
from robust_longitudinal_receiver import controls,analytic_bounds


def finite_bin(T=4.472,bins=512,order=2,weight_bits=40,adc_bits=16,adc_range=16.,Ncap=320,gain_bound=.001,detuning_bound=1e-6):
    kr=4.;k0=1e-4;F=3/(1+1e-6);nb=.1;eta=.5
    edges=np.linspace(0,T,bins+1);dt=T/bins
    def rhs(t,y):
        w=controls(np.array([t]),T)[0][0]
        return [-.5*(kr*w+k0)*y[0]+F*w]
    sol=solve_ivp(rhs,[0,T],[0.],dense_output=True,method='DOP853',rtol=2e-12,atol=1e-14,max_step=.015)
    gn,gw=leggauss(16)
    labels=[(q,d-q) for d in range(order+1) for q in range(d+1)]
    C=np.zeros((bins,len(labels)));hb=np.zeros(bins);ab=np.zeros(bins)
    for j in range(bins):
        breaks=[edges[j]]+[x for x in [.1,T-.1] if edges[j]<x<edges[j+1]]+[edges[j+1]]
        for l,r in zip(breaks[:-1],breaks[1:]):
            t=(l+r)/2+(r-l)*gn/2;wg=(r-l)*gw/2
            w,W=controls(t,T);H=np.sqrt(kr*w)*np.exp(-k0*t/2-kr*W/2);h=np.sqrt(kr*w)*sol.sol(t)[0]
            for k,(q,s) in enumerate(labels):C[j,k]+=np.dot(wg,H*(t/T)**q*(W/T)**s)/np.sqrt(dt)
            hb[j]+=np.dot(wg,h)/np.sqrt(dt)
            ab[j]+=np.dot(wg,np.sqrt(w))/np.sqrt(dt)
    Cn=C/np.linalg.norm(C,axis=0)[None,:];U,svals,_=np.linalg.svd(Cn,full_matrices=False)
    v=hb-U@(U.T@hb);fv=v/np.linalg.norm(v)
    step=4/2**weight_bits # signed coefficient range [-2,+2)
    ints=np.rint(fv/step).astype(np.int64);fq=ints*step;fqnorm=np.linalg.norm(fq);fact=fq/fqnorm
    err_actual=np.linalg.norm(fact-fv)
    err_bound=2*(np.sqrt(bins)*step/2)/(1-np.sqrt(bins)*step/2)
    # A, all signal derivatives, and null overlap are computed for ACTUAL rational weights.
    A=float(fact@ab);mu=float(fact@hb)
    t=np.linspace(0,T,12001);w,W=controls(t,T);H=np.sqrt(kr*w)*np.exp(-k0*t/2-kr*W/2)
    idx=np.minimum((t/dt).astype(int),bins-1);f= fact[idx]/np.sqrt(dt)
    d=dict(T=T,kr=kr,k0=k0,F=F,nb=nb,eta=eta,order=order,A=A,t=t,f=f,H=H,w=w,W=W)
    b=analytic_bounds(d,gain_bound,detuning_bound,Ncap)
    c=b['incoming_overlap_bound']+err_bound
    # Repeat signal bound using the larger implemented-filter overlap.
    km=kr*(1-gain_bound);kp=kr*(1+gain_bound);Dmax=2/(km+k0)+.1;Bmax=Dmax*np.sqrt(kp*T)
    small=2*F/km*(c+np.hypot(k0/2,detuning_bound)*Bmax)
    lo=(1-1e-6)*(2*F/np.sqrt(kp)*A-small);hi=(1+1e-6)*(2*F/np.sqrt(km)*A+small);im=(1+1e-6)*small
    adc_step=2*adc_range/2**adc_bits
    score_error=adc_step/2*float(np.sum(abs(fact)))
    score_error_bound=adc_step/2*np.sqrt(bins)
    vth=2*nb+1;wvar=1+2*eta*nb
    qmax=float(ndtr((score_error_bound-2*np.sqrt(eta)*lo)/np.sqrt(wvar)))
    logqmin=log_ndtr((-score_error_bound-2*np.sqrt(eta)*hi)/np.sqrt(wvar))
    loggamma=-np.log(2)-2*vth*lo*lo+2*eta*vth*vth*im*im/wvar
    e=qmax+float(np.exp(2*loggamma-logqmin))
    eps=float(np.arcsin(c)*np.sqrt(vth*Ncap+nb))
    # Uniform cap-based quadrature MGF bound for every individual time bin.
    cbin=np.sqrt(kp*dt)
    hbin=2*3./km*np.sqrt(kp*dt) # Factual<=3
    shift=2*np.sqrt(eta)*(cbin*np.sqrt(Ncap)+hbin)
    pclip=2*np.exp(-max(adc_range-shift,0)**2/(2*wvar))
    out=dict(T=T,bins=bins,bin_duration=dt,derivative_order=order,weight_bits=weight_bits,weight_range=[-2,2],weight_step=step,
        weight_integer_min=int(min(ints)),weight_integer_max=int(max(ints)),coefficient_L2_error_actual=float(err_actual),coefficient_L2_error_bound=float(err_bound),
        filter_norm_before_normalization=float(fqnorm),max_derivative_null_residual_actual=float(max(abs(fact@C))),singular_values=svals.tolist(),
        nominal_signal_mu=mu,nominal_signal_energy=mu*mu,
        adc_bits=adc_bits,adc_range=adc_range,adc_step=adc_step,score_quantization_error_actual_bound=score_error,score_quantization_error_cauchy_bound=float(score_error_bound),
        actual_incoming_overlap_bound=float(c),photon_cap=Ncap,nb=nb,eta=eta,readout_gain_bound=gain_bound,detuning_bound=detuning_bound,force_gain_bound=1e-6,
        signal_Re_lower=float(lo),signal_Re_upper=float(hi),signal_abs_Im_upper=float(im),reference_CP_bad_including_ADC_guard=float(e),
        capped_instrument_dilation_error_upper=eps,per_bin_clip_bound=float(pclip),per_readout_clip_union_bound=float(bins*pclip),million_readout_clip_union_bound=float(1e6*bins*pclip),
        all_interval_scope='T includes both .1 force/port ramps. ADC integration is during T; actual final calculation/refresh latency must be charged separately. Raw records internal with no future-use contract.',
        adc_scope='Reference CP good subinstrument uses outer score regions |Y_f|>d. Finite quantizer can make any decision in middle strip. Clipping separate uniform cap-bound event; no independent fault coin.',
        arithmetic_scope=f'Store40-bit coefficients and{adc_bits}-bit signed samples; products require{40+adc_bits} bits, sum512terms requires{49+adc_bits} signed bits plus guard. Use at least{8*int(np.ceil((49+adc_bits)/8))}-bit protected accumulator. Extra state-machine/controller fault admitted separately.')
    fname=Path(__file__).with_name('finite_bin_receiver_weights.json')
    if adc_bits==16:fname.write_text(json.dumps(dict(T=T,bins=bins,weight_step=step,integer_weights=ints.tolist()),indent=2)+'\n')
    return out

if __name__=='__main__':
    out={'selected_16bit_adc':finite_bin(), 'comparison_24bit_adc_at_earlier_time':finite_bin(T=4.466,adc_bits=24)}
    Path(__file__).with_name('finite_bin_receiver_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
