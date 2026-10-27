#!/usr/bin/env python3
"""Infinite-ladder response from the two endpoint measures, g = 1/5.

All integrations include the one-body atoms and continua.  The real parts of
the continuum-continuum integrals use an explicit Cauchy principal value; the
imaginary parts use the on-shell density.  The result is a floating-point
diagnostic, not an interval-arithmetic certificate.  See PROOF.md.
"""
from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass

import numpy as np
from scipy.integrate import quad, IntegrationWarning
from scipy.optimize import brentq
from scipy.linalg import eigh_tridiagonal, null_space
import warnings

warnings.simplefilter("error", IntegrationWarning)
PI = math.pi


@dataclass
class Channel:
    center: float
    k: float                   # squared memory/end-of-chain coupling
    atom: float = 0.0
    mass: float = 0.0

    def surface(self, z: float) -> float:
        w = z - self.center
        if abs(w) <= 1:
            raise ValueError(("surface argument is not outside bath", z))
        return 2 * (-w + math.copysign(math.sqrt(w*w - 1), w))

    def surface_prime(self, z: float) -> float:
        w = z - self.center
        if abs(w) <= 1:
            raise ValueError(("surface argument is not outside bath", z))
        return 2 * (-1 + abs(w) / math.sqrt(w*w - 1))

    def m(self, z: float) -> float:
        return 1 / (3-z-self.k*self.surface(z))

    def mprime(self, z: float) -> float:
        d = 3-z-self.k*self.surface(z)
        return (1+self.k*self.surface_prime(z)) / d**2

    def m_boundary(self, z: float) -> complex:
        """Upper boundary of endpoint resolvent, at real z away from atom."""
        w=z-self.center
        if abs(w)>=1:
            if abs(w)==1:
                s=complex(-2*w,0)
                return 1/(3-z-self.k*s)
            return complex(self.m(z),0)
        s=complex(-2*w,2*math.sqrt(1-w*w))
        return 1/(3-z-self.k*s)

    def density(self, x: float) -> float:
        w = x-self.center
        if abs(w) >= 1:
            return 0.0
        q = math.sqrt(1-w*w)
        a = 3-x-2*self.k*(self.center-x)
        return 2*self.k*q / (PI*(a*a+4*self.k*self.k*q*q))

    def init_atom(self) -> None:
        if self.center == 5:
            interval = (2.8, 3.0)
        else:
            interval = (3.0, 3.1)
        self.atom = brentq(lambda z: 3-z-self.k*self.surface(z),
                           *interval, xtol=1e-14)
        self.mass = 1/(1+self.k*self.surface_prime(self.atom))


def band_integral(ch, fun, eps=2e-11):
    """Integrate rho(x)*fun(x) using a smooth theta parameterization."""
    def integrand(theta):
        x=ch.center+math.cos(theta)
        return ch.density(x)*math.sin(theta)*fun(x)
    return quad(integrand, 0, PI, epsabs=eps, epsrel=eps, limit=300)[0]


def measure_integral(ch, fun, eps=2e-11):
    return ch.mass*fun(ch.atom)+band_integral(ch,fun,eps)


def L(ch, e, derivative=False):
    mf = ch.mprime if derivative else ch.m
    return measure_integral(ch, lambda x: mf(e-x))


