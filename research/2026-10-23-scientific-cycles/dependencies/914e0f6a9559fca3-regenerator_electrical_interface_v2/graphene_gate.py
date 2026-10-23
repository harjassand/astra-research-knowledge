"""Canonical monolayer Dirac gas + real geometric capacitor, per unit area.

SI units internally; caller supplies gate Cgeo [F/m^2].  No FE surrogate,
external voltage clock, gate loss or measured device claim is supplied here.
Both identical parallel gates are included by multiplying extensive outputs
q, qV, qT, entropy and Cv by two.  mu_eV is common, not multiplied.
"""
import numpy as np
from scipy.special import spence
from scipy.optimize import brentq

E_CHARGE = 1.602176634e-19
KB = 1.380649e-23
HBAR = 1.054571817e-34
EPS0 = 8.8541878128e-12
VF = 1.0e6
DEGENERACY = 4.0
PREF = DEGENERACY / (2*np.pi*(HBAR*VF)**2)
_gx, _gw = np.polynomial.legendre.leggauss(128)


def dirac(mu_eV, T):
    """Return n, n_mu(J^-1), n_T, Omega, S and Cv_at_mu for signed mu.

    Neutrality is n=0, including thermally excited electron/hole entropy.
    The filled T=0 valence sea is the fixed subtracted reference.
    """
    mu = float(mu_eV)*E_CHARGE
    T = float(T)
    if T <= 0:
        raise ValueError('T must be positive')
    eta = abs(mu)/(KB*T)
    li2small = spence(1+np.exp(-eta))
    nabs = PREF*(KB*T)**2*(eta*eta/2+np.pi**2/6+2*li2small)
    n = np.sign(mu)*nabs
    n_mu = PREF*KB*T*(eta+2*np.log1p(np.exp(-eta)))
    n_T = (2*n-mu*n_mu)/T
    # Direct grand-potential integral is independent of the dilogarithm n.
    xmax = max(40., eta+40.)
    x = (_gx+1)*xmax/2
    integ = np.dot(_gw, x*(np.logaddexp(0.,eta-x)
                           +np.logaddexp(0.,-eta-x)))*xmax/2
    Omega = -PREF*(KB*T)**3*integ
    entropy = (-3*Omega-mu*n)/T
    Cv_mu = (-6*Omega-4*mu*n+mu*mu*n_mu)/T
    return dict(n=float(n), n_mu=float(n_mu), n_T=float(n_T),
                Omega=float(Omega), entropy=float(entropy),
                Cv_at_mu=float(Cv_mu))


def gate(V, T, Cgeo):
    """One complete equilibrium gate at terminal electrochemical voltage V.

    V=q/Cgeo+mu/e; q=e*n.  Positive V dopes electrons on the graphene side,
    with opposite compensating charge on its metal back electrode.
    Returns analytic qV, qT and Cv at FIXED TERMINAL V, all per unit area.
    """
    V, T, Cgeo = float(V), float(T), float(Cgeo)
    if Cgeo <= 0:
        raise ValueError('Cgeo must be positive')
    if V == 0:
        mu_eV = 0.
    else:
        sign = np.sign(V)
        def voltage(muabs_eV):
            return E_CHARGE*dirac_density(muabs_eV,T)/Cgeo+muabs_eV
        mu_eV = sign*brentq(lambda u: voltage(u)-abs(V), 0.,
                           max(abs(V),1e-9), xtol=1e-13, rtol=1e-12)
    d = dirac(mu_eV,T)
    q = E_CHARGE*d['n']
    Cq = E_CHARGE**2*d['n_mu']
    qV = Cgeo*Cq/(Cgeo+Cq)
    qT = E_CHARGE*d['n_T']*Cgeo/(Cgeo+Cq)
    Cv = d['Cv_at_mu']-T*E_CHARGE**2*d['n_T']**2/(Cgeo+Cq)
    Fcanonical = d['Omega']+mu_eV*E_CHARGE*d['n']+q*q/(2*Cgeo)
    Ggrand = Fcanonical-V*q
    return dict(V=V, T=T, Cgeo=Cgeo, mu_eV=float(mu_eV), q=q,
                qV=qV, qT=qT, Cv=Cv, entropy=d['entropy'],
                Cq=Cq, Fcanonical=Fcanonical, Ggrand=Ggrand,
                n=d['n'], n_mu=d['n_mu'], n_T=d['n_T'])


