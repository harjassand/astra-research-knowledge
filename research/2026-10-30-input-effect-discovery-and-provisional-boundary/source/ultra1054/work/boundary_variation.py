"""Compatible Fourier construction against the actual quadratic ROC boundary.

Numerical proposals ONLY. Every acoustic chart is analytically deflated at
its null; no root-pseudoinverse or finite-grid admission is used as a proof.
"""
from pathlib import Path
import json,time,sys
import numpy as np,scipy.linalg as la
from scipy.optimize import minimize
import cvxpy as cp
from fractions import Fraction
root=Path(__file__).resolve().parents[1]
gd=json.loads((root/'outputs/graded_stabilization/certificate.json').read_text())
bd=json.loads((root/'outputs/hopf_structure/certificate.json').read_text())
ad=json.loads((root/'work/actual_boundary.json').read_text())
cpows=np.array(gd['cubic_powers']);qpows=np.array([p for p in __import__('itertools').product(range(3),repeat=4) if sum(p)==2])
CM=np.array(gd['cubic_constraint_matrix'],float);CM/=np.linalg.norm(CM,axis=1)[:,None]
N=la.null_space(CM);assert N.shape==(20,12)
null_det=np.array([int(tuple(p)==(1,0,0,1))-int(tuple(p)==(0,1,1,0)) for p in qpows],float)
QN=la.null_space(null_det[None,:]);assert QN.shape==(10,9)
def monomials(points,powers):return np.prod(np.asarray(points)[...,None,:]**powers,axis=-1)
def derivatives(points,powers):
    points=np.asarray(points);out=[]
    for j in range(4):
        ee=powers.copy();co=ee[:,j].copy();ee[:,j]=np.maximum(ee[:,j]-1,0)
        out.append(monomials(points,ee)*co)
    return np.stack(out,axis=-2)
Fpow=np.array([row[:4] for row in ad['F']]);Fco=np.array([float(Fraction(row[4],row[5])) for row in ad['F']])
def Fvalue(v):return monomials(v,Fpow)@Fco
def Hvalue(v):
    out=np.empty((4,4))
    for i in range(4):
        for j in range(4):
            ee=Fpow.copy();co=Fco*ee[:,i];ee[:,i]=np.maximum(ee[:,i]-1,0);co=co*ee[:,j];ee[:,j]=np.maximum(ee[:,j]-1,0)
            out[i,j]=monomials(v,ee)@co
    return out
av=np.array([float(Fraction(x)) for x in bd['ray']['A0']]);a,b,c,d=av
kernel=[av,np.array([-b,a,d,-c])];charts=[]
for chart in (0,1):
    e0=np.array([1.,0,0,0]) if chart==0 else np.array([0,1.,0,0]);e1=np.array([0,1.,0,0]) if chart==0 else np.array([1.,0,0,0])
    H0=Hvalue(e0);H2=Hvalue(e1);H1=Hvalue(e0+e1)-H0-H2
    V=la.null_space(kernel[chart][None,:]);Q=np.column_stack((kernel[chart]/la.norm(kernel[chart]),V))
    Z=[Q.T@H@Q for H in (H0,H1,H2)];assert la.norm(Z[0][:,0])<1e-11 and abs(Z[1][0,0])<1e-11
    charts.append((Q,Z,e0,e1))
def acoustic(theta,phi):
    x,y=np.cos(theta),np.sin(theta);v,w=np.cos(phi),np.sin(phi)
    U=np.array([[x,0,-y,0],[0,x,0,-y],[y,0,x,0],[0,y,0,x]])
    chart=0 if abs(v)>=abs(w) else 1;t=w/v if chart==0 else v/w
    Q,HH,e0,e1=charts[chart]
    J=HH[0]+t*HH[1]+t*t*HH[2]
    J[0,0]=HH[2][0,0];J[0,1:]=HH[1][0,1:]+t*HH[2][0,1:];J[1:,0]=J[0,1:]
    G0=derivatives(U@e0,cpows)@N;G2=derivatives(U@e1,cpows)@N
    G1=derivatives(U@(e0+e1),cpows)@N-G0-G2
    ZZ=[Q.T@U.T@G for G in (G0,G1,G2)]
    Z=ZZ[0]+t*ZZ[1]+t*t*ZZ[2];Z[0]=ZZ[1][0]+t*ZZ[2][0]
    vals,vecs=la.eigh(J);assert vals[0]>0
    D=(vecs.T@Z)/np.sqrt(vals[:,None]*(1+t*t))
    Rv=np.array([x*v,x*w,y*v,y*w]);qrow=monomials(Rv,qpows)@QN
    return D,qrow