def response(g=0.2, eps=2e-10):
    plus = Channel(5., 2*g*g)
    minus = Channel(1., g*g)
    plus.init_atom()
    minus.init_atom()
    lo=2*plus.atom+1e-9
    hi=2*minus.atom-1e-9
    E = brentq(lambda e: L(plus,e)+L(minus,e),lo,hi,xtol=1e-14)
    D = L(plus,E,True)+L(minus,E,True)
    C = math.sqrt(2/D)
    def u(x,y):
        return plus.m(E-x)+minus.m(E-y)

    # Atom/atom and the two atom/continuum contributions to M and J/C.
    def offshell(n):
        result = plus.mass*minus.mass*u(plus.atom,minus.atom)**n / (plus.atom+minus.atom-E)
        result += plus.mass*band_integral(minus, lambda y: u(plus.atom,y)**n/(plus.atom+y-E), eps)
        result += minus.mass*band_integral(plus, lambda x: u(x,minus.atom)**n/(x+minus.atom-E), eps)
        return result

    # Exact Sokhotski-Plemelj boundary of continuum-continuum piece.
    # Calculate the Cauchy PV in the inner y integral, including its square-root
    # endpoint density, and the ordinary x integral outside.
    def cc_real(n):
        def inner(x):
            c=E-x
            def numerator(y): return minus.density(y)*u(x,y)**n
            if 0 < c < 2:
                return quad(numerator,0,2,weight='cauchy',wvar=c,
                            epsabs=eps*0.2,epsrel=eps*0.2,limit=400)[0]
            return quad(lambda y: numerator(y)/(y-c),0,2,
                        epsabs=eps*0.2,epsrel=eps*0.2,limit=400)[0]
        breaks=sorted(set([4.,6.]+[a for a in [E-2,E] if 4<a<6]))
        value=0.
        for a,b in zip(breaks[:-1],breaks[1:]):
            value+=quad(lambda x: plus.density(x)*inner(x),a,b,
                        epsabs=eps,epsrel=eps,limit=400)[0]
        return value

    a=max(4., E-2.)
    b=min(6., E)
    def shell(n):
        def integrand(x):
            y=E-x
            return plus.density(x)*minus.density(y)*u(x,y)**n
        return quad(integrand,a,b,epsabs=eps*0.01,epsrel=eps,limit=400)[0]

    M = complex(offshell(0)+cc_real(0), PI*shell(0))
    J = complex(offshell(1)+cc_real(1), PI*shell(1))
    alpha=J/M
    def rho_integrand(x):
        y=E-x
        return plus.density(x)*minus.density(y)*abs(u(x,y)-alpha)**2
    rho=C*C*quad(rho_integrand,a,b,epsabs=eps*1e-4,epsrel=eps,limit=400)[0]
    Q = measure_integral(plus,lambda x: measure_integral(minus,lambda y:u(x,y)**2,eps),eps)
    answer={
        "g":g, "one_body_bound_energy_plus":plus.atom,
        "one_body_bound_energy_minus":minus.atom,
        "one_body_bound_mass_plus":plus.mass,"one_body_bound_mass_minus":minus.mass,
        "mu_plus_mass":measure_integral(plus,lambda x:1.,eps),
        "mu_minus_mass":measure_integral(minus,lambda x:1.,eps),
        "pair_energy":E,"pair_connected_shift":E-plus.atom-minus.atom,
        "L_plus":L(plus,E),"L_minus":L(minus,E),"D":D,"C":C,
        "source_norm_squared":C*C*Q,
        "source_odd_forbidden_overlap":C*(L(plus,E)+L(minus,E)),
        "M_real":M.real,"M_imag":M.imag,"J_over_C_real":J.real,
        "J_over_C_imag":J.imag,"alpha_real":alpha.real,"alpha_imag":alpha.imag,
        "shell_begin":a,"shell_end":b,"shell_bare_weight":shell(0),
        "rho":rho,
        "formal_population_rate_coefficient_2pi_rho":2*PI*rho,
        "formal_amplitude_HWHM_coefficient_pi_rho":PI*rho,
        "quadrature_requested_tolerance":eps,
        "note":"Floating-point quadrature; no certified error bound or resonance theorem.",
    }
    return answer


