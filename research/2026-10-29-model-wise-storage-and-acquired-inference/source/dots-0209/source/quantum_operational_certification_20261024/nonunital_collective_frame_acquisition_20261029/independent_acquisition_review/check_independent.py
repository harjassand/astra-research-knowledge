"""Independent deterministic physical-bank expectation and CP/TP audit."""
from pathlib import Path
import json,itertools,hashlib
from functools import reduce
import numpy as np
R=Path(__file__).parent; F=R/'frozen';a=np.load(F/'check_exact_nonunital_v1.npz');N=a['channel'];Ts=a['Ts'];O=a['O'];J=a['Jembed'];n=4;D=16
P=np.array([np.eye(2),[[0,1],[1,0]],[[0,-1j],[1j,0]],[[1,0],[0,-1]]],complex)
kron=lambda xs:reduce(np.kron,xs)
states=[(P[0]+s*P[c])/2 for c in [1,2,3] for s in [1,-1]]
cfg=np.array(list(itertools.product(range(6),repeat=n)))
rhos=np.array([kron([states[c] for c in row]) for row in cfg]);outs=(rhos.reshape(-1,D*D)@N.T).reshape(-1,D,D)
features=np.zeros((len(cfg),n,4));features[:,:,0]=1
for site in range(n):features[np.arange(len(cfg)),site,1+cfg[:,site]//2]=3*(1-2*(cfg[:,site]%2))
err=0.;rmean=0.
for i in range(1,n):
    obs=np.array([kron([P[p] if j==i else P[q] if j==0 else P[0] for j in range(n)]) for p in [1,2,3] for q in [1,2,3]])
    expected_y=np.einsum('tij,aji->ta',outs,obs).real
    weights=np.einsum('tp,tq->tpq',features[:,i,:],features[:,0,:]).reshape(-1,16)
    That=weights.T@expected_y/len(cfg)
    err=max(err,float(np.max(abs(That-Ts[i-1]))))
    # Verify each signed weighted physical input equals Pauli pair / D,
    # including independently maximally mixed spectators.
    weighted=np.einsum('tr,tij->rij',weights,rhos)/len(cfg)
    target=np.array([kron([P[p] if j==i else P[q] if j==0 else P[0] for j in range(n)])/D for p in range(4) for q in range(4)])
    rmean=max(rmean,float(np.max(abs(weighted-target))))
# Row-vectorized superoperator Choi, unnormalized.
choi=N.reshape(D,D,D,D).transpose(0,2,1,3).reshape(D*D,D*D)
herm=float(np.linalg.norm(choi-choi.conj().T));mineig=float(np.linalg.eigvalsh((choi+choi.conj().T)/2).min())
tp=float(np.linalg.norm(N.conj().T@np.eye(D).reshape(-1)-np.eye(D).reshape(-1)))
assert err<1e-12 and rmean<1e-12 and herm<1e-12 and mineig>-1e-12 and tp<1e-12
# Exact second moments of scalar estimator depend only on private settings.
second=[]
for p,q in itertools.product(range(4),repeat=2):
    fprod=features[:,1,p]*features[:,0,q]
    moment=float(9*np.mean(fprod*fprod));second.append(moment)
assert max(second)==81
# At delta=.05 a million shots fails even the nontrivial robust sign guarantee
# for the fixture's gap; diagnostics cannot be elevated to a certified stop.
m=1000000;delta=.05;eta=np.sqrt(220*np.log(288*3/delta)/m);e=12*eta
out=dict(status='PASS',full_array_product_inputs=len(cfg),pair_edges=3,physical_expectation_max_entry_error=err,weighted_input_max_entry_error=rmean,choi_hermiticity_error=herm,choi_min_eigenvalue=mineig,trace_preservation_error=tp,second_moment_by_16_input_rows=second,million_shot_eta_at_delta_005=float(eta),million_shot_operator_error_bound=float(e),source_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(F.iterdir()) if p.is_file()})
print(json.dumps(out,indent=2))
