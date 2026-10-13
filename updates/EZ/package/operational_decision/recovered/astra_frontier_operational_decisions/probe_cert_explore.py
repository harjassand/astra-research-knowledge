from explore_device import *
from itertools import product

def adjoint(phi,kappa=1,**kw):
 A,b=getA(phi,kappa,**kw)
 c=(kappa*Ns[3]).reshape(-1,order='F')
 y=solve(A.conj().T,c)
 q=y.copy();q[0]=0
 X=q.reshape((dim,dim),order='F'); X=(X+X.conj().T)/2
 alpha=y[0].real
 # O - Ldag X = alpha I
 K=[-1j*(a@X-X@a) for a in pair]
 Kd=-(Ddeph.conj().T @ X.reshape(-1,order='F')).reshape((dim,dim),order='F')
 Kk=Ns[3]-(Dbase[3].conj().T@X.reshape(-1,order='F')).reshape((dim,dim),order='F')
 h=S[1].conj().T@S[3]
 Hp=-1j*np.exp(1j*phi)*h+1j*np.exp(-1j*phi)*h.conj().T
 Kp=-1j*(Hp@X-X@Hp)
 return alpha,X,K,Kd,Kk,Kp
if __name__=='__main__':
 for k in [1,2,4,8]:
  for phi in [np.pi,np.pi/3]:
   alpha,X,K,Kd,Kk,Kp=adjoint(phi,k,d=.01,pump=.4)
   rad=[]
   for signs in product([-1,1],repeat=4):
    eig=np.linalg.eigvalsh(sum(s*.01*M for s,M in zip(signs,K)))
    rad+=[max(abs(eig))]
   print(k,phi,'value',alpha,'Uunc',max(rad),'Xnorm',np.linalg.norm(X,2),'phase',np.linalg.norm(Kp,2),'drain',np.linalg.norm(Kk,2),'noise',np.linalg.norm(Kd,2),flush=True)
 print('free check',calc(np.pi/3,4,d=.01,pump=.4,coeff=(0,0,0,0)))
 print('int check',calc(np.pi/3,4,d=.01,pump=.4))
