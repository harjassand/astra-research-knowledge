"""Paid native SOFTWARE realization of finite port experiments.

This module is the source, not the learner. It stores its own finite
realization, evaluates FINITE harmonic input histories by certified
rational elementary-function enclosures, and returns quantized records.
Its dimension, internal coefficients, work and errors are charged.
No physical experiment or executed zero-order-hold waveform is claimed.
"""
from fractions import Fraction as Q
from exact import (C,require,ceilq,dyadic,up,qbits,encode,psd,exp_minus,pi_interval,
                   sincos)


def fixture(which=0,n=256,r=3):
    require(n==256 and r==3)
    multiplier,offset=[(73,19),(117,43)][which]
    values=[Q((multiplier*i+offset)%n,n) for i in range(n)]
    rates=[Q(1)+(v if which==0 else v*v) for v in values]
    B=[[Q(1,16),Q(1 if i%2==0 else -1,16),
        Q(1 if (i//2)%2==0 else -1,16)] for i in range(n)]
    gram=[[sum((row[u]*row[v] for row in B),Q(0)) for v in range(r)] for u in range(r)]
    require(gram==[[Q(int(u==v)) for v in range(r)] for u in range(r)])
    A=[[sum((lam*row[u]*row[v] for lam,row in zip(rates,B)),Q(0))
        for v in range(r)] for u in range(r)]
    second=[[sum((lam*lam*row[u]*row[v] for lam,row in zip(rates,B)),Q(0))
             for v in range(r)] for u in range(r)]
    variance=[[second[u][v]-sum((A[u][j]*A[j][v] for j in range(r)),Q(0))
               for v in range(r)] for u in range(r)]
    require(min(rates)>=1 and len(set(rates))==n)
    require(psd([[2*int(i==j)-A[i][j] for j in range(r)] for i in range(r)]))
    require(psd([[Q(int(i==j),4)-variance[i][j] for j in range(r)] for i in range(r)]))
    require(all(row[0]!=0 for row in B))
    return {'rates':rates,'B':B,'A':A,'coupling_gram':variance,
            'prior_initial_norm':Q(1),'which':which}


def acquire(contract,source,work_bits=80,output_bits=48):
    """Return port-only record and a separately kept native cost report.

    One continuously evolving source starts from an unknown-to-learner
    unit coordinate state. Each trial waits W, then receives the nominal
    sine/cosine history with a small known-bounded gain error. There is
    no reset between trials. A deterministic bounded sensor bias is added
    before quantization. Numerical enclosure errors remain in the record.
    """
    r=contract['r'];a=Q(contract['a']);A0=Q(contract['A0']);c0=Q(contract['c0'])
    rates=source['rates'];B=source['B'];n=len(rates);R0=source['prior_initial_norm']
    smallest=min(map(Q,contract['per_coordinate_budgets']))
    p=max(output_bits,ceilq(smallest.denominator.bit_length()-smallest.numerator.bit_length())+12)
    work_bits=max(work_bits,p+32)
    small=Q(1,1<<p)
    # e^{-aT} <= 2^{-aT}; finite rational times with exact inequalities.
    Rstar=max(R0,2/a)
    wait_power=p+4
    while Rstar*Q(1,1<<wait_power)>Q(1,1<<(p+4)):wait_power+=1
    T=Q(p+4)/a;W=Q(wait_power)/a
    gain=small*(1 if source['which']==0 else -1)
    sensor=small;quant=Q(1,1<<(p+1));clock=small/16
    Ly=(A0+c0+1)*(Rstar+2/a)+2
    native_tol=Q(1,1<<(work_bits-6))
    transient=Q(1,1<<(p+4))/a
    initial=Rstar*Q(1,1<<wait_power)
    gamma=transient+initial+abs(gain)/a+sensor+quant+Ly*clock+native_tol
    require(gamma<=smallest,'The implemented native precision misses the requested budget.')
    max_phase=Q(contract['frequencies'][-1])*T+1
    phase_bits=max(0,max_phase.numerator.bit_length()-max_phase.denominator.bit_length()+1)
    pi=pi_interval(max(120,work_bits+32+phase_bits))
    exponentials=[];initial_exp=[];terms=0;squarings=0;series_bits=0
    for lam in rates:
        lo,hi,cost=exp_minus(lam*T,work_bits)
        exponentials.append(((lo+hi)/2,(hi-lo)/2,hi))
        terms+=cost['taylor_terms'];squarings+=cost['squarings']
        series_bits=max(series_bits,cost['series_coefficient_bits_max'])
        lo,hi,cost=exp_minus(lam*(W+T),work_bits)
        initial_exp.append(((lo+hi)/2,(hi-lo)/2,hi))
        terms+=cost['taylor_terms'];squarings+=cost['squarings']
        series_bits=max(series_bits,cost['series_coefficient_bits_max'])
    observations=[];trigterms=0;max_radius=Q(0);max_integer_bits=0
    state=[Q(int(i==source['which'])) for i in range(n)]
    state_errors=[Q(0)]*n
    for freq_index,w0 in enumerate(contract['frequencies']):
        w=Q(w0)
        sine,cosine,phase_error,cost=sincos(w*T,pi,work_bits)
        trigterms+=cost['taylor_terms']
        series_bits=max(series_bits,cost['series_coefficient_bits_max'])
        factors=[];factor_radius=Q(0)
        for lam,(ec,er,eh) in zip(rates,exponentials):
            centre=C(1-ec*cosine,ec*sine)/C(lam,w)
            # Complex 1-norm controls Euclidean error. Both trig components
            # are enclosed; the exponential interval is independently paid.
            err=(er*(abs(cosine)+abs(sine))+2*eh*phase_error)/lam
            err+=Q(1,1<<work_bits)
            factors.append(centre.rounded(work_bits))
            factor_radius=max(factor_radius,err)
        reports=[[C() for _ in range(r)] for _ in range(r)]
        for col in range(r):
            for imaginary in [False,True]:
                # Native state is private and continuously propagated.
                # exp(-lambda*(W+T)) accounts for both preparation and trial.
                new_state=[];new_errors=[]
                for k,((ec,er,eh),factor) in enumerate(zip(initial_exp,factors)):
                    value=factor.im if imaginary else factor.re
                    centre=ec*state[k]+(1+gain)*B[k][col]*value
                    radius=eh*state_errors[k]+er*abs(state[k])
                    radius+=(1+abs(gain))*abs(B[k][col])*factor_radius
                    radius+=Q(1,1<<(work_bits+1))
                    new_state.append(dyadic(centre,work_bits));new_errors.append(up(radius,work_bits+8))
                state,state_errors=new_state,new_errors
                for row in range(r):
                    centre=sum((B[k][row]*state[k] for k in range(n)),Q(0))
                    if imaginary:bias=sensor*(1 if (freq_index+2*row+col)%3 else -1)
                    else:bias=sensor*(1 if (freq_index+row+col)%2 else -1)
                    rounded=dyadic(centre+bias,p)
                    if imaginary:reports[row][col].im=rounded
                    else:reports[row][col].re=rounded
                    numerical=sum((abs(B[k][row])*state_errors[k] for k in range(n)),Q(0))
                    require(numerical<=native_tol,'Native finite forward enclosure exceeds its budget.')
                    max_radius=max(max_radius,numerical)
                    max_integer_bits=max(max_integer_bits,abs(rounded.numerator).bit_length(),rounded.denominator.bit_length())
        observations.append(encode({'frequency':w,'response_matrix':reports,
                                   'certified_coordinate_error':gamma}))
    N=contract['frequency_count'];trials=2*r*N
    # A fully digital actuator alternative is COSTED, not executed here.
    # Allocate a separate input-error allowance from the remaining budget.
    actuator_nu=a*smallest/8
    maxw=Q(contract['frequencies'][-1])
    hold_step=actuator_nu/(4*max(maxw,Q(1)))
    hold_updates=ceilq((T+clock)/hold_step)
    record={'contract':contract,'observations':observations,
            'channel':encode({'kind':'certified finite-harmonic SOFTWARE port experiments',
                'waiting_time_per_trial':W,'active_duration_per_trial':T,
                'prior_initial_norm':R0,'uniform_trial_start_norm_bound':Rstar,
                'initial_bound_at_start':initial,'between_trial_resets':0,
                'input_gain_mismatch_bound':abs(gain),'sensor_bias_bound':sensor,
                'quantization_bound':quant,'clock_error_bound':clock,
                'output_derivative_bound':Ly,'finite_time_transient_bound':transient,
                'native_numerical_error_bound':native_tol,'coordinate_error':gamma,
                'reported_fractional_bits':p,'native_work_fractional_bits':work_bits,
                'noise_assumption':'bounded adversarial; no statistical averaging',
                'physical_validation':'none; software source only'})}
    native_cost=encode({'native_dimension':n,'number_of_distinct_visible_source_poles':len(set(rates)),
        'encoded_source_scalars':n+n*r,'source_generation':'rational diagonal rates and normalized Hadamard port columns',
        'real_port_trials':trials,'scalar_readouts':2*r*r*N,
        'total_wait_time':trials*W,'total_active_time':trials*T,
        'input_energy_upper_bound':trials*T*(1+abs(gain))**2,
        'forward_mode_factors':n*N,'private_state_coordinate_updates':n*trials,
        'forward_real_output_weighted_terms':n*r*trials,
        'private_initial_state_assignments':n,'between_trial_resets':0,
        'exponential_evaluations':2*n,'exponential_taylor_terms':terms,
        'exponential_squarings':squarings,'trigonometric_pair_evaluations':N,
        'trigonometric_taylor_terms':trigterms,
        'native_numerical_error_max':up(max_radius,work_bits),
        'native_series_coefficient_bits_max':series_bits,
        'source_coefficient_bits_max':max(qbits(v) for v in rates+[v for row in B for v in row]),
        'source_normalization_moment_terms':3*n*r*r,
        'report_integer_bits_max':max_integer_bits,
        'source_prior_validation':{'A':source['A'],'coupling_gram':source['coupling_gram'],
             'a':'1','A0':'2','c0':'1/4','B_transpose_B':'identity, exact rational check'},
        'digital_hold_alternative_NOT_EXECUTED':{'input_error_allowance':actuator_nu,
            'step_upper_bound':hold_step,'updates_per_real_trial':hold_updates,
            'updates_all_trials':hold_updates*trials,
            'added_output_error_bound':actuator_nu/a,
            'purpose':'explicit finite actuation cost; actual native execution uses a finite harmonic command'}})
    return record,native_cost
