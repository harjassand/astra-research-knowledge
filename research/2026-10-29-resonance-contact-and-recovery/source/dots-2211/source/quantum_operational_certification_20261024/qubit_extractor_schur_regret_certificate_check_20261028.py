import numpy as np,json,hashlib
from pathlib import Path
I=np.eye(2);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]]);Zp=np.diag([1.,-1.]);pa=[X,Y,Zp];B=[np.kron(p,I) for p in pa];d=4
P=(np.eye(8)+sum(np.kron(p.T,b) for p,b in zip(pa,B)))/4;T=np.eye(8)-P
val,vec=np.linalg.eigh(T);basis=vec[:,val>.5]
base=[b/8 for b in B];base[2]=base[2]+np.kron(I,Zp)/16
rows=[];rng=np.random.default_rng(2026102848);maxkernel=0.;mingap=1.
for theta in [.001,.01,.03,.1,.2,.3]:
 U=np.kron(np.diag(np.exp(-1j*theta*np.array([1,-1]))),I);C=[U@c@U.conj().T for c in base]
 y=sum((c@b+b@c)/2 for c,b in zip(C,B));H=sum(np.kron(p.T,c) for p,c in zip(pa,C));Q=np.kron(I,y)-H
 zmat=T@Q@P;W=T@Q@T;gap=np.linalg.eigvalsh(basis.conj().T@W@basis)[0];z=np.linalg.norm(zmat,2);lam=(np.sqrt(gap**2+4*z*z)-gap)/2
 assert gap>0;kernel=np.linalg.norm(P@Q@P);maxkernel=max(maxkernel,kernel);assert kernel<1e-12
 assert np.linalg.eigvalsh(Q+lam*np.eye(8))[0]>-1e-12
 fe=(1+sum(np.trace(c@b).real for c,b in zip(C,B)))/4;regret=5/8-fe;bound=d*lam/4
 assert regret<=bound+1e-12
 rows.append({'theta':theta,'transverse_gap':float(gap),'stationarity_norm':float(z),'actual_oracle_regret':float(regret),'Schur_regret_bound':float(bound),'quadratic_bound':float(d*z*z/(4*gap))})
# Exact structural identities do not require a physical C tuple.
for _ in range(100):
 C=[]
 for j in range(3):
  a=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4));c=(a+a.conj().T)/2;c-=np.trace(c)*np.eye(4)/4;C.append(c)
 y=sum((c@b+b@c)/2 for c,b in zip(C,B));Q=np.kron(I,y)-sum(np.kron(p.T,c) for p,c in zip(pa,C));S=sum(c@b-b@c for c,b in zip(C,B))
 assert np.linalg.norm(P@Q@P)<1e-12;assert np.linalg.norm(Q@P+np.kron(I,S)@P/2)<1e-12
out={'status':'PASS_AUTHOR_KERNEL_AND_SCHUR_FIXTURES','arbitrary_Hermitian_tuple_checks':100,'max_physical_kernel_residual':maxkernel,'scope':'No actual holdout acquisition or confidence acceptance executed; physical rotated examples and structural identities only.','rows':rows};p=Path(__file__);out['source_sha256']=hashlib.sha256(p.with_name('qubit_extractor_schur_regret_certificate_20261028.md').read_bytes()).hexdigest();p.with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
