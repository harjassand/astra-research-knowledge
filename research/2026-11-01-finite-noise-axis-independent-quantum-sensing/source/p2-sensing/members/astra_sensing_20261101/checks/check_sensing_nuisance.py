"""Numerical checks of exact identities in sensing_nuisance_no_go.txt.
No stochastic fitting: checks the finite collision algebra and QFI formulas.
Run: python3 check_sensing_nuisance.py
"""
import json
import numpy as np

I=np.eye(2,dtype=complex)
X=np.array([[0,1],[1,0]],complex)
Y=np.array([[0,-1j],[1j,0]],complex)
Z=np.diag([1,-1]).astype(complex)

def check(gamma,dt,theta,omega):
    p=gamma*dt
    U=np.diag(np.exp(-.5j*omega*dt*np.array([1,-1])))
    A=np.cos(theta)*X+np.sin(theta)*Y
    Ad=-np.sin(theta)*X+np.cos(theta)*Y
    Ud=-1j*gamma*dt*Z@U
    K=[np.sqrt(1-p)*U,np.sqrt(p)*A@U]
    Kd=[np.sqrt(1-p)*Ud,np.sqrt(p)*(Ad@U+A@Ud)]
    gram=sum(d.conj().T@k for d,k in zip(Kd,K))
    alpha=sum(d.conj().T@d for d in Kd)
    return dict(beta_norm=float(np.linalg.norm(gram,2)),
                alpha_residual=float(np.linalg.norm(alpha-p*(1-p)*I,2)))

rng=np.random.default_rng(20261101)
algebra=[]
for _ in range(100):
    gamma=float(rng.uniform(.1,3))
    dt=float(rng.uniform(.001,.95/gamma))
    algebra.append(check(gamma,dt,float(rng.uniform(-3,3)),float(rng.uniform(-4,4))))

comparison=[]
gamma=.7
dt=.01
p=gamma*dt
for n in [10,100,1000,10000]:
    T=n*dt
    mean=n*p
    var=n*p*(1-p)
    F=np.array([[T*T,-2*T*mean],[-2*T*mean,4*(mean*mean+var)]])
    inverse=float(np.linalg.inv(F)[0,0])
    formula=1/(T*T)+gamma/(T*(1-p))
    comparison.append(dict(n=n,T=T,inverse_QFI=inverse,
                           formula=formula,relative_residual=abs(inverse-formula)/formula))

out={
  "max_beta_norm":max(x["beta_norm"] for x in algebra),
  "max_alpha_residual":max(x["alpha_residual"] for x in algebra),
  "QFI_comparison":comparison,
}
assert out["max_beta_norm"]<1e-12
assert out["max_alpha_residual"]<1e-12
assert max(x["relative_residual"] for x in comparison)<1e-10
print(json.dumps(out,indent=2))
