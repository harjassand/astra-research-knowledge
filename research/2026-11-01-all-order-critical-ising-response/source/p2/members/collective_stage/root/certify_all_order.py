"""Exact rational statistical enclosure from the all-order sampler histogram.

Four one-sided empirical Bernstein bounds (Maurer--Pontil, Theorem 4),
one each for lower/upper U and lower/upper W. The observed dyadic endpoints
are separate bounded random variables, so finite-precision errors remain
enclosed even at unseen endpoints. Fixed sample count; no optional stopping.
"""
import argparse
import json
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
from time import perf_counter
from all_order_response import potential_num, scores, dyadic_outer, alpha_interval


def sqrt_upper(x, bits=128):
    scale = 1 << bits
    q = isqrt((x.numerator*scale*scale)//x.denominator)
    if q*q*x.denominator < x.numerator*scale*scale:
        q += 1
    return F(q, scale)


def log_upper(x, bits=128):
    """Rational log(x) upper, using atanh series after range reduction."""
    assert x >= 1
    power = 0
    while x >= 2:
        x /= 2
        power += 1
    def series(y):
        z=(y-1)/(y+1); z2=z*z
        value=F(0); term=z
        for k in range(1, bits+1):
            value += term/(2*k-1)
            term *= z2
        tail=term/((2*bits+1)*(1-z2))
        return 2*(value+tail)
    return power*series(F(2))+series(x)


def certify(path=None, failure=F(1,20), bits=100, precomputed=None):
    started=perf_counter()
    record=json.loads(Path(path).read_text()) if precomputed is None else precomputed[0]
    n,m=record['n'],record['samples']; scale=1<<bits
    a,b=F(n*n-1,3*(n*n+1)),F(1,3)
    d=2*a; kappa=F(4,3*(n*n+1))
    a0,c0=a+2*b/n,a+b; theta0=a0/c0; h0=F(n-2,n)
    epsilon=(d-b)/3+2*b/n
    umax,wmax=h0/epsilon,h0/c0
    sums={k:0 for k in ('ul','uu','wl','wu')}; squares=dict(sums)
    max_score_width=F(0)
    for row in record.get('terminal_histogram',[]):
        s=tuple(row['state']); count=row['count']
        u,wl,wu=scores(n,s,potential_num(s,n),bits)
        ul,uu=dyadic_outer(u,bits)
        wli,_=dyadic_outer(wl,bits);_,wui=dyadic_outer(wu,bits)
        values={'ul':ul,'uu':uu,'wl':wli,'wu':wui}
        for k,v in values.items():sums[k]+=count*v;squares[k]+=count*v*v
        max_score_width=max(max_score_width,F(wui-wli,scale))
    if precomputed is None:
        assert sum(row['count'] for row in record['terminal_histogram'])==m
    else:
        _,sums,squares,max_score_width=precomputed
    log=log_upper(8/failure)
    means={};variances={};radii={}
    for k in sums:
        means[k]=F(sums[k],m*scale)
        variances[k]=F(m*squares[k]-sums[k]*sums[k],m*(m-1)*scale*scale)
        width=(umax if k.startswith('u') else wmax)+F(1,scale)
        radii[k]=sqrt_upper(2*variances[k]*log/m)+7*width*log/(3*(m-1))
    ul=max(F(0),means['ul']-radii['ul']); uu=min(umax,means['uu']+radii['uu'])
    wl=max(F(0),means['wl']-radii['wl']); wu=min(wmax,means['wu']+radii['wu'])
    lower=theta0+b*wl/(1+b*uu); upper=theta0+b*wu/(1+b*ul)
    point=theta0+b*((means['wl']+means['wu'])/2)/(1+b*(means['ul']+means['uu'])/2)
    # Fully acquired all-odd event-work potential.
    u0=F((n-2)*(n-1),6*n)
    event_bound=3*u0/(d*h0)*(1+b*h0/epsilon)
    # Var(M)=n*(1+t)/(1-t)*(1-t^n)/(1+t^n); t=(n-1)/(n+1).
    # At this critical family, (1+t)/(1-t)=n.
    dy=alpha_interval((0,),n,bits)  # Also exercises the singleton static endpoint.
    assert dy[0] <= dy[2] <= dy[1]
    from all_order_response import Dyadic
    ar=Dyadic(bits);tn=ar.power(ar.frac(F(n-1,n+1)),n)
    varl=F(n*n*(scale-tn[1]),scale+tn[1])
    varu=F(n*n*(scale-tn[0]),scale+tn[0])
    chil, chiu=lower*varl/kappa,upper*varu/kappa
    # Exact same conventional potential/reference-current comparison.
    t=F(n-1,n+1)
    p=(1-t*t)*(1+t**(n-2))/(2*(1-t**n))
    same,opp=1-b,1+b
    conventional_l=(1-b)/(same*p+opp*(1-p))
    conventional_u=(1-b)*(p/same+(1-p)/opp)
    out={
        'n':n,'samples':m,'confidence_at_least':str(1-failure),
        'arithmetic':'Exact rational confidence bounds; outward dyadic static reward; exact integer transition law.',
        'theta_definition':'kappa chi_M / Var(M), kappa=4/[3(n^2+1)]',
        'theta_interval':[float(lower),float(upper)],'theta_point':float(point),
        'theta_exact':[{'num':str(x.numerator),'den':str(x.denominator)} for x in (lower,upper)],
        'chi_interval':[float(chil),float(chiu)],
        'chi_exact':[{'num':str(x.numerator),'den':str(x.denominator)} for x in (chil,chiu)],
        'relative_interval_width':float((upper-lower)/lower),
        'midpoint_max_relative_error':float((upper-lower)/(upper+lower)),
        'conventional_first_moment_theta':[float(conventional_l),float(conventional_u)],
        'conventional_relative_width':float((conventional_u-conventional_l)/conventional_l),
        'mean_U':float((means['ul']+means['uu'])/2),'mean_W':float((means['wl']+means['wu'])/2),
        'variance_U_lower_variable':float(variances['ul']),'variance_W_lower_variable':float(variances['wl']),
        'mean_events':record['total_events']/m,'mean_proposals':record['total_proposals']/m,
        'proved_expected_events_per_sample':float(event_bound),
        'proved_expected_proposals_per_sample':float((5-4*kappa)*event_bound),
        'max_active_particles':record['max_active_particles'],'max_tree_height':record['max_tree_height'],
        'max_events':record['max_events'],'total_events':record['total_events'],
        'total_proposals':record['total_proposals'],
        'sampling_seconds':record['seconds'],'certificate_seconds':perf_counter()-started,
        'max_static_score_enclosure_width':float(max_score_width),'dyadic_bits':bits,
        'exact_endpoint_sums':{k:str(v) for k,v in sums.items()},
        'exact_endpoint_square_sums':{k:str(v) for k,v in squares.items()},
        'limitations':['Statistical confidence assumes independent uniform random bits; executable uses a seeded standard PRNG.',
                       'Expected computational work; individual excursions are unbounded.',
                       ('Histogram retained for reproducibility.' if precomputed is None else 'Streaming score accumulation: no terminal-state histogram retained.'),
                       'The proved scope is the specified positive-dual one-dimensional zero-field kinetic Ising family.']}
    return out


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('input');parser.add_argument('--output',required=True)
    parser.add_argument('--bits',type=int,default=100)
    args=parser.parse_args(); result=certify(args.input,bits=args.bits)
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if not k.endswith('exact') and not k.startswith('exact_endpoint')},indent=2))
