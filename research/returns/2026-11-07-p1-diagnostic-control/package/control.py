"""Bounded controller for the frozen native/Bernoulli-factory diagnostic.

No source parameters lambda, e, p_c or p_h are inputs to this controller.
Callbacks must implement the warranted native one-step coin interface, with
the reset/read/recovery times and errors accounted for by the caller.
This module performs no physical experiment.
"""
from fractions import Fraction as F


def ceil_fraction(x):
    x=F(x)
    return -((-x.numerator)//x.denominator)


def ceil_log2(x):
    x=F(x)
    assert x>0
    k=max(0,x.numerator.bit_length()-x.denominator.bit_length())
    while F(1<<k)<x:
        k+=1
    return k


def plan_component(spec, epsilon, n):
    """All ceilings and probability thresholds use exact finite arithmetic."""
    alpha,chi,q=(F(spec[k]) for k in ('alpha','chi','q'))
    pc_upper,ph_lower=(F(spec[k]) for k in ('p_c_upper','p_h_lower'))
    assert 0<=alpha<alpha+chi<=1
    assert 0<=pc_upper<q<ph_lower<=1
    target=alpha+chi*q
    dc=chi*(q-pc_upper)
    dh=chi*(ph_lower-q)
    d0=dc+dh
    assert 0<target<1 and dc>0 and dh>0
    part=F(epsilon)/(8*n)
    beta=chi*part
    exponent=ceil_log2(1/beta)
    nc=max(1,ceil_fraction(F(exponent)/(2*dc*dc)))
    nh=max(1,ceil_fraction(F(exponent)/(2*dh*dh)))
    tail_exponent=ceil_log2(1/part)
    trials=max(1,ceil_fraction(F(tail_exponent)/d0))
    coin_bits=max(1,ceil_log2(F(2*trials)/part))
    assert 2*nc*dc*dc>=exponent
    assert 2*nh*dh*dh>=exponent
    assert trials*d0>=tail_exponent
    assert F(2*trials,1<<coin_bits)<=part
    return {'target_observed':target,'dc':dc,'dh':dh,'d0':d0,
        'chi':chi,'beta':beta,'nc':nc,'nh':nh,'trials':trials,
        'coin_bits':coin_bits,'clip_exponent':exponent,
        'tail_exponent':tail_exponent,'fair_bit_cap':2*trials*coin_bits,
        'signal_coin_cap':trials*max(nc,nh),'per_category_factor_error':part}


def make_plan(specs,epsilon,entropy_source,a_min):
    """Compile one unconditional output, allocating 3 epsilon/4 to six terms.

    The remaining epsilon/4 is reserved for warranted instrument, controller,
    synthesis, transfer and holding residuals. Fixed residuals are never assumed
    to vanish by repeated sampling.
    """
    epsilon=F(epsilon)
    assert 0<epsilon<1 and specs
    parts=[plan_component(s,epsilon,len(specs)) for s in specs]
    alpha,chi,lam_lo,ac=(F(entropy_source[k]) for k in
                         ('alpha','chi','lambda_lower','a_c'))
    assert 0<=alpha<alpha+chi<=1 and lam_lo>0 and ac>0
    p_lo=lam_lo/(2*lam_lo+ac)
    r_lo=alpha+chi*p_lo
    r_hi=alpha+chi/2
    kappa=r_lo*(1-r_hi)
    assert 0<r_lo<=r_hi<1 and kappa>0
    bits=sum(p['fair_bit_cap'] for p in parts)
    entropy_exp=ceil_log2(8*F(bits)/epsilon)
    pair_cap=max(1,ceil_fraction(F(entropy_exp)/(2*kappa)))
    entropy_coin_cap=2*bits*pair_cap
    signal_coin_cap=sum(p['signal_coin_cap'] for p in parts)
    all_coins=entropy_coin_cap+signal_coin_cap
    probe_exp=ceil_log2(16*F(all_coins)/epsilon)
    output_exp=ceil_log2(16*F(len(specs))/epsilon)
    assert 2*kappa*pair_cap>=entropy_exp
    certified_terms={
        'clipping':sum(F(1,1<<p['clip_exponent'])/p['chi'] for p in parts),
        'race_tail':sum(F(1,1<<p['tail_exponent']) for p in parts),
        'known_coin_rounding':sum(F(2*p['trials'],1<<p['coin_bits']) for p in parts),
        'entropy_extraction':F(bits,1<<entropy_exp),
        'probe_reset':F(2*all_coins,1<<probe_exp),
        'output_reset':F(2*len(specs),1<<output_exp)}
    assert all(v<=epsilon/8 for v in certified_terms.values())
    assert sum(certified_terms.values())<=3*epsilon/4
    return {'epsilon':epsilon,'components':parts,
        'entropy_r_lower':r_lo,'entropy_r_upper':r_hi,'entropy_kappa':kappa,
        'fair_bit_cap':bits,'pairs_per_fair_bit_cap':pair_cap,
        'entropy_coin_cap':entropy_coin_cap,'signal_coin_cap':signal_coin_cap,
        'total_native_coin_cap':all_coins,'probe_reset_exponent':probe_exp,
        'output_reset_exponent':output_exp,
        'common_probe_reset_duration':F(2*probe_exp)/F(a_min),
        'parallel_output_reset_duration':F(2*output_exp)/F(a_min),
        'per_probe_reset_duration_rule':'2*probe_reset_exponent / the actual selected positive amplitude',
        'certified_error_terms':certified_terms,
        'reserved_residual_budget':epsilon/4,
        'digital_and_randomness_scope':'Exact integer/rational control; auxiliary bits are extracted from separate fresh native samples.'}


class CappedExtractor:
    """Use fresh independent raw outcomes; no outcomes are reused elsewhere."""
    def __init__(self,raw_coin,pair_cap):
        self.raw_coin=raw_coin
        self.pair_cap=pair_cap
        self.raw_calls=0
        self.bit_calls=0
        self.cap_failures=0

    def bit(self):
        self.bit_calls+=1
        for _ in range(self.pair_cap):
            a,b=self.raw_coin(),self.raw_coin()
            self.raw_calls+=2
            assert a in (0,1) and b in (0,1)
            if a!=b:
                return int((a,b)==(0,1))
        self.cap_failures+=1
        return 0


def dyadic_coin(probability,bits,fair_bit):
    """The rounding discrepancy is explicitly charged in the plan."""
    probability=F(probability)
    assert 0<=probability<=1
    threshold=(probability.numerator*(1<<bits))//probability.denominator
    word=0
    for _ in range(bits):
        bit=fair_bit()
        assert bit in (0,1)
        word=(word<<1)|bit
    return int(word<threshold)


def bounded_label(part,cold_coin,hot_coin,fair_bit):
    """Return 0=cold or 1=hot in bounded calls, with no postselection.

    A HOT proposal samples the COLD source. A COLD proposal samples the HOT
    source. The crossings are required by the gap-race identity.
    """
    target=part['target_observed']
    calls=0
    for trial in range(part['trials']):
        proposal=dyadic_coin(target,part['coin_bits'],fair_bit)
        count_n=part['nc'] if proposal else part['nh']
        source=cold_coin if proposal else hot_coin
        ones=sum(source() for _ in range(count_n))
        calls+=count_n
        mean=F(ones,count_n)
        accept=max(F(0),(target-mean)/target) if proposal else max(F(0),(mean-target)/(1-target))
        assert 0<=accept<=1
        if dyadic_coin(accept,part['coin_bits'],fair_bit):
            return proposal,{'signal_calls':calls,'trials':trial+1,'fallback':False}
    return 0,{'signal_calls':calls,'trials':part['trials'],'fallback':True}


def exact_label_from_supplied_factory(target,dc,dh,cold_coin,hot_coin,
                                      known_coin,linear_factory):
    """Exact ideal sampler using the supplied Huber primitive.

    linear_factory(C,eta,source) must have precisely the frozen contract.
    known_coin(rational_probability) must use an actual independent randomness
    service. This wrapper makes no unsupported total bit-work bound.
    """
    target,dc,dh=F(target),F(dc),F(dh)
    assert 0<target<1 and dc>0 and dh>0
    while True:
        if known_coin(target):
            if not linear_factory(1/target,dc/target,cold_coin):
                return 1
        else:
            if not linear_factory(1/(1-target),dh/(1-target),lambda:1-hot_coin()):
                return 0
