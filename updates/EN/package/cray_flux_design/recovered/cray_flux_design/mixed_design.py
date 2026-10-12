"""Mixed-probe continuation: experimentally measured flux basis, not a hidden generator.

The prototype checks the derived mixed-probe algebra and a noisy, initially rare
pathway. Its confidence LP is floating point (unlike the primary single-probe
benchmark's exact rational dual certificate). Automatic acquisition of a uniformly
well-conditioned probe basis on all hidden networks is NOT established.
"""
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from scipy.linalg import solve
from fractions import Fraction
from random import Random
import json
from benchmark import matrices,stationary,true_optimum
from opaque_assay import generate_instance
from rational_confidence import upper_log_integer,upper_sqrt

ROOT=Path(__file__).resolve().parent

def compile_mixed(z0,w0,D,df,R,U,rho,activity,eta=0.,eta_r=0.):
    k=len(z0);inv=np.linalg.inv(R);kappa=float(np.linalg.norm(inv,1))
    H=D@inv;g=df@inv
    eh=(2*eta+k*eta_r/rho)*kappa
    # x=(beta,z); all beta >=0, unlike signed mixture coefficients.
    A=[];b=[]
    for i in range(k):
        row=np.zeros(2*k);row[:k]=-H[i]-eh;row[k+i]=1;A.append(row);b.append(z0[i]+eta)
        row=np.zeros(2*k);row[:k]= H[i]-eh;row[k+i]=-1;A.append(row);b.append(-z0[i]+eta)
    for i in range(k):
        row=np.zeros(2*k);row[i]=1;row[k+i]=-U[i];A.append(row);b.append(0.)
    row=np.zeros(2*k);row[:k]=1;A.append(row);b.append(activity)
    c=np.r_[g+eh,np.zeros(k)]
    result=linprog(-c,A_ub=A,b_ub=b,bounds=[(0,activity)]*k+[(0,1)]*k,method='highs')
    if not result.success:raise RuntimeError(result.message)
    beta=result.x[:k];z=result.x[k:]
    rates=np.divide(beta,z,out=np.zeros(k),where=z>1e-14)
    rates=np.minimum(U,np.maximum(0,rates))
    return dict(H=H,g=g,kappa=kappa,H_entry_error=eh,
                floating_upper=min(1.,w0+eta-result.fun),rates=rates,
                alpha_inverse=inv)

def exact_tests():
    rng=np.random.default_rng(210346);maxerr=0.;out=[]
    for idx in range(20):
        k=2+idx%4;inst=generate_instance(37+idx,k,912001+idx,background_rate=1,reset_rate=1)
        pre=matrices(inst);U=np.repeat(7.,k);p0=stationary(inst,np.zeros(k),pre)
        probes=rng.uniform(.05,7.,(k,k));probs=[stationary(inst,u,pre) for u in probes]
        R=np.array([u*p[:k] for u,p in zip(probes,probs)]).T
        D=np.array([p[:k]-p0[:k] for p in probs]).T;df=np.array([inst.reward@(p-p0) for p in probs])
        fit=compile_mixed(p0[:k],inst.reward@p0,D,df,R,U,1,2)
        val=inst.reward@stationary(inst,fit['rates'],pre);truth=true_optimum(inst,U,pre)
        err=max(abs(val-truth),abs(fit['floating_upper']-truth));maxerr=max(maxerr,err)
        assert err<1e-8
        out.append(dict(seed=912001+idx,k=k,basis_inverse_one_norm=fit['kappa'],error=float(err)))
    return dict(cases=20,max_error=float(maxerr),instances=out)

def rare_basis_test():
    # State 0=a1, 1=a2, 2=bridge, 3=success. nu=e0; rho=bg bound=1.
    # Background: 0->1 at eta=2^-30, 2->1 at 1, other uniformisation events self.
    # Controls 0->2 and 1->3. Each ejects outside {0,1}; all targets have unique
    # stationary distributions because the independent global reset is retained.
    rare=Fraction(1,2**30);n=300000;cap=100
    def assay(u,seed):
        rng=Random(seed);rr=rng.randrange;source=[0,0];flux=[0,0];reward=0
        for _ in range(n):
            s=0
            while True:
                rate=u[s] if s<2 else 0;e=rr(2+rate)
                if e==0:
                    if s<2:source[s]+=1
                    reward+=int(s==3);break
                if e==1:
                    if s==0 and rr(2**30)==0:s=1
                    elif s==2:s=1
                else:flux[s]+=1;s=2 if s==0 else 3
        return np.r_[source,reward]/n,np.array(flux)/n,dict(source_counts=source,reward_sum=reward,tagged_counts=flux)
    def truth(u):
        L=np.zeros((4,4));L[1,0]=float(rare);L[0,0]-=float(rare);L[1,2]=1;L[2,2]-=1
        L[2,0]+=u[0];L[0,0]-=u[0];L[3,1]+=u[1];L[1,1]-=u[1]
        return solve(np.eye(4)-L,np.array([1.,0,0,0]))
    basis_u=[[cap,0],[cap,cap]];vals=[];flux=[];raw=[]
    for j,u in enumerate([[0,0]]+basis_u):
        v,r,d=assay(u,41371+j);vals.append(v);raw.append(d)
        if j:flux.append(r)
    vals=np.array(vals);R=np.array(flux).T;D=(vals[1:,:2]-vals[0,:2]).T;df=vals[1:,2]-vals[0,2]
    t=upper_log_integer(Fraction(2*((2+1)**2+2**2),1)/Fraction(1,100))
    em=float(upper_sqrt(Fraction(t,2*n)));er=float(2*(2*upper_sqrt(Fraction(t,n))+Fraction(t,n)))
    fit=compile_mixed(vals[0,:2],vals[0,2],D,df,R,np.repeat(cap,2),1,2,em,er)
    iso=truth([0,cap]);isolated_flux=cap*iso[1]
    exact_R=np.array([np.array(u)*truth(u)[:2] for u in basis_u]).T
    return dict(hidden_bottleneck_rate=str(rare),episodes_per_setting=n,
        total_episodes=3*n,probe_controls=basis_u,measured_flux_matrix=R.tolist(),
        exact_mixed_flux_matrix=exact_R.tolist(),measured_inverse_one_norm=fit['kappa'],
        isolated_second_control_true_flux=float(isolated_flux),
        expected_tagged_events_in_isolated_second_probe=n*float(isolated_flux),
        mixed_second_control_true_flux=float(exact_R[1,1]),
        mixed_second_control_observed_flux=float(R[1,1]),
        coefficient_error_bound=fit['H_entry_error'],floating_optimistic_upper=fit['floating_upper'],
        proposed_rates=fit['rates'].tolist(),truth_at_proposal=float(truth(fit['rates'])[3]),
        raw_summaries=raw,
        status='Acquired well-conditioned mixed basis and conservative confidence LP. No general basis-discovery theorem or exact rational mixed-LP dual replay is claimed.')

if __name__=='__main__':
    data=dict(exact=exact_tests(),rare=rare_basis_test())
    (ROOT/'mixed_results.json').write_text(json.dumps(data,indent=2))
    print(json.dumps({**data,'exact':{k:v for k,v in data['exact'].items() if k!='instances'}},indent=2))
