#!/usr/bin/env python3
"""Infinite-ladder hard-core pair's local-parity-breaking spectral response.

One-dimensional Stieltjes quadrature; all one-body atoms and continua included.
The analytic positivity proof is in RESULT.md; these numbers are diagnostics,
not interval-certified values. No finite-chain approximation enters the formula.
"""
from __future__ import annotations
import json
import math
import warnings
import numpy as np
from scipy.integrate import quad, IntegrationWarning
from scipy.optimize import brentq

G = 0.2

class Measure:
    def __init__(self, sign):
        self.sign = sign
        self.center = 5.0 if sign == 1 else 1.0
        self.lam = 2 * G * G if sign == 1 else G * G
        q = lambda d: 2.0 / (2.0 + d + math.sqrt((2.0+d)**2 - 1.0))
        self.d = brentq(lambda d: d-self.lam*q(d), 0., 0.2, xtol=5e-16)
        self.atom = 3.0 - self.d if sign == 1 else 3.0 + self.d
        self.weight = 1 / (1 + self.d / math.sqrt((2+self.d)**2 - 1))

    def bath_m(self, z):
        """Physics G(z)=(z-h_bath)^-1 at z on the upper rim."""
        u = z-self.center
        if u > 1:
            return 2/(u + math.sqrt(u*u-1))
        if u < -1:
            return 2/(u - math.sqrt(u*u-1))
        return complex(2*u, -2*math.sqrt(max(0., 1-u*u)))

    def stieltjes(self,z):
        """s(z)=integral mu(dx)/(x-z), real outside support, upper rim inside."""
        return -1/(z-3-self.lam*self.bath_m(z))

    def deriv_real(self,z):
        u=z-self.center
        assert abs(u) > 1
        # bath derivative (z-h)^-1 derivative is negative
        radical=math.sqrt(u*u-1)
        mb=self.bath_m(z)
        mb_prime= -abs(mb)/radical
        den=z-3-self.lam*mb
        return (1-self.lam*mb_prime)/(den*den)

    def density(self, x):
        u=x-self.center
        if abs(u)>=1: return 0.0
        v=math.sqrt(1-u*u)
        return (2*self.lam*v / math.pi) / ((x-3-2*self.lam*u)**2 + (2*self.lam*v)**2)

    def integrate_cont(self, fn, points=(), eps=2e-12):
        # cosine change smooths square-root endpoints, with breakpoints on
        # the other measure's band edges supplied to quadrature.
        theta_points = [math.acos(min(1., max(-1., x-self.center))) for x in points
                        if self.center-1 < x < self.center+1]
        def f(theta):
            x=self.center+math.cos(theta)
            return self.density(x)*math.sin(theta)*fn(x)
        kwargs=dict(points=sorted(theta_points), epsabs=eps, epsrel=eps, limit=300)
        real=quad(lambda t: float(np.real(f(t))), 0, math.pi, **kwargs)[0]
        imag=quad(lambda t: float(np.imag(f(t))), 0, math.pi, **kwargs)[0]
        return real+1j*imag

    def integrate(self, fn, points=(), eps=2e-12):
        return self.weight * fn(self.atom) + self.integrate_cont(fn, points, eps)

p,m=Measure(1),Measure(-1)

def L(s, E, eps=2e-12):
    return s.integrate(lambda x: s.stieltjes(E-x), eps=eps).real

def deriv_L(s, E, eps=2e-12):
    return s.integrate(lambda x:s.deriv_real(E-x), eps=eps).real

def solve(eps=2e-12):
    E=brentq(lambda E: L(p,E,eps)+L(m,E,eps), 2*p.atom+1e-10, 2*m.atom-1e-10, xtol=2e-14)
    D=deriv_L(p,E,eps)+deriv_L(m,E,eps)
    A=lambda x:p.stieltjes(E-x).real
    C=lambda y:m.stieltjes(E-y).real
    # The two cross-band convolution integrals have branch points at E-c+-1.
    bp_p=[E-(m.center-1), E-(m.center+1)]
    bp_m=[E-(p.center-1), E-(p.center+1)]
    G0=p.integrate(lambda x:m.stieltjes(E-x), points=bp_p, eps=eps)
    J0=(p.integrate(lambda x:A(x)*m.stieltjes(E-x), points=bp_p, eps=eps)
      + m.integrate(lambda y:C(y)*p.stieltjes(E-y), points=bp_m, eps=eps))
    q=J0/G0
    lo=max(4., E-2.)
    hi=min(6., E)
    assert hi > lo
    def integ_shell(fn):
        def f(theta):
            s=math.sin(theta); c=math.cos(theta)
            x=lo+(hi-lo)*s*s
            y=E-x
            jac=2*(hi-lo)*s*c
            return p.density(x)*m.density(y)*fn(x,y)*jac
        return quad(f, 0., math.pi/2, epsabs=1e-19, epsrel=eps, limit=300)[0]
    density=2/D * integ_shell(lambda x,y: abs(A(x)+C(y)-q)**2)
    b_shell=integ_shell(lambda x,y:1.)
    bshell1=integ_shell(lambda x,y:A(x)+C(y))
    bshell2=integ_shell(lambda x,y:(A(x)+C(y))**2)
    variance=bshell2-bshell1*bshell1/b_shell
    bound=2/D*variance
    f_norm=2/D*(p.integrate(lambda x:A(x)**2,eps=eps).real
                +m.integrate(lambda y:C(y)**2,eps=eps).real
                +2*L(p,E,eps)*L(m,E,eps))
    step=1e-6
    D_fd=sum((L(s,E+step,eps)-L(s,E-step,eps))/(2*step) for s in (p,m))
    return dict(g=G,e_plus=p.atom,e_minus=m.atom,w_plus=p.weight,w_minus=m.weight,
      E_pair=E,chi=E-p.atom-m.atom,Lplus=L(p,E,eps),Lminus=L(m,E,eps),D=D,
      G_re=G0.real,G_im=G0.imag,J_re=J0.real,J_im=J0.imag,
      q_re=q.real,q_im=q.imag,source_norm_squared=f_norm,shell_interval=[lo,hi],shell_weight=b_shell,
      shell_mean=bshell1/b_shell,shell_variance_integral=variance,
      rigorous_formula_lower_bound_numeric=bound,rho=density,
      checks=dict(D_by_centered_difference=D_fd,im_G_equals_pi_shell=G0.imag/(math.pi*b_shell),
                  im_J_equals_pi_shell_B=J0.imag/(math.pi*bshell1),
                  plus_total=p.integrate(lambda x:1.,eps=eps).real,
                  minus_total=m.integrate(lambda x:1.,eps=eps).real))

if __name__=='__main__':
    warnings.simplefilter('error', IntegrationWarning)
    out=solve()
    print(json.dumps(out,indent=2))
