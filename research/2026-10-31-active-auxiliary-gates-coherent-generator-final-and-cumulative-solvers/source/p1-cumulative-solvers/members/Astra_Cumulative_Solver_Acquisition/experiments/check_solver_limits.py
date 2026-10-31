"""Small deterministic checks; no empirical independence/novelty claims."""
import json
from pathlib import Path
import numpy as np

rows=[]
for alpha in [1., .1, .001, 1.e-6]:
    for theta in [0., .001, .05, .5, 1.2]:
        u=np.array([1.,0.]); w=np.array([0.,1.])
        v=np.cos(theta)*u+np.sin(theta)*w
        Au=np.eye(2)-(1-alpha)*np.outer(u,u)
        Av=np.eye(2)-(1-alpha)*np.outer(v,v)
        Bhalf=np.diag([alpha**-.5,1.])
        K=Bhalf@Av@Bhalf
        gamma=(1-alpha)**2*np.sin(theta)**2/alpha
        trace_pred=2+gamma
        eigen_pred=(2+gamma+np.sqrt(gamma*(gamma+4)))/2
        ev=np.linalg.eigvalsh(K)
        residual=np.linalg.norm(w-Av@w)
        error=np.linalg.norm(np.linalg.solve(Av,w)-w)
        energy=(np.linalg.solve(Av,w)-w)@Av@(np.linalg.solve(Av,w)-w)
        assert np.isclose(np.trace(K),trace_pred,rtol=1.e-10,atol=1.e-10)
        assert np.isclose(ev[-1],eigen_pred,rtol=1.e-8,atol=1.e-9)
        assert np.isclose(residual,(1-alpha)*abs(np.sin(theta)),rtol=1.e-9,atol=1.e-9)
        assert np.isclose(error,(1-alpha)/alpha*abs(np.sin(theta)),rtol=1.e-8,atol=1.e-8)
        assert np.isclose(energy,(1-alpha)**2/alpha*np.sin(theta)**2,rtol=1.e-8,atol=1.e-8)
        rows.append(dict(alpha=alpha,theta=theta,gamma=float(gamma),condition=float(eigen_pred**2),residual=float(residual),absolute_error=float(error)))
for alpha in [.1,.001,1.e-6]:
    for sigma in [.001,.01,.1]:
        t=1/(alpha+sigma)
        minimax=sigma/(alpha+sigma)
        assert np.isclose(abs(alpha*t-1),minimax)
        assert np.isclose(abs((alpha+2*sigma)*t-1),minimax)
with (Path(__file__).resolve().parents[1]/'results'/'solver_limits_checks.json').open('w') as f:
    json.dump({'status':'passed','rotation_cases':rows,'noise_cases':9,'note':'Binary64 diagnostic of formulas; proofs are in SOLVER_NOISE_AND_ROTATION.txt.'},f,indent=2)
print(json.dumps({'status':'passed','rotation_cases':len(rows),'noise_cases':9}))