def dirac_density(mu_eV,T):
    """Fast signed density without a grand-potential quadrature."""
    mu = float(mu_eV)*E_CHARGE
    eta = abs(mu)/(KB*T)
    f1 = eta*eta/2+np.pi**2/6+2*spence(1+np.exp(-eta))
    return float(np.sign(mu)*PREF*(KB*T)**2*f1)


def voltage_for_mu(mu_eV,T,Cgeo):
    return E_CHARGE*dirac_density(mu_eV,T)/Cgeo+mu_eV


def pure_R_stability(Cv, alpha, C, Gth, beta, resistance_area, T):
    """Linear test for per-area current -V/resistance_area; no inductor.

    M=[[Cv,T*alpha],[alpha,C]], thermal rhs=-Gth*dT+beta*dV.
    resistance_area [ohm*m^2].  Stable equilibrium requires D>0, Gth>0.
    """
    D = Cv*C-T*alpha*alpha
    trace = -(C*Gth+alpha*beta+Cv/resistance_area)/D
    determinant = Gth/(resistance_area*D)
    return dict(D=D, trace=trace, determinant=determinant,
                unstable=bool(trace>0 and determinant>0))


def neutral_SiC_Cgeo(thickness_m):
    """Explicit scalar Lorentz model's STATIC epsilon, not measured gate loss."""
    epsdc = 6.7*(1.827e14/1.495e14)**2
    return EPS0*epsdc/thickness_m


def parallel_totals(V,T,Cgeo,fe_Cv,fe_qT,fe_qV,passive_Cv=0.,number=2):
    """Add actual gates to supplied FE constitutive derivatives, per area.

    For N parallel FE slabs each thickness ell: fe_qV=N*epsilon_diff/ell,
    fe_qT=N*p, fe_Cv=N*ell*cV.  Do not use total active thickness for ell.
    FE derivatives must all come from one potential, or be labeled surrogate.
    """
    d=gate(V,T,Cgeo)
    Cv=fe_Cv+passive_Cv+number*d['Cv']
    alpha=fe_qT+number*d['qT']
    C=fe_qV+number*d['qV']
    return dict(Cv=Cv,alpha=alpha,C=C,D=Cv*C-T*alpha**2,gate=d)


def series_RLC_stability(Cv,alpha,C,Gth,beta,T,L_area,R_area,Cs_area=np.inf):
    """Cubic for root's qdot=i, L*idot=-R*i-V-(q-qbias)/Cs.

    All extensive device quantities are per unit area, i in A/m^2.
    Convert physical elements by L_area=L_device*area,
    R_area=R_device*area, Cs_area=Cs_device/area.
    Requires Gth=-partial_T(qrad)>0, beta=partial_V(qrad).
    """
    D=Cv*C-T*alpha**2
    A=C*Gth+alpha*beta
    invCs=0. if np.isinf(Cs_area) else 1/Cs_area
    a=np.array([L_area*D,L_area*A+R_area*D,
                R_area*A+D*invCs+Cv,A*invCs+Gth],float)
    roots=np.roots(a)
    return dict(D=D,A=A,coefficients=a.tolist(),
                roots=[[float(z.real),float(z.imag)] for z in roots],
                unstable=bool(np.any(roots.real>0)),
                routh_margin=float(a[1]*a[2]-a[0]*a[3]),
                all_coefficients_positive=bool(np.all(a>0)),
                zero_R_gain_numerator=float(alpha*beta*Cv+T*alpha**2*Gth))
