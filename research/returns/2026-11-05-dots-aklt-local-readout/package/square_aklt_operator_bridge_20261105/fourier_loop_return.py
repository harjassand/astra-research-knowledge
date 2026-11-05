"""Finite-memory closed-trail return majorant via torus Fourier resolvents.
This is a feasibility screen. Periodic aliases only add nonnegative walks,
so an exact finite-torus value is an upper bound, not quadrature estimation.
Numerical solve certification is reported separately.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
import sys,numpy as np,math,time,json,argparse
from scipy.sparse import coo_matrix,eye
from scipy.sparse.linalg import gmres,splu
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'square_aklt_loop_audit_20261105'))
from weighted_trail_bound import build,D,edge

def setup(m):
 ds,to,ww=build(m);N=len(ds);rows=[];cols=[];weights=[];deltas=[]
 for i,hist in enumerate(ds):
  ps=[(0,0)]
  for d in hist:ps.append((ps[-1][0]+D[d][0],ps[-1][1]+D[d][1]))
  used={edge(ps[k],ps[k+1])for k in range(m)};z=0
  for k,(dx,dy) in enumerate(D):
   p=(ps[-1][0]+dx,ps[-1][1]+dy)
   if edge(ps[-1],p)in used:continue
   assert ww[i,z]>0
   for o in range(4):
    rows.append(((o+hist[1])%4)*N+int(to[i,z]));cols.append(o*N+i);weights.append(ww[i,z]/5);deltas.append(D[(k+o)%4])
   z+=1
 pos=[];pw=[]
 for hist in ds:
  p=(0,0);seen={p};w=1.
  for k in hist:
   p=(p[0]+D[k][0],p[1]+D[k][1])
   if p in seen and p!=(0,0):w*=.6
   seen.add(p)
  pos.append(p);pw.append(w)
 return ds,np.array(rows),np.array(cols),np.array(weights),np.array(deltas),np.array(pos),np.array(pw)

def run(m,L,tol):
 ds,rows,cols,w,delta,pos,pw=setup(m);N=len(ds);n=4*N;I=eye(n,dtype=complex,format='csr');vals=[];errs=[];start=time.monotonic();x=1/3
 cert=np.load(Path(__file__).resolve().parents[1]/f'square_aklt_loop_audit_20261105/trail_certificate_m{m}.npz');v=np.tile(cert['v'].astype(float),4);v/=v.min();alpha=float(cert['alpha_num']/cert['alpha_den']);gap=1-x*alpha
 # Reflection in either coordinate pairs equal real return contributions.
 for ix in range(L//2+1):
  kx=2*np.pi*ix/L;multx=1 if ix in (0,L//2) else 2
  for iy in range(L//2+1):
   ky=2*np.pi*iy/L;multy=1 if iy in (0,L//2) else 2;k=np.array([kx,ky])
   T=coo_matrix((w*np.exp(1j*(delta@k)),(rows,cols)),shape=(n,n)).tocsr();A=I-x*T
   b=np.zeros(n,complex);b[:N]=pw*np.exp(1j*(pos@k))
   y,info=gmres(A,b,rtol=tol,atol=0,restart=100,maxiter=1000);assert info==0,info
   z,info=gmres(A,y,rtol=tol,atol=0,restart=100,maxiter=1000);assert info==0,info
   r1=b-A@y;r2=y-A@z;e1=np.dot(v,abs(r1))/gap;e2=(np.dot(v,abs(r2))+e1)/gap
   # v.min=1 so this l1-v bound controls sum of component errors.
   err=(m-1)*e1+e2;val=(m-1)*y.sum()+z.sum();mult=multx*multy
   vals.append(mult*val.real);errs.append(mult*err)
  print('row',ix,'of',L//2,'elapsed',time.monotonic()-start,flush=True)
 total=6*x**m*sum(vals)/(L*L);solve_error=6*x**m*sum(errs)/(L*L)
 # Exact physical lengths below m must be supplied, not lost at initialization.
 counts={4:2,6:6,8:188/5,10:188,12:27096/25}
 short=6*sum(k*c*x**k for k,c in counts.items()if k<m)
 return dict(memory=m,torus_side=L,states=n,alpha=alpha,solver_tolerance=tol,return_moment_at_and_above_memory=total,short_exact_moment=short,total_majorant_screen=total+short,residual_based_error_screen=solve_error,half_moment_screen=(total+short)/2,elapsed_seconds=time.monotonic()-start,notes='Floating feasibility screen; residual bounds omit floating assembly/roundoff and need interval padding before certification. Periodic image returns are positive extra terms.')
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--memory',type=int,default=6);ap.add_argument('--side',type=int,default=16);ap.add_argument('--tol',type=float,default=1e-10);a=ap.parse_args();z=run(a.memory,a.side,a.tol);print(json.dumps(z,indent=2));Path(__file__).with_name(f'fourier_m{a.memory}_L{a.side}.json').write_text(json.dumps(z,indent=2)+'\n')
