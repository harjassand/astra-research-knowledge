"""Independent source-formula geometry/field operations for López 2610.29921v1.

Length and field amplitude units remain independent.  Source field is grad(phi).
Labels are source-certified only on Q<1.  Never silently change cubic roots
after leaving that domain.  No particle-confinement result is imported.
"""
import numpy as np
from lopez_formula_snapshot import X as _X


def embedding(lam,beta,phi):
    return np.moveaxis(_X(lam,beta,phi),0,-1)


def jacobian(lam,beta,phi):
    vals=np.broadcast_arrays(lam,beta,phi)
    cols=[]
    for j in range(3):
        a=[np.asarray(v,dtype=complex) for v in vals]
        a[j]=a[j]+1e-25j
        cols.append(embedding(*a).imag/1e-25)
    return np.stack(cols,axis=-1)


def h_analytic(lam,beta,phi):
    """Closed real algebra for |X_phi|; analytically extendible for derivatives.

    From H=2*zeta^2+2i*zeta^3 and N'.n=-2, D=H'-2H*zeta_bar/(1+lam)+2(beta-kappa).
    Its real/imaginary components below use only ordinary real algebra, then
    h^2=lam*|D|^2/(1+lam)^2 (source eqs.19,23,24).
    """
    t=np.sqrt(lam);u=t*np.cos(phi);v=t*np.sin(phi);den=1+lam
    dre=2*beta+4*u*((1-lam)-(lam*lam+2*lam+3)*v)/den**2
    dim=(4*v+2*(3+lam)*(lam-2*v*v))/den
    return np.sqrt(lam*(dre*dre+dim*dim))/den


def h_derivative(lam,beta,phi,index):
    a=list(np.broadcast_arrays(lam,beta,phi))
    a[index]=np.asarray(a[index],complex)+1e-25j
    return h_analytic(*a).imag/1e-25


def Q(lam,beta):return 900*(lam-.15)**2+100*(beta-.02)**2


def label_data(x,zeta):
    lam=abs(zeta)**2
    n=np.stack((2*zeta.real,2*zeta.imag,lam-1),axis=-1)/(1+lam)[...,None]
    kap=4*lam*zeta.real*(1-zeta.imag)/(1+lam)**2
    beta=np.sum(n*x,axis=-1)+kap
    return lam,beta,Q(lam,beta)


def root_continue(x,seed,iterations=6):
    z=np.array(seed,dtype=complex,copy=True)
    w=x[...,0]+1j*x[...,1];wb=w.conj();zz=x[...,2]
    for _ in range(iterations):
        g=2j*z**3+(wb+2)*z*z-2*zz*z-w
        d=6j*z*z+2*(wb+2)*z-2*zz
        z-=g/d
    residual=abs((2j*z**3+(wb+2)*z*z-2*zz*z-w)/(6j*z*z+2*(wb+2)*z-2*zz))
    return z,residual


def field_known_root(x,z,gradient=False):
    wb=x[...,0]-1j*x[...,1];zz=x[...,2]
    d=6j*z*z+2*(wb+2)*z-2*zz
    n=np.stack((1-z*z,1j*(1+z*z),2*z),axis=-1)
    f=n/(z*d)[...,None]
    if not gradient:return f.imag
    nprime=np.stack((-2*z,2j*z,np.full_like(z,2)),axis=-1)
    explicit=np.stack((2*z,-2j*z,np.full_like(z,-2)),axis=-1)
    zg=n/d[...,None]
    dg=(12j*z+2*(wb+2))[...,None]*zg+explicit
    ag=zg*d[...,None]+z[...,None]*dg
    df=nprime[..., :,None]*zg[...,None,:]/(z*d)[...,None,None]-n[..., :,None]*ag[...,None,:]/(z*d)[...,None,None]**2
    return f.imag,df.imag


def field_labels(lam,beta,phi,gradient=False):
    x=embedding(lam,beta,phi);z=np.sqrt(lam)*np.exp(1j*phi)
    return field_known_root(x,z,gradient)


def gc_rhs(labels,vparallel,mu,epsilon):
    lam,beta,phi=np.moveaxis(labels,-1,0)
    bvec,db=field_labels(lam,beta,phi,True)
    strength=np.linalg.norm(bvec,axis=-1);b=bvec/strength[...,None]
    grad=np.einsum('...ij,...i->...j',db,b)
    drift=epsilon*(vparallel*vparallel+mu*strength)[...,None]*np.cross(b,grad)/strength[...,None]**2
    inv=np.linalg.inv(jacobian(lam,beta,phi))
    qdot=np.einsum('...ij,...j->...i',inv,drift)
    qdot[...,2]+=vparallel/ h_analytic(lam,beta,phi)
    vdot=-mu*np.sum(b*grad,axis=-1)
    return qdot,vdot


def gc_label_rhs(labels,vparallel,mu,epsilon):
    """Exact first-order vacuum GC equations in this source chart.

    A=(log(lam)/2)*grad(beta), b.dX=h*dphi.  The guiding-center
    one-form is log(lam)/(2*epsilon)*d beta + vparallel*h*d phi.
    H=vparallel^2/2+mu/h.  No field-root inversion or averaging is used.
    """
    lam,beta,phi=np.moveaxis(labels,-1,0)
    h=h_analytic(lam,beta,phi)
    hl=h_derivative(lam,beta,phi,0);hb=h_derivative(lam,beta,phi,1);hp=h_derivative(lam,beta,phi,2)
    factor=2*epsilon*lam*(vparallel*vparallel/h+mu/h**2)
    qdot=np.stack((factor*hb,-factor*hl,vparallel/h),axis=-1)
    vdot=mu*hp/h**3
    return qdot,vdot
