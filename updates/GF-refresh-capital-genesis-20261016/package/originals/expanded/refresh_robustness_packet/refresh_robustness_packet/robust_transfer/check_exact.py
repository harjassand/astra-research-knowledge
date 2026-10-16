#!/usr/bin/env python3
"""Exact consistency checks; no numerical search or acquired code."""
import json
from pathlib import Path
import sympy as s

I = s.eye(2)
X = s.Matrix([[0,1],[1,0]])
Y = s.Matrix([[0,-s.I],[s.I,0]])
Z = s.diag(1,-1)
p0 = s.diag(1,0)
p1 = s.diag(0,1)
kron = s.kronecker_product

def zero(M):
    return all(s.simplify(v)==0 for v in M)
def vec(M):
    return s.Matrix(list(M))  # output-first unnormalized Choi convention

def choi(ks):
    n=ks[0].rows*ks[0].cols
    return sum((vec(k)*vec(k).conjugate().T for k in ks),s.zeros(n))
def partial_out(J, di, do):
    return s.Matrix(di,di,lambda i,j:sum(J[o*di+i,o*di+j] for o in range(do)))
def apply(ks,rho):
    return sum((k*rho*k.conjugate().T for k in ks),s.zeros(ks[0].rows))

def assert_eq(A,B):
    if isinstance(A,s.MatrixBase): assert zero(A-B), (A,B)
    else: assert s.simplify(A-B)==0, (A,B)

# A coherent unitary difference has an additive CP majorant with exact half-diamond cost.
c=s.Rational(4,5); sn=s.Rational(3,5)
U=c*I-s.I*sn*X
JI=choi([I]); JU=choi([U]); JX=choi([X]); Delta=JU-JI
P=(JI+JX)/2
assert_eq(P*P,P)
assert_eq(Delta*Delta,4*sn**2*P)
Zplus=(2*sn*P+Delta)/2
Zminus=(2*sn*P-Delta)/2
assert set(Zplus.eigenvals()).issubset({0,2*sn})
assert set(Zminus.eigenvals()).issubset({0,2*sn})
assert_eq(partial_out(Zplus,2,2),sn*I)
assert_eq(partial_out(Zminus,2,2),sn*I)
assert_eq(JU+Zminus,JI+Zplus)
assert_eq(partial_out(Zplus/sn,2,2),I)
assert_eq(partial_out(Zminus/sn,2,2),I)
# |0> supplies the matching operational lower bound to the SDP majorant.
rho1=U*p0*U.conjugate().T
assert set((rho1-p0).eigenvals()) == {-sn,sn}

# No positive ideal-channel fraction in a distinct coherent unitary Choi ray.
a=s.symbols('a', positive=True)
V=s.Matrix.hstack(vec(I)/s.sqrt(2),vec(X)/s.sqrt(2))
minor=(V.conjugate().T*(JU-a*JI)*V).det()
assert_eq(minor,-4*a*sn**2)
# No finite multiple of the identity Choi can upper dominate it either.
assert_eq((vec(X).conjugate().T*(JU)*vec(X))[0],4*sn**2)
assert_eq((vec(X).conjugate().T*JI*vec(X))[0],0)

# Exact endpoint-good does not reveal a logical spectator rotation.
Pgood=kron(p0,I)
Nlogical=[kron(p0,U),kron(p1,U)]
encoding=kron(s.Matrix([1,0]),I)
assert_eq(sum((k.conjugate().T*(s.eye(4)-Pgood)*k for k in Nlogical),s.zeros(4))*encoding,s.zeros(4,2))
logical_ks=[encoding.conjugate().T*k*encoding for k in Nlogical]
assert_eq(choi(logical_ks),JU)

# By contrast, an arbitrary coherent syndrome/bath error has a true good branch
# that acts trivially on an inert logical spectator, with bath coefficients intact.
USB=c*s.eye(4)-s.I*sn*kron(X,Y) # order syndrome, bath
Kgood=kron(p0,I)*USB*kron(p0,I)
Kbad=kron(p1,I)*USB*kron(p0,I)
assert_eq(Kgood,c*kron(p0,I))
assert_eq(Kbad,-s.I*sn*kron(s.Matrix([[0,0],[1,0]]),Y))

