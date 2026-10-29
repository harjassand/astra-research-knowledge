"""Outward-ball implementation of a quantized nonlinear kinetic receiver.

Input random primitive: iid fair bits. A seeded Random is ONLY a diagnostic.
Every branch governing the output uses exact integers or strictly separated
Arb enclosures. This file does not claim a finite expected arithmetic cost.
"""
from fractions import Fraction as F
from pathlib import Path
from dataclasses import dataclass, asdict
import json, random, time, hashlib, sys
import flint
from flint import arb, acb, fmpq, ctx

sys.dont_write_bytecode = True
DIAGNOSTIC_PRECISION_LIMIT = None  # Optional fail-closed debugging; never a fallback output.
COMPARISON_TRACE = []
NONFINITE_TRACE = []

@dataclass
class Counts:
    bits: int = 0
    comparisons: int = 0
    refinements: int = 0
    max_precision: int = 0
    evaluations: int = 0
    normals: int = 0
    proposals: int = 0
    queries: int = 0
    degree: int = 0
    max_degree: int = 0
    moment_blocks: int = 0
    rotations: int = 0
    singleton_draws: int = 0
    factory_coins: int = 0
    factory_levels: int = 0

class Bits:
    def __init__(self, source, counts):
        self.source, self.counts = source, counts
    def bit(self):
        b = self.source()
        if b not in (0, 1):
            raise ValueError('iid binary source required')
        self.counts.bits += 1
        return int(b)
    def integer(self, n):
        if n < 1:
            raise ValueError('positive categorical denominator required')
        if n == 1:
            return 0
        k = (n-1).bit_length()
        while True:
            x = 0
            for _ in range(k):
                x = 2*x + self.bit()
            if x < n:
                return x

def exact_ball(x):
    x = F(x)
    return arb(fmpq(x.numerator, x.denominator))

def enclosing(lo, hi):
    return arb(exact_ball((lo+hi)/2), exact_ball((hi-lo)/2))

def integer_power(value, n):
    # Arb's generic ** uses exp(n log x), even for Python integer n.
    # In particular an interval containing zero can give NaN for x**2.
    # Polynomial multiplication is defined on every real/complex ball.
    if n < 0:
        return 1/integer_power(value,-n)
    out = arb(1)
    while n:
        if n & 1:
            out = out*value
        n >>= 1
        if n:
            value = value*value
    return out

class Real:
    """A persistent computable-real/complex DAG, with outward balls."""
    def __init__(self, calc, counts, dependencies=None):
        self.calc, self.counts, self.cache = calc, counts, {}
        self.dependencies = dependencies
    def at(self, p):
        stack = [(self,False)]
        while stack:
            node,ready = stack.pop()
            if p in node.cache:
                continue
            if node.dependencies is not None and not ready:
                stack.append((node,True))
                stack.extend((child,False) for child in reversed(node.dependencies))
                continue
            ctx.prec = max(ctx.prec, 2*p+64)
            node.counts.max_precision = max(node.counts.max_precision, ctx.prec)
            node.counts.evaluations += 1
            node.cache[p] = (node.calc(p) if node.dependencies is None else
                            node.calc([child.cache[p] for child in node.dependencies]))
            if p >= 32 and not node.cache[p].is_finite() and len(NONFINITE_TRACE) < 40:
                NONFINITE_TRACE.append(dict(p=p,line=node.calc.__code__.co_firstlineno,
                    value=str(node.cache[p]),operands=[str(child.cache.get(p,'not acquired'))
                    for child in node.dependencies or ()]))
        return self.cache[p]
    def coerce(self, x):
        return x if isinstance(x, Real) else const(x, self.counts)
    def __add__(self, x):
        x = self.coerce(x)
        return Real(lambda a: a[0]+a[1], self.counts, (self,x))
    __radd__ = __add__
    def __neg__(self):
        return Real(lambda a: -a[0], self.counts, (self,))
    def __sub__(self, x):
        return self+-self.coerce(x)
    def __rsub__(self, x):
        return self.coerce(x)+-self
    def __mul__(self, x):
        x = self.coerce(x)
        return Real(lambda a: a[0]*a[1], self.counts, (self,x))
    __rmul__ = __mul__
    def __truediv__(self, x):
        x = self.coerce(x)
        return Real(lambda a: a[0]/a[1], self.counts, (self,x))
    def __rtruediv__(self, x):
        return self.coerce(x)/self
    def __pow__(self, n):
        if not isinstance(n, int):
            raise TypeError('integer exponent required')
        return Real(lambda a: integer_power(a[0],n), self.counts, (self,))
    def sqrt(self):
        return Real(lambda a: a[0].sqrt(), self.counts, (self,))
    def log(self):
        return Real(lambda a: a[0].log(), self.counts, (self,))
    def exp(self):
        return Real(lambda a: a[0].exp(), self.counts, (self,))
    def real(self):
        return Real(lambda a: a[0].real, self.counts, (self,))
    def imag(self):
        return Real(lambda a: a[0].imag, self.counts, (self,))

