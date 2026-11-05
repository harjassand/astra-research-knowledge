"""Finite canonical-pointer receiver; floating illustration, not hardware certification."""
import json, math
from pathlib import Path
from time import perf_counter
import numpy as np
from scipy.linalg import expm
from scipy.integrate import solve_ivp
from scipy.special import ndtr

ROOT=Path(__file__).resolve().parent
N=100000; SEED=2026110517
D0=1.; alpha=.01; thermal=.03; rate=4*(1-alpha)*thermal**2
deadline=math.log(1/alpha)/rate
b=ell=1e-4; G=1.; md=1.; vQ=4e-14; vP=8*.01**2*b/3
read_sd=1e-7; bits=32; coinbits=24; half_range=16.; step=2**-27
logic_time=2e-5; future_time=.5; outcome_width=.001
rng=np.random.default_rng(SEED)
K=np.array([[1.,0.,.03,0.],[0.,1.,0.,0.],[.03,0.,.04,0.],[0.,0.,0.,1.]])
C=np.linalg.inv(K)
A=np.array([[0.,1.,0.,0.],[-1.,-1.,-.03,0.],[0.,0.,0.,1.],[-.03,0.,-.04,0.]])
noise=np.array([0.,math.sqrt(2),0.,0.])
ce,cv=np.linalg.eigh(C); Croot=(cv*np.sqrt(ce))@cv.T
m0=math.sqrt(2)*Croot@(np.array([0.,1.,1.,0.])/math.sqrt(2))

def fac(q):
    e,v=np.linalg.eigh((q+q.T)/2)
    if min(e)<-1e-10*max(max(abs(e)),1e-300): raise RuntimeError('indefinite noise')
    return v*np.sqrt(np.maximum(e,0))

def pointer_matrix(width):
    n=6; initial=np.r_[np.eye(n).ravel(),np.zeros(n*n)]
    def rhs(s,y):
        w=(1-math.cos(2*math.pi*s))/width
        L=np.zeros((n,n)); L[:4,:4]=A
        L[1,5]=G*w; L[4,0]=-G*w; L[4,5]=1/md
        D=np.zeros((n,n)); D[1,1]=2
        F=y[:n*n].reshape(n,n); Q=y[n*n:].reshape(n,n)
        return width*np.r_[(L@F).ravel(),(L@Q+Q@L.T+D).ravel()]
    sol=solve_ivp(rhs,[0,1],initial,method='DOP853',rtol=2e-12,atol=2e-15,max_step=1/32)
    if not sol.success: raise RuntimeError(sol.message)
    F=sol.y[:36,-1].reshape(6,6); Q=sol.y[36:,-1].reshape(6,6)
    return F,fac(Q),float(np.max(abs(F[:4,:4]-expm(width*A))))

def adc(q):
    words=np.rint(q/step).astype(np.int64)
    lo=-(1<<31); hi=(1<<31)-1
    return np.clip(words,lo,hi),(words<lo)|(words>hi)

def window(source,F,L):
    pointer=rng.standard_normal((len(source),2))*np.array([math.sqrt(vQ),math.sqrt(vP)])
    full=np.c_[source,pointer]@F.T+rng.standard_normal((len(source),6))@L.T
    words,over=adc(full[:,4]+read_sd*rng.standard_normal(len(source)))
    return full[:,:4],words,over,pointer[:,1]

def receiver(word0,word1,coin):
    # Only ADC words and fresh integer coin enter; no state, covariance, R or time.
    # p_hat=(word0-word1)*10000/2^27 and a=clip(1/2+p_hat/4,0,1).
    numerator=np.clip((1<<26)+2500*(word0-word1),0,1<<27)
    threshold=numerator>>3
    return np.where(coin<threshold,1,-1).astype(np.int8)

def stat(v):
    v=np.asarray(v,dtype=float)
    return {'mean':float(v.mean()),'MC_standard_error':float(v.std(ddof=1)/math.sqrt(len(v)))}

def paired(a,i):
    return {'actual':stat(a),'ideal':stat(i),'paired_difference':stat(np.asarray(a)-np.asarray(i))}

