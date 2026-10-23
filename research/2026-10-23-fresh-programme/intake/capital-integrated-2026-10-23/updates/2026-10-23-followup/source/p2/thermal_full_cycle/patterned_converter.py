"""Static susceptibility pattern: exact scalar overlaps and full resonant network.

This is a synthetic 1D, rotating-wave, flat-Markov-bath calculation, not a
Maxwell/material simulation or experiment. The standing signal modes sin(j*x)
and separately supplied pump cos(r*x) require different boundary phases or
polarization/illumination. Equal optical linewidths and ideal thermal contacts
are explicit assumptions. No fabrication or physical wall COP is established.
"""
from pathlib import Path
import json
import numpy as np
from scipy.linalg import solve_continuous_lyapunov

OUT=Path(__file__).resolve().parent
HBAR=1.054571817e-34; KB=1.380649e-23; C0=299792458.
M_COLD=10; R_PUMP=2; FSR_THz=2.; TC=300.; TH=330.
K_PATTERN=2*(M_COLD+R_PUMP)


def primitive(n,x):
    return x if n==0 else np.sin(n*x)/n


def overlap_on_intervals(j,k,r,edges,signs):
    """Integral sign_profile*cos(r*x)*sin(j*x)*sin(k*x), x in [0,pi]."""
    answer=0.
    for n,coefficient in [(j-k+r,1.),(j-k-r,1.),(j+k+r,-1.),(j+k-r,-1.)]:
        values=primitive(n,edges)
        answer+=coefficient*np.dot(signs,np.diff(values))/4
    return float(answer)


def pattern_edges(jitter_fraction=0.,rng=None):
    # RMS independent error is a fraction of the regular half-domain width.
    interior=(np.arange(K_PATTERN)+.5)*np.pi/K_PATTERN
    if jitter_fraction:
        interior=interior+rng.normal(size=K_PATTERN)*jitter_fraction*np.pi/K_PATTERN
        if not (np.all(np.diff(interior)>0) and interior[0]>0 and interior[-1]<np.pi):
            raise ValueError('Unphysical crossed or external domain boundary')
    return np.r_[0.,interior,np.pi],(-1.)**np.arange(K_PATTERN+1)


def edge_overlaps(nmax,kind='pattern',edges_signs=None):
    if kind=='graded':
        n=M_COLD//R_PUMP
        assert n*R_PUMP==M_COLD
        values=np.zeros(nmax-R_PUMP)
        values[M_COLD-1]=-np.pi/(4*(2*n+1))
        return values
    if kind=='uniform':
        edges,signs=np.array([0.,np.pi]),np.array([1.])
    elif kind=='pattern':
        edges,signs=pattern_edges() if edges_signs is None else edges_signs
    else:
        raise ValueError(kind)
    js=np.arange(1,nmax-R_PUMP+1)
    return np.array([overlap_on_intervals(j,j+R_PUMP,R_PUMP,edges,signs) for j in js])


def graded_profile(theta):
    """Bounded trigonometric polynomial, avoiding removable-node division."""
    n=M_COLD//R_PUMP
    result=np.ones_like(theta)
    for k in range(1,n+1):
        result+=2*(-1.)**k*np.cos(2*k*R_PUMP*theta)
    return (-1.)**n*result/(2*n+1)


def pair_overlaps(kind,edges_signs=None):
    values=np.zeros((R_PUMP-1,R_PUMP-1))
    if kind=='graded':
        return values
    if kind=='uniform':
        edges,signs=np.array([0.,np.pi]),np.array([1.])
    else:
        edges,signs=pattern_edges() if edges_signs is None else edges_signs
    for j in range(1,R_PUMP):
        k=R_PUMP-j
        values[j-1,k-1]=overlap_on_intervals(j,k,R_PUMP,edges,signs)
    return values


