"""Reproducible synthetic checks of a conditional lineage-moment identity.

All generated samples are simulations, not measurements of biological cells.
Requires Python 3, numpy, scipy, sympy. Run: python investigate.py
No network access is used. Outputs JSON containing exact-model predictions
and independent-lineage Monte Carlo estimates with standard errors.
"""
from __future__ import annotations
import json
import math
from pathlib import Path
from typing import Any
import numpy as np
from scipy.special import poch

SEED = 20261009
N_LINEAGES = 2048
N_GENERATIONS = 4096
BURN_IN = 128
MAX_LAG = 5


def model_moments(alpha: float | None, shape: float = 4.0) -> dict[str, Any]:
    """Stationary raw moments for R~Beta(alpha,alpha), Delta~Gamma(shape,1/shape).
    alpha=None denotes deterministic R=1/2. R and Delta are independent.
    """
    r = [1.0] + [(0.5 ** k if alpha is None else float(poch(alpha,k)/poch(2*alpha,k))) for k in range(1,4)]
    d = [float(poch(shape,k)/shape**k) for k in range(4)]
    raw = [1.0]
    for k in range(1,4):
        raw.append(r[k] * sum(math.comb(k,j)*raw[j]*d[k-j] for j in range(k)) / (1-r[k]))
    mu=raw[1]; var=raw[2]-mu*mu; skew=raw[3]-3*mu*raw[2]+2*mu**3
    a,q=r[1],r[2]
    b=mu*(q/a-a) # E[R eta], eta=R(Delta+mu)-mu
    amplitude=skew-2*b*var/(a-q)
    J=[amplitude*(a**k-q**k) for k in range(1,MAX_LAG+1)]
    return dict(mean=mu,variance=var,third_central_moment=skew,a=a,q=q,
                partition_variance=q-a*a,amplitude=amplitude,
                C=[var*a**k for k in range(1,MAX_LAG+1)],J=J)


def ratio_with_se(u: np.ndarray, v: np.ndarray) -> dict[str,float]:
    """Delta-method SE using independent lineages as sampling units."""
    um=float(u.mean());vm=float(v.mean())
    if abs(vm) < 1e-15:
        return dict(value=float('nan'),se=float('nan'))
    z=um/vm
    influence=(u-z*v)/vm
    return dict(value=z,se=float(influence.std(ddof=1)/np.sqrt(len(u))))


def summarize(C: np.ndarray,J: np.ndarray) -> dict[str,Any]:
    # C and J have axes (lag, independent lineage).
    a=ratio_with_se(C[1],C[0]);s=ratio_with_se(J[1],J[0])
    jmean=J.mean(axis=1);cmean=C.mean(axis=1)
    jse=J.std(axis=1,ddof=1)/np.sqrt(C.shape[1])
    out=dict(C=cmean.tolist(),J=jmean.tolist(),J_se=jse.tolist(),
             a_hat=a['value'],a_se=a['se'],sum_roots_hat=s['value'],sum_roots_se=s['se'])
    # q=s-a; Var(R)=s-a-a^2. Do not clip unphysical estimates.
    out['q_hat']=s['value']-a['value']
    out['partition_variance_hat']=s['value']-a['value']-a['value']**2
    da=(C[1]-a['value']*C[0])/cmean[0]
    ds=(J[1]-s['value']*J[0])/jmean[0]
    influence=ds-(1+2*a['value'])*da
    out['partition_variance_se']=float(influence.std(ddof=1)/np.sqrt(C.shape[1]))
    # Held-out lag 3 prediction determined from lags 1 and 2.
    ah=a['value'];qh=out['q_hat']
    residual=J[2]-(ah+qh)*J[1]+ah*qh*J[0]
    out['lag3_residual']=float(residual.mean())
    # Not an inferential SE: fitted-parameter effects are not included here.
    return out


