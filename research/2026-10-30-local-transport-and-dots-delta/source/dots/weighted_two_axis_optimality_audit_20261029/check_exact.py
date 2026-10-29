import sympy as s,json
from pathlib import Path
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1);ps=[X,Y,Z];kron=s.kronecker_product
bells=[s.Matrix(v)/s.sqrt(2) for v in [[1,0,0,1],[0,1,1,0],[0,1,-1,0],[1,0,0,-1]]]
rows=[]
for name,W,J,a,b in [('singular_noncommuting',s.diag(1,0),s.Matrix([[-1,1],[1,1]])/4,s.Rational(3,2),s.Rational(1,2)),('fullrank_noncommuting',s.diag(2,1),s.Matrix([[-1,1],[1,1]])/2,s.S(2),s.S(1)),('zero_W',s.zeros(2),s.Matrix([[1,s.I],[-s.I,1]])/4,s.S(0),s.S(0))]:
 m=W.rows;D=2*m;ds=[kron(X,a*W),kron(Y,b*W),kron(Z,J)]
 L=sum((kron(p.T,d) for p,d in zip(ps,ds)),s.zeros(2*D));Y0=kron(I,(a+b)*W+J);slack=kron(I,Y0)-L
 B=s.Matrix.hstack(*bells);T=kron(B,s.eye(m));diag=s.simplify(T.H*slack*T)
 expected=s.diag(s.zeros(m),2*(b*W+J),2*(a*W+J),2*(a+b)*W)
 assert diag==expected
 for C in [W,b*W+J]:assert all(e>=0 for e in C.eigenvals())
 # Choose a small rational scale making all response models genuinely CPTP.
 scale=s.Rational(1,128);scaled=[scale*d for d in ds]
 JC=kron(I,s.eye(D)/D)/2+sum((kron(p.T,d) for p,d in zip(ps,scaled)),s.zeros(2*D))/4
 assert all(JC[:n,:n].det()>0 for n in range(1,2*D+1))
 assert s.Matrix(2,2,lambda i,j:sum(JC[D*i+r,D*j+r] for r in range(D)))==I/2
 K=[]
 for j in range(m):
  A=s.zeros(2,D)
  for l in range(2):A[l,l*m+j]=1
  K.append(A)
 recover=lambda A:sum((q*A*q.H for q in K),s.zeros(2))
 score=s.Rational(1,4)+sum(s.trace(p*recover(d)) for p,d in zip(ps,scaled))/8
 upper=s.Rational(1,4)+scale*s.trace(Y0)/8
 assert score==upper
 # Recovery dual variable Q: index order test logical, output qubit, junk.
 vec=lambda A:s.Matrix([s.conjugate(A[l,c]) for l in range(2) for c in range(D)])
 Q=sum((vec(A)*vec(A).H for A in K),s.zeros(2*D))
 assert s.simplify(slack*Q)==s.zeros(2*D)
 rows.append({'name':name,'fidelity':str(score),'commutator_nonzero':W*J!=J*W,'rankW':W.rank(),'dual_equality':True})
# Choi orientation on a COMPLEX, trace-preserving recovery, all matrix units.
D=4;K0=s.Matrix([[1,0,0,0],[0,0,1,0]]);K1=Y*s.Matrix([[0,1,0,0],[0,0,0,1]]);Ks=[K0,K1]
assert sum((A.H*A for A in Ks),s.zeros(D))==s.eye(D)
vec=lambda A:s.Matrix([s.conjugate(A[l,c]) for l in range(2) for c in range(D)])
Q=sum((vec(A)*vec(A).H for A in Ks),s.zeros(2*D))
assert s.Matrix(D,D,lambda i,j:sum(Q[l*D+i,l*D+j] for l in range(2)))==s.eye(D)
checks=0
for p in [I]+ps:
 for i in range(D):
  for j in range(D):
   E=s.zeros(D);E[i,j]=1
   assert s.trace(kron(p.T,E)*Q)==s.trace(p*sum((A*E*A.H for A in Ks),s.zeros(2)));checks+=1
# Separate necessity witness, not part of author's frozen received sufficiency claim.
W=s.diag(1,1);J=s.diag(-2,0);a=s.S(2);b=s.S(1);scale=s.Rational(1,128)
ds=[scale*kron(X,a*W),scale*kron(Y,b*W),scale*kron(Z,J)]
extract=[K0,s.Matrix([[0,1,0,0],[0,0,0,1]])]
better=[X*K0,extract[1]]
def score(Ks):return s.Rational(1,4)+sum(s.trace(p*sum((A*d*A.H for A in Ks),s.zeros(2))) for p,d in zip(ps,ds))/8
improve=s.simplify(score(better)-score(extract));assert improve==s.Rational(1,256)
JC=kron(I,s.eye(D)/D)/2+sum((kron(p.T,d) for p,d in zip(ps,ds)),s.zeros(2*D))/4
assert all(JC[:n,:n].det()>0 for n in range(1,2*D+1))
out={'exact_CPTP_fixtures':rows,'complex_orientation_matrix_units':checks,'separate_necessity_witness_gain':str(improve),'scope':'Analytic optimum with specified factorization; no acquisition or physical unknown decoder.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
