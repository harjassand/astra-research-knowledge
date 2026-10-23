"""Physical BEFORE-noise phase coding versus downstream digital sign flipping.
A synthetic two-mode converter with an exact cooling-sign observational ambiguity.
No real detector, optical modulator, or measured data is represented.
"""
from pathlib import Path
import numpy as np,json,time
from thermal_bridge import lyap,expm,adj
ROOT=Path(__file__).resolve().parent

def complex_normal(rng,shape):return (rng.normal(size=shape)+1j*rng.normal(size=shape))/np.sqrt(2)

def chol_psd(C):
 w,V=np.linalg.eigh((C+adj(C))/2);assert w.min()>-1e-12;return V*np.sqrt(np.maximum(w,0))

def main():
 rng=np.random.default_rng(23102625);n=2;I=np.eye(n);H=np.array([[0.,.3],[.3,0.]],complex);G=-.5*I-1j*H;Q0=np.diag([.1,.02]);CA=lyap(G,Q0);P=.1*I;CB=CA+P
 Qi=[np.diag([1.,0]),np.diag([0.,1.])];ns=[.1,.02];truthA=np.array([np.trace(q@(x*I-CA)).real for q,x in zip(Qi,ns)]);truthB=np.array([np.trace(q@(x*I-CB)).real for q,x in zip(Qi,ns)])
 assert truthA[0]>0 and truthB[0]<0
 dt=.2;M=expm(G*dt);Minv=np.linalg.inv(M);LA=chol_psd(CA);LZ=chol_psd(P);EA=chol_psd(CA-M@CA@adj(M));EZ=chol_psd(P-M@P@adj(M));rows=[];N=100000;start=time.perf_counter()
 for rep in range(6):
  X=np.empty((N,n),complex);Z=np.empty_like(X);X[0]=LA@complex_normal(rng,(n,));Z[0]=LZ@complex_normal(rng,(n,));eA=complex_normal(rng,(N-1,n))@EA.T;eZ=complex_normal(rng,(N-1,n))@EZ.T
  for k in range(1,N):X[k]=M@X[k-1]+eA[k-1];Z[k]=M@Z[k-1]+eZ[k-1]
  eps=rng.choice([-1.,1.],N);plain=X+Z
  # A: electronics Z are introduced AFTER a hardware sign flips the signal.
  raw_hardware_A=eps[:,None]*X+Z;demod_A=eps[:,None]*raw_hardware_A
  # B: the same OU fluctuations are intrinsic pump noise, so they are modulated too.
  raw_hardware_B=eps[:,None]*(X+Z);demod_B=eps[:,None]*raw_hardware_B
  # Merely multiplying old digital data twice leaves ALL data unchanged.
  software_only=eps[:,None]*(eps[:,None]*plain);assert np.array_equal(software_only,plain)
  def estimate(Y):
   C=Minv@(Y[1:].T@Y[:-1].conj()/(len(Y)-1));C=(C+adj(C))/2
   j=np.array([np.trace(q@(x*I-C)).real for q,x in zip(Qi,ns)])
   return C,j
  def innovation_cov(Y):
   E=Y[1:]-Y[:-1]@M.T;Q=E.T@E.conj()/(len(Y)-1);C=np.linalg.solve(np.eye(n*n)-np.kron(M.conj(),M),Q.reshape(-1,order='F')).reshape((n,n),order='F');return (C+adj(C))/2
  cp,jp=estimate(plain);caa,ja=estimate(demod_A);cbb,jb=estimate(demod_B)
  cy_half,_=estimate(plain[:N//2]);cz_half,_=estimate(Z[N//2:]);dark_A=cy_half-cz_half;dark_B=cy_half
  jdA=float(np.trace(Qi[0]@(ns[0]*I-dark_A)).real);jdB=float(np.trace(Qi[0]@(ns[0]*I-dark_B)).real)
  ci=innovation_cov(plain[:N//2]);zi=innovation_cov(Z[N//2:]);jiA=float(np.trace(Qi[0]@(ns[0]*I-(ci-zi))).real);jiB=float(np.trace(Qi[0]@(ns[0]*I-ci)).real)
  rows.append({'plain_current_cold':float(jp[0]),'dark_innovation_A_current_cold':jiA,'dark_innovation_B_current_cold':jiB,'dark_reference_A_current_cold':jdA,'dark_reference_B_current_cold':jdB,'dark_reference_budget':'N/2 signal frames plus N/2 signal-blocked sensor frames; same total N read frames; noise stationary across blocking assumed','coded_A_current_cold':float(ja[0]),'coded_B_current_cold':float(jb[0]),'coded_A_covariance_error_F':float(np.linalg.norm(caa-CA)),'coded_B_covariance_error_F':float(np.linalg.norm(cbb-CB)),'plain_A_B_path_difference':0,'software_only_change':float(np.linalg.norm(software_only-plain)),'phase_bits':N,'observation_span':(N-1)*dt})
 out={'status':'Synthetic readout-control construction, not an acquired device; no novelty or hardware advantage claimed','seed':23102625,'frames_each':N,'replicates':6,'sample_interval':dt,'true_number_currents_A':truthA.tolist(),'true_number_currents_B':truthB.tolist(),'model_A':'Physical diffusion diag(.1,.02), no excess pump noise, independent downstream sensor OU G with variance .1 I','model_B':'Physical diffusion diag(.1,.02)+.1 I, no downstream colored sensor; same G and all coherent/thermal linear-response parameters','exact_plain_observation_law':'All passive Gaussian path laws match, and remain matched under arbitrary common additive coherent plant inputs. Sums of independent same-G OU sources equal one source with summed diffusion.','positive_lag_coded_identity':'E[(eps_j Y_j)(eps_k Y_k)^dagger]=Gamma_signal(j,k), j!=k, when physical signal is signed before invariant downstream noise; iid signs independent of the full joint pre-code signal/sensor process; signal/sensor cross-correlation is allowed','readout_primitive':'An actual calibrated optical/electrical phase/sign modulation BEFORE the nuisance is introduced; multiplication after digitization cannot implement it','upstream_noise_limit':'Noise upstream of the phase element is modulated with the signal and remains inseparable. Code-dependent electronics and switching transients invalidate the instantaneous model. A separate causal_filter_phase.py theorem handles a discrete causal LTI readout with fixed nonzero current tap; this simulation is instantaneous.','calibration_supplied':'G, canonical readout metric, bath couplings and occupations are supplied equally to all covariance estimators here; separate thermal_bridge.py addresses their conditional acquisition.','rows':rows,'RMS_coded_A_current_error':float(np.sqrt(np.mean([(r['coded_A_current_cold']-truthA[0])**2 for r in rows]))),'RMS_dark_innovation_A_current_error':float(np.sqrt(np.mean([(r['dark_innovation_A_current_cold']-truthA[0])**2 for r in rows]))),'RMS_dark_innovation_B_current_error':float(np.sqrt(np.mean([(r['dark_innovation_B_current_cold']-truthB[0])**2 for r in rows]))),'RMS_dark_reference_A_current_error':float(np.sqrt(np.mean([(r['dark_reference_A_current_cold']-truthA[0])**2 for r in rows]))),'RMS_dark_reference_B_current_error':float(np.sqrt(np.mean([(r['dark_reference_B_current_cold']-truthB[0])**2 for r in rows]))),'RMS_coded_B_current_error':float(np.sqrt(np.mean([(r['coded_B_current_cold']-truthB[0])**2 for r in rows]))),'wall_seconds':time.perf_counter()-start}
 (ROOT/'phase_coded_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
