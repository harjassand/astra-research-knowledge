import numpy as np
from pathlib import Path
p=Path(__file__).parent
for fn in [p/'cubic_search_m3_s0_best.npz',p/'cubic_search_m7_s10_best.npz',p/'cubic_fe_N12_s0_best.npz']:
 z=np.load(fn)
 if 'coeff' in z:
  m=int(z['m']);N=4*m+1;C=z['coeff'];ell=float(z['ell']);modes=z['modes'];x,y=np.meshgrid(np.arange(N)*2*np.pi/N,np.arange(N)*2*np.pi/N,indexing='ij');D=[]
  for k,l in modes:
   for h in [-np.sin(k*x+l*y),np.cos(k*x+l*y)]:D.append(np.array([k*np.exp(ell)*h,l*np.exp(-ell)*h])/np.hypot(k,l))
  V=np.einsum('oi,ijxy->ojxy',C,np.array(D)).reshape(4,-1)
 else:
  f=z['phi'];N=int(z['N']);ell=float(z['ell']);ux=np.roll(f,-1,1);uy=np.roll(f,-1,2);uxy=np.roll(ux,-1,2)
  V=np.stack([np.stack([ux-f,uxy-ux],axis=1),np.stack([uxy-uy,uy-f],axis=1)],axis=2)
  V=V*np.array([np.exp(ell),np.exp(-ell)]).reshape(1,2,1,1,1)*N;V=V.reshape(4,-1)
 a,b,c,d=V
 u=a*a+c*c;j=a*d-b*c;qq=2*a+d
 A=(((a-d)**2+(b+c)**2)**2/8+j*j+u*j).mean();Q=(qq*qq+c*c).mean();C=(u*(a+d)+2*j*qq).mean()
 sb=-C/(2*Q);VV=V/sb;a,b,c,d=VV;qq=2*a+d
 print(fn.name,'rho',C*C/(4*A*Q),'opt background',sb)
 print('V rms',np.sqrt((VV*VV).mean(1)),'q,c parts',np.mean(qq**2),np.mean(c*c),'jmean',np.mean(a*d-b*c))
 print('moments normalized',np.cov(VV,bias=True))
 print('range',VV.min(axis=1),VV.max(axis=1))
