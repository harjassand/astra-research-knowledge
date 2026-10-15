from geometry import *
from pathlib import Path
from sympy.polys.matrices import DomainMatrix
from sympy import QQ
import pickle,time

base=Path(__file__).parent
with open(base/'full_face.pkl','rb') as ff:data=pickle.load(ff)
rr=data['rr'];piv=data['piv'];free=data['free'];C=data['C']
y=s.Matrix(s.symbols('y0:6'))
vec=s.zeros(140,1)
for ii,cc in enumerate(free):vec[cc]=y[ii]
for row,cc in enumerate(piv):vec[cc]=-sum(rr[row,ff]*vec[ff] for ff in free)
vec=vec.applyfunc(s.cancel)
S=s.zeros(12)
for vv,(i,j0) in zip(vec[:78],cwr(range(12),2)):S[i,j0]=S[j0,i]=vv
Q=C*S*C.T
Tx=s.Matrix([[1,0,-1,0],[0,1,0,-1],[1,0,1,0],[0,1,0,1]])
Tz=s.Matrix.vstack(s.Matrix.hstack(s.eye(3),-s.eye(3)),s.Matrix.hstack(s.eye(3),s.eye(3)))
U=s.kronecker_product(Tx,Tz)/2
P=s.kronecker_product(s.diag(1,-1,-1,1),s.diag(1,-1,1,-1,1,-1))
print('symmetry constraints',flush=True)
eq=[s.cancel(vv) for vv in list(U.T*Q*U-Q)+list(P.T*Q*P-Q)]
eq=[vv for vv in eq if vv!=0]
E,_=s.linear_eq_to_matrix(eq,list(y))
ee,pp=DomainMatrix.from_Matrix(E).convert_to(QQ.frac_field(r)).rref();ee=ee.to_Matrix()
print('symmetry rank',len(pp),'rref',ee[:len(pp),:],flush=True)
sol=s.linsolve(list(E*y),list(y));print('solution',sol,flush=True)
yy=list(sol)[0];sub=dict(zip(y,yy))
Sr=S.subs(sub).applyfunc(s.cancel);vr=vec.subs(sub).applyfunc(s.cancel)
print('Gram variables',sorted(str(vv) for vv in Sr.free_symbols-{r}),flush=True)
print('S reduced')
for row in Sr.tolist():print([str(vv) for vv in row],flush=True)
with open(base/'symmetric_face.pkl','wb') as ff:pickle.dump({'S':Sr,'vec':vr,'C':C,'y':y,'sub':sub,'r':r},ff)
