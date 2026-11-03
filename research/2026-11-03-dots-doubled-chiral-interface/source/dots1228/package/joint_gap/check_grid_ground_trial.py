import numpy as np,json
from pathlib import Path
N=2; ns=np.arange(-N,N+1)
def vector(S):
 t=2*np.pi*np.arange(S)/S;k=np.arange(S)
 jump=np.where(2*((k[:,None]-k[None,:])%S)<S,1.,-1.)
 a=.3*np.sin(t[:,None])+.4*np.cos(t[None,:])+.2*jump
 psi=np.stack([np.cos(a),1j*np.sin(a)],axis=-1)
 # This unit-vector amplitude has a moving discontinuity, so derivative-only estimates fail.
 coeff=np.fft.fft2(psi,axes=(0,1))/S**2
 return coeff[ns[:,None]%S,ns[None,:]%S,:].reshape(-1)
v=vector(2048)
results={str(S):{'unnormalized_error':float(np.linalg.norm(vector(S)-v)),'cutoff_success_probability':float(np.linalg.norm(vector(S))**2)} for S in [16,32,64,128,256,512]}
r={'N':N,'reference_success_probability':float(np.linalg.norm(v)**2),'grid_results':results,'scope':'Small moving-wall vector Fourier test, not the astronomical Wilson state preparation.'}
Path(__file__).with_name('grid_ground_trial_results.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
