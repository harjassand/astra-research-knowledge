"""Model-based sensor-design fixtures, not experimental measurements."""
import numpy as np

def diffusion_gram(n:int,seed:int=314,mode:str='irregular'):
    """Periodic 1D diffusion: kappa*T=0.0003, real Fourier prior modes.
    Each of n hardware units has two permitted sensing sites. Option B
    is a spatially perturbed permutation of option A. Finite diffusion
    attenuates short wavelengths; no target probabilities are supplied.
    """
    rng=np.random.default_rng(seed)
    x=(np.arange(n)+0.35+rng.uniform(-0.15,0.15,n))/n
    if mode=='local': y=(x+rng.uniform(-0.35,0.35,n)/n)%1
    elif mode=='irregular': y=(x[rng.permutation(n)]+rng.uniform(-0.12,0.12,n)/n)%1
    elif mode=='cycle': y=(np.roll(x,-1)+rng.uniform(-0.025,0.025,n)/n)%1
    else: raise ValueError('Unknown mode')
    sites=np.column_stack([x,y]).ravel()
    rows=[np.ones(2*n)]; k=1
    while len(rows)<n:
        attenuation=np.exp(-0.0003*(2*np.pi*k)**2)
        rows.append(np.sqrt(2)*attenuation*np.cos(2*np.pi*k*sites))
        if len(rows)<n: rows.append(np.sqrt(2)*attenuation*np.sin(2*np.pi*k*sites))
        k+=1
    V=np.array(rows)/np.sqrt(n)
    return V.T@V,dict(model='periodic_1d_diffusion',n=n,seed=seed,mode=mode,
                  diffusivity_times_time=0.0003,sites=sites.tolist(),feature_matrix=V.tolist())

def cyclic_gram(n:int):
    """Algebraic stress test only. A cycle-specific DP is stronger than MCMC."""
    V=np.empty((n,2*n))
    for i in range(n):
        V[:,2*i]=np.eye(n)[:,i]; V[:,2*i+1]=np.eye(n)[:,(i+1)%n]
    return V.T@V
