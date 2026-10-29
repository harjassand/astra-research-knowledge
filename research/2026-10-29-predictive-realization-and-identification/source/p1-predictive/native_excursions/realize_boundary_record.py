"""Compile a public acquired record into a positive small Markov model.

The original-source uncertainty remains in the separate certificate. No
private source or acquisition backend is imported.
"""
from pathlib import Path
from fractions import Fraction as F
import json,time,hashlib
from consume_excursion_record import solve,stringify

ROOT=Path(__file__).resolve().parent

def main():
    started=time.perf_counter();p=ROOT/'macro_run'
    certbytes=(p/'NATIVE_EXCURSION_CERTIFICATE.json').read_bytes()
    cert=json.loads(certbytes)
    between=json.loads((p/'BETWEEN_REGION_CERTIFICATE.json').read_text())
    groups=cert['input_contracts']['module_ports'];m=sum(map(len,groups))
    slo=list(map(F,cert['stationary_event_lower']));shi=list(map(F,cert['stationary_event_upper']))
    ulo=list(map(F,cert['u_lower']));uhi=list(map(F,cert['u_upper']))
    vlo=list(map(F,cert['v_lower']));vhi=list(map(F,cert['v_upper']))
    w=[(slo[i]+shi[i])/2 for i in range(m)]
    v=[(slo[i]*ulo[i]+shi[i]*uhi[i])/2 for i in range(m)]
    b=[w[i]+v[i] for i in range(m)]
    S=[[(F(cert['S_lower'][i][j])+F(cert['S_upper'][i][j]))/2 for j in range(m)] for i in range(m)]
    cs=[sum(slo[i]*vlo[i]+shi[i]*vhi[i] for i in g)/4 for g in groups]
    gammas=[sum(v[i] for i in g)/cs[k] for k,g in enumerate(groups)]
    assert min(w)>0 and min(v)>0 and min(cs)>0
    weights=w+v
    conductance=[[F(0) for _ in range(2*m)] for _ in range(2*m)]
    for i in range(m):
        for j in range(m):
            if i!=j:conductance[i][j]=-S[i][j]
    for k,g in enumerate(groups):
        for i in g:conductance[i][m+i]=conductance[m+i][i]=gammas[k]*v[i]
    L=[[sum(conductance[i]) if i==j else -conductance[i][j] for j in range(2*m)] for i in range(2*m)]
    Q=[[-L[i][j]/weights[i] for j in range(2*m)] for i in range(2*m)]
    assert all(sum(row)==0 for row in Q)
    assert all(Q[i][j]>=0 for i in range(2*m) for j in range(2*m) if i!=j)
    assert all(weights[i]*Q[i][j]==weights[j]*Q[j][i] for i in range(2*m) for j in range(2*m))
    reconstructed_S=[[L[i][j]-L[i][m+i]*L[m+i][j]/L[m+i][m+i] for j in range(m)] for i in range(m)]
    assert reconstructed_S==S
    assert all(w[i]-L[i][m+i]*v[i]/L[m+i][m+i]==b[i] for i in range(m))
    assert all(sum(v[i]*v[i]/L[m+i][m+i] for i in g)==cs[k] for k,g in enumerate(groups))
    prepared_queries=[]
    for amask in range(1,(1<<len(groups))-1):
        A=[k for k in range(len(groups)) if amask>>k&1]
        R=[i for k,g in enumerate(groups) if k not in A for i in g]
        kept=R+[m+i for i in R]
        h=solve([[L[i][j] for j in kept] for i in kept],[weights[i] for i in kept])
        boundary_h=solve([[S[i][j] for j in R] for i in R],[b[i] for i in R])
        assert all(h[kept.index(i)]==boundary_h[R.index(i)] for i in R)
        for cmask in range(1,1<<len(groups)):
            if cmask&amask:continue
            C=[k for k in range(len(groups)) if cmask>>k&1]
            Cp=[i for k in C for i in groups[k]]
            Cstates=Cp+[m+i for i in Cp]
            exact=sum(weights[i]*h[kept.index(i)] for i in Cstates)/sum(weights[i] for i in Cstates)
            compressed=(sum(cs[k] for k in C)+sum(b[i]*boundary_h[R.index(i)] for i in Cp))/sum(b[i] for i in Cp)
            assert exact==compressed
            released=next(q for q in between['queries'] if q['source_modules']==C and q['target_modules']==A)
            lower=F(released['lower']);upper=F(released['upper'])
            assert lower<=exact<=upper
            prepared_queries.append({'source_modules':C,'target_modules':A,'prepared_mean':exact,
                'prepared_mean_display':float(exact),'original_source_interval':[lower,upper],
                'same_acquired_event':True})
    values=weights+[x for row in Q for x in row]
    out={'schema':'astra.positive_mean_realization.v1','ports':m,'states':len(weights),
        'source_hidden_dimension_used':False,'source_model_reads':0,'new_source_observations':0,
        'input_certificate_sha256':hashlib.sha256(certbytes).hexdigest(),
        'source_confidence_failure_upper':cert['failure_probability_upper'],
        'weights':weights,'conductances':conductance,'generator':Q,'module_ports':groups,
        'module_leaf_exit_rates':gammas,'module_leaf_exit_rates_display':list(map(float,gammas)),
        'point_record':{'S':S,'b':b,'v':v,'c_by_module':cs,'w_B':w},
        'query_count':len(prepared_queries),'queries':prepared_queries,
        'max_coefficient_numerator_bits':max(x.numerator.bit_length() for x in values),
        'max_coefficient_denominator_bits':max(x.denominator.bit_length() for x in values),
        'wall_seconds':time.perf_counter()-started,
        'meaning':'exact representative of the prepared point record, not identification of the original process',
        'scope':'means between declared equilibrium-conditioned module unions; original-source uncertainty retained; port holding rates and survival laws not preserved',
    }
    (p/'POSITIVE_MEAN_REALIZATION.json').write_text(json.dumps(stringify(out),indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['ports','states','query_count','module_leaf_exit_rates_display','max_coefficient_numerator_bits','max_coefficient_denominator_bits','wall_seconds','new_source_observations']},indent=2))

if __name__=='__main__':main()
