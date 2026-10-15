from geometry import *
from pathlib import Path
from sympy.polys.matrices import DomainMatrix
from sympy import QQ
import pickle,time
base=Path(__file__).parent
with open(base/'direct_face.pkl','rb') as ff:data=pickle.load(ff)
vars_=data['vars'];vec=data['vec'];free=data['free']
P=data['P'].subs(dict(zip(vars_,vec))).expand()
Tx=s.Matrix([[1,0,-1,0],[0,1,0,-1],[1,0,1,0],[0,1,0,1]])
Tz=s.Matrix.vstack(s.Matrix.hstack(s.eye(3),-s.eye(3)),s.Matrix.hstack(s.eye(3),s.eye(3)))
Px=s.diag(1,-1,-1,1);Pz=s.diag(1,-1,1,-1,1,-1)
eq=[]
print('direct symmetry',flush=True)
for AA,zz,scale in [(Tx*x,Tz*z,s.Rational(1,4)),(Px*x,Pz*z,1)]:
    sub=dict(zip(list(x)+list(z),list(AA)+list(zz)))
    PP=s.expand(P.subs(sub,simultaneous=True)*scale-P)
    eq.extend(s.Poly(PP,*(list(x)+list(z))).coeffs())
yy=[vars_[ii] for ii in free]
E,_=s.linear_eq_to_matrix(eq,yy)
rr,piv=DomainMatrix.from_Matrix(E).convert_to(QQ.frac_field(r)).rref();rr=rr.to_Matrix()
print('rank',len(piv),'remaining',len(yy)-len(piv),flush=True)
sol=s.linsolve(list(E*s.Matrix(yy)),yy);print('sol',sol,flush=True)
vsol=s.Matrix(list(sol)[0]);sub=dict(zip(yy,vsol))
vv=vec.subs(sub).applyfunc(s.cancel)
PP=P.subs(sub).expand()
with open(base/'direct_symmetric.pkl','wb') as ff:pickle.dump({'r':r,'P':PP,'vec':vv,'vars':vars_,'sol':sol},ff)
