import json
import numpy as np
from scipy.optimize import linear_sum_assignment
rng=np.random.default_rng(19453)
res=[]
for d in [2,3,4,6,10,20]:
    worst=0.; identityerr=0.
    for trial in range(12):
        Z=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d))
        U,R=np.linalg.qr(Z); U=U@(np.diag(np.diag(R)/abs(np.diag(R))).conj())
        rows,cols=linear_sum_assignment(-U.real)
        p_dist=2*d-2*U[rows,cols].real.sum()
        formula=2*d-2*np.sum(abs(U)**2*U).real
        Delta=np.zeros((d*d,d));Delta[np.arange(d)*(d+1),np.arange(d)]=1
        actual=np.linalg.norm(np.kron(U,U)@Delta@U.conj().T-Delta)**2
        identityerr=max(identityerr,abs(actual-formula))
        worst=max(worst,p_dist-formula)
    assert worst<1e-9 and identityerr<1e-9
    res.append({'dimension':d,'trials':12,'maximum_identity_error':identityerr,'maximum_inequality_violation':worst})
# A coordinate phase shows why the mixed rather than plain cubic representation is necessary.
z=np.exp(2j*np.pi/3)
assert abs(z**3-1)<1e-12 and abs(z*z*np.conj(z)-1)>1
print(json.dumps({'random_unitary_tests':res,'cube_root_phase_gate':'passed'},indent=2))
