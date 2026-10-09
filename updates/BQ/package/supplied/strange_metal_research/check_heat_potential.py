#!/usr/bin/env python3
"""Independent 1D BVP checks of the heat-potential/noise identities.

No experimental data are used. kappa(T)*rho(T)=(1+T)^p in dimensionless units.
The analytical proof in RESEARCH_NOTE.md also covers the stated continuum
geometries with aligned electrical/thermal tensors and no bulk heat leak.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
from scipy.integrate import quad, simpson, solve_bvp
import sympy as sp


def potential(T, p):
    return ((1.0 + T)**(p+1.0)-1.0)/(p+1.0)


def inverse_potential(W, p):
    return (1.0+(p+1.0)*W)**(1.0/(p+1.0))-1.0


def N_formula(V: float, T: float, p: float) -> float:
    W0 = potential(T, p)
    return quad(lambda s: inverse_potential(W0+0.5*V*V*s*(1-s),p),
                0.0, 1.0, epsabs=1e-12, epsrel=1e-12)[0]


def solve_direct(V: float, Tb: float, p: float) -> dict:
    # rho and kappa are entered separately into the spatial ODE.
    def rho(T): return 2.0 + 0.7*T
    def kap(T): return (1.0+T)**p/rho(T)
    x = np.linspace(0.0,1.0,120)
    j0 = V/rho(Tb)
    dT = V*V/(2.0*(1.0+Tb)**p)
    initial = np.array([Tb+dT*x*(1-x), j0*j0*rho(Tb)*(x-0.5), V*x])

    def ode(x,y,par):
        T,Q,phi=y; j=par[0]
        return np.array([-Q/kap(T), j*j*rho(T), j*rho(T)])
    def bc(ya,yb,par):
        return np.array([ya[0]-Tb,yb[0]-Tb,ya[2],yb[2]-V])
    sol=solve_bvp(ode,bc,x,initial,p=[j0],tol=1e-8,max_nodes=10000)
    if not sol.success:
        raise RuntimeError(sol.message)
    xx=np.linspace(0,1,4001); T,Q,phi=sol.sol(xx); j=sol.p[0]
    # Terminal Johnson temperature calculated from local Joule weights.
    N=simpson(T*rho(T),x=xx)/simpson(rho(T),x=xx)
    NN=N_formula(V,Tb,p)
    invariant=potential(T,p)-potential(Tb,p)-0.5*phi*(V-phi)
    return {'p':p,'Tb':Tb,'V':V,'N_from_spatial_BVP':float(N),
            'N_from_noise_integral':NN,'N_absolute_error':abs(N-NN),
            'heat_potential_max_residual':float(np.max(np.abs(invariant))),
            'R_from_BVP':float(V/j),'mesh_nodes':int(sol.x.size)}


def main():
    runs=[solve_direct(V,T,p) for p in [-0.5,0.0,1.0,2.3]
          for T in [0.7,2.0] for V in [0.2,1.5,4.0]]
    assert max(r['N_absolute_error'] for r in runs)<2e-7
    pde=[]
    for p in [-0.5,0.0,1.0,2.3]:
        for T in [0.7,2.0]:
            for V in [0.2,1.5,4.0]:
                hv=1e-4*max(V,1); ht=1e-4*max(T,1)
                N=N_formula(V,T,p)
                dV=(N_formula(V+hv,T,p)-N_formula(V-hv,T,p))/(2*hv)
                dT=(N_formula(V,T+ht,p)-N_formula(V,T-ht,p))/(2*ht)
                A=1/(12*(1+T)**p)
                lhs=V*dV+N-T; rhs=3*A*V*V*dT
                pde.append(abs(lhs-rhs)/(1+abs(lhs)))
    assert max(pde)<1e-7
    # Symbolically confirm the first coefficients of the moment hierarchy.
    T=sp.symbols('T', positive=True); w=sp.Function('w')(T)
    A=1/(12*w)
    B=sp.simplify(sp.Rational(3,5)*A*sp.diff(A,T))
    C=sp.simplify(sp.Rational(3,7)*A*sp.diff(B,T))
    expected_B=-sp.diff(w,T)/(240*w**3)
    expected_C=(3*sp.diff(w,T)**2-w*sp.diff(w,T,2))/(6720*w**5)
    assert sp.simplify(B-expected_B)==0 and sp.simplify(C-expected_C)==0
    out={'status':'Synthetic BVP and symbolic checks; not empirical evidence.',
         'BVP_cases':len(runs),'max_noise_absolute_error':max(r['N_absolute_error'] for r in runs),
         'max_scaled_PDE_finite_difference_residual':max(pde),
         'coefficients':{'V2':'A(T)=1/[12*w(T)]','V4':str(B),'V6':str(C),
                         'recursion':'c_(n+1)=3*A(T)*d(c_n)/dT/(2*n+3), c_0=T'},
         'runs':runs}
    dest=Path(__file__).resolve().parent/'results'/'heat_potential_checks.json'
    dest.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='runs'},indent=2))

if __name__=='__main__': main()
