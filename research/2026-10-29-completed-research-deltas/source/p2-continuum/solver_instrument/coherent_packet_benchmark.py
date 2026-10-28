#!/usr/bin/env python3
"""Exact-time product-sine kicks in displaced-Fock packets.

Floating results are diagnostics, not interval certificates. The analytic
Bessel-tail expression bounds branch truncation. No pulse discretization claim.
"""
import json,math,time,hashlib,platform
from pathlib import Path
import numpy as np
from scipy.special import jv,gammaln
from scipy.linalg import eigh,solve
OUT=Path(__file__).parent

def herm(a): return (a+a.conj().T)/2

def gram(a,n,b=None,m=None,zs=1.,zb=1.):
    if b is None:b,m=a,n
    sa,sb=a[:,0,None],b[None,:,0]
    bath=a[:,1:].conj()@b[:,1:].T
    expo=-.5*(np.sum(abs(a)**2,axis=1)[:,None]+np.sum(abs(b)**2,axis=1)[None,:])
    base=np.exp(expo+zs*sa.conj()*sb+zb*bath)
    p10=zs*sb-sa;p01=zs*sa.conj()-sb.conj()
    an=n[:,None]==1;bn=m[None,:]==1
    poly=np.ones_like(base)
    poly=np.where(an&~bn,p10,poly)
    poly=np.where(~an&bn,p01,poly)
    poly=np.where(an&bn,zs+p10*p01,poly)
    return base*poly

def bessel_tail(theta,order):
    x=abs(theta)/2
    if not x:return 0.
    assert x<order+2
    return float(2*np.exp(theta*theta/4+(order+1)*np.log(x)-gammaln(order+2))/(1-x/(order+2)))

def kick(a,n,c,d,theta,order):
    az=[];nz=[];cz=[]
    for ell in range(-order,order+1):
        delta=ell*d
        phase=np.exp(1j*np.imag(a.conj()@delta))
        az.append(a+delta);nz.append(n)
        cz.append(((-1j)**ell*jv(ell,theta)*phase)[:,None]*c)
    return np.vstack(az),np.concatenate(nz),np.vstack(cz)

def compress(a,n,c,tol,max_rank=1024):
    g=herm(gram(a,n));diag=np.maximum(0.,g.diagonal().real.copy())
    weights=np.sum(abs(c)**2,axis=1)
    L=np.zeros((len(n),min(len(n),max_rank)),complex);piv=[]
    for k in range(L.shape[1]):
        p=int(np.argmax(diag*weights))
        if diag[p]*weights[p]<=tol:break
        piv.append(p)
        L[:,k]=(g[:,p]-L[:,:k]@L[p,:k].conj())/np.sqrt(diag[p])
        diag=np.maximum(0.,diag-abs(L[:,k])**2);diag[p]=0.
    ix=np.array(piv,int);sub=g[np.ix_(ix,ix)];rhs=g[ix]@c
    cp=solve(sub,rhs,assume_a='her',check_finite=False)
    d=c.copy();d[ix]-=cp
    ev=np.linalg.eigvalsh(herm(d.conj().T@g@d))
    rec={'before':len(n),'after':len(ix),'selected_gram_condition':float(np.linalg.cond(sub)),
         'rank_cap':max_rank,'rank_cap_hit':len(ix)==L.shape[1],
         'selected_gram_min_eigenvalue':float(np.linalg.eigvalsh(sub)[0]),
         'max_cholesky_diagonal_remainder':float(diag.max()),
         'discarded_map_norm_float':float(np.sqrt(max(0.,ev[-1]))),
         'discarded_squared_eigenvalues_float':ev.tolist(),
         'normal_equation_residual':float(np.linalg.norm(sub@cp-rhs)),
         'diagnostic_only':True}
    return a[ix],n[ix],cp,rec

