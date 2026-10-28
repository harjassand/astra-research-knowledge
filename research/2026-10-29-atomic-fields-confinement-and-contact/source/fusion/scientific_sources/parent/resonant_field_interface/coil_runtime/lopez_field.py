"""Direct evaluation of arXiv:2610.29921v1 eqs.(3),(12),(13).
Length unit and magnetic field amplitude are arbitrary. No physical coil is assumed.
"""
import numpy as np

def X(lam,beta,phi):
    lam,beta,phi=np.broadcast_arrays(lam,beta,phi)
    t=np.sqrt(lam); den=1+lam
    A=np.array([1-lam*np.cos(2*phi),-lam*np.sin(2*phi),2*t*np.cos(phi)])
    C=np.array([-lam*np.sin(2*phi),1+lam*np.cos(2*phi),2*t*np.sin(phi)])
    Hre=2*lam*np.cos(2*phi)-2*lam*t*np.sin(3*phi)
    Him=2*lam*np.sin(2*phi)+2*lam*t*np.cos(3*phi)
    n=np.array([2*t*np.cos(phi),2*t*np.sin(phi),(lam-1)+0*phi])/den
    kappa=4*lam*t*np.cos(phi)*(1-t*np.sin(phi))/den**2
    return (Hre*A+Him*C)/den**2+(beta-kappa)*n

def derivative(lam,beta,phi,index):
    v=[lam,beta,phi]; v[index]=np.asarray(v[index],dtype=complex)+1e-25j
    return np.imag(X(*v))/1e-25

def h(lam,beta,phi):
    xp=derivative(lam,beta,phi,2)
    return np.sqrt(np.sum(xp*xp,axis=0))

def B_at_labels(lam,beta,phi):
    xp=derivative(lam,beta,phi,2)
    return xp/np.sum(xp*xp,axis=0)

def Q(lam,beta): return 900*(lam-.15)**2+100*(beta-.02)**2

def surface(r,theta,phi):
    return X(.15+r*np.cos(theta)/30,.02+r*np.sin(theta)/10,phi)

def surface_theta(r,theta,phi):
    lam=.15+r*np.cos(theta)/30; beta=.02+r*np.sin(theta)/10
    return -r*np.sin(theta)/30*derivative(lam,beta,phi,0)+r*np.cos(theta)/10*derivative(lam,beta,phi,1)

def root_at_cartesian(x):
    xx,yy,zz=x; w=xx+1j*yy
    roots=np.roots([2j,np.conj(w)+2,-2*zz,-w])
    lam=abs(roots)**2
    n=np.array([2*roots.real,2*roots.imag,lam-1])/(1+lam)
    kap=4*lam*roots.real*(1-roots.imag)/(1+lam)**2
    beta=np.einsum('ij,i->j',n,x)+kap
    qs=Q(lam,beta)
    k=np.argmin(qs)
    return roots[k],float(lam[k]),float(beta[k]),float(qs[k])

def B_cartesian(x,derivatives=False):
    z,lam,beta,q=root_at_cartesian(x)
    xx,yy,zz=x; wb=xx-1j*yy
    D=6j*z*z+2*(wb+2)*z-2*zz
    N=np.array([1-z*z,1j*(1+z*z),2*z])
    F=N/(z*D)
    if not derivatives: return F.imag
    Np=np.array([-2*z,2j*z,2])
    M=np.array([2*z,-2j*z,-2])
    zgrad=N/D
    Dgrad=(12j*z+2*(wb+2))*zgrad+M
    Agrad=zgrad*D+z*Dgrad
    dF=np.outer(Np,zgrad)/(z*D)-np.outer(N,Agrad)/(z*D)**2
    return F.imag,dF.imag
