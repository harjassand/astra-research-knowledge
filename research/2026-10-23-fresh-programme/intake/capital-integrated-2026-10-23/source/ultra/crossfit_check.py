"""Matched-data cross-fitting check for covariance errors in variables.
This is a finite diagnostic; no consistency or superiority claim.
"""
import json,numpy as np
from pathlib import Path
from research import lyap,design_matrix,covariance_from_draws
ROOT=Path(__file__).resolve().parent;rng=np.random.default_rng(23102620)
row=json.loads((ROOT/'expander_designs.json').read_text())[1];n=8;I=np.eye(n);H=[np.array(h) for h in row['H']];D=[I+sg*h for h in H for sg in [1,-1]]
A=rng.normal(size=(n,n));A*=.75/np.linalg.norm(A,2);g1,g2,c=17.,34.,1.03
C1=[lyap(g1*I-A,g1*c*d) for d in D];C2=lyap(g2*I-A,g1*c*D[0]);B1=lyap(g1*I-A,3*I);B2=lyap(g2*I-A,5*I);R1=.2*I;R2=.3*I

def system(Cs):
 M=design_matrix(Cs)*np.sqrt(len(Cs));M=np.column_stack([M,np.concatenate([2*g1*d.reshape(-1) for d in D+[D[0]]])]);b=np.concatenate([2*g*x.reshape(-1) for g,x in zip([g1]*16+[g2],Cs)]);return M,b

def half(N):
 h0=covariance_from_draws(B1+R1,N,rng);cs=[covariance_from_draws(B1+R1+x,N,rng)-h0 for x in C1]
 h02=covariance_from_draws(B2+R2,N,rng);cs.append(covariance_from_draws(B2+R2+C2,N,rng)-h02);return cs
rows=[]
for rep in range(8):
 cs1,cs2=half(5000),half(5000);M1,b1=system(cs1);M2,b2=system(cs2)
 M,b=(M1+M2)/2,(b1+b2)/2;ols=np.linalg.lstsq(M,b,rcond=None)[0]
 G=(M1.T@M2+M2.T@M1)/2;h=(M1.T@b2+M2.T@b1)/2
 iv=np.linalg.solve(G,h);rows.append({'OLS_A_error_F':float(np.linalg.norm(ols[:-1].reshape(n,n)-A)),'OLS_gain':float(ols[-1]),'crossfit_A_error_F':float(np.linalg.norm(iv[:-1].reshape(n,n)-A)),'crossfit_gain':float(iv[-1]),'crossfit_Gram_min_eigen':float(np.linalg.eigvalsh(G)[0])})
out={'seed':23102620,'total_snapshots_each':190000,'replicates':8,'rows':rows,'OLS_RMS_A_error':float(np.sqrt(np.mean([r['OLS_A_error_F']**2 for r in rows]))),'crossfit_RMS_A_error':float(np.sqrt(np.mean([r['crossfit_A_error_F']**2 for r in rows]))),'OLS_gain_mean':float(np.mean([r['OLS_gain'] for r in rows])),'crossfit_gain_mean':float(np.mean([r['crossfit_gain'] for r in rows])),'true_gain':c,'interpretation':'Independent covariance halves make cross-products unbiased at the true parameters, but inversion can be unstable. This selected model, finite repetitions and different seed do not establish finite-sample advantage or hardware usefulness.'};(ROOT/'crossfit_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