def const(x, counts):
    if x == 'i':
        return Real(lambda p: acb(0, 1), counts)
    x = F(x)
    return Real(lambda p: exact_ball(x), counts)

class Uniform(Real):
    def __init__(self, bits):
        self.bits, self.prefix, self.depth = bits, 0, 0
        super().__init__(self.enclose, bits.counts)
    def enclose(self, p):
        while self.depth < p:
            self.prefix = 2*self.prefix+self.bits.bit()
            self.depth += 1
        # Use the entire currently acquired prefix, never change a past bit.
        return arb((2*self.prefix+1, -self.depth-1), (1, -self.depth-1))

def less(a, b, counts):
    a = a if isinstance(a, Real) else const(a, counts)
    b = b if isinstance(b, Real) else const(b, counts)
    counts.comparisons += 1
    frame = dict(comparison=counts.comparisons,p=0,last_a='',last_b='')
    COMPARISON_TRACE.append(frame)
    p = 16
    while True:
        frame['p'] = p
        if DIAGNOSTIC_PRECISION_LIMIT is not None and p > DIAGNOSTIC_PRECISION_LIMIT:
            raise RuntimeError('FAIL_CLOSED precision diagnostic '+json.dumps(dict(
                requested=p,last_a=str(aa),last_b=str(bb),counts=asdict(counts),trace=COMPARISON_TRACE,
                nonfinite=NONFINITE_TRACE)))
        try:
            aa, bb = a.at(p), b.at(p)
            frame['last_a'],frame['last_b'] = str(aa),str(bb)
            if aa.is_finite() and bb.is_finite():
                if aa.upper() < bb.lower():
                    COMPARISON_TRACE.pop()
                    return True
                if aa.lower() > bb.upper():
                    COMPARISON_TRACE.pop()
                    return False
        except ZeroDivisionError:
            pass
        counts.refinements += 1
        p *= 2

def coin(probability, bits):
    return less(Uniform(bits), probability, bits.counts)

class Normal(Real):
    def __init__(self, bits):
        self.u, self.lo, self.hi, self.ready = Uniform(bits), F(-1), F(1), False
        self.bits = bits
        bits.counts.normals += 1
        super().__init__(self.enclose, bits.counts)
    def cdf(self, x):
        return Real(lambda p: (1+(exact_ball(x)/arb(2).sqrt()).erf())/2, self.counts)
    def enclose(self, p):
        if not self.ready:
            while less(self.u, self.cdf(self.lo), self.counts):
                self.lo *= 2
            while less(self.cdf(self.hi), self.u, self.counts):
                self.hi *= 2
            self.ready = True
        while self.hi-self.lo > F(1, 1 << p):
            mid = (self.lo+self.hi)/2
            if less(self.u, self.cdf(mid), self.counts):
                self.hi = mid
            else:
                self.lo = mid
        return enclosing(self.lo, self.hi)

def norm2(z):
    return sum(x.real()**2+x.imag()**2 for x in z)

def quadratic(z, e):
    return sum(z[i]*e[i][j]*z[j] for i in range(3) for j in range(3))

def transpose_apply(r, z):
    return [sum(r[3*j+i]*z[j] for j in range(3)) for i in range(3)]

def poisson(rate, bits):
    u = Uniform(bits)
    term = (-rate).exp()
    total, q = term, 0
    while not less(u, total, bits.counts):
        q += 1
        term = term*rate/q
        total = total+term
    return q

ROTATIONS = [
    [1,0,0,0,0,-1,0,1,0], [1,0,0,0,0,1,0,-1,0],
    [0,0,1,0,1,0,-1,0,0], [0,0,-1,0,1,0,1,0,0],
]
E_CATALOG = [
    [[F(-1),0,0],[0,0,0],[0,0,1]],
    [[F(-1,5),F(4,5),0],[F(4,5),F(-1,5),0],[0,0,0]],
]

