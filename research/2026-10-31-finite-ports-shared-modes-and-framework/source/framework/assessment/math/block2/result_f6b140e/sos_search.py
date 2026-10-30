"""Local SOS discovery for optimized ordinary-heat certificates.
Numerical feasibility is diagnostic only; exact receiver required for any claim.
"""
from optimize_primitive import *
import numpy as np
import json
X=x1+s.I*x2;Y=y1+s.I*y2;P=P1+s.I*P2;Q=Q1+s.I*Q2;R=R1+s.I*R2
ab2=lambda z:s.expand(z*s.conjugate(z))
re=lambda z:s.expand((z+s.conjugate(z))/2)
g,aa,bb,nu=s.symbols('g aa bb nu',real=True)
full=Lrt+2*re(s.conjugate(X)*Q*R)+(4-g)*re(Y*Q*s.conjugate(P))+g*re(Y*R*s.conjugate(Q))+aa*ab2(P)+bb*ab2(Q)+(4*nu-aa-bb)*ab2(R)
groups=[[s.conjugate(X)*P,s.conjugate(Y)*Q,X*s.conjugate(Q),Y*s.conjugate(R),R],[s.conjugate(Y)*P,Y*R,X*s.conjugate(R),Q],[X*R,Y*Q,P],[X*Q,Y*P],[X*P]]
gs=[]; expr=0;entries=[];mats=[]
for k,zs in enumerate(groups):
    mat=s.zeros(len(zs))
    for i in range(len(zs)):
        for j in range(i,len(zs)):
            v=s.Symbol(f'G{k}_{i}_{j}',real=True);gs.append(v);entries.append((k,i,j));mat[i,j]=mat[j,i]=v
            expr+=v*(ab2(zs[i]) if i==j else 2*re(zs[i]*s.conjugate(zs[j])))
    mats.append(mat)
unknown=gs+[r,t,g,aa,bb]
poly=s.Poly(s.expand(expr-full),*vars)
Am,bm=s.linear_eq_to_matrix(poly.coeffs(),unknown)
print('SOS linear system',Am.shape,'rank',Am.rank(),flush=True)
np.savez(__file__.replace('.py','_system.npz'),A=np.array(Am,dtype=float),b0=np.array(bm.subs(nu,0),dtype=float).ravel(),b1=np.array(bm.diff(nu),dtype=float).ravel())
nuval=float(__import__('sys').argv[1]) if len(__import__('sys').argv)>1 else .1875
Amn=np.array(Am,dtype=float);bn=np.array(bm.subs(nu,nuval),dtype=float).ravel()
# Frobenius coordinates for symmetric matrices.
weights=np.array([1 if i==j else 2**.5 for k,i,j in entries]+[1]*5)
At=Amn/weights[None,:]
pi=np.linalg.pinv(At,rcond=1e-10)
proj_aff=lambda v:v+pi@(bn-At@v)
def proj_psd(v):
    ans=v.copy();offset=0
    for zs in groups:
        nn=len(zs);ma=np.zeros((nn,nn));ids=[]
        for i in range(nn):
            for j in range(i,nn):
                idx=offset;val=v[idx]/weights[idx];ma[i,j]=ma[j,i]=val;ids.append((idx,i,j));offset+=1
        lam,vec=np.linalg.eigh(ma);pos=(vec*np.maximum(lam,0))@vec.T
        for idx,i,j in ids:ans[idx]=pos[i,j]*weights[idx]
    return ans
v=np.zeros(len(unknown));best=1e9
for it in range(40000):
    pa=proj_aff(v); pb=proj_psd(2*pa-v);v+=pb-pa
    if it%1000==0:
        feas=proj_aff(v);err=np.linalg.norm(feas-proj_psd(feas));
        if err<best:best=err
        if it%10000==0:print('iteration',it,'residual',err,'params',feas[-5:],flush=True)
        if err<1e-9:break
out=proj_aff(v)/weights
print('FINAL',it,'residual',best,'parameters',out[-5:],flush=True)
for ma in mats:
    vals=np.array(ma.subs(dict(zip(unknown,out))),dtype=float);print(vals,flush=True);print('eigenvalues',np.linalg.eigvalsh(vals),flush=True)
open(__file__.replace('.py',f'_{nuval}_result.json'),'w').write(json.dumps(dict(nu=nuval,error=float(best),unknowns={str(k):float(val) for k,val in zip(unknown,out)}),indent=2))
