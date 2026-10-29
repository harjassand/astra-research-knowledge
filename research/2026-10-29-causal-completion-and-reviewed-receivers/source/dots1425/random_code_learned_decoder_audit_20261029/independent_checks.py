"""Exact two-qubit Clifford CODE-ORBIT moments and independent composition checks.
Not a full Clifford sampler and not a learned recovery execution.
"""
import sympy as s
import numpy as np
from fractions import Fraction as F
from pathlib import Path
import json
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1)
P=[s.kronecker_product(a,b) for a in [I,X,Y,Z] for b in [I,X,Y,Z]]
D=4;k=2
# The 30 rank-2 stabilizer code projectors form the Clifford orbit of I tensor |0><0|.
# Each nonidentity Pauli and its negative has the same number of Clifford preimages.
Ps=[(s.eye(4)+sign*p)/2 for p in P[1:] for sign in [-1,1]]
assert all(p*p==p and s.trace(p)==2 for p in Ps)
Fswap=s.zeros(16)
for i in range(4):
 for j in range(4):Fswap[4*i+j,4*j+i]=1
moment=sum((s.kronecker_product(p,p) for p in Ps),s.zeros(16))/30
assert moment==s.Rational(7,30)*s.eye(16)+s.Rational(1,15)*Fswap
# Derive the variable-marginal centered moment from same/distinct column moments.
d,kk,a,b=s.symbols('d kk a b',positive=True)
same=(a+b)/(d*(d+1));off=(b-a/d)/(d*d-1);distinctdiag=(a-b/d)/(d*d-1)
J2=same/kk+(kk-1)*off/kk
tau2=same/kk+(kk-1)*distinctdiag/kk
center=s.factor(J2-tau2/kk)
expected=(kk*kk-1)/(kk*kk*(d*d-1))*(b-a/d)
assert s.simplify(center-expected)==0
fixed=s.factor(J2-a/(kk*d*d));assert s.simplify(fixed-(kk*d-1)/(kk*d*(d*d-1))*(b-a/d))==0

# Rational/complex-rational Kraus fixtures, including nonunital rectangular noise.
partial=[]
for e in range(2):
 q=s.zeros(2,4)
 for i in range(2):q[i,2*i+e]=1
 partial.append(q)
W=s.Rational(3,5)*I+s.Rational(4,5)*s.I*X
ad0=s.diag(1,s.Rational(4,5));ad1=s.Matrix([[0,s.Rational(3,5)],[0,0]])
ad=[s.kronecker_product(ad0*W,I),s.kronecker_product(ad1*W,I)]
embed=s.zeros(5,4)
for i in range(4):embed[i,i]=1
erasure=[s.Rational(3,5)*embed]
for i in range(4):
 q=s.zeros(5,4);q[4,i]=s.Rational(4,5);erasure.append(q)
fixtures=[('partial_trace_4_to_2',partial),('complex_rotated_AD_4_to_4',ad),('random_unitary_dephasing',[s.Rational(3,5)*s.eye(4),s.Rational(4,5)*s.kronecker_product(Z,X)]),('rectangular_erasure_4_to_5',erasure),('complex_unitary',[s.kronecker_product(W,W)])]
rows=[]
for name,K in fixtures:
 assert sum((q.adjoint()*q for q in K),s.zeros(4))==s.eye(4)
 outdim=K[0].rows;r=len(K);N_I=sum((q*q.adjoint() for q in K),s.zeros(outdim));T_I=s.Matrix([[s.trace(q*t.adjoint()) for t in K] for q in K]);aa=s.trace(T_I*T_I);bb=s.trace(N_I*N_I)
 vals=[];fixedvals=[]
 for p in Ps:
  pairs=[[q.adjoint()*t for t in K] for q in K]
  j2=sum(s.trace(p*pairs[i][j]*p*pairs[j][i]) for i in range(r) for j in range(r))/k**2
  t2=sum(s.trace(p*pairs[i][j])*s.trace(p*pairs[j][i]) for i in range(r) for j in range(r))/k**2
  val=s.simplify(j2-t2/k);assert val>=0;vals.append(val)
 avg=s.simplify(sum(vals)/30);analytic=s.Rational(k*k-1,k*k*(D*D-1))*(bb-aa/D)
 assert s.simplify(avg-analytic)==0
 assert avg<=bb/D**2 and bb<=r*D
 rows.append({'name':name,'D':D,'k':k,'Dout':outdim,'kraus_list_length':r,'a':str(aa),'b':str(bb),'exact_centered_moment':str(avg),'minimum_over_code_orbit':str(min(vals)),'maximum_over_code_orbit':str(max(vals))})
# Boundary k=1, full code k=D, and all allowed scalar coefficient comparisons.
for DD in range(2,41):
 for Kk in range(1,DD+1):
  coeff=F(Kk*Kk-1,Kk*Kk*(DD*DD-1));assert coeff<=F(1,DD*DD)
assert s.simplify(center.subs(kk,1))==0

