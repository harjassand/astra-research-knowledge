#!/usr/local/bin/python3
"""Infinite-volume local-parity-breaking response for the supplied ladder.

The analytical classification is proved in PROOF.md. This file evaluates the
complete one-body measures, the exact even pair, and the odd rank-one formula.
Floating-point quadrature results are diagnostics, not interval certificates.
"""
import json
import math
from dataclasses import dataclass
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

PI = math.pi

@dataclass
class Measure:
    center: float
    lam2: float
    epsabs: float = 2e-12
    epsrel: float = 2e-12

    def __post_init__(self):
        d = 3.0 - self.center
        self.atom = 3.0 + 2*self.lam2*(d-math.copysign(math.sqrt(d*d-1+4*self.lam2),d))/(1-4*self.lam2)
        self.weight = float(1/(1-self.lam2*self.mp(self.atom)).real)

    def m(self, z):
        t = np.asarray(z, dtype=complex)-self.center
        # Product of principal square roots has the correct Stieltjes branch.
        root = np.sqrt(t-1)*np.sqrt(t+1)
        # Reciprocal form prevents cancellation at large argument.
        return 2/(t+root)

    def mp(self,z):
        t = complex(z)-self.center
        root = np.sqrt(t-1+0j)*np.sqrt(t+1+0j)
        return -2/(root*(t+root))

    def r(self,z):
        """<memory,(h-z)^(-1) memory>; positive imaginary part above R."""
        return 1/(3-z+self.lam2*self.m(z))

    def rp(self,z):
        return (1-self.lam2*self.mp(z))*self.r(z)**2

    def density(self,x):
        t = x-self.center
        if abs(t) >= 1:
            return 0.0
        v = math.sqrt(max(0.0,1-t*t))
        a = 3-x+2*self.lam2*t
        return 2*self.lam2*v/(PI*(a*a+4*self.lam2**2*v*v))

    def theta_weight(self,theta):
        t=math.cos(theta)
        x=self.center+t
        a=3-x+2*self.lam2*t
        return 2*self.lam2*math.sin(theta)**2/(PI*(a*a+4*self.lam2**2*math.sin(theta)**2))

    def cont(self,fun,breaks=()):
        points=[0.0, PI]
        for x in breaks:
            u=x-self.center
            if -1 < u < 1:
                points.append(math.acos(u))
        points=sorted(set(points))
        def integrand(theta):
            x=self.center+math.cos(theta)
            return self.theta_weight(theta)*fun(x)
        real=imag=0.0
        for a,b in zip(points[:-1],points[1:]):
            real += quad(lambda th:float(np.real(integrand(th))),a,b,epsabs=self.epsabs,epsrel=self.epsrel,limit=200)[0]
            imag += quad(lambda th:float(np.imag(integrand(th))),a,b,epsabs=self.epsabs,epsrel=self.epsrel,limit=200)[0]
        return real+1j*imag

    def integral(self,fun,breaks=()):
        return self.weight*fun(self.atom)+self.cont(fun,breaks)

    def L(self,E):
        return float(self.integral(lambda x:self.r(E-x)).real)

    def Lprime(self,E):
        return float(self.integral(lambda x:self.rp(E-x)).real)


def calculate(g=.2,tol=2e-12):
    plus=Measure(5.,2*g*g,tol,tol)
    minus=Measure(1.,g*g,tol,tol)
    E=brentq(lambda e:plus.L(e)+minus.L(e),2*plus.atom+1e-9,2*minus.atom-1e-9,xtol=1e-14,rtol=9e-16)
    D=plus.Lprime(E)+minus.Lprime(E)
    C=math.sqrt(2/D)
    Ap=lambda x:float(plus.r(E-x).real)
    Am=lambda y:float(minus.r(E-y).real)
    bb=plus.atom+minus.atom
    # Cauchy transforms evaluated analytically in one coordinate. These contain
    # the bound-bound, bound-continuum and continuum-continuum terms.
    K=plus.integral(lambda x:minus.r(E-x),breaks=(E-2,E))
    J=C*(plus.integral(lambda x:Ap(x)*minus.r(E-x),breaks=(E-2,E))+
          minus.integral(lambda y:Am(y)*plus.r(E-y),breaks=(E-6,E-4)))
    c=J/K
    lo=max(4.,E-2.)
    hi=min(6.,E)
    def W(x):return plus.density(x)*minus.density(E-x)
    def s(x):return Ap(x)+Am(E-x)
    def shell(fun):
        # x = lo+(hi-lo) sin^2(theta) smooths the square-root endpoints.
        def f(th):
            x=lo+(hi-lo)*math.sin(th)**2
            return fun(x)*2*(hi-lo)*math.sin(th)*math.cos(th)
        return quad(f,0,PI/2,epsabs=tol*1e-4,epsrel=tol,limit=300)[0]
    M0=shell(W)
    M1=shell(lambda x:W(x)*C*s(x))
    M2=shell(lambda x:W(x)*(C*s(x))**2)
    rho=shell(lambda x:W(x)*abs(C*s(x)-c)**2)
    lower=max(0.,M2-M1*M1/M0)
    # This norm formula uses independent x/y in the odd product space.
    residual=C*(plus.L(E)+minus.L(E))
    norm_formula=C*C*(plus.integral(lambda x:Ap(x)**2).real+minus.integral(lambda y:Am(y)**2).real+2*plus.L(E)*minus.L(E))
    return dict(g=g,quadrature_tolerance=tol,Eplus=plus.atom,Eminus=minus.atom,Zplus=plus.weight,Zminus=minus.weight,
        measure_mass_plus=plus.integral(lambda x:1.).real,measure_mass_minus=minus.integral(lambda x:1.).real,
        Ep=E,connected_shift=E-bb,even_pair_normalization_D=D,source_prefactor_C=C,
        pair_bare_overlap_squared=2*plus.L(E)**2/D,source_q_overlap=residual,source_norm_squared=norm_formula,
        K_real=float(K.real),K_imag=float(K.imag),J_real=float(J.real),J_imag=float(J.imag),
        c_real=float(c.real),c_imag=float(c.imag),shell_interval=[lo,hi],shell_mass=M0,
        shell_K_imag_error=float(K.imag-PI*M0),rho=rho,variance_lower_bound=lower,
        density_moments=[M0,M1,M2],
        shell_amplitude_samples=[[x,C*s(x)] for x in np.linspace(lo+.05*(hi-lo),hi-.05*(hi-lo),5)],
        amplitude_decay_rate_coefficient=PI*rho,probability_decay_rate_coefficient=2*PI*rho)

if __name__=='__main__':
    results=[calculate(.2,tol) for tol in [2e-10,2e-12,2e-13]]
    for run in results:
        assert abs(run['measure_mass_plus']-1)<1e-10
        assert abs(run['measure_mass_minus']-1)<1e-10
        assert abs(run['source_q_overlap'])<1e-10
        assert abs(run['shell_K_imag_error'])<1e-10
        assert run['rho']>run['variance_lower_bound']>0
    output={'classification':'FINITE_STRICTLY_POSITIVE (analytical proof in PROOF.md)',
            'scope':'Exact infinite-volume dressed source and odd hard-core compression; numeric digits are ordinary quadrature.',
            'runs':results}
    out=Path(__file__).with_name('results.json')
    out.write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(output,indent=2))
