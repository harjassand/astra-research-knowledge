"""Actual finite-record budgets and same-model comparators, with no data.

Two assigned N32 thermal accesses, directed scalar moments, non-IID
exposures, PSD/duration electronics, zero-start transient and explicit
calibration debt. This computes plans, not a physical classification.
"""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal as D
import hashlib,json,time
from acquire_moments import I,DN,UP,NEAR,qi

HERE=Path(__file__).resolve().parent
BASE=HERE.parent
PSD=F(1,100);RISK=F(1,20);N=32

def ceil_i(x):return int(UP.to_integral_value(x.hi))
def ep(x):return x.exp()

def pi_interval():
    def atan(q,terms=48):
        s=sum((F((-1)**j,(2*j+1)*q**(2*j+1)) for j in range(terms)),F(0))
        e=F(1,(2*terms+1)*q**(2*terms+1))
        return qi(s)+I(-qi(e).hi,qi(e).hi)
    return 16*atan(5)-4*atan(239)

def cos_i(x):
    total=I(1);term=I(1)
    for j in range(1,51):
        term=-term*x.sq()/((2*j-1)*(2*j));total=total+term
    rem=(term*x.sq()/(101*102)).abs()
    return total+I(-rem.hi,rem.hi)

def continuant(c,n=32):
    vals=[(1,0,0),(c,1,0)]
    for _ in range(2,n+1):
        a,ap,app=vals[-1];b,bp,bpp=vals[-2]
        vals.append((c*a-b,a+c*ap-bp,2*ap+c*app-bpp))
    dn,pn,qn=vals[-1];dm,pm,_=vals[-2]
    mu=F(pn,dn);var=mu*mu-F(qn,dn)
    return dict(d=F(dm,dn),g=F(1,dn),mu=mu,travelvar=var,
                R2pp=F(dm*pn-pm*dn,dn*dn),updates=3*(n-1),maxbits=max(abs(x).bit_length() for row in vals for x in row))

def spectral(c,pi):
    modes=[]
    for j in range(1,N+1):
        x=j*pi/(N+1);lam=c-2*cos_i(x);weight=(1-cos_i(2*x))/(N+1)
        assert lam.lo>0 and weight.lo>0
        modes.append((lam,weight))
    k=min(l.lo for l,w in modes)
    return modes,I(k)

def harmonic(modes,delta):
    variance=I(0);cross=I(0)
    for lam,w in modes:
        z=lam*delta;e=(-z).exp()
        variance=variance+w/lam*2*(z-1+e)/z.sq()
        cross=cross+w/lam*((1-e)/z).sq()
    assert variance.lo>0 and cross.lo>0
    return variance,cross

def first_integer_time(bound,target):
    if bound(I(0)).hi<=target.lo:return 0
    hi=1
    while bound(I(hi)).hi>target.lo:hi*=2
    lo=0
    while hi-lo>1:
        mid=(lo+hi)//2
        if bound(I(mid)).hi<=target.lo:hi=mid
        else:lo=mid
    return hi

def calibration(signal,reference,power,noise_precision):
    s=I(signal.lo);r=max(abs(reference.lo),abs(reference.hi))
    # These one-source sensitivities are NOT a joint physical certificate.
    gain=s/(24*I(r)) if power==2 else s/(8*I(r))
    return {'total_score_mean_error_required_upper':str((s/8).lo),
       'gain_relative_error_if_it_uses_entire_budget':str(gain.lo),
       'reference_relative_variance_or_mean_error_if_only_source':str((s/(8*I(r))).lo),
       'electronics_variance_precision_required':str((s/8).lo) if noise_precision else 'Not needed for the statistic mean; independent zero-mean electronics and PSD upper are still premises.',
       'gain_convention':'Displayed one-source gain sensitivity assumes Z=G*F+eta: gain acts on physical exposure F before independent additive electronics eta. For gain on the entire raw read, the coarse-PSD square rule must use Vdelta+sigma_max rather than Vdelta in its gain sensitivity. The externally warranted combined score-mean error contract is unchanged.',
       'interpretation':'Only nominal theta1/model is certified. These are reference-side equivalent sensitivities, not a qualified rectangle for uncertain temperature/K. Contrast must be requalified if those model parameters vary. No calibration data supplied.'}

