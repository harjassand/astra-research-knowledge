import numpy as np
from scipy.integrate import solve_ivp

I=np.eye(2,dtype=complex)
X=np.array([[0,1],[1,0]],complex)
Y=np.array([[0,-1j],[1j,0]],complex)
Z=np.diag([1,-1]).astype(complex)
sm=np.array([[0,1],[0,0]],complex)
def kron(*args):
    a=np.array([1.0],complex)
    for b in args: a=np.kron(a,b)
    return a

def pulse(t,Omega=1.0):
    T=np.pi/Omega
    a=np.sqrt(1/(2*T))
    tail=a*a*(1.5*(T-t)+np.sin(4*Omega*t)/(2*Omega)-np.sin(8*Omega*t)/(16*Omega))
    w=a*(1-np.cos(4*Omega*t))*np.exp(-1j*Omega*t)
    return np.conjugate(w)/np.sqrt(1-tail)

def simulate(eta,mu=.005,s=.2,rtol=1e-11,atol=1e-13):
    T=np.pi; gamma=mu/T
    H=kron(I,X,I)/2
    C=np.sqrt(eta*gamma)*kron(I,Z,I)
    L=np.sqrt((1-eta)*gamma)*kron(I,Z,I)
    R0=kron(I,I,sm)
    plus=np.array([1,1])/np.sqrt(2)
    minus=np.array([1,-1])/np.sqrt(2)
    zero=np.array([1,0]);one=np.array([0,1])
    psi=(kron(zero,plus,zero)+kron(one,minus,zero))/np.sqrt(2)
    rho=np.outer(psi,psi.conjugate())
    def rhs(t,y):
        A=y.reshape(8,8)
        R=pulse(t)*R0
        J=C+R
        h=H+(R.conj().T@C-C.conj().T@R)/(2j)
        D=-1j*(h@A-A@h)
        for K in [J,L]:
            Q=K.conj().T@K
            D+=K@A@K.conj().T-(Q@A+A@Q)/2
        return D.ravel()
    sol=solve_ivp(rhs,(0,T),rho.ravel(),method='DOP853',rtol=rtol,atol=atol)
    rho=sol.y[:,-1].reshape(8,8)
    v=np.sqrt(eta*mu/2)
    F=kron(np.diag([1,np.sqrt(s)]),I,np.diag([np.sqrt(s)*v,1]))
    rho=F@rho@F.conj().T
    ar=np.trace(rho.reshape(2,2,2,2,2,2),axis1=1,axis2=4).reshape(4,4)
    bell=np.array([1,0,0,-1])/np.sqrt(2)
    p=np.trace(ar).real
    fidelity=(bell.conj()@ar@bell).real/p
    p0=np.exp(-mu)*s*eta*mu/2
    ratio=s/2+np.expm1(mu)*(1+2/s)
    return {'eta':eta,'success':p,'success_over_eta':p/eta,'bell_fidelity':fidelity,
            'guaranteed_success':p0,'guaranteed_fidelity':1/(1+ratio),'rhs_evals':sol.nfev,
            'min_eigenvalue':np.linalg.eigvalsh((ar+ar.conj().T)/2).min().real,
            'raw_state':ar/p}

def purification(q):
    bad=30*(q/3)**3*(1-q)**2+18*(q/3)**5
    good=(1-q)**5+15*(q/3)**4*(1-q)
    return bad/(bad+good),bad+good

if __name__=='__main__':
    for eta in [1.,.1,.01,.001]:
        x=simulate(eta);x.pop('raw_state');print(x)
    r=.1+np.expm1(.005)*11
    q=r/(1+r);cost=1
    print('purification_initial',q)
    for level in range(1,5):
        q,a=purification(q);cost*=5/a
        print({'level':level,'error':q,'accept':a,'expected_raw_pairs':cost})
