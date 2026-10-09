#!/usr/bin/env python3
"""Exact, stdlib-only interval certificate for a legal primitive KMS example.

All computational decisions use integers/Fraction; no floating-point number
enters any assertion. This finite certificate supports, but does not replace,
the separate all-kappa stationary sharpness proof. Read the companion note
for the legality/transport proof and the meaning of J and E.
"""
from fractions import Fraction as F
from math import comb, factorial, isqrt
from pathlib import Path
import hashlib
import json

PRECISION = 420
SCALE = 10**PRECISION
TERMS = 120
DIM = 7
ZERO = (0, 0)

def enc(x):
    x = F(x)
    n, d = x.numerator*SCALE, x.denominator
    return n//d, -((-n)//d)

def add(a, b): return a[0]+b[0], a[1]+b[1]
def neg(a): return -a[1], -a[0]
def sub(a, b): return add(a, neg(b))
def mul(a, b):
    p = (a[0]*b[0], a[0]*b[1], a[1]*b[0], a[1]*b[1])
    return min(p)//SCALE, -((-max(p))//SCALE)

def times(a, x):
    x=F(x); n,d=x.numerator,x.denominator
    p=(a[0]*n,a[1]*n)
    return min(p)//d,-((-max(p))//d)

def sqrt_rational(x):
    x=F(x); v=isqrt((x.numerator*SCALE*SCALE)//x.denominator)
    assert v*v*x.denominator <= x.numerator*SCALE*SCALE
    assert (v+1)*(v+1)*x.denominator > x.numerator*SCALE*SCALE
    return v,v+1

def isum(items):
    result=ZERO
    for item in items: result=add(result,item)
    return result

def imatmul(a,b):
    return [[isum(mul(a[i][k],b[k][j]) for k in range(DIM))
             for j in range(DIM)] for i in range(DIM)]

def qmatmul(a,b):
    return [[sum((a[i][k]*b[k][j] for k in range(DIM)),F(0))
             for j in range(DIM)] for i in range(DIM)]

def transpose(a): return list(map(list,zip(*a)))

def print_interval(a, places=14):
    # Decimal endpoint strings are outward rounded, not float summaries.
    divisor=10**(PRECISION-places)
    lo=a[0]//divisor; hi=-((-a[1])//divisor)
    def fmt(v):
        sign='-' if v<0 else ''; v=abs(v)
        return f'{sign}{v//10**places}.{v%10**places:0{places}d}'
    return [fmt(lo),fmt(hi)]

def run():
    h=F(1,65536); eps=F(1,10**100); eta=F(1,10**50)
    r=[(1+i*h)/(1-i*h) for i in range(5)]
    gamma=[F((-1)**(4-i)*comb(4,i),factorial(4))*h**-4 for i in range(5)]
    # Basis order: center, anchor, five leaves.
    s=[F(1),F(1)]+r; Z=sum(x*x for x in s)
    stationary=[[s[i]**2 if i==j else F(0) for j in range(DIM)] for i in range(DIM)]
    R=[row[:] for row in stationary]
    for i in range(5): R[i+2][1]=R[1][i+2]=eps*(r[i]+1)*gamma[i]
    assert sum(R[i][i] for i in range(DIM))==Z
    # Symmetric norm bound implies every eigenvalue R is in (1-rad,1+rad).
    D=[[R[i][j]-(1 if i==j else 0) for j in range(DIM)] for i in range(DIM)]
    row_norm=max(sum(abs(x) for x in row) for row in D)
    rad=F(1,1000)
    assert row_norm<rad<1

    # K=d B d^-1 and C=d V d^-1 are rational even though B is algebraic.
    K=[[F(0) for _ in range(DIM)] for _ in range(DIM)]
    C=[[F(0) for _ in range(DIM)] for _ in range(DIM)]
    C[0][0]=sum(x*x for x in r)
    for i in range(5):
        K[0][i+2]=1; K[i+2][0]=r[i]
        for j in range(5): C[i+2][j+2]=2*r[i]/(r[i]+r[j])
    def generator(X):
        CX=qmatmul(C,X); XC=qmatmul(X,transpose(C)); KXK=qmatmul(qmatmul(K,X),transpose(K))
        return [[(CX[i][j]+XC[i][j])/2-KXK[i][j] for j in range(DIM)] for i in range(DIM)]
    assert all(x==0 for row in generator(stationary) for x in row)
    assert all(C[i][j]+C[j][i]==2*qmatmul(transpose(K),K)[i][j]
               for i in range(DIM) for j in range(DIM))
    G=generator(R)
    for i in range(DIM):
        for j in range(DIM): G[i][j]+=eta*(R[i][j]-stationary[i][j])
    assert all(G[i][i]==0 for i in range(DIM))
    assert all(G[i][j]==G[j][i] for i in range(DIM) for j in range(DIM))

    # Spectral log/sqrt series around I, outward-rounded at every operation.
    Di=[[enc(x) for x in row] for row in D]
    power=[[enc(int(i==j)) for j in range(DIM)] for i in range(DIM)]
    root=[row[:] for row in power]
    log=[[ZERO for _ in range(DIM)] for _ in range(DIM)]
    coefficient=F(1)
    for n in range(1,TERMS+1):
        power=imatmul(power,Di)
        coefficient*=F(3-2*n,2*n)
        for i in range(DIM):
            for j in range(DIM):
                root[i][j]=add(root[i][j],times(power[i][j],coefficient))
                log[i][j]=add(log[i][j],times(power[i][j],F((-1)**(n+1),n)))
    # Both absolute series coefficients <=1, so this bounds the operator
    # norm of each omitted tail and therefore every matrix entry error.
    tail=rad**(TERMS+1)/(1-rad)
    tail_hi=enc(tail)[1]
    for i in range(DIM):
        for j in range(DIM):
            root[i][j]=add(root[i][j],(-tail_hi,tail_hi))
            log[i][j]=add(log[i][j],(-tail_hi,tail_hi))

    # J=Tr L_*rho(log rho-log sigma). G has zero diagonal, so all
    # stationary-log and scalar normalization terms vanish exactly.
    J=times(isum(times(log[j][i],G[i][j]) for i in range(DIM) for j in range(DIM)),1/Z)
    sqrt_products=[[sqrt_rational(r[i]*r[j]) for j in range(5)] for i in range(5)]
    star_cross=isum(mul(sqrt_products[i][j],root[i+2][j+2]) for i in range(5) for j in range(5))
    E_star=times(sub(enc(2*sum(x*x for x in r)),times(star_cross,2)),1/Z)
    overlap=times(isum(times(root[i][i],s[i]) for i in range(DIM)),1/Z)
    E_replacement=sub(enc(1),mul(overlap,overlap))
    E=add(E_star,times(E_replacement,eta))
    gap=sub(J,times(E,F(16,5)))
    assert E[0]>0 and J[0]>0
    assert F(gap[1],SCALE)<-eps**2/F(250)
    scale=eps**-2
    record={
        'status':'PASS_EXACT_INTEGER_INTERVAL_CERTIFICATE',
        'scope':'One faithful rational state for a legal primitive seven-dimensional KMS generator has J < (16/5) E. Not a general nonlinear lower bound.',
        'parameters':{'dimension':DIM,'h':str(h),'epsilon':str(eps),'replacement_rate':str(eta),'gamma':[str(x) for x in gamma],'raw_stationary_root':[str(x) for x in s],'Z':str(Z)},
        'arithmetic':{'kind':'outward fixed-denominator integer intervals; exact Fraction inputs','decimal_denominator_exponent':PRECISION,'series_terms':TERMS,'spectral_radius_upper':str(rad),'series_tail_upper':str(tail)},
        'scaled_by_epsilon_squared':{'J':print_interval(times(J,scale)),'E':print_interval(times(E,scale)),'J_minus_16E_over_5':print_interval(times(gap,scale))},
        'exact_certified_gap':'J-(16/5)E < -(1/250)*epsilon^2',
        'checks':['rational trace and normalization','strict faithfulness via exact row norm','stationary state killed exactly','trace preservation C+C^T=2K^TK','zero diagonal physical generator on the input','positive J and E interval lower bounds','strict negative full nonlinear endpoint gap'],
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    }
    out=Path(__file__).with_name('FINITE_DIMENSION7_CERTIFICATE.json')
    assert not out.exists(), 'Refuse to replace a frozen certificate; use --verify.'
    out.write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps(record['scaled_by_epsilon_squared'],indent=2))
    return record

if __name__=='__main__':
    import sys
    if len(sys.argv)>1 and sys.argv[1]=='--verify':
        # Recompute to a temporary sibling while preserving frozen output.
        import tempfile
        source=Path(__file__)
        with tempfile.TemporaryDirectory(prefix='cycle07-replay-') as td:
            clone=Path(td)/source.name; clone.write_bytes(source.read_bytes())
            import runpy
            result=runpy.run_path(str(clone))['run']()
            assert result==json.loads(source.with_name('FINITE_DIMENSION7_CERTIFICATE.json').read_text())
        print('Frozen certificate exactly reproduced.')
    else:
        run()
