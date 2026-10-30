"""Exact finite algebra and optional floating-point checks for the scoped barrier.

All exact series use Gaussian integers and exponential derivatives in x=d/2.
No checkpoint code is imported or modified. No finite check substitutes for the
analytic moving-bath lower bound in PROOF.md.
"""
from fractions import Fraction
from itertools import product
from math import comb, factorial, sqrt, log, e
import json
from pathlib import Path

TABLE = {
    ('X','Y'): ('Z',(0,1)), ('Y','Z'): ('X',(0,1)), ('Z','X'): ('Y',(0,1)),
    ('Y','X'): ('Z',(0,-1)), ('Z','Y'): ('X',(0,-1)), ('X','Z'): ('Y',(0,-1)),
}
HANDLES = {'A':'XIX','B':'IXY','C':'YIZ'}
ZERO, ONE = (0,0), (1,0)


def ga(a,b): return a[0]+b[0],a[1]+b[1]
def gm(a,b): return a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]
def gs(a,n): return a[0]*n,a[1]*n

def pm(a,b):
    out=[]; phase=ONE
    for x,y in zip(a,b):
        if x=='I': z,p=y,ONE
        elif y=='I': z,p=x,ONE
        elif x==y: z,p='I',ONE
        else: z,p=TABLE[x,y]
        out.append(z); phase=gm(phase,p)
    return ''.join(out),phase

def add(a,b):
    out=dict(a)
    for p,c in b.items(): out[p]=ga(out.get(p,ZERO),c)
    return {p:c for p,c in out.items() if c!=ZERO}

def scale(a,n): return {p:gs(c,n) for p,c in a.items() if gs(c,n)!=ZERO}
def mul(a,b):
    out={}
    for p,c in a.items():
        for q,d in b.items():
            r,f=pm(p,q); out[r]=ga(out.get(r,ZERO),gm(gm(c,d),f))
    return {p:c for p,c in out.items() if c!=ZERO}

def dagger(a): return {p:(c[0],-c[1]) for p,c in a.items()}

def smul(a,b,degree):
    return [sum_polys(scale(mul(a[j],b[n-j]),comb(n,j)) for j in range(n+1))
            for n in range(degree+1)]

def sum_polys(xs):
    out={}
    for x in xs: out=add(out,x)
    return out

def inverse(word): return [(h,-s) for h,s in reversed(word)]
def comm(u,v): return inverse(v)+inverse(u)+v+u

def word5():
    word=comm([('B',1)],[('C',1)])
    for unused in range(3): word=comm([('A',1)],word)
    # Reverse C so the clean fifth-order term has the target orientation.
    word=[(h,-s if h=='C' else s) for h,s in word]
    return word+list(reversed(word))

PROFILE=word5()

def waveform(profile):
    cumulative=Fraction(0); angle=Fraction(0); hs=[]; mus={h:Fraction(0) for h in HANDLES}
    absolute_area=Fraction(0)
    for handle,orientation in profile:
        nxt=cumulative+(orientation if handle=='A' else 0)
        midpoint=(cumulative+nxt)/2
        h=(midpoint>0)-(midpoint<0)
        hs.append(h)
        # F_A has constant sign on this unit interval (zero endpoints allowed).
        absolute_area+=abs(midpoint)
        mus[handle]+=orientation*(angle+Fraction(h,2))
        angle+=h; cumulative=nxt
    assert cumulative==0
    assert mus['A']==-absolute_area and absolute_area>0
    return hs,mus,angle

HS,MUS,NET_ANGLE=waveform(PROFILE)

def evolution(profile,hs,coins,degree=5,gains=None):
    gains=gains or {'A':1,'B':1,'C':1}
    series=[{'III':ONE}]+[{} for unused in range(degree)]
    for (handle,orientation),h in zip(profile,hs):
        # exp(x L), x=d/2. L=-i(2g*s*orientation*J+h Z_M).
        control=2*gains[handle]*coins[handle]*orientation
        assert int(control)==control
        generator={HANDLES[handle]:(0,-int(control))}
        if h: generator['IIZ']=(0,-h)
        pulse=[{'III':ONE}]
        for n in range(1,degree+1): pulse.append(mul(generator,pulse[-1]))
        series=smul(pulse,series,degree)
    return series


def format_coefficient(poly,n):
    denominator=2**n*factorial(n)
    return {p:[str(Fraction(c[0],denominator)),str(Fraction(c[1],denominator))]
            for p,c in poly.items()}


