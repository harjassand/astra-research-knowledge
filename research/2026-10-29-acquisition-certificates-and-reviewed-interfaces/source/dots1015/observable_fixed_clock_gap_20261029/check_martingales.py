"""Exact finite adaptive-history checks, not a quantum hardware simulation."""
from fractions import Fraction as F
from math import comb
from pathlib import Path
import json
R=F(2);M=2;p=F(1,2);L=F(1);T=5

def phi(G):
 if G>=R:return F(0)
 if G<=-R:return G
 return -(R-G)**2/(4*R)
def grad(G):return max(F(0),min(F(1),(R-G)/(2*R)))
# States include actual G and action-dependent retained classical memory.
states={(F(0),0):F(1)};centering=0;potential_checks=0;bias_checks=0;maxrange=F(0)
for t in range(T):
 nxt={}
 for (G,mem),mass in states.items():
  ell=F(1 if mem%2==0 else -1);a=grad(G);cand=[]
  for z in [-R/2,R/2]:
   w=G+z;x=F(int(w<F(3,2)));gap=w*x-min(F(0),w);cand.append((x,gap))
  xbar=sum(x for x,e in cand)/2;mu=sum(e for x,e in cand)/2
  assert (xbar-a)**2<=(mu+R/M)/R;bias_checks+=1
  Y=[];mean=F(0)
  for x,e in cand:
   for role,prob in [('learn',F(1,2)),('service',F(1,4)),('validate',F(1,4))]:
    g=ell/p if role=='learn' else F(0)
    r=ell*x # comparator x*=0, current loss difference
    y=r-g*a-ell*(xbar-a);weight=prob/2;mean+=weight*y;Y.append(y)
    assert g*a<=phi(G+g)-phi(G)+g*g/(4*R);potential_checks+=1
    # Current action changes the subsequent source state; no counterfactual reset.
    new=(G+g,(mem+int(x)+(role=='service'))%3);nxt[new]=nxt.get(new,F(0))+mass*weight
  assert mean==0;centering+=1;maxrange=max(maxrange,max(Y)-min(Y));assert max(Y)-min(Y)<=2*(1+L/p)
 states=nxt
 assert sum(states.values())==1
# Exact adaptive nonnegative-gap process, B=1, q depends on previous gap count.
# Track both observed sum and accumulated conditional means (units1/5).
dist={(0,0):F(1)};H=60;kdelta=4;delta=F(1,2**kdelta)
for t in range(H):
 nxt={}
 for (observed,mean_units),prob in dist.items():
  qnum=1 if observed%2==0 else 3
  nxt[(observed,mean_units+qnum)]=nxt.get((observed,mean_units+qnum),F(0))+prob*F(5-qnum,5)
  nxt[(observed+1,mean_units+qnum)]=nxt.get((observed+1,mean_units+qnum),F(0))+prob*F(qnum,5)
 dist=nxt
failure=sum(prob for (obs,mu),prob in dist.items() if F(mu,5)>2*obs+2*kdelta)
assert failure<=delta and failure>0
# Validation conditional martingale centering, includes candidate-dependent q.
for q in [F(0),F(1,7),F(3,5),F(1)]:
 assert q*(1-q)+(1-q)*(-q)==0
 assert (1-q)-(-q)==1
out={'scope':'Exact scalar adaptive-source martingale identities and adaptive gap-tail enumeration; not physical quantum execution or all-case proof by simulation.','rounds':T,'conditional_states_checked':centering,'potential_steps_checked':potential_checks,'bias_bounds_checked':bias_checks,'max_Y_conditional_range':str(maxrange),'general_range_bound':str(2*(1+L/p)),'adaptive_gap_process_rounds':H,'adaptive_gap_tail_failure_exact':str(failure),'adaptive_gap_tail_failure_float':float(failure),'allocated_failure':str(delta),'validation_range1_verified':True}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
