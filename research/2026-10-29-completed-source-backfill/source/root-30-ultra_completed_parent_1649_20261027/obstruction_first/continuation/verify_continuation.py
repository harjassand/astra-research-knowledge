"""Independent Fraction replay of the actual A4 beta3/4 warm certificate.

No producer imports or mpmath arithmetic. Exact CRT integers are inputs.
This does not repeat every modular multiplication on chains4..6.
"""
import pathlib,json,math
from fractions import Fraction as F
ROOT=pathlib.Path(__file__).resolve().parent
class I:
    def __init__(s,a,b=None):s.a=F(a);s.b=F(a if b is None else b);assert s.a<=s.b
    def __add__(x,y):y=toI(y);return I(x.a+y.a,x.b+y.b)
    __radd__=__add__
    def __neg__(x):return I(-x.b,-x.a)
    def __sub__(x,y):return x+-toI(y)
    def __rsub__(x,y):return toI(y)+-x
    def __mul__(x,y):
        y=toI(y);v=[x.a*y.a,x.a*y.b,x.b*y.a,x.b*y.b];return I(min(v),max(v))
    __rmul__=__mul__
    def __truediv__(x,y):
        y=toI(y);assert not y.a<=0<=y.b;return x*I(1/y.b,1/y.a)
    def __rtruediv__(x,y):return toI(y)/x
    def __pow__(x,n):
        assert n>=0
        if n==0:return I(1)
        if n%2 or x.a>=0:return I(x.a**n,x.b**n)
        if x.b<=0:return I(x.b**n,x.a**n)
        return I(0,max(x.a**n,x.b**n))
def toI(x):return x if isinstance(x,I)else I(x)
def exp_pos(x):
    x=F(x);assert 0<=x<258;term=F(1);s=term
    for k in range(1,257):term*=x/k;s+=term
    return I(s,s+term*x/257/(1-x/258))
def trace_box(rec,beta,norm):
    d=rec['degree'];value=sum(F(int(v))*(-beta/2)**k/math.factorial(k)for k,v in enumerate(rec['trace_2H_powers']))
    x=norm*beta;error=5**rec['n']*exp_pos(x).b*x**(d+1)/math.factorial(d+1)
    return I(value-error,value+error)
def analytic_check(records):
    spectra={1:[(5,0)],2:[(1,-6),(3,-5),(5,-3),(7,0),(9,4)],3:[]}
    for a in range(5):
        for j in range(abs(a-2),a+3):spectra[3].append((2*j+1,(j*(j+1)-a*(a+1)-6)//2))
    for n,s in spectra.items():
        for k,v in enumerate(records[n]['trace_2H_powers']):assert int(v)==sum(deg*(2*e)**k for deg,e in s)
    for r in records.values():
        n=r['n'];degree=r['degree']
        if n>1:
            product=math.prod(r['CRT_primes']);assert product==int(r['CRT_modulus'])
            assert product>2*5**n*(12*(n-1))**degree
        for k,v in enumerate(r['trace_2H_powers']):assert abs(int(v))<=5**n*(12*(n-1))**k
def run():
    data=json.loads((ROOT/'data/open_moments_exact_degree192.json').read_text());recs={r['n']:r for r in data['chains']};analytic_check(recs)
    old=json.loads((ROOT/'data/open_moments_exact_degree96.json').read_text())
    for r in old['chains']:assert r['trace_2H_powers']==recs[r['n']]['trace_2H_powers'][:97]
    output=json.loads((ROOT/'data/vacuum_krylov_transfer_degree192_A4.json').read_text())
    row=next(r for r in output['rows']if r['beta_exact']=='0.75');beta=F(3,4)
    m=[I(1)]+[trace_box(recs[r],beta,F(6*(r-1)))/(5**r)for r in range(1,7)]
    c=[I(F(s))for s in row['candidate_rational_decimal_coefficients']]
    def quadratic(off):return sum(c[i]*c[j]*m[i+j+off]for i in range(3)for j in range(3))
    den=quadratic(0);assert den.a>0;theta=quadratic(1)/den;variance=quadratic(2)/den-theta**2;assert variance.b>=0
    total=I(0)
    for a in range(5):
        for b in range(5):
            for j in range(abs(a-b),a+b+1):
                e=(j*(j+1)-a*(a+1)-b*(b+1))//2;q=exp_pos(abs(beta*e));q=q if e<=0 else 1/q
                total+=(2*j+1)*q/625
    tw=json.loads((ROOT/'data/twisted4_moments_exact_degree192.json').read_text());vals={}
    for rec in tw['records']:
        vals[rec['twist']]=trace_box(dict(rec,n=4),beta,F(24))/625
        assert rec['trace_2H_powers'][:4]==['625','0','120000','-120000']
    invariant=(total+3*vals['P']+8*vals['C'])/12;comp=total-invariant;rem=invariant-I(theta.a)**4
    assert rem.a>=0 and comp.a>=0
    raw=F(str(row['all_other_moduli_J_upper']));radius=F(math.ceil(raw*10**10),10**10)
    assert radius**4>=rem.b and radius**4>=comp.b/3 and theta.a>radius
    top_upper=theta.b+variance.b/(theta.a-radius)
    mass=total-I(theta.a)**4;tail=mass.b*radius**252/theta.a**256
    defect=(2*tail+tail**2)/(1+tail)**2;assert defect<F(2,10**24)
    propagated=128*defect/(1-defect);assert propagated<F(3,10**22)
    compiler=json.loads((ROOT/'data/thermal_purity_lift.json').read_text())['acquired_A4_warm_restart']
    assert compiler['L']==256 and compiler['cold_beta']==96 and not compiler['cold_seed_acquired']
    budget=F(compiler['propagated_initial_log_error_upper'])
    for k,r in enumerate(compiler['thermal_input_table']):
        assert not r['thermal_inputs_acquired']
        budget+=3*2**(6-k)*F(r['required_each_log_purity_error_at_most'])
    assert budget<=F(1,1000)
    cold=json.loads((ROOT/'data/cold_moment_boundary.json').read_text())
    assert F(cold['positive_eigenvalue_margin_lower_rational'])>0
    assert exp_pos(F(396,1000)*64).a/7500-1>13542475
    result={'status':'PASS_INDEPENDENT_FRACTION_A4_WARM_REPLAY','beta':'3/4','L':256,
        'spatial_defect_upper_float':math.nextafter(float(defect),math.inf),
        'seven_doubling_initial_log_error_upper_float':math.nextafter(float(propagated),math.inf),
        'Perron_separation_lower_float':math.nextafter(float(theta.a-radius),-math.inf),
        'Perron_log_width_upper_via_ratio_float':math.nextafter(float((top_upper-theta.a)/theta.a),math.inf),
        'scope':'Exact rational replay of trace/Taylor/rotation-count/residual/tail from integer moments; analytic chains1..3 checked through192 and96/192 consistency checked. Does not regenerate every CRT multiplication on4..6 or the open5 dyadic matrix products.'}
    (ROOT/'data/continuation_verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2));return result
if __name__=='__main__':run()
