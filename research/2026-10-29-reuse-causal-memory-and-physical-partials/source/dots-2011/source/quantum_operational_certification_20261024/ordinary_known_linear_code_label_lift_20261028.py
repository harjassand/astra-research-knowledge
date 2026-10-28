#!/usr/bin/env python3
"""Exact label/lift/circuit fixtures; no RNG and no source acquisition outcomes."""
from fractions import Fraction as F
from collections import defaultdict
from pathlib import Path
import itertools,json,hashlib

def logical(c,l):
 r=0
 for i,v in enumerate(c):
  if l>>i&1:r^=v
 return r

def decoder(n,c,es):
 out={}
 for l,g in itertools.product(range(1<<len(c)),range(len(es))):
  x=logical(c,l)^es[g];assert x not in out;out[x]=(l,g)
 assert len(out)==1<<n
 return out
cases=[(3,[7],[0,4,2,1]),(4,[12,6],[0,1,2,15])]
rows=[];basis_checks=0;moments=0
for n,c,es in cases:
 k=len(c);d=1<<n;dec=decoder(n,c,es)
 nonlinear=any(dec[x^y][0] != dec[x][0]^dec[y][0] for x,y in itertools.product(range(d),repeat=2))
 assert nonlinear
 # Basis-level proof of U_tilde, lifted Z and all logical commutation relations.
 seen=set()
 for l,g,a in itertools.product(range(1<<k),range(len(es)),range(d)):
  x=logical(c,l)^es[g]^a;seen.add((x,a));assert dec[x^a]==(l,g)
  for i in range(k):
   assert dec[(x^c[i])^a]==(l^(1<<i),g);basis_checks+=1
  for r in range(1<<k):
   xx,rr=x,r
   # Exact true three-controlled-reflection logical SWAP, retaining coordinate ancillas.
   for i in range(k):
    rr^=((dec[xx^a][0]>>i)&1)<<i
    if rr>>i&1:xx^=c[i]
    rr^=((dec[xx^a][0]>>i)&1)<<i
   assert rr==l and xx==logical(c,r)^es[g]^a;basis_checks+=1
 assert len(seen)==d*d
 # Actual uniform computational preparation/injection labels and X-coherence labels.
 for f in range(d):
  for j in range(n):
   diag=[F(0) for _ in range(d)]
   for l,g in itertools.product(range(1<<k),range(len(es))):
    x=logical(c,l)^es[g];diag[x^f]+=F(-1 if x>>j&1 else 1,d)
   want=[F((-1 if f>>j&1 else 1)*(-1 if y>>j&1 else 1),d) for y in range(d)]
   assert diag==want;moments+=d
  for i in range(k):
   mat=defaultdict(F)
   for l,g in itertools.product(range(1<<k),range(len(es))):
    x=logical(c,l)^es[g];mat[x^f,(x^c[i])^f]+=F(1,d)
   assert dict(mat)=={(x,x^c[i]):F(1,d) for x in range(d)};moments+=d*d
 rows.append({'n':n,'k':k,'columns':c,'transversal':es,'nonlinear_logical_label':nonlinear})
# Explicit multi-logical circuit with ONE noncommuting rational coordinate fit.
n=4;c=[12,6];es=[0,1,2,15];dec=decoder(n,c,es);k=2;t=F(1,1000)
co=(1-t*t)/(1+t*t);si=2*t/(1+t*t)
# S_0=co Z_(bit0)+si X_(bits0,1), other S_j=Z_j. S0,S1 do not commute.
assert co*co+si*si==1 and si!=0
# State key (physical x, coordinate a, receiver r, reference l, retained memory m).
def add(out,key,v):
 if v:out[key]+=v

