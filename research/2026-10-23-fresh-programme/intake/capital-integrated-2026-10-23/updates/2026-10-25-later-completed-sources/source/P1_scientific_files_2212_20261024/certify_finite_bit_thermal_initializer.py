#!/usr/bin/env python3
"""Standalone certified finite-bit initializer for four N(0,1/2) coordinates.

Only Python standard-library INTEGER/rational operations govern the result.
No SciPy, NumPy, floating CDF, or floating quantile is used. Decimal strings
are display only. Input uniform random bits and independent sign bits are
supplied resources. The executable evaluates deterministic representative
quantiles; it does not sample a physical experiment or millions of draws.
"""
from fractions import Fraction as F
from decimal import Decimal, localcontext
from math import factorial, isqrt
from pathlib import Path
import hashlib
import json
import time

BITS=640
SCALE=1<<BITS
UNIFORM_BITS=128
UNIFORM_SIZE=1<<UNIFORM_BITS
GRID_BITS=60
GRID_DENOMINATOR=1<<GRID_BITS
GRID_UNITS=1<<(BITS-GRID_BITS)
RADIUS=8
ERF_DEGREE=512
ATAN_TERMS=256
INVERSE_DERIVATIVE_POWER=103


def ceildiv(n,d):
    assert d>0
    return -((-n)//d)


class Interval:
    """Fixed-dyadic enclosure [lo,hi]/2^640, including negative values."""
    __slots__=('lo','hi')
    def __init__(self,lo,hi=None):
        self.lo=int(lo); self.hi=int(lo if hi is None else hi)
        assert self.lo<=self.hi
    @staticmethod
    def rational(q):
        q=F(q)
        return Interval(q.numerator*SCALE//q.denominator,
                        ceildiv(q.numerator*SCALE,q.denominator))
    @staticmethod
    def point_units(n):
        return Interval(n,n)
    def __add__(self,other):
        if not isinstance(other,Interval):other=Interval.rational(other)
        return Interval(self.lo+other.lo,self.hi+other.hi)
    __radd__=__add__
    def __neg__(self):return Interval(-self.hi,-self.lo)
    def __sub__(self,other):return self+-other if isinstance(other,Interval) else self+-F(other)
    def __mul__(self,other):
        if not isinstance(other,Interval):other=Interval.rational(other)
        products=(self.lo*other.lo,self.lo*other.hi,self.hi*other.lo,self.hi*other.hi)
        return Interval(min(products)//SCALE,ceildiv(max(products),SCALE))
    __rmul__=__mul__
    def ratio(self,p,q=1):
        assert p>=0 and q>0
        return Interval(self.lo*p//q,ceildiv(self.hi*p,q))
    def reciprocal(self):
        assert self.lo>0
        return Interval(SCALE*SCALE//self.hi,ceildiv(SCALE*SCALE,self.lo))
    def sqrt(self):
        assert self.lo>=0
        low=isqrt(self.lo*SCALE)
        upper_square=self.hi*SCALE
        high=isqrt(upper_square)
        if high*high<upper_square:high+=1
        return Interval(low,high)
    def width(self):return F(self.hi-self.lo,SCALE)


def fraction_json(q):
    q=F(q)
    return {'n':str(q.numerator),'d':str(q.denominator)}


def decimal_display(q,precision=90):
    q=F(q)
    with localcontext() as ctx:
        ctx.prec=precision
        return str(Decimal(q.numerator)/Decimal(q.denominator))


def interval_json(iv):
    return {'lower':fraction_json(F(iv.lo,SCALE)),
            'upper':fraction_json(F(iv.hi,SCALE)),
            'width':fraction_json(iv.width()),
            'display_only':[decimal_display(F(iv.lo,SCALE)),decimal_display(F(iv.hi,SCALE))]}


def arctan_reciprocal(denominator,terms=ATAN_TERMS):
    """Alternating series, with a fully rational one-term remainder bound."""
    ratio=F(1,denominator*denominator)
    power=F(1,denominator)
    total=Interval.rational(0)
    for n in range(terms):
        term=Interval.rational(power/(2*n+1))
        total=total+term if n%2==0 else total-term
        power*=ratio
    next_term=Interval.rational(power/(2*terms+1))
    # The first omitted term has sign (-1)^terms.
    if terms%2==0:
        return Interval(total.lo,total.hi+next_term.hi)
    return Interval(total.lo-next_term.hi,total.hi)


def machin_pi():
    a=arctan_reciprocal(5)
    b=arctan_reciprocal(239)
    pi=a.ratio(16)-b.ratio(4)
    assert 3*SCALE<pi.lo<=pi.hi<4*SCALE
    assert pi.hi-pi.lo<1<<17
    # Rational tangent identity for 4 atan(1/5)-atan(1/239)=pi/4.
    tan_four=F(120,119)
    tangent=(tan_four-F(1,239))/(1+tan_four/F(239))
    assert tangent==1
    return pi


class ThermalInitializer:
    def __init__(self):
        self.pi=machin_pi()
        self.prefactor=self.pi.sqrt().reciprocal().ratio(2)
        assert SCALE<self.prefactor.lo<self.prefactor.hi<2*SCALE
        self.cache={0:Interval(0)}
        self.cdf_requests=0
        self.cdf_evaluations=0
        self.taylor_term_updates=0
        self.largest_term_bits_above_binary_point=0
        self.largest_cdf_width_units=0
        # Uniform Lagrange remainder at x<=8, n=512.
        assert RADIUS**(2*ERF_DEGREE+3)*(1<<700)<factorial(ERF_DEGREE+1)*(2*ERF_DEGREE+3)
        assert 3**64<1<<103
        assert 3**65<1<<104

    def cdf(self,x_units):
        """Certified erf(x) for the exact dyadic x=x_units/2^640 in [0,8]."""
        assert 0<=x_units<=RADIUS*SCALE
        self.cdf_requests+=1
        if x_units in self.cache:return self.cache[x_units]
        x=Interval.point_units(x_units)
        squared=x*x
        term=x
        total=term
        for n in range(1,ERF_DEGREE+1):
            term=(term*squared).ratio(2*n-1,n*(2*n+1))
            total=total+term if n%2==0 else total-term
            self.taylor_term_updates+=1
            self.largest_term_bits_above_binary_point=max(
                self.largest_term_bits_above_binary_point,
                max(abs(term.lo),abs(term.hi)).bit_length()-BITS)
        next_term=(term*squared).ratio(2*ERF_DEGREE+1,(ERF_DEGREE+1)*(2*ERF_DEGREE+3))
        self.taylor_term_updates+=1
        # Integral Taylor remainder sign is (-1)^(ERF_DEGREE+1).
        if ERF_DEGREE%2==0:
            integral=Interval(total.lo-next_term.hi,total.hi)
        else:
            integral=Interval(total.lo,total.hi+next_term.hi)
        result=self.prefactor*integral
        result=Interval(max(0,result.lo),min(SCALE,result.hi))
        # Proven conservative all-call width; violation is a hard failure,
        # not an unreported approximation or a floating CDF fallback.
        assert result.hi-result.lo<=1<<(BITS-400)
        self.largest_cdf_width_units=max(self.largest_cdf_width_units,result.hi-result.lo)
        self.cdf_evaluations+=1
        self.cache[x_units]=result
        return result

    def lower_quantile(self,k):
        """Certified contractive capped quantile for exactly k/2^128."""
        assert isinstance(k,int) and 0<=k<UNIFORM_SIZE
        result=self._lower_quantile_units(k<<(BITS-UNIFORM_BITS))
        result['uniform_128_bit_integer']=str(k)
        result['uniform_128_bit_input']=True
        return result

    def _lower_quantile_units(self,u):
        """General dyadic target helper, also used for the ambiguity test."""
        assert 0<=u<SCALE
        before=(self.cdf_requests,self.cdf_evaluations,self.taylor_term_updates)
        iterations=ambiguities=0
        last_cdf=None
        if u==0:
            low=high=0
            status='exact_zero'
        else:
            cap=self.cdf(RADIUS*SCALE)
            last_cdf=cap
            if u>=cap.hi:
                low=high=RADIUS*SCALE
                status='certified_cap'
            elif u>=cap.lo:
                low=max(0,RADIUS*SCALE-(cap.hi-u)*(1<<INVERSE_DERIVATIVE_POWER))
                high=RADIUS*SCALE
                ambiguities+=1
                status='cap_boundary_inverse_enclosure'
            else:
                low=0;high=RADIUS*SCALE
                status='bisection'
                while high-low>GRID_UNITS:
                    iterations+=1
                    assert iterations<=64
                    mid=(low+high)//2
                    cdf=self.cdf(mid)
                    last_cdf=cdf
                    if u>=cdf.hi:
                        low=mid
                    elif u<=cdf.lo:
                        high=mid
                    else:
                        # erf'(x)>=2^-103 on [0,8].
                        low=max(low,mid-(cdf.hi-u)*(1<<INVERSE_DERIVATIVE_POWER))
                        high=min(high,mid+(u-cdf.lo)*(1<<INVERSE_DERIVATIVE_POWER))
                        ambiguities+=1
                        status='interior_inverse_enclosure'
                        assert high-low<=GRID_UNITS
        assert 0<=low<=high<=RADIUS*SCALE
        assert high-low<=GRID_UNITS
        grid_index=low//GRID_UNITS
        value=F(grid_index,GRID_DENOMINATOR)
        error_upper=F(high,SCALE)-value
        assert 0<=error_upper<=F(2,GRID_DENOMINATOR)
        result={
            'uniform_target':fraction_json(F(u,SCALE)),
            'status':status,
            'lower_magnitude_grid_index':str(grid_index),
            'magnitude':fraction_json(value),
            'magnitude_decimal_display_only':decimal_display(value),
            'capped_true_quantile_bracket':interval_json(Interval(low,high)),
            'coordinate_numerical_error_upper':fraction_json(error_upper),
            'bisection_iterations':iterations,
            'ambiguous_CDF_inverse_updates':ambiguities,
            'CDF_requests':self.cdf_requests-before[0],
            'CDF_evaluations_not_cached':self.cdf_evaluations-before[1],
            'Taylor_term_updates':self.taylor_term_updates-before[2],
            'last_CDF_interval':interval_json(last_cdf) if last_cdf else None,
        }
        return result

    def initialize_four(self,uniform_integers,sign_bits):
        """Four finite coordinates, retaining all four individual certificates.

        No randomness is generated: independent uniform 128-bit integers
        and four independent fair sign bits are explicit supplied inputs.
        """
        assert len(uniform_integers)==len(sign_bits)==4
        assert all(b in (0,1) for b in sign_bits)
        cert=[self.lower_quantile(int(k)) for k in uniform_integers]
        values=[F(int(q['magnitude']['n']),int(q['magnitude']['d']))
                *(-1 if bit else 1) for q,bit in zip(cert,sign_bits)]
        return values,cert


def main():
    started=time.monotonic()
    init=ThermalInitializer()
    cap=init.cdf(RADIUS*SCALE)
    cap_grid_low=cap.lo>>(BITS-UNIFORM_BITS)
    cap_grid_high=cap.hi>>(BITS-UNIFORM_BITS)
    assert cap_grid_low==cap_grid_high
    targets=[('zero',0),('smallest_positive_uniform',1),
             ('uniform_2_power_minus_64',1<<64),
             ('one_quarter',UNIFORM_SIZE//4),('one_half',UNIFORM_SIZE//2),
             ('three_quarters',3*UNIFORM_SIZE//4),
             ('one_minus_2_power_minus_64',UNIFORM_SIZE-(1<<64)),
             ('one_minus_2_power_minus_96',UNIFORM_SIZE-(1<<32)),
             ('largest_uniform_below_cap_CDF',cap_grid_low),
             ('smallest_uniform_above_cap_CDF',cap_grid_low+1),
             ('maximum_128_bit_uniform',UNIFORM_SIZE-1)]
    quantiles=[]
    for label,k in targets:
        result=init.lower_quantile(k)
        result['label']=label
        quantiles.append(result)

    # Deliberately exercise the interval-overlap branch at the first
    # bisection point x=4. This target is an auxiliary 640-bit dyadic,
    # NOT a claimed 128-bit draw or an acquired sample.
    midpoint_cdf=init.cdf(4*SCALE)
    auxiliary_target=(midpoint_cdf.lo+midpoint_cdf.hi)//2
    ambiguity_test=init._lower_quantile_units(auxiliary_target)
    assert ambiguity_test['ambiguous_CDF_inverse_updates']==1
    assert ambiguity_test['status']=='interior_inverse_enclosure'
    ambiguity_test['uniform_128_bit_input']=False
    ambiguity_test['scope']='Deterministic auxiliary target chosen inside the certified erf(4) interval to test inverse-enclosure logic.'

    delta=F(1,GRID_DENOMINATOR)
    e0=4*delta
    tail=4*F(3,8)**64
    uniform_floor_transport=F(4*RADIUS,UNIFORM_SIZE)
    transport=uniform_floor_transport+e0
    examples=[]
    for theta,inverse_sqrt in ((F(1,16),4),(F(1,1024),32),(F(1,1<<40),1<<20)):
        assert theta*inverse_sqrt*inverse_sqrt==1
        allowance=tail+inverse_sqrt*transport
        examples.append({'theta':fraction_json(theta),
                         'halftrace_initialization_upper':fraction_json(allowance),
                         'upper_decimal_display_only':decimal_display(allowance)})

    out={
        'status':'CERTIFIED_FINITE_BIT_CONTRACTIVE_THERMAL_INITIALIZER',
        'target':'Four independent real N(0,1/2) coordinates, i.e. m=2 complex thermal variance nu=1.',
        'fixed_dyadic_precision_bits':BITS,
        'uniform_input_bits_per_magnitude':UNIFORM_BITS,
        'independent_fair_sign_bits_required':4,
        'cap_radius_per_real_coordinate':RADIUS,
        'coordinate_grid_spacing':fraction_json(delta),
        'erf_integrated_Taylor_degree':ERF_DEGREE,
        'Machin_arctan_terms_per_argument':ATAN_TERMS,
        'pi_interval':interval_json(init.pi),
        'erf_prefactor_interval':interval_json(init.prefactor),
        'erf_at_cap_interval':interval_json(cap),
        'largest_128_bit_integer_below_true_cap_CDF':str(cap_grid_low),
        'representative_quantiles':quantiles,
        'auxiliary_ambiguous_CDF_branch_test':ambiguity_test,
        'allowance_coefficients':{
            'union_tail_probability_upper':fraction_json(tail),
            'four_coordinate_expected_floor_transport_upper':fraction_json(uniform_floor_transport),
            'four_coordinate_Euclidean_numerical_error_upper_e0':fraction_json(e0),
            'transport_coefficient_divided_by_sqrt_theta':fraction_json(transport),
            'formula':'4*(3/8)^64 + (32*2^-128 + 4*2^-60)/sqrt(theta)',
        },
        'halftrace_allowance_examples':examples,
        'moment_statement':'Under the monotone ideal-uniform coupling, every output coordinate magnitude is <= its ideal Gaussian magnitude; therefore every increasing function of squared radius, including all radial moments and exponential radial moments, is dominated.',
        'execution_counts':{
            'CDF_requests':init.cdf_requests,'CDF_evaluations_not_cached':init.cdf_evaluations,
            'Taylor_term_updates':init.taylor_term_updates,
            'largest_term_integer_bits_observed':init.largest_term_bits_above_binary_point,
            'largest_CDF_interval_width':fraction_json(F(init.largest_cdf_width_units,SCALE)),
            'maximum_normal_bisection_iterations_observed':max(q['bisection_iterations'] for q in quantiles),
            'deterministic_representative_quantiles':len(quantiles),
            'random_draws_generated':0,
            'runtime_seconds_observed':time.monotonic()-started,
        },
        'resources':[
            'The independent unbiased random-bit source remains supplied.',
            'Model parameters and the coherent-mixture preparation interface remain supplied.',
            'All certificate operations are exact integers or rational operations; decimal strings and runtime are display metadata.',
            'No floating CDF/quantile, SciPy, or empirical Gaussian tail estimate is used.',
            'All previous source states and certificates are read-independent and unchanged.',
        ],
        'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    dest=Path(__file__).with_name('FINITE_BIT_THERMAL_INITIALIZER_CERTIFICATE.json')
    if dest.exists():raise FileExistsError('Preserve previous output; replay code in a new directory.')
    dest.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'certificate':str(dest),
        'quantiles':[{'label':q['label'],'magnitude':q['magnitude_decimal_display_only'],
                      'status':q['status'],'iterations':q['bisection_iterations'],
                      'uncached_CDF_evaluations':q['CDF_evaluations_not_cached'],
                      'inverse_bracket_width':q['capped_true_quantile_bracket']['width']}
                     for q in quantiles],
        'ambiguity_branch':{'status':ambiguity_test['status'],
                            'inverse_bracket_width':ambiguity_test['capped_true_quantile_bracket']['width']},
        'execution_counts':out['execution_counts'],
        'allowance_examples':examples},indent=2))


if __name__=='__main__':main()
