"""Conservative simultaneous Gaussian covariance uncertainty, then abstention."""
from pathlib import Path
import json,numpy as np
from research import lyap,covariance_from_draws,design_matrix
ROOT=Path(__file__).resolve().parent;rng=np.random.default_rng(23102621);n=8;K=19;alpha=.05;N=10000;I=np.eye(n)
H=[np.array(h) for h in json.loads((ROOT/'expander_designs.json').read_text())[1]['H']];Ds=[I+s*h for h in H for s in [1,-1]]
A=rng.normal(size=(n,n));A*=.75/np.linalg.norm(A,2);g1,g2,c=17.,34.,1.03
B1=lyap(g1*I-A,3*I)+.2*I;B2=lyap(g2*I-A,5*I)+.3*I
obs=[B1]+[B1+lyap(g1*I-A,g1*c*d) for d in Ds]+[B2,B2+lyap(g2*I-A,g1*c*Ds[0])]
S=[covariance_from_draws(x,N,rng) for x in obs];delta=np.sqrt(8*np.log(2*K*n*n/alpha)/(N-1));assert delta<1
es=[float(delta/(1-delta)*np.sqrt((n*np.sum(np.diag(s)**2)+np.trace(s)**2)/2)) for s in S]
Cs=[s-S[0] for s in S[1:17]]+[S[18]-S[17]];eps=[e+es[0] for e in es[1:17]]+[es[18]+es[17]]
M=design_matrix(Cs);M=np.column_stack([M,np.concatenate([2*d.reshape(-1) for d in Ds+[Ds[0]]])/np.sqrt(17)]);sv=float(np.linalg.svd(M,compute_uv=False)[-1]);eta=float(2*np.sqrt(np.mean(np.square(eps))))
assert eta>sv
out={'seed':23102621,'alpha':alpha,'total_snapshots':K*N,'regimes':K,'per_regime_N':N,'delta':float(delta),'individual_spectral_error_bounds':es,'eta':eta,'measured_joint_singular_float':sv,'decision':'ABSTAIN','reason':'Uncertainty eta exceeds the measured smallest singular value. No rigorous positive singular lower bound or recovery claim is asserted.','assumptions':'Independent Gaussian snapshots, exact noise shapes and calibrated damping increment; shared-baseline correlation handled by simultaneous union event.'};(ROOT/'confidence_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='individual_spectral_error_bounds'}))