def trim(x):return {a:b for a,b in x.items() if b}
def qcopy(st,j):
 out=defaultdict(F)
 for key,amp in st.items():
  x,a,r,l,m=key
  if j:
   add(out,(x,a^(((x>>j)&1)<<j),r,l,m),amp)
  else:
   # (I tensor(I+X_A)+S tensor(I-X_A))/2.
   add(out,key,amp/2);add(out,(x,a^1,r,l,m),amp/2)
   z=-1 if x&1 else 1
   add(out,key,amp*co*z/2);add(out,(x,a^1,r,l,m),-amp*co*z/2)
   add(out,(x^3,a,r,l,m),amp*si/2);add(out,(x^3,a^1,r,l,m),-amp*si/2)
 return trim(out)
def w(st,inv=False):
 for j in (range(n-1,-1,-1) if inv else range(n)):st=qcopy(st,j)
 return st
def zhat(st,i):
 st=w(st);st={key:amp*(-1 if dec[key[1]][0]>>i&1 else 1) for key,amp in st.items()};return w(st,True)
def rx(st,i):return {(x,a,r^(1<<i),l,m):v for (x,a,r,l,m),v in st.items()}
def qz(st,i):
 out=defaultdict(F)
 for vec,sgn in [(st,1),(rx(st,i),1),(zhat(st,i),1),(rx(zhat(st,i),i),-1)]:
  for key,v in vec.items():add(out,key,F(sgn,2)*v)
 return trim(out)
def cx(st,i):return {(x^(c[i] if r>>i&1 else 0),a,r,l,m):v for (x,a,r,l,m),v in st.items()}
def norm(st):return sum(v*v for v in st.values())
def bell_fidelity(st):
 env=defaultdict(F)
 for (x,a,r,l,m),v in st.items():
  if r==l:env[x,a,m]+=v/F(2)
 return sum(v*v for v in env.values())
losses=[];eta=F(k*(4*n+1))*2*t
for initr in range(4):
 st={}
 for l in range(4):
  for g,m,amp in [(0,0,F(3,5)),(3,1,F(4,5))]:st[logical(c,l)^es[g],0,initr,l,m]=amp/2
 assert norm(st)==1
 # Exact reflection and common-conjugation commutation on this coherent input.
 assert zhat(zhat(st,0),0)==st
 assert zhat(zhat(st,0),1)==zhat(zhat(st,1),0)
 for i in range(k):st=qz(cx(qz(st,i),i),i)
 assert norm(st)==1
 loss=1-bell_fidelity(st);assert 0<=loss<=eta*eta
 losses.append(str(loss))
# The general finite budget at a first sufficient geometrical stage.
budget_cases=0
for n,k in [(3,1),(4,2),(5,3)]:
 d=1<<n;m=k+1
 for delta in [F(1,32),F(1,128)]:
  for theta in [F(1,1),F(1,20)]:
   gamma=theta/d;a=F(1,16*d);stage=0
   while a>delta*gamma/5:a/=2;stage+=1
   N=8*m*3**n/a**2
   assert N<800*m*3**n/(delta**2*gamma**2)
   e=F(5,4)*a;h=gamma-e;assert h>e and 2*e<=delta*(2*h-e)
   budget_cases+=1
out={'status':'PASS_EXACT_NONLINEAR_COSET_LABEL_LIFT_AND_COHERENT_MULTI_LOGICAL_CIRCUIT',
 'source_outcomes':0,'rng_draws':0,'nonlinear_transversal_cases':rows,
 'augmented_basis_and_true_swap_checks':basis_checks,'signed_moment_entries':moments,
 'actual_noncommuting_rational_coordinate_fit':{'t':str(t),'cos':str(co),'sin':str(si)},
 'coherent_gauge_memory_test':'(3|g0,m0>+4|g3,m1>)/5',
 'actual_two_logical_receiver_losses_by_initial_receiver_basis':losses,
 'unitary_telescoping_squared_upper_bound':str(eta*eta),
 'rational_stage_budget_cases':budget_cases,
 'scope':'exact source-disabled finite fixtures and actual structured-circuit simulation, not sampled acquisition or general learned-reflection synthesis',
 'sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),Path(__file__).with_suffix('.md')]}}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
