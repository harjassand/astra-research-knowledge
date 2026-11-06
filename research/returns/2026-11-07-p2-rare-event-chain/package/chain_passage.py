"""Certified finite-pattern first passage for open zero-field Ising chains.

Only Python integers/Fraction and NumPy object arrays enter certificates.
No floating-point arithmetic, simulation, full-state generator, or spectral
oracle enters the algorithms below.  See RESEARCH_REPORT.txt for the model,
analytic enclosure proofs, and bit-cost theorem.  This is a reference
construction, not a claim of optimized practical performance.
"""
from fractions import Fraction as F
from dataclasses import dataclass
from math import prod, factorial
import numpy as np


def bits_for(x):
    x = F(x)
    if x <= 0:
        raise ValueError("positive tolerance required")
    b = max(0, x.denominator.bit_length() - x.numerator.bit_length())
    while F(1, 1 << b) > x:
        b += 1
    return b


def ceilq(x):
    x = F(x)
    return -((-x.numerator) // x.denominator)


def ceil_log2(x):
    x = F(x)
    if x <= 1:
        return 0
    k = max(0, x.numerator.bit_length() - x.denominator.bit_length())
    while (1 << k) < x:
        k += 1
    return k


def nearest_div(a, b):
    if b < 0:
        a,b=-a,-b
    return (2 * int(a) + int(b)) // (2 * int(b))


def dyad(x, b):
    x = F(x)
    return F(nearest_div(x.numerator * (1 << b), x.denominator), 1 << b)


@dataclass(frozen=True)
class C:
    re: F = F(0)
    im: F = F(0)

    def __post_init__(self):
        object.__setattr__(self, 're', F(self.re))
        object.__setattr__(self, 'im', F(self.im))

    @staticmethod
    def make(x):
        return x if isinstance(x, C) else C(x)

    def __add__(self, x):
        x = C.make(x)
        return C(self.re + x.re, self.im + x.im)

    __radd__ = __add__

    def __neg__(self):
        return C(-self.re, -self.im)

    def __sub__(self, x):
        return self + (-C.make(x))

    def __rsub__(self, x):
        return C.make(x) - self

    def __mul__(self, x):
        x = C.make(x)
        return C(self.re*x.re-self.im*x.im, self.re*x.im+self.im*x.re)

    __rmul__ = __mul__

    def __truediv__(self, x):
        x = C.make(x)
        q = x.re*x.re+x.im*x.im
        if not q:
            raise ZeroDivisionError
        return C((self.re*x.re+self.im*x.im)/q,
                 (self.im*x.re-self.re*x.im)/q)

    def __rtruediv__(self, x):
        return C.make(x) / self

    def abs1(self):
        return abs(self.re) + abs(self.im)

    def abslo(self):
        return max(abs(self.re), abs(self.im))

    def conj(self):
        return C(self.re, -self.im)


@dataclass(frozen=True)
class Ball:
    mid: C
    err: F

    def __post_init__(self):
        object.__setattr__(self, 'mid', C.make(self.mid))
        object.__setattr__(self, 'err', F(self.err))

    def round(self, tolerance):
        b = bits_for(F(tolerance)) + 2
        mid = C(dyad(self.mid.re, b), dyad(self.mid.im, b))
        return Ball(mid, self.err + F(1, 1 << b))

    def compact(self, extra_error):
        """Dyadic center AND outward-rounded radius; increase <= extra_error/2."""
        b=bits_for(extra_error)+2
        unit=F(1,1 << b)
        mid=C(dyad(self.mid.re,b),dyad(self.mid.im,b))
        radius=ceilq((self.err+unit)/unit)*unit
        return Ball(mid,radius)


def zeros(n):
    return np.zeros((n, n), dtype=object)


def iround(A, den):
    return np.array([nearest_div(v, den) for v in A.flat], dtype=object).reshape(A.shape)


def mm(A, B):
    ar, ai = A
    br, bi = B
    if not np.any(ai) and not np.any(bi):
        return ar @ br, zeros(len(ar))
    return ar @ br - ai @ bi, ar @ bi + ai @ br


def trimm(A, B):
    """Exact A B when B is tridiagonal."""
    n = len(A[0])
    out = []
    for ar, ai, br, bi in [(A[0], A[1], B[0], B[1]),
                           (A[1], -A[0], B[0], B[1])]:
        o = zeros(n)
        for j in range(n):
            for k in range(max(0, j-1), min(n, j+2)):
                o[:, j] += ar[:, k]*br[k, j] - ai[:, k]*bi[k, j]
        out.append(o)
    return out[0], out[1]


def exp_fixed(A, bound, tolerance, tridiagonal=False, stats=None):
    """exp(A), with all exp(A/2^j) bounded in complex-row-l1 norm by bound.

    A is a pair of exact rational matrices. Output integer matrices divided
    by 2^P, with certified row-l1 error <= tolerance. The bound is a proved
    model property, not inferred from a numerical exponential.
    """
    n = len(A[0])
    norm = max(sum(abs(A[0][i][j])+abs(A[1][i][j]) for j in range(n)) for i in range(n))
    scaling = ceil_log2(8*norm)
    B = 2*ceilq(bound)+2
    p = bits_for(tolerance) + scaling*ceil_log2(B) + ceil_log2(64*n) + 12
    while True:
        N = 0
        tail = F(1, 2)  # 2*(1/4)^(N+1)/(N+1)!, at N=0
        while tail > F(1, 1 << p):
            N += 1
            tail /= 4*(N+1)
        err = F(B**scaling * 4*n*(N+3), 1 << p)
        if err <= tolerance and F(n, 1 << p) <= F(1, 8):
            break
        p += 8
    S = 1 << p
    den = 1 << scaling
    Z = tuple(np.array([[nearest_div(F(v).numerator*S,
                                     F(v).denominator*den) for v in row]
                        for row in part], dtype=object) for part in A)
    T = (np.eye(n, dtype=object)*S, zeros(n))
    V = (T[0].copy(), T[1].copy())
    for k in range(1, N+1):
        T = trimm(T, Z) if tridiagonal else mm(T, Z)
        T = (iround(T[0], S*k), iround(T[1], S*k))
        V = (V[0]+T[0], V[1]+T[1])
    for _ in range(scaling):
        V = mm(V, V)
        V = (iround(V[0], S), iround(V[1], S))
    if stats is not None:
        stats['exponentials'] = stats.get('exponentials', 0)+1
        stats['max_fixed_bits'] = max(stats.get('max_fixed_bits', 0), p)
        stats['max_scalings'] = max(stats.get('max_scalings', 0), scaling)
        stats['max_taylor_terms'] = max(stats.get('max_taylor_terms', 0), N)
    return V, S, err


def exp_ball(w, tolerance, stats=None):
    w = C.make(w)
    if w.re > 1:
        raise ValueError('this primitive is contracted only for Re(w)<=1')
    cutoff = max(1, bits_for(tolerance))
    if w.re <= -cutoff:
        return Ball(C(), F(1, 1 << cutoff))
    bound = (1 if w.im == 0 else 2) if w.re <= 0 else 4
    scaling=ceil_log2(8*w.abs1()); B=2*bound+2
    p=bits_for(tolerance)+scaling*ceil_log2(B)+18
    while True:
        N=0; tail=F(1,2)
        while tail > F(1,1 << p):
            N+=1; tail/=4*(N+1)
        err=F(B**scaling*4*(N+3),1 << p)
        if err <= tolerance:
            break
        p+=8
    S=1 << p
    z=(nearest_div(w.re.numerator*S,w.re.denominator*(1 << scaling)),
       nearest_div(w.im.numerator*S,w.im.denominator*(1 << scaling)))
    term=(S,0); value=(S,0)
    for k in range(1,N+1):
        v=gmul(term,z)
        term=(nearest_div(v[0],S*k),nearest_div(v[1],S*k))
        value=(value[0]+term[0],value[1]+term[1])
    for _ in range(scaling):
        v=gmul(value,value)
        value=(nearest_div(v[0],S),nearest_div(v[1],S))
    if stats is not None:
        stats['scalar_exponentials']=stats.get('scalar_exponentials',0)+1
    return Ball(C(F(value[0],S),F(value[1],S)),err)


def gmul(a, b):
    return a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0]


