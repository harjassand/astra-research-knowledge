#!/usr/bin/env python3
"""Physical noise forecast for root's moderate-frequency oscillator dual.

Known H1/modal quantities are supplied here. Noise is propagated from actual
scalar samples through phase cycling and finite-duration sinusoid regression.
This is not end-to-end acquisition. The matched likelihood benchmark is local
and uses the SAME kernel observation covariance and known modal quantities.
"""
import itertools
import json
import math
import time
from pathlib import Path

import numpy as np

ROOT=Path(__file__).resolve().parent


def design(n,gamma):
    rng=np.random.default_rng(417+n)
    lam=np.linspace(1,4,n)
    a=np.ones(n)/np.sqrt(n)
    Q=np.linalg.qr(np.column_stack([a,np.eye(n)[:,:n-1]]))[0]
    if Q[:,0]@a<0:
        Q[:,0]*=-1
    C=Q[:,1:]
    m=n-1
    inds=list(itertools.combinations_with_replacement(range(m),4))
    perms=[np.asarray(list(set(itertools.permutations(i)))) for i in inds]
    pairs=list(itertools.combinations_with_replacement(range(m),2))
    freqs=[]
    for _ in range(3*(len(inds)+1)+50):
        fs=np.sqrt(lam[rng.integers(n,size=3)])*rng.choice([-1,1],3)
        fs+=gamma*rng.uniform(-.25,.25,3)
        freqs.append(fs)
    O=np.linalg.qr(rng.normal(size=(m,m)))[0]
    return lam,a,C,inds,perms,pairs,np.asarray(freqs),O


def matrices(lam,a,C,inds,perms,pairs,freqs,gamma):
    n=len(lam)
    m=n-1
    index={x:i+1 for i,x in enumerate(inds)}
    z=C.T@(lam*a)
    L=np.zeros((len(pairs),len(inds)+1))
    for ri,(i,j) in enumerate(pairs):
        for k in range(m):
            for l in range(m):
                L[ri,index[tuple(sorted([i,j,k,l]))]]+=z[k]*z[l]
    rows=[]
    for fs in freqs:
        ss=1j*np.concatenate(([sum(fs)],fs))
        modal=a[None,:]/(ss[:,None]**2+gamma*ss[:,None]+lam[None,:])
        port=modal@a
        hidden=modal@C
        row=[np.prod(port)]
        for pr in perms:
            row.append(np.sum(np.prod(hidden[np.arange(4)[None,:],pr],axis=1)))
        rows.append(row)
    return np.asarray(rows),L,z


def tensor(O,inds,alpha=.3):
    return np.asarray([alpha]+[alpha*sum(np.prod(O[r,list(i)]) for r in range(len(O))) for i in inds])


def gram_sinusoids(freqs,samples,dt,wash):
    # All four real cubic mixing frequencies, each represented by cosine/sine.
    f1,f2,f3=np.abs(freqs)
    fs=np.abs([f1+f2+f3,f1+f2-f3,f1-f2+f3,-f1+f2+f3])
    target=int(np.argmin(abs(fs-abs(sum(freqs)))))
    center=wash+(samples+1)*dt/2
    def gain(w):
        # Exact finite sample geometric sum, including the observed endpoint.
        return np.sinc(w*samples*dt/(2*np.pi))/np.sinc(w*dt/(2*np.pi))
    def mc(w):
        return np.cos(w*center)*gain(w)
    def ms(w):
        return np.sin(w*center)*gain(w)
    G=np.empty((8,8))
    for i in range(4):
        for j in range(4):
            G[i,j]=.5*(mc(fs[i]-fs[j])+mc(fs[i]+fs[j]))
            G[i+4,j+4]=.5*(mc(fs[i]-fs[j])-mc(fs[i]+fs[j]))
            G[i,j+4]=.5*(ms(fs[j]+fs[i])+ms(fs[j]-fs[i]))
            G[j+4,i]=G[i,j+4]
    eig,V=np.linalg.eigh(G)
    cond=eig[-1]/max(eig[0],1e-300)
    if eig[0]<=1e-12*eig[-1]:
        return None,float(cond)
    inv=(V/eig)@V.T
    sub=inv[np.ix_([target,target+4],[target,target+4])]
    # Coefficients of F=-H3: real = -const*cosine, imaginary = const*sine.
    signs=np.array([-1.,1.])
    if sum(freqs)<0:
        signs[1]*=-1
    return sub*signs[:,None]*signs[None,:],float(cond)


