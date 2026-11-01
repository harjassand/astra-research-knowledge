#!/usr/bin/env python3
"""Supporting author checks; finite checks are not a substitute for the proof."""
import itertools, json, math, random
from fractions import Fraction
from pathlib import Path
import sympy as sp

ROOT=Path(__file__).resolve().parent
s=(sp.sqrt(7)-1)/2;t=2-s;alpha=sp.Rational(2,9)
q=tuple(alpha*v for v in (1,s*s,s,s,t))
Z=(0,0,0,0,0); AA=(2,0,0,0,0); AC=(1,0,1,0,0); AD=(1,0,0,1,0)
AE=(1,0,0,0,1); CD=(0,0,1,1,0); AB=(1,1,0,0,0)
base=[(AA,AC,sp.Integer(1)),(AC,AA,sp.Integer(1)),(AA,AD,sp.Integer(1)),(AD,AA,sp.Integer(1)),
      (AA,AE,sp.Integer(1)),(AE,AA,sp.Integer(1)),(AE,CD,sp.Integer(1)),(CD,AE,sp.Integer(2)),
      (CD,AB,sp.Integer(1)),(AB,CD,sp.Integer(1))]
comp=[(y,z,s if y==AA and z in (AC,AD) else k) for y,z,k in base]+[(AA,CD,1-s)]
A,B,C,D,E=xs=sp.symbols('A B C D E',integer=True,nonnegative=True)
def mon(x,y):
    return sp.prod(a**b for a,b in zip(x,y))
def ff(x,y):
    return sp.prod(sp.prod(a-j for j in range(b)) for a,b in zip(x,y))
assert sp.simplify(sum(q)-1)==0
assert sp.simplify(2*s*s+2*s-3)==0
for v in (AA,AC,AD,AE,CD,AB):
    assert sp.simplify(sum(k*mon(q,y) for y,z,k in comp if y==v)-sum(k*mon(q,y) for y,z,k in comp if z==v))==0
for i in range(5):
    assert sp.simplify(sum(k*ff(xs,y)*(z[i]-y[i]) for y,z,k in base)-sum(k*ff(xs,y)*(z[i]-y[i]) for y,z,k in comp))==0
shift_rows=[]; abs_coeff=[0]*6
for y,z,k in comp:
    target=tuple(x+b-a for x,a,b in zip(xs,y,z))
    delta=sp.expand(ff(target,z)-ff(xs,z))
    coeff=sp.simplify(k*mon(q,y)/mon(q,z))
    row=[delta.coeff(v) for v in xs]+[delta.subs(dict.fromkeys(xs,0))]
    for i,c in enumerate(row):abs_coeff[i]+=coeff*abs(c)
    shift_rows.append({'source':y,'target':z,'delta':str(delta),'weight':str(sp.simplify(coeff))})
abs_coeff=[sp.simplify(v) for v in abs_coeff]
expected=[8+sp.sqrt(7),1,4,4,2,8]
assert all(sp.simplify(a-b)==0 for a,b in zip(abs_coeff,expected))
incident=sp.simplify(sum(k*mon(q,y) for y,z,k in comp if y==AA or z==AA))
assert sp.simplify(incident-2*(s+2)*alpha**2)==0
assert 8+sp.sqrt(7)<sp.Rational(32,3)
assert s<sp.Rational(5,6) and s**2>sp.Rational(1,2)
assert q[1]>sp.Rational(1,7)
assert sp.Rational(6,5)-sp.Rational(484,5)*sp.Rational(1,1000)>1
assert 44*sp.Rational(1,1000)**2<2*alpha
assert 32+sp.Rational(1,9)+sp.Rational(18,32)<33

def occ_harm(h,b):
    return sp.simplify(128*h*(4+33*h)/(3*(sp.Rational(h,6)-b)**2))
assert occ_harm(5,sp.Rational(1,2))==324480
assert occ_harm(8,sp.Integer(1))==823296
assert sp.Rational(1,10)-100*sp.Rational(1,10**6)>0
assert (sp.Rational(1,10)-100*sp.Rational(1,10**6))*2000>2

exponential_examples=[]
for NN,ell,threshold in [(10**19,46,23),(10**20,48,2200)]:
    # exp(ell)>6NN by a rational lower partial sum, hence log(6NN)<ell.
    term=Fraction(1); lower=term
    for j in range(1,201):
        term*=Fraction(ell,j);lower+=term
    assert lower>6*NN
    xx=Fraction(NN*NN,10**12*1920)-169*NN
    exponent=xx*xx/(104*5*NN*NN*ell*ell+Fraction(4,3)*ell*xx)
    assert exponent>threshold
    exponential_examples.append({'N':str(NN),'m0':'1e-6','log_upper':ell,'exponent_lower':threshold,'exact_exponent_at_log_upper':str(exponent)})

qn=tuple(float(v) for v in q); sn=float(s); an=float(alpha)
orig=[(y,z,float(k)) for y,z,k in base]
cn=[(y,z,float(k)) for y,z,k in comp]
def ff_n(x,y):
    ans=1
    for a,b in zip(x,y):
        for j in range(b):ans*=a-j
    return ans

