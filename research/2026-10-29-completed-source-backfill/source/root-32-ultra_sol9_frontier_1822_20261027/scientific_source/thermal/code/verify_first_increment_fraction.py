"""Independent stdlib-Fraction replay of the first connected increment.

No producer import, eigensolver, mpmath, Chebyshev routine or numeric trace
proposal is used. The only data inputs are exact saved CRT integers.
"""
from fractions import Fraction as F
import pathlib,json,math,time,functools,hashlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
PRIOR=ROOT.parents[1]/'sol8_opportunity_selection_20261027/obstruction_first/continuation'

def add(a,b):return a[0]+b[0],a[1]+b[1]
def scale(a,c):return (a[0]*c,a[1]*c)if c>=0 else(a[1]*c,a[0]*c)
def sub(a,b):return add(a,scale(b,-1))
@functools.lru_cache(None)
def exp_bounds(x):
    x=F(x)
    if x<0:
        lo,hi=exp_bounds(-x);return 1/hi,1/lo
    degree=max(100,2*math.ceil(x)+100)
    term=F(1);total=F(1)
    for k in range(1,degree+1):term*=x/k;total+=term
    nxt=term*x/(degree+1);ratio=x/(degree+2)
    assert ratio<1
    return total,total+nxt/(1-ratio)

def thermal(rec,beta,bonds):
    if bonds==0:return F(5),F(5)
    mom=list(map(int,rec['trace_2H_powers']));d=len(mom)-1
    t=-beta/2;power=F(1);factorial=1;value=F(0)
    for k,v in enumerate(mom):
        if k:power*=t;factorial*=k
        value+=v*power/factorial
    x=6*bonds*beta
    tail=5**rec['n']*exp_bounds(x)[1]*x**(d+1)/math.factorial(d+1)
    return value-tail,value+tail

def z4(beta):
    value=(F(0),F(0))
    for a in range(5):
        for b in range(5):
            for j in range(abs(a-b),a+b+1):
                e=(j*(j+1)-a*(a+1)-b*(b+1))//2
                value=add(value,scale(exp_bounds(-beta*e),F(2*j+1,625)))
    return value

def quadratic(c,m,offset):
    val=(F(0),F(0))
    for i,a in enumerate(c):
        for j,b in enumerate(c):val=add(val,scale(m[i+j+offset],a*b))
    return val

def run():
    start=time.monotonic()
    paths={'open':PRIOR/'data/open_moments_exact_degree192.json',
           'twist4':PRIOR/'data/twisted4_moments_exact_degree192.json',
           'cycle6':ROOT/'results/cycle6_moments_exact_degree192.json'}
    inputs={k:json.loads(p.read_text())for k,p in paths.items()}
    op={r['n']:r for r in inputs['open']['chains']}
    tw={r['twist']:dict(r,n=4)for r in inputs['twist4']['records']}
    six={r['twist']:r for r in inputs['cycle6']['records']}
    assert set(six)=={'I','P'}
    rows=[];tails=[]
    choices=[(F(3,4),[F(16,1250),F(-91,100),F(-1)],F(233,25),F(3),F(21,5),F(184,25),4),
             (F(3,2),[F(37,100),F(-1),F(-17,1000)],F(285),F(141),F(197),F(257),6)]
    for beta,c,theta,ri,ro,rn,pn in choices:
        m=[(F(1),F(1))]+[scale(thermal(op[r],beta,r-1),F(1,5**r))for r in range(1,7)]
        g=quadratic(c,m,0);h=quadratic(c,m,1)
        assert g[0]>0
        margin=h[0]-theta*g[1];assert margin>0
        zz=z4(beta);p4=scale(thermal(tw['P'],beta,4),F(1,625));c4=scale(thermal(tw['C'],beta,4),F(1,625))
        i4=scale(add(add(zz,scale(p4,3)),scale(c4,8)),F(1,12))
        o4=scale(sub(add(zz,scale(p4,3)),scale(c4,4)),F(1,12))
        if pn==4:nn=scale(sub(zz,p4),F(1,4))
        else:nn=scale(sub(thermal(six['I'],beta,6),thermal(six['P'],beta,6)),F(1,4*5**6))
        assert i4[1]-theta**4 < ri**4
        assert F(0)<o4[0]<=o4[1]<ro**4
        assert F(0)<nn[0]<=nn[1]<rn**pn
        tau=(ri/theta)**256+2*(ro/theta)**256+3*(rn/theta)**256
        tails.append(tau)
        rows.append({'beta_exact':str(beta),'candidate_coefficients':list(map(str,c)),
                     'theta_strict_lower':str(theta),'rI_strict_upper':str(ri),
                     'rO_strict_upper':str(ro),'rN_strict_upper':str(rn),'N_moment':pn,
                     'Rayleigh_positive_margin':str(margin),
                     'complete_loop_tail_upper_rational':str(tau)})
    assert 2*tails[1]<F(3,10**11)
    assert 4*tails[0]<F(1,10**24)
    result={'status':'PASS_EXACT_FRACTION_FIRST_CONNECTED_THERMAL_INCREMENT',
            'quantity':'log T512(3/4) - 2 log T256(3/4)',
            'strict_lower':'-3/100000000000','strict_upper':'1/1000000000000000000000000',
            'logS256_beta3over2_strict_lower':'-3/100000000000',
            'one_minus_S256_beta3over2_strict_upper':'3/100000000000',
            'all_comparisons_exact_rational':True,'rows':rows,
            'source_receipts':{k:{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}for k,p in paths.items()},
            'seconds':time.monotonic()-start,
            'scope':'One actual connected dyadic increment; no individual fine cold log-purity, remaining increment, final T512(96), or uniform gap.'}
    (ROOT/'results/first_increment_fraction_replay.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items()if k not in ['rows','source_receipts']},indent=2))

if __name__=='__main__':run()
