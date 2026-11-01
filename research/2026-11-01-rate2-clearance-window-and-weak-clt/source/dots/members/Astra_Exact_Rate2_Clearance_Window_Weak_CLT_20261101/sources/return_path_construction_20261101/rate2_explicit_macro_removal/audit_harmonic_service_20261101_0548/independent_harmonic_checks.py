"""Independent full-generator/finite-mark audit; no author imports or floats.
Replay in a copy: deterministic JSON outputs are written beside this script.
Finite checks supplement, not replace, MATHEMATICAL_REVIEW.md.
"""
from fractions import Fraction as Q
from itertools import product
from math import factorial
from pathlib import Path
import json
import sympy as sy
ROOT=Path(__file__).resolve().parent
counts={'assertions':0,'origin_small_states':0,'region_states':0,'enabled_region_marks':0,'direct_exponential_states':0,'service_parameters':0}
def ck(v,why=''):
 counts['assertions']+=1
 if not v:raise AssertionError(why)
# All 12 literal increments, not an import of author reaction encoding.
def reactions(x):
 a,b,c,d,e=x
 return [('imm',(1,0,0,0,0),1),('death',(-1,0,0,0,0),a),
 ('2A_AC',(-1,0,1,0,0),a*(a-1)),('AC_2A',(1,0,-1,0,0),a*c),
 ('2A_AD',(-1,0,0,1,0),a*(a-1)),('AD_2A',(1,0,0,-1,0),a*d),
 ('2A_AE',(-1,0,0,0,1),a*(a-1)),('AE_2A',(1,0,0,0,-1),a*e),
 ('AE_CD',(-1,0,1,1,-1),a*e),('CD_AE',(1,0,-1,-1,1),2*c*d),
 ('CD_AB',(1,1,-1,-1,0),c*d),('AB_CD',(-1,-1,1,1,0),a*b)]
def shift(x,v):return tuple(a+b for a,b in zip(x,v))
def M(x):return x[0]+min(x[2],x[3])
def H(x):
 c=x[0]+x[2];d=x[0]+x[3]
 return Q(2*c*d,c+d) if c+d else Q(0)
def ff(x):return x[0]*(x[0]-1)
def W(x,N):return H(x)-Q(100*ff(x),N)
a,b,c,d,e=sy.symbols('a b c d e');xx=(a,b,c,d,e)
GA=sy.Integer(0);Gff=sy.Integer(0);Gc=sy.Integer(0);Gd=sy.Integer(0);qH=sy.Integer(0);qall=sy.Integer(0)
neutral={'AB_CD','CD_AB','AE_CD','CD_AE'}
for name,v,r in reactions(xx):
 y=shift(xx,v);dc=v[0]+v[2];dd=v[0]+v[3]
 GA+=r*v[0];Gff+=r*(y[0]*(y[0]-1)-a*(a-1));Gc+=r*dc;Gd+=r*dd;qall+=r
 if dc or dd:qH+=r
 ck(sum(v)==(1 if name=='imm' else -1 if name=='death' else 0))
 ck(abs(v[0])==1)
 ck(dc in (-1,0,1) and dd in (-1,0,1) and dc*dc+dd*dd<=2)
 ck((name in neutral)==(dc==0 and dd==0))
