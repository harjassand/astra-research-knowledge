from pathlib import Path
import numpy as np,json,math
rng=np.random.default_rng(19411)
rows=[];worst=0.
# Actual coherent QPE, bin-copy and QPE inverse on each eigenvalue.
for M,s in [(16,1),(32,1),(8,3)]:
 J=4;w=4/J
 H=np.array([[1.,1.],[1.,-1.]])/np.sqrt(2);HM=np.array([[1.]])
 for _ in range(int(np.log2(M))):HM=np.kron(HM,H)
 F=np.exp(2j*np.pi*np.outer(np.arange(M),np.arange(M))/M)/np.sqrt(M)
 for phi in [-.249,-.13,-.001,.0,.113,.249]:
  U=F.conj().T@np.diag(np.exp(2j*np.pi*phi*np.arange(M)))@HM
  V=np.array([[1.]])
  for _ in range(s):V=np.kron(V,U)
  amps=V[:,0];indices=np.indices((M,)*s).reshape(s,-1).T
  vals=4*np.where(indices/M<.5,indices/M,indices/M-1);med=np.median(vals,axis=1)
  for offset in [0.,.125,.5,.875]:
   labs=np.floor((med-offset)/w).astype(int)%J;ideal=int(np.floor((4*phi-offset)/w))%J
   encoded=np.zeros((M**s,J),complex);encoded[np.arange(M**s),labs]=amps
   actual=V.conj().T@encoded
   p=float(np.sum(abs(amps[labs==ideal])**2));target=np.zeros_like(actual);target[0,ideal]=1
   overlap=np.vdot(target,actual);dist=np.linalg.norm(actual-target)
   err=max(abs(overlap-p),abs(dist**2-2*(1-p)));worst=max(worst,float(err))
   assert err<1e-11
   rows.append({'M':M,'s':s,'phi':phi,'offset':offset,'correct_bin_probability':p,'isometry_distance':float(dist)})
# Theorem schedules, with rational public T upper bound U=4sM.
sched=[]
for nu in [1/2,1/8,1/32]:
 for J in [4,16,64]:
  w=4/J;g=nu**2*w/256;beta=nu**2/32
  L=2**math.ceil(math.log2(256/nu**2));M=2**math.ceil(math.log2(4096/g));s=1
  while 2**(-s)>beta:s+=2
  U=4*s*M;tau=nu/4;times=[np.pi*2**ell/2 for ell in range(int(math.log2(M)))]*(2*s)
  upper_times=[2**(ell+1) for ell in range(int(math.log2(M)))]*(2*s)
  counts=[math.ceil(16*u)+math.ceil(64*u*U/tau) for u in upper_times]
  err=sum(64*t*t/n for t,n in zip(times,counts));bound=math.sqrt(2*beta)+2*math.sqrt(2*g/w+1/L)
  assert err<=tau and bound<nu/2
  assert sum(counts)<=16*U+64*U*U/tau+2*len(times)
  sched.append({'nu':nu,'J':J,'M':M,'s':s,'phase_qubits':s*int(math.log2(M)),'ideal_bound_over_nu':bound/nu,'simulation_bound_over_tau':err/tau,'source_preparation_upper_bound':8*sum(counts)})
out={'coherent_compute_copy_uncompute_cases':len(rows),'max_overlap_identity_residual':worst,'cases':rows,'public_schedules':sched,'scope':'Small coherent ideal-QPE diagnostics and arithmetic of enormous bounded schedules; no theorem-sized programmed QPE executed'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'coherent_cases':len(rows),'max_residual':worst,'schedules':len(sched)}))
