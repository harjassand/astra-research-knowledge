"""A posteriori interval certificate of finite-torus positive return bounds.
GMRES vectors are arbitrary witnesses. No solver convergence assumption enters
bounds: rectangular interval residuals plus an integer resolvent supersolution
control their error for the exact rational/roots-of-unity operator.
"""
from fourier_loop_return import *
from resolvent_error_weight import get_q
from fractions import Fraction as F
import mpmath as mp
INF=np.inf;EPS=np.finfo(float).eps

def up(x):return np.nextafter(x,INF)
def down(x):return np.nextafter(x,-INF)
def sumup(x):
 # Conservative gamma_n bound for any binary64 summation order, all x>=0.
 a=float(np.sum(x));n=np.size(x);g=(n+2)*EPS
 return float(up(a/(1-g)))
def absum(z):return up(abs(z.real)+abs(z.imag))
def bounds_iv(a):return float(down(float(a.a))),float(up(float(a.b)))
def table(L,coeff):
 out=[];mp.iv.prec=100
 for k in range(L):
  angle=2*mp.iv.pi*k/L;c=mp.iv.mpf(coeff.numerator)/coeff.denominator
  lr,hr=bounds_iv(c*mp.iv.cos(angle));li,hi=bounds_iv(c*mp.iv.sin(angle))
  cr=(lr+hr)/2;ci=(li+hi)/2
  out.append((cr+1j*ci,lr,hr,li,hi))
 return tuple(np.array([r[j] for r in out])for j in range(5))

def mulint(lo,hi,y):
 return down(np.where(y>=0,lo*y,hi*y)),up(np.where(y>=0,hi*y,lo*y))
def residual_bound(y,b_lo,b_hi,coef_intervals,slots,q):
 # b_lo, b_hi are complex rectangular bounds; all binary64 operations below
 # are outward rounded with nextafter after each elementary product/sum.
 rl=down(b_lo.real-y.real);rh=up(b_hi.real-y.real)
 il=down(b_lo.imag-y.imag);ih=up(b_hi.imag-y.imag)
 crl,crh,cil,cih=coef_intervals
 for rows,cols,ids in slots:
  yr=y.real[cols];yi=y.imag[cols]
  al,ah=mulint(crl[ids],crh[ids],yr);bl,bh=mulint(cil[ids],cih[ids],yi)
  pl=down(al-bh);ph=up(ah-bl)
  rl[rows]=down(rl[rows]+pl);rh[rows]=up(rh[rows]+ph)
  al,ah=mulint(crl[ids],crh[ids],yi);bl,bh=mulint(cil[ids],cih[ids],yr)
  pl=down(al+bl);ph=up(ah+bh)
  il[rows]=down(il[rows]+pl);ih[rows]=up(ih[rows]+ph)
 r=up(np.maximum(abs(rl),abs(rh))+np.maximum(abs(il),abs(ih)))
 return sumup(up(q*r))
def eval_linear(y,mask):
 a=y.real[mask];value=float(a.sum());err=(a.size+2)*EPS*sumup(abs(a))
 return value,float(up(err/(1-(a.size+2)*EPS)))

