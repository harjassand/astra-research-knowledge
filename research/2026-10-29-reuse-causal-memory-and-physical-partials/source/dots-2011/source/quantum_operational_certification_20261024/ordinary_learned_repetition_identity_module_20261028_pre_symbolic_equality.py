#!/usr/bin/env python3
"""Exact source-disabled CP identity-component checks, including coherent memory."""
from pathlib import Path
import itertools,json,hashlib
import sympy as s
I=s.eye(2);X=s.Matrix([[0,1],[1,0]])
def kron(*args):
 r=s.ones(1,1)
 for a in args:r=s.kronecker_product(r,a)
 return r
def mm(a,b):
 z=s.zeros(2);z[a,b]=1;return z
Ls=[s.diag(s.Rational(3,5),s.Rational(4,5)),s.Matrix([[0,s.Rational(3,5)],[s.Rational(4,5),0]])]
assert sum((L.H*L for L in Ls),s.zeros(2))==I
p=s.symbols('p',real=True);r=3*p*p-2*p**3
assert s.diff(r,p)==6*p*(1-p) and s.expand(3*p*p-r)==2*p**3
# Native coherent logical-memory Choi matrices and explicit positive residual Kraus sums.
psmax=[s.Rational(1,100),s.Rational(1,10),s.Rational(1,4),s.Rational(49,100)]
bs=[s.Rational(0),s.Rational(1,1000),s.Rational(1,10)]
fixtures=[];entries=0
for pm,b in itertools.product(psmax,bs):
 ps=[pm/3,pm];rs=[3*t*t-2*t**3 for t in ps];rm=3*pm*pm-2*pm**3;eta=b+rm-b*rm
 assert rm<=3*pm*pm and all(0<=t<=rm for t in rs)
 for a,c,u,v in itertools.product(range(2),repeat=4):
  E=mm(a,c);om=mm(u,v);Ks=[L*om*L.H for L in Ls];T=sum(Ks,s.zeros(2))
  good=sum(((1-t)*K for t,K in zip(rs,Ks)),s.zeros(2));bad=sum((t*K for t,K in zip(rs,Ks)),s.zeros(2))
  exact=kron(E,good)+kron(X*E*X,bad)
  residual=kron(E,sum(((rm-t)*K for t,K in zip(rs,Ks)),s.zeros(2)))+kron(X*E*X,bad)
  assert exact==(1-rm)*kron(E,T)+residual;entries+=16
  # An actual complete CP learned-error channel: deliberately coherent joint-memory unitary.
  U=s.Matrix([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]])
  error=U*kron(E,T)*U.H
  learned=(1-b)*exact+b*error
  composedres=(1-b)*residual+b*error
  assert learned==(1-eta)*kron(E,T)+composedres;entries+=16
 # Trace factors on a complete basis, not only density inputs.
 for u,v in itertools.product(range(2),repeat=2):
  om=mm(u,v);Ks=[L*om*L.H for L in Ls]
  assert s.trace(sum(((rm-t)*K+t*K for t,K in zip(rs,Ks)),s.zeros(2)))==rm*s.trace(om)
 for J in [1,2,7,31]:
  w=(1-eta)**J;assert 0<=1-w<=J*eta
 fixtures.append({'p_max':str(pm),'b':str(b),'r_max':str(rm),'eta':str(eta)})
# Unencoded control noise may mask code suppression: a paid order-p replacement branch.
small=s.Rational(1,1000);native=3*small**2-2*small**3
assert small>100*native
out={'status':'PASS_COMPLETE_CP_IDENTITY_COMPONENT_AND_FINITE_ADAPTIVE_WEIGHT_ARITHMETIC',
 'source_outcomes':0,'rng_draws':0,'native_and_learned_complete_matrix_entries':entries,
 'coherent_state_dependent_memory_instrument':True,'actual_complete_residual_joint_unitary':'logical-memory SWAP',
 'fixtures':fixtures,'finite_horizons':[1,2,7,31],
 'scope':'exact map/decomposition fixtures; acquired uniform decoder certificate and arbitrary-controller composition imported from their received proofs',
 'sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),Path(__file__).with_suffix('.md')]}}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
