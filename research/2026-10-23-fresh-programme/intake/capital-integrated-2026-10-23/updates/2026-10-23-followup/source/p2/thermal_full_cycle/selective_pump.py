"""Selective spatial pump synthesis in the exact resonant three-mode model.

All examples are synthetic. This code does not contain measured mode profiles,
material loss data, fabricated structures or experimental heat measurements.
The two pump controls are a conditional interface, not assumed available hardware.
"""
from pathlib import Path
import json
import numpy as np
from scipy.linalg import eigh, solve_continuous_lyapunov
from scipy.optimize import minimize_scalar

HBAR=1.054571817e-34; KB=1.380649e-23
OUT=Path(__file__).resolve().parent


def occupation(thz,t):
    return 1/np.expm1(HBAR*2*np.pi*thz*1e12/(KB*t))


def matrices(vp,vm,rnoise):
    gp=np.outer(vp,vp.conj());gm=np.outer(vm,vm.conj())
    return gp-rnoise*gm,gp+gm


def optimum_at_power(P,A,B,R,alpha=0.,leak=0.):
    """P=u^dag R u; A,B and alpha in explicitly normalized heat units.

    Exact direction optimum at fixed P; R is Hermitian positive definite.
    Requires cold pump heat = alpha*P for every allowed pump direction.
    """
    values,vecs=eigh(A,R+P*B)
    w=vecs[:,-1]
    w=w/np.sqrt(np.vdot(w,R@w).real)
    u=np.sqrt(P)*w
    gross=float(np.vdot(u,A@u).real/(1+np.vdot(u,B@u).real))
    return dict(u=u,gross=gross,net=gross-alpha*P-leak,
                eigenvalue=float(values[-1]),P=float(P))


def q_for_u(u,A,B,R,alpha=0.,leak=0.):
    return (np.vdot(u,A@u).real/(1+np.vdot(u,B@u).real)
            -alpha*np.vdot(u,R@u).real-leak)


def covariance(gplus,gminus):
    """Physical equal linewidth kappa=1; g's normalized to kappa/2.

    Matrix ordering is cold20THz, hot24THz, hot16THz. q is scaled by
    Q0=hbar*omega_c*kappa*Delta_plus/2; work includes BOTH pump channels.
    """
    nc=occupation(20,300);np_=occupation(24,330);nm=occupation(16,330)
    gplus=gplus/2;gminus=gminus/2
    h=np.array([[0,gplus,gminus],[gplus.conjugate(),0,0],
                [gminus.conjugate(),0,0]],complex)
    drift=-np.eye(3)/2-1j*h
    N=solve_continuous_lyapunov(drift,-np.diag([nc,np_,nm]))
    heat=np.array([1.,1.2,.8])*(np.array([nc,np_,nm])-N.diagonal().real)
    # N_ij=<a_j^dag a_i>. Outward central->endpoint current:
    jp=-2*np.imag(gplus*N[1,0])
    jm=-2*np.imag(gminus*N[2,0])
    work=.2*(jp-jm)
    Q0=(nc-np_)/2
    return dict(cold_over_Q0=float(heat[0]/Q0),
                hot_over_Q0=float((heat[1]+heat[2])/Q0),
                work_over_Q0=float(work/Q0),
                energy_balance_error_over_Q0=float(abs(sum(heat)+work)/Q0),
                central_current_error=float(abs(heat[0]-jp-jm)))


