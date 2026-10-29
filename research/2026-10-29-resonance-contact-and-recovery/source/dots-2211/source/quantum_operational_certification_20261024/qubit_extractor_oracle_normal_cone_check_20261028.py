import sympy as s,numpy as np,json,hashlib
from pathlib import Path
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1);pa=[X,Y,Z]
def kron(*xs):
 z=xs[0]
 for x in xs[1:]:z=s.kronecker_product(z,x)
 return z
def cert(B,C):
 d=B[0].rows;H=sum((kron(p.T,c) for p,c in zip(pa,C)),s.zeros(2*d));KB=(s.eye(2*d)+sum((kron(p.T,b) for p,b in zip(pa,B)),s.zeros(2*d)))/2;P=KB/2;yb=sum((c*b for c,b in zip(C,B)),s.zeros(d));return yb,kron(I,yb)-H,P
C=[s.Rational(1,5)*X,s.Rational(1,5)*Y,-s.Rational(1,10)*Z];yb,Q,P=cert(pa,C)
assert yb==s.Rational(3,10)*I and Q*P==s.zeros(4);eigA=Q.eigenvals();assert eigA=={s.Rational(4,5):1,s.Rational(1,5):2,0:1}
B=[kron(p,I) for p in pa];la=s.Rational(1,2);ep=s.Rational(1,4);C=[la*b/4 for b in B];C[2]+=ep*kron(I,Z)/4;yb,Q,P=cert(B,C)
assert Q*P==s.zeros(8) and yb==yb.H;assert min(Q.eigenvals())==0;assert min((Q-s.Rational(3,8)*(s.eye(8)-P)).eigenvals())==0
JN=(s.eye(8)+la*sum((kron(p.T,p,I) for p in pa),s.zeros(8))+ep*kron(Z,I,Z))/8
assert min(JN.eigenvals())==s.Rational(1,32)
# Trace over logical output of C_Z.
pt=s.zeros(2)
for l in range(2):pt+=C[2][2*l:2*l+2,2*l:2*l+2]
assert pt==ep*Z/2
cy=[Y/2,-X/2,Z/2];yr,qr,pr=cert(pa,cy);assert yr==I/2-s.I*Z
rng=np.random.default_rng(2026102841);pan=[np.array(p).astype(complex) for p in pa];Bn=[np.array(b).astype(complex) for b in B];Cn=[np.array(c).astype(complex) for c in C];checks=0;minratio=1e9
for _ in range(300):
 z=rng.normal(size=(8,4))+1j*rng.normal(size=(8,4));v,_=np.linalg.qr(z);ks=[v[2*i:2*i+2] for i in range(4)]
 A=[sum(k.conj().T@p@k for k in ks) for p in pan]
 gap=sum(np.trace(c@(b-a)).real for c,b,a in zip(Cn,Bn,A));D2=sum(np.linalg.norm(a-b)**2 for a,b in zip(A,Bn));bound=(3/8)*D2/8
 assert gap>=bound-1e-12;minratio=min(minratio,gap/bound);checks+=1
out={'status':'PASS_AUTHOR_EXACT_CONE_EXAMPLES_AND_RANDOM_DECODER_CHECKS','example_A_dual_eigenvalues':{str(k):v for k,v in eigA.items()},'example_B_dual_eigenvalues':{str(k):v for k,v in Q.eigenvals().items()},'example_B_normalized_Choi_eigenvalues':{str(k):v for k,v in JN.eigenvals().items()},'example_B_disjoint_gauge_contrast':str(pt),'arbitrary_CPTP_decoder_checks':checks,'minimum_curvature_ratio':minratio,'scope':'Exact physical examples/cone/kernel checks; random full decoder curvature fixtures, not an executed generic SDP or acquired learner.'}
p=Path(__file__);src=p.with_name('qubit_extractor_oracle_normal_cone_20261028.md');out['source_sha256']=hashlib.sha256(src.read_bytes()).hexdigest();p.with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
