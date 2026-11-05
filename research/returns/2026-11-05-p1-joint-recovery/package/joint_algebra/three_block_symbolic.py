import sympy as S
c,s,x=S.symbols('c s x',real=True);I=S.I
p=[S.eye(2),S.Matrix([[0,1],[1,0]]),S.Matrix([[0,-I],[I,0]]),S.diag(1,-1)]
def local(n,j,a):
 z=S.Matrix([[1]])
 for k in range(n):z=S.kronecker_product(z,p[a if j==k else 0])
 return z
def swap(n,i,j):
 d=2**n;out=S.zeros(d)
 for a in range(d):
  f=((a>>(n-1-i))^(a>>(n-1-j)))&1;b=a^(f<<(n-1-i))^(f<<(n-1-j));out[b,a]=1
 return out
site=[[local(3,j,a) for a in range(1,4)] for j in range(3)]
dot=lambda i,j:sum((site[i][a]*site[j][a] for a in range(3)),S.zeros(8))
P=S.eye(8)/4-(dot(0,1)+dot(1,2))/6+dot(0,2)/12
print('projector rank',S.trace(P),'residual',P*P-P,flush=True)
U=S.eye(16)
for j in range(1,4):U=(c*S.eye(16)+I*s*swap(4,0,j))*U
W=S.expand(U*S.kronecker_product(p[3],S.eye(8))*U.T.conjugate())
PP=S.kronecker_product(p[0],P);QQ=S.eye(16)-PP
Y=S.expand(PP*W*PP+QQ*W*QQ)
A=S.expand((Y[:8,:8]+Y[8:,8:])/2)
b=S.expand(S.trace(A*A)/8);g=S.expand(S.trace(Y*Y)/16)
def to_x(v):
 pp=S.Poly(v,c,s);out=0
 for (i,j),co in pp.terms():
  assert i%2==j%2==0,(i,j)
  out+=co*(1-x)**(i//2)*x**(j//2)
 return S.factor(out)
bx=to_x(b);gx=to_x(g);hx=S.factor(gx-bx)
print('b=',bx,flush=True);print('h=',hx,flush=True);print('g=',gx,flush=True);print('loss=',S.factor(1-gx),flush=True);print('a_infty=',S.factor(bx/(1-hx)),flush=True)
