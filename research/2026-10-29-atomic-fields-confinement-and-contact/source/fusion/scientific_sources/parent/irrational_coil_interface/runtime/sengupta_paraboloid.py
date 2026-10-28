"""Independent implementation of 2610.28466v1, equations (1),(2),(5)-(7).

This is the reference paraboloidal member, not the ellipsoidal trapped
iso-action orbit already studied by the authors. All units are dimensionless.
The source's minus sign in X_y is essential for its declared metric.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'positive_current_operation'/'vendor'))
import numpy as np
from scipy.special import ellipj,ellipk

_lo,_hi=1e-9,.99
for _ in range(80):
    _mid=(_lo+_hi)/2
    if ellipk(1-_mid)/ellipk(_mid)>2.5:_lo=_mid
    else:_hi=_mid
M=(_lo+_hi)/2
KMOD=np.sqrt(M);K=ellipk(M);KP=ellipk(1-M)
KAPPA=2*KP/np.pi
U0=np.arccosh(np.sqrt(5)/np.cosh(2*np.pi/5))
PSI0=1/KMOD-1


def complex_jacobi(z):
    """Complex Jacobi functions via the real addition identities."""
    su,cu,du,_=ellipj(np.real(z),M)
    sv,cv,dv,_=ellipj(np.imag(z),1-M)
    den=cv*cv+M*su*su*sv*sv
    sn=(su*dv+1j*cu*du*sv*cv)/den
    cn=(cu*cv-1j*su*du*sv*dv)/den
    dn=(du*cv*dv-1j*M*su*cu*sv)/den
    return sn,cn,dn


def embedding(q):
    u,v,z=np.moveaxis(np.asarray(q),-1,0)
    su,sv=np.sinh(u),np.sinh(v);c,s=np.cos(z),np.sin(z)
    return np.stack((su*c-sv*s,su*s-sv*c,su*sv+.5*np.sin(2*z)),axis=-1)


def jacobian(q):
    u,v,z=np.moveaxis(np.asarray(q),-1,0)
    su,sv,cu,cv=np.sinh(u),np.sinh(v),np.cosh(u),np.cosh(v)
    c,s=np.cos(z),np.sin(z)
    xu=np.stack((cu*c,cu*s,cu*sv),axis=-1)
    xv=np.stack((-cv*s,-cv*c,su*cv),axis=-1)
    xz=np.stack((-su*s-sv*c,su*c+sv*s,np.cos(2*z)),axis=-1)
    return np.stack((xu,xv,xz),axis=-1)


def surface_label(q):
    u,v,z=np.moveaxis(np.asarray(q),-1,0)
    _,cx,dx,_=ellipj(KAPPA*(u-U0),M)
    _,cy,dy,_=ellipj(KAPPA*v,M)
    U=cx/dx;V=dy/(KMOD*cy)
    s,c,d,_=ellipj(KAPPA*z,1-M)
    return np.sqrt(d*d*(U-V)**2/((c*c+M*U*U*s*s)*(c*c+M*V*V*s*s)))


def label_partials(q):
    """Analytic derivatives of source equation (2)."""
    u,v,z=np.moveaxis(np.asarray(q),-1,0)
    sx,cx,dx,_=ellipj(KAPPA*(u-U0),M)
    sy,cy,dy,_=ellipj(KAPPA*v,M)
    U=cx/dx;V=dy/(KMOD*cy)
    Uu=-KAPPA*(1-M)*sx/dx**2;Vv=KAPPA*(1-M)*sy/(KMOD*cy**2)
    sf,cf,df,_=ellipj(KAPPA*z,1-M)
    sp=KAPPA*cf*df;cp=-KAPPA*sf*df;dp=-KAPPA*(1-M)*sf*cf
    D1=cf**2+M*U**2*sf**2;D2=cf**2+M*V**2*sf**2
    psi=np.sqrt(df**2*(U-V)**2/(D1*D2))
    pu=Uu/(U-V)-M*U*Uu*sf**2/D1
    pv=-Vv/(U-V)-M*V*Vv*sf**2/D2
    pz=dp/df-(cf*cp+M*U**2*sf*sp)/D1-(cf*cp+M*V**2*sf*sp)/D2
    return psi[...,None]*np.stack((pu,pv,pz),axis=-1)


def data(q,gradient=False):
    u,v,z=np.moveaxis(np.asarray(q),-1,0)
    su,sv,cu,cv=np.sinh(u),np.sinh(v),np.cosh(u),np.cosh(v)
    P=cu*cv;E=su*sv-np.sin(2*z);D=P*P-E*E;h=E/P
    p1,c1,d1=complex_jacobi(K+KAPPA*(u-U0)+1j*KAPPA*z)
    p2,c2,d2=complex_jacobi(K+KAPPA*v+1j*(KP+KAPPA*z))
    b,e,A=p1.imag,p2.imag,(p1+p2).real
    contrav=np.stack((b-h*e,e-h*b,A),axis=-1)/D[...,None]
    J=jacobian(q);field=np.einsum('...ij,...j->...i',J,contrav)
    N=b*b+e*e-2*h*b*e+A*A;strength=np.sqrt(N/D)
    out={'B':field,'strength':strength,'contravariant':contrav,'D':D,'A':A,'J':J}
    if gradient:
        zero=np.zeros_like(u)
        Pq=np.stack((su*cv,cu*sv,zero),axis=-1)
        Eq=np.stack((cu*sv,su*cv,-2*np.cos(2*z)),axis=-1)
        Dq=2*P[...,None]*Pq-2*E[...,None]*Eq
        hq=(Eq-h[...,None]*Pq)/P[...,None]
        p1q=KAPPA*c1*d1;p2q=KAPPA*c2*d2
        bq=np.stack((p1q.imag,zero,p1q.real),axis=-1)
        eq=np.stack((zero,p2q.imag,p2q.real),axis=-1)
        Aq=np.stack((p1q.real,p2q.real,-(p1q+p2q).imag),axis=-1)
        Nq=2*b[...,None]*bq+2*e[...,None]*eq-2*(b*e)[...,None]*hq-2*h[...,None]*(e[...,None]*bq+b[...,None]*eq)+2*A[...,None]*Aq
        partial=(Nq*D[...,None]-N[...,None]*Dq)/(2*strength[...,None]*D[...,None]**2)
        out['grad_strength']=np.linalg.solve(np.swapaxes(J,-1,-2),partial[...,None])[...,0]
    return out


def gc_rhs(q,vparallel,mu,epsilon):
    vals=data(q,True);B=vals['B'];mag=vals['strength'];b=B/mag[...,None];grad=vals['grad_strength']
    velocity=vparallel[...,None]*b+epsilon*(vparallel*vparallel+mu*mag)[...,None]*np.cross(b,grad)/mag[...,None]**2
    qdot=np.linalg.solve(vals['J'],velocity[...,None])[...,0]
    vdot=-mu*np.sum(b*grad,axis=-1)
    return qdot,vdot


def regular(q):
    u,v,_=np.moveaxis(np.asarray(q),-1,0)
    return (u>abs(v))&(abs(KAPPA*(u-U0))<K)&(abs(KAPPA*v)<K)
