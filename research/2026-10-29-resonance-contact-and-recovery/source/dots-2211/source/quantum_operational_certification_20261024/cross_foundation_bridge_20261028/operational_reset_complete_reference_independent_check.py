#!/usr/bin/env python3
"""Exact full-qubit quotient reset, nonunit raw masses, entangled reference, selection boundary."""
from pathlib import Path
import json,itertools
import sympy as s
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1)
rhos=[(I+Z)/2,(I+s.Rational(3,5)*X+s.Rational(4,5)*Z)/2,(I+s.Rational(3,5)*Y+s.Rational(4,5)*Z)/2,(I+(X+Y)/5+3*Z/5)/2]
m=s.Matrix([[1,s.Rational(1,2),s.Rational(1,3),s.Rational(1,4)]])
tau=[m[j]*rhos[j] for j in range(4)];effects=[I,(I+Z)/2,(I+X)/2,(I+Y)/2]
H=s.Matrix(4,4,lambda i,j:s.trace(effects[i]*tau[j]));assert H.det()!=0
Hi=H.inv();K=sum(abs(x) for x in Hi);q=s.Rational(1,4)
Psi=lambda A:q*A+(1-q)*I*s.trace(A)/2
HR=s.Matrix(4,4,lambda i,j:s.trace(effects[i]*Psi(tau[j])));C=s.simplify(Hi*HR)
assert m*C==m
W=s.Matrix(4,3,lambda i,j:-m[j+1] if i==0 else int(i==j+1));E=s.eye(4)[1:,:]
D=s.simplify(E*C*W);assert D==q*s.eye(3) and m*W==s.zeros(1,3) and s.simplify(C*W-W*D)==s.zeros(4,3)
v=Hi*s.Matrix([s.trace(F*I/2) for F in effects]);assert C*v==v and m*v==s.ones(1,1) and any(x<0 for x in v)
# Pi on Bell memory/reference retains genuinely nonclassical correlations.
phi=s.Matrix([1,0,0,1])/s.sqrt(2);Omega=phi*phi.H
ptrM=lambda A:s.Matrix(2,2,lambda i,j:sum(A[2*b+i,2*b+j] for b in range(2)))
blocks=[ptrM(s.kronecker_product(F,I)*Omega) for F in effects]
coords=[sum((Hi[i,j]*blocks[j] for j in range(4)),s.zeros(2)) for i in range(4)]
assert sum((m[j]*coords[j] for j in range(4)),s.zeros(2))==I/2
reconstructed=sum((s.kronecker_product(tau[j],coords[j]) for j in range(4)),s.zeros(4));assert s.simplify(reconstructed-Omega)==s.zeros(4)
negative_blocks=sum(any(ev<0 for ev in A.eigenvals()) for A in coords);assert negative_blocks>0
horizons=[]
for t in range(9):
 coeff=C**t;xt=[sum((coeff[i,j]*coords[j] for j in range(4)),s.zeros(2)) for i in range(4)]
 actual=sum((s.kronecker_product(tau[j],xt[j]) for j in range(4)),s.zeros(4));ideal=s.eye(4)/4
 actual=s.simplify(actual);assert s.simplify(actual-q**t*Omega-(1-q**t)*ideal)==s.zeros(4)
 half=s.simplify(sum(abs(a)*b for a,b in (actual-ideal).eigenvals().items())/2);assert half==s.Rational(3,4)*q**t
 horizons.append({'t':t,'actual_complete_reference_error':str(half),'certificate':str(min(1,2*K*q**t))})
# Explicit simultaneous interval certificate with nontrivial trace-row uncertainty.
h=s.Rational(1,100000);mh=m+s.Matrix([[0,h,-h,h]]);Ch=C+s.Matrix(4,4,lambda i,j:h*(-1)**(i+j));F=s.ones(4)*h;d=[0,h,h,h]
Dh=s.Matrix(3,3,lambda i,j:Ch[i+1,j+1]-Ch[i+1,0]*mh[j+1]);B=s.Matrix(3,3,lambda i,j:F[i+1,j+1]+F[i+1,0]+abs(Ch[i+1,0])*d[j+1])
assert all(abs(D[i,j]-Dh[i,j])<=B[i,j] for i,j in itertools.product(range(3),repeat=2))
cert=max(sum(abs(Dh[i,j])+B[i,j] for i in range(3)) for j in range(3));assert q<=cert<1
# Data-dependent word selection: perfect replacers have c=0 but different limits.
selected=s.diag(s.Rational(1,2),0,0,s.Rational(1,2));product=s.eye(4)/4
selection_error=sum(abs(a)*b for a,b in (selected-product).eigenvals().items())/2;assert selection_error==s.Rational(1,2)
out={'status':'PASS_COMPLETE_REFERENCE_QUOTIENT_RESET_AND_SELECTION_BOUNDARY','source_draws':0,'rng_draws':0,'rank':4,'raw_trace_row':str(m),'K':str(K),'D':str(D),'signed_stationary_coordinate':str(v),'negative_operator_coordinate_blocks':negative_blocks,'entangled_reference_horizons':horizons,'interval_certificate_with_trace_uncertainty':str(cert),'selected_replacer_limit_record_correlation_half_distance':str(selection_error),'scope':'Exact finite-qubit identities. An appended invisible shift counter is an analytic extension, not simulated infinite memory.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
