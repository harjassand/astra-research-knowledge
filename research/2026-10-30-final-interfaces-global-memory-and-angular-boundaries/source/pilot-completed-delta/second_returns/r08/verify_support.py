"""Exact SOS support replay: polynomial identity and rational interval LDL.

No numerical solver or network is used. The root interval and all
arithmetic bounds are rational. Rounding is always outward to 256 bits.
"""
from pathlib import Path
from fractions import Fraction as Q
from dataclasses import dataclass
import json,time
import sympy as s

OUT=Path(__file__).resolve().parent
CASE=OUT.parents[2]/'cases'/'angular'
BITS=256;SCALE=1<<BITS
def down(v):return Q((v.numerator*SCALE)//v.denominator,SCALE)
def up(v):return Q(-((-v.numerator*SCALE)//v.denominator),SCALE)
@dataclass(frozen=True)
class I:
    lo:Q
    hi:Q
    def __init__(self,lo,hi=None):
        object.__setattr__(self,'lo',Q(lo));object.__setattr__(self,'hi',Q(lo if hi is None else hi))
        assert self.lo<=self.hi
    def __add__(self,v):
        if not isinstance(v,I):v=I(v)
        return I(down(self.lo+v.lo),up(self.hi+v.hi))
    __radd__=__add__
    def __neg__(self):return I(-self.hi,-self.lo)
    def __sub__(self,v):return self+-asI(v)
    def __rsub__(self,v):return asI(v)+-self
    def __mul__(self,v):
        v=asI(v);ends=[self.lo*v.lo,self.lo*v.hi,self.hi*v.lo,self.hi*v.hi]
        return I(down(min(ends)),up(max(ends)))
    __rmul__=__mul__
    def __truediv__(self,v):
        v=asI(v);assert not v.lo<=0<=v.hi
        return self*I(down(min(1/v.lo,1/v.hi)),up(max(1/v.lo,1/v.hi)))
    def __rtruediv__(self,v):return asI(v)/self
    def __pow__(self,n):
        assert isinstance(n,int) and n>=0
        ans=I(1)
        for _ in range(n):ans=ans*self
        return ans
def asI(v):return v if isinstance(v,I) else I(v)
def fq(v):return Q(int(s.numer(v)),int(s.denom(v)))

def polynomial_interval(expr,var,box):
    ans=I(0)
    for co in s.Poly(expr,var).all_coeffs():ans=ans*box+fq(co)
    return ans

def interval_ldl(matrix):
    n=len(matrix);lower=[[I(0) for _ in range(n)] for _ in range(n)];diag=[]
    for i in range(n):
        dd=matrix[i][i]-sum((lower[i][k]*lower[i][k]*diag[k] for k in range(i)),I(0))
        assert dd.lo>0,('nonpositive interval pivot',i,dd)
        diag.append(dd);lower[i][i]=I(1)
        for j in range(i+1,n):
            lower[j][i]=(matrix[j][i]-sum((lower[j][k]*lower[i][k]*diag[k]
                                          for k in range(i)),I(0)))/dd
    return diag

def main():
    started=time.perf_counter();raw=json.loads((OUT/'support_gram.json').read_text())
    a,b,c,d,t,z,v1,v2,v3=s.symbols('a b c d t z v1 v2 v3')
    av=(a,b,c,d);vv=(z,v1,v2,v3)
    mod=s.Poly(s.sympify(raw['modulus'],locals={'t':t}),t)
    def rem(v):return s.rem(s.expand(v),mod.as_expr(),t)
    def parse(v):return s.sympify(v,locals={'t':t})
    K=s.Matrix(list(map(parse,raw['base_K'])))
    R=s.Matrix([1,t,0,0]);H=s.Matrix([z,t*z+v1,v2,v3])
    seed=json.loads((CASE/'seed_299_301.json').read_text())
    beta=s.Rational(seed['beta']);r=s.Rational(seed['r'])
    T=sum(w*w for w in av);q=a*d-b*c;X=a*a+c*c-b*b-d*d
    F=T*T+4*(r-1)*q*q+4*beta*q*X
    HK=s.hessian(F,av).subs(dict(zip(av,K)),simultaneous=True)
    support=parse(raw['support_det_coefficient'])
    assert rem(support-(HK*R)[3])==0
    P=(HK-support*s.hessian(q,av)).applyfunc(rem)
    assert all(rem(v)==0 for v in P*R)
    FH=F.subs(dict(zip(av,H)),simultaneous=True)
    cubic=sum(s.diff(F,w).subs(dict(zip(av,H)),simultaneous=True)*kk for w,kk in zip(av,K))
    J=(H.T*HK*H)[0]/2+cubic+FH-support*q.subs(dict(zip(av,H)),simultaneous=True)
    margin=s.Rational(raw['margin'])
    G=s.zeros(13)
    for i,j,co in raw['gram_entries']:G[i,j]=G[j,i]=parse(co)
    features=s.Matrix([s.prod(w**e for w,e in zip(vv,pw)) for pw in raw['feature_powers']])
    difference=s.Poly(s.expand(J-margin*(H.dot(H))**2-(features.T*G*features)[0]),*vv)
    assert all(rem(co)==0 for co in difference.coeffs())
    print('Exact quartic support/SOS identity checked from the literal seed.',flush=True)
    # There is exactly one root in (17/100,19/100). Enclose it by signs.
    lo=Q(17,100);hi=Q(19,100)
    assert mod.count_roots(s.Rational(lo.numerator,lo.denominator),s.Rational(hi.numerator,hi.denominator))==1
    def value(v):
        ans=Q(0)
        for co in mod.all_coeffs():ans=ans*v+fq(co)
        return ans
    assert value(lo)>0 and value(hi)<0
    for _ in range(300):
        mid=(lo+hi)/2
        if value(mid)>0:lo=mid
        else:hi=mid
    box=I(lo,hi)
    matrix=[[polynomial_interval(G[i,j],t,box) for j in range(13)] for i in range(13)]
    pivots=interval_ldl(matrix)
    certificate={'root_polynomial':str(mod.as_expr()),
        'root_interval':[str(lo),str(hi)],'outward_dyadic_bits':BITS,
        'gram_dimension':13,'positive_LDL_pivot_bounds':[str(p.lo) for p in pivots],
        'margin':str(margin),'polynomial_identity_exact':True,
        'positive_definiteness_exact':True,
        'inequality':'F(K+H)-F(K)-DF(K):H-support*det(H) >= (1/64)*|H|^4 for all real H',
        'seconds':time.perf_counter()-started}
    (OUT/'support_certificate.json').write_text(json.dumps(certificate,indent=2)+'\n')
    print(json.dumps({'identity_exact':True,'interval_LDL_all_pivots_positive':True,
                      'minimum_pivot_lower_bound':float(min(p.lo for p in pivots)),
                      'margin':str(margin),'seconds':certificate['seconds']},indent=2),flush=True)

if __name__=='__main__':main()
