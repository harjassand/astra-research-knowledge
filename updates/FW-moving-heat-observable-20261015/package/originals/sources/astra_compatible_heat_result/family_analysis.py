from reconstruct import *
import pickle,time
from sympy.polys.matrices import DomainMatrix
from sympy import QQ
from pathlib import Path
base=Path(__file__).parent
xb=list(cwr(range(4),2));zb=list(cwr(range(6),2))
vars_=list(x)+list(z)
exps=[]
for i,j0 in xb:
 for k,l in zb:
  e=[0]*10;e[i]+=1;e[j0]+=1;e[4+k]+=1;e[4+l]+=1;exps.append(tuple(e))
ix={e:k for k,e in enumerate(exps)}
def pcol(p):
 out=s.zeros(226,1)
 for e,val in s.Poly(p,*vars_).terms():out[ix[e],0]=val
 return out
print('constructing',flush=True)
ell=C.T*Z
GM=s.Matrix.hstack(*[pcol(s.expand((1 if i==j else 2)*ell[i]*ell[j])) for i,j in cwr(range(18),2)])
WM=[]
for ik,(i,k) in enumerate(pairs):
 for ij,(ii,jj) in enumerate(xb):
  pol=x[ii]*x[jj];W1=s.zeros(4);W1[i,k]=pol;W1[k,i]=-pol
  vcol=pcol(correction(W1))
  offset=210
  for i0,k0,l0 in combinations(range(4),3):
   co=s.expand(s.diff(W1[k0,l0],x[i0])-s.diff(W1[i0,l0],x[k0])+s.diff(W1[i0,k0],x[l0]))
   for a0 in range(4):vcol[offset]=s.diff(co,x[a0]);offset+=1
  WM.append(vcol)
WM=s.Matrix.hstack(*WM)
fbase=[u**2,v**2,u*v,w**2,u*w,v*w,u*j,v*j,w*j]
FM=s.Matrix.hstack(*[pcol(heat(fi)) for fi in fbase])
M=GM.row_join(-WM)
# The signs of the closure rows are immaterial: closure RHS is zero.
MA=M.row_join(-FM)
print('rref',MA.shape,flush=True);t=time.time()
rr,piv=DomainMatrix.from_Matrix(MA).convert_to(QQ).rref()
rr=rr.to_Matrix()
print('rref sec',time.time()-t,'rank M',sum(k<231 for k in piv),'rank augmented',len(piv),flush=True)
constraints=[]
for row in range(rr.rows):
 if all(v==0 for v in rr[row,:231]) and any(v!=0 for v in rr[row,231:]):constraints.append(rr[row,231:])
constraints=s.Matrix.vstack(*constraints) if constraints else s.zeros(0,9)
print('coefficient constraints',constraints,flush=True)
print('allowed dimension',9-constraints.rank(),flush=True)
allowed=constraints.nullspace()
for bi in allowed:print('basis',list(bi),'F=',s.factor(sum((bi[k]*fbase[k] for k in range(9)),s.S(0))),flush=True)
# Use rref with all free certificate variables =0 to construct a linear right inverse on allowed coefficients.
Tlift=s.zeros(231,9)
for row,k in enumerate(piv):
 if k<231:
  for q in range(9):Tlift[k,q]=-rr[row,231+q]
assert all(M*Tlift*b==FM*b for b in allowed)
# rref is M*x-FM*f=0, so x= -rr_f f. Signs above verified.
with open(base/'family_data.pkl','wb') as f:pickle.dump({'GM':GM,'WM':WM,'FM':FM,'M':M,'rr':rr,'piv':piv,'constraints':constraints,'allowed':allowed,'Tlift':Tlift,'fbase':fbase},f)
print('saved',flush=True)
