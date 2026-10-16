"""One reduced-only constrained-LS structural test on the unchanged weighted basis."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1'
import resource
resource.setrlimit(resource.RLIMIT_AS,(2*1024**3,2*1024**3))
import pathlib,sys,json,hashlib,time
import numpy as np,scipy.linalg as la
from numpy.polynomial import chebyshev as ch
sys.path.insert(0,str(pathlib.Path(__file__).parents[1]))
import diagnostic as d
P=pathlib.Path(__file__).parent;SOURCE=P.parent/'weighted_repair/candidate.npz';d.P=P;d.START=time.perf_counter();d.LOG=[]
z=np.load(SOURCE);oldm=len(z['time_coefficients']);m=oldm-1
basis=[[z[f'basis_{j}_core_{i}'] for i in range(8)] for j in range(1,oldm)]
# Structural support is verified from saved physical dyadic cores, not inferred.
for b in basis:
 for a in b:
  assert np.all(a[:,:39,:]==0) and np.all(a[:,62:,:]==0)
# Delta basis is byte-for-byte the original exported delta.
for a in basis[0]:assert a.shape==(1,163,1) and np.array_equal(a[0,:,0],np.eye(163)[50])
M=z['gram'][1:oldm,1:oldm];K=z['projection_operator'][1:oldm,1:oldm]
S=np.ones(m);S[0]=z['sqrt_mu'][50]**8
mass_physical=np.array([d.functional(b) for b in basis]);mw=S*mass_physical
fphysical=np.array([d.flux(b) for b in basis]);assert np.all(fphysical==0)
fw=S*fphysical
unconstrained=la.solve(M,K,assume_a='sym');v=la.solve(M,mw,assume_a='sym');denominator=float(mw@v)
Cw=unconstrained-np.outer(v,(mw@unconstrained+fw))/denominator
Cg=S[:,None]*Cw/S[None,:]
C=np.zeros((m+1,m+1));C[:m,:m]=Cg;C[-1,:m]=fphysical
initial=np.zeros(m+1);initial[0]=1;coeff=d.cheb_solve(C,initial,32);st=d.standard(coeff,initial)
td=np.pad(ch.chebder(st,axis=1)*2/d.h,((0,0),(0,1)))-C@st
arrays={'time_coefficients':coeff[:m],'initial_coefficients':initial[:m],'overflow_coefficients':coeff[-1],'initial_overflow':np.array(0.),'projected_generator':C,'whitened_projected_generator':Cw,'gram_whitened':M,'projection_operator_whitened':K,'mass_functional':np.r_[mass_physical,1.],'physical_flux':fphysical,'coefficient_scaling':S,'mu':z['mu'],'sqrt_mu':z['sqrt_mu']}
for j,b in enumerate(basis):
 for i,a in enumerate(b):arrays[f'basis_{j}_core_{i}']=a
np.savez(P/'candidate.npz',**arrays)
manifest=json.loads((SOURCE.parent/'candidate.json').read_text());manifest.update(method='reduced-only constrained weighted least-squares projection on the unchanged12 localized physical basis vectors; not AMEn',basis_count=m,source_candidate_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),constraint='Cw=M^-1K-M^-1m*(m^T M^-1K+f^T)/(m^T M^-1m), Cphysical=S*Cw*S^-1; physical sink derivative=fphysical^T a',no_new_enrichment=True,initial_basis_index=0,first_basis_role='exact delta; broad Riesz trial direction removed',physical_flux_zero_reason='Every saved physical core is exactly supported39..61, separated from cap162; full-generator action at support boundaries retained')
(P/'candidate.json').write_text(json.dumps(manifest,indent=2));end=ch.chebval(1,st.T);mc=arrays['mass_functional'];mp=mc@st;mp[0]-=1
report=dict(source=str(SOURCE),source_sha256=manifest['source_candidate_sha256'],candidate_sha256=hashlib.sha256((P/'candidate.npz').read_bytes()).hexdigest(),method='one authorized reduced-only structural test; no new basis/weights/model/slab',basis_count=m,degree=32,h='0.0001',gram_condition=float(np.linalg.cond(M)),constraint_denominator=denominator,unconstrained_mass_row_norm=float(la.norm(mw@unconstrained+fw)),constrained_mass_row_norm=float(la.norm(mw@Cw+fw)),physical_mass_row_norm=float(la.norm(mc@C)),physical_flux=fphysical.tolist(),endpoint_augmented_mass=float(mc@end),mass_coefficient_l1=float(sum(abs(mp))),endpoint_success=float(sum(d.functional(b,[d.LOW]*8)*end[j] for j,b in enumerate(basis))),endpoint_overflow=float(end[-1]),endpoint_outside39_61_exact=0,initial_error_exact=0,join_error_exact=0,reduced_time_defect_coefficient_fro=float(la.norm(td)),full_residual_upper='not yet evaluated; awaiting independent full-operator witness before duplicating large contractions',elapsed_seconds=time.perf_counter()-d.START,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
(P/'construction.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