def physical_covariances(lam,a,freqs,gamma,alpha=.3,eta=.05,sigma=1e-5,dt=.05):
    T=20/gamma
    wash=12/gamma
    samples=int(np.ceil(T/dt))
    T=samples*dt
    # Perturbative condition alpha*||xL||^2/(gamma*sqrt(lambda_min)) <= eta.
    state_limit=np.sqrt(eta*gamma*np.sqrt(min(lam))/alpha)
    blocks=[]
    amps=[]
    conditions=[]
    valid=[]
    extrapolation_variance=1025/9
    for index,fs in enumerate(freqs):
        norms=np.linalg.norm(a[None,:]/(-fs[:,None]**2+1j*gamma*fs[:,None]+lam[None,:]),axis=1)
        A=state_limit/(3*norms)
        amps.append(A)
        Gsub,cond=gram_sinusoids(fs,samples,dt,wash)
        conditions.append(cond)
        if Gsub is None:
            blocks.append(None)
            continue
        cov=extrapolation_variance*sigma*sigma/(18*samples*np.prod(A)**2)*Gsub
        blocks.append(cov)
        valid.append(index)
    amps=np.asarray(amps)
    # Eight signs at full amplitude, eight at half amplitude.
    energy=5*T*np.sum(amps*amps) # measured steady portions only
    energy_including_wash=5*(T+wash)*np.sum(amps*amps)
    return blocks,dict(sigma=sigma,dt=dt,gamma=gamma,perturbative_eta=eta,
        linear_state_norm_bound=float(state_limit),measurement_time_per_trial=T,
        settling_time_per_trial=wash,scalar_samples_per_trial=samples,
        trials_per_frequency=16,queried_frequencies=len(freqs),usable_frequencies=len(valid),
        total_trials=16*len(freqs),total_measured_scalars=16*len(freqs)*samples,
        total_physical_duration_excluding_resets=16*len(freqs)*(T+wash),
        input_max_bound=float(np.max(amps.sum(axis=1))),
        tone_amplitude_min=float(amps.min()),tone_amplitude_max=float(amps.max()),
        steady_input_energy_forecast=float(energy),
        total_input_energy_forecast=float(energy_including_wash),
        mixing_regression_condition_max=float(max(conditions)),
        mixing_regression_condition_median=float(np.median(conditions)))


def whiten(A,covs):
    rows=[]
    transforms=[]
    for index,(row,cov) in enumerate(zip(A,covs)):
        if cov is None:
            continue
        eig,V=np.linalg.eigh(cov)
        invroot=(V/np.sqrt(eig))@V.T
        rows.extend(invroot@np.vstack([row.real,row.imag]))
        transforms.append((index,invroot))
    return np.asarray(rows),transforms


def known_alpha_constraints(inds,pairs,m,alpha=.3):
    index={x:i+1 for i,x in enumerate(inds)}
    R=np.zeros((len(pairs)+1,len(inds)+1))
    rhs=np.zeros(len(pairs)+1)
    R[0,0]=1
    rhs[0]=alpha
    for row,(i,j) in enumerate(pairs,1):
        for k in range(m):
            R[row,index[tuple(sorted([i,j,k,k]))]]+=1
        rhs[row]=alpha if i==j else 0
    _,s,Vh=np.linalg.svd(R,full_matrices=True)
    rank=int(sum(s>s[0]*1e-12))
    nullspace=Vh[rank:].T
    particular=np.linalg.lstsq(R,rhs,rcond=1e-12)[0]
    return R,rhs,nullspace,particular


def optimal_dual(F,L,nullspace=None,particular=None):
    N=np.eye(F.shape[1]) if nullspace is None else nullspace
    t0=np.zeros(F.shape[1]) if particular is None else particular
    restricted=F@N
    target=L@N
    U,s,Vh=np.linalg.svd(restricted,full_matrices=False)
    keep=s>s[0]*1e-11
    W=target@((Vh[keep].T/s[keep])@U[:,keep].T)
    offset=L@t0-W@(F@t0)
    return W,float(np.linalg.norm(W@restricted-target)/np.linalg.norm(target)),int(sum(keep)),offset


def unpack(v,pairs,m):
    A=np.zeros((m,m))
    for x,(i,j) in zip(v,pairs):
        A[i,j]=A[j,i]=x
    return A


