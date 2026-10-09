"""Exact rational interval audit; display rounding is not used for assertions."""
from fractions import Fraction as F
from decimal import Decimal, localcontext
import json

class I:
    def __init__(self, lo, hi=None):
        self.lo, self.hi = F(lo), F(lo if hi is None else hi)
        assert self.lo <= self.hi
    def __add__(self, x):
        x = x if isinstance(x, I) else I(x)
        return I(self.lo+x.lo, self.hi+x.hi)
    __radd__ = __add__
    def __neg__(self): return I(-self.hi, -self.lo)
    def __sub__(self, x): return self + (-x if isinstance(x, I) else -I(x))
    def __rsub__(self, x): return I(x)+(-self)
    def __mul__(self, x):
        x = x if isinstance(x, I) else I(x)
        p = [self.lo*x.lo, self.lo*x.hi, self.hi*x.lo, self.hi*x.hi]
        return I(min(p), max(p))
    __rmul__ = __mul__
    def __truediv__(self, x):
        x = x if isinstance(x, I) else I(x)
        assert x.lo*x.hi > 0
        return self*I(1/x.hi, 1/x.lo)
    def display(self):
        with localcontext() as c:
            c.prec=28
            return [str(Decimal(x.numerator)/Decimal(x.denominator)) for x in (self.lo,self.hi)]

def log_reduced(y):
    assert 1 <= y <= 2
    z=(y-1)/(y+1)
    low=2*sum((z**(2*j+1)/F(2*j+1) for j in range(50)),F(0))
    tail=2*z**101/(101*(1-z*z))
    return I(low,low+tail)

LN2=log_reduced(F(2))
def ln(x):
    x=F(x)
    assert x>0
    k=0
    while x>2: x/=2; k+=1
    while x<1: x*=2; k-=1
    return k*LN2+log_reduced(x)

q=1024
alpha,beta,s=F(34),F(4053,100),F(31)
lnq=10*LN2
def logq(x): return ln(x)/lnq
def entropy(x,y): return ((x+y)*ln(x+y)-x*ln(x)-y*ln(y))/lnq
ell=logq(F(1023,1024))
rho_minus=entropy(beta,s)+alpha+62*ell-2
rho_plus=alpha-1+31*ell+entropy(beta,s)
a_star=(alpha+beta-1)*I(1)/rho_minus
b_star=1+(I(F(1,330))+entropy(2*beta,s)-entropy(beta,s)+alpha+31*ell-1)/rho_minus

checks={
    "a_star_lt_1_889":a_star.hi<F(1889,1000),
    "b_star_lt_1_909":b_star.hi<F(1909,1000),
    "three_rho_plus_lt_121":(3*rho_plus).hi<121,
    "rho_minus_over_242_gt_0_16":(rho_minus/242).lo>F(4,25),
    "rho_plus_over_242_lt_0_17":(rho_plus/242).hi<F(17,100),
    "d_rate_lt_85":alpha+beta<85,
    "balanced_bad_exponent_lt_2_rho_minus":(3*rho_plus-F(85,2)-2*rho_minus).hi<0,
    "balanced_rho_minus_over_85_gt_0_459":(rho_minus/85).lo>F(459,1000),
    "balanced_rho_plus_over_85_lt_0_472":(rho_plus/85).hi<F(472,1000),
}
assert all(checks.values()),checks
values={"rho_minus":rho_minus,"rho_plus":rho_plus,"a_star":a_star,"b_star":b_star,
        "constant_cap_bad_rate":3*rho_plus-121,
        "constant_cap_density_lower":rho_minus/242,"constant_cap_density_upper":rho_plus/242,
        "balanced_bad_minus_2size_rate":3*rho_plus-F(85,2)-2*rho_minus}
print(json.dumps({"method":"Fraction interval arithmetic; 50-term positive atanh series with geometric tail",
                  "checks":checks,"intervals":{k:v.display() for k,v in values.items()}},indent=2))
