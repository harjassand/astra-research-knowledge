"""Verify pairwise stationary Fisher identities for a nonlinear driven diffusion on T^2.

All stationary densities are computed by solving an explicitly constructed
finite-state (positive-rate) finite-volume generator; this is a consistent
O(h^2) approximation of the given continuum diffusion, not an exact sampler.
No trajectory is observed. This is a numerical diagnostic, not experimental
verification of a scientific claim or a rate guarantee.
"""
from __future__ import annotations
import argparse
import json
from itertools import combinations
import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import spsolve

D_TRUE = np.array([[0.65, 0.12], [0.12, 0.50]])
CONTROLS = np.array([[0., 0.], [0.8, 0.15], [-0.25, 0.85]])


def field(x,y):
    bx=-1.3*np.sin(x)+0.67*np.sin(y)+0.37*np.cos(x-y)+0.28*np.sin(2*y+x)
    by=-0.85*np.sin(y)-0.46*np.sin(x)+0.21*np.cos(x+2*y)+0.43*np.sin(2*x-y)
    return bx,by


def generator(n, u):
    h=2*np.pi/n
    x,y=np.meshgrid(-np.pi+h*np.arange(n), -np.pi+h*np.arange(n), indexing='ij')
    bx,by=field(x,y)
    bx=bx+u[0];by=by+u[1]
    rates=[(+1,0,(D_TRUE[0,0]-D_TRUE[0,1])/h**2+bx/(2*h)),
            (-1,0,(D_TRUE[0,0]-D_TRUE[0,1])/h**2+-bx/(2*h)),
            (0,+1,(D_TRUE[1,1]-D_TRUE[0,1])/h**2+by/(2*h)),
            (0,-1,(D_TRUE[1,1]-D_TRUE[0,1])/h**2+-by/(2*h)),
            (+1,+1,np.full((n,n),D_TRUE[0,1]/h**2)),
            (-1,-1,np.full((n,n),D_TRUE[0,1]/h**2))]
    src=np.arange(n*n).reshape((n,n))
    rows=[];cols=[];data=[];loss=np.zeros((n,n))
    for di,dj,r in rates:
        assert float(np.min(r)) >= 0, "Discretization does not have nonnegative rates"
        # src[i,j] jumps to (i+di,j+dj) -- roll array indexes to neighbor ids
        dst=np.roll(src,(-di,-dj),axis=(0,1))
        rows.extend(dst.ravel().tolist())
        cols.extend(src.ravel().tolist())
        data.extend(r.ravel().tolist())
        loss+=r
    rows.extend(src.ravel().tolist());cols.extend(src.ravel().tolist());data.extend((-loss).ravel().tolist())
    L=sp.coo_matrix((data,(rows,cols)),shape=(n*n,n*n)).tocsr()
    return L


def stationary(n,u):
    L=generator(n,u).tolil()
    L[0,:]=np.ones(n*n)
    rhs=np.zeros(n*n);rhs[0]=1.
    p=spsolve(L.tocsr(),rhs)
    assert p.min()>0, (p.min(),p.max())
    assert abs(p.sum()-1)<1e-10
    return p.reshape((n,n))


def grad(z,h):
    return np.stack(((np.roll(z,-1,0)-np.roll(z,+1,0))/(2*h),
                     (np.roll(z,-1,1)-np.roll(z,+1,1))/(2*h)),axis=-1)


def fish(p_i, p_j, u_i, u_j, h, weights=None):
    """M_ij=E_p_i[q(log r) w w^T], g=E_p_i[q(log r) delta_u dot w]"""
    log_r=np.log(p_i/p_j)
    w=grad(log_r,h)
    if weights is None: weights=[np.ones_like(log_r)]
    mats=[];rhs=[]
    for q in weights:
        v=p_i*q
        M=np.einsum('ij,ijm,ijn->mn',v,w,w)
        g=(u_i-u_j)@np.einsum('ij,ijm->m',v,w)
        mats.append([M[0,0],2*M[0,1],M[1,1]])
        rhs.append(g)
    return np.array(mats),np.array(rhs),float(np.max(np.linalg.norm(w,axis=-1)))