def coh(alpha,N):
    c=np.empty(N,complex);c[0]=np.exp(-abs(alpha)**2/2)
    for j in range(1,N):c[j]=c[j-1]*alpha/np.sqrt(j)
    return c

def projection(a,n,c,N):
    v=np.zeros((N**a.shape[1],2),complex)
    for aa,nn,cc in zip(a,n,c):
        s=coh(aa[0],N)
        if nn:s=np.r_[0.,np.sqrt(np.arange(1,N))*s[:-1]]-aa[0].conjugate()*s
        for ab in aa[1:]:s=np.kron(s,coh(ab,N))
        v+=np.outer(s,cc)
    return v

def bath_vectors(s):
    if 'continuum' not in s:
        return [np.array([s['eta_bath']*np.exp(1j*s['omega_bath']*tm)]) for tm in s['times']]
    p=s['continuum'];v=p['phase_mass'];dt=s['times'][1]-s['times'][0]
    cov=v*np.exp(1j*p['omega_min']*dt)/(1-1j*p['scale']*dt)**2
    return [np.array([np.sqrt(v),0.]),np.array([cov/np.sqrt(v),np.sqrt(v-abs(cov)**2/v)])]

def axis_mat(state,mat,axis):
    tmp=np.tensordot(mat,state,axes=(1,axis))
    return np.moveaxis(tmp,0,axis)

def fock(N,s):
    q=np.diag(np.sqrt(np.arange(1,N)),1);q=q+q.T
    lam,v=eigh(q);bv=bath_vectors(s);dim=1+len(bv[0])
    ans=np.zeros((N,)*dim+(2,),complex)
    ans[(0,)*dim+(0,)]=1;ans[(1,)+(0,)*(dim-1)+(1,)]=1
    for tm,theta,fb in zip(s['times'],s['areas'],bv):
        fs=s['eta_source']*np.exp(1j*s['omega_source']*tm)
        fv=np.r_[fs,fb]
        vs=[np.exp(1j*np.angle(f)*np.arange(N))[:,None]*v for f in fv]
        shape=(N,)+(1,)*(dim-1)
        ss=np.sin(abs(fs)*lam).reshape(shape)
        bath=np.zeros((N,)*(dim-1))
        for k,f in enumerate(fb):
            shape=(1,)*k+(N,)+(1,)*(dim-2-k)
            bath+=abs(f)*lam.reshape(shape)
        phase=np.exp(-1j*theta*ss*np.sin(bath)[None,...])
        for axis,mat in enumerate(vs):ans=axis_mat(ans,mat.conj().T,axis)
        ans*=phase[...,None]
        for axis,mat in enumerate(vs):ans=axis_mat(ans,mat,axis)
    return ans.reshape(N**dim,2)

