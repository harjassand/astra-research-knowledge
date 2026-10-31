"""Exact algebra/rational bounds plus separately labeled floating diagnostics.
Not a gate backend, hardware test, or generic numerical certificate.
"""
from fractions import Fraction as F
import json
from pathlib import Path
import sympy as S
import numpy as np
from scipy.linalg import expm

def rational_bracket(lam,c,T):
    lam,c,T=map(F,(lam,c,T))
    if lam<=0 or c<0 or T<0:raise ValueError('invalid physical parameters')
    U=4*c*c*T/lam
    A=max(F(0),U-8*c*c/(lam*lam))
    lower=A*max(F(0),1-2*U)
    return lower,min(F(1),U)

def run():
    checks=[]
    def ck(n,b):assert b,n;checks.append(n)
    l,c=S.symbols('lambda c',positive=True,real=True)
    X=S.Matrix([[0,1],[1,0]]);Z=S.diag(1,-1);L=S.Matrix([[0,1],[0,0]])
    vs=S.symbols('v0:4');rho=S.Matrix(2,2,vs)
    cross=-S.I*c*(X*rho+rho*X)+l*(L*rho*L.H-(L.H*L*rho+rho*L.H*L)/2)
    ck('exact f first equation',S.expand(S.trace(cross)+2*S.I*c*S.trace(X*rho))==0)
    ck('exact x first equation',S.expand(S.trace(X*cross)+2*S.I*c*S.trace(rho)+l*S.trace(X*rho)/2)==0)
    # Canonical two-environment-vector isometry, rational parameter family.
    for t in [S.Rational(j,20) for j in range(1,20)]:
        # sqrt(1-p)=(1-t²)/(1+t²), so all overlap geometry is exact.
        a=(1-t*t)/(1+t*t); b=2*t/(1+t*t);p=b*b
        e0=S.Matrix([a,b]);e1=S.Matrix([a,-b]);ideal=S.Matrix([1,0])
        d2=S.expand(((e0-ideal).T*(e0-ideal))[0])
        ck('exact optimized geometry '+str(t),S.simplify(d2-(2-2*a))==0 and p<=d2<=2*p)
    exact=[]
    for lam in [16,64,1000,10**6]:
        for c0 in [F(1,10),F(1,2),F(1)]:
            for T in [F(1,4),F(1),F(4)]:
                if lam*T>=4 and 8*c0*c0*T/lam<=F(1,2):
                    lo,hi=rational_bracket(lam,c0,T)
                    ck('finite rational scale '+str((lam,c0,T)),lo>=c0*c0*T/lam and hi<=4*c0*c0*T/lam)
                    exact.append({'lambda':str(lam),'c':str(c0),'T':str(T),'p_lower':str(lo),'p_upper':str(hi),'optimized_isometry_squared_lower':str(lo),'optimized_isometry_squared_upper':str(2*hi)})
    # Independent 16-dimensional Liouvillian versus closed 2-dimensional ODE.
    I=np.eye(2);Xn=np.array(X,float);Zn=np.array(Z,float);Ln=np.array(L,float);rows=[]
    for lam in [.1,1.,8.,100.,1000.]:
        for c0 in [.1,1.,3.]:
            for T in [.01,.2,1.]:
                H=c0*np.kron(Xn,Zn);J=np.kron(Ln,I);C=J.T@J
                G=-1j*(np.kron(np.eye(4),H)-np.kron(H.T,np.eye(4)))+lam*(np.kron(J,J)-(np.kron(np.eye(4),C)+np.kron(C.T,np.eye(4)))/2)
                rho=np.kron(np.diag([1.,0.]),np.array([[.5,.5],[.5,.5]]))
                full=(expm(T*G)@rho.reshape(-1,order='F')).reshape((4,4),order='F')
                ffull=2*(full[0,1]+full[2,3]);fred=(expm(T*np.array([[0.,1.],[-4*c0*c0,-lam/2]]))@np.array([1.,0.]))[0]
                tol=5e-10
                ck('dense ODE diagnostic '+str((lam,c0,T)),abs(ffull-fred)<tol)
                p=(1-fred)/2; lo,hi=rational_bracket(F(str(lam)),F(str(c0)),F(str(T)))
                ck('bound diagnostic '+str((lam,c0,T)),float(lo)-tol<=p<=float(hi)+tol)
                rows.append({'lambda':lam,'c':c0,'T':T,'p_double':p,'ode_residual':float(abs(ffull-fred))})
    return {'count':len(checks),'checks':checks,'exact_rational_certificates':exact,'floating_diagnostics':rows,'scope':'symbolic identities and exact rational sufficient bounds are certified by arithmetic; dense floating checks are diagnostics only'}
if __name__=='__main__':
    out=run();Path(__file__).with_name('benchmark_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(out['count'],'checks passed')
