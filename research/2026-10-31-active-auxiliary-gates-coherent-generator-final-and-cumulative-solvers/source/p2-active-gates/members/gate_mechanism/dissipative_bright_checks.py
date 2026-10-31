"""Matrix diagnostics for the uniformly accretive bright/excited decay lemma.
The proof is the Lyapunov inequality, not this floating-point check.
Supports arbitrary common Hamiltonian H, non-Hermitian A with Re(A)>0,
and bounded differential excited Hamiltonian D.
"""
import json
from pathlib import Path
import numpy as np
from scipy.linalg import expm, eigvalsh, svdvals
rng=np.random.default_rng(761050)
n=3;g=0.7;h=1.9;kappa=1.3;detuning=0.8
alpha=min(1.,kappa/(2*h+(kappa/2+detuning)**2/g))
C=np.sqrt((2+alpha)/(2-alpha))
rate=alpha*g/(2*(2+alpha))
I=np.eye(n)
V=np.block([[I,-0.5j*alpha*I],[0.5j*alpha*I,I]])
bound=np.block([[-0.5*alpha*g*I,np.zeros((n,n))],[np.zeros((n,n)),-0.5*kappa*I]])
def herm(scale=1.):
    a=rng.normal(size=(n,n))+1j*rng.normal(size=(n,n))
    a=(a+a.conj().T)/2
    return scale*a/max(abs(eigvalsh(a)))
def sample_generator():
    z=rng.normal(size=(n,n))+1j*rng.normal(size=(n,n))
    U,_=np.linalg.qr(z)
    G=(U*rng.uniform(g,h,size=n))@U.conj().T
    A=G+1j*herm(5.)
    H=herm(200.)
    D=herm(detuning)
    M=np.block([[-1j*H,-1j*A.conj().T],[-1j*A,-1j*(H+D)-kappa/2*I]])
    return M
largest_residual=-np.inf
Utotal=np.eye(2*n,dtype=complex)
trajectory=[]
dt=0.07
for j in range(1000):
    M=sample_generator()
    residual=M.conj().T@V+V@M-bound
    largest_residual=max(largest_residual,float(eigvalsh(residual)[-1]))
    Utotal=expm(M*dt)@Utotal
    if (j+1)%100==0:
        t=(j+1)*dt
        value=float(svdvals(Utotal)[0])
        ceiling=float(C*np.exp(-rate*t))
        assert value<=ceiling+1e-10
        trajectory.append({'time':t,'propagator_norm':value,'theorem_ceiling':ceiling})
assert largest_residual<1e-10
out={'dimension_source':n,'g':g,'h':h,'kappa':kappa,'D_bound':detuning,
     'alpha':alpha,'C':C,'amplitude_rate':rate,
     'largest_lyapunov_residual_eigenvalue':largest_residual,
     'random_switches':1000,'trajectory':trajectory}
Path(__file__).with_name('dissipative_bright_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
