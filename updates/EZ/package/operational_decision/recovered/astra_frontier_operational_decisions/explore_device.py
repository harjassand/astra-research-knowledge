import numpy as np
from scipy.linalg import solve
I=np.eye(2); sm=np.array([[0.,1.],[0.,0.]]); Z=np.diag([1.,-1.]); n=sm.T@sm
N=4; dim=2**N

def emb(a,i):
    z=np.array([[1.]])
    for j in range(N): z=np.kron(z,a if i==j else I)
    return z
S=[emb(sm,i).astype(complex) for i in range(N)]; Ns=[a.conj().T@a for a in S]; Zs=[emb(Z,i) for i in range(N)]
Id=np.eye(dim); ident=np.eye(dim*dim)
def diss(L):
    P=L.conj().T@L
    return np.kron(L.conj(),L)-.5*np.kron(Id,P)-.5*np.kron(P.T,Id)
Dbase=[diss(s) for s in S]
Dpump=[diss(s.conj().T) for s in S]
Ddeph=sum(diss(z) for z in Zs)/4
pair=[Ns[0]@Ns[1]+Ns[0]@Ns[2], Ns[1]@Ns[3]+Ns[2]@Ns[3], Ns[1]@Ns[2], Ns[0]@Ns[3]]
tr=Id.reshape(-1,order='F')
def getA(phi,kappa=1,d=.05,pump=1,coeff=(4,3,1,2)):
    H=sum(c*p for c,p in zip(coeff,pair))
    for i,j,z in [(0,1,1),(0,2,1),(1,3,np.exp(1j*phi)),(2,3,1)]:
        h=S[i].conj().T@S[j]
        H=H-z*h-np.conj(z)*h.conj().T
    L=-1j*(np.kron(Id,H)-np.kron(H.T,Id))+pump*Dpump[0]+kappa*Dbase[3]+d*Ddeph
    A=L.copy(); A[0,:]=tr; rhs=np.zeros(dim*dim,complex);rhs[0]=1
    return A,rhs

def calc(phi,kappa=1,**kw):
    A,b=getA(phi,kappa,**kw); x=solve(A,b);rho=x.reshape((dim,dim),order='F')
    return float((kappa*np.trace(Ns[3]@rho)).real), np.linalg.norm(A@x-b,np.inf), float(np.trace(sum(Ns)@rho).real)
if __name__=='__main__':
    for d in [.05,.2,1.0]:
      for k in [.25,.5,1,2,4,8]:
        vals=[calc(p,k,d=d) for p in [0,np.pi/3,2*np.pi/3,np.pi]]
        print(d,k,[(round(v[0],8),round(v[2],4)) for v in vals],flush=True)
