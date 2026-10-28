"""Rational Bessel tails and outward Decimal kernels for a nonlinear continuum channel.
No external packages, Fock cutoffs, frequency quadrature, or Gram inversions.
The model is two specified kicks, not the P2 waveform or component circuit.
"""
from decimal import Decimal, Context, ROUND_FLOOR, ROUND_CEILING, ROUND_HALF_EVEN
from fractions import Fraction as F
from functools import lru_cache
from math import factorial
from pathlib import Path
import json, time, hashlib

PREC = 48
LOW=Context(prec=PREC,rounding=ROUND_FLOOR,Emin=-999999,Emax=999999)
HIGH=Context(prec=PREC,rounding=ROUND_CEILING,Emin=-999999,Emax=999999)
NEAR=Context(prec=PREC,rounding=ROUND_HALF_EVEN,Emin=-999999,Emax=999999)
class I:
    __slots__=('lo','hi')
    def __init__(self,lo,hi=None):
        self.lo=Decimal(lo); self.hi=Decimal(lo if hi is None else hi)
    @staticmethod
    def rat(x):
        x=F(x); a,b=Decimal(x.numerator),Decimal(x.denominator)
        return I(LOW.divide(a,b),HIGH.divide(a,b))
    def __add__(self,x):
        if not isinstance(x,I): x=I.rat(x)
        return I(LOW.add(self.lo,x.lo),HIGH.add(self.hi,x.hi))
    __radd__=__add__
    def __neg__(self): return I(self.hi.copy_negate(),self.lo.copy_negate())
    def __sub__(self,x): return self+(-x if isinstance(x,I) else -F(x))
    def __mul__(self,x):
        if not isinstance(x,I): x=I.rat(x)
        low=[LOW.multiply(a,b) for a in (self.lo,self.hi) for b in (x.lo,x.hi)]
        high=[HIGH.multiply(a,b) for a in (self.lo,self.hi) for b in (x.lo,x.hi)]
        return I(min(low),max(high))
    __rmul__=__mul__
    def exp(self):
        # Decimal.exp is correctly rounded; one adjacent representable guards it.
        return I(NEAR.next_minus(NEAR.exp(self.lo)),NEAR.next_plus(NEAR.exp(self.hi)))
    def sqrt(self):
        assert self.lo>=0
        return I(NEAR.next_minus(NEAR.sqrt(self.lo)) if self.lo else 0,
                 NEAR.next_plus(NEAR.sqrt(self.hi)))
    def out(self): return [str(self.lo),str(self.hi)]

def atan_interval(q,n=90):
    q=F(q); s=sum(((-1)**k*q**(2*k+1)/F(2*k+1) for k in range(n)),F(0))
    nxt=(-1)**n*q**(2*n+1)/F(2*n+1)
    return min(s,s+nxt),max(s,s+nxt)
a,b=atan_interval(F(1,5)); c,d=atan_interval(F(1,239))
PI_LO,PI_HI=16*a-4*d,16*b-4*c
PI=I(I.rat(PI_LO).lo,I.rat(PI_HI).hi)
PI_MID=(PI_LO+PI_HI)/2
NTRIG=19
COSCOEF=[I.rat(F((-1)**k,factorial(2*k))) for k in range(NTRIG+1)]
SINCOEF=[I.rat(F((-1)**k,factorial(2*k+1))) for k in range(NTRIG+1)]
@lru_cache(None)
def sincos(x):
    k=round(2*x/PI_MID)
    r=I.rat(x)-PI*F(k,2)
    assert r.lo>=-1 and r.hi<=1
    z=r*r
    co=COSCOEF[-1]; si=SINCOEF[-1]
    for j in range(NTRIG-1,-1,-1):
        co=COSCOEF[j]+z*co; si=SINCOEF[j]+z*si
    co=co+I.rat(F(1,factorial(2*NTRIG+2)))*I(-1,1)
    si=r*si+I.rat(F(1,factorial(2*NTRIG+3)))*I(-1,1)
    return [(co,si),(-si,co),(-co,-si),(si,-co)][k%4]
@lru_cache(None)
def expreal(x): return I.rat(x).exp()

def bessel_center(n,x,m=22):
    nabs=abs(n); sign=(-1)**nabs if n<0 else 1
    terms=[(-1)**k*(x/2)**(2*k+nabs)/F(factorial(k)*factorial(k+nabs)) for k in range(m)]
    s=sum(terms,F(0)); nxt=(-1)**m*(x/2)**(2*m+nabs)/F(factorial(m)*factorial(m+nabs))
    assert x*x/4<1
    return sign*(s+nxt/2),abs(nxt)/2

def tail(K,x):
    a=x*x/F(4*(K+2)); q=x/F(2*(K+2))
    assert a<1 and q<1
    return 2*(x/2)**(K+1)/F(factorial(K+1))/(1-a)/(1-q)

def matmul(A,B):
    return tuple(sum(A[2*i+k]*B[2*k+j] for k in range(2)) for i in range(2) for j in range(2))
def transpose(A): return (A[0],A[2],A[1],A[3])
IDENT=(1,0,0,1); X=(0,1,1,0); Z=(1,0,0,-1)

K=8
THETA=(F(1,2),F(3,4))
V=F(21,10); DELAY=F(3,5)
# rho(omega)=V exp(-omega), omega>=0; C(0,T)=V/(1-iT).
CRE=V/(1+DELAY*DELAY); CIM=V*DELAY/(1+DELAY*DELAY)

