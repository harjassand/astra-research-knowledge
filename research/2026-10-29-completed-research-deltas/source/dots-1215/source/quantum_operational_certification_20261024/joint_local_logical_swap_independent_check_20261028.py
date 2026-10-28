#!/usr/bin/env python3
"""Exact prescribed two-logical-qubit joint swap check; no source calls or RNG."""
import json
from pathlib import Path
import sympy as s
R=s.Rational;I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Z=s.diag(1,-1);K=s.kronecker_product
clean=lambda A:A.applyfunc(s.expand)
zero=lambda A:clean(A)==s.zeros(*A.shape)
tr=lambda A:s.expand(s.trace(A))
q=2;D=4;dg=2;dp=8;da=4
U=clean((3*s.eye(dp)+4*s.I*K(X,I,X))/5*(5*s.eye(dp)+12*s.I*K(I,Z,X))/13)
assert zero(U.H*U-s.eye(dp))
sigma=s.diag(R(999,1000),R(1,1000))
rho=clean(U*K(s.eye(D)/D,sigma)*U.H);state=K(rho,s.eye(da)/da)
Bz=[clean(U*K(Z,I,I)*U.H),clean(U*K(I,Z,I)*U.H)]
Bx=[clean(U*K(X,I,I)*U.H),clean(U*K(I,X,I)*U.H)]
Zp=[Bz[0],clean(R(99,101)*Bz[1]+R(20,101)*Bx[0]*Bx[1])]
Xp=[clean(R(99,101)*Bx[0]+R(20,101)*Bz[0]),Bx[1]]
for b in Bx+Bz+Xp+Zp:assert zero(b*b-s.eye(dp)) and zero(b-b.H)
assert not zero(Zp[0]*Zp[1]-Zp[1]*Zp[0])
assert not zero(Xp[0]*Zp[0]+Zp[0]*Xp[0])
AX=[K(X,I),K(I,X)];AZ=[K(Z,I),K(I,Z)]
def forward(z,i):return K((s.eye(dp)+z)/2,s.eye(da))+K((s.eye(dp)-z)/2,AX[i])
def backward(x,i):return K(s.eye(dp),(s.eye(da)+AZ[i])/2)+K(x,(s.eye(da)-AZ[i])/2)
ideal=[];learned=[];expected=[];deltas=[]
for i in range(q):
 dz=tr(rho*(Bz[i]-Zp[i])**2);dx=tr(rho*(Bx[i]-Xp[i])**2);deltas.append({'logical_index':i,'delta_X':str(dx),'delta_Z':str(dz)})
 ideal.extend([forward(Bz[i],i),backward(Bx[i],i),forward(Bz[i],i)])
 learned.extend([forward(Zp[i],i),backward(Xp[i],i),forward(Zp[i],i)])
 expected.extend([dz/2,dx/2,dz/2])
Wi=s.eye(dp*da);Wl=s.eye(dp*da);records=[]
for k,(a,b,e) in enumerate(zip(ideal,learned,expected)):
 assert zero(a.H*a-s.eye(dp*da)) and zero(b.H*b-s.eye(dp*da))
 assert zero(a*state*a.H-state)
 gate_error=tr(state*(a-b).H*(a-b));assert gate_error==e
 Wi=clean(a*Wi);Wl=clean(b*Wl)
 assert zero(Wi*state*Wi.H-state)
 records.append({'gate':k,'squared_gate_error':str(gate_error),'ideal_prefix_invariant':True})
# Independent joint Bell fidelity via the Kraus trace formula after U encoding.
def fidelity(W):
 T=clean(W*K(U,s.eye(da)));ans=s.S(0)
 for gout in range(dp):
  for gin,p in enumerate([R(999,1000),R(1,1000)]):
   for ain in range(da):
    amp=sum(T[gout*da+l,(l*dg+gin)*da+ain] for l in range(D))
    ans+=p*s.expand(amp*s.conjugate(amp))/(da*D**2)
 return s.expand(ans)
assert fidelity(Wi)==1
F=fidelity(Wl);loss=1-F
hybrid=s.expand(2-2*s.re(tr(state*Wi.H*Wl)))
bound=3*q*sum(expected)
assert 0<=loss<=hybrid<=bound<1
# The special reduced-state invariance is generally lost for pure-|00> receiver initialization.
pureA=s.zeros(da);pureA[0,0]=1
assert not zero(ideal[0]*K(rho,pureA)*ideal[0].H-K(rho,pureA))
# Positive generator contractions alone do not imply identity-dominant joint Pauli noise.
pI=R(3,10);pXX=R(4,10);pZZ=R(3,10)
assert pI+pXX+pZZ==1 and 1-2*pXX>0 and 1-2*pZZ>0 and pXX>pI
# Exact two-qubit stabilizer ensemble: all 60 rank-one joint eigenspaces.
Y=s.Matrix([[0,-s.I],[s.I,0]])
paulis=[K(a,b) for a in (I,X,Y,Z) for b in (I,X,Y,Z)]
states={}
for a in range(1,16):
 for b in range(a+1,16):
  P,Q=paulis[a],paulis[b]
  if not zero(P*Q-Q*P):continue
  for sa in (-1,1):
   for sb in (-1,1):
    st=clean((s.eye(4)+sa*P)*(s.eye(4)+sb*Q)/4)
    assert tr(st)==1 and zero(st*st-st)
    states[tuple(st)]=st
assert len(states)==60
moment=sum((K(st,st) for st in states.values()),s.zeros(16))/60
swap=s.zeros(16)
for a in range(4):
 for b in range(4):swap[b*4+a,a*4+b]=1
assert zero(moment-(s.eye(16)+swap)/20)
# Nonunital joint channel: amplitude damping on one qubit, identity on the other.
ks=[K(s.diag(1,R(3,5)),I),K(s.Matrix([[0,R(4,5)],[0,0]]),I)]
assert zero(sum((a.H*a for a in ks),s.zeros(4))-s.eye(4))
Fe=sum(tr(a)*s.conjugate(tr(a)) for a in ks)/16
ordinary_error=sum(1-sum(tr(st*a*st*a.H) for a in ks) for st in states.values())/60
assert Fe==R(16,25) and ordinary_error==R(4,5)*(1-Fe)==R(36,125)
out={'status':'PASS','source_calls':0,'RNG_used':False,'logical_qubits':q,'physical_qubits':3,'gauge_eigenvalues':['999/1000','1/1000'],'learned_crosscommutation_exactly_false':True,'learned_within_pair_anticommutation_exactly_false':True,'deltas':deltas,'gate_checks':records,'joint_Bell_loss':str(loss),'purified_hybrid_squared_norm':str(hybrid),'displayed_joint_bound':str(bound),'ideal_joint_Bell_fidelity':'1','pure_receiver_ancilla_countercheck_noninvariant':True,'positive_generator_contrasts_do_not_imply_identity_dominance':True,'exact_two_qubit_stabilizer_states':len(states),'exact_projective_two_design':True,'nonunital_global_test_error':str(ordinary_error),'nonunital_global_Bell_loss':str(1-Fe),'kind':'exact prescribed joint-channel and gate checks, not an acquisition/source experiment'}
p=Path(__file__).with_suffix('.json');p.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(p.read_text(),end='')
