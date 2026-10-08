import sympy as s,json
I=s.I
Jz=s.diag(s.Rational(3,2),s.Rational(1,2),s.Rational(-1,2),s.Rational(-3,2))
Jp=s.zeros(4);Jp[0,1]=s.sqrt(3);Jp[1,2]=2;Jp[2,3]=s.sqrt(3)
Jx=(Jp+Jp.T)/2;Jy=(Jp-Jp.T)/(2*I);J=[Jx,Jy,Jz]; Id=s.eye(4)
G=[s.simplify((Jy*Jz+Jz*Jy)/s.sqrt(3)),s.simplify((Jz*Jx+Jx*Jz)/s.sqrt(3)),s.simplify((Jx*Jy+Jy*Jx)/s.sqrt(3)),s.simplify((Jx*Jx-Jy*Jy)/s.sqrt(3)),Jz*Jz-s.Rational(5,4)*Id]
assert all(s.simplify(g*g-Id)==s.zeros(4) for g in G)
assert all(s.simplify(G[i]*G[j]+G[j]*G[i])==s.zeros(4) for i in range(5) for j in range(i))
K=s.kronecker_product
W1=s.Rational(4,5)*sum((K(q.T,K(q,Id)+K(Id,q)) for q in J),s.zeros(64))
W2=sum((K(q.T,K(q,Id)+K(Id,q)) for q in G),s.zeros(64))
vec=s.zeros(16,1)
for i in range(4):vec[5*i,0]=1
P=vec*vec.T/4
Wf=s.zeros(64)
# direct matrix construction singlet R A and R B
for r in range(4):
 for a in range(4):
  for b in range(4):
   row=(r*4+a)*4+b
   for rr in range(4):
    for aa in range(4):
     for bb in range(4):
      col=(rr*4+aa)*4+bb
      Wf[row,col]=16*(P[r*4+a,rr*4+aa]*int(b==bb)+P[r*4+b,rr*4+bb]*int(a==aa))-2*int(row==col)
W13=Wf-W2;W3=s.simplify(Wf-W1-W2)
T=s.zeros(4)
for i in range(4):T[i,3-i]=(-1)**i
U=K(T,Id,Id)
W3t=s.simplify(U*W3*U.T)
Jzt=K(Jz,Id,Id)+K(Id,Jz,Id)+K(Id,Id,Jz)
assert s.simplify(W3t*Jzt-Jzt*W3t)==s.zeros(64)
assert W3t==W3t.conjugate().T
M=[s.Rational(3,2)-i for i in range(4)]
blocks={}
for r in range(4):
 for a in range(4):
  for b in range(4):blocks.setdefault(str(M[r]+M[a]+M[b]),[]).append((r*4+a)*4+b)
rows=[]
for m,ix in blocks.items():
 Q=9*s.eye(len(ix))-W3t.extract(ix,ix)
 # LDL without square roots, Hermitian exact pivots
 L=s.eye(len(ix)); ds=[]
 for k in range(len(ix)):
  dk=s.simplify(Q[k,k]-sum(L[k,j]*ds[j]*s.conjugate(L[k,j]) for j in range(k)));ds.append(dk)
  assert dk>0,(m,k,dk)
  for i in range(k+1,len(ix)):
   L[i,k]=s.simplify((Q[i,k]-sum(L[i,j]*ds[j]*s.conjugate(L[k,j]) for j in range(k)))/dk)
 assert s.simplify(Q-L*s.diag(*ds)*L.conjugate().T)==s.zeros(len(ix))
 rows.append({'M':m,'indices':ix,'pivots':[str(x) for x in ds]})
x=s.symbols('x')
for W,poly in [(W2,x*(x-6)*(x-2)*(x+4)*(x*x-20)),(W13,x*(x-12)*(x-8)*(x-2)*(x+2)*(x+4))]:
 coeff=s.Poly(poly,x).all_coeffs();Z=s.zeros(64)
 for c in coeff:Z=Z*W+c*s.eye(64)
 assert Z==s.zeros(64)
print('quadrupole charpoly',s.factor(W2.charpoly().as_expr()),flush=True)
print('dipole+octupole charpoly',s.factor(W13.charpoly().as_expr()),flush=True)
print('octupole upper bound 9 LDL pivots',rows,flush=True)
json.dump({'quad_charpoly':str(s.factor(W2.charpoly().as_expr())),'dipole_octupole_charpoly':str(s.factor(W13.charpoly().as_expr())),'octupole_9_ldl':rows},open(__file__.replace('.py','.json'),'w'),indent=2)