def run(settings,order=8,tol=1e-10,prefix='packet',cutoffs=(12,18,24,32,44)):
    bv=bath_vectors(settings)
    a=np.zeros((2,1+len(bv[0])),complex);n=np.array([0,1]);c=np.eye(2,dtype=complex)
    receipt={'settings':settings,'order':order,'compression_tol':tol,
      'scope':'Two exact-time product-sine kicks; no continuous-pulse claim.',
      'arithmetic':'float64 diagnostics; no interval or roundoff certificate',
      'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
      'python':platform.python_version(),'numpy':np.__version__,'kicks':[]}
    for tm,theta,fb in zip(settings['times'],settings['areas'],bv):
        fs=settings['eta_source']*np.exp(1j*settings['omega_source']*tm)
        for sign,subtheta in [(-1,theta/2),(1,-theta/2)]:
            vnorm=float(np.sqrt(np.linalg.eigvalsh(herm(c.conj().T@gram(a,n)@c))[-1]))
            a,n,c=kick(a,n,c,1j*np.r_[fs,sign*fb],subtheta,order)
            a,n,c,rec=compress(a,n,c,tol)
            receipt['kicks'].append({'time':tm,'area':subtheta,'bath_sign':sign,
              'input_map_norm':vnorm,'bessel_tail_formula_float':bessel_tail(subtheta,order),
              'compression':rec})
            print('stage',len(receipt['kicks']),'packets',len(n),'discard',rec['discarded_map_norm_float'],flush=True)
    g=gram(a,n);vgram=herm(c.conj().T@g@c);val,vec=eigh(vgram)
    polar=(vec*(val**-.5))@vec.conj().T;cp=c@polar
    correction=float(np.max(abs(np.sqrt(val)-1)))
    receipt['final_packets']=len(n);receipt['map_squared_singular_values']=val.tolist()
    receipt['polar_correction_operator_norm']=correction
    receipt['tail_sum_float']=float(sum(x['input_map_norm']*x['bessel_tail_formula_float'] for x in receipt['kicks']))
    receipt['discard_sum_float']=float(sum(x['compression']['discarded_map_norm_float'] for x in receipt['kicks']))
    receipt['formal_error_expression']='sum(tail_j*input_map_norm_j)+sum(actual_discard_j)+polar_correction; floating arithmetic still needs enclosure'
    receipt['fock_comparisons']=[]
    for N in cutoffs:
        vf=fock(N,settings);vp=projection(a,n,cp,N);cross=vp.conj().T@vf
        ev=np.linalg.eigvalsh(herm(2*np.eye(2)-cross-cross.conj().T))
        receipt['fock_comparisons'].append({'cutoff_per_oscillator':N,
           'infinite_packet_to_fock_operator_error_float':float(np.sqrt(max(0.,ev[-1]))),
           'squared_error_eigenvalues_float':ev.tolist(),
           'fock_isometry_defect':float(np.linalg.norm(vf.conj().T@vf-np.eye(2))),
           'packet_projection_missing_mass_max_float':float(np.linalg.eigvalsh(herm(np.eye(2)-vp.conj().T@vp))[-1])})
    psrc=herm(cp.conj().T@gram(a,n,zs=0,zb=1)@cp)
    g0=gram(a,n,zs=0,zb=0);bi=a[:,1:].conj()@a[:,1:].T
    psmall=sum(herm(cp.conj().T@(g0*bi**k/math.factorial(k))@cp) for k in range(3))
    pburst=herm(psrc-psmall);pnovac=herm(cp.conj().T@gram(a,n,zs=1,zb=0)@cp)
    receipt['instrument_diagnostics']={
      'source_vacuum_probability_input_0_1':psrc.diagonal().real.tolist(),
      'source_vacuum_and_bath_ge3_probability_input_0_1':pburst.diagonal().real.tolist(),
      'bath_vacuum_probability_input_0_1':pnovac.diagonal().real.tolist(),
      'burst_effect_eigenvalues':np.linalg.eigvalsh(pburst).tolist()}
    # Independent direct photon-number effect in the largest Fock reference.
    N=cutoffs[-1];nbath=a.shape[1]-1
    mask=np.indices((N,)*nbath).sum(axis=0).reshape(-1)>=3
    selected=vf.reshape((N,)*a.shape[1]+(2,))[0].reshape(-1,2)[mask]
    fock_effect=herm(selected.conj().T@selected)
    receipt['instrument_diagnostics']['fock_burst_probability_input_0_1']=fock_effect.diagonal().real.tolist()
    receipt['instrument_diagnostics']['fock_vs_packet_burst_effect_norm']=float(np.linalg.norm(fock_effect-pburst,2))
    np.savez_compressed(OUT/(prefix+'_result.npz'),alpha=a,n=n,c=cp,unpolarized_c=c,gram=g,polar=polar)
    return receipt

if __name__=='__main__':
    t=time.time();settings={'times':[0.,.65],'areas':[1.5,1.2],'eta_source':.8,'eta_bath':.75,'omega_source':1.,'omega_bath':1.6}
    receipt=run(settings);receipt['runtime_seconds']=time.time()-t
    (OUT/'packet_benchmark_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))
