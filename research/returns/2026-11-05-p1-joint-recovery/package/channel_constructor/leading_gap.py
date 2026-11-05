import sympy as s, itertools
p=[s.eye(2),s.Matrix([[0,1],[1,0]]),s.Matrix([[0,-s.I],[s.I,0]]),s.diag(1,-1)]
n=3; inds=list(itertools.product(range(4), repeat=n+1)); enc={k:i for i,k in enumerate(inds)}; bath=list(itertools.product(range(4),repeat=n)); bidx={k:i for i,k in enumerate(bath)}
def kron(ks):
 o=s.Matrix([[1]])
 for k in ks:o=s.kronecker_product(o,p[k])
 return o
F=(s.kronecker_product(p[0],p[0])+sum((s.kronecker_product(q,q) for q in p[1:]),s.zeros(4)))/2
loc={}
for a,b in itertools.product(range(4),repeat=2):
 C=s.I*(F*kron([a,b])-kron([a,b])*F)
 loc[a,b]=[(d,e,s.simplify(s.trace(kron([d,e])*C)/4)) for d,e in itertools.product(range(4),repeat=2) if s.trace(kron([d,e])*C)!=0]
L=[]; SW=[]
for j in range(1,n+1):
 A=s.zeros(4**(n+1));B=s.zeros(4**(n+1))
 for col,k in enumerate(inds):
  for d,e,val in loc[k[0],k[j]]:
   h=list(k);h[0]=d;h[j]=e;A[enc[tuple(h)],col]=val
  h=list(k);h[0],h[j]=h[j],h[0];B[enc[tuple(h)],col]=1
 L.append(A);SW.append(B)
R1=sum(L,s.zeros(4**(n+1)))
R2=sum(SW,s.zeros(4**(n+1)))+sum((L[j]*L[k] for j in range(n) for k in range(j)),s.zeros(4**(n+1)))
rows=[i for i,k in enumerate(inds) if k[0]]; cols=[enc[(0,)+b] for b in bath]
A=R1.extract(rows,cols);B=R2.extract(rows,cols);C=A.T*A
x=s.symbols('x');f=s.interpolate([(0,0),(2,s.Rational(1,2)),(6,s.Rational(1,6)),(12,s.Rational(1,12))],x);P=s.zeros(64)
for (k,),coef in s.Poly(f,x).terms():P+=coef*C**k
print('rank A',A.rank(),'pinvcheck',C*P*C==C,'f',f)
K=s.zeros(64,4)
for col,(i,j) in enumerate([(0,1),(0,2),(1,2)]):
 for a in range(1,4):
  v=[0]*3;v[i]=v[j]=a;K[bidx[tuple(v)],col]=1
for a,b,c in itertools.permutations([1,2,3]):K[bidx[(a,b,c)],3]=s.LeviCivita(a,b,c)
Q=B*K; S=s.simplify(Q.T*Q-Q.T*A*P*A.T*Q)
print('C K',C*K==s.zeros(64,4));print('Gram',K.T*K);print('effective S',S);print('eig',((K.T*K).inv()*S).eigenvals());
