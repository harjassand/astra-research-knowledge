#!/usr/bin/env python3
"""Vectorized independent quantum-propagation perturbation audit.
Uses the exact real-controlled full Hamiltonian at the nominal geometry,
then perturbs physical emitter positions, coupling intensity and onsite energies.
"""
import json,runpy,numpy as np
from scipy.integrate import solve_ivp
s=runpy.run_path('/mnt/data/astra_temporal_dark_inband_certified_20261027.py')
w,wt,v,x,T,mu,N,freq,controls=[s[n] for n in ['w','wt','v','x','T','mu','N','freq','controls']]
settings=[('exact',[0,0,0],1.,0.),('outer_0.001',[-.001,0,.001],1.,0.),('outer_0.01',[-.01,0,.01],1.,0.),('outer_0.03',[-.03,0,.03],1.,0.),('central_0.01',[0,.01,0],1.,0.),('amplitude_0.001',[0,0,0],1.001,0.),('amplitude_0.01',[0,0,0],1.01,0.),('onsite_0.001',[0,0,0],1.,.001),('onsite_0.01',[0,0,0],1.,.01)]
Ws=[]
for name,dx,scale,shift in settings:
    xpos=x+np.array(dx)
    Ws.append(scale*np.vstack([np.sqrt(wt)[:,None]*v[:,None]*np.exp(1j*sgn*w[:,None]*xpos[None,:]) for sgn in (+1,-1)]))
Ws=np.stack(Ws); count=len(Ws);dim=5+len(freq)
D=np.zeros((count,5));D[:,3]=[z[3] for z in settings]

def rhs(t,flat):
    y=flat.reshape(count,dim);u=y[:,:5];r=y[:,5:]
    _,_,H,*_=controls(t)
    Hwork=u@H.T+D*u
    coup=np.einsum('ci,cij->cj',r,Ws.conj())
    rd=np.einsum('cj,cij->ci',u[:,2:],Ws) # W has shape c,rad,3; cji -> ci
    du=-1j*(Hwork+np.concatenate([np.zeros((count,2),complex),coup],axis=1))
    dr=-1j*(freq[None,:]*r+rd)
    return np.concatenate([du,dr],axis=1).reshape(-1)

Y0=np.zeros((count,dim),complex);Y0[:,0]=1
sol=solve_ivp(rhs,(0,T),Y0.reshape(-1),method='DOP853',atol=2e-11,rtol=1e-9,max_step=.028)
assert sol.success
Z=sol.y[:,-1].reshape(count,dim)
expected=np.zeros(dim,complex);expected[1]=np.exp(-1j*mu*T)
results=[]
for i,(name,dx,scale,shift) in enumerate(settings):
    z=Z[i]
    results.append({'case':name,'full_state_error':float(np.linalg.norm(z-expected)),
      'final_radiation_norm':float(np.linalg.norm(z[5:])),
      'target_probability':float(abs(z[1])**2),
      'final_norm':float(np.linalg.norm(z))})
Lipschitz=T*np.sqrt(2*s['eta']**2*(s['cutoff']**4/280))
out={'position_perturbation_Lipschitz_coefficient':Lipschitz,'results':results,
'scope':'Vectorized finite-mode quadrature diagnostic; continuum position bound follows separately from Duhamel with phase derivatives; no experimental tolerances implied.'}
open('/mnt/data/astra_temporal_dark_inband_perturbation_20261027.json','w').write(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
