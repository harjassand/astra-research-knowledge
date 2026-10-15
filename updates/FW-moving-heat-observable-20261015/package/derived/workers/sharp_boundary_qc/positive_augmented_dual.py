"""Exact equality dual for all non-SOS pointwise local positive-r heat forms."""
from geometry import *
from pathlib import Path
from sympy.polys.matrices import DomainMatrix
from sympy import QQ
import pickle,time
base=Path(__file__).parent
with open(base/'direct_face.pkl','rb') as ff:data=pickle.load(ff)
vars_=data['vars'];P=data['P'];d1,d2=vars_[-2:]
eq=[]
# A new zero forced by the old flat acoustic and target-rotation tangents.
subzero=dict(zip(list(x)+list(z),[1,0,0,1,0,1,0,0,0,-(r+1)]))
eq.extend([s.cancel(s.diff(P,xx).subs(subzero)) for xx in x])
eq.append(3*d1-(2*r+1)*d2)
Tx=s.Matrix([[1,0,-1,0],[0,1,0,-1],[1,0,1,0],[0,1,0,1]])
Tz=s.Matrix.vstack(s.Matrix.hstack(s.eye(3),-s.eye(3)),s.Matrix.hstack(s.eye(3),s.eye(3)))
Px=s.diag(1,-1,-1,1);Pz=s.diag(1,-1,1,-1,1,-1)
h=(2*r+1)/3;AK=s.Matrix([b,h*a,d,h*c]);zk=s.Matrix([z[2],h*z[1],h*h*z[0],z[5],h*z[4],h*h*z[3]])
print('augment pointwise face',flush=True)
for AA,zz,scale in [(Tx*x,Tz*z,s.Rational(1,4)),(Px*x,Pz*z,1),(AK,zk,1/h**3)]:
    pp=P.subs(dict(zip(list(x)+list(z),list(AA)+list(zz))),simultaneous=True)*scale-P
    eq.extend([s.cancel(cc) for cc in s.Poly(pp,*(list(x)+list(z)),domain='EX').coeffs()])
EE,_=s.linear_eq_to_matrix(eq,vars_)
E=EE.col_join(data['E'])
print('system',E.shape,flush=True)
rr,piv=DomainMatrix.from_Matrix(E).convert_to(QQ.frac_field(r)).rref();rr=rr.to_Matrix()
print('rank',len(piv),'free',[i for i in range(62) if i not in piv],flush=True)
jet=dict(zip(list(x)+list(z),[0,0,1,0,0,1,0,0,0,0]))
L,_=s.linear_eq_to_matrix([s.cancel(P.subs(jet))],vars_)
c=r*(r+1)*(2*r+1)/(r+2)
target=L.T.copy();target[61]+=c
dualrr,dualpiv=DomainMatrix.from_Matrix(E.T.row_join(target)).convert_to(QQ.frac_field(r)).rref()
dualrr=dualrr.to_Matrix();assert E.rows not in dualpiv
lam=s.zeros(E.rows,1)
for row,cc in enumerate(dualpiv):lam[cc]=s.cancel(dualrr[row,-1])
assert all(s.cancel(vv)==0 for vv in E.T*lam-target)
nonzero=[(i,s.factor(vv)) for i,vv in enumerate(lam) if vv!=0]
print('dual nonzero',len(nonzero),nonzero,flush=True)
print('r1 ranks',E.subs(r,1).rank(),E.subs(r,1).col_join(L.subs(r,1)).rank(),flush=True)
with open(base/'positive_augmented_dual.pkl','wb') as ff:pickle.dump({'r':r,'E':E,'L':L,'lam':lam,'c':c,'vars':vars_,'P':P,'eq':eq,'rank':len(piv),'target':target},ff)
