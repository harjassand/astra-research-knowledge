import numpy as np
beta,p,Ec,Delta=1.,.01,8.,1.
q=lambda E:p+(1-2*p)/(1+np.exp(beta*E))
qh,qc=q(2*Ec+Delta),q(Ec)
a,b=qh*(1-qc)**2,(1-qh)*qc**2
q0=q(Delta); L=20; M=L//2
pi=np.array([(a/b)**(k-M) if k<=M else (q0/(1-q0))**(k-M) for k in range(L+1)]);pi/=pi.sum()
Q=np.eye(L+1)
for k in list(range(L))+list(reversed(range(L))):
 u,v=(a,b) if k<M else (q0,1-q0)
 T=np.eye(L+1);T[k,k]=1-u;T[k,k+1]=u;T[k+1,k]=v;T[k+1,k+1]=1-v
 Q=Q@T
print('equal-rate source a,b,ratio:',a,b,a/b)
print('stationarity maximum residual:',abs(pi@Q-pi).max())
print('minimal one-sweep mass at middle:',Q[:,M].min())
print('boundary probability k=0 or L:',pi[0]+pi[-1])
print('finite-n check only; asymptotic proof in CONSTRUCTIVE_ATTACK.md')
assert a>b
assert abs(pi@Q-pi).max()<1e-14
assert Q[:,M].min()>0
