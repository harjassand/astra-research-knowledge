"""New Pro3 construction: certified entrance law for an imprecisely timed event.

The trigger is a two-state CTMC with reaction from state one. Unobserved
inactive sites evolve independently until that event. The event is observed
only in a time bin. Its unknown time creates correlations between the inactive
sites. This program constructs a positive product mixture and certifies its
entire conditional law, without expanding the inactive configuration space.

Dependency: the preserved pro3_gate_experiment.py supplies the directed Decimal
interval class. This is an explicit new dependency, not a historical helper.
All probability parameters and reported mixture coefficients are exact
rationals; interval exp and positive uniformization enclose event-bin weights.
"""
from fractions import Fraction as F
from decimal import Decimal as D, ROUND_FLOOR, ROUND_CEILING
from math import ceil
import json
import time
from pro3_gate_experiment import I, DOWN, UP, NEAR


def midpoint_fraction(interval):
    return (F(interval.lo)+F(interval.hi))/2


def decimal_string(x, precision=25, rounding=None):
    from decimal import localcontext
    with localcontext() as ctx:
        ctx.prec=precision
        if rounding is not None:
            ctx.rounding=rounding
        return str(D(x.numerator)/D(x.denominator))


class TriggerCDF:
    """Certified P(first trigger by t) by positive uniformization.

    Source rules: 0->1 at alpha, 1->0 at beta, 1->absorbed at kappa.
    Only this three-state local model is constructed.
    """
    def __init__(self, alpha, beta, kappa, terms=80):
        self.rate=max(alpha,beta+kappa)
        v=[F(1),F(0),F(0)]
        P=[[1-alpha/self.rate,alpha/self.rate,F(0)],
           [beta/self.rate,1-(beta+kappa)/self.rate,kappa/self.rate],
           [F(0),F(0),F(1)]]
        self.coefficients=[]
        for k in range(terms+1):
            self.coefficients.append(I(v[2]))
            v=[sum((v[i]*P[i][j] for i in range(3)),F(0)) for j in range(3)]
        self.cache={}

    def __call__(self,t):
        if t in self.cache: return self.cache[t]
        z=I(self.rate*t); term=I(1)
        poisson=I(1); event=self.coefficients[0]
        for k,a in enumerate(self.coefficients[1:],1):
            term=term*z/k
            poisson=poisson+term
            event=event+term*a
        e=(-z).exp()
        part=e*event; covered=e*poisson
        tail=max(D(0),UP.subtract(D(1),covered.lo))
        result=I(max(D(0),part.lo),min(D(1),UP.add(part.hi,tail)))
        self.cache[t]=result
        return result

    def bin_mass(self,a,b):
        x,y=self(a),self(b)
        return I(max(D(0),DOWN.subtract(y.lo,x.hi)),
                 min(D(1),UP.subtract(y.hi,x.lo)))