# Independent complex random logical channels and full Pauli conjugation twirl.
rng=np.random.default_rng(202610291405)
p1=[np.array(z.tolist(),complex) for z in [I,X,Y,Z]]
def paulilist(n):
 pp=[np.ones((1,1),complex)]
 for _ in range(n):pp=[np.kron(q,p) for q in pp for p in p1]
 return pp
def apply(K,a):return sum(q@a@q.conj().T for q in K)
def choi(K):
 dim=K[0].shape[1]
 return sum(np.outer(q.T.reshape(-1),q.T.reshape(-1).conj()) for q in K)/dim
max_offdiag=0;max_fe=0;max_trace=0;twirls=[]
for n in [1,2,3]:
 dim=2**n;pp=paulilist(n)
 for repeat in range(4):
  env=3;g=rng.normal(size=(dim*env,dim))+1j*rng.normal(size=(dim*env,dim));v=np.linalg.qr(g)[0];K=[v.reshape(dim,env,dim)[:,e,:] for e in range(env)]
  J=choi(K);tw=sum(choi([p.conj().T@q@p for q in K]) for p in pp)/len(pp)
  bell=np.column_stack([p.T.reshape(-1)/np.sqrt(dim) for p in pp]);jj=bell.conj().T@tw@bell;max_offdiag=max(max_offdiag,float(np.max(abs(jj-np.diag(np.diag(jj))))))
  weights=np.diag(jj).real;assert weights.min()>-1e-12 and abs(sum(weights)-1)<1e-12
  fe0=sum(abs(np.trace(q))**2 for q in K)/dim**2;fet=float(weights[0]);max_fe=max(max_fe,abs(fe0-fet))
  omega=np.outer(bell[:,0],bell[:,0].conj());Dchoi=np.linalg.norm(tw-omega,ord='nuc')/2;error=1-fet;max_trace=max(max_trace,abs(Dchoi-error))
  # Pauli-channel triangle upper bound equals this Bell-input trace lower bound.
  assert abs(Dchoi-error)<2e-12
  twirls.append({'logical_dimension':dim,'Fe':fet,'certified_by_Pauli_structure_halfdiamond':error})
assert max_offdiag<2e-12 and max_fe<2e-12
# Exact coherent error distinguishes discarded vs released pad key.
# V=cos(pi/6) I+i sin(pi/6) Z; twirled nonidentity mass=1/4;
# each keyed Bell output has trace distance sqrt(1-Fe)=1/2.
key_boundary={'Fe':str(F(3,4)),'retired_key_halfdiamond':str(F(1,4)),'retained_key_Bell_input_trace_distance':str(F(1,2))}
# Exact sampler budgets. Group order modulo phase is not a power of two.
sampling=[]
for n in range(1,21):
 G=2**(n*n+2*n)
 for j in range(1,n+1):G*=4**j-1
 b=(G-1).bit_length();p=F(G,2**b);assert F(1,2)<p<=1 and G&(G-1)!=0
 for q in [1,4,12,30]:
  eta=F(1,2**q);fail=(1-p)**q;assert fail<=eta
  # For any fixed valid integer, sum over first-accept positions is independent
  # of its value, hence conditioning on success preserves exact uniformity.
  prob_each=F(1,2**b)*sum((1-p)**j for j in range(q));assert prob_each==(1-fail)/G
 sampling.append({'n':n,'group_order_bits':G.bit_length(),'draw_bits':b,'expected_bits_upper_bound':2*b,'tested_caps':[1,4,12,30]})
# Algebraic composition of the squared-fidelity learner with code average.
for den in [10,31,100]:
 for i in range(den+1):
  f=F(i,den);assert f*f>=1-2*(1-f)

boundaries={'key_retirement':key_boundary,'bad_fixed_Clifford_seed':{'source':'trace out last qubit, D=2048,k=r=2','bad_code':'swap the logical carrier into the traced-out qubit','optimal_entanglement_fidelity':str(F(1,4)),'average_optimal_infidelity_bound':str(F(1,16))},'source_adapts_after_seed':{'source':'N_U=trace out first logical qubit after conjugation by U dagger','D':2048,'k':2,'kraus_rank':2,'all_seed_optimal_fidelity':str(F(1,4)),'violated_if_wrongly_applied_average_optimal_fidelity_lower_bound':str(F(15,16))}}
out={'scope':'Exact second moments on a nontrivial Clifford code orbit and independent logical-twirl/finite-bit composition checks. Not a physical learner or full Clifford compiler execution.','exact_projector_orbit_size':30,'exact_projector_second_moment':'7/30 I + 1/15 SWAP','symbolic_centered_moment':str(center),'symbolic_fixed_margin_moment':str(fixed),'exact_source_cases':rows,'logical_twirl_cases':len(twirls),'maximum_twirl_Bell_offdiagonal':max_offdiag,'maximum_twirl_Fe_change':max_fe,'maximum_Pauli_error_identity_residual':max_trace,'sampler_n_cases':len(sampling),'scope_boundary_witnesses':boundaries,'logical_twirl_details':twirls,'sampler_checks':sampling,'passed':True}
(Path(__file__).parent/'INDEPENDENT_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['logical_twirl_details','sampler_checks']},indent=2))
