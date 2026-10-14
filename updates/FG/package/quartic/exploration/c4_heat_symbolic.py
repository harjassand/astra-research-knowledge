import sympy as s,numpy as np,itertools,os,pickle
BASE=os.path.dirname(__file__)
z=np.load(BASE+'/heat_matrices.npz');N=s.Matrix(z['N'].astype(int).tolist());E=s.Matrix(z['E'].astype(int).tolist())
if os.path.exists(BASE+'/exact_annihilator.pkl'):
 with open(BASE+'/exact_annihilator.pkl','rb') as f:P=pickle.load(f)
else:
 print('exact annihilator',flush=True)
 pc=N.rref()[1];NB=N[:,list(pc)];pr=NB.T.rref()[1];NI=NB[list(pr),:].inv()
 P=s.zeros(210-len(pr),210);rr=0
 for j in range(210):
  if j not in pr:
   P[rr,j]=1;row=NB[j,:]*NI
   for k,v in enumerate(pr):P[rr,v]=-row[k]
   rr+=1
 with open(BASE+'/exact_annihilator.pkl','wb') as f:pickle.dump(P,f)
 print('ann rank',P.rows,flush=True)
a=s.symbols('a b c d');h=s.symbols('h0:6');x=s.Matrix([a[0],a[2]]);y=s.Matrix([a[1],a[3]]);X=s.Matrix([h[0],h[3]]);Y=s.Matrix([h[1],h[4]]);Z=s.Matrix([h[2],h[5]])
cross=lambda v,w:v[0]*w[1]-v[1]*w[0]
zz=[x.dot(X),x.dot(Z),y.dot(Y),cross(x,Y),cross(y,X),cross(y,Z)]
ww=[-y.dot(Z),-y.dot(X),-x.dot(Y),cross(y,Y),cross(x,Z),cross(x,X)]
pa=list(itertools.combinations_with_replacement(range(4),2));ph=list(itertools.combinations_with_replacement(range(6),2))
def ex(p,n):
 e=[0]*n
 for j in p:e[j]+=1
 return tuple(e)
idx={ex(p,4)+ex(q,6):i for i,(p,q) in enumerate(itertools.product(pa,ph))}
def vec(poly):
 v=s.zeros(210,1)
 for exp,c in s.Poly(s.expand(poly),*(a+h)).terms():
  if c:v[idx[exp]]=c
 return v
ij=list(itertools.combinations_with_replacement(range(6),2));T=s.Matrix.hstack(*[vec((zz[i]*zz[j]+ww[i]*ww[j])*(1 if i==j else 2)) for i,j in ij])
EA=s.Matrix.hstack(E[:,0]+E[:,1],E[:,2],E[:,3],E[:,6]+E[:,7]);EM=E[:,2]-E[:,3]
C=P*T;Cb=P*EA;Cd=P*EM
param=s.symbols('a0 c0 e0 L0 delta')
sol=s.linsolve((C,Cb*s.Matrix(param[:4])-Cd*param[4]))
sol=list(sol)[0]
S=s.zeros(6)
for (i,j),v in zip(ij,sol):S[i,j]=S[j,i]=s.factor(v)
print('rank target',C.rank(),'S');print(S)
with open(BASE+'/c4_heat_symbolic.pkl','wb') as f:pickle.dump(dict(S=S,T=T,P=P,C=C,EA=EA,EM=EM,sol=sol,ij=ij,param=param),f)
