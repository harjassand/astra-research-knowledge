"""Independent synthetic full-current audit of catalytic_cycle72.py.
Thermal-average comparator and capture-off comparator are kept distinct.
"""
from pathlib import Path
import importlib.util
import json
import mpmath as mp
p=Path(__file__).resolve().parents[1]/'invention'/'catalytic_cycle72.py'
s=importlib.util.spec_from_file_location('cycle72',p)
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
mp.mp.dps=55


def stat(Q):
    n=Q.rows; A=Q.T.copy();b=mp.matrix(n,1)
    for j in range(n):A[n-1,j]=1
    b[n-1]=1
    return mp.lu_solve(A,b)


def bias(Q,g,pi=None):
    n=Q.rows
    if pi is None:pi=stat(Q)
    J=sum(pi[i]*g[i] for i in range(n))
    A=Q.copy()
    for i in range(n):
        for j in range(n):A[i,j]+=pi[j]
    h=mp.lu_solve(A,mp.matrix([J-g[i] for i in range(n)]))
    return J,h


def reward_rate(case):
    g=mp.matrix(len(case['states']),1)
    for i,j,kp,km,w,dF,label,site,step in case['edges']:
        if site>=0 and step==5:
            g[i]+=kp;g[j]-=km
    return g


def thermal_certificate(case):
    Q,pi,states=case['Q'],case['pi'],case['states']
    g=reward_rate(case);C=36
    K=[mp.matrix(C,C),mp.matrix(C,C)]
    r=[mp.matrix(C,1),mp.matrix(C,1)]
    mu=mp.matrix(C,1);p1=mp.matrix(C,1)
    for z,state in enumerate(states):
        a=6*state[0]+state[1];v=state[2]
        mu[a]+=pi[z]
        if v:p1[a]+=pi[z]
        r[v][a]=g[z]
        for zz,ss in enumerate(states):
            b=6*ss[0]+ss[1]
            K[v][a,b]+=Q[z,zz]
    gap=mp.mpf(str(case['output']['mode_free_energy_eV']))
    tau=mp.mpf(str(case['output']['thermal_lifetime_s']))
    q=mp.exp(-case['beta']*gap);pstar=q/(1+q);gamma=1/tau
    Kbar=(1-pstar)*K[0]+pstar*K[1]
    rbar=(1-pstar)*r[0]+pstar*r[1]
    pib=stat(Kbar);Jth,h=bias(Kbar,rbar,pib)
    w=r[1]-r[0]+(K[1]-K[0])*h
    J=sum(pi[i]*g[i] for i in range(len(states)))
    shift=sum((p1[i]-pstar*mu[i])*w[i] for i in range(C))
    bath=sum(gamma*(p1[i]-q*(mu[i]-p1[i]))*
             mp.log(p1[i]/(q*(mu[i]-p1[i]))) for i in range(C))
    Vmu=sum(mu[i]*w[i]**2/(4*gamma*(1+q)) for i in range(C))
    Vmax=max(w[i]**2/(4*gamma*(1+q)) for i in range(C))
    affinity=4*mp.mpf(str(case['output']['eta_V']))*case['beta']
    sigma=affinity*J
    kappa=affinity*Vmax/Jth
    return {'J':str(J),'Jth':str(Jth),'difference':str(J-Jth),
        'identity_residual':str(J-Jth-shift),
        'bath_entropy':str(bath),'total_entropy':str(sigma),
        'V_stationary':str(Vmu),'V_max':str(Vmax),
        'squared_shift':str((J-Jth)**2),
        'squared_shift_bound_stationary':str(bath*Vmu),
        'squared_shift_bound_total_max':str(sigma*Vmax),
        'gain_bound_max':str(1+kappa/2+mp.sqrt(kappa+kappa*kappa/4)),
        'actual_gain_over_thermal_comparator':str(J/Jth),
        'max_absolute_reward_sensitivity':str(max(abs(x) for x in w))}


def comparator_change(old,new):
    Q0,Q1=old['Q'],new['Q'];pi1=new['pi']
    g0,g1=reward_rate(old),reward_rate(new)
    J0,h=bias(Q0,g0,old['pi'])
    J1=sum(pi1[i]*g1[i] for i in range(len(pi1)))
    v=g1-g0+(Q1-Q0)*h
    identity=sum(pi1[i]*v[i] for i in range(len(pi1)))
    by_label={}
    for sign,case in ((1,new),(-1,old)):
        for i,j,kp,km,work,dF,label,site,step in case['edges']:
            r=mp.mpf(int(site>=0 and step==5))
            weight=r+h[j]-h[i]
            contribution=sign*(pi1[i]*kp-pi1[j]*km)*weight
            by_label[label]=by_label.get(label,mp.mpf(0))+contribution
    return {'J0':str(J0),'J1':str(J1),'net_change':str(J1-J0),
            'identity_residual':str(J1-J0-identity),
            'changed_channel_contributions':{k:str(v) for k,v in by_label.items()}}


def main():
    out=[]
    for mode in ('modulate','consume'):
        old=m.solve_case(mode=mode,capture='0',fast='100',internal=True)
        new=m.solve_case(mode=mode,capture='1',fast='100',internal=True)
        x={'mode':mode,'thermal_projection':thermal_certificate(new),
           'capture_on_minus_capture_off':comparator_change(old,new)}
        out.append(x);print(json.dumps(x),flush=True)
    p=Path(__file__).with_name('catalytic_poisson_audit_results.json')
    p.write_text(json.dumps(out,indent=2))

if __name__=='__main__':main()
