"""Exact integer/dyadic interval certificates for the charged-compliance designs.

Only Python standard library. Every arithmetic operation rounds outwards to
2^-256. exp uses a positive Taylor sum plus an explicit geometric tail;
pi uses Machin's formula and alternating atan tails. No numerical library,
frequency grid, machine float, or uncharged omitted optical band is used.
"""
from fractions import Fraction
from math import isqrt
from pathlib import Path

BITS=256
D=1<<BITS

def ceildiv(n,d): return -((-n)//d)

class I:
    __slots__=('lo','hi')
    def __init__(self,x=0,y=None,raw=False):
        if raw: self.lo,self.hi=x,y;return
        if isinstance(x,I):self.lo,self.hi=x.lo,x.hi;return
        q=Fraction(x); self.lo=q.numerator*D//q.denominator
        q=Fraction(x if y is None else y);self.hi=ceildiv(q.numerator*D,q.denominator)
        assert self.lo<=self.hi
    def __add__(self,o):
        o=I(o);return I(self.lo+o.lo,self.hi+o.hi,raw=True)
    __radd__=__add__
    def __neg__(self):return I(-self.hi,-self.lo,raw=True)
    def __sub__(self,o):return self+-I(o)
    def __rsub__(self,o):return I(o)+-self
    def __mul__(self,o):
        o=I(o);v=[a*b for a in (self.lo,self.hi) for b in (o.lo,o.hi)]
        return I(min(v)//D,ceildiv(max(v),D),raw=True)
    __rmul__=__mul__
    def inv(self):
        assert not self.lo<=0<=self.hi,(self.lo,self.hi)
        return I(D*D//self.hi,ceildiv(D*D,self.lo),raw=True)
    def __truediv__(self,o):return self*I(o).inv()
    def __rtruediv__(self,o):return I(o)*self.inv()
    def __pow__(self,n):
        assert isinstance(n,int) and n>=0
        ans=I(1);a=self
        while n:
            if n&1:ans=ans*a
            a=a*a;n//=2
        return ans
    def sqrt(self):
        assert self.lo>=0
        return I(isqrt(self.lo*D),isqrt(self.hi*D)+1,raw=True)
    def pos(self):return self.lo>0
    def neg(self):return self.hi<0
    def fmt(self,digits=24):
        def dec(n,up):
            scale=10**digits
            v=ceildiv(n*scale,D) if up else n*scale//D
            sg='-' if v<0 else '';v=abs(v)
            return sg+str(v//scale)+'.'+str(v%scale).zfill(digits)
        return '['+dec(self.lo,False)+', '+dec(self.hi,True)+']'

def exp(x,N=256):
    x=I(x);assert x.lo>=0
    term=I(1);ans=I(1)
    for n in range(1,N+1):
        term=term*x/n;ans+=term
    nxt=term*x/(N+1)
    rat=x/(N+2);assert rat.hi<D
    tail=nxt/(1-rat)
    # The true infinite tail is nonnegative and at most this upper bound.
    return I(ans.lo,ans.hi+tail.hi,raw=True)

def sinh(x):
    ex=exp(x)
    return (ex-1/ex)/2

def bose(x):
    x=I(x)
    if x.lo==x.hi==0:return I(1)
    return (x/sinh(x))**2

def atan(q,N=80):
    q=I(q);q2=q*q;t=q;ans=I(0)
    for n in range(N):
        ans+=t/(2*n+1) if n%2==0 else -t/(2*n+1)
        t=t*q2
    remainder=t/(2*N+1)
    assert N%2==0
    return I(ans.lo,ans.hi+remainder.hi,raw=True)

PI=16*atan(Fraction(1,5))-4*atan(Fraction(1,239))
JINF=PI*PI/6

def tail(x,N=100):
    x=I(x);z=1/exp(2*x);zz=z;ans=I(0)
    for n in range(1,N+1):
        ans+=zz*(2*x*x+2*x/n+Fraction(1,n*n))
        zz=zz*z
    rem=zz*(2*x*x+2*x/(N+1)+Fraction(1,(N+1)**2))/(1-z)
    return I(ans.lo,ans.hi+rem.hi,raw=True)

def band(a,b):
    a=I(a);b=I(b)
    return (JINF if a.lo==a.hi==0 else tail(a))-tail(b)

def endpoints(t,A=4,B=2):
    t=I(t);A=I(A);B=I(B)
    dd=((t+A)**2-4*B*t).sqrt()
    s2=(t+A+dd)/2;p2=B*t/s2
    return p2.sqrt(),t.sqrt(),s2.sqrt()

def dual(p,r,s):
    z=[w*w for w in [p,r,s]]
    h=[w**3*bose(w) for w in [p,r,s]]
    d1=(h[1]-h[0])/(z[1]-z[0]);d12=(h[2]-h[1])/(z[2]-z[1])
    d2=(d12-d1)/(z[2]-z[0])
    a=-d2;la=-d1+d2*(z[0]+z[1]);nu=-h[0]+d1*z[0]-d2*z[0]*z[1]
    return la,a,nu

def conductance(ends):
    p,r,s=ends
    return band(0,p)+band(r,s)


def all_checks():
    lines=['# Reproducible exact interval certificate',
           '',f'Precision: {BITS} binary fractional bits. Bounds below are rounded outward.',
           'All assertions are exact integer inequalities; full Bose tails are included.','']
    def show(name,x):lines.append(name+' = '+I(x).fmt())
    # Target point: exact algebraic endpoints.
    rt=I(8).sqrt();p=I(5).sqrt()-1;s=I(5).sqrt()+1
    la,a,nu=dual(p,rt,s)
    assert la.neg() and a.pos() and nu.neg()
    jt=conductance((p,rt,s));jr=band(0,I(2).sqrt())
    lines+=['## Requested cap C=1/4: exact two-unit-mass k=4 pendant','']
    for n,x in [('p',p),('r',rt),('s',s),('lambda',la),('a=2mu',a),('nu',nu),('J_target',jt),('J_rigid',jr),('J_target/J_rigid',jt/jr)]:show(n,x)
    # A certified mu=0 crossing for fixed A=4.
    rlo=I('5.28683321830262');rhi=I('5.28683321830264')
    dl=dual(*endpoints(rlo*rlo));dh=dual(*endpoints(rhi*rhi))
    assert dl[1].pos() and dh[1].neg()
    rbox=I('5.28683321830262','5.28683321830264')
    lb,ab,nb=dual(*endpoints(rbox*rbox))
    assert lb.pos() and nb.neg()
    lines+=['','## Certified fixed-trace a=0 crossing (existence; no global uniqueness assertion)','']
    for n,x in [('r_crossing',rbox),('C_crossing',2/(rbox*rbox)),('a_at_lower_r',dl[1]),('a_at_upper_r',dh[1]),('lambda_on_bracket',lb),('nu_on_bracket',nb)]:show(n,x)
    # Severe-cap exact infimum: A=2+C*r^2 and a=0 by IVT.
    C=Fraction(1,20)
    lo='5.28796811028488';hi='5.28796811028490'
    xl=I(lo);xh=I(hi)
    al=2+C*xl*xl;ah=2+C*xh*xh
    dlow=dual(*endpoints(xl*xl,al));dhigh=dual(*endpoints(xh*xh,ah))
    assert dlow[1].pos() and dhigh[1].neg()
    xb=I(lo,hi);Ab=2+C*xb*xb
    el= endpoints(xb*xb,Ab);dlim=dual(*el)
    assert dlim[0].pos() and dlim[2].neg() and (4-Ab).pos()
    jlim=conductance(el)
    jp=conductance(endpoints(40))
    lines+=['','## Severe cap C=1/20: exact a=0 limiting spectrum','']
    for n,x in [('r_infimum',xb),('A_infimum',Ab),('a_at_lower_r',dlow[1]),('a_at_upper_r',dhigh[1]),('lambda_on_bracket',dlim[0]),('nu_on_bracket',dlim[2]),('J_infimum',jlim),('J_optimized_pendant_k20',jp),('pendant_minus_infimum',jp-jlim)]:show(n,x)
    assert (jp-jlim).pos()
    # Exact finite three-band construction: rational low trace and high band.
    Al=Fraction(17,5);delta=Fraction(3,5);H=Fraction(400)
    Bl=Fraction(2)*H/(H+delta)
    target=Fraction(1,2)+C/2
    tt=(Al-Bl)/(Bl*(target-1/Bl+delta/(H*(H+delta))))
    ef=endpoints(tt,Al,Bl);pend=endpoints(40)
    assert (I(H)-ef[2]*ef[2]).pos()
    Htop=I(H+delta).sqrt();jf=conductance(ef)+band(I(H).sqrt(),Htop)
    assert (jp-jf).pos() and (jf-jlim).pos()
    # Exact q coefficients; q(z)=(z^2+c*z+d)/(z*(z+t)*(z+H)).
    cc=(Bl*tt+(tt+Al)*(H+delta)-tt*H)/4
    dd=Bl*tt*(H+delta)/4
    ds=(I(cc*cc-4*dd)).sqrt()
    sig1=(I(cc)-ds)/2;sig2=(I(cc)+ds)/2
    kap=tt+H-cc
    rho1=(tt*H-dd-kap*sig1)/(sig2-sig1);rho2=kap-rho1
    mass1=rho1/sig1;mass2=rho2/sig2
    assert sig1.pos() and sig2.pos() and rho1.pos() and rho2.pos()
    # Exact resource identities, independently from intervals.
    assert Al+delta==4
    assert Bl*(H+delta)/H==2
    assert 1/Bl+(Al-Bl)/(Bl*tt)-delta/(H*(H+delta))==target
    assert tt*H/dd==2
    lines+=['','## Actual finite three-band positive star at C=1/20','',
           'Exact rational parameters:',f'A_low = {Al}',f'B_low = {Bl}',f'r_low^2 = {tt}',f'H = {H}',f'delta = {delta}',f'q_numerator_c = {cc}',f'q_numerator_d = {dd}',f'total_internal_spring_sum = {kap}','']
    for n,x in [('p_low',ef[0]),('r_low',ef[1]),('s_low',ef[2]),('high_band_start',I(H).sqrt()),('high_band_end',Htop),('branch_sigma_1',sig1),('branch_sigma_2',sig2),('branch_spring_1',rho1),('branch_spring_2',rho2),('branch_mass_1',mass1),('branch_mass_2',mass2),('total_mass',1+mass1+mass2),('C_CM',C),('J_finite_3band',jf),('optimized_pendant_minus_3band',jp-jf),('3band_minus_infimum',jf-jlim),('relative_gain_over_pendant',(jp-jf)/jp)]:show(n,x)
    # A strict improvement under a spring-sum cap only .1 percent above its
    # physical feasibility minimum. The one-pendant comparator remains k=20.
    delta=Fraction(1,100);H=Fraction(64);Al=4-delta
    Bl=2*H/(H+delta)
    tt=(Al-Bl)/(Bl*(target-1/Bl+delta/(H*(H+delta))))
    ee=endpoints(tt,Al,Bl)
    assert (I(H)-ee[2]*ee[2]).pos()
    cc=(Bl*tt+(tt+Al)*(H+delta)-tt*H)/4;dd=Bl*tt*(H+delta)/4
    kap=tt+H-cc
    assert kap < Fraction(1001,50) # 20.02, charged to both competitors
    disc=I(cc*cc-4*dd).sqrt();sg1=(I(cc)-disc)/2;sg2=(I(cc)+disc)/2
    kk1=(tt*H-dd-kap*sg1)/(sg2-sg1);kk2=kap-kk1
    mm1=kk1/sg1;mm2=kk2/sg2
    assert all(v.pos() for v in [sg1,sg2,kk1,kk2,mm1,mm2])
    jj=conductance(ee)+band(I(H).sqrt(),I(H+delta).sqrt())
    assert (jp-jj).pos()
    lp,ap,np=dual(*pend)
    R8=bose(I(8))+lp/8+ap*8+np/(8**3)
    assert R8.neg()
    kp=(I(H)-40)*(I(H)-pend[0]**2)*(I(H)-pend[2]**2)/(4*H*H)
    assert kp.pos()
    assert Al+delta==4 and Bl*(H+delta)/H==2
    assert 1/Bl+(Al-Bl)/(Bl*tt)-delta/(H*(H+delta))==target
    lines+=['','## Finite extra mode with C=1/20 and total spring sum <20.02','',
            f'A_low = {Al}',f'delta = {delta}',f'H = {H}',f'B_low = {Bl}',
            f'r_low^2 = {tt}',f'total_internal_spring_sum = {kap}',
            f'q_numerator_c = {cc}',f'q_numerator_d = {dd}','']
    for n,x in [('p_low',ee[0]),('r_low',ee[1]),('s_low',ee[2]),
                ('high_band_start',I(H).sqrt()),('high_band_end',I(H+delta).sqrt()),
                ('branch_mass_1',mm1),('branch_mass_2',mm2),
                ('branch_spring_1',kk1),('branch_spring_2',kk2),
                ('spring_sum',kap),('J_finite_small_overhead',jj),
                ('pendant_minus_small_overhead',jp-jj),
                ('pendant_R_at_w8',R8),('dJ_ddelta_at_zero',R8/16),
                ('dkappa_ddelta_at_zero',kp)]:show(n,x)
    lines+=['','PASS: exact signs, positive finite parts, all full-spectrum Bose integrals,',
            'exact trace/log/compliance resources, and a strict three-band improvement.','']
    return '\n'.join(lines)

if __name__=='__main__':
    out=all_checks()
    Path(__file__).with_name('CERTIFICATE.md').write_text(out)
    print(out)
