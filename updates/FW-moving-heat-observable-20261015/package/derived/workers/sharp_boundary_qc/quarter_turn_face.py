"""Separate exploratory continuation: universal sharp-ray elliptic C4 face."""
from geometry import *
from pathlib import Path
from sympy.polys.matrices import DomainMatrix
from sympy import QQ
import pickle,time
base=Path(__file__).parent
with open(base/'symmetric_face.pkl','rb') as ff:data=pickle.load(ff)
y=data['y'];C=data['C'];h=(2*r+1)/3
subD={y[4]:(2*r+1)/(r-1),y[5]:-3/(r-1)}
S=data['S'].subs(subD).applyfunc(s.cancel)
Q=C*S*C.T
Tx=s.Matrix([[0,1,0,0],[h,0,0,0],[0,0,0,1],[0,0,h,0]])
tz=s.Matrix([[0,0,1],[0,h,0],[h*h,0,0]])
Tz=s.diag(tz,tz);U=s.kronecker_product(Tx,Tz)
print('quarter turn invariance',flush=True)
E,_=s.linear_eq_to_matrix([s.cancel(vv) for vv in U.T*Q*U-(-h)**3*Q if vv!=0],[y[0],y[1],y[3]])
rr,piv=DomainMatrix.from_Matrix(E).convert_to(QQ.frac_field(r)).rref();rr=rr.to_Matrix()
# Nonhomogeneous terms are present after diffusion normalization.
eq=[s.cancel(vv) for vv in U.T*Q*U-(-h)**3*Q if vv!=0]
sol=s.linsolve(eq,[y[0],y[1],y[3]])
print('solution',sol,flush=True)
solution=list(sol)[0]
sub=dict(subD);sub.update(dict(zip([y[0],y[1],y[3]],solution)))
SS=data['S'].subs(sub).applyfunc(s.cancel)
vv=data['vec'].subs(sub).applyfunc(s.cancel)
print('free parameters',SS.free_symbols-{r},flush=True)
with open(base/'quarter_turn_face.pkl','wb') as ff:pickle.dump({'r':r,'y':y,'S':SS,'vec':vv,'C':C,'sub':sub},ff)
print('S diag',[s.factor(SS[i,i]) for i in range(12)],flush=True)
