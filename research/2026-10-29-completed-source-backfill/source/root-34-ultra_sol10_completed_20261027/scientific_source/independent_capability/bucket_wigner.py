"""Exact positive-axis root/sign certificates and numeric negativity volumes.

This is a diagnostic of the constructed state, not an independent audit of
the factory source. Root counts/signs are rational algebra; areas are mpmath
numerics without interval enclosure.
"""
import contextlib,io,json,time
from pathlib import Path
from fractions import Fraction as Q
from math import comb,factorial
import sympy as s
import mpmath as mp
with contextlib.redirect_stdout(io.StringIO()):
    import bucket_factory as b

mp.mp.dps=80
xx=s.symbols('x');OUT=Path(__file__).resolve().parent/'outputs'
def evaluate_state(q,label):
    start=time.perf_counter()
    coeff=[sum(q[k]*(-1)**(k+j)*comb(k,j) for k in range(j,len(q)))/factorial(j) for j in range(len(q))]
    PP=s.Poly.from_list([s.Rational(z.numerator,z.denominator) for z in reversed(coeff)],xx)
    _,P=PP.clear_denoms();_,P=P.primitive()
    assert s.degree(s.gcd(P,P.diff()))==0
    nr=int(P.count_roots(0,s.oo))
    intervals=P.intervals(eps=s.Rational(1,10**6),inf=0)
    assert len(intervals)==nr and all(mult==1 for _,mult in intervals)
    co=[mp.mpf(v.numerator)/v.denominator for v in coeff]
    def f(t):
        ans=mp.mpf(0)
        for v in reversed(co):ans=ans*t+v
        return ans
    def torat(z):return Q(int(s.numer(z)),int(s.denom(z)))
    def tomp(z):return mp.mpf(int(s.numer(z)))/int(s.denom(z))
    roots=[]
    for (lo,hi),_ in intervals:
        if lo==hi:roots.append(tomp(lo))
        else:roots.append(mp.findroot(f,(tomp(lo),tomp(hi)),solver='bisect',tol=mp.mpf('1e-60'),maxsteps=250))
    edges=[mp.mpf(0)]+roots
    # All constructed photon distributions have positive even-degree tail.
    assert f(roots[-1]+100)>0
    negative_intervals=[];neg=mp.mpf(0)
    for j,(aa,bb) in enumerate(zip(edges[:-1],edges[1:])):
        mid=(aa+bb)/2
        if f(mid)<0:
            neg-=mp.quad(lambda t:mp.exp(-t/2)*f(t)/2,[aa,bb])
            if j==0:lower=Q(0)
            else:lower=torat(intervals[j-1][0][1])
            upper=torat(intervals[j][0][0])
            witness=(lower+upper)/2
            value=sum(c*witness**k for k,c in enumerate(coeff))
            assert value<0
            negative_intervals.append({'witness_t_exact':str(witness),
                                       'Wigner_polynomial_sign_exact':-1,
                                       'scaled_Wigner_at_witness_numeric':float(2/mp.pi*mp.exp(-mp.mpf(witness.numerator)/witness.denominator/2)*f(mp.mpf(witness.numerator)/witness.denominator))})
    return {'label':label,'degree':P.degree(),'positive_roots_exact':nr,
            'squarefree_exact':True,'P0_sign_exact':int(s.sign(P.eval(0))),
            'negative_radial_intervals_exact':len(negative_intervals),
            'negative_point_certificates':negative_intervals,
            'negative_volume_numeric':float(neg),
            'area_scope':'80-digit quadrature diagnostic, not interval certified',
            'elapsed_seconds':time.perf_counter()-start}

rows=[evaluate_state(list(b.p),'one_source')]
for n in [2,4,8,16]:
    st=b.law(n,b.p,b.det)
    q=[v/st['Z'] for v in b.output_coefficients(st,b.det)]
    rows.append(evaluate_state(q,'factory_'+str(n)))
result={'status':'EXACT_ROOT_AND_SIGN_CERTIFICATES; numeric volumes not interval certified',
        'states':rows,'scope':'No monotonicity in all n and no practical approximate stellar-rank or computational-resource claim'}
(OUT/'BUCKET_WIGNER_REPLAY.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='states'}))
for r in rows:print(json.dumps({k:r[k] for k in ['label','positive_roots_exact','negative_radial_intervals_exact','negative_volume_numeric','elapsed_seconds']}))
