"""Try the stronger-than-needed coefficient-in-b² positivity certificate.

Exact univariate Sturm checks, not a positivity inference from a grid.
If this sufficient certificate fails the angular problem remains open.
"""
from pathlib import Path
import hashlib,json,time
import sympy as S


def strip_endpoints(p,d):
    for root in (-1,1):
        factor=S.Poly(d-root,d)
        while p.degree()>0 and p.eval(root)==0:p=p.exquo(factor)
    return p


def main():
    start=time.perf_counter();here=Path(__file__).parent
    raw=json.loads((here/'PROFILE_CANDIDATE.json').read_text());b,d=S.symbols('b d',real=True)
    checks=[];bad=[]
    for minor in raw['leading_minors']:
        assert S.Rational(minor['constant'])>0
        for factor_index,(text,power) in enumerate(minor['factors']):
            P=S.Poly(S.sympify(text,locals={'b':b,'d':d}),b,d)
            assert all(e[0]%2==0 for e,c in P.terms())
            maxpower=P.degree(b)//2
            for j in range(maxpower+1):
                p=S.Poly(sum(c*d**e[1]for e,c in P.terms()if e[0]==2*j),d)
                if p.is_zero:continue
                sturm_base=strip_endpoints(p,d)
                odd=[]
                for f,m in sturm_base.sqf_list()[1]:
                    if m%2:odd.append(int(f.count_roots(-1,1)))
                witness=next(S.Rational(1,k)for k in range(2,100)if p.eval(S.Rational(1,k))!=0)
                value=p.eval(witness);nonnegative=bool((not any(odd)) and value>0)
                rootcount=int(sturm_base.count_roots(-1,1))
                record={'minor':minor['k'],'factor':factor_index,'b2_power':j,
                        'coefficients_low_to_high':[str(c)for c in reversed(p.all_coeffs())],
                        'odd_root_counts':odd,'test_point':str(witness),'test_value':str(value),
                        'all_interior_roots':rootcount,'nonnegative_on_interval':nonnegative}
                checks.append(record)
                if not nonnegative:bad.append(record)
            print('checked minor',minor['k'],'factor',factor_index,'badsofar',len(bad),flush=True)
    zero_coeffs=[r for r in checks if r['b2_power']==0]
    strict=all(bool(r['all_interior_roots']==0 and S.Rational(r['test_value'])>0)for r in zero_coeffs)
    out={'scope':'exact sufficient factor/coefficient Sturm certificate for one rational angular primitive',
         'all_nonnegative':not bad,'constant_b2_coefficients_strict_interior':strict,
         'check_count':len(checks),'failures':bad,'checks':checks,
         'seconds_after_imports':time.perf_counter()-start,
         'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'input_sha256':hashlib.sha256((here/'PROFILE_CANDIDATE.json').read_bytes()).hexdigest()}
    (here/'UNIVARIATE_CERTIFICATE.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k]for k in ('all_nonnegative','constant_b2_coefficients_strict_interior','check_count','seconds_after_imports')},indent=2))
    print('failures',[(r['minor'],r['factor'],r['b2_power'],r['odd_root_counts'])for r in bad])


if __name__=='__main__':main()
