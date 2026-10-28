#!/usr/bin/env python3
"""Prescribed exact algebra and deterministic interval checks. Zero source calls/RNG."""
import heapq,itertools,json
from pathlib import Path
import sympy as s
R=s.Rational;I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Z=s.diag(1,-1);K=s.kronecker_product
clean=lambda A:A.applyfunc(s.expand)
zero=lambda A:clean(A)==s.zeros(*A.shape)
tr=lambda A:s.expand(s.trace(A))
# Exact single-pair learned controlled-reflection receiver.
Bz=K(Z,I);Bx=K(X,I);Xp=K(X,Z);Ip=s.eye(4)
CZ=K((Ip+Bz)/2,I)+K((Ip-Bz)/2,X)
CX=K(Ip,(I+Z)/2)+K(Xp,(I-Z)/2)
V=clean(CZ*CX*CZ);assert zero(V.H*V-s.eye(8))
def keep_last(A,left_dim,last_dim):
 return s.Matrix(last_dim,last_dim,lambda a,b:sum(A[k*last_dim+a,k*last_dim+b] for k in range(left_dim)))
for g in (0,1):
 gauge=s.zeros(2);gauge[g,g]=1
 for a,b in itertools.product(range(2),repeat=2):
  E=s.zeros(2);E[a,b]=1
  got=clean(keep_last(V*K(E,gauge,I/2)*V.H,4,2))
  assert zero(got-(Z**g)*E*(Z**g))
p=s.symbols('p',real=True)
rho=K(I/2,s.diag(1-p,p))
assert tr(rho*(Bx-Xp)**2)==4*p
witness=[{'q':q,'p':str(p0),'joint_loss':str(1-(1-p0)**q),'sum_delta_X':str(4*q*p0)} for q in (1,2,5,17) for p0 in (R(1,1000),R(1,100))]
# Antithetic identity-source example: learner 1's patch contains both logicals.
P={sgn:(I+sgn*X)/2 for sgn in (-1,1)}
omega=s.zeros(16);conditional=[]
for s1 in (-1,1):
 om=s.zeros(16)
 for s2 in (-1,1):
  first=K(P[s1],P[s2]);second=K(P[-s1],P[-s2])
  plus,minus=(first,second) if s1==1 else (second,first)
  om+=K(plus,minus)/2
 conditional.append(clean(om));omega+=om/2
omega=clean(omega)
assert zero(conditional[0]-conditional[1])
rplus=K(P[1],I/2);rminus=K(P[-1],I/2)
plus_marg=s.Matrix(4,4,lambda a,b:sum(omega[a*4+k,b*4+k] for k in range(4)))
minus_marg=keep_last(omega,4,4)
assert zero(plus_marg-rplus) and zero(minus_marg-rminus)
assert not zero(omega-K(rplus,rminus))
gaugeX=K(I,X)
assert tr(omega*K(gaugeX,gaugeX))==-1
assert tr(rplus*gaugeX)==tr(rminus*gaugeX)==0
# Conditioning on a minus-bank spectator X result changes the plus-bank state.
for u in (-1,1):
 effect=K(s.eye(4),K(I,P[u]));weighted=clean(effect*omega*effect)
 prob=tr(weighted);assert prob==R(1,2)
 condplus=s.Matrix(4,4,lambda a,b:sum(weighted[a*4+k,b*4+k] for k in range(4)))/prob
 assert zero(condplus-K(P[1],P[-u]))

