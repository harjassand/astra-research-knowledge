from reconstruct import *
import pickle,time
from sympy.polys.matrices import DomainMatrix
from sympy import QQ
from pathlib import Path
base=Path(__file__).parent
with open(base/'family_data.pkl','rb') as f:old=pickle.load(f)
r=s.symbols('r');k=-1/(r+1)
Cr=C.copy()
for row in [5,8]:Cr[row,5]=k;Cr[row,10]=-k
xb=list(cwr(range(4),2));zb=list(cwr(range(6),2));vars_=list(x)+list(z);exps=[]
for i,j0 in xb:
 for ki,l in zb:
  e=[0]*10;e[i]+=1;e[j0]+=1;e[4+ki]+=1;e[4+l]+=1;exps.append(tuple(e))
ix={e:ki for ki,e in enumerate(exps)}
def pcol(p):
 out=s.zeros(226,1)
 for e,val in s.Poly(p,*vars_).terms():out[ix[e],0]=s.cancel(val)
 return out
ell=Cr.T*Z
GM=s.Matrix.hstack(*[pcol(s.expand((1 if i==j else 2)*ell[i]*ell[j])) for i,j in cwr(range(18),2)])
M=GM.row_join(-old['WM'])
F=3*(u+v-2*j)**2+r*(r-1)/6*u**2+j**2+r*u*j
FM=pcol(heat(F))
# Fix free columns at the original rational certificate, so continuation equals source at r=-5/2.
basevec=s.Matrix([S[i,j] for i,j in cwr(range(18),2)]+list(W))
piv=[k0 for k0 in old['piv'] if k0<231];free=[k0 for k0 in range(231) if k0 not in piv]
Mp=M[:,piv];rhs=FM-M[:,free]*basevec[free,:]
print('rref moving',Mp.shape,flush=True);t=time.time()
DM=DomainMatrix.from_Matrix(Mp.row_join(rhs)).convert_to(QQ.frac_field(r))
rr,pp=DM.rref();rr=rr.to_Matrix()
print('seconds',time.time()-t,'rank',len(pp),'consistent',all(v==0 for v in rr[len(piv):,-1]),flush=True)
assert len(pp)==len(piv)
vec=basevec.copy()
for row,col in enumerate(piv):vec[col]=s.cancel(rr[row,-1])
assert all(s.cancel(vv)==0 for vv in M*vec-FM)
assert vec.subs(r,-R(5,2))==basevec
Sr=s.zeros(18);Wr=s.zeros(6,10)
for val,(i,j0) in zip(vec[:171],cwr(range(18),2)):Sr[i,j0]=Sr[j0,i]=val
for i in range(6):
 for j0 in range(10):Wr[i,j0]=vec[171+10*i+j0]
print('nonconstant entries',sum(s.diff(q,r)!=0 for q in vec),flush=True)
from collections import Counter
print('degrees',Counter((s.degree(s.fraction(q)[0],r),s.degree(s.fraction(q)[1],r)) for q in vec if q!=0),flush=True)
with open(base/'moving_family.pkl','wb') as f:pickle.dump({'r':r,'C':Cr,'S':Sr,'W':Wr,'F':F,'vec':vec,'piv':piv,'free':free},f)
print('saved',flush=True)
