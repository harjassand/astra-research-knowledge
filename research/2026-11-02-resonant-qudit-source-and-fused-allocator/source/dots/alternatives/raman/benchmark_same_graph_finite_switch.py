import numpy as np
from scipy.linalg import expm
import json

def model(w,eta,s,drift=0.005,gamma=1e-6,off=1e-5,timing=0.002,impurity=1e-5,switch_time=0.01,ramp_steps=4):
 D=1/eta;nb=2*w;d=2*nb;A=np.diag(np.full(w-1,D))+np.diag(np.ones(w-2),1)+np.diag(np.ones(w-2),-1);Ai=np.linalg.inv(A);J=abs(-Ai[-1,0]);shift=Ai[0,0];h=np.sqrt(J)/2
 H=np.zeros((d,d),complex);end=[];dump=[]
 for c in range(2):
  o=c*nb
  for j in range(1,w):H[o+j,o+j]=D
  H[o,o]=H[o+w,o+w]=shift
  for j in range(w):H[o+j,o+j+1]=H[o+j+1,o+j]=(1+drift)*(s if j==w-1 else 1)
  H[o,o+w]=H[o+w,o]=(-1)**c*J*(1+drift)
  L=np.zeros((d,d));L[(1-c)*nb,o+w]=np.sqrt(J);end.append(L)
  for j in range(1,w):
   q=o+w+j;H[q,q]=D;H[q,o+j]=H[o+j,q]=h*(1+drift)
   L=np.zeros((d,d));L[o+j-1,q]=1;dump.append(L)
 I=np.eye(d);vecI=I.reshape(-1,order='F');noise=gamma*(np.outer(vecI,vecI)/d-np.eye(d*d))
 def generator(H,Ls):
  K=-1j*(np.kron(I,H)-np.kron(H.T,I))+noise
  for L in list(Ls)+[np.sqrt(impurity)*L.conj().T for L in Ls]:
   B=L.conj().T@L;K+=np.kron(L.conj(),L)-.5*np.kron(I,B)-.5*np.kron(B.T,I)
  return K
 def basis(c):
  rho=np.zeros((d,d));rho[c*nb,c*nb]=1;return rho.reshape(-1,order='F')
 def wrong(v):
  rho=v.reshape((d,d),order='F');return float(sum(rho[j,j].real for j in range(d) if (-1)**(j//nb)!=s))
 K=generator(H,end+dump)
 offjumps=[np.sqrt(off)*L for L in end+dump]
 gates=[]
 for j in range(w):
  HH=np.zeros((d,d),complex)
  for c in range(2):
   o=c*nb;HH[o+j,o+j+1]=HH[o+j+1,o+j]=(1+drift)*(s if j==w-1 else 1)
  gates.append((generator(HH+off*H,offjumps),np.pi/4 if j==0 else np.pi/2))
 # e phase +i, bounded onsite tuning Delta (without fractional drift here)
 HH=np.zeros((d,d),complex)
 for c in range(2):HH[c*nb+w,c*nb+w]=-D*(1+drift)
 gates.append((generator(HH+off*H,offjumps),np.pi/(2*D)))
 HH=np.zeros((d,d),complex)
 for c in range(2):
  o=c*nb;HH[o,o+w]=HH[o+w,o]=(-1)**c*J*(1+drift)
 gates.append((generator(HH+off*H,offjumps),np.pi/(4*J)))
 gates=[(KK,t*(1+timing)) for KK,t in gates]
 resetK=generator(off*H,end+dump)
 ramped=[];prev=resetK
 for KK,t in gates:
  for step in range(ramp_steps):
   q=(step+.5)/ramp_steps;ramped.append(((1-q)*prev+q*KK,switch_time*(1+timing)/ramp_steps))
  ramped.append((KK,t));prev=KK
 for step in range(ramp_steps):
  q=(step+.5)/ramp_steps;ramped.append(((1-q)*prev+q*resetK,switch_time*(1+timing)/ramp_steps))
 gates=ramped;tg=sum(t for _,t in gates)
 out=[]
 for init in [0,1]:
  v=basis(init)
  for KK,t in gates:v=expm(KK*t)@v
  for R in [2,4,6]:
   T=tg+R/J;active=expm(resetK*(R/J))@v;passive=expm(K*T)@basis(init)
   out.append(dict(eta=eta,syndrome=s,initial_cache=init,gamma_over_g=gamma,drift=drift,off_ratio=off,clock_fractional_bias=timing,reservoir_up_down_ratio=impurity,switch_time_g=switch_time,ramp_steps=ramp_steps,J=J,total_time_g=T,total_time_J=T*J,active_wrong=wrong(active),autonomous_wrong_same_time=wrong(passive)))
 return out
if __name__=='__main__':
 for eta in [.1,.2]:
  for s in [1,-1]:
   for x in model(4,eta,s):print(json.dumps(x),flush=True)
