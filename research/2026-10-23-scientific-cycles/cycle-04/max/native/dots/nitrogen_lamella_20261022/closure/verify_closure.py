"""Small algebraic certificates only. No trajectory and no fitted transport law."""
import json
from pathlib import Path
import numpy as np
from scipy.optimize import brentq

OUT = Path(__file__).resolve().parent
RU = 8.31446261815324
W = np.array([.028, .032, .014])
RI = RU / W
C0 = np.array([1000., 850., 1500.])
AA = np.array([.12, .17, .08])
HF = np.array([0., 0., 2.e6])

def species(T):
    T = np.asarray(T)
    h = C0 * T[..., None] + .5 * AA * T[..., None]**2 + HF
    cp = C0 + AA * T[..., None]
    s0 = C0 * np.log(T[..., None]) + AA * T[..., None]
    return h, cp, s0

def props(T, Y, P):
    h, cpi, s0 = species(T)
    rm = Y @ RI
    cp = np.sum(Y*cpi, axis=-1)
    x = Y * RI / rm[..., None]
    g_over_t = h/T[..., None] - s0 + RI*np.log(x*P/101325.)
    return rm, cp, h, g_over_t

def logmean(a, b):
    if np.isclose(a, b, rtol=1.e-12, atol=0.):
        return .5*(a+b)
    return (b-a)/np.log(b/a)

def ms_face(YL, YR, TL, TR, P, distance, kappa, dij):
    xL = YL*RI/(YL@RI)
    xR = YR*RI/(YR@RI)
    ell = np.array([logmean(a,b) for a,b in zip(xL,xR)])
    S = ell.sum()
    x = ell/S
    grad = (xR-xL)/distance
    n = len(x)
    mat = np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            if i == j: continue
            mat[i,i] += x[j]/dij[i,j]
            mat[i,j] -= x[i]/dij[i,j]
    A = mat.copy(); rhs = -grad.copy()
    A[-1] = W; rhs[-1] = 0.
    w = np.linalg.solve(A,rhs)
    c = P/(RU*.5*(TL+TR))
    j = W*c*w
    hL, _, sL = species(TL); hR, _, sR = species(TR)
    beta = 1/TR - 1/TL
    hbar = ((hR/TR-sR)-(hL/TL-sL))/beta
    q = -kappa*(TR-TL)/distance
    qe = q+hbar@j
    _,_,_,zL=props(np.array(TL),YL,P)
    _,_,_,zR=props(np.array(TR),YR,P)
    sig = qe*beta-j@(zR-zL)
    v = w/x
    friction = sum(x[i]*x[l]*(v[i]-v[l])**2/dij[i,l]
                   for i in range(n) for l in range(i+1,n))
    certified = kappa*TL*TR/distance*beta**2+c*RU*distance/S*friction
    return j,qe,{'entropy_direct_W_m2K':float(sig),'entropy_friction_W_m2K':float(certified),
                 'relative_entropy_identity_residual':float((sig-certified)/certified),
                 'mass_flux_sum_kg_m2s':float(j.sum()),
                 'MS_equation_max_residual_per_m':float(max(abs(mat@w+grad))),
                 'logmean_normalizer':float(S)}

def algebraic_certificate():
    mu = np.array([1.e-5,1.5e-5,.85e-5])
    T = np.array([2700.,1300.,300.])
    Y = np.array([[.75,.20,.05],[.78,.21,.01],[.79,.209,.001]])
    P = 101325.
    rm,cp,h,_ = props(T,Y,P)
    v = rm*T/P
    L = mu@v
    # Arbitrary conservative face data; this check concerns balances, not entropy.
    j = np.array([[0,0,0],[.003,-.002,-.001],[-.0005,.0007,-.0002],[0,0,0]])
    qe = np.array([0.,1200.,-700.,0.])
    Ydot = -np.diff(j,axis=0)/mu[:,None]
    rdot = Ydot@RI
    A = -np.diff(qe)/mu - np.sum(h*Ydot,axis=1)
    denom = L-np.sum(mu*rm*v/cp)
    pdot = np.sum(mu*(rm*A/cp+T*rdot))/denom
    tdot = (v*pdot+A)/cp
    vdot = (rm*tdot+T*rdot-v*pdot)/P
    hdot = cp*tdot+np.sum(h*Ydot,axis=1)
    udot = hdot-v*pdot-P*vdot
    return {'denominator_m':float(denom),
            'denominator_cv_form_m':float(np.sum(mu*v*(cp-rm)/cp)),
            'closed_width_dot_m_s':float(mu@vdot),
            'global_internal_energy_dot_W_m2':float(mu@udot),
            'global_enthalpy_dot_minus_LPdot_W_m2':float(mu@hdot-L*pdot),
            'max_cell_mass_fraction_sum_dot_per_s':float(max(abs(Ydot.sum(axis=1)))),
            'global_species_mass_dot_kg_m2s':(mu@Ydot).tolist(),
            'pressure_dot_Pa_s':float(pdot),
            'pressure_derivative_EOS_residual_Pa_s':float(pdot-np.sum(mu*(rm*tdot+T*rdot))/L)}

