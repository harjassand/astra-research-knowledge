import itertools,json
from collections import Counter
from pathlib import Path
import sympy as s
out=[]
for n in [2,3]:
 states=list(itertools.permutations(range(n))); d=len(states); idx={x:i for i,x in enumerate(states)}
 def move(x,c):return (c,)+tuple(a for a in x if a!=c)
 Ts=[]
 for c in range(n):
  T=s.zeros(d)
  for j,x in enumerate(states):T[j,idx[move(x,c)]]=1
  Ts.append(T)
 P=sum(Ts,s.zeros(d))/n; I=s.eye(d); psi=s.ones(d,1)/s.sqrt(d); Pg=psi*psi.T
 C=sum(((T-I).T*(T-I) for T in Ts),s.zeros(d))/n
 H=s.I*(P-P.T)/2
 assert C==2*I-P-P.T and (H*psi)==s.zeros(d,1)
 assert sum((T.T*T for T in Ts),s.zeros(d))/n==I
 for a in range(d):
  for b in range(d):
   E=s.zeros(d); E[a,b]=1
   Phi=sum((T*E*T.T for T in Ts),s.zeros(d))/n
   D=sum(((T-I)*E*(T-I).T for T in Ts),s.zeros(d))/n-(C*E+E*C)/2-s.I*(H*E-E*H)
   assert D==Phi-E
 for a in range(d):
  E=s.zeros(d);E[a,a]=1
  adj=sum((T.T*E*T for T in Ts),s.zeros(d))/n
  assert adj==s.diag(*list(P.row(a)))
 out.append({'n':n,'d':d,'exact_TP_dark_generator_and_reverse_diagonal':True})
for n,k in [(2,3),(3,3),(3,5),(4,4),(4,5)]:
 states=list(itertools.permutations(range(n))); roots=Counter(); good=0
 for seq in itertools.product(range(n),repeat=k):
  if len(set(seq))!=n:continue
  finals=[]
  for x0 in states:
   x=x0
   for c in seq:x=(c,)+tuple(a for a in x if a!=c)
   finals.append(x)
  assert len(set(finals))==1
  good+=1;roots[finals[0]]+=1
 assert len(roots)==len(states) and len(set(roots.values()))==1
 out.append({'n':n,'steps':k,'good_words':good,'all_words':n**k,'roots':len(roots),'words_per_root':next(iter(roots.values())),'exact_equivariant_uniform_root':True})
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
