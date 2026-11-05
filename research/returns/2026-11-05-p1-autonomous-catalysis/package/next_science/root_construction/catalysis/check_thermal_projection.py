"""Check thermal projection on a separately built synthetic reversible model.
This is not a fit or empirical validation of the PtCo mechanism.
"""
from pathlib import Path
import importlib.util
import json
import math
import mpmath as mp
from scipy.optimize import minimize_scalar

HERE=Path(__file__).resolve().parent
modelpath=HERE.parent.parent/'invention'/'catalytic_cycle72.py'
spec=importlib.util.spec_from_file_location('cycle72',modelpath)
model=importlib.util.module_from_spec(spec)
spec.loader.exec_module(model)
mp.mp.dps=55
M=mp.mpf

def invariant(Q):
    n=Q.rows; A=Q.T.copy(); rhs=mp.matrix(n,1)
    for j in range(n): A[n-1,j]=1
    rhs[n-1]=1
    return mp.lu_solve(A,rhs)

def analyze(fast,capture):
    obj=model.solve_case(mode='consume',fast=fast,capture=capture,internal=True)
    states=obj['states']; pi=obj['pi']; edges=obj['edges']
    nchem=len(states)//2
    K=[mp.matrix(nchem,nchem),mp.matrix(nchem,nchem)]
    r=[mp.matrix(nchem,1),mp.matrix(nchem,1)]
    entropy=entropy_gate=M(0)
    for x,y,kp,km,work,dF,label,site,step in edges:
        i,g=x//2,states[x][2]; j,gg=y//2,states[y][2]
        if label!='thermal':
            if i!=j:
                K[g][i,j]+=kp; K[g][i,i]-=kp
                K[gg][j,i]+=km; K[gg][j,j]-=km
            if step==0:
                r[g][i]+=kp; r[gg][j]-=km
        fp,fr=pi[x]*kp,pi[y]*km
        s=(fp-fr)*mp.log(fp/fr)
        entropy+=s
        if label=='thermal': entropy_gate+=s
    q=mp.exp(-obj['beta']*M('0.126'))
    peq=q/(1+q); gamma=1/M('4.1e-8')
    Kbar=(1-peq)*K[0]+peq*K[1]
    rbar=(1-peq)*r[0]+peq*r[1]
    mubar=invariant(Kbar)
    Jth=sum(mubar[i]*rbar[i] for i in range(nchem))
    A=Kbar.copy(); rhs=mp.matrix([Jth-rbar[i] for i in range(nchem)])
    for j in range(nchem): A[nchem-1,j]=0
    A[nchem-1,nchem-1]=1; rhs[nchem-1]=0
    h=mp.lu_solve(A,rhs)
    w=r[1]-r[0]+(K[1]-K[0])*h
    mu=[pi[2*i]+pi[2*i+1] for i in range(nchem)]
    delta=[pi[2*i+1]/mu[i]-peq for i in range(nchem)]
    J=sum(pi[2*i]*r[0][i]+pi[2*i+1]*r[1][i] for i in range(nchem))
    correction=sum(mu[i]*delta[i]*w[i] for i in range(nchem))
    identity_error=J-Jth-correction
    assert abs(identity_error)<M('1e-35')
    coeff=[w[i]**2/(4*gamma*(1+q)) for i in range(nchem)]
    Vmu=sum(mu[i]*coeff[i] for i in range(nchem)); Vmax=max(coeff)
    gap=abs(J-Jth)
    assert gap**2<=entropy_gate*Vmu+M('1e-35')
    assert entropy_gate<=entropy+M('1e-35')
    affinity=4*M('.3')*obj['beta']
    assert abs(entropy-affinity*J)<M('1e-35')
    kappa=affinity*Vmax/Jth
    gbound=1+kappa/2+mp.sqrt(kappa+kappa**2/4)
    assert J/Jth<=gbound+M('1e-35')
    pf=float(peq)
    def ratio(p):
        if abs(p-pf)<1e-9: return pf*(1-pf)
        return (p-pf)/(math.log(p/(1-p))-math.log(pf/(1-pf)))
    opt=minimize_scalar(lambda p:-ratio(p),bounds=(1e-12,1-1e-12),method='bounded')
    csharp=-float(opt.fun)
    sharpkappa=kappa*M(str(csharp*4))
    sharpbound=1+sharpkappa/2+mp.sqrt(sharpkappa+sharpkappa**2/4)
    return {'synthetic':True,'other_forward_rate_s-1':float(fast),'capture_fraction':float(capture),
         'actual_total_current_s-1':float(J),'thermal_projected_total_current_s-1':float(Jth),
         'actual_over_thermal_projected_gain':float(J/Jth),
         'exact_response_identity_error':str(identity_error),
         'entropy_total_kB_s-1':float(entropy),'entropy_gate_kB_s-1':float(entropy_gate),
         'V_weighted_s-1':float(Vmu),'V_max_s-1':float(Vmax),
         'current_difference_s-1':float(J-Jth),
         'bound_abs_difference_using_gate_entropy_and_mu_s-1':float(mp.sqrt(entropy_gate*Vmu)),
         'bound_abs_difference_using_total_entropy_and_Vmax_s-1':float(mp.sqrt(entropy*Vmax)),
         'a_priori_gain_upper_bound_Pinsker':float(gbound),
         'binary_coefficient_sharp_numerical':csharp,
         'binary_coefficient_maximizing_conditional_occupation':float(opt.x),
         'a_priori_gain_upper_bound_sharper_binary_constant':float(sharpbound),
         'max_complete_cycle_response_contrast_s-1':float(max(abs(v) for v in w))}

if __name__=='__main__':
    cases=[]
    for fast in ('100','1e6'):
        for cap in ('0','1'):
            out=analyze(fast,cap); cases.append(out); print(json.dumps(out),flush=True)
    (HERE/'thermal_projection_checks.json').write_text(json.dumps({
        'status':'mathematical checks on independently constructed synthetic reversible model; not empirical validation',
        'cases':cases},indent=2))
