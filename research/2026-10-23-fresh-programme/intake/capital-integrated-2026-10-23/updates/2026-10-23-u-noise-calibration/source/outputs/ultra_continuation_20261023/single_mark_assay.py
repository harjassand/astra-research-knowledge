"""One scalar inherited instrument: a bounded derivative-moment Krylov assay.
New synthetic independent families; full timestamp regression is the comparator.
"""
from pathlib import Path
import json,time,numpy as np
from paired_assay import conventional,project,J
ROOT=Path(__file__).resolve().parent

def sample(N,a,w,rng):
 t=rng.uniform(0,1,N);u=rng.normal(size=(N,1));b=np.array([.7,.2]);v0=u*b+rng.normal(size=(N,2))@np.linalg.cholesky(np.eye(2)-np.outer(b,b)).T
 co,si=np.cos(w*t),np.sin(w*t);rot=np.column_stack([co*v0[:,0]+si*v0[:,1],-si*v0[:,0]+co*v0[:,1]])
 v=np.exp(-a*t)[:,None]*rot+np.sqrt(1-np.exp(-2*a*t))[:,None]*rng.normal(size=(N,2))
 return t,u+.3*rng.normal(size=(N,1)),v+np.sqrt(.1)*rng.normal(size=(N,2))

def moments(t,u,v):
 weights=[2*np.sin(np.pi*t)**2,2*np.pi*np.sin(2*np.pi*t),4*np.pi**2*np.cos(2*np.pi*t)]
 m=[(w[:,None]*v).T@u/len(t) for w in weights];H0=np.column_stack(m[:2]);H1=np.column_stack(m[1:]);return H1@np.linalg.inv(H0),H0

def exact_kernel(F):
 z,V=np.linalg.eig(F);b=2*np.pi;phi=b*b*(-np.expm1(-z))/(z*(z*z+b*b));return (V*phi)@np.linalg.inv(V)

def main():
 rng=np.random.default_rng(23102624);rows=[];start=time.perf_counter();S=np.array([[.7],[.2]])
 for w in [1.5,8.]:
  F=.7*np.eye(2)+w*J;M0=exact_kernel(F)@S;H0=np.column_stack([M0,F@M0]);H1=np.column_stack([F@M0,F@F@M0]);err=float(np.linalg.norm(H1@np.linalg.inv(H0)-F));assert err<1e-11
  for N in [5000,50000]:
   tests=[]
   for _ in range(6):
    t,u,v=sample(N,.7,w,rng);fw,h= moments(t,u,v);fc,cd=conventional(t,u,v)
    tests.append({'weak_raw_error_F':float(np.linalg.norm(fw-F)),'weak_rotor_projected_error_F':float(np.linalg.norm(project(fw)-F)),'conditional_regression_error_F':float(np.linalg.norm(fc-F)),'Krylov_sigma_float':float(np.linalg.svd(h,compute_uv=False)[-1]),'conditional_regression_evaluations':cd['evaluations']})
   row={'omega':w,'pairs':N,'early_measurements_per_family':1,'late_measurements_per_family':2,'max_late_delay':1,'known_means':0,'exact_reconstruction_error':err,'population_Krylov_sigma':float(np.linalg.svd(H0,compute_uv=False)[-1]),'weak_RMS_projected':float(np.sqrt(np.mean([r['weak_rotor_projected_error_F']**2 for r in tests]))),'conventional_RMS':float(np.sqrt(np.mean([r['conditional_regression_error_F']**2 for r in tests]))),'replicates':tests};rows.append(row);print(json.dumps({k:v for k,v in row.items() if k!='replicates'}),flush=True)
 # Exact uncontrollable full-law obstruction: second coordinate is stationary,
 # independent of U and the first coordinate. It is observed once per family.
 failure={'S':[[.7],[0]],'F1':[[.7,0],[0,1]],'F2':[[.7,0],[0,9]],'stationary_state_covariance':'I for both; diffusion equals F in dX=-F Xdt+sqrt(2F)dW','paired_joint_covariance':'[[VarU,S^T exp(-F^T t)],[exp(-Ft)S,I]] is identical for every t','conclusion':'Every independently sampled destructive-pair data law is identical; second decay rate cannot be inferred without inherited excitation or repeated readout.'}
 (ROOT/'single_mark_results.json').write_text(json.dumps({'seed':23102624,'status':'synthetic; no physical validation or historical priority claim','rows':rows,'exact_uncontrollable_failure':failure,'wall_seconds':time.perf_counter()-start},indent=2)+'\n')
if __name__=='__main__':main()