def qmon(y):return math.prod(a**b for a,b in zip(qn,y))

def incV(x,y,z,N):
    ans=0.0
    for xi,yi,zi,qi in zip(x,y,z,qn):
        d=zi-yi
        if d>0:ans+=sum(math.log(xi+j)-math.log(qi*N) for j in range(1,d+1))
        elif d<0:ans+=sum(math.log(qi*N)-math.log(xi-j) for j in range(-d))
    return ans

def check(x,N):
    S=sum(x); a=x[0]
    lv0=lvc=0.0;df=dd=shift=0.0
    for y,z,k in orig:
        rate=k*ff_n(x,y)
        if rate:lv0+=rate*incV(x,y,z,N)
    for y,z,k in cn:
        uy=ff_n(x,y)/qmon(y);uz=ff_n(x,z)/qmon(z);w=k*qmon(y)
        if uy:
            target=tuple(xi+zi-yi for xi,yi,zi in zip(x,y,z))
            v=ff_n(target,z)/qmon(z)
            assert v>0
            lvc+=w*uy*math.log(v/uy)
        else:v=uz
        shift+=w*abs(v-uz)
        df+=w*(math.sqrt(uy)-math.sqrt(uz))**2
        my=math.prod((xi/qi)**yi for xi,qi,yi in zip(x,qn,y))
        mz=math.prod((xi/qi)**zi for xi,qi,zi in zip(x,qn,z))
        dd+=w*(math.sqrt(my)-math.sqrt(mz))**2
    tol=1e-8*(1+S*S)
    assert lv0<=lvc+tol,(x,'competitor',lv0,lvc)
    assert lvc<=-.5*df+1.5*shift+tol,(x,'shift')
    assert shift<=(8+math.sqrt(7))*a+x[1]+4*x[2]+4*x[3]+2*x[4]+8+tol
    assert df>=.5*dd-2*(sn+2)-tol,(x,'falling')
    assert lv0<=-.25*dd+16*S+15+tol,(x,'internal')
    port=math.log((a+1)/(an*N))+(a*math.log(an*N/a) if a else 0)
    assert lv0+port<=-.25*dd+33*N+tol,(x,N,'full')
    for y,z,k in orig:
        if ff_n(x,y):assert abs(incV(x,y,z,N))<=2*math.log(6*N)+1e-9
    assert abs(math.log((a+1)/(an*N)))<=2*math.log(6*N)
    if a:assert abs(math.log(an*N/a))<=2*math.log(6*N)
    qall=sum(k*ff_n(x,y) for y,z,k in orig)+a+1
    assert qall<=3*S*S+1 and qall<=13*N*N
    M=a+min(x[2],x[3])
    if S and M:
        m=min(.001,M/S)
        assert dd+tol>=6*m*m*(a-an*S)**2,(x,'coercivity')
    return sum(1 for y,z,k in cn if ff_n(x,y)>0)

cases=marks=0
for S in range(13):
    for a in range(S+1):
      for b in range(S-a+1):
       for c in range(S-a-b+1):
        for d in range(S-a-b-c+1):
         x=(a,b,c,d,S-a-b-c-d)
         marks+=check(x,32);cases+=1
rng=random.Random(202611010706)
for _ in range(12000):
    N=rng.choice([32,100,1000,10**6,10**9])
    total=rng.randrange(0,2*N+1)
    cuts=sorted([0,total]+[rng.randrange(total+1) for i in range(4)])
    x=tuple(cuts[i+1]-cuts[i] for i in range(5))
    # Force absent/one-count A and other species in a substantial subfamily.
    if rng.random()<.4:
        j=rng.randrange(5);target=rng.randrange(2)
        if x[j]>target:
            xx=list(x);xx[(j+1)%5]+=xx[j]-target;xx[j]=target;x=tuple(xx)
    marks+=check(x,N);cases+=1
report={'status':'PASS supporting symbolic and finite checks; theorem pending independent review',
        'symbolic_checks':['q normalization','complex balance at every binary complex','full count drift equivalence',
          'all eleven affine shifted-target identities','exact absolute-shift envelope','AA incident flux',
          'coercivity rational margins','full drift constant','occupation constants','harmonic horizon/size margins'],
        'abs_shift_coefficients':[str(v) for v in abs_coeff], 'shift_rows':shift_rows,
        'finite_count_states':cases,'enabled_competitor_marks':marks,
        'finite_checks':['actual original<=competitor','exact shifted-target inequality','full count boundary drift',
                        'falling-to-ordinary dissipation','output coercivity on M region'],
        'T5_occupation_coefficient':324480,'T8_occupation_coefficient':823296,
        'exponential_examples_exact':exponential_examples,
        'example_T5':{'m0':'1e-6','N':'1e20','occupation_error':'0.0032448'},
        'limitations':['finite numerical checks are supporting diagnostics only','no larger persistence strip acquired',
          'no microscopic mixing or preparation certificate','population threshold remains severe']}
(ROOT/'CHECK_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
