#!/usr/bin/env python3
"""Reproduce ASTRA static-matched spectral-substitution reference calculations.

No output is experimental data or a prediction of superconducting performance.
Optical reference: planar hBN/vacuum, not a fitted kappa-ET heterostructure.
Requires Python 3.10+, NumPy, SciPy. Run: python validate_operation.py
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
from scipy.integrate import simpson, quad_vec
from scipy.linalg import eigh
from optical_model import rp, eps, A, B

OUT = Path(__file__).resolve().parent
LOG: list[str] = []

def check(condition: bool, name: str) -> None:
    if not condition:
        raise AssertionError(name)
    LOG.append('PASS: '+name)

def covariance(K: np.ndarray, masses: np.ndarray) -> np.ndarray:
    """Ground-state displacement covariance in units hbar=1."""
    if np.min(masses) <= 0:
        raise ValueError('Masses must be positive')
    mhi=np.diag(masses**-0.5)
    lam, v=eigh(mhi@K@mhi)
    if np.min(lam) <= 0:
        raise ValueError('Stiffness must be strictly positive definite')
    return 0.5*mhi@(v*(lam**-0.5))@v.T@mhi

def layer_moments(seq: np.ndarray, vals: np.ndarray) -> np.ndarray:
    """Exact integrals of piecewise-constant scalar coefficient times z^0,z^1,z^2.
    Unit-width layers, origin at geometric midplane; caps would add equal terms.
    """
    edges=np.arange(len(seq)+1,dtype=float)-len(seq)/2
    return np.array([np.sum(vals[seq]*(edges[1:]**(n+1)-edges[:-1]**(n+1))/(n+1)) for n in range(3)])

def witness(nu: float, z_nm: float, loss: float=1, n_q: int=10000, ideal: bool=False) -> tuple[float,float]:
    """Evanescent quasistatic dipole-kernel proxy integral q^2 exp(-2qz) Im rp dq.
    Not full radiative LDOS, not the target-material interaction kernel.
    q starts above the vacuum light line over the studied spectral window.
    """
    q=np.geomspace(1.2e6,1e9,n_q)
    weight=q*q*np.exp(-2*q*z_nm*1e-9)
    ia=simpson(weight*rp(nu,q,A,loss=loss,ideal=ideal).imag,x=q)
    ib=simpson(weight*rp(nu,q,B,loss=loss,ideal=ideal).imag,x=q)
    return float(ia),float(ib)

def main() -> None:
    results: dict[str,object] = {'status':'Internally executed reference models; NOT laboratory data; NOT a superconductivity forecast.'}
    signs=1-2*A
    moments=[int(np.sum(signs*np.arange(8)**n)) for n in range(4)]
    check(moments[:3]==[0,0,0], 'equal isotope moments through degree two')
    check(np.array_equal(B,A[::-1]), 'complement equals physical layer-order reversal')
    results['signed_discrete_moments']=moments
    for vals in [np.array([299.,281.]),np.array([2.1,3.7]),np.array([-4.3,9.1])]:
        ma=layer_moments(A,vals);mb=layer_moments(B,vals)
        check(np.allclose(ma,mb,rtol=1e-12,atol=1e-12),'linear-laminate moment equality for '+str(vals.tolist()))
    # A deliberately unbalanced alternative fails the bending-extension matching test.
    naive=np.array([0,0,0,0,1,1,1,1])
    check(abs(layer_moments(naive,np.array([299.,281.]))[1]-layer_moments(naive[::-1],np.array([299.,281.]))[1])>1,
          'counterexample: equal inventory alone does not match extension-bending coupling')

    qs=np.geomspace(1.2e6,4e8,801)
    err=float(np.max(abs(rp(0,qs,A,ideal=True)-rp(0,qs,B,ideal=True))))
    check(err<1e-12,'identical finite-q static reflection in ideal mass-scaled dielectric model')
    emp_rel=float(np.max(abs(rp(0,qs,A)-rp(0,qs,B)))/np.max(abs(rp(0,qs,A))))
    results['ideal_static_reflection_error']=err
    results['empirical_reference_max_DC_relative_difference_on_grid']=emp_rel
    nus=np.linspace(1380.,1580.,121)
    qa=np.geomspace(1.2e6,2e8,101)
    responses=[rp(nus[:,None],qa[None,:],s) for s in [A,B]]
    check(min(float(x.imag.min()) for x in responses)>-1e-10,'nonnegative evanescent Im rp on optical test grid')
    h8=rp(nus,2e7,np.zeros(8,dtype=int),layer_nm=10)
    h1=rp(nus,2e7,np.zeros(1,dtype=int),layer_nm=80)
    check(np.allclose(h8,h1,rtol=1e-9,atol=1e-9),'homogeneous-layer subdivision invariance')
    check(np.max(abs(rp(nus,2e7,A)-rp(nus,2e7,B)))>0.1,'finite-frequency contrast survives static and elastic moment matching')

    rows=[]
    for loss in [1.,3.,6.]:
        for z in [10.,20.,40.,80.]:
            ia,ib=witness(1470,z,loss)
            rows.append({'loss_multiplier':loss,'z_nm':z,'kernel_A_per_m3':ia,'kernel_B_per_m3':ib,'difference_over_mean':2*(ia-ib)/(ia+ib)})
    results['witness_1470cm-1']=rows
    low=witness(1470,20,n_q=10000)
    high=witness(1470,20,n_q=20000)
    conv=float(max(abs(np.array(low)/np.array(high)-1)))
    check(conv<1e-6,'witness q-grid convergence (10000 vs 20000 points)')
    results['witness_relative_quadrature_change']=conv
    results['fixed_q_51_per_um_1470cm-1']={'Im_r_A':float(rp(1470,51e6,A).imag),'Im_r_B':float(rp(1470,51e6,B).imag)}
    # Imaging witness vs equilibrium imaginary-frequency response: different objects.
    xis=np.geomspace(.01,1e5,160);qimag=np.geomspace(1e6,4e8,200)
    xa=rp(1j*xis[:,None],qimag[None,:],A,ideal=True)
    xb=rp(1j*xis[:,None],qimag[None,:],B,ideal=True)
    rel=np.abs(xa-xb)/np.maximum(np.abs((xa+xb)/2),1e-30)
    i,j=np.unravel_index(np.argmax(rel),rel.shape)
    results['imaginary_frequency_grid']={'max_fractional_difference':float(rel[i,j]),'xi_cm-1':float(xis[i]),'q_per_m':float(qimag[j])}
    # Optical witness finite-bandwidth check, independent of unknown target response.
    ns=np.linspace(1430,1510,81)
    va=[];vb=[]
    for nu in ns:
        ia,ib=witness(float(nu),20,n_q=5000)
        va.append(ia);vb.append(ib)
    w=np.exp(-0.5*((ns-1470)/10)**2)
    ia=simpson(np.array(va)*w,x=ns);ib=simpson(np.array(vb)*w,x=ns)
    results['Gaussian_spectral_witness_sigma_10cm-1_at_20nm']={'difference_over_mean':float(2*(ia-ib)/(ia+ib)),'integration_interval_cm-1':[1430,1510]}

    # Pure-mass harmonic bounds: no phenomenological gain or linewidth used here.
    rng=np.random.default_rng(8142026)
    worstlow=1.;worsthigh=1.
    r=1.1
    ma=np.r_[20.,10.+A];mb=np.r_[20.,10.+B]
    for trial in range(60):
        ortho,_=np.linalg.qr(rng.normal(size=(9,9)))
        eigenvalues=np.geomspace(1,10**rng.uniform(1,5),9)
        K=(ortho*eigenvalues)@ortho.T
        ca=covariance(K,ma);cb=covariance(K,mb)
        ev=eigh(cb,ca,eigvals_only=True)
        check(float(ev.min())>=r**-0.5-1e-8 and float(ev.max())<=r**0.5+1e-8,
              'harmonic covariance Loewner bound case '+str(trial))
        worstlow=min(worstlow,float(ev.min()));worsthigh=max(worsthigh,float(ev.max()))
    K=np.diag(np.ones(9)*4)-np.diag(np.ones(8),1)-np.diag(np.ones(8),-1)
    cint,err_int=quad_vec(lambda xi:np.linalg.inv(K+xi*xi*np.diag(ma))/np.pi,0,np.inf,epsabs=1e-11,epsrel=1e-11)
    check(np.allclose(cint,covariance(K,ma),rtol=1e-9,atol=1e-10),'covariance integral identity checked against normal modes')
    check(np.allclose(covariance(K,ma*r),covariance(K,ma)/np.sqrt(r),rtol=1e-10),'uniform mass-scaling equality saturates covariance bound')
    results['harmonic_covariance']={'mass_ratio_bound':r,'lower_factor':r**-0.5,'upper_factor':r**0.5,'random_case_extrema':[worstlow,worsthigh],'integral_error_estimate':float(err_int),'scope':'Common positive stiffness matrix, harmonic displacement covariance. Not a bound on Tc or nonlinear electron response.'}
    # MFM numbers are a conditional design budget, not measured new-system noise.
    k=2.8;f0=77000.;target=2.
    hz_per_pN_per_um=f0/(2*k)*1e-6
    costs=[]
    for sd in [.5,2.,10.]:
        n=int(np.ceil((5*sd/target)**2))
        costs.append({'independent_pair_sd_pN_per_um':sd,'pairs_5sigma':n,'hours_at_assumed_8min_per_pair':n*8/60})
    results['MFM_planning']={'k_N_per_m':k,'f0_Hz':f0,'Hz_per_pN_per_um':hz_per_pN_per_um,'target_pN_per_um':target,'target_Hz':target*hz_per_pN_per_um,'required_standard_error_Hz':target*hz_per_pN_per_um/5,'costs':costs,'caveat':'sigma_pair and acquisition time are assumed examples; independent material pairs, not image pixels.'}

    spectrum=np.column_stack([nus,responses[0][:,30].real,responses[0][:,30].imag,responses[1][:,30].real,responses[1][:,30].imag])
    np.savetxt(OUT/'reference_spectrum.csv',spectrum,delimiter=',',header='wavenumber_cm-1,Re_rA,Im_rA,Re_rB,Im_rB',comments='')
    (OUT/'results.json').write_text(json.dumps(results,indent=2)+'\n')
    (OUT/'validation_log.txt').write_text('\n'.join(LOG)+'\n')
    print('\n'.join(LOG[:12]))
    print(f'{len(LOG)} assertions passed. Results: {OUT / "results.json"}')
    print(json.dumps({key:results[key] for key in ['ideal_static_reflection_error','empirical_reference_max_DC_relative_difference_on_grid','witness_relative_quadrature_change','imaginary_frequency_grid','Gaussian_spectral_witness_sigma_10cm-1_at_20nm','MFM_planning']},indent=2))

if __name__=='__main__':
    main()