# Geometry: each exact logical algebra is a distinct one-site factor i, and Wi contains i.
# This supplies an explicit valid packing witness for every tested envelope family.
geom={'cases':0,'max_q':0,'max_W':0,'max_colors':0,'max_ancestors':0,'max_descendants':0,'max_ancestor_to_K_ratio':'0'}
maxratio=R(0)
def check_envelopes(n,W,offsets):
 global maxratio
 env=[]
 for i,off in enumerate(offsets):
  left=max(0,min(i-off,n-W));env.append((left,left+W-1))
  assert left<=i<=left+W-1
 order=sorted(range(n),key=lambda i:(env[i][0],env[i][1],i))
 active=[];free=[];colors=[None]*n;used=0;overlaps=[]
 for i in order:
  left,right=env[i]
  while active and active[0][0]<left:
   _,color,idx=heapq.heappop(active);heapq.heappush(free,color)
  for _,_,j in active:overlaps.append((i,j))
  color=heapq.heappop(free) if free else used
  if color==used:used+=1
  colors[i]=color;heapq.heappush(active,(right,color,i))
 Cmax=min(n,2*W-1);span_cap=W+2*(Cmax-1)*(W-1);bound=min(n,span_cap)
 assert used<=Cmax
 parents=[[] for _ in range(n)];children=[[] for _ in range(n)]
 for i,j in overlaps:
  assert colors[i]!=colors[j]
  a,b=(i,j) if colors[i]<colors[j] else (j,i)
  parents[b].append(a);children[a].append(b)
 seq=sorted(range(n),key=lambda i:colors[i]);anc=[1<<i for i in range(n)];desc=anc.copy()
 for i in seq:
  for j in parents[i]:anc[i]|=anc[j]
 for i in reversed(seq):
  for j in children[i]:desc[i]|=desc[j]
 for collection in (anc,desc):
  for bits in collection:
   ids=[i for i in range(n) if bits>>i&1]
   assert len(ids)<=bound
   assert max(env[i][1] for i in ids)-min(env[i][0] for i in ids)+1<=span_cap
 ma=max(b.bit_count() for b in anc);md=max(b.bit_count() for b in desc)
 # Double-counting identity used in the Bell-projector sum.
 assert sum(b.bit_count() for b in anc)==sum(b.bit_count() for b in desc)
 geom['cases']+=1;geom['max_q']=max(geom['max_q'],n);geom['max_W']=max(geom['max_W'],W)
 geom['max_colors']=max(geom['max_colors'],used);geom['max_ancestors']=max(geom['max_ancestors'],ma);geom['max_descendants']=max(geom['max_descendants'],md)
 maxratio=max(maxratio,R(max(ma,md),bound))
# Exhaustive small families, with no random sampling.
for n,W in [(6,3),(7,2),(4,4)]:
 for offsets in itertools.product(range(W),repeat=n):check_envelopes(n,W,offsets)
# Long deterministic families, including near-maximal local cliques and multiple color orders.
for n in (17,65,257):
 for W in range(1,9):
  patterns=[(a,) for a in range(W)]+[(a,b) for a in range(W) for b in range(W)]+[(0,b,W-1) for b in range(W)]
  for pattern in patterns:check_envelopes(n,W,[pattern[i%len(pattern)] for i in range(n)])
  period=2*W-1
  toward=[0 if i%period<=W-1 else W-1 for i in range(n)]
  check_envelopes(n,W,toward)
geom['max_ancestor_to_K_ratio']=str(maxratio)
assert R(2)*R(22,256)+R(1,4)==R(27,64)<R(1,2)
assert R(450,16384)<R(1,20)
out={'status':'PASS','source_calls':0,'RNG_used':False,'acquisition_simulation':False,'linear_witness_single_pair_channel_exact':'(1-p)Id+p Ad_Z','linear_witness_delta_X':'4p','linear_witness_delta_Z':'0','linear_witness_values':witness,'antithetic_single_bank_marginals_exact':True,'antithetic_plus_minus_joint_product_false':True,'antithetic_spectator_X_correlation':'-1','other_bank_conditioning_changes_marginal':True,'geometry':geom,'known_integer_factor_packing_witness':'one distinct true logical qubit at each physical site; envelope contains that site','rational_budget_constants':'PASS','kind':'exact fixed-channel algebra and deterministic interval enumeration; not an empirical acquisition experiment'}
f=Path(__file__).with_suffix('.json');f.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(f.read_text(),end='')