start=perf_counter()
assert abs(m0@K@m0/2-D0)<1e-12
assert np.max(abs(A@C+C@A.T+np.outer(noise,noise)))<1e-12
raw_clock=rng.exponential(1/rate,N); success=raw_clock<=deadline
T=raw_clock[success]; n=len(T)
R=rng.choice(np.array([-1,1],dtype=np.int8),n)
ae,av=np.linalg.eig(A); coeff=np.linalg.solve(av,m0)
def means(t): return ((np.exp(t[:,None]*ae)*coeff)@av.T).real
source=R[:,None]*means(T)+rng.standard_normal((n,4))@Croot.T
F,L,err=pointer_matrix(b)
s1,w0,o0,P0=window(source,F,L)
actual,w1,o1,P1=window(s1,F,L)
coin=rng.integers(0,1<<coinbits,n,dtype=np.int64)
arm=receiver(w0,w1,coin)
# The counterfactual passive endpoint uses the same Brownian path and initial state.
h=F[:4,5]
passive=actual-P0[:,None]*(F[:4,:4]@h)[None,:]-P1[:,None]*h[None,:]
ideal=passive.copy(); ideal[:,1]=rng.standard_normal(n)
ideal_probability=np.clip(.5+ideal[:,1]/4,0,1)
ideal_arm=np.where(rng.random(n)<ideal_probability,1,-1).astype(np.int8)
# A common finite postlaunch delay and future channel. No free elapsed physical time.
elapsed=logic_time+future_time
Ffuture=expm(elapsed*A); Lfuture=fac(C-Ffuture@C@Ffuture.T)
common_noise=rng.standard_normal((n,4))@Lfuture.T
future_actual=actual@Ffuture.T+common_noise
future_ideal=ideal@Ffuture.T+common_noise
# Third detached pointer supplies an actual finite terminal one-bit outcome.
Fo,Lo,erro=pointer_matrix(outcome_width)
stateA,wordA,overflowA,_=window(future_actual,Fo,Lo)
stateI,wordI,overflowI,_=window(future_ideal,Fo,Lo)
outcome=(wordA<0).astype(np.uint8); outcomeI=(wordI<0).astype(np.uint8)
bad=o0|o1|overflowA
meanT=means(T+2*b)
zidx=[0,2,3]; Cz=C[np.ix_(zidx,zidx)]; hz=meanT[:,zidx]
weight=hz@np.linalg.inv(Cz)
den=np.sqrt(np.sum(weight*hz,axis=1))
scoreA=np.sum(actual[:,zidx]*weight,axis=1)/den
scoreI=np.sum(ideal[:,zidx]*weight,axis=1)/den
p_hat=(w0-w1)*10000/2**27
e_x=math.sqrt(vQ)+b*math.sqrt(vP)/md+read_sd+step/2
drift_bound=math.sqrt(8*(D0+math.log(2)/2))
ep=drift_bound*2*b+math.sqrt(4*b)+2*e_x/ell
backaction=math.sqrt(3*vP/(8*b))
overflow_bound=6*math.exp(-(half_range-2)**2/(2*3))
bound=thermal+ep/4+backaction+2**(-coinbits)+overflow_bound
target_mean=(2*ndtr(2)-1)/2
temporary_bits=256
pointer_temp=vP; pointer_stiffness=vP/vQ; pointer_omega=math.sqrt(pointer_stiffness)
pointer_reset_time=20/pointer_omega
pointer_reset_tv_upper=(1/pointer_temp-1)*math.exp(-40)*41**2/2
report={
 'scope':'Floating finite algorithm/source simulation. No physical waiting, calibration, clock privacy, sensor implementation or precision certification is inferred from Monte Carlo.',
 'attempts':N,'successful_clock_trials':n,'timeouts':int((~success).sum()),'ADC_overflows':int(bad.sum()),
 'source_simulator_only':{'A':A.tolist(),'Gibbs_covariance':C.tolist(),'initial_mean_m0':m0.tolist(),
   'reference_inclusive_initial_KL':D0,'conditional_initial_covariance':'Gibbs',
   'stable_eigenvalues':[[float(x.real),float(x.imag)] for x in ae]},
 'clock':{'rate':rate,'timeout_probability':alpha,'maximum_wait':deadline,
   'expected_occupancy_including_timeout':(1-alpha)/rate,
   'expected_wait_given_success':1/rate-deadline*alpha/(1-alpha),
   'empirical_wait_given_success':float(T.mean()),'density_cap':rate/(1-alpha),
   'execution':'Finite PRNG emulation of the ideal continuous law. This is not a physical bounded-density clock certificate.'},
 'receiver':{'box_width':b,'box_separation':ell,'meter_duration':2*b,'kernel':'raised cosine, integral one',
   'gain':G,'pointer_mass':md,'pointer_variance_Q':vQ,'pointer_variance_P':vP,
   'detached_readout_SD':read_sd,'ADC_bits':bits,'ADC_half_range':half_range,'ADC_step':step,
   'clip_theta':2,'coin_bits':coinbits,'fixed_logic_latency':logic_time,
   'temporary_bits_upper':temporary_bits,'elementary_Boolean_operations_upper_per_label':1024,
   'peak_interaction_coefficient':2/b,'interaction_coefficient_peak_slew':2*math.pi/b**2,
   'future_passive_duration':future_time,'terminal_pointer_width':outcome_width,
   'retained_data':'one arm bit and one terminal outcome bit per successful trial, plus timeout/overflow flags; no fine preparation reading'},
 'theorem_contract':{'thermal_error':thermal,'public_drift_L2_bound':drift_bound,
   'position_error_bound_each':e_x,'momentum_error_bound':ep,'label_metrology_error':ep/4,
   'expected_two_pointer_action':3*vP/b,'pointer_path_TV_bound':backaction,
   'coin_error_bound':2**(-coinbits),'Gaussian_family_overflow_bound':overflow_bound,
   'conditional_success_joint_error_bound_before_hardware_discrepancies':bound,
   'unexecuted_additions':'clock-law error, parameter calibration, pointer preparation/release error, actual logic/routing/reset error, model discrepancy'},
 'diagnostics':{'pointer_source_transition_error':err,'outcome_pointer_transition_error':erro,
   'actual_finite_estimator_MAE':float(np.mean(abs(p_hat-actual[:,1]))),
   'actual_finite_estimator_RMS':float(np.sqrt(np.mean((p_hat-actual[:,1])**2))),
   'ideal_arm_conditional_momentum_mean_magnitude':float(target_mean),
   'arm_balance':paired(arm,ideal_arm),'arm_times_old_reference':paired(arm*R,ideal_arm*R),
   'arm_times_hidden_score':paired(arm*scoreA,ideal_arm*scoreI),
   'reference_times_hidden_score':paired(R*scoreA,R*scoreI),
   'arm_times_launch_momentum':paired(arm*actual[:,1],ideal_arm*ideal[:,1]),
   'causal_contrast_2AY':paired(2*arm.astype(float)*outcome,2*ideal_arm.astype(float)*outcomeI),
   'warning':'These summaries do not verify full hidden/reference TV or the analytic theorem.'},
 'resource_ledger':{'source_initialization':'Supplied Gaussian Gibbs covariance plus fair-reference displacement; factory Hamiltonian/covariance access and preparation/calibration not executed. No receiver access to those data.',
   'source_excess_free_energy_units_kT':D0,
   'pointer_initialization':'Three fresh independent Gaussian pointers per successful trial; sampled in the simulation. A calibrated cold trap/reset service is additional hardware.',
   'pointer_cold_temperature_over_source':pointer_temp,'pointer_trap_stiffness':pointer_stiffness,
   'pointer_critical_damping':2*pointer_omega,
   'illustrative_finite_cold_reset_time_each':pointer_reset_time,
   'cold_reset_TV_bound_from_ambient_same_trap':pointer_reset_tv_upper,
   'pointer_nonequilibrium_free_energy_each_kT':pointer_temp-1-math.log(pointer_temp),
   'reset_status':'Reset-time calculation is an optional cold-OU service contract, not executed refrigerator hardware; finite trap release is not simulated and needs its own bound.',
   'three_pointer_sequential_reset_time_each_trial':3*pointer_reset_time,
   'physical_expected_clock_occupancy_all_attempts':N*(1-alpha)/rate,
   'physical_max_clock_occupancy_all_attempts':N*deadline,
   'physical_meter_time_all_successes':n*(2*b+outcome_width),
   'physical_future_and_logic_time_all_successes':n*(future_time+logic_time),
   'replication':'Monte Carlo uses independent reinitialized source specimens; it does not claim a free retained-source iid campaign.',
   'unexecuted_hardware':['source factory and initial KL calibration','private bounded-density arrival port and calibrated timeout','cold pointer preparation and finite trap release','readout gain/noise/backaction calibration','ADC timing and finite noise band','fresh physical random bits','fixed-deadline logic and routing','isolated temporary-memory reset and protection','terminal outcome pointer/readout','continuous source thermostat and occupancy']},
 'elapsed_computer_seconds':perf_counter()-start,
}
codes=np.zeros(N,dtype=np.uint8)
codes[success]=1+(arm>0).astype(np.uint8)+2*outcome
codes[np.flatnonzero(success)[bad]]=5
np.savez_compressed(ROOT/'retained_records.npz',record=codes)
(ROOT/'results.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'successes':n,'error_bound':bound,'expected_wait':(1-alpha)/rate,
 'hidden_reference_stat':report['diagnostics']['reference_times_hidden_score'],
 'arm_reference_stat':report['diagnostics']['arm_times_old_reference'],
 'contrast':report['diagnostics']['causal_contrast_2AY'],'seconds':report['elapsed_computer_seconds']},indent=2))