def covariance_plan(case,kind,delta,retention,modes,k,unknown_noise_variance=False):
    start=time.perf_counter();sstat=I(*case['stationary_port_variance_decrease_at_Delta'])
    signal=I((sstat*retention).lo);vh,cref=harmonic(modes,delta)
    sigma=qi(PSD)/delta;S=I(vh.hi)+sigma
    if unknown_noise_variance:
        assert kind=='variance'
        effective=signal-sigma-I(vh.hi-vh.lo)
        if effective.lo<=0:
            return {'kind':'squared_exposure_with_coarse_PSD_only',
                    'status':'THIS_VARIANCE_RULE_NOT_QUALIFIED',
                    'variance_signal_lower':str(signal.lo),'electronics_variance_upper':str(sigma.hi),
                    'reason':'The coarse electronics variance envelope exceeds the proved signal. This is not an impossibility theorem for other statistics.'}
        signal=I(effective.lo)
    V=9*S.sq();Q=ceil_i(128*V/(qi(RISK)*signal.sq()))
    block=delta if kind=='variance' else 2*delta
    spacing=block+1/k
    M=qi(case['TrR']);qd=(1-(-k*delta).exp())/(k*delta)
    A=2*(M*S).sqrt()*qd;B=M*qd.sq()
    geom1=1-(-k*spacing).exp();geom2=1-(-2*k*spacing).exp()
    def transient(t):
        e=(-k*t).exp()
        return (A*e/geom1+B*e.sq()/geom2)/Q
    target=qi(RISK)*signal/16
    burn=first_integer_time(transient,target)
    duration=I(burn)+(Q-1)*spacing+block
    reference=(vh if unknown_noise_variance else vh+sigma) if kind=='variance' else cref
    return {'kind':'squared_exposure_variance' if kind=='variance' else 'adjacent_exposure_cross_product',
      'raw_score_expression':'Z_j^2' if kind=='variance' else 'Z_(j,1)*Z_(j,2)',
      'reference_convention':'RAW square; DO NOT subtract detector variance when using the supplied reference.' if kind=='variance' else 'RAW adjacent product; no electronics variance subtraction.',
      'exposure':delta.encode(),'contrast_retention_lower':str(retention.lo),'signal_lower':str(signal.lo),
      'harmonic_exposure_variance':vh.encode(),'harmonic_adjacent_cross_covariance':cref.encode(),
      'electronics_variance_or_upper':sigma.encode(),'variance_proxy':S.encode(),
      'raw_block_score_variance_constant':V.encode(),'blocks_required':str(Q),
      'readouts_per_block':1 if kind=='variance' else 2,'raw_readouts_required':str(Q*(1 if kind=='variance' else 2)),
      'block_start_spacing':spacing.encode(),'burn_in_time':burn,'observation_duration_upper':str(duration.hi),
      'zero_start_average_coupling_error_upper':str(transient(I(burn)).hi),
      'coupling_error_target':str(target.lo),'reference_score_interval':reference.encode(),
      'calibration':calibration(signal,reference,2,kind=='variance' and not unknown_noise_variance),
      'electronics_contract':'Unknown independent centered Gaussian variance in[0,Sdet_max/delta]; no variance subtraction. Harmonic reference is a lower null mean.' if unknown_noise_variance else 'Exact calibrated variance for square score; cross score needs only independent centered noise and its variance upper.',
      'risk_bound_each':str(RISK),'seconds_afterimports':time.perf_counter()-start,
      'data_readouts_obtained':0,'physical_calibration_obtained':False,
      'status':'PLAN_ONLY_NO_QUALIFIED_PHYSICAL_RECORD'}

