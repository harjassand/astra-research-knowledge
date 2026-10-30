import sys
sys.dont_write_bytecode=True
import numpy as np
from triad_core import *
F,A,B,C,D,E=S.symbols('F A B C D E',real=True)
rs=[conformal((F,A),(1,0)),conformal((B,C),(0,1)),conformal((D+E,-D+E),(1,1))]
N=moments([r[0] for r in rs],[r[1] for r in rs]);fn=S.lambdify((F,A,B,C,D,E),N,'numpy')
rng=np.random.default_rng(27);n=16;x,y=np.meshgrid(np.arange(n)*2*np.pi/n,np.arange(n)*2*np.pi/n,indexing='ij')
def energy(Z):
 xx,yy,uu,vv=Z;r=xx*xx+yy*yy;t=uu*uu+vv*vv
 return t*t+2*r*t+xx*(uu*uu-vv*vv)+2*yy*uu*vv+3*(r+t)/16
for _ in range(8):
 pars=rng.normal(size=6);ph=rng.normal(size=3);mean=rng.normal(size=4);waves=[x+ph[0],y+ph[1],x+y+ph[2]]
 rr=[conformal((pars[0],pars[1]),(1,0)),conformal((pars[2],pars[3]),(0,1)),conformal((pars[4]+pars[5],-pars[4]+pars[5]),(1,1))]
 G=sum(np.array(list(z)+list(w),float)[:,None,None]*np.cos(theta) for (z,w),theta in zip(rr,waves))
 mat=np.array(fn(*pars),float);h=np.cos(ph[0]+ph[1]-ph[2]);mat[:4,4]*=h;mat[4,:4]*=h;mat[4,5]*=h;mat[5,4]*=h
 vector=np.r_[mean,1.,1.];expected=vector@mat@vector/2
 actual=np.mean(energy(mean[:,None,None]+G))-energy(mean)
 assert abs(actual-expected)<1e-10*(1+abs(actual)),(actual,expected)
print('PASS: eight actual compatible trigonometric fields, arbitrary phases and nonzero means, match the reconstructed exact moments.')
