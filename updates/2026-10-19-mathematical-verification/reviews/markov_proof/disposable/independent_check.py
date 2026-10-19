"""Independent exact/safely rounded audit. No source audit code is imported.

SymPy certifies algebraic identities. mpmath only proposes a root bracket and
performs a secondary numerical check; all stated enclosures are verified with
outward-rounded integer interval arithmetic and explicit series remainders.
"""
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
import json
import sys
import sympy as sp
import mpmath as mp

HERE = Path(__file__).resolve().parent
SCALE = 10**90

def ceildiv(n, d):
    return -((-n)//d)

class IV:
    def __init__(self, lo, hi=None):
        self.lo, self.hi = int(lo), int(lo if hi is None else hi)
        assert self.lo <= self.hi
    @classmethod
    def bounds(cls, lo, hi):
        lo, hi = F(lo), F(hi)
        return cls((lo.numerator*SCALE)//lo.denominator,
                   ceildiv(hi.numerator*SCALE, hi.denominator))
    @classmethod
    def exact(cls, value):
        return cls.bounds(F(value), F(value))
    def __add__(self, other):
        other = asiv(other)
        return IV(self.lo+other.lo, self.hi+other.hi)
    __radd__ = __add__
    def __neg__(self):
        return IV(-self.hi, -self.lo)
    def __sub__(self, other):
        return self + (-asiv(other))
    def __rsub__(self, other):
        return asiv(other) + (-self)
    def __mul__(self, other):
        other = asiv(other)
        ps = [a*b for a in (self.lo,self.hi) for b in (other.lo,other.hi)]
        return IV(min(ps)//SCALE, ceildiv(max(ps),SCALE))
    __rmul__ = __mul__
    def __truediv__(self, other):
        other = asiv(other)
        assert other.lo > 0 or other.hi < 0, "division interval contains zero"
        fs = [(a*SCALE)//b for a in (self.lo,self.hi) for b in (other.lo,other.hi)]
        cs = [ceildiv(a*SCALE,b) for a in (self.lo,self.hi) for b in (other.lo,other.hi)]
        return IV(min(fs),max(cs))
    def __rtruediv__(self, other):
        return asiv(other)/self
    def sqrt(self):
        assert self.lo >= 0
        low = isqrt(self.lo*SCALE)
        high = isqrt(self.hi*SCALE)
        if high*high != self.hi*SCALE:
            high += 1
        return IV(low,high)
    def log(self):
        assert self.lo > 0
        return IV(log_point(self.lo).lo,log_point(self.hi).hi)
    def strings(self):
        return [decimal(self.lo),decimal(self.hi)]

def asiv(x):
    return x if isinstance(x,IV) else IV.exact(x)

def decimal(n):
    sign = '-' if n < 0 else ''
    n = abs(n)
    return f'{sign}{n//SCALE}.{n%SCALE:090d}'

def atanh_series_fraction(z, n):
    # 2 atanh(z) for 0 <= z < 1; positive omitted tail bounded geometrically.
    total = sum((z**(2*k+1)/F(2*k+1) for k in range(n)),F(0)) * 2
    tail = 2*z**(2*n+1)/(F(2*n+1)*(1-z*z))
    return total,total+tail

LOG2 = IV.bounds(*atanh_series_fraction(F(1,3),120))

def atan_inverse_fraction(d,n=100):
    z=F(1,d)
    total=sum(((-1)**k*z**(2*k+1)/F(2*k+1) for k in range(n)),F(0))
    next_term=(-1)**n*z**(2*n+1)/F(2*n+1)
    return IV.bounds(min(total,total+next_term),max(total,total+next_term))

PI=16*atan_inverse_fraction(5)-4*atan_inverse_fraction(239)

def log_point(n):
    x=F(n,SCALE)
    m=0
    while x>=2:
        x/=2
        m+=1
    while x<1:
        x*=2
        m-=1
    z=IV.exact((x-1)/(x+1))
    zz=z*z
    power=z
    total=IV.exact(0)
    terms=120
    for k in range(terms):
        total+=power/(2*k+1)
        power*=zz
    # All omitted terms are positive. Since 1 <= x < 2, z <= 1/3.
    tail=2*power/((2*terms+1)*(1-zz))
    series=2*total
    return IV(series.lo,series.hi+tail.hi)+m*LOG2

def interval_values(A):
    b=18*LOG2
    omega=2*PI
    s=(2*(A*A+omega*omega)).sqrt()
    c1=b-A
    c2=b+3*A
    ell1=((c1+s)/(c1-s)).log()
    ell2=((c2+2*s)/(c2-2*s)).log()
    val=s*(2*ell1+ell2)/4
    sprime=2*A/s
    derivative=sprime*(2*ell1+ell2)/4+s*((c1*sprime+s)/(c1*c1-s*s)+(c2*sprime-3*s)/(c2*c2-4*s*s))
    return val,derivative

def exact_algebra():
    a,b,t,A,B,C,omega=sp.symbols('a b t A B C omega',real=True)
    one=sp.ones(4,1)
    v=sp.Matrix([1,-1,0,0])/sp.sqrt(2)
    u=sp.Matrix([1,1,-1,-1])/2
    w=sp.Matrix([0,0,1,-1])/sp.sqrt(2)
    H=sp.Matrix.hstack(one/2,v,u,w)
    Pi=one*one.T/4
    assert H.T*H==sp.eye(4)
    L=-a*v*v.T-b*(u*u.T+w*w.T)
    Q=L+A*(u*u.T-w*w.T)+B*u*w.T+C*w*u.T
    block=sp.simplify(H.T*Q*H)
    target=sp.Matrix([[0,0,0,0],[0,-a,0,0],[0,0,-b+A,B],[0,0,C,-b-A]])
    assert sp.simplify(block-target)==sp.zeros(4)
    assert Q*one==sp.zeros(4,1) and sp.simplify(one.T*Q)==sp.zeros(1,4)
    R=sp.Matrix([[A,B],[C,-A]])
    assert sp.simplify((R*R).subs(B*C,-A*A-omega*omega)+omega*omega*sp.eye(2))==sp.zeros(2)
    P=sp.Matrix([[264193,260097,262143,262143],
                 [260097,264193,262143,262143],
                 [262143,262143,262147,262143],
                 [262143,262143,262143,262147]])/1048576
    spectral=Pi+sp.Rational(1,256)*v*v.T+sp.Rational(1,262144)*(u*u.T+w*w.T)
    assert P==spectral
    assert H.T*P*H==sp.diag(1,sp.Rational(1,256),sp.Rational(1,262144),sp.Rational(1,262144))
    Q0=sp.Matrix([[-2*a-b+t,2*a-b+t,b+3*t,b-5*t],
                  [2*a-b+t,-2*a-b+t,b+3*t,b-5*t],
                  [b-5*t,b-5*t,-3*b-t,b+11*t],
                  [b+3*t,b+3*t,b-5*t,-3*b-t]])/4
    assert sp.simplify(Q0-Q.subs({A:t,B:2*sp.sqrt(2)*t,C:-2*sp.sqrt(2)*t}))==sp.zeros(4)
    M=sp.simplify(H.T*Q0*H)
    R0=M[2:4,2:4]+b*sp.eye(2)
    assert sp.simplify(R0*R0+7*t*t*sp.eye(2))==sp.zeros(2)
    assert sp.simplify((R0*R0).subs(t,2*sp.pi/sp.sqrt(7))+4*sp.pi**2*sp.eye(2))==sp.zeros(2)
    assert sp.simplify(Q0*one)==sp.zeros(4,1) and sp.simplify(one.T*Q0)==sp.zeros(1,4)
    z=sp.symbols('z',positive=True)
    f=z*sp.log((1+z)/(1-z))
    assert sp.simplify(sp.diff(f,z,2)-4/(1-z*z)**2)==0
    return {'orthonormal_basis':True,'full_logarithm_block':True,'row_and_column_sums_zero':True,
            'rational_P_spectral_identity':True,'Q0_exact_outer_product_identity':True,
            'Q0_rotation_block_square_minus_4pi2':True,
            'exact_exponential_conclusion':'exp(Q0)=Pi+2^-8 vv^T+2^-18(uu^T+ww^T)=P, using exp(R0)=I',
            'convex_perspective_second_derivative':True,
            'Q0_spectral_block':str(M)}

mp.mp.dps=90
bmp=18*mp.log(2)
wmp=2*mp.pi
def fmp(A):
    s=mp.sqrt(2)*mp.sqrt(A*A+wmp*wmp)
    return s/4*(2*mp.log((bmp-A+s)/(bmp-A-s))+mp.log((bmp+3*A+2*s)/(bmp+3*A-2*s)))
def dfmp(A):
    return mp.diff(fmp,A)
root=mp.findroot(dfmp,(mp.mpf('2.2'),mp.mpf('2.4')))
den=10**40
num=int(mp.floor(root*den))
rootlo,roothi=F(num,den),F(num+1,den)
flo,dlo=interval_values(IV.exact(rootlo))
fhi,dhi=interval_values(IV.exact(roothi))
assert dlo.hi<0, dlo.strings()
assert dhi.lo>0, dhi.strings()
froot,_=interval_values(IV.bounds(rootlo,roothi))
assert F(froot.lo,SCALE)>F('26.178911678346')
assert F(froot.hi,SCALE)<F('26.178911678347')
assert rootlo>F('2.2905478380320084')
assert roothi<F('2.2905478380320091')
rootiv=IV.bounds(rootlo,roothi)
biv=18*LOG2
omegaiv=2*PI
root_s=(2*(rootiv*rootiv+omegaiv*omegaiv)).sqrt()
root_margins={'A_minus_b_plus_2a':rootiv-2*LOG2,
              'b_minus_A_minus_s':biv-rootiv-root_s,
              'b_plus_3A_minus_2s':biv+3*rootiv-2*root_s,
              'b_minus_first_winding_threshold':biv-5*omegaiv/IV.exact(7).sqrt(),
              'second_winding_threshold_minus_b':10*omegaiv/IV.exact(7).sqrt()-biv}
assert all(x.lo>0 for x in root_margins.values())

# Independent direct six-pair evaluation tests the entropy normalization.
vmp=mp.matrix([1,-1,0,0])/mp.sqrt(2)
ump=mp.matrix([1,1,-1,-1])/2
wvecmp=mp.matrix([0,0,1,-1])/mp.sqrt(2)
amp=8*mp.log(2)
rmp=mp.sqrt(root*root+wmp*wmp)
Qmp=-amp*(vmp*vmp.T)-bmp*(ump*ump.T+wvecmp*wvecmp.T)+root*(ump*ump.T-wvecmp*wvecmp.T)+rmp*(ump*wvecmp.T-wvecmp*ump.T)
direct=sum((Qmp[i,j]-Qmp[j,i])/4*mp.log(Qmp[i,j]/Qmp[j,i]) for i in range(4) for j in range(i+1,4))
tiv=2*PI/IV.exact(7).sqrt()
positivity1=18*LOG2-5*tiv
positivity2=tiv-2*LOG2
assert positivity1.lo>0 and positivity2.lo>0
data={'method':'Independent SymPy exact spectral identities plus 90-place outward-rounded integer interval arithmetic; no source checker read or run',
      'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__,'mpmath':mp.__version__},
      'algebra':exact_algebra(),
      'constant_intervals':{'pi':PI.strings(),'log2':LOG2.strings()},
      'root_interval':IV.bounds(rootlo,roothi).strings(),
      'derivative_at_lower':dlo.strings(),'derivative_at_upper':dhi.strings(),
      'entropy_interval':froot.strings(),
      'source_12_digit_entropy_enclosure_independently_verified':True,
      'root_and_winding_feasibility_margins':{k:v.strings() for k,v in root_margins.items()},
      'Q0_strict_positivity_margins':{'b_minus_5t':positivity1.strings(),'t_minus_2log2':positivity2.strings()},
      'secondary_mpmath':{'root':mp.nstr(root,85),'entropy':mp.nstr(fmp(root),85),
                         'direct_pairwise_entropy':mp.nstr(direct,85),
                         'pairwise_vs_scalar_abs_difference':mp.nstr(abs(direct-fmp(root)),8)},
      'proof_dependency':'Root uniqueness and attainment use the analytic strict-convexity proof; root existence is certified by the derivative signs.'}
(HERE/'independent_certificate.json').write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps(data,indent=2))