def drift_reconstruction(n, dens):
    """Reconstruct b(x) from d+1 exact stationary grid laws and known D.

    Differentiation and discrete PDE truncation make this a consistency test;
    sites with small score-ratio singular values are explicitly excluded.
    """
    h=2*np.pi/n
    def trace_d_hessian_over_p(p):
        p_xx=(np.roll(p,-1,0)-2*p+np.roll(p,+1,0))/h**2
        p_yy=(np.roll(p,-1,1)-2*p+np.roll(p,+1,1))/h**2
        p_xy=(np.roll(np.roll(p,-1,0),-1,1)-np.roll(np.roll(p,-1,0),+1,1)
             -np.roll(np.roll(p,+1,0),-1,1)+np.roll(np.roll(p,+1,0),+1,1))/(4*h*h)
        return (D_TRUE[0,0]*p_xx+2*D_TRUE[0,1]*p_xy+D_TRUE[1,1]*p_yy)/p
    scores=[grad(np.log(p),h) for p in dens]
    W=np.stack([scores[i]-scores[0] for i in [1,2]],axis=-2)
    H0=trace_d_hessian_over_p(dens[0])
    rhs=np.stack([trace_d_hessian_over_p(dens[i])-H0-
                  np.einsum('ijm,m->ij',scores[i],CONTROLS[i])
                  for i in [1,2]],axis=-1)
    sv=np.linalg.svd(W,compute_uv=False)
    condition=sv[...,0]/np.maximum(sv[...,1],1e-300)
    mask=(condition<20) & (sv[...,1]>0.08)
    if np.sum(mask)==0: return {'fraction_cells_rank_stable':0.}
    b_hat=np.linalg.solve(W[mask],rhs[mask][...,None])[...,0]
    x,y=np.meshgrid(-np.pi+h*np.arange(n),-np.pi+h*np.arange(n),indexing='ij')
    bx,by=field(x,y)
    b=np.stack((bx,by),axis=-1)[mask]
    return {'fraction_cells_rank_stable':float(mask.mean()),
            'drift_relative_rms_error_on_rank_stable_cells':float(
                np.linalg.norm(b_hat-b)/np.linalg.norm(b)),
            'median_local_score_ratio_cond':float(np.median(condition[mask]))}


def run(n):
    h=2*np.pi/n
    dens=[stationary(n, u) for u in CONTROLS]
    mat=[];rhs=[];pair_details=[]
    for i,j in combinations(range(3),2):
        f,g,wmax=fish(dens[i],dens[j],CONTROLS[i],CONTROLS[j],h)
        mat.extend(f); rhs.extend(g)
        resid=float((f@np.array([D_TRUE[0,0],D_TRUE[0,1],D_TRUE[1,1]])-g)[0])
        pair_details.append({'pair':[i,j],'identity_residual_discretized':resid,'max_score_difference':wmax})
    mat=np.array(mat);rhs=np.array(rhs)
    recovered=np.linalg.solve(mat,rhs)
    Dhat=np.array([[recovered[0],recovered[1]],[recovered[1],recovered[2]]])
    p0,p1=dens[0],dens[1]
    logr=np.log(p1/p0)
    z=(logr-np.mean(logr))/np.std(logr)
    # Distinct conditional-level weighted Fisher equations from ONLY TWO conditions.
    # Use Chebyshev powers of the centered/scaled log-density ratio.
    qs=[np.ones_like(z),z,z*z,z**3,z**4,z**5,z**6]
    f2,g2,_=fish(p1,p0,CONTROLS[1],CONTROLS[0],h,weights=qs)
    # Scale all rows for numerical condition; least squares overdetermined
    s=np.linalg.norm(f2,axis=1)
    c=f2/s[:,None];target=g2/s
    est2=np.linalg.lstsq(c,target,rcond=None)[0]
    Dtwo=np.array([[est2[0],est2[1]],[est2[1],est2[2]]])
    # All-pair equations with single row each: same information n+1 snapshots
    return {'grid_N_per_side':n,'cells':n*n,'numerical_convergence_order_expected':2,
       'true_D':D_TRUE.tolist(),'recovered_D_three_regimes':Dhat.tolist(),
       'three_regime_relative_error':float(np.linalg.norm(Dhat-D_TRUE)/np.linalg.norm(D_TRUE)),
       'three_regime_linear_system_cond':float(np.linalg.cond(mat)),
       'recovered_D_two_regimes_weighted':Dtwo.tolist(),
       'two_regime_relative_error':float(np.linalg.norm(Dtwo-D_TRUE)/np.linalg.norm(D_TRUE)),
       'two_regime_weighted_rank':int(np.linalg.matrix_rank(c)),
       'two_regime_cond':float(np.linalg.cond(c)),
       'two_regime_numerical_eq_residual':(c @ est2 -target).tolist(),
       'non_affine_logratio_oscillation':float(logr.max()-logr.min()),
       'pair_details':pair_details,'drift':drift_reconstruction(n,dens)}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--sizes',nargs='+',type=int,default=[24,40,64,96]);ap.add_argument('--output',default='torus_results.json');a=ap.parse_args()
    out={'description':__doc__,'results':[]}
    for n in a.sizes:
        v=run(n);out['results'].append(v);print(json.dumps(v,indent=2))
    with open(a.output,'w') as f:json.dump(out,f,indent=2)

if __name__=='__main__':main()
