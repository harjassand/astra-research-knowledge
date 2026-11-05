"""Exact IID counterexample for canonical majority-path envelopes.
The chain has Z-error distance 2m, not balanced CSS distance 2m.
"""
from fractions import Fraction as F
from math import comb,isqrt
from pathlib import Path
import json

def graph(m):
 # v_j=j, upper/lower midpoint labels m+1+2j and m+2+2j.
 E=[]
 for j in range(m):
  u=m+1+2*j;v=u+1;E.extend([(j,u),(u,j+1),(j,v),(v,j+1)])
 checks=[x for x in range(3*m+1) if x not in (0,m)]
 ids={x:i for i,x in enumerate(checks)}
 masks=[sum(1<<ids[x] for x in e if x in ids) for e in E]
 return masks
checks=[]
for m in range(1,5):
 masks=graph(m);syndromes=[0]*(1<<(4*m));best={};weight_enumerators={}
 for e in range(1<<(4*m)):
  if e:
   bit=e&-e;syndromes[e]=syndromes[e^bit]^masks[bit.bit_length()-1]
  L=((e>>0)&1)^((e>>2)&1);key=(syndromes[e],L)
  best[key]=min(best.get(key,4*m+1),e.bit_count())
  weight_enumerators.setdefault(key,[0]*(4*m+1))[e.bit_count()]+=1
 for sy,L in best:
  if best[sy,0]==best[sy,1]:assert weight_enumerators[sy,0]==weight_enumerators[sy,1]
 violations=0;strict=ties=0
 for e,sy in enumerate(syndromes):
  L=((e>>0)&1)^((e>>2)&1)
  expected=best[sy,1-L]-best[sy,L]
  actual=0
  for j in range(m):
   a=((e>>(4*j))&3).bit_count();b=((e>>(4*j+2))&3).bit_count()
   cost0=min(a+b,4-a-b);cost1=min(2-a+b,2-b+a)
   actual+=cost1-cost0
  assert actual==expected,(m,e,actual,expected)
  strict+=actual<0;ties+=actual==0
 checks.append({'m':m,'error_patterns':len(syndromes),'syndrome_logical_classes':len(best),'all_class_cost_differences_match':True,'strict_patterns':strict,'tie_patterns':ties,'tied_coset_weight_enumerators_equal':True})

def sqrt_upper(x,den=10**20):
 n=isqrt(x.numerator*den*den//x.denominator)
 if n*n*x.denominator<x.numerator*den*den:n+=1
 r=F(n,den);assert r*r>=x
 return r

def distribution(m,p):
 a=(1-p)**4+p**4;b=2*p*p*(1-p)**2;c=1-a-b
 den=p.denominator**4
 A=int(a*den);B=int(b*den);C=int(c*den)
 assert A+B+C==den
 row=[1]
 for _ in range(m):
  nxt=[0]*(len(row)+2)
  for k,w in enumerate(row):nxt[k]+=B*w;nxt[k+1]+=C*w;nxt[k+2]+=A*w
  row=nxt
 return F(sum(row[:m]),den**m),F(row[m],den**m)
rows=[]
for p in [F(1,10000),F(1,1000),F(1,200),F(1,100)]:
 a=(1-p)**4+p**4;b=2*p*p*(1-p)**2;c=1-a-b
 rho=c+2*sqrt_upper(a*b);r=rho/(8*p*(1-p))
 assert r<1
 for m in [5,10,20,50,100,200]:
  strict,tie=distribution(m,p)
  z=2**m*sum(F(comb(2*m,k))*p**k*(1-p)**(2*m-k) for k in range(m,2*m+1))
  bound=(2*m+1)*r**m
  assert strict+tie<=rho**m
  assert (strict+tie)/z<=bound
  rows.append({'p':str(p),'m':m,'Z_distance':2*m,'dual_X_distance':2,'base_upper_exact':str(r),'base_upper':float(r),'acceptance_if_equal_tie_mass':float((strict+tie/2)/z),'acceptance_lower_from_strict_failures':float(strict/z),'acceptance_upper_including_all_ties':float((strict+tie)/z),'chernoff_acceptance_upper':min(1.,float(bound)),'negative_log10_Z':None})
out={'exhaustive_checks':checks,'formula':'acceptance <= (2m+1)[(c+2sqrt(ab))/(8p(1-p))]^m; a=(1-p)^4+p^4,b=2p²(1-p)²,c=1-a-b','small_p_base':'(2+sqrt(2))/4','rows':rows,'scope':'Planar serial-diamond decoding graph, Z-error distance2m and dual X-distance2. Does not prove the same scaling for ordinary square surface codes.'}
Path(__file__).with_name('diamond_checks.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'checks':checks,'rows':rows},indent=2))