def packets():
    coeff=[]; errors=[]
    for x in THETA:
        pairs={n:bessel_center(n,x) for n in range(-K,K+1)}
        coeff.append({n:p[0] for n,p in pairs.items()})
        errors.append(tail(K,x)+sum(p[1] for p in pairs.values()))
    out=[]
    for n in range(-K,K+1):
        for m in range(-K,K+1):
            M=matmul(Z if m%2 else IDENT,X if n%2 else IDENT)
            M=tuple((-1 if (n+m)%2 else 1)*x for x in M)
            out.append({'n':n,'m':m,'c':coeff[0][n]*coeff[1][m],
                        'norm':V*(n*n+m*m)+2*CRE*n*m,
                        'phase':CIM*n*m,'M':M})
    return out,errors

def no_click(pk,z):
    # Store Hermitian matrix as [q00,q11,Re q01,Im q01].
    Q=[I(0) for _ in range(4)]
    for j,p in enumerate(pk):
        diag=I.rat(p['c']**2)*expreal(-(1-z)*p['norm'])
        Q[0]=Q[0]+diag; Q[1]=Q[1]+diag
        for q in pk[j+1:]:
            re=V*(p['n']*q['n']+p['m']*q['m'])+CRE*(p['n']*q['m']+p['m']*q['n'])
            im=CIM*(p['n']*q['m']-p['m']*q['n'])
            exponent=-(p['norm']+q['norm'])/2+z*re
            phase=q['phase']-p['phase']+z*im
            amp=I.rat(p['c']*q['c'])*expreal(exponent)
            co,si=sincos(phase); rr=amp*co; ii=amp*si
            M=matmul(transpose(p['M']),q['M'])
            Q[0]=Q[0]+rr*(2*M[0]); Q[1]=Q[1]+rr*(2*M[3])
            Q[2]=Q[2]+rr*(M[1]+M[2]); Q[3]=Q[3]+ii*(M[1]-M[2])
    return Q

def vecadd(A,B,s=1): return [a+b*s for a,b in zip(A,B)]
def event_interval(p,eps):
    assert p.hi>=0, 'negative upper probability: invalid arithmetic or model'
    p=I(max(Decimal(0),p.lo),max(Decimal(0),p.hi))
    r=p.sqrt(); e=I.rat(eps)
    low=max(Decimal(0),LOW.subtract(r.lo,e.hi))
    high=HIGH.add(r.hi,e.hi)
    return I(max(Decimal(0),LOW.multiply(low,low)),min(Decimal(1),HIGH.multiply(high,high)))
def rational_out(x): return {'numerator':str(x.numerator),'denominator':str(x.denominator),'decimal_interval':I.rat(x).out()}

def run():
    start=time.time(); pk,errs=packets(); eps=(1+errs[0])*(1+errs[1])-1
    halfdiamond=2*eps
    assert halfdiamond<F(2,1000000000) # exact rational comparison
    mats={}
    for name,z in [('all',F(1)),('no1',F(2,5)),('no2',F(3,4)),('no12',F(3,20))]:
        mats[name]=no_click(pk,z)
        print('finished',name,'seconds',round(time.time()-start,2),flush=True)
    patterns={
      'neither':mats['no12'],
      'only1':vecadd(mats['no2'],mats['no12'],-1),
      'only2':vecadd(mats['no1'],mats['no12'],-1),
      'both':vecadd(vecadd(vecadd(mats['all'],mats['no1'],-1),mats['no2'],-1),mats['no12'])}
    records={}
    for name,Q in patterns.items():
        p={'zero':Q[0],'one':Q[1],
           'plus':(Q[0]+Q[1]+Q[2]*2)*F(1,2),
           'plus_i':(Q[0]+Q[1]-Q[3]*2)*F(1,2)}
        records[name]={'raw_effect':[x.out() for x in Q],
                       'physical_exact_probability':{k:event_interval(v,eps).out() for k,v in p.items()}}
    result={'model':'two noncommuting Pauli-sine kicks coupled to exact positive-frequency exponential continuum',
      'physical_device_claim':False,'time_and_frequency_units':'dimensionless',
      'rho':'(21/10) exp(-omega), omega>=0','delay':'3/5','areas':['1/2','3/4'],
      'axes':['Pauli X','Pauli Z'],'detector_effects':['(3/5)I','(1/4)I'],
      'source_input_dimension':2,'reference_uniform':True,'bath_fock_cutoff':None,
      'spectral_quadrature':None,'bessel_cutoff_each_direction':K,'packets':len(pk),
      'bessel_coefficient_taylor_terms':22,'decimal_precision':PREC,
      'arithmetic':'exact rational coefficients and tails; outward Decimal kernel intervals; rigorous trig Taylor remainders',
      'kick_errors':[rational_out(e) for e in errs],
      'unnormalized_isometry_error':rational_out(eps),
      'polar_CPTP_half_diamond_bound':rational_out(halfdiamond),
      'raw_gram':[x.out() for x in mats['all']],
      'records':records,'runtime_seconds':time.time()-start,
      'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    output=Path(__file__).resolve().parent.parent/'data'/'certified_continuum_kicks.json'
    output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'output':str(output),'halfdiamond':float(halfdiamond),'probabilities':{k:v['physical_exact_probability'] for k,v in records.items()},'runtime':result['runtime_seconds']},indent=2))
if __name__=='__main__': run()
