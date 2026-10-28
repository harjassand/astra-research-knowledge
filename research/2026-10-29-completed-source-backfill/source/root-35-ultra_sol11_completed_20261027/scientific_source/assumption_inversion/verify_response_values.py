"""Independent stdlib Fraction reconstruction of two critical response cases.

No producer imports. Uses actual Fraction state vectors rather than common-
denominator integer propagation. Checks the discrete Duhamel identity at every
step, all four truncated sums, and the uniformization certificates. Independently
encloses exp(-8) using the alternating exp(-1) series raised to the eighth power.
"""
from fractions import Fraction as R
from pathlib import Path
import json
import math
import time

OUT=Path(__file__).resolve().parent


def exp8_bounds():
    term=R(1)
    total=R(1)
    for k in range(1,100):
        term*=-R(1,k)
        total+=term
    #99 is odd: S99<exp(-1)<S100.
    lo=total
    hi=total-term/R(100)  # term is negative, next term positive.
    assert 0<lo<hi
    return lo**8,hi**8


def main():
    start=time.monotonic()
    data=json.loads((OUT/'EXACT_COMPARISON.json').read_text())
    eleft,eright=map(R,data['exp_negative_interval'])
    independent_l,independent_h=exp8_bounds()
    assert eleft<independent_l<independent_h<eright
    checked=[]
    for case in data['rows']:
        # Two extremes of the parameter precision at the smallest state size.
        if case['n']!=64 or case['eta'] not in ['1/100','1/100000000000000000000']:
            continue
        inp=json.loads((OUT/case['input']['path']).read_text())
        n=inp['n']
        rows=[[(j,R(w,8)) for j,w in row] for row in inp['P_numerator_rows']]
        eta=R(case['eta'])
        kills=set(inp['D_nonzero_unit_diagonal'])
        block,generic,jets,direct=case['methods']
        assert block['m']==generic['m']==jets['m']
        mblock=block['m']
        mmax=max(mblock,direct['m'])
        K=jets['K']
        u=[R(x,8) for x in inp['b_numerators']]
        v=u[:]
        z=[R(0)]*n
        tower=[u[:]]+[[R(0)]*n for _ in range(K)]
        coefficient=R(1)
        sz,su,sv=R(0),R(0),R(0)
        sj=[R(0)]*(K+1)

        def p0_action(vec):
            return [sum((w*vec[j] for j,w in row),R(0)) for row in rows]

        for k in range(mmax+1):
            assert all(eta*z[i]==u[i]-v[i] for i in range(n))
            if k<=mblock:
                sz+=coefficient*z[0]
                for j in range(1,K+1):
                    sj[j]+=coefficient*tower[j][0]
            if k<=direct['m']:
                su+=coefficient*u[0]
                sv+=coefficient*v[0]
            if k==mmax:
                break
            old_u=u
            u=p0_action(u)
            new_v=p0_action(v)
            new_z=p0_action(z)
            for i in kills:
                new_v[i]-=eta*v[i]/2
                new_z[i]+=(old_u[i]-eta*z[i])/2
            v,z=new_v,new_z
            if k<mblock:
                ntower=[p0_action(vec) for vec in tower]
                for j in range(1,K+1):
                    for i in kills:
                        ntower[j][i]+=tower[j-1][i]/2
                tower=ntower
            coefficient*=R(8,k+1)
        assert sz==R(block['partial_sum'])==R(generic['partial_sum'])
        assert [su,sv]==list(map(R,direct['partial_sums']))
        assert sj==list(map(R,jets['partial_sums']))

        def tail(after):
            assert after+2>8
            return eright*R(8)**(after+1)/math.factorial(after+1)/(1-R(8,after+2))

        block_bounds=(eleft*sz,eright*sz+R(7)*tail(mblock-1))
        assert block_bounds==tuple(map(R,[block['lower'],block['upper']]))
        bmax=R(7,4)
        dl=(eleft*su-eright*sv-bmax*tail(direct['m']))/eta
        dh=(eright*su+bmax*tail(direct['m'])-eleft*sv)/eta
        assert (dl,dh)==tuple(map(R,[direct['lower'],direct['upper']]))
        jl,jh=R(0),R(0)
        for j in range(1,K+1):
            lo=eleft*sj[j]
            hi=eright*sj[j]+bmax*R(4)**j/math.factorial(j)*tail(mblock-j)
            factor=eta**(j-1)
            if j%2:
                jl+=factor*lo
                jh+=factor*hi
            else:
                jl-=factor*hi
                jh-=factor*lo
        remainder=eta**K*bmax*R(4)**(K+1)/math.factorial(K+1)
        assert remainder==R(jets['remainder_bound'])
        if K%2:
            jl-=remainder
        else:
            jh+=remainder
        assert (jl,jh)==tuple(map(R,[jets['lower'],jets['upper']]))
        assert max(block_bounds[0],dl,jl)<=min(block_bounds[1],dh,jh)
        assert all(R(m['upper'])-R(m['lower'])<=R(1,10**12) for m in case['methods'])
        checked.append({'n':n,'eta':str(eta),'discrete_identity_steps':mmax+1,
                        'jet_order':K,'all_four_truncated_sums':'EXACTLY_RECONSTRUCTED',
                        'all_four_intervals':'EXACTLY_RECONSTRUCTED'})
    # Every saved case passes its declared precision and comparator arithmetic.
    for case in data['rows']:
        for m in case['methods']:
            assert R(m['lower'])<=R(m['upper'])
            assert R(m['upper'])-R(m['lower'])<=R(case['tolerance'])
        best=min(m['full_query_seconds'] for m in case['methods'][:3])
        assert best==case['ordinary_best_seconds']
        assert case['candidate_to_best_ordinary_ratio']>=1
    out={'status':'INDEPENDENT_FRACTION_RECONSTRUCTION_PASSED','critical_cases':checked,
         'all_saved_cases_precision_checked':len(data['rows']),
         'exp_minus8':'INDEPENDENT_ALTERNATING_SERIES_ENCLOSURE',
         'seconds':time.monotonic()-start,
         'scope':'Full independent state-vector reconstruction for two n64 cases; '
                 'precision and comparator arithmetic for all12. The finite checks do not establish '
                 'new-method novelty, a general performance theorem, or physical acquisition.'}
    (OUT/'INDEPENDENT_RESPONSE_REPLAY.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':
    main()
