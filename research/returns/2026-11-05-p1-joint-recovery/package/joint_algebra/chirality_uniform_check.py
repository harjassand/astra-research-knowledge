from pathlib import Path
ROOT=Path(__file__).resolve().parent
import numpy as np,math,json
from singlet_singular import schur,gateU
from yangian_weak import local
p=[np.array([[0,1],[1,0]]),np.array([[0,-1j],[1j,0]]),np.diag([1,-1])]
for n in range(3,7):
 d=2**n;site=[[local(n,j,a) for a in range(1,4)] for j in range(n)];J=[sum(site[j][a] for j in range(n)) for a in range(3)];J2=sum(a@a for a in J)
 Y=[sum(site[i][b]@site[j][c]-site[i][c]@site[j][b] for i in range(n) for j in range(i+1,n)) for a,b,c in [(0,1,2),(1,2,0),(2,0,1)]];C=sum(j@y for j,y in zip(J,Y));ee,V=np.linalg.eigh(J2);Ji=(V*np.where(ee>1e-8,1/np.maximum(ee,1e-8),0))@V.conj().T;Ypar=[j@Ji@C for j in J];K=np.trace(C@C@Ji).real/d
 Ps=[np.kron(W@W.T,np.eye(2)) for ws in schur(n-1).values() for W in ws];PPs=[np.kron(np.eye(2),P) for P in Ps]
 kernel=max(np.linalg.norm(sum(P@y@P for P in Ps)) for y in Ypar)
 F=np.kron(p[0],Ypar[1])-np.kron(p[1],Ypar[0]);Fn=np.trace(F@F).real/(2*d)
 for th in [.03,.1,.3,.7]:
  c=np.cos(th);s=np.sin(th);U=gateU(n,th);W=U@np.kron(p[2],np.eye(d))@U.conj().T;w=W.reshape(2,d,2,d);B=(w[0,:,0,:]+w[1,:,1,:])/2;WQ=W-np.kron(np.eye(2),B);after=sum(P@WQ@P for P in PPs)
  loss=(np.linalg.norm(WQ)**2-np.linalg.norm(after)**2)/(2*d)
  tail=sum(math.comb(n,k)*c**(4*n-2*k)*2**k*s**(2*k) for k in range(4,n+1,2))
  bound=max(c**(2*n-2)*s*s*math.sqrt(n*(n-1)*(n-2)/(6*(5*n-12)))-math.sqrt(tail),0)**2
  overlap=np.trace(F@WQ).real/(2*d*Fn)
  contam=abs(overlap+.5*c**(2*n-2)*s*s)*math.sqrt(Fn)
  print(json.dumps(dict(n=n,theta=th,kernel_residual=float(kernel),K=float(K),loss=float(loss),bound=float(bound),slack=float(loss-bound),contamination=float(contam),tail_norm=float(math.sqrt(tail)))),flush=True)
a=.1;dd=math.exp(-2*a)*(a/math.sqrt(30)-math.sqrt(math.cosh(2*a)-1-2*a*a))**2
print(json.dumps(dict(alpha=a,limiting_loss=dd,limiting_halfdiamond_floor=.75*(1-math.sqrt(1-dd)))),flush=True)
