#!/usr/bin/env python3
from pathlib import Path
from fractions import Fraction as F
from math import comb
import json,hashlib,sys
import sympy as s
sys.set_int_max_str_digits(0)
HERE=Path(__file__).parent;ROOT=HERE.parent

def tail(k,p,j):return sum((F(comb(k,t))*p**t*(1-p)**(k-t) for t in range(j+1,k+1)),F(0))
rows=json.loads((ROOT/'exact_tails_v1.json').read_text());replay=[]
for r in rows:
 k=r['k'];p=F(r['delta']);val=tail(k,p,r['j']);assert val==F(int(r['tail_numerator']),int(r['tail_denominator']))
 pure=1-(1-p)**k;assert abs(float(pure)-r['pure_approx_trace_distance'])<1e-14
 replay.append({'k':k,'delta':str(p),'j':r['j'],'tail':float(val),'exact_fraction_matches':True,'pure_approx_trace_distance':float(pure)})
# Exact S4 character calculation across spectra, not RSK or author's argument.
classes=[(1,[1,1,1,1]),(6,[2,1,1]),(3,[2,2]),(8,[3,1]),(6,[4])]
parts=[([4],[1,1,1,1,1]),([3,1],[3,1,-1,0,-1]),([2,2],[2,0,2,-1,0]),([2,1,1],[3,-1,-1,0,1]),([1,1,1,1],[1,-1,1,1,-1])]
schur=[]
for delta in [F(0),F(1,100),F(1,10),F(1,3),F(1,2)]:
 for d in [2,3,5,10]:
  spectrum=[1-delta]+[delta/(d-1)]*(d-1);probs=[]
  for shape,chars in parts:
   z=F(0)
   for (size,cycles),ch in zip(classes,chars):
    trace=F(1)
    for ell in cycles:trace*=sum(p**ell for p in spectrum)
    z+=size*ch*trace
   prob=F(chars[0],24)*z;assert prob>=0;probs.append(prob)
  assert sum(probs)==1
  for j in range(5):
   bad=sum((p for p,(shape,_) in zip(probs,parts) if 4-shape[0]>j),F(0));bound=tail(4,delta,j);assert bad<=bound
  schur.append({'delta':str(delta),'dimension':d,'probabilities':[str(p) for p in probs]})
# Exact 2-copy distributed swap, with entangled rho_AB.
phi=s.Matrix([1,0,0,1])/s.sqrt(2);e01=s.Matrix([0,1,0,0]);rho=s.Rational(9,10)*phi*phi.H+s.Rational(1,10)*e01*e01.H;two=s.kronecker_product(rho,rho)
def swap(a,b):
 U=s.zeros(16)
 for i in range(16):
  bits=list(map(int,f'{i:04b}'));bits[a],bits[b]=bits[b],bits[a];j=int(''.join(map(str,bits)),2);U[j,i]=1
 return U
SA=swap(0,2);SB=swap(1,3);joint={}
for a in [1,-1]:
 for b in [1,-1]:joint[f'{a},{b}']=s.trace(two*(s.eye(16)+a*SA)*(s.eye(16)+b*SB))/4
purity=s.trace(rho*rho);q=joint['1,-1']+joint['-1,1'];assert q==(1-purity)/2
# Pure non-identical marginals and genuinely correlated identical near-pure marginals.
SW=s.Matrix([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]]);anti=(s.eye(4)-SW)/2
assert (e01.H*anti*e01)[0]==s.Rational(1,2)
psi=s.Matrix([0,1,-1,0])/s.sqrt(2);e00=s.Matrix([1,0,0,0]);delta=s.Rational(1,10);Omega=(1-2*delta)*e00*e00.H+2*delta*psi*psi.H
marg=s.Matrix(2,2,lambda i,j:sum(Omega[2*i+a,2*j+a] for a in range(2)));assert marg==s.diag(1-delta,delta)
bad=s.trace(Omega*anti);assert bad==2*delta and bad>1-(1-delta)**2
# Minimal fixed zero-event sample sizes, exact integer comparisons, no simulated data.
cert=[];beta=F(1,1000)
for delta in [F(1,20),F(1,100),F(1,200)]:
 q0=delta*(1-delta);n=0;acc=F(1)
 while acc>beta:n+=1;acc*=1-q0
 assert (1-q0)**(n-1)>beta
 cert.append({'delta':str(delta),'q0':str(q0),'beta':str(beta),'n_min':n,'source_copies':2*n,'acceptance_at_boundary':float(acc),'acceptance_at_half_boundary':float((1-q0/2)**n),'exact_accept_numerator_sha256':hashlib.sha256(str(acc.numerator).encode()).hexdigest(),'exact_accept_denominator_sha256':hashlib.sha256(str(acc.denominator).encode()).hexdigest()})
out={'status':'PASS_INDEPENDENT_EXACT_TAIL_BRANCH_SWAP_AND_CERTIFICATE_CHECKS','tails':replay,'S4_spectral_checks':schur,'distributed_swap':{'purity':str(purity),'joint_local_sign_probabilities':{k:str(v) for k,v in joint.items()},'antisymmetric_product_sign_probability':str(q)},'pure_nonidentical_counterexample_antisymmetric_weight':'1/2','identical_marginal_correlated_counterexample':{'delta':'1/10','marginal':'diag(9/10,1/10)','bad_weight':str(bad),'iid_bound':'19/100'},'zero_event_certificates':cert,'scope':'Exact protocol design and rational checks; no experimental or simulated acquisition bank.'}
(HERE/'check_source_tail_v1.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'certificates':cert,'distributed_swap':out['distributed_swap']},indent=2))