def make_entrance_action(n_inactive=8, eta=F(1,200), left=F(0), right=F(3)):
    assert n_inactive >= 2 and eta > 0 and 0 <= left < right
    started=time.perf_counter()
    lambdas=[1+F(i,10) for i in range(n_inactive)]
    stationary=[F(4,5)]*n_inactive
    initial=[F(0)]*n_inactive
    cdf=TriggerCDF(F(2,5),F(3,5),F(7,10))
    cache={}
    def local_probabilities(t):
        if t not in cache:
            cache[t]=[I(pi)+(I(p0)-I(pi))*(-I(lam*t)).exp()
                      for pi,p0,lam in zip(stationary,initial,lambdas)]
        return cache[t]
    def variation(a,b):
        return sum((I(abs(p0-pi))*
                    ((-I(lam*a)).exp()-(-I(lam*b)).exp())
                    for pi,p0,lam in zip(stationary,initial,lambdas)),I(0))

    # Dyadic refinement is verified cell by cell. The theorem's ideal
    # variation-quantile partition need not be dyadic.
    cells=[]; pending=[(left,right)]
    while pending:
        a,b=pending.pop()
        change=variation(a,b)
        if change.hi<=I(eta).lo:
            cells.append((a,b,change.hi))
        else:
            assert b-a>F(1,2**60)
            m=(a+b)/2
            pending.extend([(m,b),(a,m)])

    total_mass=F(0); total_mass_error=F(0)
    max_propagation_error=F(0)
    terms=[]
    for a,b,change in cells:
        t=(a+b)/2
        mass_interval=cdf.bin_mass(a,b)
        mass=midpoint_fraction(mass_interval)
        mass_error=max(mass-F(mass_interval.lo),F(mass_interval.hi)-mass)
        total_mass+=mass; total_mass_error+=mass_error
        probabilities=[]; local_error=F(0)
        for interval in local_probabilities(t):
            probability=midpoint_fraction(interval)
            assert 0<=probability<=1
            probabilities.append(probability)
            local_error+=max(probability-F(interval.lo),F(interval.hi)-probability)
        max_propagation_error=max(max_propagation_error,local_error)
        terms.append({'cell':(a,b),'representative':t,'mass':mass,
                      'probabilities':probabilities,'variation_upper':F(change)})
    event_probability=cdf.bin_mass(left,right)
    p_lower=F(event_probability.lo)
    assert p_lower>0 and total_mass>0
    certificate=eta+max_propagation_error+total_mass_error/p_lower

    # All finite-mixture expectations below are exact rational calculations.
    mean0=mean1=pair=F(0)
    for term in terms:
        weight=term['mass']/total_mass
        term['weight']=weight
        p0,p1=term['probabilities'][:2]
        mean0+=weight*p0; mean1+=weight*p1; pair+=weight*p0*p1
    covariance=pair-mean0*mean1
    # A [0,1] statistic changes by <=TV. The product of two marginals
    # changes by <=2TV, so this bounds the true covariance as well.
    covariance_lower=covariance-3*certificate
    covariance_upper=covariance+3*certificate
    assert covariance_lower>0

    summary={
      'status':'new work; certified full conditional entrance law',
      'observation':'first reaction time in [0,3], trigger initially zero',
      'trigger_rates':{'alpha':'2/5','beta':'3/5','kappa':'7/10'},
      'inactive_modules':n_inactive,
      'full_hidden_configurations':str(2**(n_inactive+1)),
      'expanded_local_states':3,
      'eta':str(eta),'mixture_terms':len(terms),
      'event_probability_interval':[str(event_probability.lo),str(event_probability.hi)],
      'event_bin_weight_L1_error_upper':decimal_string(total_mass_error,rounding=ROUND_CEILING),
      'local_propagation_TV_error_upper':decimal_string(max_propagation_error,rounding=ROUND_CEILING),
      'conditional_entrance_TV_upper':decimal_string(certificate,rounding=ROUND_CEILING),
      'conditional_entrance_TV_exact_rational_bound':str(certificate),
      'inactive_0_mean':decimal_string(mean0),
      'inactive_1_mean':decimal_string(mean1),
      'both_active_probability':decimal_string(pair),
      'product_of_marginals':decimal_string(mean0*mean1),
      'covariance_of_approximating_mixture':decimal_string(covariance),
      'true_covariance_enclosure':[decimal_string(covariance_lower,rounding=ROUND_FLOOR),decimal_string(covariance_upper,rounding=ROUND_CEILING)],
      'elapsed_seconds':time.perf_counter()-started,
      'scope':'No global state expansion. The positive mixture is a reusable approximation to the entire post-event inactive-site law. The numerical certificate includes time quantization, event-bin weight evaluation and local propagator rounding.'
    }
    serialized=[{'weight':str(x['weight']),
                 'time_cell':[str(y) for y in x['cell']],
                 'representative_time':str(x['representative']),
                 'bernoulli_probabilities':[str(y) for y in x['probabilities']],
                 'variation_upper':str(x['variation_upper'])}
                for x in terms]
    return summary,serialized


if __name__=='__main__':
    summary,mixture=make_entrance_action()
    print(json.dumps(summary,indent=2))
    with open('entrance_time_bins_results.json','w') as handle:
        json.dump({'summary':summary,'positive_product_mixture':mixture},handle,indent=2)
