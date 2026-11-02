import numpy as np
from scipy.linalg import expm
from scipy.integrate import quad
import json
rng=np.random.default_rng(20261102)
K=4;t=1.;eta=.05;g=eta*t/K;beta=80.;D=1
A=t*(2*np.eye(K-1)-np.eye(K-1,k=1)-np.eye(K-1,k=-1));v=np.zeros(K-1);v[0]=v[-1]=1
x=D*eta**2;a0=64*x/K;b=32*x*t/K**2
rho=lambda l:g*g*(v@expm(-A*l)@v)
rhow=lambda l:2*g*g*expm(-A*l)[0,-1]
J=quad(rhow,0,beta)[0];R=quad(lambda l:rhow(l)*np.expm1(a0+b*l),0,beta)[0]
E=np.exp(a0)*quad(lambda l:l*rho(l)*np.exp(b*l),0,beta)[0]
def H(s):
 h=np.zeros((K,K));h[1:,1:]=A;h[0,1]=h[1,0]=-g;h[0,-1]=h[-1,0]=-g*s;return h
Zplus=np.trace(expm(-beta*H(1)))
results=[]
for j in range(20):
 n=int(rng.integers(1,8)); ds=rng.dirichlet(np.ones(n))*beta;ss=rng.choice([-1,1],n);P=np.eye(K)
 for dt,s in zip(ds,ss):P=expm(-dt*H(s))@P
 Z=np.trace(P);L=float(np.sum(ds[ss<0]));Nj=int(np.sum(ss!=np.roll(ss,1)));res=abs(np.log(Z/Zplus)+2*J*L);bound=2*R*L+2*E*Nj
 results.append(dict(n=n,negative_time=L,jumps=Nj,Z=float(Z),residual=float(res),bound=float(bound),pass_bound=bool(res<=bound+1e-12)))
out=dict(K=K,t=t,eta=eta,beta=beta,a0=a0,b=b,Jbeta=J,R=R,E=E,all_pass=all(r['pass_bound'] for r in results),tests=results)
print(json.dumps(out,indent=2))
