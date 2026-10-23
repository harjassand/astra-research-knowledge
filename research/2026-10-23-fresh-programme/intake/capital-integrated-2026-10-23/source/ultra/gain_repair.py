"""A second known damping value identifies a common unknown injection gain."""
import json,numpy as np
from pathlib import Path
from research import lyap,decode,design_matrix,covariance_from_draws
ROOT=Path(__file__).resolve().parent
rng=np.random.default_rng(23102619);row=json.loads((ROOT/'expander_designs.json').read_text())[1];n=row['n'];I=np.eye(n);H=[np.array(h) for h in row['H']];D=[I+sg*h for h in H for sg in [1,-1]]
# General real drift, not restricted to skew matrices, held separate from earlier test seed.
A=rng.normal(size=(n,n));A*=.75/np.linalg.norm(A,2)
gamma1,gamma2,c=17.,34.,1.03
C1=[lyap(gamma1*I-A,gamma1*c*d) for d in D]
C2=lyap(gamma2*I-A,gamma1*c*D[0]) # Identical injected amplitude; only damping changes.
Awrong,_,_=decode(C1,D,gamma1);Z=gamma1*I-Awrong
T=2*gamma1*D[0]-Z@C2-C2@Z.T
chat=2*(gamma2-gamma1)*np.sum(C2*C2)/np.sum(T*C2);Arepaired=gamma1*I-chat*Z
assert abs(chat-c)<1e-11 and np.linalg.norm(Arepaired-A)<1e-10

def joint(C1,C2):
 Cs=C1+[C2];Ds=D+[D[0]];gammas=[gamma1]*len(D)+[gamma2]
 M=design_matrix(Cs)*np.sqrt(len(Cs));v=np.concatenate([2*gamma1*d.reshape(-1) for d in Ds]);M=np.column_stack([M,v])
 rhs=np.concatenate([2*g*x.reshape(-1) for g,x in zip(gammas,Cs)])
 sol,_,_,s=np.linalg.lstsq(M,rhs,rcond=None)
 return sol[:-1].reshape((n,n)),float(sol[-1]),float(s[-1]),float(np.linalg.norm(M@sol-rhs))
Aj,cj,sj,rj=joint(C1,C2);assert np.linalg.norm(Aj-A)<1e-10 and abs(cj-c)<1e-11
# Unknown background and readout covariances may differ between damping levels,
# but are common within the baseline/probe pair at that level.
B1=lyap(gamma1*I-A,3*I);B2=lyap(gamma2*I-A,5*I)
R1=.2*I;R2=.3*I;Nper=10000;raw=[]
for repeat in range(6):
 h0=covariance_from_draws(B1+R1,Nper,rng)
 C1hat=[covariance_from_draws(B1+R1+x,Nper,rng)-h0 for x in C1]
 h02=covariance_from_draws(B2+R2,Nper,rng)
 C2hat=covariance_from_draws(B2+R2+C2,Nper,rng)-h02
 ah,ch,ss,res=joint(C1hat,C2hat);raw.append({'A_error_F':float(np.linalg.norm(ah-A)),'gain_estimate':ch,'fit_residual':res,'smallest_unscaled_joint_singular':ss})
out={'status':'conditional exact construction plus synthetic checks; unreviewed','n':n,'gamma1':gamma1,'gamma2':gamma2,'true_gain':c,'closed_form_gain':chat,'closed_form_drift_error_F':float(np.linalg.norm(Arepaired-A)),'joint_gain':cj,'joint_drift_error_F':float(np.linalg.norm(Aj-A)),'joint_residual':rj,'settings_including_two_baselines':19,'same_injected_noise_amplitude_at_both_damping_values':True,'raw_total_snapshots_each_repeat':19*Nper,'raw_repeats':raw,'raw_RMS_drift_error_F':float(np.sqrt(np.mean([r['A_error_F']**2 for r in raw]))),'raw_RMS_gain_error':float(np.sqrt(np.mean([(r['gain_estimate']-c)**2 for r in raw]))),'requirements':['One common positive injection gain across all noise settings and damping levels','Known absolute damping increment gamma2-gamma1','All drift changes under the damping intervention exactly -delta_gamma I','Independent, intervention-stationary additive readout noise within each local baseline/probe pair','Full state readout; stable linear model; covariance acquisition'],'physical_acquisition':'UNKNOWN'}
(ROOT/'gain_repair_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
