from pathlib import Path
ROOT = str(Path(__file__).resolve().parent) + "/"
# Reuse the already-defined exact embeddings, without running the later spectral checks.
exec(open(ROOT+'compressed_yangian.py').read().split("u,v=S.symbols")[0])
u=S.symbols('u',real=True)
def swap(n,i,j):
 out=S.zeros(2**n)
 for a in range(2**n):
  f=((a>>(n-1-i))^(a>>(n-1-j)))&1;b=a^(f<<(n-1-i))^(f<<(n-1-j));out[b,a]=1
 return out
M=S.eye(16)
for j in range(1,4):M=(u*S.eye(16)+I*swap(4,0,j))*M
# One RTT component, full monodromy, same conventions as the nonzero compressed component.
M0=M.subs(u,0);M1=M.subs(u,1);a0=M0[:8,:8];a1=M1[:8,:8];b0=M0[:8,8:];c1=M1[8:,:8];d0=M0[8:,8:];d1=M1[8:,8:]
Def=S.simplify(-(b0*c1-c1*b0)-I*(d1*a0-d0*a1));print('full RTT component zero',Def==S.zeros(8),flush=True)
# At physical u=1, normalization does not change Choi rank.
phi=S.Matrix([1,0,0,1])/S.sqrt(2);init=S.kronecker_product(phi,S.eye(8));globalU=S.kronecker_product(S.eye(2),M1)
for tag,F in [('P',Fp),('Q',Fq)]:
 A=S.simplify(S.kronecker_product(S.eye(4),F.T)*globalU*init)
 print('conditional Choi rank at u1',tag,A.rank(),'columns',A.cols,'branch dimension',F.cols,flush=True)
 Df=S.simplify(sum((F.T*y*(S.eye(8)-F*F.T)*y*F for y in Y),S.zeros(F.cols)))
 print('Schwarz defect',tag,Df,flush=True)
# Exact reduced Choi-amplitude blocks for the rank-two branch at arbitrary u.
singlet=S.Matrix([0,1,-1,0])/S.sqrt(2)
BB=S.simplify(S.kronecker_product(S.eye(4),Fp.T)*S.kronecker_product(S.eye(2),M)*S.kronecker_product(singlet,S.eye(8)))
fout0=(ket(2,8)-ket(4,8))/S.sqrt(2)
fout1=S.sqrt(S.Rational(2,3))*ket(1,8)-(ket(2,8)+ket(4,8))/S.sqrt(6)
Fout=S.Matrix.hstack(fout0,fout1);Fin=S.Matrix.hstack(Fp[:,0],Fq[:,4])
KK=S.simplify(Fout.T*BB*Fin)
print('rank2-branch reduced Choi amplitude',KK,flush=True)
print('rank2-branch reduced Choi det',S.factor(KK.det()),flush=True)
print('rank2-branch spin3/2 amplitude',S.simplify((ket(0,8).T*BB*ket(0,8))[0]),flush=True)
