"""Explicit finite-bit Chen--Liu homogeneous counting program.

Scientific guarantee is CONDITIONAL on their exchange-gap theorem. Generic
large-instance branches are acquired code, not a claim of execution here.
The CLI only executes tiny exact fixtures and prints certified loop budgets.
The count program has no silent shortened chain or unbounded rejection loop.
Coefficient LC/range contracts are inputs, not inferred from finite checks.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import combinations
from math import ceil
import json
import random
from pathlib import Path


def ceil_log2(q):
    q=F(q)
    if q<=1: return 0
    # Exact logarithm ceiling in O(log of answer) big-integer work.
    k=max(0,q.numerator.bit_length()-q.denominator.bit_length())
    while q.numerator>q.denominator*(1<<k): k+=1
    while k>0 and q.numerator<=q.denominator*(1<<(k-1)): k-=1
    return k


def ceil_fraction(q):
    q=F(q)
    return (q.numerator+q.denominator-1)//q.denominator


@dataclass(frozen=True)
class Problem:
    n: int
    a: int
    mu: object
    nu: object
    s0: int
    t0: int
    range_bits_mu: int
    range_bits_nu: int
    # This flag is a PROVED contract, never guessed by this implementation.
    self_complementary: bool=False

    def validate(self):
        assert self.n>=0 and 0<=self.a<=self.n
        assert self.range_bits_mu>=0 and self.range_bits_nu>=0
        assert self.s0.bit_count()==self.a
        assert self.t0.bit_count()==self.n-self.a
        assert 0<=self.s0<(1<<self.n) and 0<=self.t0<(1<<self.n)
        assert F(self.mu(self.s0))>0 and F(self.nu(self.t0))>0
        if self.self_complementary: assert 2*self.a==self.n


@dataclass
class CertifiedPlan:
    n: int
    rho: F
    penalty: F
    cd_updates: int
    cd_batches: int
    cd_batch_samples: int
    normalizer_batch_samples: int
    overlap_samples: int
    total_samples: int
    sample_tv: F
    stationary_log2_lower_bound: int
    exchange_steps_per_sample: int
    total_exchange_steps: int
    binary_choice_cap: int
    coin_digits_per_choice: int
    total_coin_digits: int

    def json(self):
        return {k:str(v) if isinstance(v,F) else v for k,v in self.__dict__.items()}


def certified_plan(problem,rho):
    problem.validate(); n=problem.n; rho=F(rho)
    assert n>=2 and 0<rho<=1 and 0<problem.a<n
    # Exact complement symmetry gives zero gradient, permitting a larger t.
    t=F(1,(64 if problem.self_complementary else 256)*n*n); eta=F(1,4*n)
    bits=problem.range_bits_mu+problem.range_bits_nu
    b=2*n+bits
    if problem.self_complementary:
        updates=batches=cd_m=0
    else:
        updates=ceil_fraction(128*b/(eta*eta))+1
        batches=updates+1
        cd_m=ceil_fraction(32/(eta*eta)*ceil_log2(128*n*batches))
    alpha=rho/(64*n)
    norm_m=ceil_fraction(ceil_log2(256*n)/(2*alpha*alpha))
    overlap_m=ceil_fraction(ceil_log2(128)/(2*(rho/8)**2))
    total=batches*cd_m+2*n*norm_m+overlap_m
    sample_tv=F(1,256*total)
    penalty_bits=(6 if problem.self_complementary else 8)+2*ceil_log2(n)
    # log2(1+1/(32n)) <= 1/(16n), using ln(2)>=1/2.
    field_bits=(updates+16*n-1)//(16*n)
    h=2*n+bits+min(problem.a,n-problem.a)*penalty_bits+n*field_bits
    steps=ceil_fraction((2*n/t)*(h+ceil_log2(1/sample_tv)+2))
    all_steps=steps*total
    choice_cap=(2*n+1)*all_steps
    coin_digits=ceil_log2(64*max(1,choice_cap))
    return CertifiedPlan(n,rho,t,updates,batches,cd_m,norm_m,overlap_m,total,
                         sample_tv,h,steps,all_steps,choice_cap,coin_digits,
                         choice_cap*coin_digits)


class TapeAbort(Exception):
    pass


class BoundedCoins:
    def __init__(self,bit_source,binary_choice_cap,digits_per_choice):
        self.bit_source=bit_source
        self.cap=binary_choice_cap
        self.digits_per_choice=digits_per_choice
        self.choices=0; self.digits=0

    def bernoulli(self,p):
        p=F(p)
        assert 0<=p<=1
        if p==0: return False
        if p==1: return True
        self.choices+=1
        if self.choices>self.cap: raise TapeAbort("binary choice cap")
        prefix=0
        for r in range(1,self.digits_per_choice+1):
            bit=self.bit_source()
            if bit not in (0,1): raise ValueError("bit source returned a non-bit")
            prefix=2*prefix+bit; self.digits+=1
            if prefix*p.denominator>=p.numerator*(1<<r): return False
            if (prefix+1)*p.denominator<=p.numerator*(1<<r): return True
        raise TapeAbort("rational-coin ambiguity cap")

    def categorical(self,weights):
        weights=[F(w) for w in weights]
        assert weights and all(w>=0 for w in weights)
        remaining=sum(weights,F(0)); assert remaining>0
        for i,w in enumerate(weights[:-1]):
            if self.bernoulli(w/remaining): return i
            remaining-=w
        assert weights[-1]>0
        return len(weights)-1


def restricted(original,forced,forbidden):
    def coefficient(mask):
        if (mask&forced)!=forced or mask&forbidden: return F(0)
        return F(original(mask))
    return coefficient


def exchange_step(problem,mu,nu,fields,state,penalty,coins):
    n=problem.n; s,t=state
    present=[(0,u) for u in range(n) if (s>>u)&1]
    present +=[(1,u) for u in range(n) if (t>>u)&1]
    assert len(present)==n
    side,u=present[coins.categorical([1]*n)]
    current,other=(s,t) if side==0 else (t,s)
    acceptance=F(1,2) if (other>>u)&1 else penalty/2
    if not coins.bernoulli(acceptance): return state
    base=current&~(1<<u)
    oracle=mu if side==0 else nu
    candidates=[v for v in range(n) if not (base>>v)&1]
    weights=[fields[v]*F(oracle(base|(1<<v))) for v in candidates]
    assert sum(weights,F(0))>0  # reinsertion of u is always feasible
    v=candidates[coins.categorical(weights)]
    new=base|(1<<v)
    assert F(oracle(new))>0
    return (new,t) if side==0 else (s,new)


def soft_sample(problem,mu,nu,fields,state,plan,coins):
    # Every draw has the same explicit worst-case mixing cap. Conditional on
    # all earlier history, its ideal law is within plan.sample_tv of stationarity.
    assert F(mu(state[0]))>0 and F(nu(state[1]))>0
    for _ in range(plan.exchange_steps_per_sample):
        state=exchange_step(problem,mu,nu,fields,state,plan.penalty,coins)
    return state


def find_fields(problem,plan,coins):
    n=problem.n; fields=[F(1)]*n
    if problem.self_complementary: return fields
    eta=F(1,4*n); update_base=1+eta/8
    state=(problem.s0,problem.t0)
    for iteration in range(plan.cd_batches):
        sums=[0]*n
        for _ in range(plan.cd_batch_samples):
            state=soft_sample(problem,problem.mu,problem.nu,fields,state,plan,coins)
            s,t=state
            for u in range(n): sums[u]+=((s>>u)&1)+((t>>u)&1)-1
        gradients=[F(x,plan.cd_batch_samples) for x in sums]
        u=max(range(n),key=lambda u:abs(gradients[u]))
        if abs(gradients[u])<=eta/2: return fields
        if iteration>=plan.cd_updates: return None
        fields[u]=fields[u]/update_base if gradients[u]>0 else fields[u]*update_base
    return None


def soft_weight(problem,fields,state,penalty):
    s,t=state
    value=F(problem.mu(s))*F(problem.nu(t))*penalty**((s&t).bit_count())
    for u,z in enumerate(fields):
        if (s>>u)&1: value*=z
        if (t>>u)&1: value*=z
    return value


def normalizer(problem,fields,plan,coins):
    n=problem.n
    forced=[0,0]; forbidden=[0,0]
    state=(problem.s0,problem.t0)
    product_probability=F(1)
    for side,u in [(side,u) for side in (0,1) for u in range(n)]:
        mu=restricted(problem.mu,forced[0],forbidden[0])
        nu=restricted(problem.nu,forced[1],forbidden[1])
        ones=0; witness=[None,None]
        for _ in range(plan.normalizer_batch_samples):
            state=soft_sample(problem,mu,nu,fields,state,plan,coins)
            bit=(state[side]>>u)&1
            ones+=bit; witness[bit]=state
        chosen=int(2*ones>=plan.normalizer_batch_samples)
        number=ones if chosen else plan.normalizer_batch_samples-ones
        assert number>0 and witness[chosen] is not None
        product_probability*=F(number,plan.normalizer_batch_samples)
        state=witness[chosen]
        if chosen: forced[side]|=1<<u
        else: forbidden[side]|=1<<u
    value=soft_weight(problem,fields,state,plan.penalty)
    assert value>0 and product_probability>0
    return value/product_probability


def exact_small(problem,maximum_n=12):
    problem.validate()
    if problem.n>maximum_n: raise ValueError("outside constant-size exact branch")
    all_bits=(1<<problem.n)-1
    value=F(0)
    for subset in combinations(range(problem.n),problem.a):
        mask=sum(1<<i for i in subset)
        value+=F(problem.mu(mask))*F(problem.nu(all_bits^mask))
    return value


def count(problem,rho,bit_source,exact_cutoff=12):
    """Return one complete 3/4-success count repetition.

    Calling this on n>exact_cutoff intentionally executes the enormous certified
    loops. There is no lowered experimental budget in this function. The caller
    can inspect certified_plan first. Whole-count coin aborts return zero.
    """
    problem.validate(); rho=F(rho); assert 0<rho<=1
    if problem.a in (0,problem.n):
        mask=0 if problem.a==0 else (1<<problem.n)-1
        return F(problem.mu(mask))*F(problem.nu(((1<<problem.n)-1)^mask))
    if problem.n<=exact_cutoff: return exact_small(problem,exact_cutoff)
    plan=certified_plan(problem,rho)
    coins=BoundedCoins(bit_source,plan.binary_choice_cap,plan.coin_digits_per_choice)
    try:
        fields=find_fields(problem,plan,coins)
        if fields is None: return F(0)
        zhat=normalizer(problem,fields,plan,coins)
        state=(problem.s0,problem.t0); complementary=0; all_bits=(1<<problem.n)-1
        for _ in range(plan.overlap_samples):
            state=soft_sample(problem,problem.mu,problem.nu,fields,state,plan,coins)
            complementary+=int(state[1]==(all_bits^state[0]))
        p=F(complementary,plan.overlap_samples)
        return p*zhat/sum_product(fields)
    except TapeAbort:
        return F(0)


def sum_product(values):
    result=F(1)
    for v in values: result*=v
    return result


def amplified_count(problem,rho,failure_probability,bit_source,exact_cutoff=12):
    failure_probability=F(failure_probability)
    assert 0<failure_probability<1
    repetitions=8*ceil_log2(1/failure_probability)+1
    answers=[count(problem,rho,bit_source,exact_cutoff) for _ in range(repetitions)]
    return sorted(answers)[len(answers)//2]


def transition_matrix(problem,fields,penalty):
    """Independent finite-state diagnostic, not used by the count program."""
    n=problem.n
    def support(oracle,degree):
        return [sum(1<<i for i in subset) for subset in combinations(range(n),degree)
                if F(oracle(sum(1<<i for i in subset)))>0]
    states=[(s,t) for s in support(problem.mu,problem.a) for t in support(problem.nu,n-problem.a)]
    index={x:i for i,x in enumerate(states)}
    matrix=[[F(0) for _ in states] for _ in states]
    for i,(s,t) in enumerate(states):
        for side,current,other,oracle in ((0,s,t,problem.mu),(1,t,s,problem.nu)):
            for u in range(n):
                if not (current>>u)&1: continue
                accept=F(1,2) if (other>>u)&1 else penalty/2
                matrix[i][i]+=(1-accept)/n
                base=current&~(1<<u)
                candidates=[v for v in range(n) if not (base>>v)&1]
                weights=[fields[v]*F(oracle(base|(1<<v))) for v in candidates]
                denominator=sum(weights,F(0)); assert denominator>0
                for v,w in zip(candidates,weights):
                    new=base|(1<<v); target=(new,t) if side==0 else (s,new)
                    if w: matrix[i][index[target]]+=accept*w/(n*denominator)
        assert sum(matrix[i],F(0))==1
    weights=[soft_weight(problem,fields,x,penalty) for x in states]
    for i in range(len(states)):
        for j in range(len(states)):
            assert weights[i]*matrix[i][j]==weights[j]*matrix[j][i]
    return states,matrix


def diagnostics():
    mu=lambda s: F({1:2,2:3}.get(s,0))
    nu=lambda s: F({1:5,2:7}.get(s,0))
    problem=Problem(2,1,mu,nu,1,1,1,1)
    assert exact_small(problem)==29
    rng=random.Random(1729)
    assert count(problem,F(1,4),lambda:rng.getrandbits(1))==29
    states,matrix=transition_matrix(problem,[F(1,3),F(7,5)],F(1,1024))
    assert len(states)==4
    coins=BoundedCoins(lambda:rng.getrandbits(1),10000,64)
    state=(1,1)
    for _ in range(250):
        state=exchange_step(problem,mu,nu,[F(1,3),F(7,5)],state,F(1,1024),coins)
        assert mu(state[0])>0 and nu(state[1])>0
    forced_mu=restricted(mu,1,0)
    forced=Problem(2,1,forced_mu,nu,1,1,1,1)
    forced_states,_=transition_matrix(forced,[F(1,3),F(7,5)],F(1,1024))
    assert len(forced_states)==2
    for _ in range(250):
        state=exchange_step(forced,forced_mu,nu,[F(1,3),F(7,5)],(1,state[1]),F(1,1024),coins)
        assert state[0]==1 and nu(state[1])>0
    ones=lambda s:F(int(s.bit_count()==1))
    balanced=Problem(2,1,ones,ones,1,1,0,0,True)
    # Verify rational coins against every 8-bit prefix for denominator256 cases.
    for numerator in (0,1,51,127,128,255,256):
        true_count=0
        for prefix in range(256):
            bits=iter((prefix>>(7-i))&1 for i in range(8))
            tape=BoundedCoins(lambda:next(bits),1,8)
            true_count+=int(tape.bernoulli(F(numerator,256)))
        assert true_count==numerator
    return {"status":"PASS","scope":"exact branch and finite exchange/coin diagnostics only; generic full certified loops NOT executed",
            "exact_count":29,"exchange_states":4,"forced_exchange_states":2,
            "executed_exchange_steps":500,"coin_threshold_prefix_checks":7*256,
            "n2_general_plan":certified_plan(problem,F(1,4)).json(),
            "n2_self_complementary_plan":certified_plan(balanced,F(1,4)).json()}


if __name__=="__main__":
    result=diagnostics()
    target=Path(__file__).with_name("homogeneous_count_checks.json")
    target.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))
