"""Independent exact polynomial/jump/bound checks; no author code imports.
This writes deterministic adjacent results. Run replays only in a fresh copy.
Finite assertions supplement the independent uniform proof, not replace it.
"""
from fractions import Fraction as Q
from itertools import product
from math import factorial,isqrt
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
count={'assertions':0,'states':0,'enabled_jumps':0,'exponential_states':0,'scale_cases':0}
def ok(b,why=''):
    count['assertions']+=1
    if not b: raise AssertionError(why)
# Six-variable sparse polynomials, the sixth symbol is nonnegative composition slack.
ZERO=(0,)*6
def const(x): return {} if not x else {ZERO:Q(x)}
def var(i):
    t=list(ZERO);t[i]=1;return {tuple(t):Q(1)}
def add(*polys):
    z={}
    for p in polys:
        for k,v in p.items(): z[k]=z.get(k,Q(0))+v
    return {k:v for k,v in z.items() if v}
def mul(p,q):
    z={}
    for a,x in p.items():
        for b,y in q.items():
            k=tuple(i+j for i,j in zip(a,b));z[k]=z.get(k,Q(0))+x*y
    return {k:v for k,v in z.items() if v}
def scale(p,c): return {k:v*c for k,v in p.items() if v*c}
def substitute_b(p):
    # B=100(C+D+E+t), exact polynomial substitution, no sampling.
    z={}
    for powers,v in p.items():
        term=const(v)
        for i,n in enumerate(powers):
            base=scale(add(C,D,E,T),100) if i==1 else var(i)
            for j in range(n):term=mul(term,base)
        z=add(z,term)
    return z
A,B,C,D,E,T=[var(i) for i in range(6)]
aa=mul(A,A);ab=mul(A,B);cd=mul(C,D);ae=mul(A,E)
fall=add(aa,scale(A,-1))
# Actual jumps independently entered as (name, increment, polynomial rate).
channels=[('0_A',(1,0,0,0,0),const(1)),('A_0',(-1,0,0,0,0),A),
 ('2A_AC',(-1,0,1,0,0),fall),('AC_2A',(1,0,-1,0,0),mul(A,C)),
 ('2A_AD',(-1,0,0,1,0),fall),('AD_2A',(1,0,0,-1,0),mul(A,D)),
 ('2A_AE',(-1,0,0,0,1),fall),('AE_2A',(1,0,0,0,-1),ae),
 ('AE_CD',(-1,0,1,1,-1),ae),('CD_AE',(1,0,-1,-1,1),scale(cd,2)),
 ('CD_AB',(1,1,-1,-1,0),cd),('AB_CD',(-1,-1,1,1,0),ab)]
LU={};GAMMA={};TOTAL={};marks={}
for name,delta,rate in channels:
    du=Q(delta[4])-Q(delta[0],10);marks[name]=du
    ok(abs(du)<=Q(11,10))
    ok(sum(delta)==(1 if name=='0_A' else -1 if name=='A_0' else 0))
    LU=add(LU,scale(rate,du));GAMMA=add(GAMMA,scale(rate,du*du));TOTAL=add(TOTAL,rate)
