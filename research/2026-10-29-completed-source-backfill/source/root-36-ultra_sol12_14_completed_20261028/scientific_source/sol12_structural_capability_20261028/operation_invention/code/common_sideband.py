"""Pose-free trace beat in a supplied finite-body affine-response model.

All charge, permanent-dipole and gradient-response terms are retained.
An ordinary simultaneous Fourier regression receives the identical data.
This is a simulation/identity, not an apparatus or bandwidth qualification.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1');os.environ.setdefault('OMP_NUM_THREADS','1')
from pathlib import Path
import json,time
import numpy as np
import sympy as s

ROOT=Path(__file__).resolve().parents[1]
G=np.array([[[1,0,0],[0,-1,0],[0,0,0]],[[0,1,0],[1,0,0],[0,0,0]],[[0,0,1],[0,0,0],[1,0,0]]],float)

def rotation(t,rate=3.):
    axis=np.array([1.,2.,3.]);axis/=np.linalg.norm(axis)
    K=np.array([[0,-axis[2],axis[1]],[axis[2],0,-axis[0]],[-axis[1],axis[0],0]])
    angle=2*np.pi*rate*t
    return np.eye(3)[None,:,:]+np.sin(angle)[:,None,None]*K+(1-np.cos(angle))[:,None,None]*(K@K)

def main():
    begin=time.monotonic();N=4096;t=np.arange(N)/N;B=9;beat=17;v=np.array([101,173,257]);u=v+beat
    assert all(np.trace(g)==0 and np.array_equal(g,g.T)for g in G)
    assert np.array_equal(np.array([g@np.array([1,0,0])for g in G]),np.eye(3))
    # Exact carrier support guard, before any simulated outcome.
    nuisance=set(map(int,u))|set(map(int,v))|{0}
    for i in range(3):
        for j in range(3):
            nuisance.add(int(u[i]+v[j]))
            if i!=j:nuisance.add(int(abs(u[i]-v[j])))
            nuisance.add(int(v[i]+v[j]));nuisance.add(int(abs(v[i]-v[j])))
    minimum_gap=min(abs(k-beat)for k in nuisance)
    assert minimum_gap>B and 2*beat>B and N>2*(max(nuisance)+B)
    R=rotation(t);body=np.diag([1.,2.,4.]);alpha=np.einsum('tij,jk,tlk->til',R,body,R)
    rng=np.random.default_rng(20261028);raw=rng.normal(size=(3,3,3));raw=(raw+raw.transpose(0,2,1))/2
    tensor=np.einsum('tia,tjb,tkc,abc->tijk',R,R,R,raw)
    position=.01*np.c_[np.cos(2*np.pi*t),np.sin(2*np.pi*t),np.cos(4*np.pi*t)]
    q=.3
    permanent=np.einsum('tij,j->ti',R,np.array([.2,-.4,.3]))+q*position
    # Translation-dependent induced dipole is linear in the affine gradient.
    tensor+=np.einsum('tij,tk->tijk',alpha,position)
    e=np.cos(2*np.pi*t[:,None]*u)
    gradient=np.einsum('tj,jkl->tkl',np.cos(2*np.pi*t[:,None]*v),G)
    p=permanent+np.einsum('tij,tj->ti',alpha,e)+np.einsum('tijk,tjk->ti',tensor,gradient)
    force=q*e+np.einsum('tij,tj->ti',gradient,p)
    phase=np.exp(-2j*np.pi*beat*t)
    estimate=4*np.mean(force[:,0]*phase)
    assert abs(estimate-7)<2e-11
    # Equally informed ordinary Fourier regression. Orthogonality makes this
    # identical to the lock-in sufficient statistic; no inference advantage.
    X=np.c_[np.ones(N),np.cos(2*np.pi*beat*t),np.sin(2*np.pi*beat*t)]
    beta=np.linalg.lstsq(X,force[:,0],rcond=None)[0]
    ordinary=2*(beta[1]-1j*beta[2]);assert abs(ordinary-estimate)<3e-12
    full_fourier=4*np.fft.rfft(force[:,0])[beat]/N
    assert abs(full_fourier-estimate)<3e-12
    sigma=.02;noise=rng.normal(0,sigma,N);noisy=force[:,0]+noise
    noisy_est=4*np.mean(noisy*phase);ordinary_noisy=2*(np.linalg.lstsq(X,noisy,rcond=None)[0][1]-1j*np.linalg.lstsq(X,noisy,rcond=None)[0][2])
    assert abs(noisy_est-ordinary_noisy)<3e-12
    # Dispersion countercontrol: equal carrier traces do NOT supply matching
    # tensors. A non-tumbling fixed orientation suffices as an allowed case.
    disp=np.array([np.diag([6.,.5,.5]),np.diag([.5,6.,.5]),np.diag([.5,.5,6.])])
    assert np.allclose(np.trace(disp,axis1=1,axis2=2),7)
    columns=np.stack([disp[j,:,j]for j in range(3)])
    pdisp=e@columns
    fdisp=np.einsum('tij,tj->ti',gradient,pdisp)
    dispersion_est=4*np.mean(fdisp[:,0]*phase)
    assert abs(dispersion_est-18)<2e-11
    # Finite-window leakage is not an acquired exact Fourier projection.
    keep=t<.997
    cut=4*np.mean(force[keep,0]*phase[keep])
    # The strongest ordinary comparator is allowed the declared nuisance
    # support and actual timestamps. Full joint Fourier regression repairs
    # the shortened window, rather than being forced to use a biased DFT.
    allowed={beat}
    for carrier in nuisance:
        for shift in range(-B,B+1):allowed.add(abs(carrier+shift))
    freqs=np.array(sorted(allowed-{0}));tc=t[keep]
    design=np.c_[np.ones(len(tc)),np.cos(2*np.pi*tc[:,None]*freqs),np.sin(2*np.pi*tc[:,None]*freqs)]
    fitted,_,rank,sv=np.linalg.lstsq(design,force[keep,0],rcond=1e-12)
    where=int(np.where(freqs==beat)[0][0]);cut_ordinary=2*(fitted[1+where]-1j*fitted[1+len(freqs)+where])
    assert rank==design.shape[1] and abs(cut_ordinary-7)<2e-9
    # Add a forbidden-band nuisance at the readout frequency: no information
    # in this single coefficient distinguishes it from changed trace.
    alias=.1*np.cos(2*np.pi*beat*t)
    contaminated=4*np.mean((force[:,0]+alias)*phase)
    assert abs(contaminated-estimate-.2)<3e-12
    output={'status':'PASS_CONDITIONAL_POSE_FREE_SIDE_BAND_AND_MATCHED_ORDINARY_CONTROL',
      'samples':N,'observation_period_model_units':1,'coefficient_bandwidth':B,'rotation_cycles':3,
      'gradient_carriers':v.tolist(),'uniform_carriers':u.tolist(),'trace_beat':beat,
      'minimum_nuisance_carrier_gap':minimum_gap,'true_trace':7.,'estimate_real':estimate.real,'estimate_imag':estimate.imag,
      'ordinary_Fourier_regression_real':ordinary.real,'ordinary_Fourier_regression_imag':ordinary.imag,
      'ordinary_complete_Fourier_real':full_fourier.real,'ordinary_complete_Fourier_imag':full_fourier.imag,
      'noise_std_per_force_sample':sigma,'noisy_trace_real':noisy_est.real,
      'trace_real_standard_deviation':np.sqrt(8/N)*sigma,
      'ordinary_and_lockin_same_noisy_statistic':True,
      'dispersion_equal_individual_traces':[7,7,7],'dispersion_counterestimate':dispersion_est.real,
      'incomplete_window_fraction':float(sum(keep)/N),'incomplete_window_estimate':[cut.real,cut.imag],
      'ordinary_correct_timestamps_estimate':[cut_ordinary.real,cut_ordinary.imag],
      'ordinary_joint_regression_columns':design.shape[1],'ordinary_joint_regression_rank':int(rank),
      'ordinary_joint_regression_condition':float(sv[0]/sv[-1]),
      'forbidden_band_counterestimate':[contaminated.real,contaminated.imag],
      'carrier_model_and_bandwidth_physically_acquired':False,
      'scope':'Supplied periodic bandlimited instantaneous finite-body linear-response model; no measured material, true polarizability trace/void certificate or apparatus acquired.',
      'seconds':time.monotonic()-begin}
    np.savez(ROOT/'results/common_sideband_timeseries.npz',time=t,force=force,alpha=alpha,position=position,noisy_readout=noisy)
    (ROOT/'results/common_sideband.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(output,indent=2))

if __name__=='__main__':main()
