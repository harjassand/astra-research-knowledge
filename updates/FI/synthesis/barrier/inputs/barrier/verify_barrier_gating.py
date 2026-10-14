#!/usr/bin/env python3
"""Reproducible conditional Landau-model calculations; not material validation.

Dependencies: numpy, scipy, sympy. Run:
    python verify_barrier_gating.py --output results.json

Source for the *illustrative* BaTiO3 parameter screen:
Bar et al., arXiv:2604.26089v1, Table 1 and elastic/electrostrictive
constants in End Notes .1. This combines a frozen-coefficient scalar
coexistence model with ideal symmetric biaxial elastic loading. It is NOT a
fit to, or prediction for, a fabricated device. The coefficient a is
set by exact coexistence, not copied from a measured susceptibility.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import numpy as np
import sympy as sp
from scipy.integrate import quad


def check_symbolic() -> dict:
    q, b, c, u, C, K, alpha = sp.symbols('q b c u C K alpha', positive=True)
    B = sp.symbols('B', positive=True)
    a = 3*b**2/(16*c)
    qb2 = 3*b/(4*c)
    f0 = a*q**2/2-b*q**4/4+c*q**6/6
    assert sp.simplify(f0 - c*q**2*(q**2-qb2)**2/6) == 0
    # Tangent-compensated removal is a nonnegative quartic Bregman divergence.
    d = (q**4-B**4)/4-B**3*(q-B)
    assert sp.factor(d) == (q-B)**2*(3*B**2+2*B*q+q**2)/4
    estar=C*alpha*q**2/(C+K)
    elastic=sp.simplify(C*(estar-alpha*q**2)**2/2+K*estar**2/2)
    ugate=2*alpha**2*C*K/(C+K)
    assert sp.simplify(elastic-ugate*q**4/4) == 0
    assert sp.simplify(sp.diff(elastic,K)-estar**2/2) == 0
    return {'coexistence_factorization': True, 'removal_nonnegative_factorization': True,
            'elastic_elimination': True, 'gate_work_derivative': True}


def audit_path(b: float, c: float, fraction: float, samples: int = 401) -> dict:
    if b <= 0 or c <= 0 or fraction <= 0:
        raise ValueError('b, c, and gate fraction must be positive')
    a=3*b*b/(16*c); qb=np.sqrt(3*b/(4*c)); U=fraction*b
    def f(q: float, u: float, h: float) -> float:
        return a*q*q/2+(u-b)*q**4/4+c*q**6/6-h*q
    def fp(q: float, u: float) -> float:
        return a*q+(u-b)*q**3+c*q**5
    def fpp(q: float, u: float) -> float:
        return a+3*(u-b)*q*q+5*c*q**4
    points=[]
    for t in np.linspace(0,1,samples):
        points.append((0.,t*U,0.))
    for q in np.linspace(0,qb,samples):
        points.append((float(q),U,float(fp(q,U))))
    for u in np.linspace(U,0,samples):
        points.append((float(qb),float(u),float(u*qb**3)))
    max_stationarity=0.; worst_global_excess=0.; min_curvature=np.inf
    for q,u,h in points:
        roots=np.roots([c,0,u-b,0,a,-h])
        real_roots=[float(z.real) for z in roots if abs(z.imag)<1e-7]
        if not real_roots:
            raise AssertionError('No real stationary point found')
        best=min(f(r,u,h) for r in real_roots)
        worst_global_excess=max(worst_global_excess,f(q,u,h)-best)
        max_stationarity=max(max_stationarity,abs(fp(q,u)-h))
        min_curvature=min(min_curvature,fpp(q,u))
    field_work=quad(lambda q:fp(q,U),0,qb,epsabs=1e-11)[0]
    gate_work=quad(lambda u:qb**4/4,U,0,epsabs=1e-11)[0]
    gap_global=a if U>=b else a-9*(b-U)**2/(20*c)
    assert gap_global>0
    assert max_stationarity<1e-10
    assert worst_global_excess<1e-10
    assert abs(field_work+gate_work)<1e-10
    spinodal_q=np.sqrt((3*b-np.sqrt(9*b*b-20*c*a))/(10*c))
    spinodal_h=fp(spinodal_q,0.)
    barrier=b**3/(96*c*c)
    # Direct Hessian check of the spatial failure for a mean-only clamp.
    if U<3*b:
        qg=np.sqrt((3*b-U)/(10*c)); N=4
        base=a-3*b*qg*qg+5*c*qg**4
        H=(base+U*qg*qg)*np.eye(N)+(2*U*qg*qg/N)*np.ones((N,N))
        predicted=a-(3*b-U)**2/(20*c)
        assert abs(np.linalg.eigvalsh(H)[0]-predicted)<1e-10
    return {'parameters':{'a':a,'b':b,'c':c,'q_B':float(qb),'U':U},
            'sampled_control_points':len(points),'max_stationarity_residual':max_stationarity,
            'worst_energy_excess_over_stationary_global_minimum':worst_global_excess,
            'min_sampled_path_curvature':min_curvature,'exact_middle_global_curvature_bound':gap_global,
            'field_work':field_work,'gate_work':gate_work,'net_reversible_work':field_work+gate_work,
            'peak_field':U*qb**3,'field_only_A_spinodal':spinodal_h,
            'peak_field_over_field_only_spinodal':U*qb**3/spinodal_h,
            'ungated_barrier_density':barrier,
            'circulated_work_over_ungated_barrier':field_work/barrier,
            'matched_quadratic_gate': {
                'description':'Constant quadratic gate during traversal, matched global curvature margin; not an optimization over all feedback controls.',
                'k':gap_global-a+9*b*b/(20*c),
                'circulated_work':(gap_global-a+9*b*b/(20*c))*qb*qb/2,
                'peak_field':(gap_global-a+9*b*b/(20*c))*qb,
                'quartic_to_quadratic_work_ratio':field_work/((gap_global-a+9*b*b/(20*c))*qb*qb/2)},
            'global_clamp_counterexample':{
                'homogeneous_energy':'F = sum f0(q_i) + U/(4*N)*(sum q_i^2)^2 - h*sum q_i',
                'nonuniform_mode_curvature_min': a-(3*b-U)**2/(20*c) if U<3*b else a,
                'q_at_nonuniform_mode_min':float(np.sqrt((3*b-U)/(10*c))) if U<3*b else 0.,
                'within_traversed_interval':bool(0 <= (3*b-U)/(10*c) <= qb*qb)}}


def bto_screen(fraction: float) -> dict:
    # f0 = A P^2 + B P^4 + D P^6, versus a P^2/2 - b P^4/4 + c P^6/6.
    B=-1.69e8; D=2.37e9
    b=-4*B; c=6*D; a=3*b*b/(16*c)
    p=np.sqrt(3*b/(4*c)); U=fraction*b
    C11=178e9; C12=96.4e9
    Q12=-0.045; Q11=0.11
    # In-plane exx=eyy=e; zero out-of-plane stress.
    D_biax=C11+C12-2*C12*C12/C11
    C_effective=2*D_biax
    umax=2*C_effective*Q12*Q12
    if U>=umax:
        raise ValueError('Requested gate exceeds ideal fully clamped limit')
    kappa=U/(umax-U) # Effective biaxial reference stiffness ratio K/C_effective.
    e=Q12*p*p/(1+kappa)
    ez=Q11*p*p-2*C12/C11*(e-Q12*p*p)
    strain=np.array([e,e,ez])
    stress=np.array([D_biax*(e-Q12*p*p),D_biax*(e-Q12*p*p),0.])
    spin_q=np.sqrt((3*b-np.sqrt(9*b*b-20*c*a))/(10*c))
    spin_field=a*spin_q-b*spin_q**3+c*spin_q**5
    return {'status':'illustrative frozen-coefficient material screen, not a device prediction',
            'source':'https://arxiv.org/html/2604.26089v1',
            'B_J_m5_Cminus4':B,'D_J_m9_Cminus6':D,
            'polarization_C_per_m2':p,'a_set_by_coexistence':a,
            'required_U_J_m5_Cminus4':U,'fully_biaxially_clamped_U_limit':umax,
            'effective_biaxial_modulus_Pa':C_effective,
            'required_effective_reference_modulus_Pa':kappa*C_effective,
            'ideal_reference_to_active_stiffness_ratio':kappa,
            'middle_global_curvature_fraction':1-2.4*(1-fraction)**2 if fraction<1 else 1,
            'peak_electric_field_V_per_m':U*p**3,
            'voltage_across_500nm_V':U*p**3*500e-9,
            'ideal_circulated_work_J_per_m3':U*p**4/4,
            'active_strain_at_gated_endpoint':strain.tolist(),
            'active_normal_stress_at_gated_endpoint_Pa':stress.tolist(),
            'field_only_scalar_spinodal_V_per_m':spin_field,
            'caveats':['Measured multidimensional constitutive data are required.',
                       'Symmetric local biaxial spring loading and zero out-of-plane stress are assumed.',
                       'No local stiffness gate or recovery efficiency was experimentally obtained.',
                       'No dielectric breakdown, fatigue, domain or rate certification is implied.',
                       'The preprint end-note sixth-order temperature formula is not used; Table 1 supplies D.']}


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=Path('results.json'))
    args=parser.parse_args()
    results={'scope':'Exact scalar mean-field algebra and floating-point diagnostics only.',
             'symbolic':check_symbolic(),
             'normalized_models':[audit_path(3.,1.,fraction) for fraction in (1.,0.55)],
             'BaTiO3_illustrative_screens':[bto_screen(fraction) for fraction in (1.,0.55)]}
    args.output.write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(results,indent=2))

if __name__=='__main__':
    main()