formula_LU=add(scale(cd,Q(17,10)),scale(aa,Q(13,10)),scale(A,-Q(6,5)),const(-Q(1,10)),scale(ab,Q(1,10)),scale(mul(A,add(C,D)),-Q(1,10)),scale(ae,-2))
formula_G=add(const(Q(1,100)),scale(A,Q(1,100)),scale(fall,Q(123,100)),scale(mul(A,add(C,D)),Q(1,100)),scale(ab,Q(1,100)),scale(cd,Q(163,100)),scale(ae,Q(101,50)))
ok(LU==formula_LU);ok(GAMMA==formula_G)
P=add(scale(add(cd,aa),Q(1,2)),scale(ab,Q(2,25)))
f=add(scale(aa,Q(4,5)),scale(A,-Q(6,5)),const(Q(1,2)))
square=add(scale(mul(add(A,const(-Q(3,4))),add(A,const(-Q(3,4)))),Q(4,5)),const(Q(1,20)))
ok(f==square) # f>=1/20, even for real A.
res=substitute_b(add(LU,scale(P,-1),const(Q(3,5))))
expected=add(f,scale(cd,Q(6,5)),scale(mul(A,add(C,D)),Q(19,10)),scale(mul(A,T),2))
ok(res==expected)
upper=add(const(Q(1,100)),scale(aa,Q(31,25)),scale(cd,Q(163,100)),scale(ab,Q(151,5000)))
ok(all(v>=0 for v in substitute_b(add(upper,scale(GAMMA,-1))).values()))
ok(all(v>=0 for v in add(scale(P,4),const(Q(1,100)),scale(upper,-1)).values()))
S=add(A,B,C,D,E)
# Global event intensity <=3 S^2+1, stronger than the stated 32N^2 tube price.
ok(all(v>=0 for v in add(scale(mul(S,S),3),const(1),scale(TOTAL,-1)).values()))
ok(3*4+1<=32)
# Outward rational exponential enclosures for all six constant jump exponents.
def exp_interval(x,K=16):
    if x<0:
        lo,hi=exp_interval(-x,K);return 1/hi,1/lo
    term=Q(1);s=term
    for k in range(1,K+1):term*=x/k;s+=term
    nxt=term*x/(K+1)
    return s,s+nxt/(1-x/(K+2))
exp_upper={}
for du in set(marks.values()):
    lo,hi=exp_interval(-du/10)
    ok(0<lo<=hi)
    ok(hi-1<=-du/10+du*du/100)
    exp_upper[du]=hi
ok(Q(100,89)<2) # e^(11/100)<=sum geometric=(1-11/100)^-1<2.
ok(Q(3,200)*16-Q(601,10000)>=Q(16,100))

def evaluate(p,x):
    y=tuple(x)+(0,)
    return sum(v*__import__('functools').reduce(lambda r,ij:r*ij[0]**ij[1],zip(y,k),1) for k,v in p.items())
def mm(x):return x[0]+min(x[2],x[3])
def rr(x):return x[2]+x[3]+x[4]
seeds=set(product(range(5),repeat=4)) # a,c,d,e
for a in [0,1,4,10**10,10**30]:
    for c,d,e in [(0,10**40,0),(10**40,0,0),(0,0,10**40),(10**20,10**20,0),(1,10**30,1)]:
        seeds.add((a,c,d,e))
for a,c,d,e in sorted(seeds):
    for b in [100*(c+d+e),100*(c+d+e)+1,100*(c+d+e)+10**50]:
        x=(a,b,c,d,e);m=mm(x);s=sum(x)
        lu=Q(0);gamma=Q(0);qsum=Q(0);lz_upper=Q(0)
        ok(100*rr(x)<=b)
        for name,delta,rp in channels:
            q=evaluate(rp,x);ok(q>=0)
            if not q:continue
            y=tuple(v+w for v,w in zip(x,delta))
            ok(min(y)>=0)
            dm=mm(y)-m;ok(dm in (-1,0,1))
            if name=='AB_CD':ok(dm==0 and sum(y)==s and y[1]==b-1)
            du=Q(y[4]-x[4])-Q(y[0]-x[0],10)
            ok(du==marks[name])
            lu+=q*du;gamma+=q*du*du;qsum+=q;lz_upper+=q*(exp_upper[du]-1)
            count['enabled_jumps']+=1
        p=(Q(c*d+a*a,2)+Q(2*a*b,25))
        ok(lu==evaluate(LU,x) and gamma==evaluate(GAMMA,x))
        ok(lu>=p-Q(3,5))
        ok(p>=Q(m*m,4)+Q(2*a*b,25))
        ok(gamma<=4*p+Q(1,100)<=4*lu+Q(241,100))
        ok(qsum<=3*s*s+1)
        ok(lz_upper<=-lu/10+gamma/100)
        if m>=4:
            ok(lz_upper<=-Q(m*m,100));count['exponential_states']+=1
        count['states']+=1
