"""Integer-only exact finite-group draw GIVEN iid fair input bits.

Time must be a nonnegative rational. No floats/transcendentals appear in
the draw. A seeded PRNG is only the execution diagnostic, not the ideal law.
von Neumann's descending-run exp coin is established ordinary machinery.
"""
from fractions import Fraction as F
from pathlib import Path
import json,random,time,hashlib,math

class Bits:
    def __init__(self,bit):
        self.source=bit;self.bits=0;self.unit_calls=0;self.max_run=0;self.max_prefix=0
    def bit(self):
        b=self.source()
        if b not in (0,1):raise ValueError('bit source must return0 or1')
        self.bits+=1;return int(b)
    def integer(self,n):
        if n<1:raise ValueError('positive integer range required')
        if n==1:return 0
        k=(n-1).bit_length()
        while True:
            value=0
            for _ in range(k):value=2*value+self.bit()
            if value<n:return value

class Uniform:
    def __init__(self,bits):self.bits=bits;self.depth=0;self.value=0
    def prefix(self,k):
        while self.depth<k:
            self.value=2*self.value+self.bits.bit();self.depth+=1
            self.bits.max_prefix=max(self.bits.max_prefix,self.depth)
        return self.value>>(self.depth-k)
    def below_rational(self,x):
        if x<=0:return False
        if x>=1:return True
        k=0
        while True:
            k+=1;p=self.prefix(k);scale=x.numerator*(1<<k)
            if (p+1)*x.denominator<=scale:return True
            if p*x.denominator>=scale:return False
    def below_uniform(self,other):
        k=0
        while True:
            k+=1;a=self.prefix(k);b=other.prefix(k)
            if a!=b:return a<b

def unit_exp_coin(x,bits):
    """Bernoulli(exp(-x)), exact rational0<=x<=1 via descending run parity."""
    assert isinstance(x,F) and 0<=x<=1
    if not x:return True
    bits.unit_calls+=1;length=0;previous=x
    while True:
        u=Uniform(bits)
        below=u.below_rational(previous) if isinstance(previous,F) else u.below_uniform(previous)
        if not below:
            bits.max_run=max(bits.max_run,length);return length%2==0
        length+=1;previous=u

def exp_coin(x,bits):
    """Bernoulli(exp(-x)) for finite rational x>=0; lazy product, no exp call."""
    if not isinstance(x,(int,F)):raise TypeError('exact integer/Fraction input required')
    x=F(x)
    if x<0:raise ValueError('nonnegative exponent required')
    whole=x.numerator//x.denominator;fraction=x-whole;i=0
    while i<whole:
        if not unit_exp_coin(F(1),bits):return False
        i+=1
    return unit_exp_coin(fraction,bits)

class Singleton:
    def __init__(self,program):
        self.program=program
        assert len(program['group'])==24 and len(program['columns'])==5
        for c in program['columns']:
            assert all(isinstance(w,int) and w>=0 for w in c['weights'])
            assert sum(c['weights'])==c['denominator']
    def draw_group_index(self,t,bits):
        if not isinstance(t,(int,F)):raise TypeError('exact rational time required')
        t=F(t)
        if t<0:raise ValueError('nonnegative time required')
        k=sum(exp_coin(t/4,bits) for _ in range(4))
        col=self.program['columns'][k];u=bits.integer(col['denominator']);total=0
        for g,w in enumerate(col['weights']):
            total+=w
            if u<total:return g
        raise AssertionError('categorical column not normalized')

def run():
    rng=random.Random(2026102971);out={'coin_controls':[],'group_controls':[]}
    for x in (F(0),F(1,2),F(1),F(7,4),F(1000000)):
        bits=Bits(lambda:rng.getrandbits(1));tick=time.perf_counter();n=20000
        successes=sum(exp_coin(x,bits) for _ in range(n));p=math.exp(-float(x))
        out['coin_controls'].append(dict(x=str(x),n=n,successes=successes,reference_float=p,
             fair_bits=bits.bits,unit_calls=bits.unit_calls,max_run=bits.max_run,max_prefix=bits.max_prefix,
             seconds=time.perf_counter()-tick))
    path=Path(__file__).resolve().parents[1]/'t_collision_operation/outputs/FINITE_SINGLETON_PROGRAM.json'
    raw=path.read_bytes();sampler=Singleton(json.loads(raw))
    for t in (F(0),F(3),F(1000000)):
        bits=Bits(lambda:rng.getrandbits(1));counts=[0]*24;tick=time.perf_counter();n=10000
        for _ in range(n):counts[sampler.draw_group_index(t,bits)]+=1
        out['group_controls'].append(dict(t=str(t),n=n,counts=counts,fair_bits=bits.bits,
             unit_calls=bits.unit_calls,max_run=bits.max_run,max_prefix=bits.max_prefix,seconds=time.perf_counter()-tick))
    out.update(scope='integer-only draw algorithm exact under iid fair bits; seed is diagnostic only; not full velocity output',
               seed=2026102971,program_sha256=hashlib.sha256(raw).hexdigest(),
               theoretical_expected_bit_bound_per_group_draw=512,
               time_contract='nonnegative rational; arithmetic input bits charged; no float/exp in draw')
    return out

if __name__=='__main__':
    result=run();Path(__file__).with_name('FAIRBIT_EXECUTION.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('scope','program_sha256','theoretical_expected_bit_bound_per_group_draw')},indent=2))
    print([(x['t'],x['fair_bits']/x['n'],x['seconds']) for x in result['group_controls']])