def finite_check(g=.2, n=9):
    """Independently compress finite two-boson Hilbert spaces, check formulas."""
    specs=[]
    for center,k in ((5.,2*g*g),(1.,g*g)):
        vals, U=eigh_tridiagonal(np.r_[3.,np.full(n,center)],
                                 np.r_[math.sqrt(k),np.full(n-1,-.5)])
        specs.append((vals,U[0,:]**2,U[0,:]))
    xp,wp,ep=specs[0]; ym,wm,em=specs[1]
    def finite_L(vals,w,E):
        return np.sum(w[:,None]*w[None,:]/(vals[:,None]+vals[None,:]-E))
    bp=xp[np.argmin(abs(xp-3))]; bm=ym[np.argmin(abs(ym-3))]
    E=brentq(lambda z:finite_L(xp,wp,z)+finite_L(ym,wm,z),2*bp+1e-8,2*bm-1e-8,xtol=1e-14)
    Lpder=lambda vals,w:np.sum(w[:,None]*w[None,:]/(vals[:,None]+vals[None,:]-E)**2)
    C=math.sqrt(2/(Lpder(xp,wp)+Lpder(ym,wm)))
    a=np.sum(wp[None,:]/(xp[:,None]+xp[None,:]-E),axis=1)
    b=np.sum(wm[None,:]/(ym[:,None]+ym[None,:]-E),axis=1)
    q=(ep[:,None]*em[None,:]).ravel()
    f=(C*ep[:,None]*em[None,:]*(a[:,None]+b[None,:])).ravel()
    H0=np.diag((xp[:,None]+ym[None,:]).ravel())
    Qbasis=null_space(q.reshape(1,-1))
    H=Qbasis.T@H0@Qbasis
    fQ=Qbasis.T@f
    z=E+0.15j
    exact=np.vdot(fQ,np.linalg.solve(H-z*np.eye(H.shape[0]),fQ))
    r=1/(np.diag(H0)-z)
    formula=np.dot(f*r,f)-np.dot(f*r,q)**2/np.dot(q*r,q)
    return {"n":n,"E":E,"norm_f_squared":float(f@f),
            "q_overlap":float(q@f),"direct_real":float(exact.real),
            "direct_imag":float(exact.imag),"rank_one_real":float(formula.real),
            "rank_one_imag":float(formula.imag),"difference":float(abs(exact-formula))}


def fock_check(g=.2,n=4):
    """Direct local hard-core Fock construction, independent of the reduction."""
    d=2+2*n
    h=np.diag([3.,3.]+[5.]*n+[1.]*n)
    for mem in [0,1]:
        h[mem,2]=h[2,mem]=g
        h[mem,2+n]=h[2+n,mem]=g/math.sqrt(2)*(1 if mem==0 else -1)
    for first in [2,2+n]:
        for j in range(n-1):
            h[first+j,first+j+1]=h[first+j+1,first+j]=-.5
    basis=[(i,j) for i in range(d) for j in range(i,d)
           if not (i==j and i in (0,1))]
    loc={q:i for i,q in enumerate(basis)}
    N=len(basis)
    H=np.zeros((N,N))
    for col,(i,j) in enumerate(basis):
        occupation=np.bincount([i,j],minlength=d)
        for a in range(d):
            if occupation[a]==0: continue
            occ1=occupation.copy()
            factor=math.sqrt(occ1[a])
            occ1[a]-=1
            for b in np.flatnonzero(h[:,a]):
                occ2=occ1.copy()
                amp=factor*math.sqrt(occ2[b]+1)*h[b,a]
                occ2[b]+=1
                if occ2[0]>1 or occ2[1]>1: continue
                state=tuple(np.repeat(np.arange(d),occ2))
                H[loc[state],col]+=amp
    assert np.max(abs(H-H.T))<1e-12
    swap=np.arange(d);swap[0]=1;swap[1]=0
    sign=np.ones(d);sign[2+n:]=-1
    S=np.zeros((N,N))
    for j,(a,b) in enumerate(basis):
        S[loc[tuple(sorted((swap[a],swap[b])))],j]=sign[a]*sign[b]
    assert np.max(abs(H@S-S@H))<1e-12
    sev,U=np.linalg.eigh(S)
    Be=U[:,sev>0];Bo=U[:,sev<0]
    ev,W=np.linalg.eigh(Be.T@H@Be)
    p=np.zeros(N);p[loc[(0,1)]]=1
    overlaps=(p@Be@W)**2
    ix=int(np.argmax(overlaps))
    E=ev[ix]
    psi=Be@W[:,ix]
    v=np.array([(int(a==0)+int(b==0))-(int(a==1)+int(b==1)) for a,b in basis])
    f=Bo.T@(v*psi)
    Ho=Bo.T@H@Bo
    z=E+.15j
    resolvent=np.vdot(f,np.linalg.solve(Ho-z*np.eye(Ho.shape[0]),f))
    reduced=finite_check(g,n)
    r=complex(reduced['rank_one_real'],reduced['rank_one_imag'])
    return {'n':n,'fock_dimension':N,'E':float(E),'norm_f_squared':float(f@f),
            'resolvent_real':float(resolvent.real),'resolvent_imag':float(resolvent.imag),
            'pair_energy_difference':float(abs(E-reduced['E'])),
            'source_norm_difference':float(abs(f@f-reduced['norm_f_squared'])),
            'resolvent_difference':float(abs(resolvent-r))}


