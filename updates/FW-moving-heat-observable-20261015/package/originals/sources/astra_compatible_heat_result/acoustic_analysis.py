from reconstruct import *
n,m=s.symbols('n m',real=True)
fbase=[u**2,v**2,u*v,w**2,u*w,v*w,u*j,v*j,w*j]
f=s.Matrix(s.symbols('f0:9'))
F=sum(f[i]*fbase[i] for i in range(9))
H=s.Matrix([n,m,0,0])
h=(H.T*s.hessian(G,x)*H)[0].expand()
M=s.hessian(h,x)/2
print('M=',M)
print('det factor',s.factor(M.det()))
print('n=0',M.subs({n:0,m:1}), 'null',M.subs({n:0,m:1}).nullspace())
print('m=0',M.subs({n:1,m:0}), 'null',M.subs({n:1,m:0}).nullspace())
for inds in combinations(range(4),3):print('minor',inds,s.factor(M.extract(inds,inds).det()))
# Acoustic constraints from h_F >=0 and h_F(I,e12)=0: first variation A and n and target must vanish.
hF=(H.T*s.hessian(F,x)*H)[0].expand()
contact={a:1,b:0,c:0,d:1,n:0,m:1}
eq=[s.diff(hF,xi).subs(contact).expand() for xi in list(x)+[n,m]]
EC,bb=s.linear_eq_to_matrix(eq,list(f));print('one contact constraints',EC.rref()[0]);print('dimension',9-EC.rank())
for bi in EC.nullspace():print('one contact basis',list(bi),s.factor(sum(bi[i]*fbase[i] for i in range(9))))
