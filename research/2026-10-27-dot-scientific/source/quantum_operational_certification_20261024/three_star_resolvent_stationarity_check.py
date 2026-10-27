import numpy as np
from scipy.integrate import quad
from three_star_full_balancing_targeted import value
p=1/6;d=p/3;x=np.array([49/60,1/120,1/120]);b=x/3;c=np.array([3/40,1/560,1/560])
def integrand(s):
 u=d-c*c/(3*(b+s));return -3*np.log1p((u-d)/(d+3*s)).sum()-np.log1p((u.sum()-3*d)/(3*d+s))+2*sum(np.log1p((u[i]+u[j]-2*d)/(2*d+2*s)) for i,j in [(0,1),(0,2),(1,2)])
z=quad(integrand,0,np.inf,epsabs=1e-12,epsrel=1e-10)[0]
print('value',value(p,x,c),'resolvent',z);assert abs(value(p,x,c)-z)<1e-12
for i in range(3):
 def grad(s):
  u=d-c*c/(3*(b+s));return 2*c[i]/(b[i]+s)*(1/(u[i]+3*s)+1/(3*(u.sum()+s))-sum(2/(3*(u[i]+u[j]+2*s)) for j in range(3) if j!=i))
 gi=quad(grad,0,np.inf,epsabs=1e-10)[0];e=np.eye(3)[i]*1e-6;num=(value(p,x,c+e)-value(p,x,c-e))/2e-6
 print(i,gi,num);assert abs(gi-num)<1e-7
# Homogeneous d,b derivatives (trace not held fixed) are load-bearing.
def homogeneous(d,b,c):
 pp=3*d;xx=3*b
 return value(pp,xx,c)+(1-(pp+xx.sum()))*np.log(3)
def Gi(s,i):
 u=d-c*c/(3*(b+s));return -3/(u[i]+3*s)-1/(u.sum()+s)+sum(2/(u[i]+u[j]+2*s) for j in range(3) if i!=j)
gd=sum(quad(lambda s:Gi(s,i),0,np.inf,epsabs=1e-10)[0] for i in range(3))
h=1e-6;nd=(homogeneous(d+h,b,c)-homogeneous(d-h,b,c))/(2*h)
print('d derivative',gd,nd);assert abs(gd-nd)<1e-7
for i in range(3):
 gb=c[i]**2/3*quad(lambda s:Gi(s,i)/(b[i]+s)**2,0,np.inf,epsabs=1e-9)[0]
 e=np.eye(3)[i]*h;nb=(homogeneous(d,b+e,c)-homogeneous(d,b-e,c))/(2*h)
 print('b derivative',i,gb,nb);assert abs(gb-nb)<1e-7
