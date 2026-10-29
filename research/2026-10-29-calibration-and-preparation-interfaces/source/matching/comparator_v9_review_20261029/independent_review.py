import runpy,contextlib,io,json,numpy as np,hashlib
from pathlib import Path
base=Path(__file__).parent/'source/sequential_singlet_guard_20261029'
with contextlib.redirect_stdout(io.StringIO()): z=runpy.run_path(str(base/'compare_actual_two_design_v9.py'))
f=z['f']; out={}
def choi(S):
 return S.reshape(2,2,2,2).transpose(0,2,1,3).reshape(4,4)
cp=[]
for vi,m in enumerate(f.mp):
 for name in ['good','bad','testpass','testfail']:
  C=choi(m[name]);cp.append({'variant':vi,'map':name,'choi_min_eigenvalue':float(np.linalg.eigvalsh(C).min()),'hermitian_residual':float(np.linalg.norm(C-C.conj().T))})
 assert np.linalg.norm(f.effect(m['good']+m['bad'])-np.eye(2))<1e-12
 assert np.linalg.norm(f.effect(m['testpass']+m['testfail'])-np.eye(2))<1e-12
out['complete_CP_TP_checks']=cp
# Independent terminal bucket DP. Kraus reconstruct each bath superoperator from its Choi.
def kraus(S):
 vals,V=np.linalg.eigh(choi(S));return [np.sqrt(v)*w.reshape(2,2) for v,w in zip(vals,V.T) if v>1e-16]
def apply(K,r): return sum(np.einsum('ab,...bc,dc->...ad',A,r,A.conj()) for A in K)
def dp(m,s,cap):
 Ks={k:kraus(m[k]) for k in ['good','bad','testpass','testfail']}
 live=np.zeros((155,8,2,2),complex);live[0,0]=f.sigma;acc=np.zeros((8,2,2),complex);abort=0.;calls=0.
 tr=lambda r:float(np.trace(r,axis1=-2,axis2=-1).sum().real)
 for r in range(cap):
  calls+=tr(live);gp=s*apply(Ks['good'],live);bp=s*apply(Ks['bad'],live);nxt=(1-s)*apply(Ks['testpass'],live);abort+=(1-s)*tr(apply(Ks['testfail'],live))
  for j in range(155):
   dest=acc if j==154 else nxt[j+1]
   for k in range(8):dest[k]+=gp[j,k];dest[min(k+1,7)]+=bp[j,k]
  live=nxt
 return {'accept_probability':tr(acc),'accepted_more_than_t_fault_weight':tr(acc[-1]),'expected_source_calls':calls,'total_mass':tr(acc)+abort+tr(live)}
out['independent_kraus_DP_sixstate']=dp(f.mp[0],.4,500)
original=json.load(open(base/'compare_actual_two_design_v9.json'))['two_design_actual_test']['exact_compressed_DP']
for k in ['accept_probability','accepted_more_than_t_fault_weight','expected_source_calls']:assert abs(out['independent_kraus_DP_sixstate'][k]-original[k])<2e-8
# Restore actual weighted test maps from physical projector formula, not scalar rescaling.
Ts=[]
for fail in [False,True]:
 def fun(sig):
  out=np.zeros((2,2),complex)
  for S in f.Ss:
   for sign in [-1,1]:
    Pi=(np.eye(16)+sign*S)/2;Pt=(np.eye(16)+(-sign if fail else sign)*S)/2;Y=np.kron(Pt,np.eye(2));rho=np.kron(Pi@f.PH/2,sig);out+=f.ptrD(Y@f.Ugood@rho@f.Ugood.conj().T@Y)/6
  return out
 Ts.append(f.superof(fun))
m=dict(f.mp[0]);m['testpass'],m['testfail']=Ts
out['optimized_weighted_C3_hazard_slack']=float(np.linalg.eigvalsh(3*f.effect(Ts[1])-f.effect(m['bad'])).min())
out['independent_kraus_DP_weighted_C3']=dp(m,.25,800)
out['comparison_scope']='Same acquired candidate, same final bath, same U0, R=1, b=0,t=6,J=155. Different caps500/800; cap mass must be charged. Total physical control cost not compared.'
print(json.dumps(out,indent=2))
# Export exact supplied fixture matrices for subsequent new-operation comparisons.
np.savez(Path(__file__).with_name('reviewed_fixture_arrays.npz'),E=f.E,Vhat=f.Vhat,Ds=np.array(f.Ds),sigma=f.sigma,Ugood=f.Ugood,Uburst=f.Uburst,good=f.mp[0]['good'],bad=f.mp[0]['bad'],two_pass=f.mp[0]['testpass'],two_fail=f.mp[0]['testfail'],weighted_pass=Ts[0],weighted_fail=Ts[1])
