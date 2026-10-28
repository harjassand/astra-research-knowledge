#!/usr/bin/env python3
"""Exact contact/normalization identities and complete ordinary QC control."""
from pathlib import Path
import json,time
import sympy as s

start=time.perf_counter()
OUT=Path(__file__).resolve().parent
av=s.symbols('a0:4',real=True)
xv=s.symbols('x0:4',real=True)
bv=s.symbols('b0:4',real=True)
A=s.Matrix(2,2,av);X=s.Matrix(2,2,xv);B=s.Matrix(2,2,bv)
T=sum(v*v for v in av);R=sum(v*v for v in xv);inner=sum(a*x for a,x in zip(av,xv))
q=A.det()
def sub(poly,values):return s.expand(poly.subs(dict(zip(av,list(values))),simultaneous=True))
def breg(poly,base,inc):
    grad=s.Matrix([s.diff(poly,aa) for aa in av])
    return s.expand(sub(poly,base+inc)-sub(poly,base)-sum(sub(grad[i],base)*inc[i] for i in range(4)))

# Quartic Bregman expansion verified on all 35 homogeneous monomials.
monomials=[]
for aa in range(5):
 for bb in range(5-aa):
  for cc in range(5-aa-bb):
   dd=4-aa-bb-cc
   monomials.append(av[0]**aa*av[1]**bb*av[2]**cc*av[3]**dd)
t=s.symbols('t',real=True)
for mm in monomials:
    line=sub(mm,A+t*X)
    expected=s.diff(line,t,2).subs(t,0)/2+s.diff(line,t,3).subs(t,0)/6+sub(mm,X)
    assert s.expand(breg(mm,A,X)-expected)==0

# Recenter an actual shifted transported known QC polynomial.
P=s.Matrix([[2,1],[1,1]]);S=s.Matrix([[1,2],[0,1]])
shift=s.Matrix([[1,-2],[1,0]])
M=P*(A-shift)*S
tm=sum(mm*mm for mm in M);qm=M.det()
H=s.expand(tm*tm-s.Rational(9,4)*tm*qm)
A0=s.Matrix([[1,0],[0,0]])
HA=sub(H,A-B+A0)
assert s.expand(breg(HA,B,X)-breg(H,A0,X))==0

# General complex-spinor/Hopf fidelity identity (no unit assumption).
def hopf(M):
    a,b,c,d=list(M)
    return s.Matrix([a*a+c*c-b*b-d*d,2*(a*b+c*d),2*(a*d-b*c)])
TB=sum(bb*bb for bb in bv)
complex_real=sum(aa*bb for aa,bb in zip(av,bv))
complex_imag=av[0]*bv[2]-av[2]*bv[0]+av[1]*bv[3]-av[3]*bv[1]
assert s.expand(2*(complex_real**2+complex_imag**2)-T*TB-(hopf(A).T*hopf(B))[0])==0

# Global strict-contact control, not merely a finite sample of centers.
norm4=T*T
wedge=sum((av[i]*xv[j]-av[j]*xv[i])**2 for i in range(4) for j in range(i+1,4))
remainder=breg(norm4,A,X)-s.Rational(1,4)*(T*R+R*R)
certificate=(s.Rational(7,4)*wedge+s.Rational(23,4)*inner*inner
             +4*inner*R+s.Rational(3,4)*R*R)
assert s.expand(remainder-certificate)==0
small=s.Matrix([[s.Rational(23,4),2],[2,s.Rational(3,4)]])
assert small[0,0]>0 and small.det()==s.Rational(5,16)>0

# QC of DM gamma=9/8 is an established primary-source input.
gamma=s.Rational(9,8);epsilon=s.Rational(1,100)
assert gamma*gamma<s.Rational(4,3)
DM=T*T-2*gamma*T*q
F_control=DM+epsilon*T*T
assert s.expand(breg(F_control,A,X)-breg(DM,A,X)-epsilon*breg(norm4,A,X))==0
assert sum(abs(coef) for coef in s.Poly(norm4,*av).coeffs())==16

data={'status':'EXACT_CONTACT_IDENTITIES_AND_ORDINARY_CONTROL_PASS',
      'quartic_monomials_checked':35,'recenter_identity':'PASS',
      'Hopf_complex_fidelity_identity':'PASS',
      'global_norm4_margin_quadratic':'1/4','global_norm4_margin_quartic':'1/4',
      'positive_residual_2x2_determinant':'5/16',
      'ordinary_QC_control':'DM_gamma9/8 + norm4/100',
      'ordinary_control_model':'H=DM_gamma9/8 at every A',
      'ordinary_control_unit_quadratic_margin':'1/400',
      'ordinary_control_quartic_margin':'1/400',
      'target_contact':'NOT_ACQUIRED_BY_THIS_WORKER',
      'target_full_QC':'UNKNOWN','runtime_seconds':time.perf_counter()-start}
(OUT/'CONTACT_IDENTITY_REPLAY.json').write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps(data,indent=2))
