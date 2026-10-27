import mpmath as m
m.mp.dps=65
A=m.matrix([[6,0,-1],[0,5,-1],[-1,-1,4]])/10
D=m.matrix([[7,-1,1],[-1,6,5],[1,5,12]])/10
C=m.matrix([[23,22,-32],[-11,5,12],[-37,-31,16]])/10

def block(a,b,c,d):
 return m.matrix([[a[i,j] if i<a.rows and j<a.cols else b[i,j-a.cols] if i<a.rows else c[i-a.rows,j] if j<a.cols else d[i-a.rows,j-a.cols] for j in range(a.cols+b.cols)] for i in range(a.rows+c.rows)])
def kron(a,b):return m.matrix([[a[i//b.rows,j//b.cols]*b[i%b.rows,j%b.cols] for j in range(a.cols*b.cols)] for i in range(a.rows*b.rows)])
def ff(a):return sum(x*m.log(x) for x in m.eigsy(a,eigvals_only=True) if x>m.mpf('1e-48'))
def deficit(a):
 n=a.rows//3;r=m.matrix(n);pt=m.matrix(a.rows)
 for i in range(n):
  for j in range(n):r[i,j]=sum(a[k*n+i,k*n+j] for k in range(3))
 for i in range(3):
  for j in range(3):
   for k in range(n):
    for l in range(n):pt[i*n+k,j*n+l]=a[j*n+k,i*n+l]
 b=(kron(m.eye(3),r)-pt)/2;t=sum(a[i,i] for i in range(a.rows))
 return ff(a)+ff(r)-2*ff(b)-t*m.log(3)
Y=block(A+C*D**-1*C.T,C,C.T,D)
L=m.eye(3).copy();L=block(m.eye(3),-C*D**-1,m.matrix(0,3),m.matrix(0,3))
kappa=1/max(m.eigsy(L*L.T,eigvals_only=True));K=m.sqrt(kappa)*L
vals,W=m.eigsy(m.eye(6)-K.T*K);F=W*m.diag([m.sqrt(max(m.mpf(0),v)) for v in vals])*W.T
omega=m.matrix(18,1)
for i in range(3):omega[6*i+i]=1
src=omega*omega.T+kron(m.eye(3),Y)
acc=kron(m.eye(3),K)*src*kron(m.eye(3),K.T)
fail=kron(m.eye(3),F)*src*kron(m.eye(3),F)
x=deficit(src);a=deficit(acc);b=deficit(fail);gap=x-a-b
print('kappa',m.nstr(kappa,50));print('original homogeneous',m.nstr(x,50));print('accepted homogeneous',m.nstr(a,50));print('failure homogeneous',m.nstr(b,50));print('original minus flagged instrument',m.nstr(gap,50))
t=sum(src[i,i] for i in range(18));print('actual TP gap',m.nstr(gap/t,50));assert gap<-m.mpf('.00095')
assert min(m.eigsy(A,eigvals_only=True))>0 and min(m.eigsy(D,eigvals_only=True))>0
assert m.norm(K*m.matrix([[1,0,0],[0,1,0],[0,0,1],[0,0,0],[0,0,0],[0,0,0]])-m.sqrt(kappa)*m.eye(3))<m.mpf('1e-50')
print('rational actual TP source / exact-success GLS instrument failure PASS')