def run_certificate(m,L,tol,x):
 assert L%2==0 and L>2*m
 ds,rows,cols,w,delta,pos,pw=setup(m);N=len(ds);n=4*N;I=eye(n,dtype=complex,format='csr');start=time.monotonic()
 source_good=[];source_r=[];sink_s=np.zeros(n,bool);sink_t=np.zeros(n,bool)
 for i,hist in enumerate(ds):
  ps=[(0,0)];r=0
  for d in hist:
   p=(ps[-1][0]+D[d][0],ps[-1][1]+D[d][1]);r+=int(p in ps and p!=(0,0));ps.append(p)
  source_r.append(r);source_good.append((0,0)not in ps[1:])
  if ps[-1]not in ps[:-1]:
   for o in range(4):
    final=(hist[-1]+o)%4
    sink_s[o*N+i]=final==0;sink_t[o*N+i]=final in (1,3)
 source_r=np.array(source_r);source_good=np.array(source_good)
 # Group incoming edges into slots having at most one update per target row.
 order=np.argsort(rows,kind='stable');groups=[];last=-1;j=0
 for e in order:
  if rows[e]!=last:last=rows[e];j=0
  if len(groups)<=j:groups.append([])
  groups[j].append(e);j+=1
 slots=[]
 for g in groups:
  ids=np.array(g);slots.append((rows[ids],cols[ids],ids))
 qbase=get_q(m);cert=np.load(Path(__file__).with_name(f'residual_supersolution_m{m}.npz'));qint=cert['q'];qden=int(cert['den'])
 trail=np.load(Path(__file__).resolve().parents[1]/f'square_aklt_loop_audit_20261105/trail_certificate_m{m}.npz');to,ww=trail['targets'],trail['weights']
 assert np.all(15*qint>=15*qden+(ww*qint[to]).sum(1))
 # qbase resolves x0=1/3. Scale by rationalfactor1001/1000 for tinypositive tilt.
 scale=F(1001,1000);qmax_exact=F(int(qint.max()),qden)
 assert scale*(1-3*(x-F(1,3))*qmax_exact)>=1
 q=up(up(np.tile(qbase,4))*float(scale));qmax=float(q.max())
 # Independently certify the actual binary64 q as exact dyadic rationals.
 # This eliminates all reliance on the rounding direction of qbase/scale.
 assert qmax<1024
 qdy=np.ldexp(q[:N],52).astype(np.int64).astype(object);dyden=2**52
 assert all(float(a)/dyden==b for a,b in zip(qdy,q[:N]))
 exact_slack=5*x.denominator*qdy-5*x.denominator*dyden-x.numerator*(ww*qdy[to]).sum(1)
 assert min(exact_slack)>=0
 edge_tabs=[table(L,x),table(L,x*F(3,5))]
 source_tabs=[table(L,F(3,5)**r)for r in range(int(source_r.max())+1)]
 all_records=[]
 for ix in range(L//2+1):
  mx=1 if ix in(0,L//2) else 2
  for iy in range(L//2+1):
   my=1 if iy in(0,L//2) else 2;mult=mx*my
   phases=(delta[:,0]*ix+delta[:,1]*iy)%L
   iscontact=w<.9
   cs=[]
   for j in range(5):cs.append(np.where(iscontact,edge_tabs[1][j][phases],edge_tabs[0][j][phases]))
   C=coo_matrix((cs[0],(rows,cols)),shape=(n,n)).tocsr();A=I-C
   phases_b=(pos[:,0]*ix+pos[:,1]*iy)%L
   b=np.zeros(n,complex);blo=np.zeros(n,complex);bhi=np.zeros(n,complex)
   for r,tb in enumerate(source_tabs):
    ids=np.flatnonzero(source_good & (source_r==r));ph=phases_b[ids]
    b[ids]=tb[0][ph];blo[ids]=tb[1][ph]+1j*tb[3][ph];bhi[ids]=tb[2][ph]+1j*tb[4][ph]
   y,info=gmres(A,b,rtol=tol,atol=0,restart=100,maxiter=1000);assert info==0
   z,info=gmres(A,y,rtol=tol,atol=0,restart=100,maxiter=1000);assert info==0
   e1=residual_bound(y,blo,bhi,cs[1:],slots,q)
   e2=float(up(residual_bound(z,y,y,cs[1:],slots,q)+up(qmax*e1)))
   rr=[]
   for mask in(sink_s,sink_t):
    fy,ey=eval_linear(y,mask);fz,ez=eval_linear(z,mask)
    # Keep rational arithmetic for combination and Fourier averaging.
    gu=F(fy)+F(ey)+F(e1)
    hu=(m-1)*(F(fy)+F(ey))+F(fz)+F(ez)+(m-1)*F(e1)+F(e2)
    rr.append((gu,hu))
   all_records.append((mult,rr,e1,e2))
  print('row',ix,'of',L//2,'elapsed',time.monotonic()-start,flush=True)
 counts_s={4:F(0),6:F(2),8:F(10),10:F(308,5),12:F(352)}
 counts_t={4:F(2),6:F(4),8:F(126,5),10:F(584,5),12:F(16664,25)}
 outs=[]
 for index,cc in enumerate((counts_s,counts_t)):
  g=x**m*sum((mult*r[index][0]for mult,r,*_ in all_records),F(0))/(L*L)
  h=x**m*sum((mult*r[index][1]for mult,r,*_ in all_records),F(0))/(L*L)
  g+=sum((c*x**k for k,c in cc.items()if k<=m),F(0))
  h+=sum((k*c*x**k for k,c in cc.items()if k<=m),F(0))
  outs.append((g,6*h))
 (gs,s),(gt,t)=outs;a_s=s/5+t/2;a_t=s/2+7*t/20;m4=F(6,5)*gs*s+F(3,5)*gt*t;qfinal=a_s+m4
 assert a_s-a_t>=3*x**4 # absorbs simple-loop self through forced4turns.
 report=dict(memory=m,torus_side=L,states=n,tilted_x=str(x),positive_mu=math.log(float(3*x)),straight_excursion_mass_upper=float(gs),turn_excursion_mass_upper=float(gt),straight_length_moment_upper=float(s),turn_length_moment_upper=float(t),straight_charge_upper=float(a_s),turn_charge_upper=float(a_t),degree4_coverage_upper=float(m4),raw_branching_q_upper=float(qfinal),raw_branching_q_upper_rational=str(qfinal),margin=float(1-qfinal),supersolution_max=qmax,max_interval_residual_error=max(r[-1]for r in all_records),elapsed_seconds=time.monotonic()-start,claim='Positive tilted all-loop raw branching bound conditional on documented combinatorial mapping; interval residuals and integer resolvent witness certify finite-torus arithmetic. No quantum-gap or cumulant claim.')
 return report
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--memory',type=int,default=10);ap.add_argument('--side',type=int,default=32);ap.add_argument('--tol',type=float,default=1e-11);a=ap.parse_args();r=run_certificate(a.memory,a.side,a.tol,F(1000001,3000000));print(json.dumps(r,indent=2));Path(__file__).with_name(f'certified_geometry_m{a.memory}_L{a.side}.json').write_text(json.dumps(r,indent=2)+'\n')
