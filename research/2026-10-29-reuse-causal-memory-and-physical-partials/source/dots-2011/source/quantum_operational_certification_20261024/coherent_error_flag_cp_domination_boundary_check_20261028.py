"""Author floating complete-isometry/twirl check, zero acquired data."""
from pathlib import Path
import numpy as np,json,hashlib
I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]],complex);Z=np.diag([1,-1]);P=[I,X,Y,Z]
phi=np.array([1,0,0,1],complex)/np.sqrt(2);z0=np.array([[1],[0]],complex);z1=np.array([[0],[1]],complex)
rows=[]
for p in [.1,.25,.5,.8]:
 for t in [.001,.01,.05,.1]:
  c=(1-t*t)/(1+t*t);s=2*t/(1+t*t);b=s*s;W=c*I-1j*s*Z
  A=np.sqrt(1-p)*np.kron(I,z0)+np.sqrt(p)*np.kron(Z,z1)
  learned=np.zeros((8,8),complex);exact=np.zeros((8,8),complex)
  for Q in P:
   v=np.kron(I,np.kron(Q.conj().T@W,I)@A@Q)@phi
   v0=np.kron(I,np.kron(Q.conj().T,I)@A@Q)@phi
   learned+=np.outer(v,v.conj())/4;exact+=np.outer(v0,v0.conj())/4
  distance=np.abs(np.linalg.eigvalsh(learned-exact)).sum()/2
  formula=np.sqrt(b)*np.sqrt(b*(1-2*p)**2+4*p*(1-p));assert abs(distance-formula)<2e-14
  reduced=np.einsum('aman->mn',(learned-exact).reshape(4,2,4,2).transpose(1,0,3,2))
  # Explicit trace over final memory index, avoiding assumptions about partial transpose.
  reduced2=sum((learned-exact)[a::2,a::2] for a in range(2));assert np.max(abs(reduced-reduced2))<1e-15
  rd=np.abs(np.linalg.eigvalsh(reduced2)).sum()/2;assert abs(rd-abs(1-2*p)*b)<2e-14
  l0=np.array([c*np.sqrt(1-p),-1j*s*np.sqrt(p)])
  block=np.outer(l0,l0.conj())-c*c*(1-p)*np.diag([1,0])
  det=np.linalg.det(block).real;assert abs(det+c*c*s*s*p*(1-p))<2e-15 and det<0
  rows.append({'p':p,'t':t,'b':b,'complete_Bell_memory_distance':float(distance),'formula':float(formula),'reduced_distance':float(rd),'cp_difference_block_determinant':float(det)})
root=Path(__file__).resolve().parent
out={'status':'PASS_AUTHOR_COMPLETE_COHERENT_FLAG_TWIRL_BOUNDARY','cases':len(rows),'source_calls':0,'rng_draws':0,'source_sha256':hashlib.sha256((root/'coherent_error_flag_cp_domination_boundary_20261028.md').read_bytes()).hexdigest(),'rows':rows}
(root/'coherent_error_flag_cp_domination_boundary_check_20261028.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'],len(rows))
