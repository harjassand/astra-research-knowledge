"""Independent dense audit of field, bond-source, and overlap extensions."""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
import json
from pathlib import Path
import numpy as np
from scipy.linalg import eigh
from scipy.special import expit
from audit_local_schur import finite_matrices,pinv_psd,local_theta,local_theta_components
from conditional_decimation import SP,prefactors

def run():
    rng=np.random.default_rng(202611013);records=[]
    for n in [3,5,7,9]:
        for trial in range(3):
            J=rng.uniform(-1.2,1.6,n+1);H=rng.uniform(-.8,.8,n)
            nu=np.exp(rng.uniform(-2,2,n));nu[1::2]*=[1.,.03,1e-4][trial]
            modifiers=np.exp(rng.uniform(-1.2,1.2,(n,2,2)))
            rates=np.empty((n,2,2,2))
            for i in range(n):
                for l,L in enumerate(SP):
                    for s,S in enumerate(SP):
                        for r,R in enumerate(SP):
                            rates[i,l,s,r]=nu[i]*modifiers[i,l,r]*expit(-2*S*(H[i]+J[i]*L+J[i+1]*R))
            F,KS,U,g,spins=finite_matrices(J,rates,H);K=F+KS;P=U@U.T
            Ai=pinv_psd(U.T@KS@U,1);Fi=pinv_psd(F,U.shape[1]);Ki=pinv_psd(K,1)
            Avec=U.T@KS@U;ev,V=eigh(Avec);Aih=(V[:,1:]/np.sqrt(ev[1:]))@V[:,1:].T
            B=(np.eye(len(g))-P)@KS@U
            theta_exact=float(eigh(Aih@B.T@Fi@B@Aih,eigvals_only=True)[-1])
            theta=local_theta_components(J,rates,H);theta_var=local_theta(J,rates,True,H)
            acoef=rng.normal(size=n);bcoef=rng.normal(size=n+1)
            full=np.c_[np.ones(len(g)),spins,np.ones(len(g))]
            raw=spins@acoef+np.sum(full[:,:-1]*full[:,1:]*bcoef[None,:],axis=1)
            raw-=g*g@raw;f=g*raw
            qraw=np.zeros(len(g));vraw=np.zeros(len(g));bterms=np.zeros(len(g))
            gaps=prefactors(rates)
            for i in range(0,n,2):
                L=full[:,i];R=full[:,i+2];x=spins[:,i]
                mean=np.tanh(H[i]+J[i]*L+J[i+1]*R)
                h=acoef[i]+bcoef[i]*L+bcoef[i+1]*R
                gamma=gaps[i,(L>0).astype(int),(R>0).astype(int)]
                qraw+=h*(x-mean);vraw+=h*(x-mean)/gamma
                bterms+=h*h*(1-mean*mean)/gamma
            q=(np.eye(len(g))-P)@f;p=U.T@f
            qerror=float(np.max(np.abs(g*qraw-q)))
            verror=float(np.linalg.norm(g*vraw-Fi@q)/max(np.linalg.norm(Fi@q),1e-300))
            aa=float(p@Ai@p);bb=float(q@Fi@q);bb_local=float((g*g)@bterms)
            vv=g*vraw;cc=float(vv@KS@vv);chi=float(f@Ki@f)
            cross=np.sqrt(max(theta*aa*bb_local,0))
            lower=aa+max(bb_local-cross,0)**2/(bb_local+cc)
            upper=(1+theta)*aa+bb_local+2*cross
            # Fit only the closed nearest-neighbor source family on retained spins.
            ns=(n-1)//2
            slow=np.array([[1 if st>>i&1 else -1 for i in range(ns)] for st in range(1<<ns)])
            source_basis=np.c_[np.ones(len(slow)),slow,slow[:,:-1]*slow[:,1:]]
            gs=U.T@g
            projected_values=(U.T@f)/gs
            residual=projected_values-source_basis@np.linalg.lstsq(source_basis,projected_values,rcond=None)[0]
            gibbs_values=2*np.log(gs)
            gres=gibbs_values-source_basis@np.linalg.lstsq(source_basis,gibbs_values,rcond=None)[0]
            records.append(dict(n=n,trial=trial,theta_exact=theta_exact,theta_components=theta,
                theta_variance=theta_var,theta_pass=bool(theta_exact<=theta*(1+1e-7)),
                q_absolute_error=qerror,v_relative_error=verror,b_relative_error=abs(bb_local/bb-1),
                projected_source_closure_error=float(np.max(abs(residual))),
                projected_Gibbs_closure_error=float(np.max(abs(gres))),
                chi=chi,a=aa,b=bb_local,c=cc,lower=lower,upper=upper,
                bound_pass=bool(lower<=chi*(1+1e-7) and chi<=upper*(1+1e-7))))
    out={'scope':'Independent exact physical finite-state projection; nonzero fields, disordered couplings, arbitrary positive endpoint multipliers, site and bond sources. Floating audit.',
        'all_pass':all(x['theta_pass'] and x['bound_pass'] for x in records),'records':records}
    Path(__file__).with_name('audit_fields_sources_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'all_pass':out['all_pass'],'cases':len(records),
        'maxima':{k:max(x[k] for x in records) for k in ['q_absolute_error','v_relative_error','b_relative_error','projected_source_closure_error','projected_Gibbs_closure_error']}},indent=2))

if __name__=='__main__':run()
