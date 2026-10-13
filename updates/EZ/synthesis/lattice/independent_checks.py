#!/usr/bin/env python3
"""Independent toy-model checks: exact piecewise-constant propagators.

No experimental input; kBT=a=lambda0=1 unless explicitly changed.
The submitted producer uses solve_ivp; this file does not import producer code.
NumPy is used only by the separate synthetic matrix-bound diagnostic.
"""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path


def entropy(p):
    return -p*math.log(p)-(1-p)*math.log1p(-p)


def cycle(*, u0, U, V, Z, omega, phi, nsteps=32768, lambda0=1.0):
    """Midpoint piecewise-constant approximation; each segment propagated exactly.

    z=F a/(4 kBT). Midpoint transition states put +/-z in directional rates.
    V modulates intracell/intercell saddle energies; Z is a uniform direct force.
    Return displacement, control work and independently quadratured entropy.
    """
    k=lambda0/(4*math.cosh(u0/2))
    dtheta=2*math.pi/nsteps
    dt=dtheta/omega
    segments=[]
    rr, bb=1., 0.
    for i in range(nsteps):
        theta=(i+.5)*dtheta
        u=u0+U*math.cos(theta)
        v=V*math.cos(theta+phi)
        z=Z*math.cos(theta+phi)
        ap=k*math.exp(-v-u/2+z)
        am=k*math.exp(-v+u/2-z)
        bp=k*math.exp(v+u/2+z)
        bm=k*math.exp(v-u/2-z)
        lam=ap+am+bp+bm
        peq=(ap+bm)/lam
        decay=math.exp(-lam*dt)
        shift=peq*(-math.expm1(-lam*dt))
        rr, bb=decay*rr, decay*bb+shift
        segments.append((u,z,ap,am,bp,bm,lam,peq,decay,shift))
    p0=bb/(1-rr)
    p=p0
    dx=0.
    site_work=0.
    force_work=0.
    sigma=0.
    min_sigma=math.inf
    # Three-point Gauss quadrature independent of thermodynamic balance formula.
    nodes=(.5-math.sqrt(15)/10,.5,.5+math.sqrt(15)/10)
    weights=(5/18,4/9,5/18)
    for i,(u,z,ap,am,bp,bm,lam,peq,decay,shift) in enumerate(segments):
        q=decay*p+shift
        int_p=peq*dt+(p-peq)*(-math.expm1(-lam*dt))/lam
        local_dx=((ap-bm)*dt+(bp-am-ap+bm)*int_p)/2
        local_sigma=0.
        for node,weight in zip(nodes,weights):
            pp=peq+(p-peq)*math.exp(-lam*node*dt)
            j1=ap*(1-pp)-am*pp
            j2=bp*pp-bm*(1-pp)
            rate=(j1*math.log(ap*(1-pp)/(am*pp))
                  +j2*math.log(bp*pp/(bm*(1-pp))))
            local_sigma += weight*dt*rate
        dx += local_dx
        force_work += 4*z*local_dx
        next_u=segments[(i+1)%nsteps][0]
        site_work += (q-.5)*(next_u-u)
        sigma += local_sigma
        min_sigma=min(min_sigma,local_sigma)
        p=q
    return dict(delta_x_over_a=dx, periodic_residual=p-p0,
                site_work_over_kBT=site_work,
                direct_force_work_over_kBT=force_work,
                integrated_entropy_over_kB=sigma,
                energy_balance_residual=site_work+force_work-sigma,
                minimum_segment_entropy=min_sigma,nsteps=nsteps)


def phase_fit(*, u0, U, V, Z, omega, nsteps=32768):
    phases=(0.,math.pi/2,math.pi,-math.pi/2)
    runs=[cycle(u0=u0,U=U,V=V,Z=Z,omega=omega,phi=phi,nsteps=nsteps)
          for phi in phases]
    sin=.5*(runs[1]['delta_x_over_a']-runs[3]['delta_x_over_a'])
    cos=.5*(runs[0]['delta_x_over_a']-runs[2]['delta_x_over_a'])
    chi=1/(4*math.cosh(u0/2)**2)
    cg=math.pi/2*chi*U*V
    cd=math.pi/2*chi*U*Z*math.tanh(u0/2)
    rolloff=1/(1+omega**2)
    expected_sin=rolloff*(cg+cd)
    expected_cos=rolloff*(omega*cg-cd/omega)
    for actual,expected in ((sin,expected_sin),(cos,expected_cos)):
        assert math.isclose(actual,expected,rel_tol=.0002,abs_tol=1e-12),(actual,expected)
    assert max(abs(r['periodic_residual']) for r in runs)<2e-11
    assert min(r['minimum_segment_entropy'] for r in runs)>-1e-16
    assert max(abs(r['energy_balance_residual']) for r in runs)<1e-10
    return dict(u0=u0,U=U,V=V,Z=Z,omega=omega,
                measured_sine=sin,measured_cosine=cos,
                predicted_sine=expected_sin,predicted_cosine=expected_cos,
                inferred_geometric=sin+omega*cos,predicted_geometric=cg,
                inferred_force=omega**2*sin-omega*cos,predicted_force=cd,
                runs=runs)


