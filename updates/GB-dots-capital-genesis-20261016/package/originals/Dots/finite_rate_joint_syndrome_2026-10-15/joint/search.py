import os
os.environ['OPENBLAS_NUM_THREADS']='1'
import numpy as np,json,time
from scipy.linalg import expm,block_diag
from pathlib import Path
rng=np.random.default_rng(761207);I=np.eye(2);X=np.array([[0,1],[1,0]],complex);Z=np.diag([1,-1]);R=np.array([[0,1],[0,0]],complex)
def norm(A):return np.linalg.norm(A,2)
def randA():
 A=rng.normal(size=(2,2))+1j*rng.normal(size=(2,2));return A/norm(A)
def randH():
 A=randA();A=A+A.conj().T;return A/norm(A)
def eps(J,g,t):return J*J/g*(t+np.expm1(-2*g*t)/(2*g))
def calc(A,B,HB,J1,J2,g1,g2,t):
 V1=J1*(np.kron(np.kron(R,I),A)+np.kron(np.kron(R.conj().T,I),A.conj().T));V2=J2*(np.kron(np.kron(I,R),B)+np.kron(np.kron(I,R.conj().T),B.conj().T))
 H=HB+V1+V2;n=8;S1=np.kron(np.kron(Z,I),I);S2=np.kron(np.kron(I,Z),I)
 # Adjoint generator, column vectorization.
 L=1j*(np.kron(np.eye(n),H)-np.kron(H.T,np.eye(n)))+g1*(np.kron(S1.T,S1)-np.eye(n*n))+g2*(np.kron(S2.T,S2)-np.eye(n*n))
 M=np.diag([0.]*6+[1.,1.]);F=(expm(L*t)@M.reshape(-1,order='F')).reshape((n,n),order='F')[:2,:2];F=(F+F.conj().T)/2
 p=float(np.linalg.eigvalsh(F)[-1]);bound=eps(J1,g1,t)*eps(J2,g2,t)
 return p,bound,F
best={'ratio':0};results=[];start=time.process_time()
for k in range(1200):
 mode=['bath_only','diagonal_dependent'][k%2]
 J1,J2=10**rng.uniform(-1.5,.15,2);g1,g2=10**rng.uniform(-.5,.5,2);t=10**rng.uniform(-1,.6)
 A=randA();B=randA();scale=10**rng.uniform(-1,1)
 HB=np.kron(np.eye(4),scale*randH()) if mode=='bath_only' else block_diag(*[scale*randH() for _ in range(4)])
 p,b,F=calc(A,B,HB,J1,J2,g1,g2,t);ratio=p/b
 if ratio>best['ratio']:
  best={'ratio':ratio,'p':p,'bound':b,'mode':mode,'J1':J1,'J2':J2,'g1':g1,'g2':g2,'t':t,'iteration':k};np.savez(Path(__file__).with_name('best.npz'),A=A,B=B,HB=HB,**{a:best[a] for a in ['J1','J2','g1','g2','t']});print(best,flush=True)
 if ratio>1.000001:break
results={'best':best,'iterations':k+1,'cpu_seconds':time.process_time()-start};Path(__file__).with_name('search_result.json').write_text(json.dumps(results,indent=2));print(results)
