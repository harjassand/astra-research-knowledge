"""Necessary face for any pointwise nonnegative local corrected biquadratic.

Unlike full_face.py, this makes no SOS assumption. At each zero, positivity
forces its gradient to vanish. Fourth-order contact along the exact acoustic
curves additionally forces the derivative of that gradient to vanish.
"""
from geometry import *
from pathlib import Path
from sympy.polys.matrices import DomainMatrix
from sympy import QQ
import pickle,time

base=Path(__file__).parent
w=s.symbols('w0:60');d1,d2=s.symbols('d1 d2')
mons=[x[i]*x[k] for i,k in cwr(range(4),2)]
OO=s.zeros(4)
for ii,(i,k) in enumerate(combinations(range(4),2)):
    pol=sum(w[10*ii+jj]*mm for jj,mm in enumerate(mons))
    OO[i,k]=pol;OO[k,i]=-pol
HH=s.hessian(F,x)
P=s.expand(d1*(B1.T*HH*B1)[0]+d2*(B2.T*HH*B2)[0]+(B1.T*OO*B2)[0])
grad=[s.diff(P,xx) for xx in list(x)+list(z)]
eq=[]
print('contact necessary constraints',flush=True)
for AA,xi in [(old_A,(t,1)),(new_A,(1,t))]:
    vA=s.Matrix(list(R*AA));vz=rankone_jet(R[:,0],xi)
    sub=dict(zip(list(x)+list(z),list(vA)+list(vz)))
    for gg in grad:
        expr=s.expand(gg.subs(sub,simultaneous=True))
        for order in [0,1]:
            cc=s.expand(expr.diff(t,order).subs(t,0))
            eq.extend(s.Poly(cc,p,q).coeffs())
for i,k,l in combinations(range(4),3):
    closed=s.expand(s.diff(OO[k,l],x[i])-s.diff(OO[i,l],x[k])+s.diff(OO[i,k],x[l]))
    eq.extend(s.Poly(closed,*x).coeffs())
eq=[s.cancel(vv) for vv in eq if vv!=0]
vars_=list(w)+[d1,d2]
E,_=s.linear_eq_to_matrix(eq,vars_)
print('rref',E.shape,flush=True);start=time.time()
rr,piv=DomainMatrix.from_Matrix(E).convert_to(QQ.frac_field(r)).rref();rr=rr.to_Matrix()
print('rank',len(piv),'seconds',time.time()-start,flush=True)
free=[cc for cc in range(62) if cc not in piv]
print('free',free,flush=True)
vec=s.zeros(62,1)
for cc in free:vec[cc]=vars_[cc]
for row,cc in enumerate(piv):vec[cc]=-sum(rr[row,ff]*vec[ff] for ff in free)
vec=vec.applyfunc(s.cancel)
print('diffusions',vec[-2:],flush=True)
with open(base/'direct_face.pkl','wb') as ff:pickle.dump({'r':r,'vars':vars_,'vec':vec,'rr':rr,'piv':piv,'free':free,'E':E,'P':P,'O':OO},ff)
