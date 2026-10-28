#!/usr/bin/env python3
"""Exact low kernel moments for every single-primary quadratic source.

C_k = sum_X (-1)^Q(X) [dim ker X choose k]_q, 0 <= k <= J.
The exponent of the cost depends on J.  All C_0,...,C_t determine the
full count, but this is NOT a uniform polynomial algorithm when J grows.
The primary decomposition may be acquired from a literal input operator.
"""
from pathlib import Path
from fractions import Fraction
from functools import lru_cache
import sys,time

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/p) for p in ('work_norm_glue_agent','work_norm_frontier_agent',
    'work_norm_slice_agent','work_matrix_root')]
from nonresonant_primary_gaussian import NonresonantPrimaryGaussian,shifted_polynomial,value
from resonant_primary_gaussian import ResonantPrimaryGaussian
from nonresonant_primary_modular import bounded_partitions,b_factor
from resonant_primary_modular import skew_quotient_sum
from arbitrary_operator_hall import hl_monomial_coefficient,n_stat,transpose_partition
from feedback_nilpotent_gaussians import shifted_trace_polynomial
from matrix_kloosterman import Field,charpoly,factor_polynomial,primary_columns


@lru_cache(None)
def gaussian_binomial(n,k,q):
    if k<0 or k>n:return 0
    k=min(k,n-k);row=[1]+[0]*k
    for i in range(1,n+1):
        for j in range(min(i,k),0,-1):row[j]=row[j-1]+q**j*row[j]
    return row[k]


def submodule_number(shape,subtype,Q):
    source=transpose_partition(shape);target=transpose_partition(subtype)+(0,)
    if len(target)-1>len(source):return 0
    result=1
    for j in range(len(target)-1):
        a,b=target[j],target[j+1]
        if a>source[j]:return 0
        result*=Q**(b*(source[j]-a))*gaussian_binomial(source[j]-b,a-b,Q)
    return result


class NewtonProfile:
    """Keep the J+1 annihilator weights independent, over exact rationals.

Coordinates are (number of odd parts, number of parts). The latter is
the Newton coefficient index, not another enumerated partition family.
"""
    def __init__(self,q,J):
        self.q=q;self.J=J;self.width=J+1;self.length=(J+1)**2
        zero=[Fraction(0)]*self.length;zero[0]=Fraction(1)
        self.moments={0:{():tuple(zero)}}
        self.states=1;self.max_states=1;self.coefficient_calls=0;self.rational_bits=1

    def acquire_degree(self,degree):
        if degree in self.moments:return
        shapes=sorted(bounded_partitions(degree,self.J));values={}
        for shape in shapes:
            target=[Fraction(0)]*self.length
            target[sum(x%2 for x in shape)*self.width+len(shape)]=1/b_factor(shape,Fraction(self.q))
            for lower in shapes:
                if lower>=shape:break
                c=hl_monomial_coefficient(shape,lower,Fraction(1,self.q))
                self.coefficient_calls+=1
                if c:target=[x-c*y for x,y in zip(target,values[lower])]
            for x in target:
                self.rational_bits=max(self.rational_bits,x.numerator.bit_length(),x.denominator.bit_length())
            values[shape]=tuple(target)
        self.moments[degree]=values;self.states+=len(values);self.max_states=max(self.max_states,len(values))

    @lru_cache(None)
    def evaluate(self,shape,d):
        m=sum(shape);c=d*m;self.acquire_degree(c);Q=self.q**d
        factor=Fraction(Q)**(m+n_stat(shape))*b_factor(shape,Fraction(1,Q))
        answer=[Fraction(0)]*self.length
        for mu in bounded_partitions(m,self.J):
            coefficient=hl_monomial_coefficient(shape,mu,Q);self.coefficient_calls+=1
            if coefficient:
                row=self.moments[c][tuple(d*x for x in mu)]
                answer=[x+factor*coefficient*y for x,y in zip(answer,row)]
        return tuple(answer)


