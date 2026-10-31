"""Dense small-system diagnostics, not a scalable compiler or proof."""
import json
import numpy as np
from scipy.linalg import expm

I=np.eye(2,dtype=complex)
X=np.array([[0,1],[1,0]],complex)
Y=np.array([[0,-1j],[1j,0]],complex)
Z=np.diag([1,-1]).astype(complex)
sm=np.array([[0,1],[0,0]],complex)
def comm(H):
    n=len(H);eye=np.eye(n)
    return -1j*(np.kron(eye,H)-np.kron(H.T,eye))
def vec(a): return a.reshape(-1,order='F')
def mat(a,n): return a.reshape((n,n),order='F')
def ptr(a): return np.trace(a.reshape(2,4,2,4),axis1=1,axis2=3)
rho=(I+Y)/2
H0=.3*Y
As=[.7*X,.9*Z]
gammas=[.5,.8]
T=.7
Gamma=sum(g*np.linalg.norm(a,2)**2 for g,a in zip(gammas,As))
rows=[]
for scale in [1,8,64,512]:
    rates=[scale,1.7*scale]
    vs=np.sqrt(np.array(gammas)*rates)
    Xe=[np.kron(X,I),np.kron(I,X)]
    Sme=[np.kron(sm,I),np.kron(I,sm)]
    H=np.kron(H0,np.eye(4))+sum(v*np.kron(a,x) for v,a,x in zip(vs,As,Xe))
    jumps=[2*np.sqrt(l)*np.kron(I,s) for l,s in zip(rates,Sme)]
    G=comm(H)
    Jsuper=[]
    for j in jumps:
        jj=j.conj().T@j
        js=np.kron(j.conj(),j);Jsuper.append(js)
        G+=js-.5*(np.kron(np.eye(8),jj)+np.kron(jj.T,np.eye(8)))
    env=np.zeros((4,4),complex);env[0,0]=1
    initial=vec(np.kron(rho,env))
    out=ptr(mat(expm(T*G)@initial,8))
    C=np.zeros((16,16),complex)
    for s in range(4):
        hs=H0+sum(v*a*((-1)**((s>>i)&1)) for i,(v,a) in enumerate(zip(vs,As)))
        C[4*s:4*s+4,4*s:4*s+4]=comm(hs)-sum(rates)*np.eye(4)
        for i,l in enumerate(rates):
            d=s^(1<<i);C[4*d:4*d+4,4*s:4*s+4]+=l*np.eye(4)
    ci=np.tile(vec(rho)/4,4)
    co=expm(T*C)@ci
    cout=sum(mat(co[4*s:4*s+4],2) for s in range(4))
    err=np.linalg.norm(out-cout,ord='nuc')
    assert err<1e-10,(scale,err)
    counts=[]
    for theta in [.1,.5,1]:
        Gt=G+np.expm1(theta)*sum(Jsuper)
        mgf=np.trace(mat(expm(T*Gt)@initial,8)).real
        bound=np.exp(Gamma*T*np.expm1(theta))
        assert mgf<=bound+1e-10,(scale,theta,mgf,bound)
        counts.append({'theta':theta,'mgf':float(mgf),'upper_bound':float(bound)})
    rows.append({'rates':rates,'marginal_trace_norm_error':float(err),'count_checks':counts})
print(json.dumps({'scope':'dense floating diagnostics; no large-rate algorithm claim','Gamma':Gamma,'T':T,'rows':rows},indent=2))
