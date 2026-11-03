import numpy as np,json
from pathlib import Path
S=64;N=3;kappa=1e-4
t=2*np.pi*np.arange(S)/S
a=.3*np.sin(t)+.2*np.where(np.arange(S)<S//2,1.,-1.)
W=np.zeros((2*S,2*S),complex)
for j,x in enumerate(a):W[2*j:2*j+2,2*j:2*j+2]=[[np.cos(x),-np.sin(x)],[np.sin(x),np.cos(x)]]
H0=np.kron(np.eye(S)-np.ones((S,S))/S,np.eye(2))+np.kron(np.eye(S),np.diag([0.,1.]))
H=W@H0@W.conj().T
omega=W@np.kron(np.ones(S)/np.sqrt(S),[1.,0.])
ns=np.arange(-N,N+1)
J=np.kron(np.exp(1j*t[:,None]*ns[None,:])/np.sqrt(S),np.eye(2))
v=J.conj().T@omega;success=float(np.vdot(v,v).real);v/=np.linalg.norm(v)
Hc=J.conj().T@H@J+kappa*np.kron(np.diag(ns**2),np.eye(2));e,u=np.linalg.eigh(Hc)
p=float(abs(np.vdot(u[:,0],v))**2)
accept=u[:,e<.5]@(u[:,e<.5].conj().T@v)
r={'scope':'Finite one-rotor even-pair toy validating trial/filter algebra, not Wilson endpoint.','grid':S,'cutoff':N,'cutoff_success':success,'ground_energy':float(e[0]),'first_excited_energy':float(e[1]),'gap':float(e[1]-e[0]),'trial_ground_overlap_squared':p,'known_threshold':.5,'states_below_threshold':int(sum(e<.5)),'ideal_filter_success':float(np.linalg.norm(accept)**2),'ideal_filter_ground_fidelity':float(abs(np.vdot(u[:,0],accept/np.linalg.norm(accept)))**2)}
Path(__file__).with_name('trial_ground_filter_results.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