def _nonresonant(shape,E,phi,J,profile):
    F=E.F;q=F.q;d=E.d;m=sum(shape);Q=q**d
    phase=F.trace(F.mul(E.beta,F.mul(E.eta,E.eta)))
    sources=[shifted_trace_polynomial(phi,F,E.eta if h%2 else 0,E.beta) for h in range(4)]
    residual={}
    for source in sources:
        key=frozenset(source)
        if key in residual:continue
        state=E.eight_state(source);initial=state['initial'];multiplier=state['multiplier']
        entries=[]
        for k in range(m+1):entries.append(initial[k] if k<8 else multiplier*entries[k-8])
        residual[key]=entries
    answer=[Fraction(0)]*(J+1);types=0
    for size in range(sum(shape[:J])+1):
        for alpha in bounded_partitions(size,J):
            if any(i>=len(shape) or x>shape[i] for i,x in enumerate(alpha)):continue
            multiplicity=submodule_number(shape,alpha,Q)
            if not multiplicity:continue
            row=profile.evaluate(alpha,d);types+=1
            for odd in range(J+1):
                if (d*size-odd)%2:
                    if any(row[odd*(J+1)+k] for k in range(J+1)):raise AssertionError('boundary parity')
                    continue
                h=(d*size-odd)//2%4
                scalar=multiplicity*residual[frozenset(sources[h])][m-size]
                if phase*(h*(h-1)//2)%2:scalar=-scalar
                for k in range(J+1):answer[k]+=scalar*row[odd*(J+1)+k]
    return answer,dict(controlled_types=types,distinct_quotient_sources=len(residual),resonant=False)


def nonresonant_first_kernel_moment(shape,field_h,irreducible,beta,phi=(),eta=0):
    """Independent closed cyclic-height formula for C_1; no Hall table."""
    shape=tuple(shape);E=NonresonantPrimaryGaussian(field_h,irreducible,beta,eta)
    if not shape or any(type(x) is not int or x<=0 for x in shape) or tuple(sorted(shape,reverse=True))!=shape:
        raise ValueError('positive nonincreasing primary block lengths required')
    F=E.F;q=F.q;d=E.d;m=sum(shape);t=d*m;Q=q**d;E.gaussian(0,phi)
    phase=F.trace(F.mul(beta,F.mul(eta,eta)))
    sources=[shifted_trace_polynomial(set(phi),F,eta if h%2 else 0,beta) for h in range(4)]
    residual={}
    for source in sources:
        key=frozenset(source)
        if key in residual:continue
        state=E.eight_state(source);entries=[]
        for k in range(m+1):entries.append(state['initial'][k] if k<8 else state['multiplier']*entries[k-8])
        residual[key]=entries
    total=0;K=0
    for r,column in enumerate(transpose_partition(shape),1):
        old=K;K+=column
        multiplicity,remainder=divmod(Q**K-Q**old,q-1)
        if remainder:raise AssertionError('cyclic vector count not divisible by q-1')
        h=(d*r)//2%4;sign=-1 if phase*(h*(h-1)//2)%2 else 1
        total+=multiplicity*residual[frozenset(sources[h])][m-r]*sign
    return q**(t*(t-1)//2)*total


def _resonant(shape,E,phi,J,profile,trace_program):
    F=E.F;d=E.d;m=sum(shape);Q=F.q**d
    evaluate=(lambda x:value(phi,x)) if trace_program is None else trace_program
    observations={x:evaluate(x) for x in sorted({0,E.eta})}
    if any(x not in (0,1) for x in observations.values()):raise ValueError('trace program must return a Boolean bit')
    polynomial,transfer=skew_quotient_sum(shape,J,Q)
    scale=Q**(m+n_stat(shape));answer=[Fraction(0)]*(J+1)
    phase=F.trace(F.mul(E.beta,F.mul(E.eta,E.eta)))
    for mu,c in polynomial.items():
        size=sum(mu);degree=d*size;profile.acquire_degree(degree)
        row=profile.moments[degree][tuple(d*x for x in mu)]
        remaining=m-size;support=E.trace_support(remaining);base=E.periodic_sign(remaining)
        for odd in range(J+1):
            if (degree-odd)%2:
                if any(row[odd*(J+1)+k] for k in range(J+1)):raise AssertionError('boundary parity')
                continue
            h=(degree-odd)//2%4;delta=E.eta if h%2 else 0;point=support^delta
            if point not in observations:raise AssertionError('trace escaped the two-point support')
            sign=base*(1-2*observations[point])
            if F.trace(F.mul(F.mul(E.beta,delta),support)):sign=-sign
            if phase*(h*(h-1)//2)%2:sign=-sign
            for k in range(J+1):answer[k]+=scale*c*sign*row[odd*(J+1)+k]
    return answer,dict(**transfer,trace_program_values=observations,resonant=True)


def primary_kernel_moments(shape,field_h,irreducible,beta,phi=(),eta=0,maximum=2,trace_program=None):
    begun=time.perf_counter();shape=tuple(shape);phi=set(phi);F=Field(field_h)
    if not shape or any(type(x) is not int or x<=0 for x in shape) or tuple(sorted(shape,reverse=True))!=shape:
        raise ValueError('positive nonincreasing primary block lengths required')
    if any(type(x) is not int or x<0 or x.bit_length()>F.a for x in phi):raise ValueError('trace ANF outside the field coordinates')
    f=tuple(irreducible);d=len(f)-1;t=d*sum(shape);J=maximum
    if type(J) is not int or not 0<=J<=t:raise ValueError('0<=maximum<=matrix size required')
    resonant=shifted_polynomial(f,beta,F)==list(f)
    E=(ResonantPrimaryGaussian if resonant else NonresonantPrimaryGaussian)(field_h,f,beta,eta)
    if not resonant and trace_program is not None:raise ValueError('the general trace program interface requires resonance')
    if not resonant:E.gaussian(0,phi)
    profile=NewtonProfile(F.q,J)
    answer,stats=(_resonant(shape,E,phi,J,profile,trace_program) if resonant
        else _nonresonant(shape,E,phi,J,profile))
    moments=[]
    for k,c in enumerate(answer):
        actual=(-1)**k*F.q**(t*(t-1)//2-k*(k-1)//2)*c
        if actual.denominator!=1:raise AssertionError(('nonintegral physical kernel moment',k,actual))
        moments.append(actual.numerator)
    return dict(kernel_moments=moments,matrix_size=t,field_degree=F.a,
        primary_shape=shape,maximum=J,supplied_primary_decomposition=True,
        exact_moments=True,full_count_reconstructed=False,
        stats=dict(**stats,total_finite_variable_states=profile.states,
            maximum_degree_states=profile.max_states,hl_coefficient_calls=profile.coefficient_calls,
            maximum_moment_rational_bits=profile.rational_bits,
            maximum_output_bits=max(1,*(abs(x).bit_length() for x in moments)),
            bit_time_bound='(a+1)^{O(1)}(t+1)^{O((J+1)^2)} for fixed J',
            uniform_polynomial_in_J=False,enumerated_full_partition_tables=False,
            seconds=time.perf_counter()-begun))


def literal_primary_kernel_moments(D,field_h,beta,phi=(),eta=0,maximum=2,trace_program=None):
    begun=time.perf_counter();F=Field(field_h);D=[list(row) for row in D];t=len(D)
    if not t or any(len(row)!=t for row in D) or any(type(x) is not int or not 0<=x<F.q for row in D for x in row):
        raise ValueError('nonempty square operator over the supplied field required')
    polynomial=charpoly(D,F);factors=factor_polynomial(polynomial,F)
    if len(factors)!=1:raise ValueError('a single primary operator is required')
    f,m=factors[0];columns=primary_columns(D,f,m,F)
    out=primary_kernel_moments(transpose_partition(columns),field_h,f,beta,phi,eta,maximum,trace_program)
    out.update(supplied_primary_decomposition=False,acquired_characteristic_polynomial=polynomial,
        acquired_irreducible=f,acquired_primary_columns=columns,input_operator_bits=F.a*t*t)
    out['stats']['total_seconds']=time.perf_counter()-begun
    return out


def newton_remainder_value(moments,q,s):
    """Value of the retained polynomial; equals the full one only with all moments."""
    product=1;answer=0
    for k,c in enumerate(moments):
        answer+=c*product
        product*=s-q**k
    return answer


def full_count_from_all_moments(moments,q,t,padding=None):
    """Exact rectangular matrix count; refuses an incomplete moment vector."""
    if len(moments)!=t+1:raise ValueError('all t+1 moments are required for a full integer count')
    T=t if padding is None else padding
    if type(T) is not int or T<0:raise ValueError('nonnegative explicit rectangular width required')
    gap=q**(t*T)*newton_remainder_value(moments,q,q**T)
    domain=q**(t*t+2*t*T)
    return dict(gap=gap,satisfying_count=(domain-gap)//2,
        original_bits=(q.bit_length()-1)*(t*t+2*t*T),full_count_reconstructed=True)
