import numpy as np,json,pathlib
R=pathlib.Path(__file__).resolve().parent
# Known orthonormal singlet basis: matching12|34 and orthogonalized13|24.
def singlet(M):
 v=np.zeros(16)
 for c in range(4):
  ix=0;s=1
  for j,(a,b) in enumerate(M):
   bit=(c>>j)&1;ix|=1<<(a if bit else b);s*=(-1 if bit else 1)
  v[ix]=s/2
 return v
u=singlet(((0,1),(2,3)));v=singlet(((0,2),(1,3)));v-=u*(u@v);v/=np.linalg.norm(v)
V=np.column_stack((u,v));Z=np.diag([1.,-1.]);X=np.array([[0.,1.],[1.,0.]])
reset=[np.outer(np.eye(2)[:,0],np.eye(2)[:,f]) for f in range(2)]
Es=[np.kron(V,r) for r in reset]
Ds=[np.kron(np.linalg.matrix_power(Z,f)@V.T,reset[f]) for f in range(2)]
comp=np.linalg.svd(V.T,full_matrices=True)[2].T[:,2:]
for f in range(2):
 for j in range(14):
  for a in range(2):Ds.append(np.kron(np.outer(np.eye(2)[:,a],comp[:,j])/np.sqrt(2),reset[f]))
assert np.linalg.norm(sum(e.T@e for e in Es)-np.eye(4))<1e-12
assert np.linalg.norm(sum(d.T@d for d in Ds)-np.eye(32))<1e-12
N=np.kron(np.eye(16),X)
vals=[]
for initial in (0,1):
 Einit=np.kron(np.eye(2),np.eye(2)[:,[initial]])
 rt=sv=0.
 for e in Es:
  for d in Ds:
   rt+=abs(np.trace((d@e@Einit).reshape(2,2,2)[:,0,:])/2)**2
   sv+=abs(np.trace((d@N@e@Einit).reshape(2,2,2)[:,0,:])/2)**2
 vals.append({'initial_bath_bit':initial,'roundtrip_entanglement_fidelity':float(rt),'service_entanglement_fidelity':float(sv)})
 assert abs(rt-1)<1e-12 and sv<1e-12
out={'all_checks_passed':True,'cases':vals,'membership_failure':0.,'matching_failure':0.,'full_path_two_basis_failure':.5,'source_physical_channel':'identity; source flips only shared bath bit'}
(R/'check_shared_memory_v3.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