def field(vectors,mode='triad'):
    nn=12;xx,yy=np.meshgrid(np.arange(nn)*2*np.pi/nn,np.arange(nn)*2*np.pi/nn,indexing='ij')
    if mode=='triad':freqs=np.array([[1,0],[0,1],[1,1]])
    else:freqs=np.array(mode)
    G=np.zeros((nn,nn,4))
    for vi,ki in zip(vectors,freqs):G+=np.outer(vi,ki).ravel()*np.cos(ki[0]*xx+ki[1]*yy)[...,None]
    G/=np.sqrt(np.mean(np.sum(G*G,axis=-1)))
    Fbar=float(np.mean(Fvalue(G)));cb=np.mean(monomials(G,cpows),axis=(0,1))@N
    qb=np.mean(monomials(G,qpows),axis=(0,1))@QN
    return Fbar,cb,qb,G
def solve_shape(vectors,points,maxcuts=8,mode='triad'):
    Fbar,cb,qb,G=field(vectors,mode);points=list(points)
    # The true Fourier mode directions are admitted as acoustic obligations.
    freqs=np.array([[1,0],[0,1],[1,1]]) if mode=='triad' else np.array(mode)
    for vi,ki in zip(vectors,freqs):points.append((float(np.arctan2(vi[1],vi[0])%np.pi),float(np.arctan2(ki[1],ki[0])%np.pi)))
    z=cp.Variable(12);q=cp.Variable(9)
    for iteration in range(maxcuts):
        cons=[]
        for th,ph in points:
            D,qr=acoustic(th,ph);s=qr@q
            cons.append(cp.SOC(s+1,cp.hstack([np.sqrt(2)*D@z,s-1])))
        # A bound regularizes exploratory solves, never certifies a candidate.
        cons.append(cp.norm(q)<=1000)
        problem=cp.Problem(cp.Minimize(Fbar+cb@z+qb@q),cons)
        problem.solve(solver='CLARABEL',tol_gap_abs=1e-8,tol_feas=1e-8,tol_gap_rel=1e-8,max_iter=200)
        if z.value is None:raise ValueError(problem.status)
        zv=z.value.copy();qv=q.value.copy()
        def violation(v):
            D,qr=acoustic(*v);val=D@zv;return float(val@val-2*(qr@qv))
        grid=[(i*np.pi/15,j*np.pi/15) for i in range(15) for j in range(15)]
        vals=sorted(((violation(p),p) for p in grid),reverse=True);new=[]
        for _,initial in vals[:6]:
            res=minimize(lambda v:-violation(v),np.array(initial),method='BFGS',options={'maxiter':70,'gtol':1e-7})
            vv=violation(res.x);point=tuple(float(x%np.pi) for x in res.x)
            if vv>1e-7:new.append((vv,point))
        largest=max([val for val,_ in new],default=vals[0][0])
        if not new:break
        points.extend(p for _,p in new)
    return {'value':float(problem.value),'Fbar':Fbar,'max_numerical_violation':largest,'iterations':iteration+1,
      'cubic_coefficients':(N@zv).tolist(),'quadratic_coefficients':(QN@qv).tolist(),
      'points':[list(p) for p in points],'vectors':np.asarray(vectors).tolist(),
      'mode':mode,'scope':'Numerical construction only; continuous acoustic optimization is not an exact ROC certificate.'}
if __name__=='__main__':
    start=time.perf_counter();pts=[(i*np.pi/10,j*np.pi/10) for i in range(10) for j in range(10)]
    shapes=[np.array([[1.,0],[0,1.],[1.,1.]]),np.array([[1.,0],[0,1.],[1.,-1.]]),np.array([[1.,1],[1,-1.],[1.,0]])]
    best=None
    for i,vectors in enumerate(shapes):
        result=solve_shape(vectors,pts);print(json.dumps({k:result[k] for k in ('value','Fbar','max_numerical_violation','iterations')}),flush=True)
        if best is None or result['value']<best['value']:best=result
        (root/'work/actual_boundary_proposal.json').write_text(json.dumps({'best':best,'seconds':time.perf_counter()-start},indent=2)+'\n')
