"""End-to-end finite-sample weak stationary-generator identification.

Learns a *supplied* 8-term Fourier basis of the nonlinear drift and all three
entries of an unknown constant 2x2 diffusion matrix from ONLY iid stationary
position samples and known additive force controls. Uses weak generator moments
E[(b+u)·grad f+D:Hess f]=0. NO estimated density scores or trajectories.

Data simulator samples from numerical stationary distributions of the periodic
second-order Markov spatial approximation, optionally with cell jitter.
This is not physical validation and not generic function-free recovery.
"""
import argparse,json,time
import numpy as np
from general_identity_torus import stationary, CONTROLS, D_TRUE, field

THETA_TRUE=np.array([-1.3,.67,.37,.28,-.85,-.46,.21,.43])
DIM_PARAMETERS=11


def bases(x,y):
    b=np.stack([np.sin(x),np.sin(y),np.cos(x-y),np.sin(x+2*y),
                np.sin(y),np.sin(x),np.cos(x+2*y),np.sin(2*x-y)],axis=-1)
    return b


def wavevectors(kmax=3):
    return [(i,j) for i in range(-kmax,kmax+1) for j in range(-kmax,kmax+1)
            if (i>0 or (i==0 and j>0))]


def build_equations(regimes, controls=CONTROLS,kmax=3):
    mat=[];rhs=[]
    ks=wavevectors(kmax)
    for xs,u in zip(regimes,controls):
        x=xs[:,0];y=xs[:,1]
        b=bases(x,y)
        for k,l in ks:
            arg=k*x+l*y
            for f, gfac in ((np.sin(arg),np.cos(arg)),(np.cos(arg),-np.sin(arg))):
                # weak equation from sin/cos test f: grad f=(k,l)*gfac
                grad_x=k*gfac; grad_y=l*gfac
                features=np.column_stack((b[:,:4]*grad_x[:,None],b[:,4:]*grad_y[:,None],
                                          -k*k*f,-2*k*l*f,-l*l*f))
                mat.append(features.mean(axis=0))
                rhs.append(-float((u[0]*grad_x+u[1]*grad_y).mean()))
    return np.array(mat),np.array(rhs)


def fit(regimes):
    a,g=build_equations(regimes)
    z=np.linalg.lstsq(a,g,rcond=None)[0]
    D=np.array([[z[-3],z[-2]],[z[-2],z[-1]]])
    return {'drift_coeff_rel_error':float(np.linalg.norm(z[:8]-THETA_TRUE)/np.linalg.norm(THETA_TRUE)),
      'D_rel_error':float(np.linalg.norm(D-D_TRUE)/np.linalg.norm(D_TRUE)),
      'D_min_eigenvalue':float(np.linalg.eigvalsh(D).min()),
      'design_rank':int(np.linalg.matrix_rank(a)),
      'design_cond':float(np.linalg.cond(a)),
      'joint_params_rel_error':float(np.linalg.norm(z-np.r_[THETA_TRUE,D_TRUE[0,0],D_TRUE[0,1],D_TRUE[1,1]])/np.linalg.norm(np.r_[THETA_TRUE,D_TRUE[0,0],D_TRUE[0,1],D_TRUE[1,1]])),
      'lstsq_residual':float(np.linalg.norm(a@z-g)),
      'estimated_D':D.tolist()}


def take(p,n,rng,jitter=True):
    side=len(p);h=2*np.pi/side
    ij=np.column_stack(np.unravel_index(rng.choice(side*side,n,p=p.ravel()),p.shape))
    xs=-np.pi+h*ij
    if jitter:xs+=rng.uniform(-h/2,h/2,size=xs.shape)
    return xs


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--grid',type=int,default=128)
    ap.add_argument('--sizes',nargs='+',type=int,default=[1000,5000,20000,80000]);ap.add_argument('--reps',type=int,default=10)
    ap.add_argument('--output',default='stein_results.json');args=ap.parse_args()
    rng=np.random.default_rng(21195)
    start=time.perf_counter()
    densities=[stationary(args.grid,u) for u in CONTROLS]
    equilibrate_cpu=time.perf_counter()-start
    # The learned model uses only sampled coordinates and known control labels,
    # not the numerical stationary mass arrays (which are used only to sample).
    out={'grid':args.grid,'equilibrium_PDE_solve_seconds':equilibrate_cpu,
         'assumed_drift_basis_functions':8,'unknown_generator_parameters':11,
         'wavevectors':len(wavevectors(3)),'test_functions_per_regime':2*len(wavevectors(3)),
         'rows':[],'aggregate':[]}
    for n in args.sizes:
        temp=[]
        for i in range(args.reps):
            start=time.perf_counter()
            regimes=[take(p,n,rng) for p in densities]
            fitinfo=fit(regimes)
            fitinfo.update({'n_per_regime':n,'total_snapshot_samples':3*n,
                            'sample_and_fit_seconds':time.perf_counter()-start})
            temp.append(fitinfo);out['rows'].append(fitinfo)
        summary={'n_per_regime':n,'successes':len(temp),'total_snapshot_samples':3*n}
        for k in ['drift_coeff_rel_error','D_rel_error','design_cond','sample_and_fit_seconds','D_min_eigenvalue']:
            v=np.array([r[k] for r in temp]);summary[k+'_mean']=float(v.mean());summary[k+'_median']=float(np.median(v))
        out['aggregate'].append(summary);print(json.dumps(summary,indent=2))
    with open(args.output,'w') as f:json.dump(out,f,indent=2)

if __name__=='__main__':main()
