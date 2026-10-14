#!/usr/bin/env python3
"""Independent history-interface diagnostics; no experimental inputs are inferred.

Python >=3.10, NumPy, SciPy. No producer implementation is imported.
"""
from pathlib import Path
import argparse, json, math
import numpy as np
from scipy.linalg import expm
from scipy.integrate import solve_ivp
from scipy import constants as const


def split(U, labels):
    labels=np.asarray(labels)
    diff=labels[:,None]-labels[None,:]
    return {int(m):np.where(diff==m,U,0) for m in np.unique(diff)}


def select(K, parts, ell, x):
    return sum(np.exp(1j*(m+n)*x)*A@K@parts[n].conj().T
               for m,A in parts.items() for n in parts if m-n==ell)


def second_code_coefficients(model, s):
    H=np.diag(model['energies'])+np.diag(model['coupling'],1)+np.diag(model['coupling'],-1)
    pulses=[split(expm(-1j*area*H),[0,1,2]) for area in model['areas']]
    K=select(np.diag([1.,0.,0.]),pulses[0],-1,s/2)
    coefficients=[]
    for h in [-3,-1,1,3]:
        m,n=(h+1)//2,(h-1)//2
        K2=pulses[1][m]@K@pulses[1][n].conj().T
        coefficients.append(np.trace(select(select(K2,pulses[2],1,s/2),pulses[3],-1,s/2)))
    return np.array(coefficients)


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',type=Path,default=Path(__file__).with_name('independent_results.json'))
    args=ap.parse_args();base=Path(__file__).resolve().parent
    out={'status':'INTERNAL ANALYTIC/NUMERICAL DIAGNOSTICS; NO LABORATORY VALIDATION','groups':{}}
    s=.702;a=s/2

    # Exact formula nullspace is evaluated independently of any pulse simulator.
    kappa=math.sin(3*a)/math.sin(a)
    h=np.array([-3,-1,1,3])
    blind=np.array([-1.,kappa,-kappa,1.])/2
    port_matrix=np.exp(1j*np.outer([-a,0.,a],h))
    assert np.linalg.norm(port_matrix@blind)<1e-13
    extra=np.exp(.5j*a*h)@blind
    assert abs(extra)>.01
    out['groups']['exact_three_port_blind_direction']={
        's':s,'coefficient_vector':blind.tolist(),'maximum_old_port_residual':float(np.max(abs(port_matrix@blind))),
        'extra_half_momentum_response':[float(extra.real),float(extra.imag)],
        'proof':'sin(3x) - [sin(3a)/sin(a)] sin(x) vanishes at x=-a,0,a; exact identity, not a numerical proof'}

    # An explicit coherent RWA ladder mixture, not just arbitrary Fourier numbers.
    saved=json.loads((base/'blind_port_search.json').read_text())
    cs=np.array([second_code_coefficients(m,s) for m in saved['models']])
    resid=cs[:,0]+cs[:,3]
    barycentric=np.linalg.solve(np.array([resid.real,resid.imag,np.ones(3)]),np.array([0.,0.,1.]))
    assert np.min(barycentric)>.08
    assert all(m['areas']==[1.,1.,1.,1.] for m in saved['models'])
    mixed=barycentric@cs
    residual=2*(math.cos(3*a)-math.cos(a))*(mixed[0]+mixed[3])
    assert abs(residual)<1e-13 and abs(mixed[3])>.002
    Splus=np.exp(1j*a*h)@mixed;Sminus=np.exp(-1j*a*h)@mixed
    apparent=np.array([(np.exp(1j*a)*Splus-np.exp(-1j*a)*Sminus)/(2j*math.sin(s)),
                       (-np.exp(-1j*a)*Splus+np.exp(1j*a)*Sminus)/(2j*math.sin(s))])
    out['groups']['three_band_physical_pulse_mixture']={
        'weights_defined_by_barycentric_formula':barycentric.tolist(),
        'third_port_residual':[float(residual.real),float(residual.imag)],
        'actual_odd_coefficients':[[float(z.real),float(z.imag)] for z in mixed],
        'apparent_two_band_coefficients':[[float(z.real),float(z.imag)] for z in apparent],
        'nonzero_three_band_leakage_amplitude':float(abs(mixed[3])),
        'scope':'finite floating realization of block-diagonal three-level ladder models under identical four unit-area pulse controls; only static class detunings and dipoles differ; not CaOH+, no certified interval arithmetic'}

    # Finite-band inversion and fixed maximum momentum conditioning certificate.
    rows=[]
    for r in range(1,8):
        n=2*r-1;freq=np.arange(-n,n+1,2)
        xs=np.linspace(-a,a,max(2*r,5))
        design=np.exp(1j*np.outer(xs,freq))
        sv=np.linalg.svd(design,compute_uv=False)
        coefficients=np.array([(-1)**j*math.comb(n,j) for j in range(n+1)],float)
        coefficients/=np.linalg.norm(coefficients)
        worst=np.linalg.norm(design@coefficients)
        bound=math.sqrt(len(xs))*(2*math.sin(a))**n/math.sqrt(math.comb(2*n,n))
        assert worst<=bound+1e-12
        condition_lower=math.sqrt(math.comb(2*n,n))/(2*math.sin(a))**n
        assert sv[0]/sv[-1]>=condition_lower*(1-1e-10)
        rows.append({'bands':r+1,'unknown_coefficients':2*r,'ports':len(xs),
                     'condition_number':float(sv[0]/sv[-1]),'proven_condition_lower_bound':condition_lower,
                     'null_test_vector_norm':float(worst),'upper_bound_on_test_vector_norm':bound})
    out['groups']['fixed_cat_phase_arc_conditioning']=rows

    # Reference agreement is not instrument identification. All known equatorial
    # calibration inputs give the same C=.4 for both legitimate +/-1 POVMs.
    X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]],complex);Z=np.diag([1.,-1.])
    O0=.4*np.kron(X,np.eye(2));O1=np.kron(X,.4*np.eye(2)+.6*Z)
    assert np.max(abs(np.linalg.eigvalsh(O1)))<=1+1e-14
    discrepancy=0.
    for phi in np.linspace(0,2*math.pi,41):
        anc=(np.eye(2)+math.cos(phi)*X+math.sin(phi)*Y)/2
        ref=np.kron(anc,np.eye(2)/2)
        discrepancy=max(discrepancy,abs(np.trace((O1-O0)@ref)))
    anc=(np.eye(2)+X)/2
    science=np.kron(anc,np.diag([1.,0.]))
    difference=np.trace((O1-O0)@science).real
    assert discrepancy<1e-14 and abs(difference-.6)<1e-14
    out['groups']['loaded_reference_instrument_countermodel']={
        'reference_C':.4,'all_reference_phase_scans_discrepancy':float(discrepancy),
        'science_expectation_O0':float(np.trace(O0@science).real),
        'science_expectation_O1':float(np.trace(O1@science).real),
        'difference':float(difference),'meaning':'valid joint POVMs agree on entire loaded reference phase circle but differ on a science-correlated hidden state'}

    # Explicit conditional parking construction using the original allowed D state.
    # Ground RF/Raman swap, followed by old-D-to-vacant-S shelving, avoids a delta-m=3 edge.
    R=np.array([[1,0,1],[0,math.sqrt(2),0],[1,0,-1]],complex)/math.sqrt(2)
    ground_swap=np.array([[0,1,0],[1,0,0],[0,0,1]],complex)
    shelf=np.array([[0,0,1],[0,1,0],[1,0,0]],complex)
    W=shelf@ground_swap@R
    plus=np.array([1,0,1])/math.sqrt(2);minus=np.array([1,0,-1])/math.sqrt(2)
    assert np.linalg.norm(W@plus-[0,1,0])<1e-14
    assert np.linalg.norm(W@minus-[1,0,0])<1e-14
    for dphase in [-20.,0.,20.]:
        light=np.diag([np.exp(-.31j),np.exp(-.31j),np.exp(-1j*dphase)])
        for v in [plus,minus]:assert np.linalg.norm(W.conj().T@light@W@v-np.exp(-.31j)*v)<1e-13
    out['groups']['parking_using_allowed_old_D_state']={
        'states':['S,-1/2','S,+1/2','D,-5/2'],
        'forward_operations':['optical +/- to energy basis','ground-Zeeman swap','D,-5/2 to now-vacant S,-1/2 shelving'],
        'status':'exact conditional unitary construction; RF/Raman selectivity, cat dependence, spectator modes and full round-trip errors unacquired'}

    # Integrate the Schrodinger equation directly for a small rotor. This does
    # not reuse the producer's splitting, eigensystem or frequency filter.
    jmax=4;js=np.arange(jmax+1);N=len(js);sigma=116.2e-15/(2*math.sqrt(2*math.log(2)))
    e=np.r_[.3655*js*(js+1),.3655*js*(js+1)]
    D=np.zeros((2*N,2*N),complex)
    for j in range(jmax):
        g=(j+1)/math.sqrt((2*j+1)*(2*j+3))
        for je,jg in [(j+1,j),(j,j+1)]:D[N+je,jg]=D[jg,N+je]=g
    dipole=4.810962939951982e-31;fluence=275.
    field_peak=math.sqrt(2*fluence/(const.epsilon_0*const.c*math.sqrt(2*math.pi)*sigma))
    theta=dipole*field_peak/const.hbar*2*math.sqrt(math.pi)*sigma
    H0=np.diag(2*math.pi*const.c*100*e*sigma)
    def rhs(u,flat):
        H=H0+theta/(4*math.sqrt(math.pi))*math.exp(-u*u/4)*D
        return (-1j*H@flat.reshape((2*N,2*N))).reshape(-1)
    sol=solve_ivp(rhs,[-8.,8.],np.eye(2*N,dtype=complex).reshape(-1),rtol=2e-11,atol=2e-13,method='DOP853')
    U=sol.y[:,-1].reshape((2*N,2*N));phase=np.exp(8j*np.diag(H0));U=phase[:,None]*U*phase[None,:]
    ref=np.load(base/'repaired_small_rotor_pulse.npy')
    err=float(np.linalg.norm(U-ref,ord=2));unitarity=float(np.linalg.norm(U.conj().T@U-np.eye(2*N),ord=2))
    assert sol.success and err<1e-6 and unitarity<1e-9
    out['groups']['independent_small_rotor_ODE']={'success':sol.success,'steps':len(sol.t),
        'ODE_vs_repaired_400_step_splitting_operator_norm':err,'ODE_unitarity_operator_error':unitarity,
        'scope':'Jmax4,M0 reference equation only; not full CaOH+ or universal numerical certification'}

    # Acquisition, geometry, and emission scales remain conditional arithmetic.
    source_grid=json.loads((base/'replay_repaired/rotor_reference_results.json').read_text())
    costs=[]
    for row in source_grid:
        if row['t3_ps']!=1.:continue
        amplitude=abs(complex(*row['XL']));trials=100/(.4**2*math.sin(s)**2*amplitude**2)
        costs.append({'centre_cm':row['center_cm'],'each_fluence_Jcm2':row['fluence_each_J_cm2'],
                      'coefficient_magnitude':amplitude,'planning_trials_C04':trials,
                      'planning_days_at_assumed_50_Hz':trials/50/86400})
    out['groups']['reference_costs']=costs
    out['groups']['same_physical_model_gates']={
        'grating_cutoff_cm_inverse_for_K0p9k0':.9*3783,
        'Gaussian_spectral_fraction_below_cutoff_at_retuned_centre':.5*math.erfc((3783-.9*3783)/(126.7/(2*math.sqrt(2*math.log(2))))/math.sqrt(2)),
        'one_isotropic_emission_fringe_at_kd0p78':math.sin(.78)/.78,
        'meaning':'illustrative exact integrals/scale arithmetic; actual angular emission, spectral phase, loss, T2, atomic transfer and complete-cycle rate remain unacquired'}
    args.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))


if __name__=='__main__':main()
