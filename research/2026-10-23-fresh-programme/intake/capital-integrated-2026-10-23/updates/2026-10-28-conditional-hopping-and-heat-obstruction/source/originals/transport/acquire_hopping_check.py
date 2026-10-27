from pathlib import Path
import numpy as np,math,json
OUT=Path(__file__).parent
amax=1.25;dmax=2.1;detmax=8.;L=2*amax+dmax+detmax;tau=1/(4*L);eps=.01;M=4;failure=.01;delta=tau*eps/3

def expm(A):
 ans=np.eye(3);term=ans.copy()
 for k in range(1,60):term=term@A/k;ans+=term
 return ans

def logm_near_identity(M):
 X=M-np.eye(3);ans=np.zeros((3,3));power=np.eye(3)
 for k in range(1,120):power=power@X;ans+=((-1)**(k+1)/k)*power
 return ans
rng=np.random.default_rng(271027);worst=0.
for k in range(1000):
 a=rng.uniform(.75,amax);d=rng.uniform(1.9,dmax);Delta=rng.uniform(-detmax,detmax)
 K=np.array([[-d,-Delta,0],[Delta,-d,2*a],[0,-2*a,0]])
 transition=expm(tau*K);assert np.linalg.norm(transition-np.eye(3),2)<=math.exp(.25)-1+1e-12
 observed=transition+rng.uniform(-delta,delta,size=(3,3));assert np.linalg.norm(observed-np.eye(3),2)<.5
 acquired=logm_near_identity(observed)/tau;estimate=-acquired[2,1]/2
 err=abs(estimate-a);assert err<=eps+1e-10;worst=max(worst,err)
 bound=np.linalg.norm(observed-transition,2)/tau;assert err<=bound+1e-10
shots=math.ceil(2/delta**2*math.log(18*M/failure))
rec={'status':'NUMERICAL_DIAGNOSTIC_PASS','random_cases':1000,'maximum_amplitude_error':worst,'uniform_theorem_error':eps,'L':L,'tau':tau,'total_mean_error_budget':delta,'shots_per_setting_if_all_budget_statistical':shots,'settings':9*M,'total_shots_if_all_budget_statistical':shots*9*M,'caution':'No acquisition performed. Preparation/readout/switching/timing biases must be reserved inside delta. Structure/locality/Markovianity and support-complete isolation are premises.'}
(OUT/'HOPPING_ASSAY_CHECKS.json').write_text(json.dumps(rec,indent=2)+'\n');print(json.dumps(rec,indent=2))
