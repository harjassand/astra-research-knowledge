"""Read-only diagnostics of the immutable exported trajectory and reduced matrix."""
import diagnostic as d
import numpy as np, scipy.linalg as la
from numpy.polynomial import chebyshev as ch
from decimal import Decimal,localcontext
import json,time,resource,pathlib
z=np.load(d.P/'candidate.npz');m=z['time_coefficients'].shape[0]
basis=[[z[f'basis_{j}_core_{i}'] for i in range(8)] for j in range(m)]
cf=np.vstack([z['time_coefficients'],z['overflow_coefficients']]);initial=np.r_[z['initial_coefficients'],z['initial_overflow']];st=d.standard(cf,initial);end=ch.chebval(1,st.T);C=z['projected_generator']
# A similarity transform changes coordinate units only. It does not change the projected ODE.
S=np.ones(m+1);S[0]=z['mass_functional'][0];Cs=S[:,None]*C/S[None,:]
end_expm=la.expm(d.h*Cs)@(S*initial);end_expm/=S

def fpoly(weights,overflow=0):
 b=np.array([d.functional(q,weights) for q in basis]+[overflow]);a=[]
 for q in basis:
  g=d.Agrid(q);a.append(d.functional(g,weights)+overflow*d.flux(q))
 a=np.r_[a,0.];coeff=np.pad(ch.chebder(b@st)*2/d.h,(0,1))-a@st
 return dict(coefficient_l1=float(np.sum(abs(coeff))),integrated_abs_float=d.integral_abs(coeff),endpoint_functional=float(b@end),coefficients=coeff.tolist())
one=np.ones(d.D);high=(d.N>=63).astype(float);cube=((d.N>=38)&(d.N<=62)).astype(float)
aggregates={'site0_ge63_grid':fpoly([high]+[one]*7),'cube38_62_grid':fpoly([cube]*8),'total_grid':fpoly([one]*8),'total_augmented':fpoly([one]*8,1)}
# Exact-dyadic coefficients are accumulated with80-decimal-digit arithmetic.
# This is high precision, not a directed interval enclosure.
def high_mass(q):
 with localcontext() as ctx:
  ctx.prec=80;vec=[Decimal(1)]
  for core in q:
   l,n,r=core.shape;out=[Decimal(0)]*r
   for a in range(l):
    for b in range(r):
     total=sum((Decimal.from_float(float(x)) for x in core[a,:,b]),Decimal(0))
     out[b]+=vec[a]*total
   vec=out
  return vec[0]
ms=[high_mass(q) for q in basis]+[Decimal(1)]
with localcontext() as ctx:
 ctx.prec=80
 # At s=1, anchored even terms vanish and odd terms get factor2.
 end_exact=[Decimal.from_float(float(v))+sum((2*Decimal.from_float(float(cf[j,k])) for k in range(1,cf.shape[1],2)),Decimal(0)) for j,v in enumerate(initial)]
 mass_end=sum((a*b for a,b in zip(ms,end_exact)),Decimal(0))
 masspoly=[sum((ms[j]*Decimal.from_float(float(cf[j,k])) for j in range(m+1)),Decimal(0)) for k in range(1,cf.shape[1])]
 out=dict(endpoint_collocation=end.tolist(),endpoint_reduced_expm=end_expm.tolist(),same_reduced_ode_max_endpoint_difference=float(np.max(np.abs(end-end_expm))),same_reduced_ode_augmented_l1_difference_upper=float(sum(d.functional([np.abs(a) for a in q])*abs(end[i]-end_expm[i]) for i,q in enumerate(basis))+abs(end[-1]-end_expm[-1])),overflow_collocation=float(end[-1]),overflow_reduced_expm=float(end_expm[-1]),uniform_grid_mass_collocation=float(end[0]*S[0]),uniform_grid_mass_reduced_expm=float(end_expm[0]*S[0]),mass_end_80decimal=str(mass_end),mass_defect_80decimal=str(mass_end-1),mass_coeff_l1_80decimal=str(sum(abs(x) for x in masspoly)),basis_mass_80decimal=[str(x) for x in ms],aggregates=aggregates,raw_reduced_generator_norm=float(la.norm(C)),mass_scaled_reduced_generator_norm=float(la.norm(Cs)),elapsed_seconds=time.perf_counter()-d.START,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,warning='High precision and matrix exponential here are diagnostics, not outward enclosures; no new trajectory or solver rerun.')
(d.P/'candidate_audit.json').write_text(json.dumps(out,indent=2));print(json.dumps({k:v for k,v in out.items() if k not in ['basis_mass_80decimal','endpoint_collocation','endpoint_reduced_expm','aggregates']},indent=2));print('aggregate absolute integrals', {k:v['integrated_abs_float'] for k,v in aggregates.items()})
