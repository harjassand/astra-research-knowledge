from fractions import Fraction as F
from pathlib import Path
import itertools,json
import numpy as np

HERE=Path(__file__).resolve().parent
def norm1(X):return float(np.sum(np.abs(np.linalg.eigvalsh((X+X.conj().T)/2))))

rows=[]
for M in [1,2,5,20]:
    beta=F(1,100);e0=F(1,10)
    q=[F(1,20),F(1,10)];w=[F(1,3),F(2,3)]
    actual=beta+(1-beta)*sum(ww*(1-(1-qq)**M) for ww,qq in zip(w,q))
    assert actual<=M*e0+beta
    rows.append({'payloads':M,'exact_shared_calibration_Pauli_halfdiamond':str(actual),'claimed_upper':str(M*e0+beta)})

# Independent exact counterexample: shared all-Z branch versus independent
# copies of the single-use average, assessed on product Bell references.
b=F(1,10)
shared=[1-b,0,0,b];iid=[(1-b)**2,b*(1-b),b*(1-b),b*b]
distance=sum(abs(x-y) for x,y in zip(shared,iid))/2
assert distance==2*b*(1-b)

rng=np.random.default_rng(444091);twirls=[]
for k in [2,3]:
    H=rng.normal(size=(k,k))+1j*rng.normal(size=(k,k));H=(H+H.conj().T)/2;H/=np.linalg.norm(H,2)
    e,v=np.linalg.eigh(H);U=(v*np.exp(.3j*e))@v.conj().T
    X=np.roll(np.eye(k),1,axis=0);Z=np.diag(np.exp(2j*np.pi*np.arange(k)/k))
    weyl=[np.linalg.matrix_power(X,a)@np.linalg.matrix_power(Z,b) for a in range(k) for b in range(k)]
    Ks=[W.conj().T@U@W/k for W in weyl]
    J=sum(np.outer(K.T.reshape(-1),K.T.reshape(-1).conj()) for K in Ks)/k
    bell=np.array([W.T.reshape(-1)/np.sqrt(k) for W in weyl]).T
    diagonal=bell.conj().T@J@bell
    residual=float(np.max(np.abs(diagonal-np.diag(np.diag(diagonal)))))
    assert residual<1e-13
    probs=np.diag(diagonal).real
    assert probs.min()>-1e-14 and abs(sum(probs)-1)<1e-13
    assert abs((1-probs[0])-(1-abs(np.trace(U))**2/k**2))<1e-13
    twirls.append({'logical_dimension':k,'Bell_offdiagonal_residual':residual,'Pauli_error_probability':float(1-probs[0])})

# Tensor-product channels preserve the hybrid guarantee on entangled inputs.
I=np.eye(2);Z=np.diag([1.,-1.]);ent=[]
for M in [2,3,4]:
    q=.07;z=rng.normal(size=2**M)+1j*rng.normal(size=2**M);z/=np.linalg.norm(z)
    rho=np.outer(z,z.conj());out=np.zeros_like(rho)
    for pattern in itertools.product([0,1],repeat=M):
        K=np.array([[1.]])
        for bit in pattern:K=np.kron(K,np.sqrt(q)*Z if bit else np.sqrt(1-q)*I)
        out+=K@rho@K.conj().T
    error=norm1(out-rho)/2
    assert error<=M*q+1e-13
    ent.append({'M':M,'entangled_input_trace_distance':error,'hybrid_bound':M*q})

result={'exact_shared_calibration_cases':rows,'shared_vs_iid_counterexample':{'beta':str(b),'shared_two_error_probability':str(b),'iid_two_error_probability':str(b*b),'exact_channel_halfdiamond_difference':str(distance)},'independent_Weyl_twirl_checks':twirls,'entangled_tensor_channel_checks':ent,'scope':'Small analytical/matrix diagnostics; no outer code, rate, or large joint compression execution.'}
(HERE/'INDEPENDENT_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
