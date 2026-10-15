from pathlib import Path
import json,hashlib
import numpy as np
import sympy as s
OUT=Path(__file__).resolve().parent
z=s.symbols('z',real=True);K=s.Matrix([[1,z],[0,z*z/4+1]]);sym=(K+K.T)/2
assert s.det(sym)==1
assert K*s.Matrix([1,0])==s.Matrix([1,0])
assert (s.Matrix([[1,0]])*K*s.Matrix([0,1]))[0]==z
A=K.inv();assert s.simplify((A+A.T)/2-A.T*sym*A)==s.zeros(2)
rng=np.random.default_rng(20261015);max_identity=0.;max_excess=-float('inf');cases=120
for i in range(cases):
 n=6;r=3;B=rng.normal(size=(n,n));skew=rng.normal(size=(n,n));A=B.T@B+np.eye(n)+.4*(skew-skew.T)
 V=rng.normal(size=(n,r));b=rng.normal(size=n);c=rng.normal(size=n);x=np.linalg.solve(A,b);Y=np.linalg.solve(A,V);Kr=V.T@Y;l=Y.T@c;t=V.T@x
 D=np.diag(rng.uniform(0,1,r));S=np.diag(np.sqrt(np.diag(D)));d=np.linalg.norm(D,2);M=np.eye(r)+S@Kr@S
 assert np.linalg.svd(np.linalg.inv(M),compute_uv=False)[0]<=1+1e-12
 exact=c@np.linalg.solve(A+V@D@V.T,b)-c@x;pred=-(S@l)@np.linalg.solve(M,S@t);max_identity=max(max_identity,abs(exact-pred));assert abs(exact-pred)<2e-12
 eK=rng.normal(size=(r,r))*.001;el=rng.normal(size=r)*.001;et=rng.normal(size=r)*.001
 Kh=Kr+eK;lh=l+el;th=t+et;epsK=np.linalg.norm(eK,2);epsl=np.linalg.norm(el);epst=np.linalg.norm(et);eta=d*epsK;assert eta<1
 ah=S@th;bh=S@lh;ph=-bh@np.linalg.solve(np.eye(r)+S@Kh@S,ah)
 rad=np.sqrt(d)*epsl*(np.linalg.norm(ah)+np.sqrt(d)*epst)+np.linalg.norm(bh)*np.sqrt(d)*epst+np.linalg.norm(bh)*np.linalg.norm(ah)*eta/(1-eta)
 max_excess=max(max_excess,abs(exact-ph)-rad);assert abs(exact-ph)<=rad+3e-12
receipt=dict(status='PASS',scope='Exact symbolic2-state fiber plus120 seeded finite matrix/update/error fixtures. Not universal analytic proof or physical validation.',symbolic_groups=4,numerical_cases=cases,maximum_update_identity_error=max_identity,maximum_error_minus_certificate=max_excess,script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),source='Root new derivation; standard matrix/passivity machinery; priority UNKNOWN')
(OUT/'TASK_COMPLETE_CHECK.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