class Receiver:
    def __init__(self, bits, program):
        self.bits, self.counts, self.program = bits, bits.counts, program
        for col in program['columns']:
            assert min(col['weights']) >= 0 and sum(col['weights']) == col['denominator']
        self.a, self.b, self.c, self.h = F(1), F(11,10), F(21,20), F(1,20)
        self.C = const(self.b**3, self.counts).sqrt()
    def draw_e(self):
        return E_CATALOG[self.bits.bit()]
    def singleton(self, z, left):
        self.counts.singleton_draws += 1
        # left is generally a computable real, not a rational input.
        prob = (-left/4).exp()
        k = sum(coin(prob, self.bits) for _ in range(4))
        col = self.program['columns'][k]
        u, total = self.bits.integer(col['denominator']), 0
        for g, w in enumerate(col['weights']):
            total += w
            if u < total:
                return quadratic(transpose_apply(self.program['group'][g], z), self.draw_e())
        raise AssertionError('invalid exact categorical table')
    def moment(self, q, z, t):
        if q == 0:
            return const(1, self.counts)
        stack, out = [(q,z,t)], const(1, self.counts)
        while stack:
            q,z,left = stack.pop()
            self.counts.moment_blocks += 1
            if q == 1:
                out = out*self.singleton(z,left)
                continue
            wait = -Uniform(self.bits).log()
            if not less(wait,left,self.counts):
                out = out*quadratic(z,self.draw_e())**q
                continue
            self.counts.rotations += 1
            rz = transpose_apply(ROTATIONS[self.bits.integer(4)],z)
            za,zb = [(x+y)/2 for x,y in zip(z,rz)],[(x-y)/2 for x,y in zip(z,rz)]
            ua,ub = norm2(za),norm2(zb)
            j = sum(coin(ua,self.bits) for _ in range(q))
            rest = left-wait
            if j:
                scale = ua.sqrt()
                stack.append((j,[x/scale for x in za],rest))
            if j < q:
                scale = ub.sqrt()
                stack.append((q-j,[x/scale for x in zb],rest))
        return out
    def ratio_over_C(self,v,t):
        self.counts.queries += 1
        xi = [Normal(self.bits) for _ in range(3)]
        imaginary = const('i',self.counts)
        z = [x-imaginary*y/self.b for x,y in zip(xi,v)]
        r2 = norm2(z)
        q = poisson(self.h*r2/2,self.bits)
        self.counts.degree += q
        self.counts.max_degree = max(self.counts.max_degree,q)
        if q:
            scale = r2.sqrt()
            mark = self.moment(q,[x/scale for x in z],t)
        else:
            mark = const(1,self.counts)
        phase = (self.c/self.b-1)*sum(x*y for x,y in zip(xi,v))
        return (((-1)**q)*(imaginary*phase).exp()*mark).real()
    def linear_factory(self,pcoin,epsilon):
        # Huber's established linear Bernoulli factory, multiplier2.
        gamma = F(1,2)
        threshold = F(23,5)/epsilon  # Compute BEFORE min(.644).
        if less(F(161,250),epsilon,self.counts):
            epsilon = const(F(161,250),self.counts)
        i,c = 1,const(2,self.counts)
        while True:
            self.counts.factory_levels += 1
            while True:
                self.counts.factory_coins += 1
                b = pcoin()
                geometric = 1
                while not coin((c-1)/c,self.bits):
                    geometric += 1
                i += -1+(1-int(b))*geometric
                if i == 0 or not less(i,threshold,self.counts):
                    break
            if i == 0:
                return True
            if not coin((1+gamma*epsilon)**(-i),self.bits):
                return False
            c = c*(1+gamma*epsilon)
            epsilon = epsilon*(1-gamma)
            threshold = threshold/(1-gamma)
    def velocity(self,t):
        if F(t) < 0:
            raise ValueError('nonnegative rational time required')
        t = const(F(t),self.counts)
        while True:
            self.counts.proposals += 1
            scale = const(self.b,self.counts).sqrt()
            v = [scale*Normal(self.bits) for _ in range(3)]
            ell = (-(1-1/self.b)*sum(x*x for x in v)/2).exp()
            def pcoin():
                return coin((1-self.ratio_over_C(v,t))/2,self.bits)
            if not self.linear_factory(pcoin,ell/self.C):
                return v

def dyadic_fraction(x):
    mantissa,exponent = x.man_exp()
    mantissa,exponent = int(mantissa),int(exponent)
    return F(mantissa*(1 << exponent)) if exponent >= 0 else F(mantissa,1 << -exponent)

def quantize(x,h,counts):
    if F(h) <= 0:
        raise ValueError('positive rational bin width required')
    p = 16
    while True:
        a = x.at(p)
        if a.is_finite():
            lo,hi = dyadic_fraction(a.lower())/h,dyadic_fraction(a.upper())/h
            flo,fhi = lo.numerator//lo.denominator,hi.numerator//hi.denominator
            if flo == fhi:
                return flo
        counts.refinements += 1
        p *= 2

def run(times,per_time,seed):
    raw = (Path(__file__).resolve().parents[1]/'t_collision_operation/outputs/FINITE_SINGLETON_PROGRAM.json').read_bytes()
    program = json.loads(raw)
    rng = random.Random(seed)
    rows = []
    for t in times:
        counts = Counts()
        bits = Bits(lambda:rng.getrandbits(1),counts)
        receiver = Receiver(bits,program)
        outputs = []
        tick = time.perf_counter()
        for _ in range(per_time):
            v = receiver.velocity(F(t))
            outputs.append([quantize(x,F(1,4),counts) for x in v])
        rows.append(dict(t=str(t),n=per_time,quantization_width='1/4',integer_bins=outputs,
                         counts=asdict(counts),seconds=time.perf_counter()-tick))
    return dict(scope='certified strict-ball branches, quantized output; iid-bit law theorem separate from seeded diagnostic; expected total bit cost UNKNOWN',
                python_flint_version=flint.__version__,seed=seed,
                program_sha256=hashlib.sha256(raw).hexdigest(),rows=rows)

if __name__ == '__main__':
    result = run([F(x) for x in sys.argv[1:]] or [F(0),F(3),F(1000000)],3,2026102987)
    Path(__file__).with_name('EXECUTION.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
