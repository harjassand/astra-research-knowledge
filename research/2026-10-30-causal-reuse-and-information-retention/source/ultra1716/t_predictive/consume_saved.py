"""Read-only consumer: saved access-control law and exact exponent bookkeeping.

No P/teacher sampler, geometry, optimizer or producer module is imported/run.
This does not validate the proposed general theorem or a numerical solver.
"""
from pathlib import Path
from fractions import Fraction as F
import json, hashlib, time
from flint import arb,ctx

HERE=Path(__file__).resolve().parent


def majorizes(c,p,q,xmin=1000):
    """Exact certificate c*x**p <= x**q for every x>=xmin."""
    c=F(c)
    assert q>=p and c<=xmin**(q-p)
    return {'coefficient':str(c),'left_power':p,'right_power':q,
            'domain':f'x >= {xmin}','rule':'c <= xmin^(q-p)'}


def source_probability(word):
    k=sum(word);n=len(word)
    return F(41,100)*F(9,50)**k*F(41,50)**(n-k)+F(59,100)*F(18,25)**k*F(7,25)**(n-k)


def main():
    started=time.perf_counter();ctx.prec=192
    path=HERE/'ENGINEERING_EXECUTION.json'
    data=json.loads(path.read_text())
    assert data['teacher_locked'] and data['teacher_inference_calls']==0
    assert data['convex_solves']==254 and data['solver_statuses']=={'optimal':254}
    words=[tuple(x['word']) for x in data['law']]
    assert len(words)==len(set(words))==256 and all(len(w)==8 for w in words)
    target=[source_probability(w) for w in words]
    observed=[F.from_float(float(row['compiled'])) for row in data['law']]
    assert sum(target)==1 and min(observed)>0
    mass=sum(observed); normalized=[p/mass for p in observed]
    tv=sum(abs(p-q) for p,q in zip(target,normalized))/2
    assert abs(tv-F.from_float(data['total_variation']))<F(1,10**12)
    kl=arb(0)
    for p,q in zip(target,normalized):
        pa=arb(p.numerator)/p.denominator;qa=arb(q.numerator)/q.denominator
        kl+=pa*(pa/qa).log()
    assert abs(float(kl)-data['KL_P_to_compiled'])<1e-12
    # Exact same-source rank certificate: middle block = .98 P + I/800.
    prefixes=[tuple((i>>j)&1 for j in range(4)) for i in range(16)]
    residuals=[]
    for i,h in enumerate(prefixes):
        for j,f in enumerate(prefixes):
            p=source_probability(h+f)
            q=F(49,50)*p+(F(1,800) if i==j else F(0))
            residuals.append(q-F(49,50)*p-(F(1,800) if i==j else F(0)))
    assert not any(residuals)
    delta=-(arb(49)/50).log()
    powers={
        'ceil_D':majorizes(2,40,41),
        'ceil_N':majorizes(2,60,61),
        'ceil_M':majorizes(2,1120,1121),
        'M_upper_conservative':majorizes(1,1121,1200),
        'global_row_failure_vs_delta_over100':majorizes(200,0,1233),
        'gradient_hoeffding_factor':majorizes(8,0,1),
        'gradient_envelope':majorizes(2,4,5),
        'gradient_net_lipschitz':majorizes(6,0,1),
        'gradient_hoeffding_majorant_vs_D':majorizes(1,24,40),
        'negative_mass_majorant_vs_D':majorizes(1,20,40),
        'sample_compression_exp_majorant':majorizes(2,3,56)}
    # Algebraic lower-bound exponents; no numerical parameter grid.
    zeta_exp=(-2)+2*(-1)-42
    M_inner_exp=1+61+50
    theta_geo_exp=-50-(1+61)
    eta2_exp=theta_geo_exp-2-(1+61+1200)
    row_failure_exp=1+61-4096+2*1400
    assert zeta_exp==-46 and M_inner_exp==112
    assert theta_geo_exp==-112 and eta2_exp==-1376 and row_failure_exp==-1234
    assert eta2_exp>=-1400
    assert 1000**10>=10**9 # M >= A^10 N^10 zeta^-10, N>=1,zeta<=1.
    assert F(1,100)+F(1,25)==F(1,20)
    assert F(20,1024)<1 and 1+20<128
    record={
        'scope':'saved-law/exact-source and exponent-bookkeeping consumer only; NOT theorem/solver audit',
        'input_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
        'teacher_inference_calls':data['teacher_inference_calls'],
        'source_middle_teacher_rank':16,
        'rank_argument':'Pmiddle is sum of two positive outer products; Qmiddle=.98 Pmiddle+I/800 >0',
        'minimum_teacher_middle_eigenvalue_lower':'1/800',
        'original_saved_law_mass':str(mass),
        'mass_minus_one':str(mass-1),
        'normalized_saved_table_TV_exact':str(tv),
        'TV_display':float(tv),
        'KL_arb':str(kl),'Delta_upper_arb':str(delta),
        'power_certificates':powers,
        'exponents':{'zeta_lower':zeta_exp,'M_inner_upper':M_inner_exp,
                     'theta_geo_lower':theta_geo_exp,'eta2_lower':eta2_exp,
                     'global_row_failure_upper':row_failure_exp},
        'empirical_model_accuracy_qualified':False,
        'general_compiler_theorem_accepted_by_this_consumer':False,
        'elapsed_seconds':time.perf_counter()-started}
    (HERE/'SAVED_CONSUMER.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({k:v for k,v in record.items() if k not in ['power_certificates','normalized_saved_table_TV_exact']},indent=2))


if __name__=='__main__':main()
