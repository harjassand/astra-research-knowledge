import sympy as S
I=S.I;sqrt=S.sqrt
pauli=[S.Matrix([[0,1],[1,0]]),S.Matrix([[0,-I],[I,0]]),S.diag(1,-1)]
def local(n,j,A):
 out=S.Matrix([[1]])
 for k in range(n):out=S.kronecker_product(out,A if k==j else S.eye(2))
 return out
def ket(i,d):
 z=S.zeros(d,1);z[i]=1;return z
sites=[[local(3,j,a) for a in pauli] for j in range(3)]
J=[sum((sites[j][a] for j in range(3)),S.zeros(8)) for a in range(3)]
Y=[]
for a,b,c in [(0,1,2),(1,2,0),(2,0,1)]:Y.append(sum((sites[i][b]*sites[j][c]-sites[i][c]*sites[j][b] for i in range(3) for j in range(i+1,3)),S.zeros(8)))
Fq=S.Matrix.hstack(ket(0,8),(ket(1,8)+ket(2,8)+ket(4,8))/sqrt(3),(ket(3,8)+ket(5,8)+ket(6,8))/sqrt(3),ket(7,8),(ket(1,8)-ket(4,8))/sqrt(2),(ket(3,8)-ket(6,8))/sqrt(2))
Fp=S.Matrix.hstack(sqrt(S.Rational(2,3))*ket(2,8)-(ket(1,8)+ket(4,8))/sqrt(6),(ket(3,8)+ket(6,8))/sqrt(6)-sqrt(S.Rational(2,3))*ket(5,8))
# A spin one, B spin one half; tensor basis A m=1,0,-1 and B up,down.
Fr=S.Matrix.hstack(ket(0,6),(ket(1,6)+sqrt(2)*ket(2,6))/sqrt(3),(sqrt(2)*ket(3,6)+ket(4,6))/sqrt(3),ket(5,6),(sqrt(2)*ket(1,6)-ket(2,6))/sqrt(3),(ket(3,6)-sqrt(2)*ket(4,6))/sqrt(3))
V=S.simplify(Fq*Fr.T)
Az=S.diag(2,0,-2);Ap=S.Matrix([[0,2*sqrt(2),0],[0,0,2*sqrt(2)],[0,0,0]]);Ax=(Ap+Ap.T)/2;Ay=(Ap-Ap.T)/(2*I)
JA=[S.kronecker_product(a,S.eye(2)) for a in [Ax,Ay,Az]];JB=[S.kronecker_product(S.eye(3),b) for b in pauli]
Cross=[JA[b]*JB[c]-JA[c]*JB[b] for a,b,c in [(0,1,2),(1,2,0),(2,0,1)]]
Jq=[S.simplify(V.T*jj*V) for jj in J];Yq=[S.simplify(V.T*yy*V) for yy in Y]
print('V isometry',S.simplify(V.T*V)==S.eye(6),flush=True)
print('Jq standard',all(S.simplify(j-a-b)==S.zeros(6) for j,a,b in zip(Jq,JA,JB)),flush=True)
print('P J standard', [S.simplify(Fp.T*j*Fp) for j in J],flush=True)
print('P Y', [S.simplify(Fp.T*y*Fp) for y in Y],flush=True)
for a in range(3):
 gamma=S.simplify(S.trace(Cross[a]*Yq[a])/S.trace(Cross[a]*Cross[a]));res=S.simplify(Yq[a]-gamma*Cross[a]);print('gamma',a,gamma,'residual',res==S.zeros(6),flush=True)
u,v=S.symbols('u v',real=True)
def swap(n,i,j):
 out=S.zeros(2**n)
 for a in range(2**n):
  f=((a>>(n-1-i))^(a>>(n-1-j)))&1;b=a^(f<<(n-1-i))^(f<<(n-1-j));out[b,a]=1
 return out
M=S.eye(16)
for j in range(1,4):M=(u*S.eye(16)+I*swap(4,0,j))*M
VP=S.kronecker_product(S.eye(2),Fp);VQ=S.kronecker_product(S.eye(2),V)
MP=S.simplify(VP.T*M*VP);MQ=S.simplify(VQ.T*M*VQ)
Pswap=swap(2,0,1);tr=S.trace(MP);trp=S.trace(Pswap*MP);alpha=S.simplify((2*tr-trp)/6);beta=S.simplify((2*trp-tr)/6)
print('MP alpha I + beta P',S.factor(alpha),S.factor(beta),'residual',S.simplify(MP-alpha*S.eye(4)-beta*Pswap)==S.zeros(4),flush=True)
print('MP effective spectral ratio',S.factor(I*alpha/beta),flush=True)
for tag,T,d in [('full',M,8),('P',MP,2),('Q',MQ,6)]:
 T0=T.subs(u,0);T1=T.subs(u,1);blocks0=[[T0[i*d:(i+1)*d,j*d:(j+1)*d] for j in range(2)] for i in range(2)];blocks1=[[T1[i*d:(i+1)*d,j*d:(j+1)*d] for j in range(2)] for i in range(2)]
 largest=None
 for i in range(2):
  for j in range(2):
   for k in range(2):
    for l in range(2):
     a=blocks0[i][j];b=blocks1[k][l]
     Df=S.simplify(-(a*b-b*a)-I*(blocks1[k][j]*blocks0[i][l]-blocks0[k][j]*blocks1[i][l]))
     ss=S.simplify(S.trace(Df.T.conjugate()*Df))
     if largest is None or float(ss)>float(largest[0]):largest=(ss,(i,j,k,l),Df)
 print('RTT defect',tag,'norm2',largest[0],'component',largest[1], 'matrix',largest[2],flush=True)
# Failure of multiplicativity for compression of the three Hermitian Y charges.
for tag,F in [('P',Fp),('Q',Fq)]:
 Df=sum((F.T*y*(S.eye(8)-F*F.T)*y*F for y in Y),S.zeros(F.cols))
 print('Y Schwarz defect',tag,'trace',S.simplify(S.trace(Df)),'matrix',S.simplify(Df),flush=True)
