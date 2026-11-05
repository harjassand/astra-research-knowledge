"""Finite classical Hamiltonian-pointer calculation; not hardware validation."""
import json
import numpy as np
from scipy.linalg import expm

def construct(k=1.1, tau=.2, count=8, qvar=1e-12, pvar=1e-4,
              pointer_mass=100., gain=1., gamma=1., mass=1., sigma=1., return_matrices=False):
    # State: x,p,P_1,...,P_m,Q_1,...,Q_m,f; f unknown constant force.
    n=3+2*count; force=n-1; ps=slice(2,2+count); qs=slice(2+count,2+2*count)
    total=np.eye(n); cov=np.zeros((n,n))
    cov[ps,ps]=pvar*np.eye(count); cov[qs,qs]=qvar*np.eye(count)
    width=tau/count
    for j in range(count):
        a=np.zeros((n,n)); a[0,1]=1/mass; a[1,0]=-k
        a[1,1]=-gamma; a[1,force]=1; a[1,2+j]=-gain
        for l in range(count): a[2+count+l,2+l]=1/pointer_mass
        a[2+count+j,0]=gain
        diffusion=np.zeros((n,n)); diffusion[1,1]=2*gamma*sigma*sigma
        block=np.block([[a,diffusion],[np.zeros_like(a),-a.T]])
        e=expm(block*width); step=e[:n,:n]
        gram=e[:n,n:]@step.T
        cov=step@cov@step.T+gram; total=step@total
    read=np.zeros((count,n))
    for j in range(count): read[j,2+count+j]=1/(gain*width)
    means=read@total[:,[0,1,force]]; cross=read@cov[:,:2]
    constraints=np.column_stack([means,cross]); obs_cov=read@cov@read.T
    rhs=np.array([0.,1.,0.,0.,0.])
    cinv_d=np.linalg.solve(obs_cov,constraints)
    weights=cinv_d@np.linalg.solve(constraints.T@cinv_d,rhs)
    variance=float(weights@obs_cov@weights)
    residual=constraints.T@weights-rhs
    result={
      'k':k,'tau':tau,'pointer_count':count,'pointer_q_variance':qvar,
      'pointer_p_variance':pvar,'pointer_mass':pointer_mass,'pulse_gain':gain,
      'weights':weights.tolist(),'variance':variance,
      'constraint_residual_max':float(np.max(np.abs(residual))),
      'max_sine_strength':float(np.exp(-variance/(2*sigma*sigma))),
      'pointer_initial_free_energy_mean':count*pvar/(2*pointer_mass),
      'measurement_backaction_impulse_variance':count*(gain*width)**2*pvar,
      'initial_phase_space_std_product':float(np.sqrt(qvar*pvar)),
      'constraint_singular_values':np.linalg.svd(constraints,compute_uv=False).tolist(),
      'endpoint_noise_covariance':(weights@cross).tolist(),
      'initial_state_gains':(weights@means).tolist(),
      'note':'Classical finite-duration Gaussian model. Exact weights are defined by the linear system; floating values are checks.'
    }
    if return_matrices:
        result['matrices']={'total':total,'covariance':cov,'readout':read,
                            'constraints':constraints,'weights':weights,
                            'observation_covariance':obs_cov}
    return result

if __name__=='__main__':
    results=[construct(k=k,tau=tau) for k in [1.,1.1,1.25] for tau in [.1,.2,.5]]
    assert max(r['constraint_residual_max'] for r in results)<1e-7
    print(json.dumps({'results':results},indent=2))