# Large-N scale/floor margins, with exact interval comparisons (no float roots).
Ns={10**40,10**40+1,10**40+10**20,10**40+2*10**20-1,10**40+2*10**20,10**40+2*10**20+1,10**48,10**80+1234567}
for k in [5*10**15,5*10**15+1,10**20]:
    n=(20000*k)**2
    Ns.update([n-1,n,n+1])
for N in sorted(n for n in Ns if n>=10**40):
    root=isqrt(N);m=root//20000;ell=m//2;H=8*m+10**12
    ok(N>=10**8*(m+1)**2)
    ok(40000**2*m*m>=N) # m>=sqrt(N)/40000
    ok(H*H<=N and 4*H<=N)
    ok(200*m<49*N)
    ok(ell>=4 and 2*(ell+1)>m)
    ok(2*ell<=m and ell-m+1<=Q(2-m,2))
    ok(Q(101,100)*32<=65)
    ok(m*m>=Q(N,16*10**8))
    ok(Q(11*N,500)-Q(m*m*10**12,400)<=-N)
    ok(160000**2*(m//1)**2>=16*N) # m/4>=sqrt(N)/160000
    # Representatives of B-rich strip: survival plus inactivity contradict B<=N/2.
    ok(m+Q(101*N,200)<Q(3*N,4))
    count['scale_cases']+=1
# Analytic log-bound certificates used for all N, not just the scale sample.
ok(Q(8,3)**33>65*10**12) # e>1+1+1/2+1/6=8/3 -> log(65 T0)<33.
ok(sum(Q(3)**k/factorial(k) for k in range(4))>10) # e^3>10 -> log10<3.
ok(10**10>120 and 10**10>4) # base and derivative of y-4log y.
ok(33+2*10**10<=3*10**10)
ok(10**10>=1920000) # 3y<=y^2/640000, y>=1e10.
ok(Q(1,3)-Q(1,16)>Q(1,4))
ok(Q(11,500)-Q(25,16)<-1)
ok(Q(1,4)-Q(2,3)<=-Q(1,3))
ok(Q(1,2500)+Q(1,10**8)<1)
ok(1+Q(3,4)>Q(101,100)) # absorbs 1.01 into e^(-m/4), m>=1.
# Algebraic tangent proof: 1/x - (4/3-4x/9)=(2x-3)^2/(9x)>=0.
ok(Q(4,3)-Q(4,9)*Q(3,2)==Q(2,3))
# Explicit scope witness: B-half crossing is a redistribution, not total removal.
N=10**40;m=isqrt(N)//20000
w=(1,N//2,m,0,N//2-m-1)
y=(0,N//2-1,m+1,1,N//2-m-1)
ok(sum(w)==sum(y)==N and y[1]<N//2)
ok(mm(w)==mm(y) and rr(y)>=Q(y[1],100))

def serial_poly(p):return [{'powers':list(k),'coefficient':str(v)} for k,v in sorted(p.items())]
(ROOT/'POLYNOMIAL_IDENTITIES.json').write_text(json.dumps({'LU':serial_poly(LU),'Gamma_U':serial_poly(GAMMA),'total_rate':serial_poly(TOTAL),'U_jump_marks':{k:str(v) for k,v in marks.items()}},indent=2,sort_keys=True)+'\n')
report={'status':'PASS_INDEPENDENT_EXACT_DIAGNOSTICS_AND_IDENTITIES','counts':count,
 'actual_channel_count':12,'author_code_imports':False,'floating_arithmetic':False,
 'exp_enclosures':'Positive rational Taylor degree 16 with geometric remainder; inversion for negative arguments.',
 'uniform_proof':'MATHEMATICAL_REVIEW.md; finite checks do not establish optional stopping or excursion composition by themselves.',
 'scope':'Activation-or-removal hitting law only; no interior-entry or full population-reduction consumer.'}
(ROOT/'INDEPENDENT_CHECK_RESULTS.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
print(json.dumps(report,indent=2,sort_keys=True))