def mean_plan(case,active,delta,k):
    signal=I(*active['thermal_port_mean_decrease_interval']);signal=I(signal.lo)
    U=F(active['peak_U']);d=F(case['Rpp_equals_Rvv']);r2=F(case['R2pp'])
    # Contiguous finite exposures equal one time-average. No IID thinning.
    noise_rate=qi(2*r2+PSD)
    T=128*noise_rate/(qi(RISK)*signal.sq())
    Q=ceil_i(T/delta);actual=Q*delta
    M=qi(F(case['TrR'])+U*U*r2)
    avg_contract=I(min(D(1),(1/(k*actual)).hi))
    def transient(t):return M.sqrt()*avg_contract*(-k*t).exp()
    burn=first_integer_time(transient,qi(RISK)*signal/16)
    reference=qi(U*d)
    return {'kind':'same_bath_contiguous_driven_mean','peak_U':str(U),
       'raw_score_expression':'Z_j',
       'signal_lower':str(signal.lo),'native_exposure':delta.encode(),'raw_readouts_required':str(Q),
       'burn_in_time':burn,'observation_duration_upper':str((I(burn)+actual).hi),
       'mean_variance_time_constant':noise_rate.encode(),
       'forced_stationary_second_moment_upper':str(M.hi),
       'zero_start_average_coupling_error_upper':str(transient(I(burn)).hi),
       'reference_score_interval':reference.encode(),'calibration':calibration(signal,reference,1,False),
       'reference_quadratic_loading_energy':str(U*U*d/2),
       'energy_scope':'Reference stored/load energy only; not irreversible power or a full-cycle work lower bound. Static force hold can have zero average mechanical work; reversible return can recover energy.',
       'risk_bound_each':str(RISK),'physical_control_or_record_acquired':False}

def deterministic_plan(case,U,delta,k):
    d=F(case['Rpp_equals_Rvv']);g=F(case['Rpv']);mu=U*g
    lo=F(0);hi=mu
    for _ in range(100):
        x=(lo+hi)/2
        if x+d*x*x*x/2>mu:hi=x
        else:lo=x
    signal=qi(g/2)*I(qi(lo**3).lo,qi(hi**3).hi);s=I(signal.lo)
    T=128*qi(PSD)/(qi(RISK)*s.sq());Q=ceil_i(T/delta);actual=Q*delta
    source_bound=qi(U)*qi(F(case['R2pp'])).sqrt()
    settle=first_integer_time(lambda t:source_bound*(-k*t).exp(),s/8)
    reference=qi(U*d)
    return {'kind':'no_internal_bath_DC_comparator','peak_U':str(U),
       'raw_score_expression':'Z_j',
       'hidden_steady_root_interval':[str(lo),str(hi)],'signal_interval':signal.encode(),
       'raw_readouts_required':str(Q),'settling_time':settle,
       'observation_duration_upper':str((I(settle)+actual).hi),
       'reference_score_interval':reference.encode(),'calibration':calibration(s,reference,1,False),
       'reference_quadratic_loading_energy':str(U*U*d/2),
       'energy_scope':'Recoverable reference loading energy; not U*y power or irreversible holding work.',
       'model_difference':'No internal thermal forcing. SAME scalar one-quartic model; all other nodes linear. This is a DIFFERENT bath access from the passive plans.',
       'physical_control_or_record_acquired':False}

