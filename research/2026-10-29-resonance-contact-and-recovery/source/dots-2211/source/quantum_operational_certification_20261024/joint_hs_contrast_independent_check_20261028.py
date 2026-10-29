#!/usr/bin/env python3
"""Independent actual Born-law joint vector moments and exact confidence arithmetic."""
from pathlib import Path
from fractions import Fraction
import numpy as np,itertools,json,math
I=np.eye(2);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1]);P=[X,Y,Z];allP=[I]+P
basis=[np.kron(A,B)/2 for A,B in itertools.product(allP,repeat=2)]
assert max(abs(np.trace(A@B)-(i==j)) for i,A in enumerate(basis) for j,B in enumerate(basis))<1e-14
CNOT=np.zeros((4,4))
for a,b in itertools.product(range(2),repeat=2):CNOT[2*a+(a^b),2*a+b]=1
rot=(3*I-4j*Y)/5;V=np.kron(rot,I)@CNOT
rows=[];events=0
for h in [0,1,2]:
 sigma=[(I+Z)/2,(I+.4*X+.3*Y)/2,I/2][h]
 p=[0.,.2,.45][h]
 def channel(rho):
  output=V@np.kron(rho,sigma)@V.conj().T;Q=np.kron(Z,X)
  return (1-p)*output+p*Q@output@Q
 expected=np.concatenate([[np.trace(B@channel(A/2)).real for B in basis] for A in P])
 vectors=[];probs=[]
 for j,sgn,axes,bits in itertools.product(range(3),[-1,1],itertools.product(range(3),repeat=2),itertools.product([-1,1],repeat=2)):
  out=channel((I+sgn*P[j])/2);pis=[(I+b*P[a])/2 for a,b in zip(axes,bits)];proj=np.kron(*pis);prob=np.trace(proj@out).real/54
  assert prob>=-1e-14
  shadow=np.kron(*[3*pi-I for pi in pis]);v=np.zeros(48);v[16*j:16*(j+1)]=[3*sgn*np.trace(B@shadow).real for B in basis]
  assert abs(v@v-225)<1e-12
  vectors.append(v);probs.append(prob);events+=1
 probs=np.array(probs);vectors=np.array(vectors);mu=probs@vectors;assert abs(sum(probs)-1)<1e-12 and np.linalg.norm(mu-expected)<1e-12
 centered=vectors-mu;cov=centered.T@(probs[:,None]*centered);var=np.trace(cov);assert abs(var-(225-mu@mu))<1e-10
 assert np.linalg.eigvalsh(cov).max()<=var+1e-10 and var<=225+1e-10 and np.linalg.norm(mu)<=np.sqrt(3)+1e-12
 assert np.max(np.linalg.norm(centered,axis=1))<=17
 rows.append({'conditional_history':h,'joint_mean_norm':float(np.linalg.norm(mu)),'conditional_dilation_variance_norm':float(var),'lower_covariance_block_norm':float(np.linalg.eigvalsh(cov).max()),'max_centered_record_norm':float(np.max(np.linalg.norm(centered,axis=1))),'exact_unrounded_record_norm_squared':225})
# Exact rational log and radius arithmetic; no data-estimated variance enters.
L=12;R=17;v=225;target=Fraction(49*32*100);partial=sum((Fraction(L**k,math.factorial(k)) for k in range(40)),Fraction(0));assert partial>target
radii=[]
for N in [1,4096,65536,2**22,2**23]:
 approx=(R*L/3+math.sqrt((R*L/3)**2+2*N*v*L))/N
 eta=Fraction(math.ceil(approx*10**12)+1,10**12)
 slack=N*eta**2-Fraction(2*R*L,3)*eta-2*v*L;assert slack>=0
 radii.append({'N':N,'rational_upper':str(eta),'polynomial_slack':str(slack)})
e=Fraction(radii[3]['rational_upper'])+Fraction(1,250);regret=e*e/Fraction(8,25);assert regret<Fraction(1,200)
out={'status':'PASS_ACTUAL_CONDITIONAL_BORN_MOMENTS_AND_JOINT_HS_RADIUS','source_draws':0,'rng_draws':0,'enumerated_Born_events':events,'real_vector_dimension':48,'dilation_dimension':49,'conditional_cases':rows,'exact_exp12_lower_bound_sufficient':True,'rational_radii':radii,'conditional_forecast_regret_below_half_percent':True,'scope':'Floating enumeration of exact specified Born laws plus rational confidence arithmetic. No sampled source or statistical guarantee inferred empirically.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