def aligned_K(Ohat,O,a,C,lam):
    m=len(O)
    ps=np.array(list(itertools.permutations(range(m))))
    G=O@Ohat.T
    scores=np.abs(G[np.arange(m)[None,:],ps]).sum(axis=1)
    perm=ps[np.argmax(scores)]
    est=Ohat[perm].copy()
    signs=np.sign(np.sum(O*est,axis=1))
    est*=signs[:,None]
    U=np.vstack([a,est@C.T])
    return (U*lam)@U.T


def run(n,gamma):
    lam,a,C,inds,perms,pairs,freqs,O=design(n,gamma)
    A,L,z=matrices(lam,a,C,inds,perms,pairs,freqs,gamma)
    covs,ledger=physical_covariances(lam,a,freqs,gamma)
    F,transforms=whiten(A,covs)
    unconstrained_W,unconstrained_residual,unconstrained_rank,_=optimal_dual(F,L)
    constraints_matrix,rhs,N,t0=known_alpha_constraints(inds,pairs,n-1)
    W,residual,rank,offset=optimal_dual(F,L,N,t0)
    cov_target=W@W.T
    unconstrained_cov_target=unconstrained_W@unconstrained_W.T
    t=tensor(O,inds)
    if np.linalg.norm(constraints_matrix@t-rhs)>1e-10:
        raise RuntimeError('known-alpha trace constraint implementation failed')
    target=L@t
    target_matrix=unpack(target,pairs,n-1)
    betas=np.linalg.eigvalsh(target_matrix)
    gap=float(np.min(np.diff(betas))) if len(betas)>1 else float(betas[0])
    frob_weights=np.array([1 if i==j else 2 for i,j in pairs])
    rms_frob=np.sqrt(np.sum(frob_weights*np.diag(cov_target)))
    unconstrained_rms_frob=np.sqrt(np.sum(frob_weights*np.diag(unconstrained_W@unconstrained_W.T)))
    Uphysical=np.vstack([a,O@C.T])
    K=(Uphysical*lam)@Uphysical.T
    rng=np.random.default_rng(551+n)
    ec,Vc=np.linalg.eigh(cov_target)
    rootcov=Vc*np.sqrt(np.maximum(ec,0))
    eu,Vu=np.linalg.eigh(unconstrained_cov_target)
    unconstrained_rootcov=Vu*np.sqrt(np.maximum(eu,0))
    errors=[]
    unconstrained_errors=[]
    for _ in range(60):
        draw=rng.normal(size=len(target))
        noisy=target+rootcov@draw
        _,V=np.linalg.eigh(unpack(noisy,pairs,n-1))
        Khat=aligned_K(V.T,O,a,C,lam)
        errors.append(np.linalg.norm(Khat-K)/np.linalg.norm(K))
        noisy_unconstrained=target+unconstrained_rootcov@draw
        _,V=np.linalg.eigh(unpack(noisy_unconstrained,pairs,n-1))
        Khat=aligned_K(V.T,O,a,C,lam)
        unconstrained_errors.append(np.linalg.norm(Khat-K)/np.linalg.norm(K))
    # Strong matched local likelihood benchmark: known H1 and physical
    # orthogonal realization, with alpha known. Same phase-cycled H3 data.
    # A full ODE fit can exploit additional orders; no fitted run is claimed.
    derivatives=[]
    Kderivatives=[]
    h=1e-5
    for i in range(n-1):
        for j in range(i+1,n-1):
            Rplus=np.eye(n-1);Rminus=np.eye(n-1)
            for R,angle in [(Rplus,h),(Rminus,-h)]:
                R[i,i]=R[j,j]=np.cos(angle)
                R[i,j]=np.sin(angle);R[j,i]=-np.sin(angle)
            derivatives.append((tensor(Rplus@O,inds)-tensor(Rminus@O,inds))/(2*h))
            G=np.zeros((n,n));G[i+1,j+1]=1;G[j+1,i+1]=-1
            Kderivatives.append((G@K-K@G).reshape(-1))
    J=F@np.array(derivatives).T
    H=J.T@J
    Fisher_cov=np.linalg.pinv(H,rcond=1e-12)
    DK=np.array(Kderivatives).T
    likelihood_K_rms=np.sqrt(np.trace(DK@Fisher_cov@DK.T))/np.linalg.norm(K)
    # Broader unknown-node-alpha physical family, matching the original
    # weighted tensor prototype's information rights.
    alpha_derivatives=[np.r_[1.,np.zeros(len(inds))]]
    for row in O:
        alpha_derivatives.append(np.asarray([0.]+[np.prod(row[list(i)]) for i in inds]))
    Junknown=np.column_stack([J,F@np.array(alpha_derivatives).T])
    Hunknown=Junknown.T@Junknown
    cov_unknown=np.linalg.pinv(Hunknown,rcond=1e-12)
    DKunknown=np.column_stack([DK,np.zeros((n*n,n))])
    unknown_alpha_likelihood_K_rms=np.sqrt(np.trace(DKunknown@cov_unknown@DKunknown.T))/np.linalg.norm(K)
    # Calibration sensitivity with exact noiseless H3 but perturbed lambda.
    calibration=[]
    direction=rng.normal(size=n)
    direction/=np.linalg.norm(direction)
    for relative_damping in [1e-4,1e-3,1e-2,.1]:
        est_lam=lam+relative_damping*gamma*direction
        estA,estL,_=matrices(est_lam,a,C,inds,perms,pairs,freqs,gamma)
        estF,_=whiten(estA,covs)
        estW,estres,_,estoffset=optimal_dual(estF,estL,N,t0)
        observed_F=F@t
        est_target=estoffset+estW@observed_F
        _,V=np.linalg.eigh(unpack(est_target,pairs,n-1))
        Khat=aligned_K(V.T,O,a,C,est_lam)
        calibration.append(dict(lambda_error_l2=float(np.linalg.norm(est_lam-lam)),
            error_over_gamma=relative_damping,
            resulting_aligned_K_relative_error=float(np.linalg.norm(Khat-K)/np.linalg.norm(K)),
            target_relative_bias=float(np.linalg.norm(est_target-target)/np.linalg.norm(target)),
            dual_residual=estres))
    return dict(n=n,gamma=gamma,physical_ledger=ledger,
        target_span_residual=residual,weighted_design_rank=rank,
        known_alpha_linear_constraints=int(constraints_matrix.shape[0]),
        known_alpha_constraint_residual=float(np.linalg.norm(constraints_matrix@t-rhs)),
        unconstrained_target_span_residual=unconstrained_residual,
        unconstrained_design_rank=unconstrained_rank,
        unconstrained_relative_rms_target_noise=float(unconstrained_rms_frob/np.linalg.norm(target_matrix)),
        unconstrained_predicted_dual_K_error_median=float(np.median(unconstrained_errors)),
        unconstrained_predicted_dual_K_error_rms=float(np.sqrt(np.mean(np.square(unconstrained_errors)))),
        target_Frobenius_norm=float(np.linalg.norm(target_matrix)),
        target_eigenvalues=betas.tolist(),minimum_hidden_eigenvalue_gap=gap,
        rms_target_Frobenius_noise=float(rms_frob),
        relative_rms_target_Frobenius_noise=float(rms_frob/np.linalg.norm(target_matrix)),
        rms_target_noise_over_minimum_eigenvalue_gap=float(rms_frob/gap),
        predicted_dual_K_error_median=float(np.median(errors)),
        predicted_dual_K_error_rms=float(np.sqrt(np.mean(np.square(errors)))),
        predicted_dual_K_error_90pct=float(np.quantile(errors,.9)),
        matched_local_physical_likelihood_predicted_K_rms=float(likelihood_K_rms),
        physical_likelihood_information_condition=float(np.linalg.cond(H)),
        unknown_alpha_matched_local_physical_likelihood_predicted_K_rms=float(unknown_alpha_likelihood_K_rms),
        unknown_alpha_physical_likelihood_information_condition=float(np.linalg.cond(Hunknown)),
        modal_calibration_sensitivity=calibration)


def main():
    started=time.perf_counter()
    results=[]
    for n,gamma in [(3,.1),(3,.03),(3,.01),(5,.03),(8,.03),(8,.01)]:
        row=run(n,gamma)
        results.append(row)
        print(json.dumps(row),flush=True)
        (ROOT/'dual_noise_partial.json').write_text(json.dumps(results,indent=2)+'\n')
    output=dict(warning='Forecast only; H1/modal data supplied, nonlinear bias not simulated.',
        results=results,runtime_s=time.perf_counter()-started)
    (ROOT/'dual_noise_forecast.json').write_text(json.dumps(output,indent=2)+'\n')


if __name__=='__main__':
    main()