def single_integral_check(g=.2,eps=1e-10):
    """Independent Fubini reduction: compute M and J using only one-body m."""
    p=Channel(5.,2*g*g); m=Channel(1.,g*g)
    p.init_atom();m.init_atom()
    E=brentq(lambda e:L(p,e)+L(m,e),2*p.atom+1e-9,2*m.atom-1e-9,xtol=1e-14)
    def a(x): return p.m(E-x)
    def b(y): return m.m(E-y)
    def component(ch,fun,component,breaks):
        cut=[0.,PI]
        for x in breaks:
            if ch.center-1 < x < ch.center+1:
                cut.append(math.acos(x-ch.center))
        cut=sorted(cut)
        def f(theta):
            x=ch.center+math.cos(theta)
            z=fun(x)
            return ch.density(x)*math.sin(theta)*(z.real if component==0 else z.imag)
        return sum(quad(f,s,t,epsabs=eps,epsrel=eps,limit=300)[0]
                   for s,t in zip(cut[:-1],cut[1:]))
    def integral(ch,fun,breaks):
        v=ch.mass*fun(ch.atom)
        return v+complex(component(ch,fun,0,breaks),component(ch,fun,1,breaks))
    M=integral(p,lambda x:m.m_boundary(E-x),[E-2,E])
    J=integral(p,lambda x:a(x)*m.m_boundary(E-x),[E-2,E])
    J+=integral(m,lambda y:b(y)*p.m_boundary(E-y),[E-6,E-4])
    return {'E':E,'M_real':M.real,'M_imag':M.imag,'J_over_C_real':J.real,
            'J_over_C_imag':J.imag,'alpha_real':(J/M).real,'alpha_imag':(J/M).imag}


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--eps',type=float,default=2e-10)
    parser.add_argument('--check',action='store_true')
    parser.add_argument('--fock-check',action='store_true')
    parser.add_argument('--single-integral-check',action='store_true')
    args=parser.parse_args()
    if args.fock_check:
        # Some Accelerate/OpenBLAS builds retain spurious floating exception
        # flags from eigensolvers; check all numerical outputs explicitly.
        with np.errstate(divide='ignore',over='ignore',invalid='ignore'):
            answer=fock_check()
        assert all(math.isfinite(float(v)) for v in answer.values())
        assert max(answer['pair_energy_difference'],answer['source_norm_difference'],
                   answer['resolvent_difference']) < 1e-11
    elif args.check:
        with np.errstate(divide='ignore',over='ignore',invalid='ignore'):
            answer=finite_check()
        assert all(math.isfinite(float(v)) for v in answer.values())
        assert abs(answer['q_overlap'])<1e-10 and answer['difference']<1e-11
    elif args.single_integral_check: answer=single_integral_check(eps=args.eps)
    else: answer=response(eps=args.eps)
    print(json.dumps(answer,indent=2,allow_nan=False))
