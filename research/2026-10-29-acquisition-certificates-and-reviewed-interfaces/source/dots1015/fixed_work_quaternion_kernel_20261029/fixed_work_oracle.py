"""Pure-rational fixed-work candidate + diagonally-dominant Gram certificate.
No tightness promise, numerical optimization, unbounded search, or timeout success.
"""
import sys
sys.set_int_max_str_digits(0)
from fractions import Fraction as F
import itertools,math
pairs=list(itertools.combinations_with_replacement(range(4),2))
def exp(pair):
 a=[0]*4
 for i in pair:a[i]+=1
 return tuple(a)
ze=[exp(p) for p in pairs];exps=sorted({tuple(a+b for a,b in zip(u,v)) for u in ze for v in ze});groups={e:[] for e in exps}
for i in range(10):
 for j in range(i,10):groups[tuple(a+b for a,b in zip(ze[i],ze[j]))].append((i,j,1 if i==j else 2))
def gram(f):
 G=[[F(0) for j in range(10)] for i in range(10)];ns=[]
 for e,grp in groups.items():
  i,j,a=grp[0];G[i][j]=G[j][i]=f[e]/a
  for k,l,b in grp[1:]:
   N=[[F(0) for j in range(10)] for i in range(10)];N[k][l]=N[l][k]=F(1);N[i][j]=N[j][i]=-F(b,a);ns.append(N)
 return G,ns
qdiag=[F(1 if i==j else 2) for i,j in pairs]
def lower(G):return min((G[i][i]-sum(abs(G[i][j]) for j in range(10) if i!=j))/qdiag[i] for i in range(10))
def stereo(u):
 ss=sum(v*v for v in u);return [(1-ss)/(1+ss)]+[2*v/(1+ss) for v in u]
def evaluate(f,q):return sum(c*math.prod(q[i]**e[i] for i in range(4)) for e,c in f.items())
def solve(raw,candidate_levels=8,gram_levels=tuple(range(4,13))):
 if any(e not in exps for e in raw):raise ValueError('invalid degree4 monomial')
 if not isinstance(candidate_levels,int) or not 0<=candidate_levels<=32:raise ValueError('declared candidate levels must be0..32')
 if any(not isinstance(k,int) or not 0<=k<=32 for k in gram_levels):raise ValueError('declared Gram levels must be0..32')
 f0={e:F(raw.get(e,0)) for e in exps};A=sum(abs(c) for c in f0.values());scale=max(F(1),A);f={e:c/scale for e,c in f0.items()};u=[F(0)]*3;q=stereo(u);upper=evaluate(f,q);evals=1
 for point in itertools.product((-1,0,1),repeat=3):
  uu=list(map(F,point));qq=stereo(uu);vv=evaluate(f,qq);evals+=1
  if vv<upper:u,q,upper=uu,qq,vv
 for k in range(1,candidate_levels+1):
  step=F(1,2**k)
  for dim in range(3):
   bestu,bestq,bestv=u,q,upper
   for sign in (-1,0,1):
    uu=u.copy();uu[dim]=min(F(1),max(F(-1),uu[dim]+sign*step));qq=stereo(uu);vv=evaluate(f,qq);evals+=1
    if vv<bestv:bestu,bestq,bestv=uu,qq,vv
   u,q,upper=bestu,bestq,bestv
 G,ns=gram(f);ys=[F(0)]*20;score=lower(G);scores=1
 for k in gram_levels:
  step=F(1,2**k)
  for dim,N in enumerate(ns):
   bestG,besty,bestv=G,ys[dim],score
   for sign in (-1,0,1):
    GG=[[G[i][j]+sign*step*N[i][j] for j in range(10)] for i in range(10)];v=lower(GG);scores+=1
    if v>bestv:bestG,besty,bestv=GG,ys[dim]+sign*step,v
   G,ys[dim],score=bestG,besty,bestv
 # Weak diagonal dominance suffices for PSD; exact verifier need not imposePD.
 certG=[[G[i][j]-(score*qdiag[i] if i==j else 0) for j in range(10)] for i in range(10)]
 dd_lower=score*scale;trivial=-A;lo=max(dd_lower,trivial);up=upper*scale
 assert sum(t*t for t in q)==1 and up>=lo
 assert evals==28+9*candidate_levels and scores==1+60*len(gram_levels)
 return {'status':'sound_gap_certificate','quaternion':list(map(str,q)),'upper':str(up),'lower':str(lo),'gap':str(up-lo),'dd_lower':str(dd_lower),'trivial_lower':str(trivial),'scale':str(scale),'rational_gram':[[str(v) for v in row] for row in certG],'free_coordinates':list(map(str,ys)),'candidate_levels':candidate_levels,'gram_levels':list(gram_levels),'objective_evaluations':evals,'gram_scores':scores,'scope':'Always-sound candidate/lower gap, no requested accuracy or measured physical clock guarantee.'}
def verify(raw,c):
 f={e:F(raw.get(e,0)) for e in exps};q=list(map(F,c['quaternion']));up=F(c['upper']);lo=F(c['lower']);dd=F(c['dd_lower']);scale=F(c['scale']);G=[[F(v) for v in row] for row in c['rational_gram']]
 assert sum(v*v for v in q)==1 and evaluate(f,q)==up
 assert all(G[i][j]==G[j][i] for i in range(10) for j in range(10))
 assert all(G[i][i]>=sum(abs(G[i][j]) for j in range(10) if i!=j) for i in range(10))
 Q2={tuple(2*(int(i==a)+int(i==b)) for i in range(4)): F(1 if a==b else 2) for a in range(4) for b in range(a,4)}
 for e,grp in groups.items():assert scale*sum(a*G[i][j] for i,j,a in grp)==f[e]-dd*Q2.get(e,0)
 assert F(c['trivial_lower'])==-sum(abs(v) for v in f.values()) and lo==max(dd,F(c['trivial_lower']))
 assert F(c['gap'])==up-lo>=0 and F(c['gap'])<=2*sum(abs(v) for v in f.values())
 return True
