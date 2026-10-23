"""Analytic calibration alias and competent diagonal comparator, finite checks."""
import json,numpy as np
from pathlib import Path
from research import lyap,decode,design_matrix
ROOT=Path(__file__).resolve().parent
rows=json.loads((ROOT/'expander_designs.json').read_text());rng=np.random.default_rng(20261024);out={}
for row in rows:
 n=row['n'];q=(n-1).bit_length();I=np.eye(n)
 H=[np.diag([1 if ((i>>j)&1) else -1 for i in range(n)]) for j in range(q)]
 D=[I+sign*h for h in H for sign in [1,-1]]
 # At zero target drift, measured response covariance equals D exactly.
 # Pair distance >= 1/q => ideal sigma_min >= min(2,2/sqrt(q)).
 s=float(np.linalg.svd(design_matrix(D),compute_uv=False)[-1]) if n<=16 else None
 out[f'diagonal_n{n}']={'noise_settings':2*q,'settings_with_baseline':2*q+1,'s0_analytic_lower':min(2.,2/np.sqrt(q)),'measured_sigma_float':s,'noncommuting_noise_settings':16,'conclusion':'Diagonal masks use fewer settings at every tested dimension; no observed setting-count advantage.'}
row=rows[1];n=row['n'];I=np.eye(n);H=[np.array(h) for h in row['H']];D=[I+sign*h for h in H for sign in [1,-1]]
X=rng.standard_normal((n,n));A=(X-X.T);A*=.5/np.linalg.norm(A,2);gamma=17.;F=gamma*I-A;delta=.01;c=1+delta
C=[lyap(F,gamma*c*d) for d in D]
A_alias=gamma*I-F/c
A_fit,s,res=decode(C,D,gamma)
assert np.linalg.norm(A_fit-A_alias)<1e-10
assert np.linalg.norm(A_alias,2)<1 and np.linalg.norm(A,2)<1
Cbase=lyap(F,gamma*I);Cbase_alias=lyap(F/c,gamma*I/c)
assert np.linalg.norm(Cbase-Cbase_alias)<1e-12
out['common_actuator_gain_alias']={'n':n,'actual_gain':c,'assumed_gain':1,'gamma':gamma,'A_true_norm2':float(np.linalg.norm(A,2)),'A_alias_norm2':float(np.linalg.norm(A_alias,2)),'drift_error_F':float(np.linalg.norm(A_fit-A)),'fitted_residual':res,'fitted_sigma_min':s,'alias_identity':'A_alias=gamma I-(gamma I-A)/(1+delta)','alternative_background_diffusion':'Q_background_alias=Q_background/(1+delta)','baseline_covariance_mismatch':float(np.linalg.norm(Cbase-Cbase_alias)),'conclusion':'Even infinitely many exact snapshots and a zero fitting residual cannot resolve uncalibrated common actuator gain.'}
(ROOT/'adversarial_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
