import numpy as np,json,math
from pathlib import Path
rng=np.random.default_rng(294955)
I=np.eye(2);X=np.array([[0,1],[1,0]]);Z=np.diag([1,-1]); phi=np.array([1,0,0,1])/np.sqrt(2);Phi=np.outer(phi,phi)
P=[I,X,Z,X@Z]; Ks=[]
for Q in P:
 beta=np.kron(I,Q)@phi
 Ks.append(np.kron(Q.T,I)@np.kron(beta.conj().reshape(1,4),np.eye(4)))
def resource(rho,bell):
 return np.kron(rho,bell).reshape([2]*8).transpose(0,2,3,1,4,6,7,5).reshape(16,16)
res=0
for a in range(4):
 for b in range(4):
  E=np.zeros((4,4),complex);E[a,b]=1
  for K in Ks: res=max(res,np.linalg.norm(K@resource(E,Phi)@K.conj().T-E/4))
assert res<1e-12
trnorm=lambda a:np.linalg.svd(a,compute_uv=False).sum()
def unitary():
 q,r=np.linalg.qr(rng.normal(size=(2,2))+1j*rng.normal(size=(2,2)))
 return q@np.diag(np.diag(r)/np.abs(np.diag(r)))
rows=[]
for case in range(40):
 A=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4));rho=A@A.conj().T;rho/=np.trace(rho)
 eps=[.01,.02,.03,.04];front=[('',rho)];acts=[];ids=[];reaches=[]
 for i in range(4):
  reaches.append(sum(np.trace(st).real for _,st in front));nxt=[]
  for hist,st in front:
   # Distinct adaptive candidate and bath operation at every actual history.
   acc=rng.uniform(.05,.85,2);split=rng.uniform(.1,.9,2)
   B=unitary()@np.diag(np.sqrt(acc)); R0=unitary()@np.diag(np.sqrt((1-acc)*split));R1=unitary()@np.diag(np.sqrt((1-acc)*(1-split)))
   assert np.linalg.norm(B.conj().T@B+R0.conj().T@R0+R1.conj().T@R1-I)<1e-12
   F=np.kron(I,B);bs=F@st@F.conj().T
   bad=np.kron(I,P[1+(len(hist)+hist.count('1')+case)%3])@phi; bad=np.outer(bad,bad.conj())
   good=resource(bs,Phi);actual=(1-eps[i])*good+eps[i]*resource(bs,bad)
   # Keep attempt/history and all public feedforward outcomes in direct-sum norm.
   for K in Ks:
    acts.append(K@actual@K.conj().T);ids.append(K@good@K.conj().T)
   for label,R in [('0',R0),('1',R1)]:
    F=np.kron(I,R);nxt.append((hist+label,F@st@F.conj().T))
  front=nxt
 # Failure record remains precisely actual, with possible payload steering.
 fail=sum(st for _,st in front)
 actualtrace=sum(np.trace(a).real for a in acts)+np.trace(fail).real
 idealtrace=sum(np.trace(a).real for a in ids)+np.trace(fail).real
 distance=sum(trnorm(a-b)/2 for a,b in zip(acts,ids))
 bound=sum(e*r for e,r in zip(eps,reaches))
 assert abs(actualtrace-1)<1e-12 and abs(idealtrace-1)<1e-12 and distance<=bound+1e-12
 rows.append({'case':case,'distance_with_public_records':distance,'reach_weighted_bound':bound,'sum_bound':sum(eps),'trace_error':max(abs(actualtrace-1),abs(idealtrace-1))})
# Comparator caveat: accepted actual effect a versus arbitrary simulator b.
a=.3;b=.2; total_ideal_trace=b+(1-a)
assert abs(total_ideal_trace-.9)<1e-12
out={'teleportation_all_DM_matrix_units_max_residual':res,'adaptive_four_attempt_two_rejection_histories':rows,'unmatched_simulator_effect_counterexample':{'actual_acceptance':a,'simulator_acceptance':b,'actual_rejection':1-a,'ideal_factory_trace':total_ideal_trace},'scope':'Synthetic finite instrument composition, not physical 155-block trajectory or adaptive acquisition yield.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2));print(json.dumps({'cases':40,'teleportation_residual':res,'max_distance':max(x['distance_with_public_records'] for x in rows)}))
