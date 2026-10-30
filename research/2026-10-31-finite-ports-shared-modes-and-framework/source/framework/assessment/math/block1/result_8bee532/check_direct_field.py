"""Independent direct trigonometric energy check of the moment convention."""
import numpy as np
import sympy as s
x,y,u,v=s.symbols('x y u v',real=True); vs=[x,y,u,v];r=x*x+y*y;t=u*u+v*v
F=t*t+2*r*t;C=x*(u*u-v*v)+2*y*u*v;Q=s.Rational(3,16)*(r+t);P=F+C+Q
pf=s.lambdify(vs,P,'numpy');ff=s.lambdify(vs,F,'numpy');cf=s.lambdify(vs,C,'numpy');qf=s.lambdify(vs,Q,'numpy')
hf=s.lambdify(vs,s.hessian(F,vs),'numpy');dF=s.lambdify(vs,[s.diff(F,j) for j in vs],'numpy');dC=s.lambdify(vs,[s.diff(C,j) for j in vs],'numpy')
p=-0.25;e=1.2;amp=np.array([.7,-.23,1.1]);ph=np.array([.3,-1.2,.6]);freq=[1, p+1j*e,p+1+1j*e]
R=[]
for k in freq:
 z=1j*np.conj(k)**4;w=1j*k*np.conj(k)**3;R.append(np.array([z.real,z.imag,w.real,w.imag]))
R=np.array(R)
angles=np.arange(32)*2*np.pi/32;xx,yy=np.meshgrid(angles,angles,indexing='ij');cos=np.array([np.cos(xx+ph[0]),np.cos(yy+ph[1]),np.cos(xx+yy+ph[2])])
G=np.einsum('j,ja,jxy->axy',amp,R,cos)
H=np.array([[np.mean(s.lambdify(vs,s.diff(F,vi,vj),'numpy')(*G)) for vj in vs] for vi in vs])
# H,w,q depend only on the individual wave second moments.
H2=sum(amp[j]**2*np.array(hf(*R[j]))/2 for j in range(3));w2=sum(amp[j]**2*np.array(dC(*R[j]))/2 for j in range(3));q2=sum(amp[j]**2*qf(*R[j])/2 for j in range(3))
vect=np.mean(np.array(dF(*G)),axis=(1,2));ww=np.mean(np.array(dC(*G)),axis=(1,2));f=np.mean(ff(*G));c=np.mean(cf(*G));q=np.mean(qf(*G))
assert np.max(abs(H-H2))<1e-10 and np.max(abs(ww-w2))<1e-10 and abs(q-q2)<1e-10
M=np.array([.2,-.4,.7,-.3]);rho=-.6
actual=np.mean(pf(*(M[:,None,None]+rho*G)))-pf(*M)
pred=rho*rho*(M@H@M/2+M@(rho*vect+ww)+rho*rho*f+rho*c+q)
assert abs(actual-pred)<1e-9
print('PASS: actual compatible two-phase map, second moments and direct background energy match; gap =',actual)