def main():
    rng=np.random.default_rng(7212026)
    nc=occupation(20,300);nhp=occupation(24,330);nhm=occupation(16,330)
    rnoise=(nhm-nc)/(nc-nhp)
    # Independent full-covariance check with complex controls and overlaps.
    covariance_errors=[];energy_errors=[];rayleigh_gaps=[]
    for _ in range(200):
        vp=rng.normal(size=3)+1j*rng.normal(size=3)
        vm=rng.normal(size=3)+1j*rng.normal(size=3)
        u=(rng.normal(size=3)+1j*rng.normal(size=3))*rng.uniform(.1,3)
        A,B=matrices(vp,vm,rnoise)
        q=q_for_u(u,A,B,np.eye(3))
        cv=covariance(np.vdot(vp,u),np.vdot(vm,u))
        covariance_errors.append(abs(q-cv['cold_over_Q0']))
        energy_errors.append(cv['energy_balance_error_over_Q0'])
        Z=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3))
        R=Z.conj().T@Z+np.eye(3)
        P=np.vdot(u,R@u).real
        opt=optimum_at_power(P,A,B,R)
        rayleigh_gaps.append(opt['gross']-q)
    assert max(covariance_errors)<1e-9
    assert max(energy_errors)<1e-9
    assert min(rayleigh_gaps)>-1e-10

    vp=np.array([1.,0.],complex);R=np.eye(2)
    alpha=.05;leak=.02;f_c=.1
    rows=[]
    for rho in [0.,.2,.5,.8,.9,.95,.99,1.]:
        vm=np.array([rho,np.sqrt(max(0.,1-rho*rho))],complex)
        A,B=matrices(vp,vm,rnoise)
        lam=float(eigh(A,R,eigvals_only=True)[-1])
        # Bounded numerical power optimization, checked against a dense grid;
        # the direction optimum at each P is exact. No general global P theorem.
        grid=np.r_[0.,np.geomspace(1e-7,100.,2001)]
        vals=np.array([optimum_at_power(p,A,B,R,alpha,leak)['net'] for p in grid])
        idx=int(np.argmax(vals))
        lo=grid[max(0,idx-1)];hi=grid[min(len(grid)-1,idx+1)]
        if idx==0:
            opt=optimum_at_power(0.,A,B,R,alpha,leak)
        else:
            search=minimize_scalar(lambda p:-optimum_at_power(p,A,B,R,alpha,leak)['net'],
                bounds=(lo,hi),method='bounded',options={'xatol':1e-12})
            opt=optimum_at_power(search.x,A,B,R,alpha,leak)
        P=opt['P'];u=opt['u']
        gp=np.vdot(vp,u);gm=np.vdot(vm,u)
        cv=covariance(gp,gm)
        assert abs(opt['gross']-cv['cold_over_Q0'])<1e-10
        absorption=alpha*P/f_c
        wall=cv['work_over_Q0']+absorption
        row=dict(overlap_correlation=rho,
            zero_passive_leak_cold_loss_threshold=lam,
            hard_null_pump_cost_multiplier=(1/(1-rho*rho) if rho<1 else None),
            optimized_P=P,net_heat_over_Q0=opt['net'],
            desired_coupling_squared=float(abs(gp)**2),
            unwanted_coupling_squared=float(abs(gm)**2),
            upper_targeted_direction_heat_at_same_P=float(q_for_u(np.sqrt(P)*vp,A,B,R,alpha,leak)),
            conversion_work_over_Q0=cv['work_over_Q0'],
            total_absorption_over_Q0=absorption,
            wall_COP_before_source_and_control_losses=(opt['net']/wall if wall>0 and opt['net']>0 else None),
            controls_real_imag=[[float(a.real),float(a.imag)] for a in u])
        if rho<1:
            null=np.array([np.sqrt(1-rho*rho),-rho],complex)
            row['hard_null_heat_at_same_P']=float(q_for_u(np.sqrt(P)*null,A,B,R,alpha,leak))
        rows.append(row)
    result=dict(status='CONDITIONAL_PUMP_SYNTHESIS_IN_SYNTHETIC_THREE_MODE_MODEL',
        actual_material_or_controllability_data='UNKNOWN',novelty='UNKNOWN',
        frequencies_THz=dict(cold=20.,hot_upper=24.,hot_lower=16.,pump=4.),
        Tc_K=300.,Th_K=330.,noise_occupation_ratio=rnoise,
        normalized_cold_pump_loss_per_control_power=alpha,
        passive_leak_over_Q0=leak,assumed_cold_deposition_fraction=f_c,
        checks=dict(random_complex_covariance_cases=200,
            maximum_heat_formula_error=max(covariance_errors),
            maximum_energy_balance_error=max(energy_errors),
            minimum_optimized_minus_trial_rayleigh_gap=min(rayleigh_gaps)),
        power_search_scope='P in [0,100], 2001-point logarithmic grid and local refinement',
        cases=rows)
    (OUT/'selective_pump_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
