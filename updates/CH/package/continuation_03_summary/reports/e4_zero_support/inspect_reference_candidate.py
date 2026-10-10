import math,numpy as np,json
from gaussian_reference_probe import gibbs

def data(eta,u,w,t,sa):
 ch=(1+t*t)/(1-t*t);sh=2*t/(1-t*t)
 r=u*ch*ch+w*sh*sh;a=w*ch*ch+u*sh*sh;c=(u+w)*ch*sh
 v=1.5;ce=math.sqrt(2);se=math.sqrt(eta);sl=math.sqrt(1-eta)
 Qb=np.array([[r,se*c*sa],[se*c*sa,eta*a*sa*sa+(1-eta)*v]])
 Pb=np.array([[r,-se*c/sa],[-se*c/sa,eta*a/sa/sa+(1-eta)*v]])
 Qe=np.array([[r,-sl*c*sa,0],[-sl*c*sa,(1-eta)*a*sa*sa+eta*v,se*ce],[0,se*ce,v]])
 Pe=np.array([[r,sl*c/sa,0],[sl*c/sa,(1-eta)*a/sa/sa+eta*v,-se*ce],[0,-se*ce,v]])
 Gb=gibbs(np.block([[Qb,np.zeros((2,2))],[np.zeros((2,2)),Pb]]))
 Ge=gibbs(np.block([[Qe,np.zeros((3,3))],[np.zeros((3,3)),Pe]]))
 Tb=np.diag([1.,se]);Te=np.array([[1.,0],[0,-sl],[0,0.]])
 Dq=Te.T@Ge[:3,:3]@Te-Tb.T@Gb[:2,:2]@Tb
 Dp=Te.T@Ge[3:,3:]@Te-Tb.T@Gb[2:,2:]@Tb
 out={}
 for name,Q,P,D in [('q',Qe,Pe,Dq),('p',Pe,Qe,Dp)]:
  vals,vecs=np.linalg.eigh(D)
  out[name]={'gap':D.tolist(),'eig':vals.tolist(),'score':vecs[:,0].tolist(),'environment_symplectic_eigenvalues':np.sqrt(np.linalg.eigvals(Q@P).real).tolist()}
 out['B_symplectic']=np.sqrt(np.linalg.eigvals(Qb@Pb).real).tolist()
 return out
if __name__=='__main__':
 print(json.dumps(data(5433561/7123561,1,1000,.005,10),indent=2))
 print(json.dumps(data(.761,2,1000,.015,10),indent=2))