GA,Gff,Gc,Gd,qH,qall=map(sy.expand,[GA,Gff,Gc,Gd,qH,qall])
ck(sy.expand(GA-(1-a-3*a*(a-1)+a*(c+d)+3*c*d-a*b))==0)
ck(sy.expand(Gc-(1+a-2*a*a+a*(d+e)))==0)
ck(sy.expand(Gd-(1+a-2*a*a+a*(c+e)))==0)
ck(sy.expand(Gff-(-6*a**3+10*a*a-2*a+2*a*a*(c+d)+2*a*e+6*a*c*d-2*a*(a-1)*b))==0)
ck(sy.expand(qH-(1+a+3*a*(a-1)+a*(c+d+e)))==0)
ck(all(v>=0 for _,v in sy.Poly(sy.expand(3*(a+b+c+d+e)**2+1-qall),a,b,c,d,e).terms()))
x,t=sy.symbols('x t',nonnegative=True)
res=sy.expand((GA-(3*(a+x)**2-a*(1+6*(a+x)+b))).subs({c:x,d:x+t}))
ck(sy.expand(res-(1+3*a+2*a*x+a*t+3*x*t))==0)
u,v=sy.symbols('u v',positive=True);hh=2*u*v/(u+v)
grad=[sy.diff(hh,u),sy.diff(hh,v)]
hess=sy.hessian(hh,(u,v))
want=-4/(u+v)**3*sy.Matrix([[v*v,-u*v],[-u*v,u*u]])
ck(all(sy.simplify(z)==0 for z in hess-want))
ck(sy.simplify(hess.det())==0)
ck(sy.simplify(-sy.trace(hess)-4*(u*u+v*v)/(u+v)**3)==0)
# Origin/axis cases ensure globally defined targets and falling-factorial startup.
for state in product(range(3),repeat=5):
 hv=H(state);ck(M(state)<=hv<=2*M(state));ck(state[0]<=M(state))
 for name,mark,r in reactions(state):
  if not r:continue
  target=shift(state,mark);ck(min(target)>=0)
  dh=H(target)-hv;df=ff(target)-ff(state)
  ck(abs(dh)<=2);ck(abs(df)<=2*state[0])
  if state[0]==0:ck(df==0)
  if name in neutral:ck(dh==0)
 counts['origin_small_states']+=1
# Uniform constants are rational, not rounded decimals.
delta=Q(1,10**6);Nlo=200000;rho=Q(1,4)-delta/2
ck(Q(1,2)-Q(8,1000)-1000*delta==Q(491,1000)>=Q(49,100))
ck(1-Q(4,1000)-Q(200,Nlo)==Q(995,1000)>=Q(49,100))
ck(1-Q(4,1000)>=Q(99,100))
ck(12-1+Q(4,1000)+1000*delta<12)
ck(6*delta+Q(12,Nlo)<=Q(24,100)*rho)
ck(delta/rho<=5*delta)
# Direct conservative full-intensity envelope, uniform for every N>=Nlo.
ck(Q(1,Nlo*Nlo)+delta/Nlo+3*delta**2+10*delta<=13*delta)
ck(32+80000*13*delta<=34)
ck(8<=50 and 34<=50 and 16<=50)
ck(8<=198 and 16+34*5*delta<=50)
ck(Q(99,100)+Q(49,100)*499+44-62>=Q(1+499+1,4))
for A in range(2,100):ck(44*A*A-62*A>=10*A*A)
ck(Q(1,400)-200*Q(1,400)**2==Q(1,800))
ck(2+200*delta<3)
ck(1/(1-Q(3,400))<2)
# Outward rational exponential for occasional direct GQ tests.
def exp_iv(z,degree=12):
 if z<0:
  lo,hi=exp_iv(-z,degree);return 1/hi,1/lo
 if not z:return Q(1),Q(1)
 term=Q(1);s=term
 for j in range(1,degree+1):term*=z/j;s+=term
 nxt=term*z/(degree+1)
 return s,s+nxt/(1-z/(degree+2))
