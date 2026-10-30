"""Finite algebra diagnostic ONLY, not an actual native code/service simulation.
Checks the new joint-kill / noncommuting post-kill activity seam.
"""
import json
from pathlib import Path
import numpy as np
from scipy.linalg import expm
rng=np.random.default_rng(3071)
I=np.eye(2); z=np.diag([1.,-1.]); angle=.37
u=np.array([[np.cos(angle),-np.sin(angle)],[np.sin(angle),np.cos(angle)]])
p=u@np.diag([1.,0.])@u.T; q=np.diag([1.,0.])
kron=lambda *xs: __import__('functools').reduce(np.kron,xs)
# AB analysis ancilla, Q syndrome ancilla, common bath. Unknown logical factor
# is an untouched external tensor factor in this deliberately algebraic fixture.
d=8; pab=kron(p,I,I); pq=kron(I,q,I); joint=pab@pq
fab=kron(u@np.diag([1.,3.])@u.T,I,I); fq=kron(I,np.diag([1.,2.]),I)
activity=kron(np.diag([0.,1.]),I,I); keep=np.eye(d)-activity
h=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d)); h=(h+h.conj().T)/14
js=[(rng.normal(size=(d,d))+1j*rng.normal(size=(d,d)))/9 for _ in range(2)]
gamma=sum(j.conj().T@j for j in js)
def killed_adjoint(P,O):
    hp=P@h@P; gp=P@gamma@P
    return 1j*(hp@O-O@hp)+sum(P@j.conj().T@P@O@P@j@P for j in js)-(gp@O+O@gp)/2
checks={}
for label,F,P in [('AB',fab,pab),('Q',fq,pq)]:
    f=P@F@P; fj=joint@F@joint
    diff=killed_adjoint(joint,fj)-joint@killed_adjoint(P,f)@joint
    outgoing=sum(joint@j.conj().T@(P-joint)@F@(P-joint)@j@joint for j in js)
    checks[label+'_extra_kill_identity_error']=float(np.linalg.norm(diff+outgoing))
    checks[label+'_extra_kill_max_eigenvalue']=float(np.linalg.eigvalsh((diff+diff.conj().T)/2).max())
# Exact full and joint CP/TNI evolution for one positive subnormalized source.
def vec(x): return x.reshape(-1,order='F')
def unvec(x): return x.reshape((d,d),order='F')
def generator(P):
    hp=P@h@P; gp=P@gamma@P
    return -1j*(np.kron(np.eye(d),hp)-np.kron(hp.T,np.eye(d)))+sum(np.kron((P@j@P).conj(),P@j@P) for j in js)-(np.kron(np.eye(d),gp)+np.kron(gp.T,np.eye(d)))/2
v=joint@(rng.normal(size=d)+1j*rng.normal(size=d)); v/=np.linalg.norm(v)
rho=.73*np.outer(v,v.conj()); time=.41
full=unvec(expm(time*generator(np.eye(d)))@vec(rho)); killed=unvec(expm(time*generator(joint))@vec(rho))
distance=float(np.linalg.svd(full-killed,compute_uv=False).sum())
filtered=keep@killed@keep
badfull=float(np.trace(activity@full).real); badkilled=float(np.trace(activity@killed).real)
gentle=float(np.linalg.svd(killed-filtered,compute_uv=False).sum())
checks.update(activity_projector_commutator=float(np.linalg.norm(activity@pab-pab@activity)),
              actual_minus_killed_min_eigenvalue=float(np.linalg.eigvalsh((full-killed+full.conj().T-killed.conj().T)/2).min()),
              full_vs_joint_trace_norm=distance,
              activity_bad_full=badfull,activity_bad_joint=badkilled,
              transfer_slack=badfull+distance-badkilled,
              post_kill_filtered_min_eigenvalue=float(np.linalg.eigvalsh((filtered+filtered.conj().T)/2).min()),
              gentle_trace_distance=gentle,
              gentle_upper=2*np.sqrt(float(np.trace(killed).real)*badkilled),
              killed_mass=float(np.trace(killed).real),
              scope='abstract finite algebra; no native absorption, Tanner-family or lifetime simulation')
assert max(checks['AB_extra_kill_identity_error'],checks['Q_extra_kill_identity_error'])<1e-12
assert max(checks['AB_extra_kill_max_eigenvalue'],checks['Q_extra_kill_max_eigenvalue'])<1e-12
assert checks['activity_projector_commutator']>.1
assert checks['actual_minus_killed_min_eigenvalue']<-.001
assert checks['transfer_slack']>=-1e-12
assert gentle<=checks['gentle_upper']+1e-12
assert checks['post_kill_filtered_min_eigenvalue']>=-1e-12
out=Path(__file__).with_suffix('.json'); out.write_text(json.dumps(checks,indent=2)+'\n')
print(json.dumps(checks,indent=2))
