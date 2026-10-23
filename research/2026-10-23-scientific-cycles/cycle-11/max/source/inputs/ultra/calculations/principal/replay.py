#!/usr/bin/env python3
"""New Cycle10 scalar/access admissions; no quantum code or predecessor replay."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from collections import defaultdict
import hashlib,json,math,time

def entropy(values):
 return -sum(float(x)*math.log(float(x)) for x in values if x)
def h2(x):return -x*math.log(x)-(1-x)*math.log1p(-x) if 0<x<1 else 0.
def g(x):return (1+x)*h2(x/(1+x)) if x else 0.
def clog(base,numerator,denominator=1):
 p=1;s=0
 while p*denominator<numerator:p*=base;s+=1
 return s
def posterior_constant(D,L):
 q=1/(D*D);cq=-math.log1p(-q)-q/(1-q)*math.log(q)
 c=0.
 for j in range(1,L+1):
  qj=q**j;h=math.log1p(-qj)-math.log1p(-q)-(q/(1-q)-j*qj/(1-qj))*math.log(q)
  p=(1-qj)/L if j<L else (1-qj)/(L*(1-q))
  c+=p*h
 return c,cq
def access_case(D,L,r,mode):
 q=F(1,D*D);law=defaultdict(F);vectors=list(product(range(1,L+1),repeat=r))
 for k in vectors:
  if mode=='none':zs=[('none',F(1))]
  elif mode=='parity':zs=[('p'+str(sum(k)%2),F(1))]
  elif mode=='full':zs=[(str(k),F(1))]
  elif mode=='first':zs=[('k'+str(k[0]),F(1))]
  elif mode=='erasure':zs=[('?',F(2,3)),(str(k),F(1,3))]
  else:raise ValueError(mode)
  for j in product(*(range(x,L+1) for x in k)):
   p=F(1,L**r)
   for a,b in zip(k,j):p*=q**(b-a)*(1-q if b<L else 1)
   for z,pz in zs:law[(k,j,z)]+=p*pz
 assert sum(law.values())==1
 marginal={}
 for name,idx in [('K',(0,)),('J',(1,)),('Z',(2,)),('KZ',(0,2)),('JZ',(1,2)),('KJZ',(0,1,2)),('KJ',(0,1))]:
  m=defaultdict(F)
  for key,p in law.items():m[tuple(key[i] for i in idx)]+=p
  assert sum(m.values())==1;marginal[name]=entropy(m.values())
 H=marginal;hkz=H['KZ']-H['Z'];hkjz=H['KJZ']-H['JZ'];hkj=H['KJ']-H['J'];info=H['K']-hkz
 B=(L+1)*math.log(D)/2;C,_=posterior_constant(D,L);U=B-.5*math.log(L)+.5*C
 conditional=r*B-.5*hkz+.5*hkjz
 assert abs(hkj-r*C)<2e-12
 assert hkjz<=r*C+2e-12
 assert conditional<=r*U+.5*info+2e-12
 assert conditional<=r*B+2e-12
 if mode=='full':assert abs(conditional-r*B)<2e-12 and abs(info-r*math.log(L))<2e-12
 rational=[[list(k),list(j),z,str(p)] for (k,j,z),p in sorted(law.items())]
 return {'D':D,'L':L,'r':r,'mode':mode,'rational_branches':len(law),'I_access':info,'H_K_given_JZ':hkjz,'actual_conditional_half_mutual_information':conditional,'resource_upper_before_min':r*U+.5*info,'source_mean_supply':r*B,'rational_law_sha256':hashlib.sha256(json.dumps(rational,separators=(',',':')).encode()).hexdigest()}
def rate_case(D,L):
 eta=F(1,L*L);t=32*clog(2,L+1)+128*clog(2,2*L*L);s=clog(D,2*L*L);Q=4*t+9*s;w=3*Q
 B=(L+1)*math.log(D)/2;C,cq=posterior_constant(D,L)
 V=B-(w+D/(D-1)+2*float(eta)*L)*math.log(D)-g(float(eta));lower=max(math.log(D),V);upper=B-.5*math.log(L)+.5*C
 assert lower<=upper+1e-8
 return {'D':D,'L':L,'eta':str(eta),'exact_t':t,'exact_s':s,'exact_Q':Q,'exact_w8':w,'B_nats':B,'achievable_rate_lower_nats':lower,'rate_upper_nats':upper,'necessary_deficit_nats':B-upper,'sufficient_deficit_nats':B-lower,'C_L':C,'geometric_entropy_upper':cq,'preprocessing_direction_bits_upper_per_queue':Q*(D-1).bit_length()+(L).bit_length(),'scope':'Scalar theorem evaluation, not a large quantum state/code or measured implementation'}
def main():
 start=time.perf_counter();cpu=time.process_time()
 cases=[access_case(D,L,r,m) for D,L,r in [(2,2,1),(2,4,2),(3,3,2),(4,2,3),(6,4,1)] for m in ['none','parity','full','first','erasure']]
 heavy=[]
 for n in [1,2,4,8,16,32]:
  ps=sum(F(3,4**j) for j in range(1,n+1));bs=sum(F(3,4**j)*2**j for j in range(1,n+1))
  assert ps==1-F(1,4**n);assert bs==3*(1-F(1,2**n))
  heavy.append({'truncation_n':n,'probability_prefix':str(ps),'probability_tail':str(F(1,4**n)),'expected_logrank_prefix_in_ln2_units':str(bs),'expected_logrank_tail_in_ln2_units':str(F(3,2**n))})
 tables=[rate_case(D,L) for D,L in [(2,2),(2,100),(2,2**16),(2,2**20),(2,2**22),(3,2**18),(6,2**18)]]
 output={'status':'PASS','access_cases':cases,'exact_access_rational_branches':sum(x['rational_branches'] for x in cases),'heavy_tail_stock':{'definition':'n>=1,p(n)=3*4^-n,J(n)=2^(2^n)','expected_lnJ':'3 ln2 exactly','expected_J':'INFINITE (positive summands diverge)','admissions':heavy},'rate_tables':tables,'wall_seconds':time.perf_counter()-start,'cpu_seconds':time.process_time()-cpu,'quantum_code_executions':0,'predecessor_science_runs':0,'hardware_calls':0,'paid_credits':0,'total_discovery_inference_cost':'UNKNOWN'}
 p=Path(__file__).with_name('RESULT.json');p.write_text(json.dumps(output,indent=2)+'\n');print(json.dumps({k:output[k] for k in ['status','exact_access_rational_branches','wall_seconds','cpu_seconds','quantum_code_executions','predecessor_science_runs']}))
if __name__=='__main__':main()
