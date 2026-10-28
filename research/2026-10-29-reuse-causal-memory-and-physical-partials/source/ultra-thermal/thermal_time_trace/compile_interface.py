"""Exact same-source information/retention coefficients; no observations.

N32,theta1,Delta1/2,Sdet1/100 is C's locked physical-access plan.
Ideal-path information is an UPPER bound for those finite noisy records.
Local Fisher coefficients are STATIONARY and evaluated ONLY at a=0.
No finite-Delta g^4 information claim is inferred.
"""
from fractions import Fraction as F
from decimal import Decimal,localcontext
from pathlib import Path
import hashlib,json,time

HERE=Path(__file__).resolve().parent

def display(x):
    with localcontext() as ctx:
        ctx.prec=18
        return str(Decimal(x.numerator)/Decimal(x.denominator))

def continuants(n):
    # D_n(c)=c D_(n-1)-D_(n-2), its first/second derivatives at c=3.
    d0,p0,q0=1,0,0;d1,p1,q1=3,1,0
    values=[(d0,p0,q0),(d1,p1,q1)]
    for k in range(2,n+1):
        nxt=(3*d1-d0,d1+3*p1-p0,2*p1+3*q1-q0)
        d0,p0,q0=d1,p1,q1;d1,p1,q1=nxt;values.append(nxt)
    return values

def compile_case(n=32,theta=F(1),delta_a=F(1,2),noise_psd=F(1,100)):
    start=time.perf_counter();assert n>=4
    vals=continuants(n);dn,pn,qn=vals[n];dm,pm,qm=vals[n-1]
    mu=F(pn,dn);travel_var=mu*mu-F(qn,dn)
    b=d=F(dm,dn);g=F(1,dn);rpp2=d*(mu-F(pm,dm))
    assert travel_var>0 and rpp2>0
    # Global all-a/finite-T KL bounds from the same-bath port cancellation.
    dc_gain=g/b
    rate_stationary=F(15,4)*delta_a**2*theta**2*d**3*dc_gain**2
    init_stationary=F(3,4)*delta_a*theta*d*d
    kappa=F(1) # 3I-A_path has lambda_min>1, no spectral oracle needed.
    moment6_zero=(theta/kappa)**3*n*(n+2)*(n+4)
    rate_zero=delta_a**2/(4*theta)*dc_gain**2*moment6_zero
    risk=F(1,20);required_kl=2*(1-2*risk)**2
    lower_time_stationary=max(F(0),required_kl-init_stationary)/rate_stationary
    lower_time_zero=required_kl/rate_zero
    # Maximal Gaussian trajectory canonical-correlation certificate.
    rho2=min(F(1),g*g*((61*mu-12)**2+(183*mu-97)**2))
    rho4=rho2*rho2;rho8=rho4*rho4
    fi_initial2=F(9,2)*theta**2*d**4*rho4
    fi_rate2=F(9,2)*theta**2*d**3*rho4
    fi_initial4=F(3,2)*theta**2*d**4*rho8
    fi_rate4=3*theta**2*d**3*rho8
    # Only an interface for C, not another complete receiver/optimization.
    exposure=3*(mu*mu+travel_var)/(2*mu)
    retention=8*mu*mu/(9*(mu*mu+travel_var))
    v_harm_upper=min(theta*b,2*theta*rpp2/exposure)
    detector_variance=noise_psd/exposure
    s_proxy=v_harm_upper+detector_variance
    result={
      'status':'EXACT_SAME_SOURCE_INFORMATION_AND_RETENTION_INTERFACE',
      'N':n,'theta':str(theta),'Delta':str(delta_a),
      'access':{'K':'3I-A_path','observed_port':1,'defect_vertex':n,'all_other_quartics':0,'drive_peak':0,'noise_psd':str(noise_psd),'baseline_exposure':'1/3','baseline_spacing':'1/3+1/kappa_lower','classification_error_each':'1/20','data_obtained':False},
      'g':g,'b_equals_d':d,'R2_pp':rpp2,'kappa_lower':kappa,
      'global_stationary_initial_KL_upper':init_stationary,
      'global_stationary_continuous_port_KL_rate_upper':rate_stationary,
      'global_zero_initial_continuous_port_KL_rate_upper':rate_zero,
      'finite_Delta_95percent_stationary_minimum_duration_lower':lower_time_stationary,
      'finite_Delta_95percent_zero_initial_minimum_duration_lower':lower_time_zero,
      'rho_squared_upper':rho2,
      'local_stationary_at_a0_Fisher_initial_chaos2_upper':fi_initial2,
      'local_stationary_at_a0_Fisher_rate_chaos2_upper':fi_rate2,
      'local_stationary_at_a0_Fisher_initial_chaos4_upper':fi_initial4,
      'local_stationary_at_a0_Fisher_rate_chaos4_upper':fi_rate4,
      'local_scope':'One-sided a derivative at a0 with stationary initialization. No finite-Delta KL bound or zero-start Fisher transfer.',
      'C_long_exposure_interface':{'travel_mean':mu,'travel_variance':travel_var,'proposed_exposure':exposure,'contrast_retention_lower':retention,'harmonic_exposure_variance_upper':v_harm_upper,'electronics_variance':detector_variance,'total_exposure_variance_proxy':s_proxy,'raw_score_variance_constant_upper':9*s_proxy*s_proxy,'classification_receiver':'Owned by C; no new contrast moment, budget or observations acquired here.'},
      'cost':{'continuant_steps':n-1,'exact_integer_recurrence_updates':3*(n-1),'max_continuant_integer_bits':max(abs(v).bit_length() for tup in vals for v in tup),'simulated_trajectories':0,'data_readouts':0,'new_scalar_Gibbs_integrals':0,'seconds_after_imports':time.perf_counter()-start},
      'input_sha256':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted((HERE/'inputs').iterdir()) if f.is_file()}
    }
    def enc(x):
        if isinstance(x,F):return {'exact':str(x),'display':display(x)}
        if isinstance(x,dict):return {k:enc(v) for k,v in x.items()}
        return x
    return enc(result)

if __name__=='__main__':
    result=compile_case();(HERE/'INTERFACE.json').write_text(json.dumps(result,indent=2)+'\n')
    keys=['global_stationary_continuous_port_KL_rate_upper','global_zero_initial_continuous_port_KL_rate_upper','finite_Delta_95percent_stationary_minimum_duration_lower','finite_Delta_95percent_zero_initial_minimum_duration_lower','local_stationary_at_a0_Fisher_rate_chaos2_upper','local_stationary_at_a0_Fisher_rate_chaos4_upper','C_long_exposure_interface','cost']
    print(json.dumps({k:result[k] for k in keys},indent=2))