def boundary_failure():
    # Illustrative gas only: NOT a calculation with the project's NASA six-species mechanism.
    rg=287.; c0=900.; a=.12; ratio=.85; hot=2700.; cold=300.; m=1+ratio
    h=lambda t:c0*t+.5*a*t*t
    u=lambda t:(c0-rg)*t+.5*a*t*t
    havg=(h(hot)+ratio*h(cold))/m
    uavg=(u(hot)+ratio*u(cold))/m
    tm=(hot+ratio*cold)/m
    th=brentq(lambda t:h(t)-havg,cold,hot)
    tu=brentq(lambda t:u(t)-uavg,cold,hot)
    return {'scope':'Illustrative ideal gas cp(T)=900+0.12T J/kg/K, Rgas=287 J/kg/K; no chemistry.',
      'constant_pressure_enthalpy_T_K':th,'closed_rigid_internal_energy_T_K':tu,
      'initial_mass_weighted_T_K':tm,'closed_rigid_final_pressure_ratio':tu/tm,
      'constant_pressure_final_width_ratio':th/tm,
      'incorrect_fixed_width_constH_internal_energy_residual_J_per_kg_hot':m*u(th)-m*uavg,
      'constant_pressure_passes_1700K':bool(th<=1700), 'closed_rigid_passes_1700K':bool(tu<=1700)}

def corrected_fick_failure():
    # An algebraic counterexample to *arbitrary unequal* mass-fraction diffusivities.
    # D ratios are deliberately extreme; this is not a physical nitrogen estimate.
    yl=np.array([.36,.50,.14]); yr=np.array([.31,.505,.185])
    dd=np.array([.02,25.,.065]); yf=.5*(yl+yr)
    raw=-dd*(yr-yl); j=raw-yf*raw.sum()
    xl=yl*RI/(yl@RI);xr=yr*RI/(yr@RI)
    sigma=-j@(RI*np.log(xr/xl))
    return {'scope':'Isothermal algebraic mass-conserving corrected-Fick counterexample; arbitrary units for rho D/d.',
      'YL':yl.tolist(),'YR':yr.tolist(),'relative_D':dd.tolist(),'mass_flux':j.tolist(),
      'sum_mass_flux':float(j.sum()),'entropy_production':float(sigma),'entropy_positive':bool(sigma>=0)}

if __name__=='__main__':
    dij=np.array([[0.,1.7e-4,2.8e-4],[1.7e-4,0.,2.5e-4],[2.8e-4,2.5e-4,0.]])
    j,qe,ms=ms_face(np.array([.75,.20,.05]),np.array([.79,.209,.001]),2700.,300.,101325.,1.e-4,.08,dij)
    result={'algebraic_closure':algebraic_certificate(),'entropy_MS_face':ms,
            'boundary_condition_failure':boundary_failure(),'unequal_corrected_fick_failure':corrected_fick_failure()}
    assert result['algebraic_closure']['denominator_m']>0
    assert abs(result['algebraic_closure']['closed_width_dot_m_s'])<1.e-12
    assert abs(result['algebraic_closure']['global_internal_energy_dot_W_m2'])<1.e-8
    assert abs(ms['relative_entropy_identity_residual'])<1.e-12
    assert ms['entropy_direct_W_m2K']>0
    assert result['boundary_condition_failure']['constant_pressure_passes_1700K']
    assert not result['boundary_condition_failure']['closed_rigid_passes_1700K']
    assert result['unequal_corrected_fick_failure']['entropy_production']<0
    (OUT/'certificate.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
