import sympy as s, pickle,os
BASE=os.path.dirname(__file__)
L,j=s.symbols('L j');v=L*L
mp=48*L**6-2545*L**4+29712*L**2-97344
# z=(248-21v)/(64v-160); z (1+j)^2 = j
jp=(248-21*v)*(1+j)**2-(64*v-160)*j
GB=s.groebner([mp,jp],j,L,order='lex',domain=s.QQ)
print('groebner',list(GB),flush=True)
def red(x):return s.factor(GB.reduce(s.expand(x))[1])
# A=L aa, b=k L bb, c=k cc, d=dd
M=s.Matrix([[12+8*j,16*j,-2*j],[16,8+12*j,-(1+3*j)],[-2*v,-v*(1+3*j),4+7*j]])
rhs=s.Matrix([-(3+j),-2,-1]);vec=M.adjugate()*rhs;aa,bb,cc=[red(x) for x in vec];dd=red(M.det())
A=L*aa;B=L*bb;C=cc;D=dd
kp=s.Matrix([A,j*A,j*B,-j*C,-D,-j*D]).applyfunc(red)
km=s.Matrix([j*B,B,A,D,j*C,C]).applyfunc(red)
print('kernels done',flush=True)
Up=s.Matrix([A-j*D,j*A-D,j*(B-C)]);Ui=s.Matrix([C+j*B,j*C+B,D+A])
Vp=s.Matrix([A+j*D,j*A+D,j*(B+C)]);Vi=s.Matrix([C-j*B,j*C-B,D-A])
un=Up.cross(Ui).applyfunc(red);vn=Vp.cross(Vi).applyfunc(red)
print('u cross',un,flush=True)
print('v cross',vn,flush=True)
# Need normalization ratios independent of j: solve vector with entries in K annihilating real/imag vectors.
# each n_r=6 unknown L-polynomial degree<=5. Linear exact constraints modulo GB.
def constant_vector_null(vectors,n):
 t=s.symbols('t:'+str(n*6));G=s.Matrix(n,1,lambda i,k:sum(t[6*i+m]*L**m for m in range(6)))
 eq=[]
 for q in vectors:
  expr=s.expand((G.T*q)[0]);coef=s.zeros(12,len(t))
  for col,tt in enumerate(t):
   rem=s.Poly(red(expr.coeff(tt)),j,L)
   for (ej,eL),c in rem.terms():coef[ej*6+eL,col]=c
  eq+=list(coef.tolist())
 NS=s.Matrix(eq).nullspace();print('constant null dimension',len(NS),flush=True)
 return [s.Matrix(n,1,lambda i,k:sum(nn[6*i+m]*L**m for m in range(6))).applyfunc(s.factor) for nn in NS]
Uvec=constant_vector_null([Up,Ui],3);Vvec=constant_vector_null([Vp,Vi],3)
print('U first',Uvec[:1]);print('V first',Vvec[:1]);
# For S range use vectors orthogonal to kp/km (same as null constraints), expected 4*6=24 dimensional.
Svec=constant_vector_null([kp,km],6)
print('S vectorcount',len(Svec),flush=True)
with open(BASE+'/sharp_kernel_symbolic.pkl','wb') as f:pickle.dump(dict(L=L,j=j,mp=mp,jp=jp,kp=kp,km=km,Uvec=Uvec,Vvec=Vvec,Svec=Svec),f)
