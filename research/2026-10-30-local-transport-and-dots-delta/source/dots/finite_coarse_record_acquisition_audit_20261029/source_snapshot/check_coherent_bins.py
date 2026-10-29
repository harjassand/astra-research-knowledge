import numpy as np,json
from pathlib import Path
rng=np.random.default_rng(8173)
def branch_vectors(b,M,J,u):
 phase=np.exp(2j*np.pi*np.arange(M)*b/4)
 psi=np.fft.fft(phase,norm='ortho')/np.sqrt(M)
 estimates=4*np.where(np.arange(M)/M<.5,np.arange(M)/M,np.arange(M)/M-1)
 bins=np.floor((estimates-u)/(4/J)).astype(int)%J
 vs=[]
 for j in range(J):
  selected=psi*(bins==j)
  vs.append(np.fft.fft(phase.conj()*np.fft.ifft(selected,norm='ortho'),norm='ortho'))
 return np.array(vs),psi,bins
rows=[]
for M in [16,32,64]:
 for case in range(12):
  bs=rng.uniform(-1,1,3);J=4;L=16;rho=np.ones((3,3))/3;errs=[];bounds=[]
  for ui in range(L):
   u=ui/L;data=[branch_vectors(b,M,J,u) for b in bs];idealbins=np.floor((bs-u)/(4/J)).astype(int)%J
   out=np.zeros((J,3,3),complex);ideal=np.zeros_like(out)
   worst=0.
   for i in range(3):
    V=data[i][0];q=V[idealbins[i],0].real
    assert abs(q-sum(abs(data[i][1][data[i][2]==idealbins[i]])**2))<1e-12
    worst=max(worst,np.sqrt(max(0,2*(1-q))))
    for j in range(3):
     for l in range(J):out[l,i,j]=rho[i,j]*np.vdot(data[j][0][l],V[l])
     if idealbins[i]==idealbins[j]:ideal[idealbins[i],i,j]=rho[i,j]
   err=.5*sum(np.sum(abs(np.linalg.eigvalsh(o-z))) for o,z in zip(out,ideal));assert err<=worst+1e-10
   assert abs(sum(np.trace(o) for o in out)-1)<1e-10
   errs.append(err);bounds.append(worst)
  rows.append(dict(M=M,case=case,mean_half_trace_error=float(np.mean(errs)),mean_isometry_bound=float(np.mean(bounds))))
# Within-bin coherence: full phase measurement destroys information that coarse copy/uncompute preserves.
M=256;data=[branch_vectors(b,M,4,0) for b in [.10,.20]]
coherent=sum(np.vdot(data[1][0][l],data[0][0][l]) for l in range(4))
fullphase=np.vdot(data[1][1],data[0][1])
assert abs(coherent)> .9 and abs(fullphase)<.1
out={'scope':'small single-QPE exact instrument diagnostics, not huge conservative schedule execution','cases':rows,'same_bin_coherence':{'copy_bin_uncompute_abs':float(abs(coherent)),'measure_full_phase_abs':float(abs(fullphase))}}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS',len(rows),'instruments; coherence',abs(coherent),abs(fullphase))
