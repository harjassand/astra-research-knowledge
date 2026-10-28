#!/usr/bin/env python3
"""Exact finite-Choi repair/constant checks; no optimizer or source sampler invoked."""
import itertools,json
from pathlib import Path
import sympy as s
R=s.Rational; I=s.eye(2); X=s.Matrix([[0,1],[1,0]]); Z=s.diag(1,-1)
K=s.kronecker_product;d=2
v=s.Matrix([1,0,0,1]);Jstar=v*v.T;J0=s.eye(4)/2
C=-R(3,5)*(K(X,X.T)+K(Z,Z.T))/8
trout=lambda A:A[:2,:2]+A[2:,2:]
assert trout(Jstar)==I and s.trace(Jstar)==d
assert s.Rational(1,2)+s.trace(C*Jstar)==R(1,5)
rows=[]
for exponent in (12,16,24,40):
 delta=R(1,2**exponent);zeta=128*d*delta
 Jtilde=Jstar+delta*(K(X,Z)+K(Z,I)-s.eye(4))/4
 assert trout(Jtilde)-I==-delta*I/2
 # Each perturbation summand has norm one; lambda_min >= -3delta/4 >= -delta.
 Jhat=Jtilde+K(I/2,I-trout(Jtilde))
 Jphys=(Jhat+4*delta*J0)/(1+4*delta)
 assert trout(Jhat)==I and trout(Jphys)==I and Jphys==Jphys.H
 floor=delta/(2*(1+4*delta))
 for size in range(1,5):
  for ix in itertools.combinations(range(4),size):
   assert Jphys.extract(ix,ix).det()>0
   assert (Jphys-floor*s.eye(4)).extract(ix,ix).det()>=0
 loss=s.expand(s.trace(C*(Jphys-Jstar)))
 assert s.trace(C*(Jtilde-Jstar))==0
 assert 0<=loss<zeta
 diff=Jphys-Jtilde
 assert 4*s.trace(diff.H*diff)<=(9*d*delta)**2 # trace norm <=2 Frobenius norm
 assert R(9,2)*d*delta<=R(9,256)*zeta
 rows.append({'delta':str(delta),'zeta':str(zeta),'repair_objective_increase':str(loss),'certified_Choi_floor':str(floor)})
assert R(22,32768)<R(1,640)
assert 2*R(22,32768)+R(1,320)<R(1,160)
assert 8*(2*R(22,32768)+R(1,320))<R(1,20)
assert R(1,4)+R(9,256)<1
out={'status':'PASS','source_calls':0,'source_sampler_executed':False,'optimizer_invoked':False,'kind':'exact prescribed rational Choi repair and scalar constant checks; not an ERM acquisition experiment','Choi_input_dimension':2,'cases':rows,'positive_definite_and_exact_TP_all_cases':True,'explicit_floor_verified_all_principal_minors':True,'repair_objective_and_tournament_constants':True}
p=Path(__file__).with_suffix('.json');p.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(p.read_text(),end='')
