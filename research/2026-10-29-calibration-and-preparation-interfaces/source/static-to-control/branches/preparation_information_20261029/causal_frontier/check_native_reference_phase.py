"""Exact rational controls for the native reference-phase assay.

Positive Bessel-series tail enclosures; no trajectory generation, experiment,
or claimed physical calibration. Float displays summarize exact intervals.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json


def bessel_intervals(c, terms=16):
    t0, t1 = F(1), c/2
    s0, s1 = t0, t1
    for k in range(1, terms+1):
        t0 *= c*c/(4*k*k)
        t1 *= c*c/(4*k*(k+1))
        s0 += t0
        s1 += t1
    k=terms
    tail0 = t0*c*c/(4*(k+1)**2)/(1-c*c/(4*(k+2)**2))
    tail1 = t1*c*c/(4*(k+1)*(k+2))/(1-c*c/(4*(k+2)*(k+3)))
    return (s0,s0+tail0),(s1,s1+tail1)


def ceil_fraction(q):
    return -(-q.numerator//q.denominator)


def main():
    cases=[]
    for n in [1,2,4,8,16,32,64,128]:
        c=F(1,n)
        i0,i1=bessel_intervals(c)
        lo,hi=i1[0]/i0[1],i1[1]/i0[0]
        assert 0<lo<hi<=c/2
        assert hi-lo<F(1,10**35)
        assert lo/c>F(1,6)  # I1>=c/2 and I0<=e^c<3; sharper exact check here.
        info=(c*lo,c*hi)
        score=(lo/c,hi/c)
        receiver=(lo/2,hi/2) # gamma=tau=a=A=1; h=log 2.
        cases.append({'n':n,'u':'1/'+str(n),'r_interval':[str(lo),str(hi)],
            'static_phase_fisher_interval':[str(x) for x in info],
            'dynamic_score_mean_over_Ah_interval':[str(x) for x in score],
            'finite_receiver_mean_amplitude_interval':[str(x) for x in receiver],
            'display':{'r':float((lo+hi)/2),'n_squared_static_fisher':float(n*n*(info[0]+info[1])/2),
                'dynamic_score_mean_over_Ah':float((score[0]+score[1])/2),
                'n_receiver_mean_amplitude':float(n*(receiver[0]+receiver[1])/2)},
            'sufficient_trials_per_phase_static_feature':ceil_fraction(80/(lo*lo)),
            'sufficient_trials_per_phase_receiver':ceil_fraction(400/(lo*lo))})
    result={'status':'PASS','scope':'exact rational Bessel controls; no physical acquisition or trajectory simulation',
        'parameters':{'a':1,'gamma_receiver':1,'gamma_driver':1,'temperature':1,'actuator_force_cap':1,
            'receiver_duration':'log(2)','dynamic_feature_duration':1,'angle_error':'pi/6','failure_probability':'1/20',
            'count_log_bound':'log(80)<5; two independently prepared phase settings required'},
        'dynamic_feature_TV_lower_bound_all_n_ge_1':'1/216',
        'bound_scope':'Exact continuous force-feature path and Gibbs driver preparation; not a finite-bandwidth assay',
        'cases':cases,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    out=Path(__file__).with_name('NATIVE_REFERENCE_PHASE_EXACT_CHECKS.json')
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'script_sha256':result['script_sha256'],
        'dynamic_feature_TV_lower_bound':result['dynamic_feature_TV_lower_bound_all_n_ge_1'],
        'cases':[{'n':x['n'],**x['display'],'static_feature_trials_per_phase':x['sufficient_trials_per_phase_static_feature'],
                  'receiver_trials_per_phase':x['sufficient_trials_per_phase_receiver']} for x in cases]},indent=2))


if __name__=='__main__':
    main()
