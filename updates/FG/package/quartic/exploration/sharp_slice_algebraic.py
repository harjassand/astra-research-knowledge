import sympy as s,numpy as np,scipy.linalg as la,pickle,os,itertools,time
BASE=os.path.dirname(__file__)
z=pickle.load(open(BASE+'/c4_spin2.pkl','rb'));ker=pickle.load(open(BASE+'/sharp_kernel_symbolic.pkl','rb'));L=ker['L'];mp=ker['mp']
def red(p):return s.rem(s.Poly(s.expand(p),L,domain=s.QQ),s.Poly(mp,L,domain=s.QQ)).as_expr()
R=s.Matrix.hstack(*[ker['Svec'][i] for i in [0,6,12,18]]);uu=ker['Uvec'][0];vv=ker['Vvec'][0]
t=s.symbols('t:12');ij4=list(itertools.combinations_with_replacement(range(4),2));ij6=list(itertools.combinations_with_replacement(range(6),2));ij3=list(itertools.combinations_with_replacement(range(3),2))
M=s.zeros(4)
for tt,(i,j) in zip(t,ij4):M[i,j]=M[j,i]=tt
SS=R*M*R.T;UU=t[10]*uu*uu.T;VV=t[11]*vv*vv.T
sv=s.Matrix([SS[i,j] for i,j in ij6]+[UU[i,j] for i,j in ij3]+[VV[i,j] for i,j in ij3])
# Obtain 15 independent projected equations.
pr=z['C'].T.rref()[1];C=z['C'][list(pr),:];rhs=(z['P']*z['EA'])[list(pr),:]*s.Matrix([1,s.Rational(7,2),s.Rational(1,2),L])
D=s.zeros(15,12)
for j in range(12):
 cc=sv.diff(t[j]);d=C*cc
 for i in range(15):D[i,j]=red(d[i])
 print('column',j,flush=True)
rt=2.9553866445792747;Dn=np.array(D.subs(L,rt)).astype(float);print('numeric rank',np.linalg.matrix_rank(Dn,tol=1e-8), 'sing',la.svdvals(Dn),flush=True)
# Expand all 12 unknowns in basis 1,L,...,L^5.
AA=s.zeros(90,72);bb=s.zeros(90,1)
for i in range(15):
 p=s.Poly(red(rhs[i]),L)
 for deg in range(6):bb[6*i+deg]=p.nth(deg)
 for j in range(12):
  for m in range(6):
   p=s.Poly(red(D[i,j]*L**m),L)
   for deg in range(6):AA[6*i+deg,6*j+m]=p.nth(deg)
print('rational system built',flush=True)
aug=AA.row_join(bb);rr,piv=aug.rref();print('rank',len(piv),'free',sorted(set(range(72))-set(piv)),flush=True)
with open(BASE+'/sharp_slice_algebraic.pkl','wb') as f:pickle.dump(dict(L=L,mp=mp,R=R,uu=uu,vv=vv,D=D,rhs=rhs,AA=AA,bb=bb,rref=rr,piv=piv,ij4=ij4),f)
