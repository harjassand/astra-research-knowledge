"""Independent exact jump and uniform-bound audit. No author code is imported.
Run in a copy: this writes its own deterministic result file beside the script.
The finite checks supplement, and do not replace, MATHEMATICAL_REVIEW.md.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
COUNTS={'assertions':0,'states':0,'enabled_jumps':0,'core_states':0,'outer_states':0,'terminal_jumps':0}
def require(condition, context=''):
    COUNTS['assertions']+=1
    if not condition: raise AssertionError(context)

def M(x): return x[0]+min(x[2],x[3])
def R(x): return x[2]+x[3]+x[4]
def cutoff(x): return max(F(0),min(F(1),F(96*(M(x)+1)-R(x),48*(M(x)+1))))
def phase(x): return x[0]**2*cutoff(x)
def h(x,N): return 1+F(16,N)*phase(x)
# Explicit increments and propensities, independently entered channel by channel.
def channels(x):
    a,b,c,d,e=x
    return [
      ('immigration',(1,0,0,0,0),1),
      ('death',(-1,0,0,0,0),a),
      ('2A_AC',(-1,0,1,0,0),a*(a-1)),
      ('AC_2A',(1,0,-1,0,0),a*c),
      ('2A_AD',(-1,0,0,1,0),a*(a-1)),
      ('AD_2A',(1,0,0,-1,0),a*d),
      ('2A_AE',(-1,0,0,0,1),a*(a-1)),
      ('AE_2A',(1,0,0,0,-1),a*e),
      ('AE_CD',(-1,0,1,1,-1),a*e),
      ('CD_AE',(1,0,-1,-1,1),2*c*d),
      ('CD_AB',(1,1,-1,-1,0),c*d),
      ('AB_CD',(-1,-1,1,1,0),a*b),
    ]
def shift(x,delta): return tuple(i+j for i,j in zip(x,delta))
def test_state(x,m,N):
    a,b,c,d,e=x; k=M(x); u=k+1; hx=h(x,N)
    require(type(m) is int and m>=1)
    require(N>=10**8*(m+1)**2 and 2*b>=N and k<m)
    require(1<=hx<=F(101,100))
    negative=0; positive_zero=F(0); total=F(0); capture=F(0); byname={}
    for name,delta,q in channels(x):
        require(q>=0,(name,x))
        require(sum(delta)==(1 if name=='immigration' else -1 if name=='death' else 0))
        if q==0: continue
        y=shift(x,delta); dm=M(y)-k
        require(min(y)>=0)
        require(dm in (-1,0,1),(name,x,dm))
        require(y[0]<=m and M(y)<=m)
        hy=h(y,N)
        require(1<=hy<=F(101,100))
        factor=F(2) if dm==-1 else F(1,2) if dm==1 else F(1)
        term=q*(factor*hy-hx); total+=term; byname[name]=(q,dm,term)
        if dm<0:
            negative+=q
            require(y[0]==a-1 and R(y)>=R(x))
            require(cutoff(y)<=cutoff(x) and hy<=hx)
            require(factor*hy-hx<=F(101,100))
        elif dm>0:
            require(factor*hy-hx<=-F(99,200))
        else:
            if hy>hx:
                require(name in ('CD_AE','CD_AB','AC_2A','AD_2A'))
                require(y[0]==a+1 and R(x)-R(y) in (1,2))
                require(phase(y)-phase(x)<=2*a+1+F(a*a,24*u)<=3*a+1)
                require(cutoff(y)>0 and R(x)<=98*u)
                positive_zero+=term
            elif name not in ('CD_AE','CD_AB','AC_2A','AD_2A'):
                require(hy<=hx)
        if name=='AB_CD':
            capture=term
            require(dm==0 and hy<=hx and y[1]==b-1)
        if M(y)>=m or 2*y[1]<N:
            COUNTS['terminal_jumps']+=1
            require(M(y)<=m)
            # Exact normalized terminal lower bound V(y)/2**(-m)>=1.
            require(m-M(y)>=0 and hy>=1)
        COUNTS['enabled_jumps']+=1
    require(negative==a+(3 if c==d else 2)*a*(a-1))
    require(a*a<=negative<=3*a*a)
    cost=F(240000*(m+1)**2*(a*a+1),N)
    require(positive_zero<=cost<=F(a*a+1,100))
    require(total<=-F(12,25) and total<=-hx/4,(x,m,N,total))
    if R(x)<=48*u:
        COUNTS['core_states']+=1
        require(capture<=-8*a*a)
        estimate=-F(99,200)-8*a*a+F(101,100)*3*a*a+F(a*a+1,100)
        require(total<=estimate<=-F(12,25))
    else:
        COUNTS['outer_states']+=1
        satellite=max(c,d,e)
        require(satellite>16*u)
        if e==satellite: name='AE_2A'
        elif c==satellite:
            require(c>d); name='AC_2A'
        else:
            require(d>c); name='AD_2A'
        require(a*satellite>=4*negative)
        if a:
            require(byname[name][0]==a*satellite and byname[name][1]==1)
        estimate=-F(99,200)-(4*F(99,200)-F(101,100))*negative+F(a*a+1,100)
        require(total<=estimate<=-F(12,25))
    COUNTS['states']+=1

# A small cube plus both sides of the nonsmooth min and clipped cutoff surfaces.
seeds=set(product(range(4),repeat=4)) # a,c,d,e
for a,s in product(range(5),range(4)):
    u=a+s+1
    for r in [48*u+j for j in range(-3,4)]+[96*u+j for j in range(-3,4)]+[10**30*u]:
        seeds.update([(a,s,s,r-2*s),(a,s,r-s,0),(a,r-s,s,0),
                      (a,s,s+1,r-2*s-1),(a,s+1,s,r-2*s-1)])
# Huge coordinates: no small-parameter, moving-total, or float shortcut.
for a,s in [(0,10**20),(10**20,0),(10**20,10**20),(10**40,3)]:
    u=a+s+1
    for r in [48*u-1,48*u,48*u+1,96*u-1,96*u,96*u+1,10**50*u]:
        seeds.update([(a,s,s,r-2*s),(a,s,r-s,0),(a,r-s,s,0)])
for a,c,d,e in sorted(seeds):
    m=a+min(c,d)+1
    for odd in (0,1):
        N=10**8*(m+1)**2+odd
        for b in [(N+1)//2, 10**12*N]:
            test_state((a,b,c,d,e),m,N)
# Independent exact constants, including sharper retained intermediate cost.
for a in range(101):
    require(3*a+1<=2*(a*a+1))
    require(a*(3*a+1)<=4*a*a)
    require(a*a<=a+2*a*(a-1)<=a+3*a*(a-1)<=3*a*a)
    if a: require(a*(2*a-1)>=a*a)
require(16*(2*7203+4*98)==236768<240000)
require(F(240000,10**8)==F(3,1250)<F(1,100))
require(-F(99,200)+F(1,100)==-F(97,200)<-F(12,25))
require(F(12,25)>F(101,400))
require(4*F(99,200)-F(101,100)-F(1,100)==F(24,25)>0)
require(F(16,10**8)<F(1,100))
# Optional sqrt scale tested without floating roots; uniform proof is separate.
from math import isqrt
for N in [4*10**8,4*10**8+1,10**10,10**20,10**50]:
    m=isqrt(N)//20000
    require(m>=1 and N>=10**8*(m+1)**2)
# log(2)<1 is certified by the positive exponential series: e>1+1+1/2>2.
require(F(1)+F(1)+F(1,2)>2)
result={
 'status':'PASS_INDEPENDENT_EXACT_FINITE_CHECKS_NOT_A_SUBSTITUTE_FOR_UNIFORM_PROOF',
 'counts':COUNTS,
 'channel_count':12,
 'maximum_seed_coordinate_digits':max(len(str(v)) for s in seeds for v in s),
 'independent_author_code_imports':False,
 'coverage':['all actual enabled channels','C=D and adjacent min corners',
             'R=48(M+1) and R=96(M+1) with neighboring integers',
             'unbounded-scale R and B representatives','even and odd reference N',
             'terminal target evaluated without killing/reset','uniform scalar inequalities'],
 'scope':'Pointwise generator and stated stopped hitting law; no activation/removal/recurrence consumer.'}
(HERE/'INDEPENDENT_CHECK_RESULTS.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps(result,indent=2,sort_keys=True))