def main():
    start=time.perf_counter();raw=(HERE/'MOMENTS.json').read_bytes();m=json.loads(raw)
    active=json.loads((HERE/'ACTIVE_INPUTS.json').read_text())
    interface_path=BASE/'thermal_time_trace'/'INTERFACE.json'
    inter=json.loads(interface_path.read_text());pi=pi_interval();results=[]
    for case,c in zip(m['cases'],[3,2]):
        case=dict(case)
        if c==3:
            lp=inter['C_long_exposure_interface'];mu=F(lp['travel_mean']['exact']);var=F(lp['travel_variance']['exact'])
            r2=F(inter['R2_pp']['exact']);case['TrR']=str(mu);case['R2pp']=str(r2)
            long_delta=qi(F(lp['proposed_exposure']['exact']));ret=qi(F(lp['contrast_retention_lower']['exact']))
            recurrence_cost={'new_recurrences':0,'source':'A accepted INTERFACE.json exact scalars'}
        else:
            values=continuant(2);mu=values['mu'];var=values['travelvar'];r2=values['R2pp']
            assert values['d']==F(case['Rpp_equals_Rvv']) and values['g']==F(case['Rpv'])
            assert mu==F(N*(N+2),6)
            assert var==F(N*(N+2)*(2*N*N+4*N+9),180)
            case['TrR']=str(mu);case['R2pp']=str(r2)
            long_delta=qi(3*(mu*mu+var)/(2*mu));ret=qi(8*mu*mu/(9*(mu*mu+var)))
            recurrence_cost={'new_recurrences':31,'exact_integer_updates':values['updates'],'max_integer_bits':values['maxbits']}
        modes,k=spectral(c,pi)
        short=covariance_plan(case,'variance',qi(F(1,c)),2*(-I(1)).exp(),modes,k)
        long=covariance_plan(case,'variance',long_delta,ret,modes,k)
        robust=covariance_plan(case,'variance',long_delta,ret,modes,k,True)
        cross_delta=qi(mu/4);cross_ret=qi(mu*mu/(mu*mu+4*var))
        cross=covariance_plan(case,'cross',cross_delta,cross_ret,modes,k)
        thermal=[];dc=[]
        for key in ['weak_fixed_peak','high_peak']:
            inp=next(row for row in active[key] if row['name']==case['name'])
            thermal.append(mean_plan(case,inp,long_delta,k))
            dc.append(deterministic_plan(case,F(inp['peak_U']),long_delta,k))
        results.append({'name':case['name'],'K_diagonal':c,'g':case['Rpv'],'d_equals_b':case['Rpp_equals_Rvv'],
          'TrR':str(mu),'TrR2':str(var),'R2pp':str(r2),'kappa_lower':str(k.lo),
          'recurrence_cost':recurrence_cost,'passive_short':short,'passive_long':long,
          'passive_long_coarse_electronics_only':robust,
          'passive_cross_no_noise_variance_calibration':cross,
          'same_bath_thermal_mean_comparators':thermal,'deterministic_DC_comparators':dc,
          'long_over_short_duration_ratio':(I(long['observation_duration_upper'])/I(short['observation_duration_upper'])).encode()})
    out={'status':'FINITE_READOUT_AND_CALIBRATION_PLANS_COMPILED_NO_PHYSICAL_DATA',
      'cases':results,'risk_each':'1/20','detector_PSD_or_upper':'1/100',
      'initialization':'Exactly zero is the mathematical plan input; no actual zero initialization/reset acquired.',
      'input_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [HERE/'MOMENTS.json',HERE/'ACTIVE_INPUTS.json',interface_path]},
      'qualified_physical_decisions':0,'trajectory_simulations':0,'new_topologies':0,
      'spectral_reference_modes_enclosed':64,'exposure_design_grid_searches':0,
      'seconds_afterimports':time.perf_counter()-start,
      'scope':'Budgets conditional on stipulated bath/model/mobility/detector calibration and actual correlated records; no IID equilibrium samples or practical-optimality claim.'}
    (HERE/'RECEIVER.json').write_text(json.dumps(out,indent=2)+'\n')
    for row in results:
        print(json.dumps({'case':row['name'],'kappa':row['kappa_lower'],
          'passive_long':{k:row['passive_long'][k] for k in ['signal_lower','exposure','raw_readouts_required','observation_duration_upper','burn_in_time']},
          'noise_calibration_free_cross':{k:row['passive_cross_no_noise_variance_calibration'][k] for k in ['signal_lower','raw_readouts_required','observation_duration_upper']},
          'coarse_noise_only_variance':row['passive_long_coarse_electronics_only'],
          'long_over_short_duration_ratio':row['long_over_short_duration_ratio'],
          'thermal_mean_comparators':[{k:r[k] for k in ['peak_U','signal_lower','raw_readouts_required','observation_duration_upper','burn_in_time','reference_quadratic_loading_energy']} for r in row['same_bath_thermal_mean_comparators']],
          'deterministic_DC_comparators':[{k:r[k] for k in ['peak_U','signal_interval','raw_readouts_required','observation_duration_upper','settling_time']} for r in row['deterministic_DC_comparators']]}))
    print(json.dumps({'seconds_afterimports':out['seconds_afterimports'],'qualified_decisions':0}))

if __name__=='__main__':main()
