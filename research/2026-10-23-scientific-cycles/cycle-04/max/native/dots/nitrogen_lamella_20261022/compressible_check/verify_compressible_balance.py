"""Exact-rational mechanics plus floating actual-source RHS diagnostics.
No compressible or low-Mach trajectory is integrated here.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import importlib.util
import json
import sys
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
from mechanics import mechanical_rhs
sys.path.insert(0, str(HERE.parent/'transport'))
from molecular_transport import BinaryDiffusion, logarithmic_face, maxwell_stefan_flux
sys.path.insert(0, str(HERE.parent/'closure'))
from nasa_secant import nasa7_h_secant
sp = importlib.util.spec_from_file_location('check_signed_kernel', ROOT/'nitrogen_finite_cycle_20261021/signed_trial_helper/helper.py')
module = importlib.util.module_from_spec(sp)
sp.loader.exec_module(module)


def exact_mechanics():
    mu = [F(2,10), F(3,10), F(5,10)]
    width = [F(2,1000), F(3,1000), F(5,1000)]
    velocity = [F(-2), F(1), F(4), F(-1)]
    pressure = [F(110000), F(70000), F(130000)]
    eta = [F(4,3)*F(k,100000) for k in [2,3,4]]
    T = [F(500), F(1300), F(2100)]
    mass = [mu[0]/2, (mu[0]+mu[1])/2, (mu[1]+mu[2])/2, mu[2]/2]
    du = [velocity[i+1]-velocity[i] for i in range(3)]
    tau = [eta[i]*du[i]/width[i] for i in range(3)]
    stress = [pressure[i]-tau[i] for i in range(3)]
    p0 = F(101325)
    force = [p0-stress[0], stress[0]-stress[1], stress[1]-stress[2], stress[2]-p0]
    Q = [F(0), F(17), F(-29), F(0)]
    Udot = sum(-stress[i]*du[i]-(Q[i+1]-Q[i]) for i in range(3))
    Kdot = sum(u*f for u,f in zip(velocity,force))
    Vdot = velocity[-1]-velocity[0]
    residual = Udot+Kdot+p0*Vdot
    diss = [tau[i]*du[i]/T[i] for i in range(3)]
    assert residual == 0 and sum(mass) == sum(mu) and sum(force) == 0
    assert min(diss) > 0
    assert sum((u+F(37))*f for u,f in zip(velocity,force)) == Kdot
    # Independent open-energy/unequal-load identity, retaining both edge signs.
    pl, pr = F(97000), F(102000)
    Fopen = [pl-stress[0], stress[0]-stress[1], stress[1]-stress[2], stress[2]-pr]
    Qopen = [F(23), F(17), F(-29), F(-7)]
    Uopen = sum(-stress[i]*du[i]-(Qopen[i+1]-Qopen[i]) for i in range(3))
    Kopen = sum(u*f for u,f in zip(velocity,Fopen))
    boundary = pl*velocity[0]-pr*velocity[-1]+Qopen[0]-Qopen[-1]
    assert Uopen+Kopen-boundary == 0
    return {'closed_energy_rate_residual_exact': str(residual),
            'general_boundary_power_residual_exact': str(Uopen+Kopen-boundary),
            'node_minus_cell_mass_exact': str(sum(mass)-sum(mu)),
            'net_force_equal_external_pressures_exact': str(sum(force)),
            'viscous_entropy_rates_exact_W_m2_K': list(map(str,diss)),
            'Galilean_constant_velocity_shift_37_m_s_preserves_Kdot': True}


def pressure_face_counterexample():
    # Illustrative two-species positive-state law, not the six-species run.
    XL, XR = np.array([.55,.45]), np.array([.45,.55])
    W = np.array([14.,46.])
    spacing, rho, R = 1.e-4, 1., 8314.46261815324
    pf = logarithmic_face(XL, XR, spacing)
    xf, grad, S = pf['X'][:,0], pf['grad_X'][:,0], float(pf['logmean_sum'][0])
    yf = W*xf/(W@xf)
    jump_logp = .3756
    naive = grad+(xf-yf)*jump_logp/spacing
    fixed = grad+S*(xf-yf)*jump_logp/spacing
    D = np.full((2,2), 1.e-4)
    jbad = maxwell_stefan_flux(xf,naive,D,rho,W)['j'][:,0]
    jgood = maxwell_stefan_flux(xf,fixed,D,rho,W)['j'][:,0]
    force = R/W*(np.log(XR/XL)+jump_logp)
    bad, good = -float(jbad@force), -float(jgood@force)
    assert bad < 0 and good > 0
    return {'scope':'Synthetic two-species equal-temperature positive-state counterexample; no trajectory',
            'pressure_ratio':float(np.exp(jump_logp)), 'logmean_sum':S,
            'naive_raw_gradient_plus_unscaled_pressure_entropy_W_m2_K':bad,
            'corrected_logface_entropy_W_m2_K':good,
            'naive_mass_flux_sum_kg_m2_s':float(jbad.sum()),
            'corrected_mass_flux_sum_kg_m2_s':float(jgood.sum())}


def actual_source_rhs():
    K = module.SignedTrialKernel()
    hot = np.load(ROOT/'nitrogen_admissibility_20261022/recycle_quench/once_through_2700_reference.npz')['hot_Y']
    cold = np.load(ROOT/'nitrogen_admissibility_20261022/recycle_quench/mix_tau_0p0001_trajectory.npz')['return_Y']
    cold = np.maximum(cold,0); cold /= cold.sum()
    alpha = np.array([.2,.5,.8,.35])
    Y = cold[:,None]*(1-alpha)+hot[:,None]*alpha
    # This diagnostic explicitly initializes positive traces; it does not alter any run.
    Y += 3.e-12; Y /= Y.sum(axis=0)
    T = np.array([420.,1100.,2200.,900.])
    P0 = 101325.
    P = P0*np.array([1.012,.996,1.008,.989])
    width = np.array([2.e-5,9.e-5,1.e-4,1.9e-4])
    velocity = np.array([-1.3,2.2,-.6,1.1,.4])
    a = K.evaluate(T,Y,P,strict=True,return_rates=True)
    R_i = K.R/K.W
    cp_i = a['cp_species']; h_i = a['h_species']
    e_i = h_i-R_i[:,None]*T
    cv = np.sum(Y*(cp_i-R_i[:,None]),axis=0)
    rho = a['rho']; mu = rho*width
    m = mechanical_rhs(mu,width,velocity,P,4*a['viscosity']/3,P0,P0)
    X = Y/K.W[:,None]; X /= X.sum(axis=0)
    dx = (width[:-1]+width[1:])/2
    face = logarithmic_face(X[:,:-1],X[:,1:],dx)
    xf = face['X']; S = face['logmean_sum']
    yf = K.W[:,None]*xf/(K.W@xf)
    d = face['grad_X']+S*(xf-yf)*np.diff(np.log(P))/dx
    Tf = (T[:-1]+T[1:])/2
    Pf = (P[:-1]+P[1:])/2
    rf = Pf*(K.W@xf)/(K.R*Tf)
    BD = BinaryDiffusion()
    D = BD.binary_diffusivities(Tf,Pf)
    f = maxwell_stefan_flux(xf,d,D,rf,K.W)
    j = np.zeros((6,5)); j[:,1:4] = f['j']
    hf = np.column_stack([nasa7_h_secant(tl,tr,K.nasa[:,8:15],K.nasa[:,1:8],R_i)
                          for tl,tr in zip(T[:-1],T[1:])])
    _,lam = K.pure_transport(Tf)
    conductivity = (np.sum(xf*lam,axis=0)+1/np.sum(xf/lam,axis=0))/2
    q = -conductivity*np.diff(T)/dx
    Q = np.zeros(5); Q[1:4] = q+np.sum(hf*j[:,1:4],axis=0)
    omega = K.W[:,None]*(K.nu@K.signed_rates(T,rho*Y/K.W[:,None])[0])
    Ydot = -np.diff(j,axis=1)/mu+omega/rho
    edot = (m['cell_internal_mechanical_power']-np.diff(Q))/mu
    Tdot = (edot-np.sum(e_i*Ydot,axis=0))/cv
    reconstructed_edot = cv*Tdot+np.sum(e_i*Ydot,axis=0)
    Udot = float(mu@reconstructed_edot)
    Kdot = float(m['total_kinetic_power'])
    invariant = Udot+Kdot+P0*(velocity[-1]-velocity[0])
    scale = max(1.,abs(Udot),abs(Kdot),abs(P0*(velocity[-1]-velocity[0])))
    # Direct total entropy derivative versus transport, reaction and viscosity terms.
    z = h_i/T-a['s_R']*R_i[:,None]+R_i[:,None]*np.log(X*P/P0)
    direct = float(np.sum(mu*(reconstructed_edot+P*m['width_rate']/mu)/T)
                   -np.sum(mu*z*Ydot))
    visc = float(np.sum(m['cell_viscous_heating_power']/T))
    chem = float(-np.sum(mu*z*omega/rho))
    faces_direct = Q[1:4]*np.diff(1/T)-np.sum(j[:,1:4]*np.diff(z,axis=1),axis=0)
    vdiff = f['w']/xf
    friction = np.zeros(3)
    cface = Pf/(K.R*Tf)
    for i in range(6):
        for k in range(i+1,6):
            friction += xf[i]*xf[k]*(vdiff[i]-vdiff[k])**2/D[i,k]
    certified_faces = q*np.diff(1/T)+cface*K.R*dx/S*friction
    entropy_budget = float(faces_direct.sum()+visc+chem)
    massscale = np.maximum(1.,np.max(abs(Ydot),axis=0))
    assert abs(invariant)/scale < 1.e-10
    assert np.max(abs(Ydot.sum(axis=0))/massscale) < 1.e-10
    assert abs(direct-entropy_budget)/max(1.,abs(entropy_budget)) < 1.e-10
    assert np.max(abs(faces_direct-certified_faces))/max(1.,np.max(abs(certified_faces))) < 1.e-10
    assert np.min(faces_direct) >= 0 and visc > 0 and chem >= 0
    assert cv.min() > 0
    return {'scope':'One deliberately nonuniform-pressure actual-source RHS state; not any trajectory or convergence test',
            'initialization_positive_trace_added_per_species':3.e-12,
            'cell_count':4, 'width_m':float(width.sum()), 'pressure_Pa':P.tolist(),
            'min_cv_J_kg_K':float(cv.min()),
            'node_minus_cell_mass_kg_m2':float(m['node_mass'].sum()-mu.sum()),
            'invariant_rate_residual_W_m2':float(invariant),
            'relative_invariant_rate_residual':float(abs(invariant)/scale),
            'max_local_species_sum_rate_s_inverse':float(np.max(abs(Ydot.sum(axis=0)))),
            'max_mass_flux_sum_kg_m2_s':float(np.max(abs(j.sum(axis=0)))),
            'global_species_source_residual_kg_m2_s':(mu@Ydot.T-(mu/rho)@omega.T).tolist(),
            'viscous_entropy_W_m2_K':visc, 'chemical_entropy_W_m2_K':chem,
            'face_entropy_W_m2_K':faces_direct.tolist(),
            'max_face_entropy_friction_identity_error_W_m2_K':float(np.max(abs(faces_direct-certified_faces))),
            'total_entropy_budget_error_W_m2_K':direct-entropy_budget,
            'total_entropy_rate_W_m2_K':direct,
            'no_Soret_or_Dufour_in_this_actual_source_diagnostic':True}


def main():
    result = {'scope':__doc__, 'exact_rational_mechanics':exact_mechanics(),
              'pressure_face_counterexample':pressure_face_counterexample(),
              'actual_source_single_rhs':actual_source_rhs(),
              'all_declared_algebraic_checks_pass':True}
    result['source_sha256'] = {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                               for p in [HERE/'mechanics.py',HERE/'verify_compressible_balance.py',
                                         HERE.parent/'transport/molecular_transport.py',
                                         ROOT/'nitrogen_finite_cycle_20261021/signed_trial_helper/helper.py']}
    (HERE/'certificate.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__ == '__main__':
    main()