def analytic_overlap(j):
    result=0.
    for q in range(1,2*j+5,2):
        if j in (q*(M_COLD+R_PUMP)-R_PUMP,q*(M_COLD+R_PUMP)):
            result-=.5*(-1.)**((q-1)//2)/q
    return result


def occupation(fthz,temp):
    return 1/np.expm1(HBAR*2*np.pi*fthz*1e12/(KB*temp))


def network(amplitude,nmax=40,kind='pattern',edges_signs=None,only_target=False):
    """amplitude=2*g_uniform,target/kappa, kappa=1.

    Heat/work units: hbar*omega_c*kappa. Same amplitude implies same stored
    pump and absorption ONLY if pump normalization and damping are unchanged.
    Pump absorption is reported separately with synthetic alpha and f below.
    """
    js=np.arange(1,nmax+1)
    temps=np.full(nmax,TH);temps[M_COLD-1]=TC
    n=occupation(js*FSR_THz,temps)
    J=edge_overlaps(nmax,kind,edges_signs)
    coupling=amplitude/2*(J/(np.pi/4))*np.sqrt(
        js[:-R_PUMP]*(js[:-R_PUMP]+R_PUMP)/(M_COLD*(M_COLD+R_PUMP)))
    if only_target:
        coupling[js[:-R_PUMP]!=M_COLD]=0.
    # Drop numerical integration roundoff so ideal disconnected components
    # really are disconnected. This is not used to hide fabrication leakage.
    coupling[np.abs(J)<1e-13]=0.
    h=np.zeros((nmax,nmax),complex)
    for j,g in enumerate(coupling):
        h[j,j+R_PUMP]=h[j+R_PUMP,j]=g
    # The physical resonant RWA also contains j+k=r pair creation. Retain it
    # for uniform and imperfect patterns; exact patterns null these overlaps.
    delta=np.zeros((nmax,nmax))
    pair_J=pair_overlaps(kind,edges_signs)
    if not only_target:
        for j in range(1,R_PUMP):
            k=R_PUMP-j
            delta[j-1,k-1]=amplitude/2*(pair_J[j-1,k-1]/(np.pi/4))*np.sqrt(j*k/(M_COLD*(M_COLD+R_PUMP)))
    delta[np.abs(delta)<1e-13]=0.
    hr=h.real
    # Quadratures have [x,p]=i and vacuum variance 1/2.
    drift=np.block([[-np.eye(nmax)/2,hr-delta],[-hr-delta,-np.eye(nmax)/2]])
    max_real_eig=float(np.linalg.eigvals(drift).real.max())
    if max_real_eig>=0:
        raise ValueError('No stable stationary covariance: parametric threshold crossed')
    diffusion=np.diag(np.r_[n+.5,n+.5])
    V=solve_continuous_lyapunov(drift,-diffusion)
    covariance=(V[:nmax,:nmax]+V[nmax:,nmax:]+1j*(V[nmax:,:nmax]-V[:nmax,nmax:]))/2-np.eye(nmax)/2
    anomalous=(V[:nmax,:nmax]-V[nmax:,nmax:]+1j*(V[:nmax,nmax:]+V[nmax:,:nmax]))/2
    heat=js/M_COLD*(n-covariance.diagonal().real)
    currents=np.array([-2*np.imag(g*covariance[j+R_PUMP,j]) for j,g in enumerate(coupling)])
    work_edges=R_PUMP/M_COLD*currents
    creation=-2*np.imag(delta.conj()*anomalous).sum(axis=1)
    work_pairs=float(np.dot(js/M_COLD,creation))
    q0=(occupation(M_COLD*FSR_THz,TC)-occupation((M_COLD+R_PUMP)*FSR_THz,TH))/2
    cold=float(heat[M_COLD-1]/q0)
    work=float((sum(work_edges)+work_pairs)/q0)
    alpha=.05;f=.1;leak=.02
    net=cold-alpha*amplitude**2-leak
    total_abs=alpha/f*amplitude**2
    active=np.flatnonzero(np.abs(coupling)>1e-12)
    return dict(amplitude=float(amplitude),nmax=int(nmax),kind=kind,only_target=only_target,
        cold_heat_over_Q0=cold,conversion_work_over_Q0=work,
        pair_creation_work_over_Q0=float(work_pairs/q0),
        maximum_real_drift_eigenvalue=max_real_eig,
        hot_heat_over_Q0=float((heat.sum()-heat[M_COLD-1])/q0),
        energy_closure_over_Q0=float(abs(heat.sum()+sum(work_edges)+work_pairs)/q0),
        total_pump_absorption_over_Q0=float(total_abs),
        net_cold_heat_over_Q0=float(net),
        wall_COP_before_source_losses=(float(net/(work+total_abs)) if net>0 and work+total_abs>0 else None),
        edge_records=[dict(lower_j=int(j+1),upper_j=int(j+1+R_PUMP),
             overlap=float(J[j]),g_over_kappa=float(coupling[j]),
             photon_current_over_Q0=float(currents[j]/q0),
             work_over_Q0=float(work_edges[j]/q0)) for j in active])


def main():
    exact=edge_overlaps(100)
    formula=np.array([analytic_overlap(j) for j in range(1,99)])
    err=float(np.max(np.abs(exact-formula)))
    assert err<1e-12
    # Independent Gauss-Legendre integration within each smooth sign-domain.
    from numpy.polynomial.legendre import leggauss
    xx,ww=leggauss(64);ed,si=pattern_edges()
    quad=[]
    for j in [1,8,10,12,34,36,58,60]:
        total=0.
        for left,right,sign in zip(ed[:-1],ed[1:],si):
            theta=(left+right)/2+(right-left)*xx/2
            total+=sign*(right-left)/2*np.dot(ww,np.cos(R_PUMP*theta)*np.sin(j*theta)*np.sin((j+R_PUMP)*theta))
        quad.append(abs(total-exact[j-1]))
    assert max(quad)<1e-12

    # The graded profile isolates one edge. Check the product identity and
    # all retained overlaps independently, without dividing by pump nodes.
    theta=np.linspace(0,np.pi,10001)
    nn=M_COLD//R_PUMP
    product_error=float(np.max(np.abs(graded_profile(theta)*np.cos(R_PUMP*theta)
        -np.cos((2*M_COLD+R_PUMP)*theta)/(2*nn+1))))
    assert product_error<1e-13
    assert np.max(np.abs(graded_profile(theta)))<=1+1e-13
    gx,gw=leggauss(600);gt=(gx+1)*np.pi/2;gwt=gw*np.pi/2
    graded_overlap_error=0.
    for j in range(1,99):
        jj=np.dot(gwt,graded_profile(gt)*np.cos(R_PUMP*gt)*np.sin(j*gt)*np.sin((j+R_PUMP)*gt))
        expected=-np.pi/(4*(2*nn+1)) if j==M_COLD else 0.
        graded_overlap_error=max(graded_overlap_error,abs(jj-expected))
    assert graded_overlap_error<1e-12

    rows=[]
    for amp in [.2,.5,1.,2.,3.,5.,10.]:
        for kind,only in [('uniform',True),('uniform',False),('pattern',False),('graded',False)]:
            rows.append(network(amp,40,kind,only_target=only))
    convergence=[network(2.,n,'pattern') for n in [16,24,40,64,88]]
    # Pump work in all-hot higher triplets matters, even though their central
    # cold heat contribution vanishes. Check convergence of that expenditure.
    assert abs(convergence[-1]['conversion_work_over_Q0']-convergence[-2]['conversion_work_over_Q0'])<1e-7
    assert max(a['energy_closure_over_Q0'] for a in rows+convergence)<1e-9

    rng=np.random.default_rng(23102026)
    jitter=[]
    # Full 40-mode covariance on 40 realizations at each fabrication-error
    # level; raw leakage statistics on 400. No empirical fabrication model.
    for sigma in [0.,.001,.005,.01,.02,.05,.1]:
        ratios=[];colds=[];works=[];nets=[];targets=[]
        for sample in range(400):
            edges=pattern_edges(sigma,rng)
            jj=edge_overlaps(40,'pattern',edges)
            target=jj[M_COLD-1]*np.sqrt(M_COLD*(M_COLD+R_PUMP))
            unwanted=jj[M_COLD-R_PUMP-1]*np.sqrt((M_COLD-R_PUMP)*M_COLD)
            ratios.append(abs(unwanted/target));targets.append(abs(jj[M_COLD-1])/.5)
            if sample<40:
                a=network(2.,40,'pattern',edges)
                colds.append(a['cold_heat_over_Q0']);works.append(a['conversion_work_over_Q0']);nets.append(a['net_cold_heat_over_Q0'])
        jitter.append(dict(rms_boundary_error_half_domain_fraction=sigma,
            independent_overlap_realizations=400,full_covariance_realizations=40,
            unwanted_over_desired_amplitude_median=float(np.median(ratios)),
            unwanted_over_desired_amplitude_95_percentile=float(np.quantile(ratios,.95)),
            desired_overlap_fraction_median=float(np.median(targets)),
            cold_heat_over_Q0_mean=float(np.mean(colds)),
            cold_heat_over_Q0_5_percentile=float(np.quantile(colds,.05)),
            net_cold_heat_over_Q0_mean=float(np.mean(nets)),
            conversion_work_over_Q0_mean=float(np.mean(works))))
    nref=3.28
    length=C0/(2*nref*FSR_THz*1e12)
    result=dict(status='SYNTHETIC_SCALAR_PATTERN_AND_FULL_RESONANT_NETWORK',
        measured_material_response='UNKNOWN',fabrication_feasibility='UNKNOWN',novelty='UNKNOWN',
        assumptions=['Sin(j*theta) signal modes; externally supplied cos(r*theta) pump.',
            'Static scalar susceptibility sign(cos(2*(m+r)*theta)); unchanged scalar linear permittivity.',
            'Nondispersive equally spaced frequencies, identical population linewidth kappa.',
            'Only mode m has a cold bath; all other retained modes have hot baths.',
            'Resonant RWA including j+k=r pair creation; physical linewidth and coupling small compared to FSR.',
            'Frequency-independent nonlinear tensor and loss only within declared toy model.',
            'No added domain-wall loss; same pump normalization/damping for uniform versus pattern.',
            'Full pump absorption alpha/f=0.5 per amplitude squared in Q0 units is synthetic.'],
        m=M_COLD,r=R_PUMP,fsr_THz=FSR_THz,Tc_K=TC,Th_K=TH,
        Q0_definition='hbar*omega_c*kappa*(n_c-n_hot_upper)/2',
        synthetic_cold_absorption_coefficient=.05,synthetic_cold_deposition_fraction=.1,
        synthetic_passive_leak_over_Q0=.02,
        target_overlap=-.5,unwanted_lower_overlap=0.,uniform_target_overlap=np.pi/4,
        stored_pump_penalty_at_matched_target_coupling=np.pi**2/4,
        exactly_isolated_graded_profile_pump_penalty=(2*nn+1)**2,
        selection_rule='j=q*(m+r)-r or q*(m+r), q positive odd; J=-(-1)^((q-1)/2)/(2*q)',
        ideal_pair_creation_spatial_overlap='zero for positive j+k=r in this high-spatial-frequency pattern',
        illustrative_scalar_GaAs_geometry=dict(index_assumed=nref,cavity_length_m=length,
            full_pattern_period_m=length/(M_COLD+R_PUMP),
            regular_half_domain_width_m=length/(2*(M_COLD+R_PUMP))),
        checks=dict(maximum_analytic_overlap_error=err,
            maximum_independent_quadrature_error=max(quad),
            maximum_graded_product_identity_error=product_error,
            maximum_graded_overlap_quadrature_error=graded_overlap_error,
            maximum_energy_closure=max(a['energy_closure_over_Q0'] for a in rows+convergence)),
        comparisons=rows,mode_cutoff_convergence=convergence,fabrication_error_scenarios=jitter)
    (OUT/'patterned_converter_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['comparisons','mode_cutoff_convergence']},indent=2))
    print('Representative amp=2 cases:')
    for a in rows:
        if a['amplitude']==2.:
            print(json.dumps({k:v for k,v in a.items() if k!='edge_records'},indent=2))
    print('Cutoff convergence:',[(a['nmax'],a['cold_heat_over_Q0'],a['conversion_work_over_Q0']) for a in convergence])


if __name__=='__main__':
    main()
