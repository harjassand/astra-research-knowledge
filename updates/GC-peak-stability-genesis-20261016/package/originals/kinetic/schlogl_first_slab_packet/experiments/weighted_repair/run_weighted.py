"""Independent weighted TT Galerkin repair, not tAMEn. Same physical problem."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1'
import resource
resource.setrlimit(resource.RLIMIT_AS,(2*1024**3,2*1024**3))
import sys,pathlib,json,time,gc
sys.path.insert(0,str(pathlib.Path(__file__).parents[1]))
import diagnostic as d
import numpy as np,scipy.linalg as la
from numpy.polynomial import chebyshev as ch
from stream_norm import norm_sum
P=pathlib.Path(__file__).parent;d.P=P;d.START=time.perf_counter();d.LOG=[];d.ROUND=[];d.MAXR=32
Z=3.-2.**-50-2.**-112;MU=2.**(-abs(d.N-50))/Z;SM=np.sqrt(MU);mus=[MU]*8
local_physical=d.local;hop_physical=d.hop;flux_physical=d.flux

def local_white(a,i):return local_physical(a*SM[None,:,None],i)/SM[None,:,None]
def hop_white(a,down):return hop_physical(a*SM[None,:,None],down)/SM[None,:,None]
def physical(q):return [a*SM[None,:,None] for a in q]
def flux_white(q):return flux_physical(physical(q))
def Aphysical(q):
 d.local=local_physical;d.hop=hop_physical
 try:return d.Agrid(q)
 finally:d.local=local_white;d.hop=hop_white

def run():
 # Same physical checks as before, then whitened similarity action check.
 p=d.operator_check();d.local=local_white;d.hop=hop_white;d.flux=flux_white
 a=d.Agrid(p);ap=Aphysical(p);sq=SM[50]**8
 # q=physical(p)=sq*delta; verify the transformed action at all nonzero neighbors.
 coords=[(50,)*8]
 for i in range(8):
  for step in [-1,1]:v=[50]*8;v[i]+=step;coords.append(tuple(v))
 for i,j in d.EDGES:
  for f,t in [(i,j),(j,i)]:v=[50]*8;v[f]-=1;v[t]+=1;coords.append(tuple(v))
 err=max(abs(d.point(a,c)-d.point(ap,c)*sq/np.prod([SM[n] for n in c])) for c in coords)
 assert err<1e-8
 d.emit('whitened_operator_check',max_entry_error=err,mu_sum=float(MU.sum()),initial_whitened_norm=1/sq,minimum_mu=float(MU.min()),maximum_shift_ratio=float(max(SM[:-1]/SM[1:])),augmented_norm_rule='grid weighted L2 plus absolute overflow, no missing sqrt2')
 del a,ap
 basis=[p]
 for j in range(d.MAXM-1):
  a=d.Agrid(basis[-1]);w=d.rounded(a,f'A{j}',support=j+1);del a
  for rep in range(2):
   for i,v in enumerate(basis):w=d.rounded(d.tsum([(w,1),(v,-d.dot(v,w))]),f'mgs{j}:{rep}:{i}',support=j+1)
  norm,_=d.normqr(w);w=d.scale(w,1/norm);basis.append(w)
  d.emit('arnoldi',direction=j+1,normalizer=norm,ranks=[a.shape[2] for a in w[:-1]],core_bytes=sum(a.nbytes for a in w),physical_mass=d.functional(w,[SM]*8),max_local_discard=max(t for x in d.ROUND for t in x['tails']),orthogonality=max(abs(d.dot(v,w)) for v in basis[:-1]))
 unit=[SM.reshape(1,d.D,1).copy() for _ in range(8)];basis=[unit]+basis;m=len(basis);M=np.eye(m+1);K=np.zeros((m+1,m+1));f=np.array([flux_white(b) for b in basis]);mass=np.array([d.functional(b,[SM]*8) for b in basis])
 for i in range(m):
  for j in range(i+1):M[i,j]=M[j,i]=d.dot(basis[i],basis[j])
 for j,b in enumerate(basis):
  a=d.Agrid(b)
  for i in range(m):K[i,j]=d.dot(basis[i],a)
  raw=K[0,j];K[0,j]=-f[j];K[-1,j]=f[j]
  d.emit('project_column',column=j,raw_mass_row=raw,enforced_mass_row=K[0,j],row_change=K[0,j]-raw,physical_flux=f[j],grid_mass_derivative=d.functional(a,[SM]*8));del a;gc.collect()
 C=la.solve(M,K,assume_a='sym',check_finite=False);initial=np.zeros(m+1);initial[1]=1/sq;mc=np.r_[mass,1.]
 d.emit('projection',dimension=m+1,gram_condition=np.linalg.cond(M),mass_left_defect=float(la.norm(mc@C)),invariant_direction_mass=mass[0],maximum_rank=max(a.shape[2] for b in basis for a in b[:-1]))
 cw=d.cheb_solve(C,initial,d.K)
 # Export physical dyadic cores. Force exact delta basis by explicit coordinate scaling,
 # then charge full physical defects of the resulting saved representation.
 pb=[physical(b) for b in basis];pb[1]=p
 S=np.ones(m+1);S[1]=sq;ce=S[:,None]*cw;Ci=S[:,None]*C/S[None,:];ini=np.zeros(m+1);ini[1]=1
 st=d.standard(ce,ini);td=np.pad(ch.chebder(st,axis=1)*2/d.h,((0,0),(0,1)))-Ci@st
 arrays={'time_coefficients':ce[:m],'initial_coefficients':ini[:m],'overflow_coefficients':ce[-1],'initial_overflow':np.array(0.),'projected_generator':Ci,'whitened_projected_generator':C,'gram':M,'projection_operator':K,'mass_functional':np.r_[[d.functional(b) for b in pb],1.],'mu':MU,'sqrt_mu':SM}
 for j,b in enumerate(pb):
  for i,a in enumerate(b):arrays[f'basis_{j}_core_{i}']=a
 np.savez(P/'candidate.npz',**arrays)
 manifest=dict(schema='schlogl-chebyshev-basis-v1',npz='candidate.npz',method='independent geometrically weighted conservation-enriched TT Arnoldi/Galerkin; not tAMEn',basis_count=m,polynomial_degree=d.K,h='0.0001',t_start='0',left='0',right='0.0001',anchored_chebyshev=True,anchored_definition='initial_j + sum_{k=1}^K c[j,k]*(T_k(2*t/h-1)-(-1)^k)',order=d.ORDER,physical_edges=d.PHYSICAL_EDGES,cap=162,target_max=15,initial=[50]*8,semantics='frozen_target_grid_plus_overflow',rates={'birth_quadratic':'2.676','birth_constant':'108.102','death_cubic':'0.040','death_linear':'37.881','diffusion':'8.2207'},initial_error_exact=0,join_error_exact=0,rank_cap=d.MAXR,direction_cap=d.MAXM,resource_cap_bytes=2*1024**3,weight='mu_i(n)=2^(-abs(n-50))/(3-2^-50-2^-112); float values saved',norm_rule='grid weighted L2 plus absolute overflow; combined augmented L2 would require sqrt2',arithmetic='float64 diagnostic; exported binary64 coefficients treated as exact dyadics; no interval enclosure')
 (P/'candidate.json').write_text(json.dumps(manifest,indent=2));d.emit('export_ready',file=str(P/'candidate.npz'),manifest=str(P/'candidate.json'),bytes=(P/'candidate.npz').stat().st_size)
 massphysical=arrays['mass_functional'];masspoly=massphysical@st;masspoly[0]-=1;end=ch.chebval(1,st.T)
 d.emit('time_diagnostic',mass_at_end=float(massphysical@end),mass_coefficient_l1=float(sum(abs(masspoly))),initial_anchored_error=0,join_error=0,reduced_defect_coefficient_fro=float(la.norm(td)),success_at_end=float(sum(d.functional(b,[d.LOW]*8)*end[i] for i,b in enumerate(pb))),overflow_at_end=float(end[-1]),localized_invariant_mass_at_end=float(end[0]*massphysical[0]))
 # Complete full physical residual against the exact saved physical basis,
 # so conversion/rescaling effects are included rather than hidden.
 bn=[norm_sum([(b,1)],mus)[0] for b in pb];temporal=sum(bn[i]*d.integral_abs(td[i]) for i in range(m))+d.integral_abs(td[-1]);spatial=0.;details=[]
 for j,b in enumerate(pb):
  a=Aphysical(b);terms=[(a,1)]+[(pb[i],-Ci[i,j]) for i in range(m)];val,meta=norm_sum(terms,mus);sink=flux_physical(b)-Ci[-1,j];intc=d.integral_abs(st[j]);contribution=(val+abs(sink))*intc;spatial+=contribution
  info=dict(column=j,full_weighted_grid_defect_norm=val,overflow_defect=sink,coefficient_integral_abs=intc,contribution=contribution,**meta);details.append(info);d.emit('full_spatial_defect',**info);del a,terms;gc.collect()
 d.emit('complete_residual_triangle',spatial=spatial,temporal=temporal,total=spatial+temporal,initial=0,join=0,overflow='included',target_freezing='included',outward_rounding=False,enclosure_width=None)
 (P/'result.json').write_text(json.dumps(dict(spatial=spatial,temporal=temporal,total=spatial+temporal,details=details),indent=2))

if __name__=='__main__':
 try:run()
 except Exception as e:d.emit('stop',exception=type(e).__name__,message=str(e));raise
 finally:(P/'rounding.json').write_text(json.dumps(d.ROUND,indent=2))