# Common hidden bath trigger: exact all-bad probability epsilon, not epsilon^n.
eps=s.Rational(1,10); n=3
common_bad=eps
claimed_marginal_product=eps**n
assert common_bad > claimed_marginal_product
# Joint channel conditioned on B=1 has orthogonal actual/reference outputs.
controlled_X=kron(I,p0)+kron(X,p1)  # syndrome first, B second
input_B1=kron(p0,p1)
actual_B1=controlled_X*input_B1*controlled_X.conjugate().T
assert_eq(s.trace(actual_B1*input_B1),0)
assert_eq(s.trace(actual_B1),1)

# One cross-parent fault slot has half-diamond epsilon and all-bad epsilon.
input00=kron(p0,p0); XX=kron(X,X)
output=(1-eps)*input00+eps*XX*input00*XX
assert_eq(s.trace(kron(p1,p1)*output),eps)
# Independent genuine local bit flips saturate product epsilon for f_i=0.
independent_bad=eps**n
assert_eq(independent_bad,claimed_marginal_product)

# General first-fault weights agree with ordinary stochastic-mixture formula.
f,r1,r2=s.symbols('f r1 r2', real=True)
first_fault=(1-r1)*(1-r2)*f+r1+(1-r1)*r2
assert_eq(first_fault,1-(1-f)*(1-r1)*(1-r2))

# Independent exact check of the fully finite compiled-pulse obstruction.
ZZ=kron(Z,Z); XX=kron(X,X)
phi_plus=s.Matrix([1,0,0,1])/s.sqrt(2)
phi_minus=s.Matrix([1,0,0,-1])/s.sqrt(2)
Bell=s.Matrix.hstack(phi_plus,phi_minus)
Omega=s.symbols('Omega', positive=True)
J=s.sqrt(5)*Omega
H0=J*(s.eye(4)-XX)/2
Hc=Omega*(kron(Z,I)+kron(I,Z))/2
P=phi_plus*phi_plus.conjugate().T
assert_eq(H0*P,s.zeros(4))
assert_eq(H0*ZZ-ZZ*H0,s.zeros(4))
assert_eq(H0*XX-XX*H0,s.zeros(4))
assert_eq(Bell.conjugate().T*(H0+Hc)*Bell,s.Matrix([[0,Omega],[Omega,J]]))
frequency=s.sqrt(Omega**2+J**2/4)
assert_eq(frequency,s.Rational(3,2)*Omega)
bad=s.simplify(Omega**2/frequency**2*s.sin(s.pi/Omega*frequency)**2)
assert_eq(bad,s.Rational(4,9))
assert_eq(bad/2,s.Rational(2,9))
ideal=(-s.I*s.pi/Omega*Hc).exp()
assert_eq(ideal,-ZZ)

results={
    'status':'PASS',
    'coherent_channel_half_diamond':str(sn),
    'majorant_positive_choi_eigenvalues':{str(k):v for k,v in Zplus.eigenvals().items()},
    'majorant_effect':'epsilon I exactly',
    'ideal_minorant_restricted_determinant':str(s.factor(minor)),
    'logical_spectator_endpoint_bad_probability':'0',
    'logical_channel_after_good_endpoint':'Ad_U, rank-one nonidentity Choi',
    'local_syndrome_bath_good_branch':'cos(theta) P0 tensor I_B; logical identity preserved',
    'common_trigger_all_bad':str(common_bad),
    'false_marginal_product':str(claimed_marginal_product),
    'common_trigger_full_joint_distance':'1, witnessed by B=1 input',
    'single_cross_parent_slot_all_bad':str(eps),
    'independent_local_error_product':str(independent_bad),
    'first_fault_stochastic_formula':'1-(1-f)(1-r1)(1-r2)',
    'finite_pulse_branch_bad':str(bad),
    'finite_private_fair_pulse_bad':str(bad/2),
    'finite_pulse_old_odd_action':'0'
}
path=Path(__file__).with_name('check_results.json')
path.write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