for N in [10**12+1,10**16]:
 small=[0,1,499,500,501,999,1000,1001,10**5,N//8]
 As=[0,1,2,10,499,1000,10**5]
 Bs=[0,N//4-1,N//4,N//4+1,N//2,N]
 for A,C,D,B,S in product(As,small,small,Bs,[3*N//4+1,N,2*N]):
  E=S-A-B-C-D
  if E<0:continue
  state=(A,B,C,D,E);hv=H(state)
  if not (1000<=hv<=delta*N and 4*S>3*N):continue
  X=max(C,D)+E;c0=A+C;d0=A+D;ss=c0+d0;wv=W(state,N)
  ck(M(state)<=hv<=2*M(state));ck(A<=M(state));ck(ss>=2*hv)
  ck(Q(9999,10000)*hv<=wv<=hv)
  g=Q(0);gam=Q(0);h_rate=0;total=0;gq=Q(0)
  direct=counts['region_states']%37==0
  for name,mark,r in reactions(state):
   if not r:continue
   target=shift(state,mark);ck(min(target)>=0)
   dh=H(target)-hv;df=ff(target)-ff(state);dw=W(target,N)-wv
   dc=mark[0]+mark[2];dd=mark[0]+mark[3]
   linear=Q(2*d0*d0,ss*ss)*dc+Q(2*c0*c0,ss*ss)*dd
   ck(dh-linear>=-Q(4,ss-2)>=-Q(4,hv))
   ck(abs(dh)<=2 and abs(df)<=2*A and abs(dw)<=3)
   if name in neutral:ck(dh==0)
   if A==0:ck(df==0)
   if dc or dd:h_rate+=r
   total+=r;g+=r*dw;gam+=r*dw*dw
   if direct:
    lo,hi=exp_iv(-dw/400);ck(hi-1<=-dw/400+dw*dw/160000)
    gq+=r*(hi-1)
   counts['enabled_region_marks']+=1
  ck(h_rate==1+A+3*A*(A-1)+A*(C+D+E))
  ck(Q(total,N*N)<=13*delta)
  lower=Q(99,100)+Q(49*A*X,100)-6*A*A-12*A+Q(200*A*(A-1)*B,N)
  ck(g>=lower and g>0)
  ck(gam<=8+34*A*A+16*A*X<=200*g)
  if 4*B>=N:ck(g>=Q(1+A*X+A*A,4))
  else:
   ck(X>=rho*N);ck(A*A<=5*delta*A*X);ck(g>=Q(99,100)+Q(A*X,4))
  if direct:ck(gq<=-g/800);counts['direct_exponential_states']+=1
  counts['region_states']+=1
# Explicit service scales, overshoots, bracket and physical endpoint.
def ceil(q):return -((-q.numerator)//q.denominator)
for m0 in [Q(1,10**6),Q(1,10**12),Q(1,2*10**100),Q(3,10**9)]:
 h=400/(m0*m0);N=ceil(32*h);r=m0*N
 ck(N>=32*h and N>=200000 and r/2>=1000)
 ck(r-2-100*m0*m0*N-r/2>=Q(2,5)*r)
 ck(r-2>r/2)
 ck(Q(3,16)*m0*m0*h==75)
 ck(2*N-75*N*N+52*N*N<=-20*N*N)
 threshold=20*N*N;variance=32*N*N*h
 ck(threshold*threshold/(2*(variance+Q(threshold,3)))==200*N*N/(32*h+Q(20,3)))
 ck(Q(1,1)+12*N<=13*N)
 ck(Q(5,4)*N+Q(N,16)<2*N)
 ck(Q(3,4)*N+Q(N,16)==Q(13*N,16))
 ck(Q(5,4)*N+Q(N,16)-Q(3,4)*N<2*N)
 ck(h-Q(N,16)*Q(2,3)<=-Q(N,96))
 counts['service_parameters']+=1
# log2 upper/lower certificates needed by BOTH Poisson directions.
ck(sum(Q(3,4)**j/factorial(j) for j in range(4))>2) # log2<3/4.
ck(2*(1-Q(3,4))==Q(1,2))
ck(Q(4,3)-Q(4,9)*Q(3,2)==Q(2,3)) # tangent-integral log2>=2/3.
# Exact intended tiny-macro substitution, without promoting any join.
m0=Q(1,2*10**100);h=400/m0**2
ck(h==1600*10**200 and 32*h==51200*10**200)
(ROOT/'EXACT_IDENTITIES.json').write_text(json.dumps({'GA':str(GA),'G_falling_factorial':str(Gff),'G_c':str(Gc),'G_d':str(Gd),'q_H':str(qH),'q_all':str(qall),'harmonic_Hessian':str(hess)},indent=2,sort_keys=True)+'\n')
report={'status':'PASS_INDEPENDENT_EXACT_SUPPORTING_CHECKS','counts':counts,'author_code_imports':False,'float_arithmetic':False,
 'scope':'Explicit harmonic macro service at the stated fixed-reference endpoint; replacement joins remain separate.',
 'proof':'MATHEMATICAL_REVIEW.md; finite checks do not prove optional stopping or event composition.'}
(ROOT/'INDEPENDENT_CHECK_RESULTS.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
print(json.dumps(report,indent=2,sort_keys=True))
