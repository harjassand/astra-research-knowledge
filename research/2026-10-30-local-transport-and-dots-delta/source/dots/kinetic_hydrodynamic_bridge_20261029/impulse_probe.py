"""Hydrodynamic forcing norm in the exact linearized 3-velocity collision model.
A spectral evaluation, not a continuum Boltzmann or rigorous interval certificate.
"""
import json
import numpy as np
from scipy.integrate import quad
from scipy.linalg import eig
from math import sqrt

a=sqrt(2/3);b=1/sqrt(3)
def A(k):return np.array([[0,-1j*k*a,0],[-1j*k*a,0,-1j*k*b],[0,-1j*k*b,-2]],complex)
def norm_integral(k):
    l,V=eig(A(k));coef=np.linalg.solve(V,np.array([0,0,1],complex));gap=-max(l.real)
    # Split early time and scale remaining integral by physical hydrodynamic rate.
    def f(t):return np.linalg.norm(V@(np.exp(l*t)*coef))
    early=quad(f,0,10,epsabs=1e-9)[0]
    # Fine oscillation can be bounded asymptotically; quadrature here reports errors.
    value,err=quad(lambda s:f(10+s/gap)/gap,0,30,epsabs=1e-7,limit=3000)
    return dict(k=k,gap=gap,gap_over_k2=gap/k**2,integral=early+value,k_times_integral=k*(early+value),quad_error=err,eigenvalues=[[float(z.real),float(z.imag)] for z in l])
print(json.dumps({'predicted_limit_k_times_L1_impulse':2*sqrt(3),'rows':[norm_integral(k) for k in [1,.3,.1,.03,.01]]},indent=2))
