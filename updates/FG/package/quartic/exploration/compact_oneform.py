import sympy as s,pickle,os,itertools
BASE=os.path.dirname(__file__);z=pickle.load(open(BASE+'/scalar_identity_general.pkl','rb'));a,b,c,d=s.symbols('a b c d');A=s.Matrix([a,b,c,d]);alpha=z['alpha'];Da=alpha.jacobian(A);om=Da.T-Da
can=(-om*A/4).applyfunc(s.expand)
u=a*a+c*c;v=b*b+d*d;w=a*b+c*d;q=a*d-b*c
# columns x=(a,c), y=(b,d), da/db/dc/dd ordering.
th=s.Matrix([-c,-d,a,b]);ze=s.Matrix([-b,a,-d,c]);tha=s.Matrix([-c,d,a,-b]);thb=s.Matrix([-d,-c,b,a]);dw=s.Matrix([b,a,d,c]);dt=s.Matrix([2*a,-2*b,2*c,-2*d])
bas=[(u+v)*th,q*th,(u+v)*ze,q*ze,(u-v)*tha,w*thb,(u-v)*dw-w*dt]
mon=list(itertools.combinations_with_replacement(range(4),3))
def vv(aa):
 ret=[]
 for i in range(4):
  p=s.Poly(aa[i],a,b,c,d)
  ret.extend([p.coeff_monomial(s.prod(A[k] for k in ks)) for ks in mon])
 return s.Matrix(ret)
M=s.Matrix.hstack(*map(vv,bas));rhs=vv(can)
print('basisrank',M.rank())
sol=next(iter(s.linsolve((M,rhs))));free=set().union(*(co.free_symbols for co in sol))-set(z['tau'])-{z['L']}
sol=[s.factor(co.subs({f:0 for f in free})) for co in sol]
print('compactcoeff',sol)
new=sum((coef*bb for coef,bb in zip(sol,bas)),s.zeros(4,1));assert (new-can).applyfunc(s.expand)==s.zeros(4,1)
print('Canonical radial primitive exact')
pickle.dump(dict(coeff=sol,basis=bas,alpha=new,L=z['L'],tau=z['tau']),open(BASE+'/compact_oneform.pkl','wb'))
