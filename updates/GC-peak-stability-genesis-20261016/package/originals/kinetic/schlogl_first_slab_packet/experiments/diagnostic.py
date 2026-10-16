"""Independent bounded TT Arnoldi/Galerkin plus Chebyshev diagnostic, not tAMEn."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1'
import resource
resource.setrlimit(resource.RLIMIT_AS,(2*1024**3,2*1024**3))
import numpy as np
import scipy.linalg as la
from numpy.polynomial import chebyshev as ch
import json,time,pathlib,hashlib,sys,gc
P=pathlib.Path(__file__).parent;START=time.perf_counter();LOG=[]
D=163;h=1e-4;RATE=8.2207;ORDER=[0,4,1,5,2,6,3,7]
PHYSICAL_EDGES=[(0,1),(1,2),(2,3),(4,5),(5,6),(6,7),(0,4),(1,5),(2,6),(3,7)]
EDGES=[tuple(sorted((ORDER.index(i),ORDER.index(j)))) for i,j in PHYSICAL_EDGES]
N=np.arange(D,dtype=float);LOW=(N<=15).astype(float);DEG=[sum(i in e for e in EDGES) for i in range(8)]
BIRTH=2.676*N*(N-1)+108.102;DEATH=.040*N*(N-1)*(N-2)+37.881*N
MAXR=16;MAXM=12;K=32;TOL=1e-10;SQRTSIZE=float(D**4)
def emit(kind,**kw):
 z=dict(kind=kind,seconds=time.perf_counter()-START,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,**kw);LOG.append(z);print(json.dumps(z),flush=True);(P/'progress.json').write_text(json.dumps(LOG,indent=2))
def copy(x):return [q.copy() for q in x]
def scale(x,a):z=list(x);z[0]=z[0]*a;return z
def dot(x,y,weight=None):
 v=np.ones((1,1))
 for i,(a,b) in enumerate(zip(x,y)):
  if weight is not None:b=b*weight[i][None,:,None]
  v=np.einsum('ab,anc,bnd->cd',v,a,b,optimize=True)
 return float(v[0,0])
def functional(x,weights=None):
 v=np.ones(1)
 for i,a in enumerate(x):v=v@np.sum(a if weights is None else a*weights[i][None,:,None],axis=1)
 return float(v[0])
def point(x,coord):
 v=np.ones(1)
 for a,n in zip(x,coord):v=v@a[:,n,:]
 return float(v[0])
def tsum(terms):
 terms=[(x,c) for x,c in terms if c!=0]
 if not terms:return [np.zeros((1,D,1)) for _ in range(8)]
 out=[]
 for i in range(8):
  if i==0:z=np.concatenate([x[i]*c for x,c in terms],axis=2)
  elif i==7:z=np.concatenate([x[i] for x,c in terms],axis=0)
  else:
   z=np.zeros((sum(x[i].shape[0] for x,c in terms),D,sum(x[i].shape[2] for x,c in terms)));a=b=0
   for x,c in terms:
    q=x[i];z[a:a+q.shape[0],:,b:b+q.shape[2]]=q;a+=q.shape[0];b+=q.shape[2]
  out.append(z)
 return out
ROUND=[]
def rounded(x,tag,support=None):
 z=copy(x)
 for i in range(7):
  a,n,b=z[i].shape;q,r=la.qr(z[i].reshape(a*n,b),mode='economic',check_finite=False);z[i]=q.reshape(a,n,-1);z[i+1]=np.einsum('ab,bnc->anc',r,z[i+1],optimize=True)
 tails=[];ranks=[]
 for i in range(7,0,-1):
  a,n,b=z[i].shape;u,s,v=la.svd(z[i].reshape(a,n*b),full_matrices=False,check_finite=False)
  tailsq=np.concatenate((np.cumsum((s*s)[::-1])[::-1],[0.]));target=TOL*TOL*np.dot(s,s)/7
  viable=np.flatnonzero(tailsq<=target);r=min(MAXR,int(viable[0]) if len(viable) else len(s));r=max(1,r)
  tails.append(float(np.sqrt(tailsq[r])));ranks.append(r);z[i]=v[:r].reshape(r,n,b);z[i-1]=np.einsum('anb,bc->anc',z[i-1],u[:,:r]*s[:r],optimize=True)
 if support is not None:
  mask=((N>=50-support)&(N<=50+support)).astype(float)
  z=[a*mask[None,:,None] for a in z]
 ROUND.append(dict(tag=tag,ranks=ranks[::-1],tails=tails));return z

def local(a,i):
 z=-(BIRTH+DEATH+RATE*DEG[i]*N)[None,:,None]*a
 z[:,1:,:]+=BIRTH[:-1][None,:,None]*a[:,:-1,:]
 z[:,:-1,:]+=DEATH[1:][None,:,None]*a[:,1:,:]
 return z
def hop(a,down):
 z=np.zeros_like(a)
 if down:z[:,:-1,:]=N[1:][None,:,None]*a[:,1:,:]
 else:z[:,1:,:]=a[:,:-1,:]
 return z
def channels(cut):return ['s','f']+[(e,k) for e,(i,j) in enumerate(EDGES) if i<cut<=j for k in (0,1)]
def H(x):
 out=[]
 for i,a in enumerate(x):
  L=['s'] if i==0 else channels(i);R=['f'] if i==7 else channels(i+1);l,n,r=a.shape;z=np.zeros((l*len(L),n,r*len(R)))
  def put(left,right,value):
   if left in L and right in R:z[L.index(left)*l:(L.index(left)+1)*l,:,R.index(right)*r:(R.index(right)+1)*r]+=value
  put('s','s',a);put('f','f',a);put('s','f',local(a,i))
  for e,(p,q) in enumerate(EDGES):
   for k in (0,1):
    c=(e,k)
    if i==p:put('s',c,RATE*hop(a,k==0))
    elif i==q:put(c,'f',hop(a,k!=0))
    elif p<i<q:put(c,c,a)
  out.append(z)
 return out
def Agrid(x):
 out=H(x)
 p=[a*LOW[None,:,None] for a in x]
 if any(not np.any(a) for a in p):return out
 return tsum([(out,1),(H(p),-1)])
def flux(x):
 total=0.;ones=np.ones(D);cap=np.zeros(D);cap[-1]=1
 for i in range(8):
  w=[ones]*8;w[i]=cap;total+=BIRTH[-1]*functional(x,w)
 for i,j in EDGES:
  for a,b in ((i,j),(j,i)):
   w=[ones]*8;w[a]=N;w[b]=cap;total+=RATE*functional(x,w)
 return float(total)
def normqr(x,mu=None):
 z=list(x);logscale=0.;maxbytes=sum(a.nbytes for a in z)
 for i in range(8):
  a=z[i] if mu is None else z[i]/np.sqrt(mu[i])[None,:,None];l,n,r=a.shape
  if i==7:return float(np.exp(logscale)*la.norm(a)),maxbytes
  q,R=la.qr(a.reshape(l*n,r),mode='economic',check_finite=False);s=la.norm(R)
  if s==0:return 0.,maxbytes
  logscale+=np.log(s);R/=s;z[i+1]=np.einsum('ab,bnc->anc',R,z[i+1],optimize=True);z[i]=None
 return 0.,maxbytes

def operator_check():
 x0=(50,)*8;p=[np.eye(D)[50].reshape(1,D,1).copy() for _ in range(8)];a=Agrid(p);oracle={x0:0.}
 def entry(y,v):y=tuple(y);oracle[y]=oracle.get(y,0)+v;oracle[x0]-=v
 for i in range(8):
  for d,r in ((1,BIRTH[50]),(-1,DEATH[50])):
   y=list(x0);y[i]+=d;entry(y,r)
 for i,j in EDGES:
  for f,t in ((i,j),(j,i)):
   y=list(x0);y[f]-=1;y[t]+=1;entry(y,RATE*50)
 error=max(abs(point(a,x)-v) for x,v in oracle.items());assert error<1e-8
 target=[np.eye(D)[15].reshape(1,D,1).copy() for _ in range(8)]
 tnorm,_=normqr(Agrid(target));assert tnorm<1e-8
 cap=[np.eye(D)[162].reshape(1,D,1).copy() for _ in range(8)]
 sumcap=functional(Agrid(cap));fcap=flux(cap);assert abs(sumcap+fcap)<1e-7
 emit('operator_validation',support=len(oracle),max_entry_error=error,escape=-oracle[x0],target_frozen_norm=tnorm,cap_grid_mass_derivative=sumcap,cap_overflow_derivative=fcap,balance=sumcap+fcap)
 return p

def cheb_solve(C,initial,degree):
 # Endpoint-inclusive anchored Chebyshev collocation. k>=1 unknowns.
 s=-np.cos(np.pi*np.arange(1,degree+1)/degree)
 V=ch.chebvander(s,degree)[:,1:]-((-1.)**np.arange(1,degree+1))[None,:]
 Vd=np.column_stack([ch.chebval(s,ch.chebder(np.eye(degree+1)[k]))*2/h for k in range(1,degree+1)])
 # Unknown matrix coeff[k,j], each time basis is one block.
 system=np.kron(Vd,np.eye(len(C)))-np.kron(V,C)
 rhs=np.tile(C@initial,degree)
 coef=la.solve(system,rhs,check_finite=False).reshape(degree,len(C)).T
 coeff=np.zeros((len(C),degree+1));coeff[:,1:]=coef
 return coeff

def standard(c,initial):
 z=c.copy();z[:,0]=initial-z[:,1:]@((-1.)**np.arange(1,z.shape[1]));return z

def integral_abs(c):
 # Float polynomial roots give all sign intervals; interval rigor is separate.
 roots=ch.chebroots(c);real=sorted(float(z.real) for z in roots if abs(z.imag)<1e-8 and -1<z.real<1)
 knots=np.array([-1]+real+[1]);F=ch.chebint(c);return float(h/2*sum(abs(ch.chebval(b,F)-ch.chebval(a,F)) for a,b in zip(knots[:-1],knots[1:])))

def run():
 p=operator_check();basis=[p];nrm=[]
 for j in range(MAXM-1):
  raw=Agrid(basis[-1]);w=rounded(raw,f'A{j}',support=j+1);del raw
  # Two passes MGS with TT compression; all errors charged later by full defects.
  for rep in range(2):
   for i,v in enumerate(basis):
    alpha=dot(v,w);w=rounded(tsum([(w,1),(v,-alpha)]),f'mgs{j}:{rep}:{i}',support=j+1)
  norm,_=normqr(w);w=scale(w,1/norm);basis.append(w)
  emit('arnoldi',direction=j+1,normalizer=norm,ranks=[a.shape[2] for a in w[:-1]],core_bytes=sum(a.nbytes for a in w),mass=functional(w),max_local_discard=max(t for x in ROUND for t in x['tails']),orthogonality=max(abs(dot(v,w)) for v in basis[:-1]))
 (P/'rounding.json').write_text(json.dumps(ROUND,indent=2))
 # Normalized grid ones is a co-kernel component. Overflow coordinate is separate.
 unit=[np.full((1,D,1),1/np.sqrt(D)) for _ in range(8)]
 basis=[unit]+basis;m=len(basis);M=np.eye(m+1);Kmat=np.zeros((m+1,m+1));f=np.array([flux(b) for b in basis]);mass=np.array([functional(b) for b in basis]);rawrow=[]
 for i in range(m):
  for j in range(i+1):M[i,j]=M[j,i]=dot(basis[i],basis[j])
 for j,b in enumerate(basis):
  a=Agrid(b)
  for i in range(m):Kmat[i,j]=dot(basis[i],a)
  rawrow.append(Kmat[0,j]);Kmat[0,j]=-f[j]/mass[0];Kmat[-1,j]=f[j]
  emit('project_column',column=j,raw_mass_row=rawrow[-1],enforced_mass_row=Kmat[0,j],row_change=Kmat[0,j]-rawrow[-1],physical_flux=f[j],grid_mass_derivative=functional(a))
  del a;gc.collect()
 C=la.solve(M,Kmat,assume_a='sym',check_finite=False);initial=np.zeros(m+1);initial[1]=1
 mc=np.r_[mass,1.];emit('projection',dimension=m+1,gram_condition=np.linalg.cond(M),mass_left_defect=float(la.norm(mc@C)),mass_constant=mass[0],ideal_mass_constant=SQRTSIZE,maximum_rank=max(a.shape[2] for b in basis for a in b[:-1]))
 coeff=cheb_solve(C,initial,K);st=standard(coeff,initial);std=ch.chebder(st,axis=1)*2/h;td=np.pad(std,((0,0),(0,1)))-C@st
 # Export anchored polynomial, retaining basis vectors separately to prevent unbounded fused ranks.
 arrays={'time_coefficients':coeff[:m],'initial_coefficients':initial[:m],'overflow_coefficients':coeff[-1],'initial_overflow':np.array(0.),'projected_generator':C,'gram':M,'projection_operator':Kmat,'mass_functional':mc}
 for j,b in enumerate(basis):
  for i,a in enumerate(b):arrays[f'basis_{j}_core_{i}']=a
 np.savez(P/'candidate.npz',**arrays)
 manifest=dict(schema='schlogl-chebyshev-basis-v1',npz='candidate.npz',target_max=15,t_start='0',method='independent conservation-enriched adaptive TT Arnoldi/Galerkin with Chebyshev collocation, not tAMEn',basis_count=m,polynomial_degree=K,h='0.0001',left='0',right='0.0001',anchored_chebyshev=True,anchored_definition='initial_j + sum_{k=1}^K c[j,k]*(T_k(2*t/h-1)-(-1)^k)',order=ORDER,physical_edges=PHYSICAL_EDGES,cap=162,initial=[50]*8,target='all counts<=15',semantics='frozen_target_grid_plus_overflow',rates={'birth_quadratic':'2.676','birth_constant':'108.102','death_cubic':'0.040','death_linear':'37.881','diffusion':'8.2207'},initial_error_exact=0,join_error_exact=0,rank_cap=MAXR,direction_cap=MAXM,resource_cap_bytes=2*1024**3,arithmetic='float64 diagnostic; exported binary64 coefficients treated as exact dyadics; no interval enclosure')
 (P/'candidate.json').write_text(json.dumps(manifest,indent=2));emit('export_ready',file=str(P/'candidate.npz'),manifest=str(P/'candidate.json'),bytes=(P/'candidate.npz').stat().st_size)
 # Mass polynomial and dense reduced time defect are separate diagnostics.
 masspoly=mc@st;masspoly[0]-=1;end=ch.chebval(1,st.T);start=ch.chebval(-1,st.T)
 emit('time_diagnostic',mass_coefficients=masspoly.tolist(),mass_at_end=float(mc@end),mass_coefficient_l1=float(np.sum(np.abs(masspoly))),left_standard_conversion_error=float(np.max(np.abs(start-initial))),initial_anchored_error=0.,join_error=0.,reduced_defect_coefficient_fro=float(la.norm(td)),success_at_end=float(sum(functional(b,[LOW]*8)*end[j] for j,b in enumerate(basis))),overflow_at_end=float(end[-1]))
 # Weight is identical to previous diagnostic for comparability.
 mu=np.exp(-.5*((N-50)/4.)**2);mu/=mu.sum();mu=.999*mu+.001/D;mus=[mu]*8
 basisnorm=[]
 for i,b in enumerate(basis):v,_=normqr(b,mus);basisnorm.append(v)
 time_bound=sum(basisnorm[i]*integral_abs(td[i]) for i in range(m))+integral_abs(td[-1])
 spatial_bound=0.;details=[]
 for j,b in enumerate(basis):
  a=Agrid(b);terms=[(a,1)]+[(basis[i],-C[i,j]) for i in range(m) if C[i,j]!=0]
  # Core allocation forecast: stop before violating cap.
  ranks=[sum(x[i].shape[2] for x,c in terms) for i in range(7)]
  estimate=sum((1 if i==0 else ranks[i-1])*D*(1 if i==7 else ranks[i])*8 for i in range(8))
  if estimate>1050*1024**2:raise MemoryError(f'Uncompressed defect core forecast {estimate} bytes exceeds declared 1050MiB core gate')
  defect=tsum(terms);del a,terms;gc.collect();val,bytes_=normqr(defect,mus);del defect;gc.collect()
  sink=f[j]-C[-1,j];intc=integral_abs(st[j]);contrib=(val+abs(sink))*intc;spatial_bound+=contrib
  d=dict(column=j,full_weighted_grid_defect_norm=val,overflow_defect=sink,coefficient_integral_abs=intc,contribution=contrib,uncompressed_core_bytes=bytes_,ranks=ranks);details.append(d);emit('full_spatial_defect',**d)
 emit('complete_residual_triangle',spatial=spatial_bound,temporal=time_bound,total=spatial_bound+time_bound,initial=0.,join=0.,overflow='included',target_freezing='included',outward_rounding=False,enclosure_width=None)
 (P/'result.json').write_text(json.dumps(dict(spatial=spatial_bound,temporal=time_bound,total=spatial_bound+time_bound,details=details),indent=2))

if __name__=='__main__':
 try:run()
 except Exception as e:
  emit('stop',exception=type(e).__name__,message=str(e));raise
 finally:
  (P/'rounding.json').write_text(json.dumps(ROUND,indent=2))