def gsub(a, b):
    return a[0]-b[0], a[1]-b[1]


def gdiv_exact(a, b):
    den = b[0]*b[0]+b[1]*b[1]
    r, i = a[0]*b[0]+a[1]*b[1], a[1]*b[0]-a[0]*b[1]
    assert den and r % den == 0 and i % den == 0
    return r//den, i//den


def pfaffian_integer(ar, ai):
    """Fraction-free Pfaffian over Gaussian integers, with exact pivoting."""
    n = len(ar)
    if n % 2:
        raise ValueError('even order required')
    if not n:
        return (1, 0)
    A = [[(int(ar[i,j]), int(ai[i,j])) for j in range(n)] for i in range(n)]
    previous, sign = (1, 0), 1
    for k in range(0, n-1, 2):
        pivot = next((j for j in range(k+1, n) if A[k][j] != (0,0)), None)
        if pivot is None:
            return (0,0)
        if pivot != k+1:
            A[pivot], A[k+1] = A[k+1], A[pivot]
            for row in A:
                row[pivot], row[k+1] = row[k+1], row[pivot]
            sign = -sign
        p = A[k][k+1]
        if k == n-2:
            return sign*p[0], sign*p[1]
        for i in range(k+2, n):
            for j in range(i+1, n):
                num = gsub(gsub(gmul(p, A[i][j]), gmul(A[k][i], A[k+1][j])),
                           tuple(-v for v in gmul(A[k][j], A[k+1][i])))
                v = gdiv_exact(num, previous)
                A[i][j], A[j][i] = v, (-v[0], -v[1])
        previous = p
    raise AssertionError


