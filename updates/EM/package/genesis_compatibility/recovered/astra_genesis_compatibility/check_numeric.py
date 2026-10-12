"""Independent dense-grid recomputation. Floating quadrature is NOT a proof."""
import numpy as np, json
from pathlib import Path
ROOT=Path(__file__).parent

def evaluate(data,N):
 A=np.array(data['A']);C=np.array(data['coefficients']); k=np.array(data['modes']);
 Etotal=Dtotal=0.;rmin=smin=float('inf');Ftotal=0
 for start in range(0,N,32):
  X=(2*np.pi/N*np.arange(start,min(start+32,N)))[:,None]
  Y=(2*np.pi/N*np.arange(N))[None,:]
  phase=k[:,0,None,None]*X+k[:,1,None,None]*Y
  sn,cs=np.sin(phase),np.cos(phase)
  Dx=[];DD=[]
  for i in range(2):
   Dx.append(np.einsum('amq,mqxy->axy',C,np.stack([k[:,i,None,None]*cs,-k[:,i,None,None]*sn],axis=1)))
   for j in range(i,2):
    DD.append(np.einsum('amq,mqxy->axy',C,np.stack([-k[:,i,None,None]*k[:,j,None,None]*sn,-k[:,i,None,None]*k[:,j,None,None]*cs],axis=1)))
  aa,bb,cc,dd=Dx[0][0]+A[0,0],Dx[1][0]+A[0,1],Dx[0][1]+A[1,0],Dx[1][1]+A[1,1]
  z=(aa+dd+1j*(cc-bb))/2;w=(aa-dd+1j*(cc+bb))/2
  r=np.abs(z);s=np.abs(w);R=r+s
  H1,H2,H3=DD
  zx=(H1[0]+H2[1]+1j*(H1[1]-H2[0]))/2
  zy=(H2[0]+H3[1]+1j*(H2[1]-H3[0]))/2
  wx=(H1[0]-H2[1]+1j*(H1[1]+H2[0]))/2
  wy=(H2[0]-H3[1]+1j*(H2[1]+H3[0]))/2
  E=0.;D=0.
  for dz,dw in [(zx,wx),(zy,wy)]:
   dz=dz*np.conj(z)/r;dw=dw*np.conj(w)/np.maximum(s,1e-100)
   E+=-12*(r-s)*R*dz.real**2-4*(r-2*s)*R**2/r*dz.imag**2+12*R*(r+3*s)*dw.real**2+12*R**2*dw.imag**2+48*s*R*dz.real*dw.real
   D+=R**2*(np.abs(dz)**2+np.abs(dw)**2)
  Etotal+=E.sum();Dtotal+=D.sum();Ftotal+=((3*s-r)*R**3).sum()
  rmin=min(rmin,float(r.min()));smin=min(smin,float(s.min()))
 return dict(N=N,E=Etotal/N**2,D=Dtotal/N**2,ratio=Etotal/Dtotal,min_r=rmin,min_s=smin,F=Ftotal/N**2)

if __name__=='__main__':
 data=json.loads((ROOT/'heat_threewave_search.json').read_text())
 out=[evaluate(data,N) for N in [64,128,256,512]]
 for row in out: print(row,flush=True)
 (ROOT/'numerical_recheck.json').write_text(json.dumps({'status':'UNCERTIFIED_FLOATING_QUADRATURE','rows':out},indent=2))