def exact_checks():
    assert MUS['A']==-130 and NET_ANGLE==0
    assert all(sum(s for k,s in PROFILE if k==h)==0 for h in HANDLES)
    assert all(sum(Fraction(2*j+1,2)*s for j,(k,s) in enumerate(PROFILE) if k==h)==0 for h in HANDLES)
    degree=9; series=[]; frozen_checks=[]
    for a,b in product((-1,1),repeat=2):
        coins={'A':a,'B':b,'C':a*b}
        frozen=evolution(PROFILE,[0]*len(PROFILE),coins,degree)
        assert frozen[0]=={'III':ONE}
        assert all(not frozen[n] for n in range(1,5))
        assert frozen[5]=={'ZXI':(0,-32*2**5*factorial(5))}
        moving=evolution(PROFILE,HS,coins,degree)
        series.append((coins,moving))
        frozen_checks.append({'sA':a,'sB':b,'coefficient_d5':format_coefficient(frozen[5],5)})
    # Check gain scaling at two exact integer box corners.
    for gains in ({'A':2,'B':1,'C':1},{'A':1,'B':2,'C':2}):
        frozen=evolution(PROFILE,[0]*len(PROFILE),{'A':1,'B':1,'C':1},degree,gains)
        coefficient=-32*gains['A']**3*gains['B']*gains['C']
        assert all(not frozen[n] for n in range(1,5))
        assert frozen[5]=={'ZXI':(0,coefficient*2**5*factorial(5))}
    # U_A = E[s_A U_s] has d^2 coefficient i*mu_A X1 Y_M.
    fourier={h:[sum_polys(scale(u[n],coins[h]) for coins,u in series)
                for n in range(degree+1)] for h in HANDLES}
    assert fourier['A'][2]=={'XIY':(0,4*8*int(MUS['A']))}
    assert fourier['C'][2]=={}
    # Heisenberg channel E[U_s^dag Z1 U_s], exact derivatives.
    average=[]
    for n in range(degree+1):
        term={}
        for coins,u in series:
            for j in range(n+1):
                term=add(term,scale(mul(mul(dagger(u[j]),{'ZII':ONE}),u[n-j]),comb(n,j)))
        average.append(term)
    assert average[0]=={'ZII':(4,0)}
    assert all(not average[n] for n in (1,2,3))
    expected=-2*int(MUS['A'])**2
    assert average[4]=={'ZII':(4*2**4*factorial(4)*expected,0)}
    assert average[6]=={'ZII':(4*2**6*factorial(6)*Fraction(16701716,3),0)}
    assert average[8]=={'ZII':(-4*2**8*factorial(8)*Fraction(1425644383,6),0)}
    assert all(not average[n] for n in (5,7,9))
    result={
        'description':'Exact finite Pauli-series checks, not an unrestricted no-go certificate',
        'segments':len(PROFILE),'raw_segments':len(PROFILE)//2,
        'areas':{h:sum(s for k,s in PROFILE if k==h) for h in HANDLES},
        'first_moments':{h:sum(Fraction(2*j+1,2)*s for j,(k,s) in enumerate(PROFILE) if k==h) for h in HANDLES},
        'mu':{h:str(v) for h,v in MUS.items()},'net_bath_angle':str(NET_ANGLE),
        'frozen_checks':frozen_checks,
        'heisenberg_Z1_coefficient_d4':str(expected),
        'heisenberg_Z1_coefficient_d5':format_coefficient(scale(average[5],Fraction(1,4)),5),
        'cubic_only_lower_bound':(5-sqrt(25-8*sqrt(2)))/4,
        'heisenberg_even_coefficients':{str(n):format_coefficient(scale(average[n],Fraction(1,4)),n) for n in (6,8)},
        'finite_certificate':finite_certificate(),
        'all_policy_action_bound':{'rho':3+2*sqrt(2),'prefactor':1/(64*(3+2*sqrt(2))**4),'exponent':16*e*log(3+2*sqrt(2))+1},
        'profile':PROFILE,'bath_h':HS,
    }
    result['first_moments']={h:str(v) for h,v in result['first_moments'].items()}
    return result



