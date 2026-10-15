import json,numpy as np,sympy as s
from pathlib import Path
ROOT=Path(__file__).resolve().parent
A=s.symbols('a b c d'); a,b,c,d=A
u=a*a+c*c;v=b*b+d*d;q=a*d-b*c
F=3*(u+v-2*q)**2+s.Rational(35,24)*u*u+q*q-s.Rational(5,2)*q*u
FUN=s.lambdify(A,[F]+[s.diff(F,x) for x in A[:2]]+[s.diff(F,A[i],A[j]) for i in range(2) for j in range(4)],'numpy',cse=True)
def fields(rec,N=128):
 grid=np.arange(N)*2*np.pi/N;xx,yy=np.meshgrid(grid,grid,indexing='ij');
 rr=[np.ones_like(xx)]+[np.zeros_like(xx) for _ in range(5)]
 inds=[(0,0),(1,0),(0,1),(2,0),(1,1),(0,2)]
 for mode,pair in zip(rec['modes'],np.array(rec['rho_coefficients']).reshape(-1,2)):
  i,j=mode;cc,ss=pair;z=i*xx+j*yy
  for h,(dx,dy) in enumerate(inds):
   n=dx+dy;fac=i**dx*j**dy
   val=fac*(cc*np.cos(z+n*np.pi/2)+ss*np.sin(z+n*np.pi/2))
   rr[h]+=val
 kk=[np.zeros_like(xx),np.ones_like(xx)]+[np.zeros_like(xx) for _ in range(3)]
 kinds=[(1,0),(0,1),(2,0),(1,1),(0,2)]
 for i,j,cc,ss in rec['phase']:
  z=i*xx+j*yy
  for h,(dx,dy) in enumerate(kinds):
   n=dx+dy;fac=i**dx*j**dy
   kk[h]+=fac*(cc*np.cos(z+n*np.pi/2)+ss*np.sin(z+n*np.pi/2))
 r,rx,ry,rxx,rxy,ryy=rr;kx,ky,kxx,kxy,kyy=kk
 a=rx/(4*r);b=ry/(4*r)
 out=FUN(a,b,kx,ky);f,ja,jb=out[:3];H=np.array(out[3:]).reshape(2,4,N,N)
 ax=(rxx/r-rx*rx/r**2)/4;bx=(rxy/r-rx*ry/r**2)/4;by=(ryy/r-ry*ry/r**2)/4
 div=H[0,0]*ax+H[0,1]*bx+H[0,2]*kxx+H[0,3]*kxy+H[1,0]*bx+H[1,1]*by+H[1,2]*kxy+H[1,3]*kyy
 g=f-a*ja-b*jb-div/4
 return {'rho_min':float(r.min()),'g_min':float(g.min()),'g_max':float(g.max()),'energy':float(np.mean(r*f)), 'weighted_g':float(np.mean(r*g))}
if __name__=='__main__':
 data=json.loads((ROOT/'density_search.json').read_text())
 for r in data['results']:print(fields(r))
