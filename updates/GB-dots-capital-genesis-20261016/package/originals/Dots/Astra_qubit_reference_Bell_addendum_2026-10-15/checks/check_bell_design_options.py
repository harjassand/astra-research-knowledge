import sympy as S
q=S.Rational;X=S.Matrix([[0,1],[1,0]]);Y=S.Matrix([[0,-S.I],[S.I,0]]);I=S.eye(2)
delta=q(1,10);t=q(3,10);B=S.diag(1,delta)/2;H=[X/2,-X/2]
def solve(A,H):
 n=A.rows; hv=S.Matrix([H[i,j] for j in range(n) for i in range(n)])
 lv=(S.kronecker_product(S.eye(n),A)+S.kronecker_product(A.T,S.eye(n))).inv()*2*t*hv
 return S.Matrix(n,n,lambda i,j:lv[j*n+i])
def moments(branches):
 mean=second=0
 for A,H in branches:
  O=solve(A,H);n=A.rows
  for label in [-1,1]:
   rho=(A+label*t*H)/(1+delta);loss=(label*S.eye(n)-O)**2
   mean+=S.trace(rho*loss)/2;second+=S.trace(rho*loss**2)/2
 return S.factor(mean),S.factor(second-mean**2)
for a,reveal,expected in [(q(9,10),q(9,20),q(335421,10671595)),(q(4,5),q(7,20),q(24489,1438085))]:
 sig=[(I+a*P)/2 for P in [X,Y]]
 A=sum((S.kronecker_product(s,B) for s in sig),S.zeros(4));Ht=sum((S.kronecker_product(s,h) for s,h in zip(sig,H)),S.zeros(4))
 mt,vt=moments([(A,Ht)]);ms,vs=moments([(reveal*B,reveal*h) for h in H]+[((1-reveal)*2*B,S.zeros(2))])
 gap=S.factor(ms-mt);assert gap==expected
 print('a,q=',a,reveal,'source MSE',ms,'target MSE',mt,'gap',gap,float(gap),'variances',float(vs),float(vt))
 if a==q(9,10):
  assert ms==q(524,605) and mt==q(14723,17639)
  O=solve(A,Ht)
  # target norm<3/4; source norm=6/11<3/4, so each loss width<3.
  mat=q(9,16)*S.eye(4)-O**2
  assert all(S.factor(mat[:k,:k].det())>0 for k in range(1,5))
  vbound=S.ceiling(1000*(vs+vt))/1000;g=q(157,5000);M=3
  assert gap>g
  ns=S.ceiling(S.N(2*(vbound+M*g/3)*S.log(20)/g**2,50))
  nc=S.ceiling(S.N(8*(vbound+M*g/6)*S.log(40)/g**2,50))
  print('Exact variances source,target',vs,vt,'variance sum bound',vbound,'gap bound',g,'M',M,'n sign',ns,'n CI',nc)

# Rigorous rational logarithm upper bounds certify the sufficient trial counts.
v=q(829,1000);g=q(157,5000);M=q(3)
l20=q(29957323,10000000);l40=q(36888795,10000000)
for log_upper,value in [(l20,20),(l40,40)]:
 assert sum(log_upper**k/S.factorial(k) for k in range(41))>value
assert 5229*g*g>2*(v+M*g/3)*l20
assert 25283*g*g>8*(v+M*g/6)*l40
print('Rational certificates: 5229 sign-order and 25283 half-gap-CI sufficient trials per arm PASS')
