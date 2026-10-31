"""Small sparse finite-cutoff thermofield and activity diagnostics.
Not the infinite-domain proof or a compiled quantum algorithm.
"""
import json
import numpy as np
from scipy import sparse as sp
from scipy.sparse.linalg import expm_multiply

def annihilator(d):return sp.diags(np.sqrt(np.arange(1,d)),1,shape=(d,d),dtype=complex,format='csr')
def kron(*xs):
    y=xs[0]
    for x in xs[1:]:y=sp.kron(y,x,format='csr')
    return y
def generator(H,jumps):
    d=H.shape[0];I=sp.eye(d,dtype=complex,format='csr')
    G=-1j*(kron(I,H)-kron(H.T,I));JS=[]
    for J in jumps:
        C=J.conj().T@J;F=kron(J.conj(),J);JS.append(F)
        G+=F-.5*(kron(I,C)+kron(C.T,I))
    return G,JS
def evolve(G,rho,t):return (expm_multiply(t*G,rho.reshape(-1,order='F'))).reshape(rho.shape,order='F')
def marginal(rho,de):return np.trace(rho.reshape(2,de,2,de),axis1=1,axis2=3)

I=sp.eye(2,dtype=complex,format='csr');X=sp.csr_matrix([[0,1],[1,0]],dtype=complex)
Y=sp.csr_matrix([[0,-1j],[1j,0]],dtype=complex)
C=sp.csr_matrix([[0,1],[0,0]],dtype=complex)
H0=.3*Y;rho=(I.toarray()+Y.toarray())/2
lam=1.;g=.5;omega=.7;T=.6;nbar=.4
dp=18;ap=annihilator(dp);np_=ap.conj().T@ap
Hp=kron(H0,sp.eye(dp))+omega*kron(I,np_)+g*(kron(C,ap.conj().T)+kron(C.conj().T,ap))
Jp=[2*np.sqrt(lam*(nbar+1))*kron(I,ap),2*np.sqrt(lam*nbar)*kron(I,ap.conj().T)]
Gp,_=generator(Hp,Jp)
probs=(nbar/(1+nbar))**np.arange(dp);probs/=probs.sum()
rp=np.kron(rho,np.diag(probs));Up=kron(X,sp.eye(dp)).toarray()
rp=evolve(Gp,rp,T/2);rp=Up@rp@Up.conj().T;rp=evolve(Gp,rp,T/2);target=marginal(rp,dp)
rows=[]
for dv in [3,4,5]:
    a=annihilator(dv);n=a.conj().T@a;Ie=sp.eye(dv,dtype=complex,format='csr')
    Hv=kron(H0,Ie,Ie)+omega*(kron(I,n,Ie)-kron(I,Ie,n))
    Hv+=g*np.sqrt(nbar+1)*(kron(C,a.conj().T,Ie)+kron(C.conj().T,a,Ie))
    Hv+=g*np.sqrt(nbar)*(kron(C.conj().T,Ie,a.conj().T)+kron(C,Ie,a))
    Jv=[2*np.sqrt(lam)*kron(I,a,Ie),2*np.sqrt(lam)*kron(I,Ie,a)]
    Gv,JS=generator(Hv,Jv);env=np.zeros((dv*dv,dv*dv),complex);env[0,0]=1
    initial=np.kron(rho,env);Uv=kron(X,Ie,Ie).toarray()
    rv=evolve(Gv,initial,T/2);rv=Uv@rv@Uv.conj().T;rv=evolve(Gv,rv,T/2)
    err=np.linalg.norm(marginal(rv,dv*dv)-target,ord='nuc')
    theta=.2;Gt=Gv+np.expm1(theta)*sum(JS)
    tilt=evolve(Gt,initial,T/2);tilt=Uv@tilt@Uv.conj().T;tilt=evolve(Gt,tilt,T/2)
    mgf=np.trace(tilt).real;Gamma=g*g*(2*nbar+1)/lam
    bound=np.exp(Gamma*T*np.expm1(theta))
    assert mgf<=bound+1e-9
    numbers=np.repeat(np.add.outer(np.arange(dv),np.arange(dv)).reshape(-1)[None,:],2,axis=0).reshape(-1)
    occ=float(np.dot(2.**numbers,np.diag(rv).real));ob=np.exp(Gamma*T/4);assert occ<=ob+1e-9
    rows.append({'virtual_local_dimension':dv,'thermal_output_trace_error':float(err),'emission_mgf':float(mgf),'emission_bound':float(bound),'number_moment':occ,'number_bound':float(ob)})
assert rows[-1]['thermal_output_trace_error']<1e-5
print(json.dumps({'scope':'finite-cutoff sparse diagnostics only','physical_local_dimension':dp,'Gamma':Gamma,'rows':rows},indent=2))
