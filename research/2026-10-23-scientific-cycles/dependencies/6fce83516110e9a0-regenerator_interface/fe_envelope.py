"""Next15 source-calibrated reversible FE envelope, per ONE bank area.
This is not a measured equilibrium potential and contains NO qualified loss.
Independent optical gates are excluded; they need their own charge/control.
"""
import numpy as np
N=10;ELL=260e-9;TR=343.;VMAX=23.27;CV=8.708;P=-.004827
COEFF=np.array([0.06145871741742188, 0.1942907523878507, 6.834114672101084, 0.007830072552565962])
def qref(v):
 a,b,z,c=COEFF;return N*(a+b*np.tanh(np.asarray(v)/z)+c*np.asarray(v))
def cref(v):
 a,b,z,c=COEFF;return N*(b/z/np.cosh(np.asarray(v)/z)**2+c)
def intqref(v):
 a,b,z,c=COEFF;v=np.asarray(v);return N*(a*v+b*z*np.log(np.cosh(v/z))+.5*c*v*v)
def G(T,V,Cv=CV):return -Cv*(T*np.log(T/TR)-T+TR)-P*(T-TR)*V-intqref(V)
def Q(T,V):return qref(V)+P*(T-TR)
def S(T,V,Cv=CV):return Cv*np.log(T/TR)+P*V
def U(T,V,Cv=CV):return G(T,V,Cv)+T*S(T,V,Cv)+V*Q(T,V)
def c_fixed_charge(T,V,Cv=CV):return Cv-T*P*P/cref(V)
def rhs(T,V,current_into,heat_into,working_dissipation=0.,Cv=CV):
 # Cv*Tdot+T*P*Vdot=heat_into+working_dissipation;
 # P*Tdot+cref(V)*Vdot=current_into (subtract leakage separately).
 C=cref(V);D=Cv*C-T*P*P;q=heat_into+working_dissipation
 return (C*q-T*P*current_into)/D,(-P*q+Cv*current_into)/D