def determinant_checks():
    import numpy as np
    rng=np.random.default_rng(8874)
    rows=[]
    for _ in range(8):
        base=rng.normal(size=(5,5))
        K=base.T@base+np.eye(5)
        A=rng.normal(size=(2,5))
        eig,vec=np.linalg.eigh(K)
        Ki_half=(vec*(1/np.sqrt(eig)))@vec.T
        B=A@Ki_half
        _,s,vh=np.linalg.svd(B,full_matrices=False)
        M=B@B.T
        Ebar=.7
        qc=Ki_half@(math.sqrt(2*Ebar)*vh[0])
        qs=Ki_half@(math.sqrt(2*Ebar)*vh[1])
        actual=abs(float(np.linalg.det(np.column_stack((A@qc,A@qs)))))
        bound=2*Ebar*math.sqrt(float(np.linalg.det(M)))
        cost=float(qc@K@qc+qs@K@qs)/4
        assert abs(actual-bound)<1e-11
        assert abs(cost-Ebar)<1e-11
        maximum_random_ratio=0.
        for _ in range(20):
            rc,rs=rng.normal(size=(2,5))
            cost_random=float(rc@K@rc+rs@K@rs)/4
            achieved=abs(float(np.linalg.det(np.column_stack((A@rc,A@rs)))))
            ratio=achieved/(2*cost_random*math.sqrt(float(np.linalg.det(M))))
            assert ratio<=1+1e-12
            maximum_random_ratio=max(maximum_random_ratio,ratio)
        rows.append(dict(bound=bound,saturated_value=actual,
                         average_elastic_energy=cost,
                         maximum_of_twenty_random_ratios=maximum_random_ratio))
    return rows


def run():
    # Match the proposed phase-odd response with a force-only model.
    u0=.7
    U=.004
    V=.003
    Z=V/math.tanh(u0/2)
    matched=[]
    for omega in (.1,1.,10.):
        geometric=phase_fit(u0=u0,U=U,V=V,Z=0.,omega=omega)
        force=phase_fit(u0=u0,U=U,V=0.,Z=Z,omega=omega)
        assert math.isclose(geometric['measured_sine'],force['measured_sine'],rel_tol=.0002)
        matched.append(dict(omega=omega,geometric=geometric,direct_force=force))
    mixtures=[phase_fit(u0=.7,U=.004,V=.002,Z=.003,omega=omega)
              for omega in (.1,1.,10.)]
    # Exact control rank one (v=constant*u, phi=0) still rectifies at finite rate.
    rank_one=cycle(u0=0.,U=.03,V=.025,Z=0.,omega=1.,phi=0.)
    assert rank_one['delta_x_over_a']>1e-4
    # Discretization convergence of the independently propagated force falsifier.
    convergence=[]
    for nsteps in (8192,16384,32768,65536):
        row=cycle(u0=u0,U=U,V=0.,Z=Z,omega=1.,phi=math.pi/2,nsteps=nsteps)
        convergence.append(row)
    assert abs(convergence[-1]['delta_x_over_a']-convergence[-2]['delta_x_over_a'])<1e-13
    return dict(status='Independent floating toy-model checks passed; no material or novelty validation.',
                algorithm='Exact constant-rate propagator on midpoint-control segments; no solve_ivp or producer import.',
                units='kBT=a=lambda0=1; Z=beta F_amplitude a/4.',
                matched_phase_odd_falsifiers=matched,mixture_discrimination=mixtures,
                rank_one_finite_rate_counterexample=rank_one,
                propagator_convergence=convergence,
                determinant_energy_bound=determinant_checks())


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    result=run()
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],
                      'matched_phase_odd_falsifiers':len(result['matched_phase_odd_falsifiers']),
                      'mixtures':len(result['mixture_discrimination']),
                      'rank_one_displacement':result['rank_one_finite_rate_counterexample']['delta_x_over_a'],
                      'synthetic_energy_fixtures':len(result['determinant_energy_bound'])},indent=2))
