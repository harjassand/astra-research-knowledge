#!/usr/local/bin/python3
"""Infinite-ladder response to V=n_L-n_R, retaining complete endpoint measures.

All quadratures are continuum quadratures; no finite chain is used here.
See PROOF.md for the rank-one hard-core reduction and normalization.
"""
from __future__ import annotations
import json
import math
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

ROOT = Path(__file__).resolve().parent

class Channel:
    def __init__(self, center, coupling_squared, tol=2e-12):
        self.c = float(center)
        self.a = float(coupling_squared)
        self.tol = tol
        interval = (2.8, 3.0) if center == 5 else (3.0, 3.1)
        self.b = brentq(lambda x: 3-x-self.a*self.surface(x).real,
                        *interval, xtol=5e-15)
        self.w = 1/(1+self.a*self.surface_prime(self.b))

    def surface(self, z):
        """Boundary value <0,(h_bath-z-i0)^-1 0>."""
        if not isinstance(z, complex):
            u = z-self.c
            if abs(u) <= 1:
                return complex(-2*u, 2*math.sqrt(max(0., 1-u*u)))
            return complex(2*(-u+math.copysign(math.sqrt(u*u-1),u)))
        u=z-self.c
        root=np.sqrt(u*u-1)
        if root.imag < 0: root=-root
        return 2*(-u+root)

    def surface_prime(self, z):
        u=z-self.c
        assert abs(u)>1
        return -2+2*abs(u)/math.sqrt(u*u-1)

    def m(self,z):
        return 1/(3-z-self.a*self.surface(z))

    def mp(self,z):
        return (1+self.a*self.surface_prime(z))*self.m(z).real**2

    def density(self,x):
        u=x-self.c
        if abs(u)>=1: return 0.
        s=math.sqrt(1-u*u)
        return 2*self.a*s/(math.pi*((3-x+2*self.a*u)**2+4*self.a*self.a*s*s))

    def cont_integral(self,fun,points=()):
        """x=c+cos(theta) removes the endpoint square roots."""
        theta_points=sorted(math.acos(x-self.c) for x in points
                            if self.c-1<x<self.c+1)
        def integrand(theta):
            x=self.c+math.cos(theta)
            return self.density(x)*math.sin(theta)*fun(x)
        real, er=quad(lambda t: complex(integrand(t)).real,0,math.pi,
                     points=theta_points,epsabs=self.tol,epsrel=self.tol,limit=300)
        imag, ei=quad(lambda t: complex(integrand(t)).imag,0,math.pi,
                     points=theta_points,epsabs=self.tol,epsrel=self.tol,limit=300)
        return complex(real,imag), er+ei

    def integral(self,fun,points=()):
        val,err=self.cont_integral(fun,points)
        return self.w*fun(self.b)+val,err

    def L(self,E):
        return self.integral(lambda x:self.m(E-x).real)[0].real

    def Lp(self,E):
        return self.integral(lambda x:self.mp(E-x))[0].real


def calculate(g=.2,tol=2e-12):
    p=Channel(5,2*g*g,tol)
    m=Channel(1,g*g,tol)
    E=brentq(lambda E:p.L(E)+m.L(E),2*p.b+1e-10,2*m.b-1e-10,
             xtol=5e-15)
    Lp,Lm=p.L(E),m.L(E)
    deriv=p.Lp(E)+m.Lp(E)
    C=math.sqrt(2/deriv)

    # D=<q,R_0(E+i0)q>; B=<q,R_0(E+i0)f>.
    D,Derr=p.integral(lambda x:m.m(E-x),[E,E-2])
    B1,B1err=p.integral(lambda x:p.m(E-x).real*m.m(E-x),[E,E-2])
    B2,B2err=m.integral(lambda y:m.m(E-y).real*p.m(E-y),[E-6,E-4])
    B=C*(B1+B2)
    alpha=B/D

    left=max(4.,E-2)
    right=min(6.,E)
    def source_shell(x):
        return C*(p.m(E-x).real+m.m(x).real)
    def shell_integrate(fun):
        val,err=quad(lambda x:p.density(x)*m.density(E-x)*fun(x),
                     left,right,epsabs=tol*1e-6,epsrel=tol,limit=300)
        return val,err
    rho,rhoerr=shell_integrate(lambda x:abs(source_shell(x)-alpha)**2)
    w0,w0err=shell_integrate(lambda x:1.)
    w1,w1err=shell_integrate(source_shell)
    w2,w2err=shell_integrate(lambda x:source_shell(x)**2)
    variance=w2-w1*w1/w0
    # Every constant alpha obeys rho >= weighted_variance.
    samples={str(x):source_shell(x) for x in np.linspace(left,right,9)}

    def cmplx(z): return {"real":z.real,"imag":z.imag}
    result={
        "g":g,"quadrature_tolerance":tol,
        "one_body_plus":{"bound_energy":p.b,"bound_weight":p.w,
                         "total_mass":p.integral(lambda x:1.)[0].real},
        "one_body_minus":{"bound_energy":m.b,"bound_weight":m.w,
                          "total_mass":m.integral(lambda x:1.)[0].real},
        "pair_energy":E,"pair_equation_residual":Lp+Lm,
        "connected_shift":E-p.b-m.b,
        "pair_normalization_C":C,"bare_pair_weight":-2*Lp*Lm/deriv,
        "D":cmplx(D),"D_quadrature_error_estimate":Derr,
        "B":cmplx(B),"B_quadrature_error_estimate":C*(B1err+B2err),
        "alpha":cmplx(alpha),"shell_interval":[left,right],
        "rho":rho,"rho_quadrature_error_estimate":rhoerr,
        "free_shell_mass":w0,"shell_source_mean":w1/w0,
        "weighted_variance_lower_bound":variance,
        "variance_moment_error_estimates":[w0err,w1err,w2err],
        "optical_identity_residual_D":D.imag-math.pi*w0,
        "optical_identity_residual_B":B.imag-math.pi*w1,
        "source_shell_samples":samples,
        "convention":"rho=(1/pi) Im <f,(H_odd-E-i0)^-1 f>; hbar=1",
        "scope":"continuum quadrature with analytic positivity proof; quadrature error estimates are not interval certificates"
    }
    return result

if __name__=="__main__":
    out={"runs":[calculate(.2,t) for t in (2e-10,2e-12,2e-13)]}
    (ROOT/"continuum_results.json").write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(out,indent=2))
