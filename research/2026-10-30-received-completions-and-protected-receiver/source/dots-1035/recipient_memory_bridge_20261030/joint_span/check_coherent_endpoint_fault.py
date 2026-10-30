# Supplemental SUPPORT diagnostic: coherent shared-bath endpoint fault, no twirl.
exec(open(__file__.replace('check_coherent_endpoint_fault.py','check_joint_span.py')).read().split('# Partial Bell measurement:')[0])
from scipy.linalg import expm
# K tensor axes Q0,Q1,Q2,A0,A1,A2,B0,B1,B2,bath,L.
a=kin.reshape(*([2]*9),bath,K)
axes=[0,3,9]+[1,2,4,5,6,7,8,10]
t=np.transpose(a,axes).reshape(12,-1)
h=rng.normal(size=(12,12))+1j*rng.normal(size=(12,12));h=(h+h.conj().T)/2
u=expm(-.17j*h)
t=u@t
inv=np.argsort(axes)
kfault=np.transpose(t.reshape(2,2,bath,2,2,2,2,2,2,2,K),inv).reshape(D,D,D,bath,K)
mats=[]
for e,f in pairs:
 for xx,zz in [(0,0),(4,0),(0,4),(4,4)]:mats.append((pauli(xx,zz)@pauli(f,0)@pauli(e,0)@V).reshape(-1))
M=np.column_stack(mats);U,sv,_=np.linalg.svd(M,full_matrices=False);U=U[:,sv>1e-10]
maxres=0.;normalization=0.
for x in range(D):
 for z in range(D):
  P=pauli(x,z);beta=P/np.sqrt(D)
  kp=np.einsum('qa,qabcl->bcl',beta.conj(),kfault)
  out=np.einsum('db,bcl->dcl',P,kp)
  normalization+=np.vdot(out,out).real/K
  for b in range(bath):
   v=out[:,b,:].reshape(-1)
   maxres=max(maxres,np.linalg.norm(v-U@(U.conj().T@v)))
result=dict(shared_bath_fault_support_module_residual=float(maxres),actual_corrected_channel_normalization=float(normalization),module_rank=int(U.shape[1]),scope='Arbitrary coherent Q0/A0/shared-bath unitary; finite-leg support test only, no stochastic Pauli sampling')
assert maxres<1e-12 and abs(normalization-1)<1e-12
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
