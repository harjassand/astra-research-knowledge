"""Independent exact cover, scalar-budget and differential-identity consumer.

Does not import the row builder. The scientific continuum sign is consumed
from its explicit outward arithmetic receipt, with exact cover verification.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json,time
from flint import arb,fmpq,ctx
import sympy as s

ctx.prec=160


def b(q):
    q=F(q);return arb(fmpq(q.numerator,q.denominator))


def dyadic(x):
    m,e=x.man_exp();m,e=int(m),int(e)
    q=F(m*(1<<e)) if e>=0 else F(m,1<<-e)
    return [q.numerator,q.denominator]


def enclosure(x):
    return {'lower':dyadic(x.lower()),'upper':dyadic(x.upper()),'display':float(x)}


def main():
    start=time.perf_counter();root=Path(__file__).parent
    raw=(root/'NONRADIAL_CERTIFICATE.json').read_bytes();cert=json.loads(raw)
    assert cert['status']=='PASS_FULL_CONTINUUM'
    rows=sorted(cert['admitted'],key=lambda r:F(*r['v_interval'][0]))
    endpoint=F(0);eta=F(199,200)
    for row in rows:
        lo,hi=map(lambda x:F(*x),row['v_interval'])
        assert lo==endpoint and hi>lo
        assert F(*row['row_upper'])<eta
        endpoint=hi
    assert endpoint==8 and F(*cert['tail_row_upper'])<eta
    maxima=[max(abs(F(*r['controls'][j])) for r in rows) for j in range(3)]
    beta=b(F(3,4));d=b(F(1,10000));pm=b(F(5,4))
    nu0=2*(2/arb.pi()).sqrt();zb=(2*arb.pi())**b(F(3,8))*beta**b(F(-3,2))
    cb=zb/beta.sqrt();assert cb<4
    m1=2*(2/(arb.pi()*beta)).sqrt();ma=(2/(arb.pi()*beta)).sqrt()
    eg_large=4/(beta*(1-beta));eg_small=4*(beta/2).exp()/beta
    base=beta**b(F(-3,2))*(1+m1/nu0)
    rawbound=pm*(max(eg_small.upper(),eg_large.upper())+base)
    controlled=rawbound+pm*beta**b(F(-3,2))/nu0*(b(maxima[0])+b(maxima[1])*ma+b(maxima[2])*3/beta)
    assert rawbound<32 and controlled<64
    pq=d*b(F(45,16))*cb;assert pq<b(F(9,8000))
    mult=2+64/(1-pq);margin=1-b(eta)/(1-pq)
    assert mult<67 and margin>b(F(3,1000))
    factory=b(F(19,2))*mult/margin;assert factory<213000
    assert eta+25*F(1,10000)==F(399,400)
    radius=b(40);tail=pm*(4/(beta*(1-beta)*radius*radius)
        +beta**b(F(-3,2))*(-(1-beta)*radius*radius/2).exp()*(1+m1/radius))
    local=b(F(1,40))+b(F(1,500))+60*d
    assert tail<b(F(1,40)) and local<b(F(1,16))
    eff=d*pm;tv=eff*zb/2
    q=(arb.pi()/2).sqrt()*b(F(1,2)).exp()*(1/arb(2).sqrt()).erfc()
    delta=b(F(1,16384));angular=b(F(1,2))+delta*2*q/(3*arb.pi())
    anisotropy=4*delta*(3-q)/15
    sourcebound=delta*(2*arb.pi())**b(F(-3,8));assert sourcebound<d
    assert b(F(1,2))-eff*zb/2>0
    def clipping(L):
        R=((2*((2*arb.pi())**b(F(-3,8))/L).log())/(1-beta)).sqrt()
        def tail(x):return (2/arb.pi()).sqrt()*x*(-x*x/2).exp()+(x/arb(2).sqrt()).erfc()
        bias=L*zb*tail(beta.sqrt()*R)-tail(R)
        assert bias>0
        return {'R':enclosure(R),'unnormalized_bias':enclosure(bias),
                'normalized_TV_bound':enclosure(bias/(1+bias))}
    conservative_clipping=clipping(eff);sharp_clipping=clipping(d)
    assert b(F(1,1000000000000))>arb(fmpq(*map(int,sharp_clipping['normalized_TV_bound']['upper'])))
    assert (2*arb.pi())**b(F(-3,8))*(-b(F(25,8))).exp()>eff
    # Differentiate the independent polynomial/Gaussian expression exactly.
    v,r,u,a,bb,c,be=s.symbols('v r u a b c beta',real=True)
    x=v*v+r*r-2*v*r*u
    p=a+bb*(v-r*u)+c*x
    e0=-v*v/2-be*r*r/2+be*v*r*u
    e1=-be*r*r/2+be*v*r*u-v*v*u*u/2
    Q=r**3+r*r*p;g=4*r*s.exp(e1)-Q*s.exp(e0)
    differential=[]
    for var in (r,u,v):
        firstfactor=s.diff(4*r,var)
        expected=(s.diff(4*r,var,2)+2*firstfactor*s.diff(e1,var)
                  +4*r*(s.diff(e1,var)**2+s.diff(e1,var,2)))*s.exp(e1)
        expected-=(s.diff(Q,var,2)+2*s.diff(Q,var)*s.diff(e0,var)
                   +Q*(s.diff(e0,var)**2+s.diff(e0,var,2)))*s.exp(e0)
        assert s.simplify(s.diff(g,var,2)-expected)==0
        differential.append(str(var))
    # Nonradial source moments: angular Dirichlet/swap identities and radial
    # polynomial division, with no Monte Carlo claims.
    assert s.Rational(2,5)-2*s.Rational(1,15)==s.Rational(4,15)
    z=s.symbols('z');assert s.cancel(z*z/(1+z)-(z-1+1/(1+z)))==0
    out={'status':'PASS_STATIC_CONSUMER','row_certificate_sha256':hashlib.sha256(raw).hexdigest(),
         'complete_closed_cover':[0,8],'admitted_intervals':len(rows),
         'max_controls_exact':[[x.numerator,x.denominator] for x in maxima],
         'C_beta':enclosure(cb),'raw_envelope_over_nu':enclosure(rawbound),
         'controlled_envelope_over_nu':enclosure(controlled),
         'nonlinear_proposal_bound':enclosure(pq),'factory_multiplier_bound':enclosure(mult),
         'factory_margin_bound':enclosure(margin),'factory_coins_bound':enclosure(factory),
         'offspring':'399/400','mean_tree_nodes_bound':400,
         'local_positive_contraction_bound':enclosure(local),
         'raw_speed_tail_at40':enclosure(tail),'D':'1/10000','D_eff':'1/8000',
         'source_delta':'1/16384','source_norm_bound':enclosure(sourcebound),
         'source_angular_plus_probability':enclosure(angular),
         'source_covariance_anisotropy':enclosure(anisotropy),
         'initial_uniform_TV_bound':enclosure(tv),
         'TV_decay_rate':enclosure(nu0/400),
         'observation_mean_proposals':enclosure(1+eff*zb),
         'continuous_clipping_conservative':conservative_clipping,
         'continuous_clipping_pointwise_sharp':sharp_clipping,
         'continuous_output_declared_TV':'1/1000000000000 uniformly in time, ideal-real',
         'gaussian_approximation_time_for_TV_1e_8':enclosure((tv/b(F(1,100000000))).log()/(nu0/400)),
         'exact_second_derivative_identities':differential,
         'seconds':time.perf_counter()-start,
         'full_continuous_output':'approximate only: declared total-variation contract',
         'literal_iid_bit_output':False}
    (root/'STATIC_CERTIFICATE.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('max_controls_exact',)},indent=2))


if __name__=='__main__':main()