def simulate_case(alpha:float|None, inherited:bool=False, noise_kind:str='none', seed:int=SEED) -> dict[str,Any]:
    rng=np.random.default_rng(seed)
    B=np.ones(N_LINEAGES)
    added=np.ones(N_LINEAGES)
    C=np.zeros((MAX_LAG,N_LINEAGES));J=np.zeros_like(C)
    H=np.zeros_like(C);K=np.zeros_like(C);F=np.zeros_like(C)
    old2sum=np.zeros_like(C); new2sum=np.zeros_like(C)
    history=np.zeros((MAX_LAG+1,N_LINEAGES))
    n_pairs=0
    for t in range(BURN_IN+N_GENERATIONS+MAX_LAG):
        innovation=rng.gamma(4.0,0.25,N_LINEAGES)
        if inherited:
            added=0.65*added+0.35*innovation
        else:
            added=innovation
        R=0.5 if alpha is None else rng.beta(alpha,alpha,N_LINEAGES)
        B=R*(B+added)
        if noise_kind=='gaussian':
            error=rng.normal(0.0,0.2,N_LINEAGES)
        elif noise_kind=='skewed':
            error=rng.exponential(0.2,N_LINEAGES)-0.2
        else:
            error=0.0
        # Mean 1 is known in each generating model; no estimated centering bias.
        y=B+error-1.0
        slot=t%(MAX_LAG+1)
        history[slot]=y
        if t >= BURN_IN+MAX_LAG:
            for k in range(1,MAX_LAG+1):
                old=history[(t-k)%(MAX_LAG+1)]
                C[k-1]+=old*y
                hh=old*y*y; kk=old*old*y
                H[k-1]+=hh; K[k-1]+=kk
                F[k-1]+=old*old*y*y
                old2sum[k-1]+=old*old; new2sum[k-1]+=y*y
                J[k-1]+=kk-hh
            n_pairs+=1
    C/=n_pairs;J/=n_pairs;H/=n_pairs;K/=n_pairs;F/=n_pairs
    # Center squares with a global second-moment estimate, not per-lineage
    # mean subtraction (which introduces an O(1/length) covariance bias).
    e2=float((old2sum[0]+new2sum[0]).mean()/(2*n_pairs))
    F=F-e2*(old2sum+new2sum)/n_pairs+e2*e2
    out=summarize(C,J)
    # Reconstruct q from the two-observable lag matrix.
    c,h,kk,ff=[z.mean(axis=1) for z in (C,H,K,F)]
    den=c[0]*ff[0]-kk[0]*h[0]
    num=c[0]*ff[1]-kk[0]*h[1]
    qm=num/den
    # Delta-method influence, independent lineages. Centering squares'
    # nuisance derivative vanishes at the true stationary mean.
    dden=ff[0]*(C[0]-c[0])+c[0]*(F[0]-ff[0])-h[0]*(K[0]-kk[0])-kk[0]*(H[0]-h[0])
    dnum=ff[1]*(C[0]-c[0])+c[0]*(F[1]-ff[1])-h[1]*(K[0]-kk[0])-kk[0]*(H[1]-h[1])
    dq=(dnum-qm*dden)/den
    ah=c[1]/c[0]
    da=(C[1]-ah*C[0])/c[0]
    v=qm-ah*ah
    dv=dq-2*ah*da
    out['matrix_q_hat']=float(qm)
    out['matrix_q_se']=float(dq.std(ddof=1)/np.sqrt(N_LINEAGES))
    out['matrix_partition_variance_hat']=float(v)
    out['matrix_partition_variance_se']=float(dv.std(ddof=1)/np.sqrt(N_LINEAGES))
    out['matrix_denominator']=float(den)
    out['H']=h.tolist();out['K']=kk.tolist();out['F']=ff.tolist()
    matrices=[np.array([[c[i],h[i]],[kk[i],ff[i]]]) for i in range(MAX_LAG)]
    pencil=np.linalg.solve(matrices[0],matrices[1])
    defect=matrices[2]-matrices[1]@pencil
    out['full_matrix_pencil']=pencil.tolist()
    out['lag3_matrix_defect_relative']=float(np.linalg.norm(defect)/np.linalg.norm(matrices[2]))
    out['C_successive_ratios']=(c[1:]/c[:-1]).tolist()
    out.update(alpha=alpha,inherited=inherited,noise_kind=noise_kind,n_lineages=N_LINEAGES,
               pairs_per_lineage=n_pairs,seed=seed)
    out['iid_model_prediction']=model_moments(alpha) if not inherited else None
    return out


def algebra_checks() -> dict[str,Any]:
    import sympy as s
    a,q,b,V,m=s.symbols('a q b V m',nonzero=True)
    H=m;K=m;C=V
    diff=[]
    amp=m-2*b*V/(a-q)
    for k in range(1,6):
        H=s.expand(q*H+2*b*C);K=a*K;C=a*C
        diff.append(s.simplify((K-H)-amp*(a**k-q**k))==0)
    assert all(diff)
    alpha=s.symbols('alpha',positive=True)
    # Symmetric beta-gamma reversible example, Gamma(alpha,1/alpha) sizes.
    qrev=(alpha+1)/(2*(2*alpha+1))
    brev=2*qrev-s.Rational(1,2)
    arev=s.simplify(2/alpha**2-2*brev*(1/alpha)/(s.Rational(1,2)-qrev))
    assert arev==0
    # Exact lag-penciling check without distribution-specific substitutions.
    W=s.symbols('W')
    Sigma=s.Matrix([[V,m],[m,W]])
    Tt=s.Matrix([[a,2*b],[0,q]])
    M1=Sigma*Tt;M2=Sigma*Tt**2
    assert s.simplify(M1.inv()*M2-Tt)==s.zeros(2)
    return dict(cubic_identity_lags_1_to_5=diff,beta_gamma_amplitude=str(arev),lag_pencil_identity=True)


def main() -> None:
    results={'status':'SYNTHETIC_MODEL_CHECKS_ONLY','seed':SEED,'algebra':algebra_checks(),'cases':{}}
    specs=[('fixed_partition',None,False,'none'),('random_partition',20.0,False,'none'),
           ('random_partition_gaussian_noise',20.0,False,'gaussian'),
           ('random_partition_skewed_noise',20.0,False,'skewed'),
           ('reversible_beta_gamma',4.0,False,'none'),
           ('inherited_additions',20.0,True,'none')]
    for i,(name,alpha,inherited,noise) in enumerate(specs):
        out=simulate_case(alpha,inherited,noise,SEED+i)
        results['cases'][name]=out
        print(name,'a=',round(out['a_hat'],6),'q=',round(out['q_hat'],6),
              'varR=',round(out['partition_variance_hat'],6),
              'SE=',round(out['partition_variance_se'],6),
              'MATRIX_VAR=',round(out['matrix_partition_variance_hat'],6),
              'MATRIX_SE=',round(out['matrix_partition_variance_se'],6),flush=True)
    path=Path(__file__).with_name('validation_results.json')
    path.write_text(json.dumps(results,indent=2)+'\n')
    print(path)

if __name__=='__main__':
    main()
