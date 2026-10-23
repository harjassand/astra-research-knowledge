"""Integrable, identifiable-source FE envelope family; NOT a measured free energy.

The 75 C branch average fixes q_ref. Three source P(T) traces fix high-field
temperature increments, while the published indirect EC curve fixes the
full-field entropy integral. One explicit low-field shape remains free.
All results are per footprint area of one ten-layer bank, SI.
"""
from pathlib import Path
import json
import numpy as np
from numpy.polynomial import Polynomial as Poly
from functools import lru_cache

DATA = json.loads(Path(__file__).with_name('envelope_data.json').read_text())
N = 10
ELL = 260e-9
TREF = 348.15
TCENTER = 343.0
CV_BASE = 7.8  # FE only; add actual electrodes/coatings/fluid elsewhere
VMAX = 89.5e6 * ELL
VNODES = np.array(DATA['E_nodes_V_m']) * ELL
FEA = np.array(DATA['qref_fit_parameters'])


def qref(V):
    a, b, z, c = FEA
    return N * (a + b * np.tanh(V/z) + c*V)


def cref(V):
    a, b, z, c = FEA
    return N * (b/z/np.cosh(V/z)**2 + c)


def intqref(V):
    a, b, z, c = FEA
    return N * (a*V + b*z*np.log(np.cosh(V/z)) + .5*c*V*V)


@lru_cache(maxsize=128)
def p_polys(shape=0.):
    """p(E,T) nodal polynomials in theta=T-343 K; -0.5<=shape<=1.

    This interval describes this five-node family, not all admissible
    constitutive responses. Low-field nodes p0=A(1+2s), pm=A(1-s) retain the
    measured entropy integral exactly while redistributing the response.
    """
    if not -.5 <= shape <= 1.:
        raise ValueError('Declared nonpositive-p family requires shape in [-0.5, 1]')
    high=[Poly(c) for c in DATA['highfield_p_polynomial_coefficients']]
    A=Poly(DATA['lowfield_A_polynomial_coefficients'])
    return [A*(1+2*shape), A*(1-shape), *high]


@lru_cache(maxsize=128)
def _arrays(shape):
    ps=p_polys(shape)
    co=np.zeros((5,3))
    for k,p in enumerate(ps):co[k,:len(p.coef)]=p.coef
    der=co[:,1:]*np.array([1,2])
    inte=np.c_[np.zeros(5),co/np.array([1,2,3])]
    return co,der,inte


def integral_v(values, V):
    """Integral of the piecewise-linear nodal values from 0 to V."""
    values=np.asarray(values)
    if V < 0 or V > VMAX+1e-12:
        raise ValueError('Voltage outside measured positive-field envelope')
    j=min(np.searchsorted(VNODES,V,side='right')-1,len(VNODES)-2)
    j=max(j,0)
    full=np.sum(.5*(values[:j]+values[1:j+1])*np.diff(VNODES[:j+1]))
    dv=V-VNODES[j]
    slope=(values[j+1]-values[j])/(VNODES[j+1]-VNODES[j])
    return full+values[j]*dv+.5*slope*dv*dv


def props(T,V,shape=0.,extra_CV=0.):
    """Q=-G_V, S=-G_T, C=Q_V, alpha=Q_T, CV=T*S_T.

    The same potential fixes every thermal/electrical derivative. CV_BASE
    is the zero-voltage FE heat capacity. A measured constant heat capacity
    at every voltage would conflict with T-dependent source p.
    """
    if not 338.-1e-10 <= T <= TREF+1e-10:
        raise ValueError('Temperature outside source-constrained envelope 338..348.15 K')
    co,der,inte=_arrays(shape);theta=T-TCENTER;ref=TREF-TCENTER
    p=np.polynomial.polynomial.polyval(theta,co.T)
    pt=np.polynomial.polynomial.polyval(theta,der.T)
    dp=np.polynomial.polynomial.polyval(theta,inte.T)-np.polynomial.polynomial.polyval(ref,inte.T)
    j=min(max(np.searchsorted(VNODES,V,side='right')-1,0),len(VNODES)-2)
    cv0=CV_BASE+extra_CV
    Q=qref(V)+N*np.interp(V,VNODES,dp)
    C=cref(V)+N*(dp[j+1]-dp[j])/(VNODES[j+1]-VNODES[j])
    alpha=N*np.interp(V,VNODES,p)
    S=cv0*np.log(T/TREF)+N*integral_v(p,V)
    CV=cv0+T*N*integral_v(pt,V)
    G=-cv0*(T*np.log(T/TREF)-T+TREF)-intqref(V)-N*integral_v(dp,V)
    return dict(Q=float(Q),C=float(C),alpha=float(alpha),CV=float(CV),
                S=float(S),G=float(G),U=float(G+T*S+V*Q),
                C_fixedQ=float(CV-T*alpha*alpha/C))


def loss_functionals(t,V,Q):
    """Actual-path coefficients, before including leakage current feedback.

    For constant terminal shunt conductance g: Wleak=g*int(V²dt).
    For constant per-film positive current density j: Wleak=N*j*int(Vdt).
    For constant terminal series resistance r_area: Wseries=r_area*int(i²dt).
    All unknown losses must then be coupled back into heat/current dynamics.
    """
    t=np.asarray(t);V=np.asarray(V);Q=np.asarray(Q)
    if np.any(np.diff(t)<=0):
        raise ValueError('Strictly increasing trajectory time required')
    i=np.gradient(Q,t)
    return dict(period_s=float(t[-1]-t[0]),
      voltage_time_V_s=float(np.trapezoid(V,t)),
      voltage_squared_time_V2_s=float(np.trapezoid(V*V,t)),
      current_squared_time_A2_s_m4=float(np.trapezoid(i*i,t)),
      Q_reset_C_m2=float(Q[-1]-Q[0]),V_reset_V=float(V[-1]-V[0]))
