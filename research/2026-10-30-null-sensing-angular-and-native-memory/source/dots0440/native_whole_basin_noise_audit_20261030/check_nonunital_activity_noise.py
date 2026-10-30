"""Finite algebra regression of the nonunital activity-congruence noise bridge."""
import numpy as np
from scipy.linalg import expm, norm
from functools import reduce
from pathlib import Path
import json
I=np.eye(2,dtype=complex); X=np.array([[0,1],[1,0]],complex); Z=np.diag([1,-1]).astype(complex)
def tensor(*xs):return reduce(np.kron,xs)
def psqrt(M,inverse=False):
 w,v=np.linalg.eigh(M); assert w.min()>0
 return (v*(1/np.sqrt(w) if inverse else np.sqrt(w)))@v.conj().T
# Site 0 is DATA. Three controller sites carry noncommuting positive activity gates.
a=.25*(tensor(I,I,I,I)+tensor(I,X,X,I))
b=.25*(tensor(I,I,I,I)+tensor(I,I,Z,X))
h=tensor(I,Z,I,I)
f=tensor(np.diag([1,7]),I,I,I)
def N(O):return 1j*(h@O-O@h)
rows=[]
for delta in [.2,.05,.01]:
 Y=expm(delta*b)@expm(delta*a); Yi=np.linalg.inv(Y); G=Y.conj().T@Y
 def M(O):return Yi.conj().T@N(Y.conj().T@O@Y)@Yi
 F=f@G; H=N(F); Fi=psqrt(F,True)
 relative=float(norm(Fi@H@Fi,2)); transformed_identity=float(norm(M(np.eye(16)),2))
 residual=float(norm(H-Y.conj().T@M(f)@Y))
 assert residual<1e-10 and transformed_identity>delta/10
 assert norm(N(f))<1e-13 and norm(f@G-G@f)<1e-12
 # Conservative finite-circuit local norm bound: ||M||cb <= 2||h|| ||Y||^2||Y^-1||^2.
 local_bound=2*norm(h,2)*norm(Y,2)**2*norm(Yi,2)**2*7
 assert relative<=local_bound+1e-12
 rows.append({'delta':delta,'relative_noise_norm':relative,'transformed_map_on_identity_norm':transformed_identity,'exact_congruence_residual':residual,'conservative_local_bound':float(local_bound)})
out={'checks':rows,'scope':'Demonstrates that noise may annihilate raw f but not fG, and that the transformed local map need not annihilate I. The dimension-free bounded-cone/factor proof, not this finite regression, establishes the theorem.'}
Path(__file__).with_name('nonunital_activity_noise_checks.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
