"""Synthetic finite-echo acquisition of inverse-dissipation residuals.
A true-source norm bound is a stated premise, not inferred from finite data.
"""
from fractions import Fraction as F
from pathlib import Path
import itertools, json
from echo_compiler import EchoCompiler, propose_maps, interval_expr, dot, matvec
from uniform_certificate import uniform_certificate, mm, psd, sub, diagonal
from dissipation_certificate import required_words, acquire_dissipation_certificate
from run_echo_experiment import Instrument, truth, dumpable


def inv2(a):
    det=a[0][0]*a[1][1]-a[0][1]*a[1][0]
    return [[a[1][1]/det,-a[0][1]/det],[-a[1][0]/det,a[0][0]/det]]


def power(a,n):
    out=diagonal([F(1)]*len(a))
    while n:
        if n&1:out=mm(out,a)
        a=mm(a,a);n//=2
    return out


def fixture(g, depth=8, eta=None, check_long=True):
    hidden=[[[1-g,g],[g,F(1,4)]],[[1-2*g,-g],[-g,F(1,3)]]]
    b=[F(1),F(0)];bound=1-g/2
    eta=g**3/100000 if eta is None else eta
    for a in hidden:
        assert psd(a) and psd(sub(diagonal([bound]*2),a))
    dictionary=[()]
    inst=Instrument(hidden,b,eta);inst.calibrate()
    words=sorted(required_words(dictionary,2,depth),key=lambda w:(len(w),w))
    records={w:inst.query(w) for w in words}
    for w,x in records.items():assert x.contains(truth(hidden,b,w))
    maps=propose_maps(dictionary,2,records,quantum=10**18)
    compiler=EchoCompiler(dictionary,2,records,maps)
    rho=max(abs(t[0][0]) for t in maps)
    old=uniform_certificate(compiler,rho=rho,metric=[[F(1)]])
    energy=acquire_dissipation_certificate(compiler,[bound]*2,depth,[[F(1)]])
    total=energy['signed_remainder_bound_all_words']+old['all_word_measurement_bound']
    actual_q=[]
    for i,a in enumerate(hidden):
        h=sub(diagonal([F(1)]*2),mm(a,a))
        assert psd(h,strict=True)
        d=[a[0][0]-maps[i][0][0],a[1][0]]
        q=dot(d,matvec(inv2(h),d))
        assert q<=energy['inverse_source_dissipation_residual_upper'][i][0][0]
        actual_q.append(q)
    checks=[]
    for w in itertools.product(range(2),repeat=6):
        result=compiler.certificate(w)
        actual=truth(hidden,b,w)
        error=abs(actual-result['corrected_prediction'].center)
        assert error<=total
        checks.append(float(error))
    long_checks=[]
    for i in range(2):
        for n in ([int(1/g),int(2/g),int(5/g)] if check_long else []):
            t=maps[i][0][0]
            expr={(): (1-n)*t**n, (i,): n*t**(n-1)}
            prediction=interval_expr(expr,records)
            actual=power(hidden[i],n)[0][0]
            error=abs(actual-prediction.center)
            assert error<=total
            assert prediction.radius<=old['all_word_measurement_bound']
            long_checks.append({'primitive':i,'length':n,'actual':float(actual),
                                'corrected_center':float(prediction.center),
                                'actual_error':float(error),'exact_containment_passed':True})
    result={'slow_scale_g':g,'raw_adc_radius':eta,
            'source_norm_bound_premise':bound,'dictionary':dictionary,
            'maps':maps,'rho':rho,'depth':depth,
            'source_readings':len(records),'calibration_standards':2,
            'total_readings':inst.calls,'resets':len(records),
            'primitive_applications':inst.operations,'max_query_length':max(map(len,words)),
            'raw_records':inst.raw,
            'decoded_records':[{'word':w,'interval':x} for w,x in records.items()],
            'dissipation_certificate':energy,
            'old_uniform_certificate_same_model_and_data':old,
            'new_total_all_word_bound':total,
            'bound_ratio_old_to_new':old['all_word_total_bound']/total,
            'checker_actual_inverse_dissipation_forms':actual_q,
            'checked_short_words':64,'maximum_checked_short_error':max(checks),
            'checked_long_words':long_checks,
            'all_exact_checks_passed':True,
            'scope':'No instrument precision, physical source norm warranty, or physical execution is acquired by numerical simulation.'}
    print('g',float(g),'readings',inst.calls,'operations',inst.operations,
          'new',float(total),'old',float(old['all_word_total_bound']),
          'ratio',float(result['bound_ratio_old_to_new']),flush=True)
    return result


def main():
    fixtures=[fixture(F(1,n)) for n in [10,20,50,100,1000]]
    noise_sweep=[fixture(F(1,1000),eta=F(1,10**p),check_long=False)
                 for p in [10,8,6]]
    depth_sweep=[fixture(F(1,1000),depth=k,eta=F(1,10**10),check_long=False)
                 for k in [0,1,2,4]]
    out=Path(__file__).resolve().parents[1]/'results'/'DISSIPATION_EXPERIMENT.json'
    out.write_text(json.dumps(dumpable({'fixtures':fixtures,'fixed_source_noise_sweep':noise_sweep,
                                      'fixed_source_depth_sweep':depth_sweep,
                                      'all_checks_passed':True}),indent=2)+'\n')


if __name__=='__main__':main()
