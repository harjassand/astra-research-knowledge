"""Adaptive continuum interval proof using rational Fourier coefficients."""
from certify_phase_density import *

def cells(data,N,x,y,tables,polys):
  sl,sh,cl,ch,phi=tables
  rho_coeff=[Q(s) for s in data['rho_coefficients']]
  phase=[(i,j,Q(A),Q(B)) for i,j,A,B in data['phase']]
  shape=x.shape
  def trig(i,j):
   idx=(2*(i*x+j*y)+i+j)%(2*N)
   rad=encl(phi*(abs(i)+abs(j))/N)[1]
   sn=I(np.maximum(-1,down(sl[idx]-rad)),np.minimum(1,up(sh[idx]+rad)))
   cs=I(np.maximum(-1,down(cl[idx]-rad)),np.minimum(1,up(ch[idx]+rad)))
   return cs,sn
  rr=[I(np.ones(shape))]+[I(np.zeros(shape)) for _ in range(5)]
  inds=[(0,0),(1,0),(0,1),(2,0),(1,1),(0,2)]
  for (i,j),(A,B) in zip(data['modes'],zip(rho_coeff[::2],rho_coeff[1::2])):
   cs,sn=trig(i,j)
   cycle=[(cs,sn),(-sn,cs),(-cs,-sn),(sn,-cs)]
   for h,(dx,dy) in enumerate(inds):
    fac=i**dx*j**dy
    if fac:
     u,v=cycle[(dx+dy)%4];rr[h]=rr[h]+fac*(I.rat(A)*u+I.rat(B)*v)
  kk=[I(np.zeros(shape)),I(np.ones(shape))]+[I(np.zeros(shape)) for _ in range(3)]
  kinds=[(1,0),(0,1),(2,0),(1,1),(0,2)]
  for i,j,A,B in phase:
   cs,sn=trig(i,j);cycle=[(cs,sn),(-sn,cs),(-cs,-sn),(sn,-cs)]
   for h,(dx,dy) in enumerate(kinds):
    fac=i**dx*j**dy
    if fac:
     u,v=cycle[(dx+dy)%4];kk[h]=kk[h]+fac*(I.rat(A)*u+I.rat(B)*v)
  r,rx,ry,rxx,rxy,ryy=rr;kx,ky,kxx,kxy,kyy=kk
  if np.any(r.lo<=0):
   return np.full(shape,-np.inf),np.full(shape,np.inf),r.lo
  a=rx/(4*r);b=ry/(4*r)
  inputs=[a,b,kx,ky];powers=[[z**j for j in range(5)] for z in inputs]
  outs=[]
  for terms in polys:
   val=I(np.zeros(shape))
   for ex,coef in terms:
    vv=I.rat(coef)
    for k,e in enumerate(ex):
     if e:vv=vv*powers[k][e]
    val=val+vv
   outs.append(val)
  f,ja,jb=outs[:3];hh=outs[3:]
  ax=(rxx/r-rx*rx/(r*r))/4;bx=(rxy/r-rx*ry/(r*r))/4;by=(ryy/r-ry*ry/(r*r))/4
  div=hh[0]*ax+hh[1]*bx+hh[2]*kxx+hh[3]*kxy+hh[4]*bx+hh[5]*by+hh[6]*kxy+hh[7]*kyy
  g=f-a*ja-b*jb-div/4

  return g.lo,g.hi,r.lo

def main():
 data=json.loads((ROOT/'phase_density_certificate.json').read_text())
 polys=poly_setup();N=256;target=1.0
 xx,yy=np.meshgrid(np.arange(N),np.arange(N),indexing='ij'); x=xx.ravel();y=yy.ravel()
 ledger=[];total=0;certmin=1e100;densitymin=1e100
 while len(x):
  if N>32768:raise RuntimeError('interval refinement limit reached')
  tables=trig_table(N);badx=[];bady=[];good=0;levelmin=1e100
  for st in range(0,len(x),1024):
   xs=x[st:st+1024];ys=y[st:st+1024]
   lo,hi,rlo=cells(data,N,xs,ys,tables,polys)
   ok=(lo>=target)&(rlo>0)
   if np.any(ok):
    good+=int(ok.sum());certmin=min(certmin,float(lo[ok].min()));densitymin=min(densitymin,float(rlo[ok].min()))
   if np.any(~ok):badx.append(xs[~ok]);bady.append(ys[~ok])
   levelmin=min(levelmin,float(lo.min()))
  total+=len(x);item={'grid_denominator':N,'tested':len(x),'certified':good,'unresolved':len(x)-good,'minimum_enclosure':levelmin}
  ledger.append(item);print(item,flush=True)
  if not badx:break
  bx=np.concatenate(badx);by=np.concatenate(bady)
  x=np.concatenate([2*bx,2*bx,2*bx+1,2*bx+1]);y=np.concatenate([2*by,2*by+1,2*by,2*by+1]);N*=2
 result={'status':'PASS','claim':'rho>0 and g_rho >=1 on the complete 2pi-periodic torus','target':1,'certified_minimum':certmin,'density_lower':densitymin,'total_cells_checked':total,'ledger':ledger,
 'meaning':'For G and the fixed phase in the coefficient file, E_theta(r^4)>= E r^4 for EVERY periodic W1,4 amplitude r. No quasiconvexity of G is assumed.',
 'proof_obligations':'analytic convexity and integration by parts proved in accompanying note; interval code relies on IEEE arithmetic basic operations'}
 (ROOT/'adaptive_continuum_certificate.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))

if __name__=='__main__':main()
