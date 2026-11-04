import numpy as np,math,json
from scipy.sparse import csr_matrix,kron as skron,eye as seye
from scipy.sparse.linalg import expm_multiply
from linear_loss_receiver_check import I,X,Z,sm,kron

def build(eta=.01,kappa=20,N=6,mu=.005,s=.2,Gamma=.1,Delta=1):
 T=np.pi;gamma=mu/T;G=np.sqrt(gamma*kappa)/2;d=8*N
 ac=np.diag(np.sqrt(np.arange(1,N)),1).astype(complex)
 ad=kron(I,I,ac,I);rd=kron(I,I,np.eye(N),sm)
 C=np.sqrt(eta*kappa)*ad;R=-1j*np.sqrt(Gamma)*rd;loss=np.sqrt((1-eta)*kappa)*ad
 H=kron(I,X,np.eye(N),I)/2+G*kron(I,Z,ac+ac.conj().T,I)+Delta*kron(I,I,np.eye(N),Z)/2+(R.conj().T@C-C.conj().T@R)/(2j)
 def spre(A):return skron(seye(d,format='csr'),csr_matrix(A),format='csr')
 def spost(A):return skron(csr_matrix(A.T),seye(d,format='csr'),format='csr')
 def dis(A):
  Q=A.conj().T@A
  return skron(csr_matrix(A.conj()),csr_matrix(A),format='csr')-(spre(Q)+spost(Q))/2
 L=-1j*(spre(H)-spost(H))+dis(C+R)+dis(loss);L.eliminate_zeros()
 plus=np.array([1,1])/np.sqrt(2);minus=np.array([1,-1])/np.sqrt(2)
 z=np.array([1,0]);o=np.array([0,1]);vac=np.eye(N)[0]
 psi=(kron(z,plus,vac,z)+kron(o,minus,vac,z))/np.sqrt(2)
 rho=np.outer(psi,psi.conj())
 v=np.sqrt(eta*gamma*4/Gamma)*(1-np.exp(-Gamma*T/2))
 F=kron(np.diag([1,np.sqrt(s)]),I,np.eye(N),np.diag([np.sqrt(s)*v,1]))
 # Rigorous algebraic upper bound using ||H||<=1+2Gsqrt(N-1)+sqrt(eta*kappa*Gamma*(N-1))
 # ||C+R||<=sqrt(eta*kappa*(N-1))+sqrt(Gamma)
 Lam=2*(1+2*G*np.sqrt(N-1)+np.sqrt(eta*kappa*Gamma*(N-1)))+2*(np.sqrt(eta*kappa*(N-1))+np.sqrt(Gamma))**2+2*(1-eta)*kappa*(N-1)
 return L,rho.reshape(-1,order='F'),F,Lam,dict(eta=eta,kappa=kappa,N=N,mu=mu,s=s,Gamma=Gamma,Delta=Delta,T=T,G=G,v=v)

def report(y,F,z):
 N=z['N'];d=8*N;A=y.reshape(d,d,order='F');A=F@A@F.conj().T
 ar=np.trace(A.reshape(2,2,N,2,2,2,N,2),axis1=2,axis2=6)
 ar=np.trace(ar,axis1=1,axis2=4).reshape(4,4)
 p=np.trace(ar).real
 f=(ar[0,0].real+ar[3,3].real+2*abs(ar[0,3]))/(2*p)
 cutoff=2*z['G']*z['T']*np.sqrt(N)*(z['mu']/(z['T']*z['kappa']))**((N-1)/2)/np.sqrt(math.factorial(N-1))
 return dict(success=p,fidelity=f,phase=float(np.angle(ar[0,3])),cutoff_diamond=cutoff,success_over_eta=p/z['eta'])

def scaled_taylor(L,y,T,Lam,n=4096,m=16):
 h=T/n;A=(h*L).tocsr()
 # Use real-plus-imaginary absolute sums, avoiding any assumption about a hypot library.
 u=2**-53
 B0=float(np.max(np.asarray((abs(A.real)+abs(A.imag)).sum(axis=0)).ravel()))
 B=float(np.nextafter(B0*(1+8192*u),math.inf))
 Lam=float(math.ceil(Lam))
 def cnorm(x):return float(np.sum(np.abs(x.real)+np.abs(x.imag)))
 # Every complex multiply/add uses <=8 real operations; sparse rows have bounded length.
 maxrow=int(np.diff(A.indptr).max());u=2**-53
 # gamma-factor dominates roundoff of a sparse complex matvec, scalar division and sum.
 ops=16*maxrow+32;gu=ops*u/(1-ops*u)
 # Local roundoff l1-vector bound, accrued in trace norm (entrywise l1 dominates trace norm).
 # Counts actual stage l1 norms; uses nonnegative outward cushions.
 round_total=0.0
 for step in range(n):
  term=y.copy();out=y.copy();local=0.0
  # Each local numerical recurrence error remains magnified by <=exp(B) in the polynomial.
  for k in range(1,m+1):
   prevnorm=cnorm(term)
   term=(A@term)/k
   local+=gu*(B/k)*prevnorm
   out=out+term
   local+=8*u*(cnorm(out)+cnorm(term))
  round_total+=local*math.exp(B)
  y=out
 h_upper=float(np.nextafter(h,math.inf))
 rem=math.exp(h_upper*Lam)*(h_upper*Lam)**(m+1)/math.factorial(m+1)
 trunc=(math.expm1(n*math.log1p(rem)))
 # Exact generator coefficient errors are separately covered by a deliberately loose allowance.
 return y,dict(n=n,m=m,induced_l1_step=B,Lambda=Lam,maxrow=maxrow,taylor_remainder_trace=trunc,roundoff_trace_bound=round_total)

if __name__=='__main__':
 for Gam in [.1,.2,.3,.5]:
  L,y,F,Lam,z=build(Gamma=Gam)
  out=report(expm_multiply(z['T']*L,y),F,z)
  print(json.dumps(dict(parameters=z,observed=out)),flush=True)
 L,y,F,Lam,z=build(Gamma=.2)
 y,cert=scaled_taylor(L,y,z['T'],Lam)
 print(json.dumps(dict(parameters=z,certified_taylor_arithmetic=cert,result=report(y,F,z))),flush=True)