def finite_certificate():
    # Rational Machin brackets certify the requested cycle count.
    def atan_bracket(denominator):
        terms=60
        lo=sum(Fraction((-1)**k,(2*k+1)*denominator**(2*k+1)) for k in range(terms))
        return lo,lo+Fraction(1,(2*terms+1)*denominator**(2*terms+1))
    a,aa=atan_bracket(5); b,bb=atan_bracket(239)
    pi_lo,pi_hi=16*a-4*bb,16*aa-4*b
    def ceil(x): return (x.numerator+x.denominator-1)//x.denominator
    d=Fraction(1,1000)
    n=ceil(pi_lo/(128*d**5))
    assert n==ceil(pi_hi/(128*d**5))
    alpha=33800*d**4-Fraction(16701716,3)*d**6+Fraction(1425644383,6)*d**8
    tail=Fraction((3*len(PROFILE))**10,factorial(10))*d**10
    assert 0<alpha<1
    # exp(-x)<=1/(1+x), leaving a fully rational lower certificate.
    bound=1-1/(1+n*alpha)-tail/alpha
    assert bound>Fraction(9999,10000)
    # An independent drift-free bound confirms this is a bath-induced failure,
    # rather than only a badly chosen finite leading-angle approximation.
    frozen=evolution(PROFILE,[0]*len(PROFILE),{'A':1,'B':1,'C':1},12)
    discrepancy=Fraction(0)
    for k,poly in enumerate(frozen):
        target={}
        if k==0: target={'III':ONE}
        if k==5: target={'ZXI':(0,-32*2**5*factorial(5))}
        if k==10: target={'III':(-512*2**10*factorial(10),0)}
        diff=add(poly,scale(target,-1))
        l1=sum(Fraction(abs(c[0])+abs(c[1]),2**k*factorial(k)) for c in diff.values())
        discrepancy+=l1*d**k
    unitary_bound=discrepancy+Fraction(len(PROFILE)**13,factorial(13))*d**13+Fraction(32**3,6)*d**15
    driftfree_bound=2*n*unitary_bound+64*d**5
    assert driftfree_bound<Fraction(15,1000000)
    return {'d':str(d),'N':n,'native_segments':len(PROFILE)*n,
            'duration':str(len(PROFILE)*n*d),'alpha':str(alpha),
            'one_cycle_remainder_bound':str(tail),
            'trace_norm_error_lower_bound':str(bound),
            'trace_norm_error_lower_bound_decimal':float(bound),
            'driftfree_diamond_error_upper_bound':str(driftfree_bound),
            'driftfree_diamond_error_upper_bound_decimal':float(driftfree_bound)}


def numerical_checks():
    import numpy as np
    I=np.eye(2,dtype=complex)
    X=np.array([[0,1],[1,0]],complex); Y=np.array([[0,-1j],[1j,0]],complex); Z=np.diag([1.,-1.]).astype(complex)
    pauli={'I':I,'X':X,'Y':Y,'Z':Z}
    def matrix(label): return np.kron(np.kron(pauli[label[0]],pauli[label[1]]),pauli[label[2]])
    native={h:matrix(label) for h,label in HANDLES.items()}; bath=matrix('IIZ'); z1=matrix('ZII')
    records=[]
    for d in (.02,.01,.005,.0025):
        us=[]
        for a,b in product((-1,1),repeat=2):
            signs={'A':a,'B':b,'C':a*b}; u=np.eye(8,dtype=complex)
            for (handle,orientation),h in zip(PROFILE,HS):
                ham=orientation*signs[handle]*native[handle]+h*bath/2
                vals,vec=np.linalg.eigh(ham)
                pulse=(vec*np.exp(-1j*d*vals))@vec.conj().T
                u=pulse@u
            us.append(u)
        heis=sum(u.conj().T@z1@u for u in us)/4
        leading=z1-2*float(MUS['A']**2)*d**4*z1
        remainder=np.linalg.norm(heis-leading,2)
        # Superoperator powering is deterministic channel averaging, not coin sampling.
        channel=sum(np.kron(u.conj(),u) for u in us)/4
        n=max(1,round(.2/(32*d**5)))
        rho=np.kron(np.kron((I+Z)/2,I/2),I/2)
        out=(np.linalg.matrix_power(channel,n)@rho.reshape(-1,order='F')).reshape(8,8,order='F')
        expectation=float(np.trace(z1@out).real)
        records.append({'d':d,'heisenberg_remainder_over_d6':remainder/d**6,'N':n,
                        'Z1_expectation_after_N':expectation,
                        'trace_drift':float(abs(np.trace(out)-1)),
                        'frozen_logical_angle':32*n*d**5,
                        'N_d4':n*d**4,
                        'unitarity':max(float(np.linalg.norm(u.conj().T@u-np.eye(8),2)) for u in us)})
    return records

if __name__=='__main__':
    result=exact_checks()
    try: result['numerical_checks']=numerical_checks()
    except ImportError as exc: result['numerical_checks_unavailable']=str(exc)
    output=Path(__file__).with_name('CHECKS.json')
    output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('profile','bath_h')},indent=2))
