#!/usr/bin/env python3
"""Independent finite-matrix scattering audit for the reciprocal parity-pole design.
Numerical grids are diagnostics; rigorous error comes from rational interval script.
"""
from astra_reciprocal_parity_design_probe_20261026 import params
from astra_reciprocal_full_scattering_search_20261026 import Bp,scattering
import numpy as np
import json
from numpy.linalg import norm,eigvalsh
from math import pi,sqrt

E0=1.5;tau=1.1;gamma=1.0;chi=1800.0
P=params(str(tau),str(gamma));cs=np.array([(1.,1.),(1.,-1.)])/sqrt(2)
M=cs.T@np.diag([P[0]['bare'],P[1]['bare']])@cs
N=cs.T@np.diag([np.sqrt(P[0]['r']),np.sqrt(P[1]['r'])])
H=np.block([[M,N],[N.T,np.diag([P[0]['Omega'],P[1]['Omega']])]])

def fullS(E,shift=0.):
 V=sqrt(gamma)*E/np.sqrt(2)*np.array([[1,1],[np.exp(1j*tau*E),np.exp(-1j*tau*E)]],complex)
 Bmat=cs.T@np.diag([Bp(E,tau,1),Bp(E,tau,-1)])@cs
 D=E*np.eye(4,dtype=complex)-H
 D[:2,:2] += Bmat+1j*pi*V@V.conj().T -shift*np.eye(2)
 W=np.zeros((4,2),complex);W[:2,:]=V
 return np.eye(2)-2j*pi*W.conj().T@np.linalg.solve(D,W)

energies=np.linspace(1.452,1.548,801)
max_sel=max_unsel=max_identity=max_unit=0.
max_sel_R=max_unsel_R=0.
for E in energies:
 V=sqrt(gamma)*E/np.sqrt(2)*np.array([[1,1],[np.exp(1j*tau*E),np.exp(-1j*tau*E)]],complex)
 P_j=cs.T
 for shift in [0.,chi]:
  S=fullS(E,shift)
  vals=np.linalg.eigvals(S)
  target=scattering(E,tau,gamma,P) if shift==0 else None
  # Unitarity and equivalence to two scalar eigenvalues
  unit=norm(S.conj().T@S-np.eye(2),ord=2)
  max_unit=max(max_unit,float(unit))
  if shift==0:
   max_sel=max(max_sel,float(norm(S+np.eye(2),ord=2)))
   max_sel_R=max(max_sel_R,float(norm(S[:,0]+[1,0])))
   # Check the two eigenphases. sorting complex eigenvalues may be arbitrary
   max_identity=max(max_identity,min(max(abs(vals[0]-target[0]),abs(vals[1]-target[1])), max(abs(vals[1]-target[0]),abs(vals[0]-target[1]))))
  else:
   max_unsel=max(max_unsel,float(norm(S-np.eye(2),ord=2)))
   max_unsel_R=max(max_unsel_R,float(norm(S[:,0]-[1,0])))
# Energy form positivity direct 2x2 Schur, high-accuracy quadrature
from scipy.integrate import quad
Wpm=[quad(lambda x,p=p:x*(1+p*np.cos(tau*x)),0,2,epsabs=1e-12)[0] for p in (+1,-1)]
schur=[p['bare']-gamma*Wpm[i]-p['r']/p['Omega'] for i,p in enumerate(P)]
assert min(schur)>0 and max_unit<1e-11 and max_identity<1e-11
out={'model':'ordinary reciprocal bidirectional two-emitter waveguide with local complex conjugate forward/backward propagating phases',
     'parameters':{'tau':tau,'gamma':gamma,'halfbandwidth':.048,'chi':chi,'parity_poles':P},
     'minimum_true_schur':min(schur),'parity_schur':schur,
     'grid_selected_operator_error':max_sel, 'grid_unselected_operator_error':max_unsel,
     'grid_selected_right_incoming_error':max_sel_R,'grid_unselected_right_incoming_error':max_unsel_R,
     'max_unitarity_residual':max_unit,'max_4x4_vs_scalar_eigenphase_residual':max_identity,
     'scope':'Full four-internal-mode Hamiltonian, all physical forward/backward ports. Grids are numerical checks. Uniform theorem separately certified by rational script.'}
with open('/mnt/data/astra_reciprocal_full_hamiltonian_audit_20261026.json','w') as f:json.dump(out,f,indent=2)
print(json.dumps(out,indent=2))