class Chain:
    def __init__(self, bonds, clocks):
        self.t = tuple(map(F, bonds))
        self.lam = tuple(map(F, clocks))
        self.n = len(self.lam)
        n = self.n
        if n < 1 or len(self.t) != n-1 or any(not 0 <= t < 1 for t in self.t) or any(l <= 0 for l in self.lam):
            raise ValueError('open ferromagnetic finite-temperature contract')
        t = (F(0),) + self.t + (F(0),)
        self.a = tuple(t[i]*(1-t[i+1]**2)/(1-t[i]**2*t[i+1]**2) for i in range(n))
        self.b = tuple(t[i+1]*(1-t[i]**2)/(1-t[i]**2*t[i+1]**2) for i in range(n))
        self.K = [[F(0) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            self.K[i][i] = self.lam[i]
            if i:
                self.K[i][i-1] = -self.lam[i]*self.a[i]
            if i+1 < n:
                self.K[i][i+1] = -self.lam[i]*self.b[i]
        w = [(1-t[i]**2*t[i+1]**2)/(self.lam[i]*(1-t[i]**2)*(1-t[i+1]**2)) for i in range(n)]
        self.CU = 2*n*max(w)/min(w)
        self.Lambda = sum(self.lam)
        self.G = 2*self.Lambda
        self.g = min(self.lam[i]*(1-self.a[i]-self.b[i]) for i in range(n))
        self.pimin = prod(1-v for v in self.t)*F(1, 1 << n)
        self.C = 1/self.pimin
        self.D = prod(v.denominator for v in self.t)
        self.eq = zeros(n)
        for i in range(n):
            q = F(1)
            for j in range(i+1, n):
                q *= self.t[j-1]
                v = q*self.D
                assert v.denominator == 1
                self.eq[i,j], self.eq[j,i] = v.numerator, -v.numerator
        self.stats = {}

    def pattern(self, x):
        x = tuple(x)
        if len(x) != self.n or any(v not in (-1,1) for v in x):
            raise ValueError('each pattern must explicitly list n signs')
        return x

    def stationary(self, x):
        x = self.pattern(x)
        return prod(1+self.t[i]*x[i]*x[i+1] for i in range(self.n-1))*F(1, 1 << self.n)

    def kernels(self, z, starts, ends, tolerance, odd=False):
        """All requested transition entries; odd means P_z(y,y)-P_z(-y,y).

        For odd=True require starts=ends=[y]. It uses one Pfaffian linear
        in the ghost row, and therefore avoids subtraction of nearly equal
        equilibrium probabilities.
        """
        z, tolerance = C.make(z), F(tolerance)
        if z.re < 0 or tolerance <= 0:
            raise ValueError('Re(time)>=0 and positive accuracy required')
        starts = [self.pattern(x) for x in starts]
        ends = [self.pattern(y) for y in ends]
        if odd and not (len(starts) == len(ends) == 1 and starts[0] == ends[0]):
            raise ValueError('odd diagonal contract')
        cutoff = max(1, ceil_log2((1 if odd else self.C)/tolerance))
        if self.g*z.re >= cutoff:
            error = (1 if odd else self.C)*F(1, 1 << cutoff)
            self.stats['stationary_shortcuts'] = self.stats.get('stationary_shortcuts',0)+1
            return [[Ball(0 if odd else self.stationary(y), error) for y in ends] for x in starts]
        n = self.n
        d = n+1+(n+1)%2
        r = d//2
        CU = F(1) if z.im == 0 else self.CU
        H = F(2) if z.im == 0 else 4+2*n*n*CU*CU+CU
        Aerr = 1+2*n*n*(2*CU+1)
        matchings = prod(range(1, d, 2))
        Lip = r*matchings*(H+1)**(r-1)
        eta = min(1/Aerr, tolerance/(4*Lip*Aerr))
        expA = ([[ -z.re*v for v in row] for row in self.K],
                [[ -z.im*v for v in row] for row in self.K])
        U, S, uerr = exp_fixed(expA, CU, eta, tridiagonal=True, stats=self.stats)
        den = S*S*self.D
        out = []
        for x in starts:
            c0 = zeros(n)
            for i in range(n):
                for j in range(i+1, n):
                    c0[i,j] = self.D*x[i]*x[j]
                    c0[j,i] = -c0[i,j]
            Dm = c0-self.eq
            UD = (U[0] @ Dm, U[1] @ Dm)
            pair = mm(UD, (U[0].T, U[1].T))
            pair = (pair[0]+self.eq*S*S, pair[1])
            means = (U[0] @ np.array(x, dtype=object), U[1] @ np.array(x, dtype=object))
            row = []
            for y in ends:
                ar, ai = zeros(d), zeros(d)
                for i in range(d):
                    for j in range(i+1, d):
                        v = 0 if odd and i == 0 else ((-1)**(i+j+1))*den
                        vi = 0
                        if i == 0 and j <= n:
                            v += means[0][j-1]*y[j-1]*S*self.D
                            vi += means[1][j-1]*y[j-1]*S*self.D
                        elif 1 <= i < j <= n:
                            v += pair[0][i-1,j-1]*y[i-1]*y[j-1]
                            vi += pair[1][i-1,j-1]*y[i-1]*y[j-1]
                        ar[i,j], ar[j,i] = v, -v
                        ai[i,j], ai[j,i] = vi, -vi
                pr, pi = pfaffian_integer(ar, ai)
                qden = den**r*(1 << (n-int(odd)))
                err = Lip*Aerr*uerr*F(1, 1 << (n-int(odd)))
                rec = Ball(C(F(pr, qden), F(pi, qden)), err).compact(tolerance/4)
                assert rec.err <= tolerance
                row.append(rec)
                self.stats['pfaffians'] = self.stats.get('pfaffians',0)+1
            out.append(row)
        return out


# Certified rational trigonometry, adapted from accepted intervention.py.
def atan_interval(den, bits):
    x=F(1,den); power=x; total=F(0); sign=1; k=0
    tol=F(1,1 << (bits+12))
    while True:
        term=sign*power/(2*k+1); updated=total+term
        if abs(term)<tol:
            return min(total,updated),max(total,updated)
        total=updated; power*=x*x; sign=-sign; k+=1


def pi_interval(bits):
    a=atan_interval(5,bits); b=atan_interval(239,bits)
    return 16*a[0]-4*b[1],16*a[1]-4*b[0]


def cheb_nodes(N, eta):
    bits = bits_for(eta)+8
    pl, ph = pi_interval(bits+8)
    pm, pe = (pl+ph)/2, (ph-pl)/2
    ans=[]
    for j in range(N):
        fac = F(2*j+1, 2*N)
        val=exp_ball(C(0,fac*pm),eta/8)
        node = max(F(-1),min(F(1),dyad(val.mid.re,bits)))
        assert val.err+fac*pe+F(1,1 << (bits+1)) <= eta
        ans.append(node)
    return ans


def cheb_weights(nodes, per_weight_error):
    """Dyadic evaluation of (16), with its own absolute error certificate.

    A rounded three-term recurrence has error <=4^N/2^P. Rounding its finite
    weighted sum and final division gives weight error <=8*4^N/2^P.
    """
    N = len(nodes)
    P=bits_for(min(F(per_weight_error),F(1,8*N*N)))+2*N+4
    S=1 << P
    weights=[]
    for x in nodes:
        p0,p1=S,nearest_div(x.numerator*S,x.denominator)
        w=S
        for k in range(2,N):
            p0,p1=p1,nearest_div(2*x.numerator*p1,x.denominator)-p0
            if k % 2 == 0:
                w+=nearest_div(2*p1,1-k*k)
        weights.append(F(nearest_div(2*w,N),S))
    error=F(8*(1 << (2*N)),S)
    assert error <= per_weight_error
    assert sum(map(abs,weights)) <= 4
    return weights,N*error


def analytic_quad(fun, lo, hi, bound, tolerance, stats=None):
    """Integrate fun on [lo,hi], analytic and |fun|<=bound on ellipse rho=3/2.

    fun(x,delta) returns an actual calibrated Ball with error<=delta.
    The user is not allowed to supply an unevaluated external oracle here:
    the callers below construct fun from kernels/renewal and exp_fixed.
    """
    lo,hi,bound,tolerance=map(F,(lo,hi,bound,tolerance))
    h,center=(hi-lo)/2,(hi+lo)/2
    if h <= 0 or bound <= 0 or tolerance <= 0:
        raise ValueError
    M=h*bound
    p=1
    power=F(2,3)
    while 16*M*power > tolerance/4:
        p+=1; power*=F(2,3)
    N=p+1
    eta=min(F(1,4*N),tolerance/(4*(128+4*N)*M))
    nodes=cheb_nodes(N,eta)
    weights,weight_error=cheb_weights(nodes,tolerance/(64*N*M))
    sample_tol=tolerance/(32*h)
    value=C()
    sample_error=F(0)
    for x,w in zip(nodes,weights):
        rec=fun(center+h*x,sample_tol)
        if rec.err > sample_tol:
            raise ArithmeticError('uncalibrated inner evaluation')
        value += w*h*rec.mid
        sample_error += abs(w)*h*rec.err
    error=16*M*power+(128+4*N)*M*eta+M*weight_error+sample_error
    out=Ball(value,error).compact(tolerance/8)
    assert out.err <= tolerance
    if stats is not None:
        stats['quadrature_panels']=stats.get('quadrature_panels',0)+1
        stats['quadrature_nodes']=stats.get('quadrature_nodes',0)+N
        stats['max_quadrature_degree']=max(stats.get('max_quadrature_degree',0),p)
    return out


def quadrature_plan(lo, hi, bound, tolerance):
    """Same certified rule as analytic_quad, but expose rational nodes."""
    lo,hi,bound,tolerance=map(F,(lo,hi,bound,tolerance))
    h,center=(hi-lo)/2,(hi+lo)/2
    M=h*bound
    p=1; power=F(2,3)
    while 16*M*power > tolerance/4:
        p+=1; power*=F(2,3)
    N=p+1
    eta=min(F(1,4*N),tolerance/(4*(128+4*N)*M))
    nodes=cheb_nodes(N,eta); weights,weight_error=cheb_weights(nodes,tolerance/(64*N*M))
    pairs=[(center+h*x,h*w) for x,w in zip(nodes,weights)]
    return pairs,16*M*power+(128+4*N)*M*eta+M*weight_error,tolerance/(32*h),p


class KernelRay:
    """Acquire a reusable, finite *computed* complex-kernel record.

    This constructor performs all matrix exponential/Pfaffian work. It is
    not physical acquisition or a free kernel oracle. It subtracts the known
    stationary component; the latter is integrated as pi(y)/s exactly.
    """
    def __init__(self, chain, starts, ends, sigma_min, tolerance):
        self.chain=chain
        self.starts=[chain.pattern(x) for x in starts]
        self.ends=[chain.pattern(y) for y in ends]
        self.sigma_min=F(sigma_min); self.tol=F(tolerance)
        if self.sigma_min <= 0 or self.tol <= 0:
            raise ValueError
        C0=chain.C
        self.left=F(1,1 << bits_for(self.tol/(32*C0)))
        k=1
        decay=self.sigma_min+chain.g
        while 3*C0*F(1,1 << k)/decay > self.tol/16:
            k+=1
        right=self.left; panels=[]
        while right < F(k)/decay:
            panels.append((right,2*right)); right*=2
        if not panels:
            panels=[(right,2*right)]; right*=2
        self.right=right
        self.tail=3*C0*self.left+3*C0*F(1,1 << k)/decay
        self.pi=[chain.stationary(y) for y in self.ends]
        self.records=[]
        self.base_error=self.tail
        self.ptol=min(F(1),self.tol/(2048*right))
        self.etol=min(F(1),self.tol/(2048*(C0+1)*right))
        for a,b in panels:
            nodes,err,_,degree=quadrature_plan(a,b,3*C0,self.tol/(8*len(panels)))
            self.base_error+=err
            for r,w in nodes:
                vals=chain.kernels(C(r,-2*r),self.starts,self.ends,self.ptol/2)
                centered=[[Ball(v.mid-self.pi[j],v.err).compact(self.ptol/4) for j,v in enumerate(row)] for row in vals]
                self.records.append((r,w,centered))
        # Quantize quadrature weights with a separate, explicitly charged error.
        wb=bits_for(self.tol/(512*len(self.records)*(C0+1)))
        new_records=[]
        for r,w,P in self.records:
            ww=dyad(w,wb)
            self.base_error+=3*C0*abs(ww-w)
            new_records.append((r,ww,P))
        self.records=new_records
        eb=bits_for(self.tol/512)
        self.base_error=F(ceilq(self.base_error*(1 << eb)),1 << eb)
        self.weight_norm=sum(abs(w) for _,w,_ in self.records)
        self.exp_queries=0
        self.resolvent_queries=0
        self.panels=len(panels)
        assert self.base_error < self.tol/2

    def resolvent(self, s):
        s=C.make(s)
        if s.im < 0:
            vals=self.resolvent(s.conj())
            return [[Ball(v.mid.conj(),v.err) for v in row] for row in vals]
        if s.re < -s.im or s.abslo() < self.sigma_min:
            raise ValueError('outside calibrated sector/scale')
        z=C(1,-2)
        nr,nc=len(self.starts),len(self.ends)
        vals=[[self.pi[j]/s for j in range(nc)] for _ in range(nr)]
        errors=[[self.base_error for _ in range(nc)] for _ in range(nr)]
        for r,w,P in self.records:
            e=exp_ball(-s*z*r,self.etol)
            self.exp_queries+=1
            for i in range(nr):
                for j in range(nc):
                    p=P[i][j]
                    vals[i][j]+=w*z*e.mid*p.mid
                    errors[i][j]+=abs(w)*3*(e.mid.abs1()*p.err+p.mid.abs1()*e.err+e.err*p.err)
        out=[]
        for i in range(nr):
            row=[]
            for j in range(nc):
                rec=Ball(vals[i][j],errors[i][j]).compact(self.tol/8)
                assert rec.err <= self.tol
                row.append(rec)
            out.append(row)
        self.resolvent_queries+=1
        return out


def inverse_complex(A):
    """Exact rational Gauss-Jordan elimination; all pivots are checked."""
    n=len(A)
    B=[[C.make(v) for v in row]+[C(int(i==j)) for j in range(n)] for i,row in enumerate(A)]
    for k in range(n):
        j=next((j for j in range(k,n) if B[j][k].abs1()),None)
        if j is None:
            raise ArithmeticError('singular midpoint')
        B[k],B[j]=B[j],B[k]
        p=B[k][k]; B[k]=[v/p for v in B[k]]
        for i in range(n):
            if i != k:
                f=B[i][k]
                B[i]=[v-f*w for v,w in zip(B[i],B[k])]
    return [row[n:] for row in B]


def resolvent_accuracy(chain, m, s, row_tolerance):
    """A priori polynomial-digit accuracy sufficient for the renewal solve."""
    s=C.make(s)
    sigma=s.abslo()
    if sigma == 0 or s.re < -abs(s.im):
        raise ValueError
    B=8*m*chain.C*(s.abs1()+chain.G)
    H=(4*m*chain.C/sigma)*B
    return min(F(1),F(1)/(16*m*B),F(row_tolerance)/(32*m*B*(1+H)))


def renewal_from_resolvent(records):
    """Rows must be A followed by x; columns A. Return h and row-l1 error."""
    m=len(records[0])
    if len(records) != m+1:
        raise ValueError
    R=[[records[i][j].mid for j in range(m)] for i in range(m)]
    r=[v.mid for v in records[-1]]
    delta=max(v.err for row in records for v in row)
    B=inverse_complex(R)
    norm=max(sum(v.abs1() for v in row) for row in B)
    q=norm*m*delta
    if q >= 1:
        raise ArithmeticError('insufficient resolvent accuracy')
    h=[sum((r[i]*B[i][j] for i in range(m)),C()) for j in range(m)]
    row_error=m*delta*(1+sum(v.abs1() for v in h))*norm/(1-q)
    return h,row_error


def passage_transform(chain, x, targets, s, tolerance):
    x=chain.pattern(x)
    A=list(dict.fromkeys(chain.pattern(y) for y in targets))
    if not A:
        raise ValueError('nonempty explicit target list required')
    if x in A:
        return [C(int(y==x)) for y in A],F(0),None
    delta=resolvent_accuracy(chain,len(A),s,tolerance)
    bank=KernelRay(chain,A+[x],A,C.make(s).abslo(),delta)
    h,err=renewal_from_resolvent(bank.resolvent(s))
    assert err <= tolerance
    return h,err,bank


def first_passage_mean(chain, x, targets, relative=F(1,1024)):
    x=chain.pattern(x); A=list(dict.fromkeys(chain.pattern(y) for y in targets))
    if x in A:
        return {'mid':F(0),'error':F(0),'interval':['0','0']}
    if not A or not 0 < relative < 1:
        raise ValueError
    d=chain.g*sum(chain.stationary(y) for y in A)
    eps=F(relative)
    s=eps*d*d/(16*chain.C*chain.Lambda)
    tol=eps*s/(32*chain.Lambda)
    h,err,bank=passage_transform(chain,x,A,C(s),tol)
    Fmid=sum(h,C())
    center=(1-Fmid.re)/s
    evaluation=err/s
    bias=s*chain.C/(d*d)
    # True T lies in [center-evaluation,center+evaluation+bias].
    mid=center+bias/2; radius=evaluation+bias/2
    return {'mid':mid,'error':radius,'interval':reciprocal_intervals(mid,radius),
            'laplace_s':s,'killed_gap_bound':d,'row_error':err,
            'kernel_records':len(bank.records),'stats':dict(chain.stats)}


def entrance_probabilities(chain, x, targets, tolerance=F(1,1024)):
    A=list(dict.fromkeys(chain.pattern(y) for y in targets))
    if not A:
        raise ValueError
    x=chain.pattern(x)
    if x in A:
        return [Ball(int(y==x),0) for y in A]
    d=chain.g*sum(chain.stationary(y) for y in A)
    s=F(tolerance)*d/(8*chain.C)
    h,err,_=passage_transform(chain,x,A,C(s),F(tolerance)/8)
    bias=s*chain.C/d
    return [Ball(C(v.re),err+bias) for v in h]


def passage_cdf(chain, x, targets, time, tolerance=F(1,1024), progress=None):
    """Complete certified CDF at a binary-rational physical time.

    Polynomial contour quadrature + one cached complex-kernel record.
    No killed-state enumeration and no unevaluated Laplace inversion.
    """
    x=chain.pattern(x); A=list(dict.fromkeys(chain.pattern(y) for y in targets))
    time,tolerance=map(F,(time,tolerance))
    if not A or time <= 0 or not 0 < tolerance < 1:
        raise ValueError
    if x in A:
        return {'interval':['1','1'],'mid':F(1),'error':F(0)}
    C0=chain.C
    k=1
    while 2*C0*F(1,1 << k) > tolerance/128:
        k+=1
    a=F(1); panels=[]
    while a < k:
        panels.append((a,2*a)); a*=2
    trunc=2*C0*F(1,1 << int(a))
    descriptors=[('V',F(0),F(1),16*C0),('H',F(-1),F(1),16*C0)]
    descriptors += [('R',lo,hi,16*C0/lo) for lo,hi in panels]
    per=tolerance/(64*len(descriptors))
    requests=[]; base=trunc
    for kind,lo,hi,bound in descriptors:
        plan,err,sample_tol,degree=quadrature_plan(lo,hi,bound,per)
        base+=err
        for q,weight in plan:
            if kind=='V':
                w=C(1,q); dw=C(0,1)
            elif kind=='H':
                w=C(q,1); dw=C(-1)
            else:
                w=C(-q,q); dw=C(-1,1)
            ftol=sample_tol*w.abslo()/(128*(1+dw.abs1()))
            etol=sample_tol/(128*(C0+1)*(1+dw.abs1()))
            requests.append((w,dw,weight,sample_tol,ftol,etol))
    sigma_min=min((w/time).abslo() for w,*_ in requests)
    delta=min(resolvent_accuracy(chain,len(A),w/time,ftol) for w,_,_,_,ftol,_ in requests)
    bank=KernelRay(chain,A+[x],A,sigma_min,delta)
    if progress is not None:
        progress({'stage':'kernel record complete','kernel_records':len(bank.records),
                  'contour_nodes':len(requests)})
    value=C(); error=base
    for request_index,(w,dw,weight,sample_tol,ftol,etol) in enumerate(requests):
        h,herr=renewal_from_resolvent(bank.resolvent(w/time))
        assert herr <= ftol
        f=C(1)-sum(h,C())
        e=exp_ball(w,etol)
        val=dw*e.mid*f/w
        rad=dw.abs1()/w.abslo()*(e.mid.abs1()*herr+f.abs1()*e.err+e.err*herr)
        assert rad <= sample_tol
        contribution=Ball(weight*val,abs(weight)*rad).compact(tolerance/(512*len(requests)))
        value+=contribution.mid
        error+=contribution.err
        if progress is not None and (request_index+1)%25 == 0:
            progress({'stage':'contour','completed':request_index+1,'total':len(requests)})
    pl,ph=pi_interval(bits_for(tolerance)+12)
    pm=(pl+ph)/2; pr=(ph-pl)/2
    survival=value.im/pm
    radius=error/pl+abs(value.im)*pr/(pl*pm)
    mid=1-survival
    lo=max(F(0),mid-radius); hi=min(F(1),mid+radius)
    assert lo <= hi and radius <= tolerance
    return {'mid':(lo+hi)/2,'error':(hi-lo)/2,'interval':[str(lo),str(hi)],
            'kernel_records':len(bank.records),'contour_nodes':len(requests),
            'resolvent_queries':bank.resolvent_queries,'scalar_exponentials':bank.exp_queries,
            'stats':dict(chain.stats)}


def compile_cdf(chain, x, targets, tolerance=F(1,1024), progress=None):
    """Finite rational piecewise-Chebyshev enclosure of the CDF for ALL t>=0.

    This intentionally conservative implementation calls the fully constructed
    passage_cdf, charging every call. It is not claimed to be a practical
    optimized implementation. Its record size and construction bit cost are
    polynomial in complete model size and requested precision digits.
    """
    A=list(dict.fromkeys(chain.pattern(y) for y in targets))
    x=chain.pattern(x); tolerance=F(tolerance)
    if not A or not 0 < tolerance < 1:
        raise ValueError
    if x in A:
        return {'initial_target':True,'tolerance':tolerance,'panels':[]}
    d=chain.g*sum(chain.stationary(y) for y in A)
    M=chain.C+1
    left=F(1,1 << bits_for(tolerance/(32*chain.Lambda)))
    k=1
    while chain.C*F(1,1 << k) > tolerance/32:
        k+=1
    right=left
    intervals=[]
    while right < F(k)/d:
        intervals.append((right,2*right));right*=2
    p=1; power=F(2,3)
    while 8*M*power > tolerance/8:
        p+=1;power*=F(2,3)
    N=p+1
    eta=min(F(1,4*N),tolerance/(128*M*(N**3+24*N)))
    nodes=cheb_nodes(N,eta)
    delta=tolerance/(64*N)
    panels=[]
    for panel_index,(lo,hi) in enumerate(intervals):
        centers=[]
        for q in nodes:
            t=(lo+hi)/2+(hi-lo)*q/2
            rec=passage_cdf(chain,x,A,t,delta)
            assert rec['error'] <= delta
            centers.append(rec['mid'])
        coeff=[F(0) for _ in range(N)]
        for q,y in zip(nodes,centers):
            v0,v1=F(1),q
            coeff[0]+=y/N
            if N>1:
                coeff[1]+=2*y*q/N
            for j in range(2,N):
                v0,v1=v1,2*q*v1-v0
                coeff[j]+=2*y*v1/N
        cb=bits_for(tolerance/(128*N))
        coeff=[dyad(c,cb) for c in coeff]
        panels.append({'left':lo,'right':hi,'coefficients':coeff,
                       'error':tolerance})
        if progress is not None:
            progress({'panel':panel_index+1,'total':len(intervals),'degree':p})
    return {'initial_target':False,'tolerance':tolerance,'left':left,'right':right,
            'killed_gap_bound':d,'panels':panels,
            'cdf_calls':len(intervals)*N,'stats':dict(chain.stats)}


def evaluate_cdf_record(record, time):
    """Rational query to the uniform record, with its advertised error."""
    time=F(time)
    if time < 0:
        raise ValueError
    if record['initial_target']:
        return Ball(1,0)
    eps=record['tolerance']
    if time <= record['left']:
        return Ball(0,eps)
    if time >= record['right']:
        return Ball(1,eps)
    for panel in record['panels']:
        if panel['left'] <= time <= panel['right']:
            q=(2*time-panel['left']-panel['right'])/(panel['right']-panel['left'])
            c=panel['coefficients']; value=c[0]
            v0,v1=F(1),q
            if len(c)>1:
                value+=c[1]*v1
            for j in range(2,len(c)):
                v0,v1=v1,2*q*v1-v0
                value+=c[j]*v1
            return Ball(max(F(0),min(F(1),value)),eps)
    raise AssertionError('incomplete compiled record')


def reciprocal_intervals(mean_mid, mean_err):
    return [str(mean_mid-mean_err),str(mean_mid+mean_err)]


def symmetric_mean(chain, y, relative=F(1,1024)):
    """Certified mean from -y to y, using an odd-sector positive integral.

    The integrand D(t)=P_t(y,y)-P_t(-y,y) has a positive spectral measure
    of total mass one on [g,G]. Hence integral D >=1/G; no 1/pi(y)
    precision penalty is needed before the final exact rational division.
    """
    y=chain.pattern(y); relative=F(relative)
    if not 0 < relative < 1:
        raise ValueError
    eps=relative/(4*chain.G)
    left=F(1, 1 << bits_for(eps/8))
    k=1
    while F(1,1 << k)/chain.g > eps/8:
        k+=1
    right=left
    panels=[]
    while right < F(k,1)/chain.g:
        panels.append((right,2*right)); right*=2
    value=C(); error=left+F(1,1 << k)/chain.g
    for a,b in panels:
        fun=lambda v,tol: chain.kernels(C(v),[y],[y],tol,odd=True)[0][0]
        rec=analytic_quad(fun,a,b,1,eps/(2*len(panels)),chain.stats)
        value+=rec.mid; error+=rec.err
    assert error <= eps
    pi=chain.stationary(y)
    mid=value.re/pi; radius=error/pi
    return {'interval':reciprocal_intervals(mid,radius),
            'mid':mid,'error':radius,'relative_radius_bound':error*chain.G,
            'stationary_target':pi,'left_cutoff':left,'right_cutoff':right,
            'panels':len(panels),'stats':dict(chain.stats)}
