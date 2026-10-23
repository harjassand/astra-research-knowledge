"""Exact fixed-power contact elimination for actual_contacts.py's TE model.

All numbers are per combined area as passed to that incumbent model.
No material or non-constant-ZT claims. The old code is imported read-only.
"""
import json, math, sys, time
from pathlib import Path
import numpy as np
from scipy.optimize import brentq, minimize_scalar

H0=2111.152; C0=4813.078; TH0=348.; TC0=338.; ZT0=1.2

def roots_at_power(P,m,H=H0,C=C0,TH=TH0,TC=TC0,zt=ZT0):
    """Return every physical positive-temperature-drop K root at fixed P,m."""
    S=H+C; u=C/S; v=H/S; L=H*C/S; D=TH-TC; TM=(TH+TC)/2
    A0=(H*TH+C*TC-P)/S
    beta=zt/(TM*(1+m)); cp=zt*m/(TM*(1+m)**2)
    B=L*D+v*P-P*beta*(u-0.5/(1+m))/cp
    E=P*(1+beta*A0)/cp
    disc=B*B-4*L*E
    if disc<0: return []
    dh=(B+math.sqrt(max(0.,disc)))/(2*L)
    ds=[dh, E/(L*dh)] if dh>0 else []
    answer=[]
    for d in ds:
        a=A0+u*d; b=A0-v*d
        K=P/(cp*d*d); q=L*(D-d)+v*P
        if K>0 and TH>=a>b>=TC and q>P:
            R=TM/(zt*K); i=d/(R*(1+m))
            qh=K*d+a*i-0.5*i*i*R; qc=K*d+b*i+0.5*i*i*R
            answer.append(dict(P_W_m2=P,Qhot_W_m2=q,eta=P/q,K_W_m2K=K,m=m,T_K=[a,b],dT_K=d,
                               equation_residual_W_m2=max(abs(H*(TH-a)-qh),abs(C*(b-TC)-qc))))
    return answer

def te_at_power(P,H=H0,C=C0,TH=TH0,TC=TC0,zt=ZT0):
    """Max eta via one convex 1D residual and one scalar root, no SCF solves.

    At fixed d, minimize the contact-eliminated quadratic over m>0.
    Its minimizing m obeys theta*m^2=theta+A0+(u-1/2)*d.
    The larger feasible d is the maximum-efficiency branch.
    """
    if P<=0: return None
    S=H+C; u=C/S; v=H/S; L=H*C/S; D=TH-TC
    theta=(TH+TC)/(2*zt); A0=(H*TH+C*TC-P)/S
    delta=u-0.5; B0=L*D+P*(v-u)
    def f(d):
        return L*d*d-B0*d+P*(2*theta+A0)+2*P*math.sqrt(theta*(theta+A0+delta*d))
    top=D-u*P/L
    if top<=0: return None
    opt=minimize_scalar(f,bounds=(0.,top),method='bounded',options={'xatol':1e-13})
    if opt.fun>0: return None
    d=brentq(f,opt.x,top,xtol=1e-13)
    m=math.sqrt((theta+A0+delta*d)/theta)
    return max(roots_at_power(P,m,H,C,TH,TC,zt),key=lambda r:r['eta'])

def te_max_power(H=H0,C=C0,TH=TH0,TC=TC0,zt=ZT0):
    """Unrestricted load/K maximum for the physical branch of this model."""
    S=H+C; u=C/S; v=H/S; L=H*C/S; D=TH-TC
    TM=(TH+TC)/2; theta=TM/zt; delta=u-0.5
    def margin(P):
        A0=(H*TH+C*TC-P)/S
        def f(d):
            return L*d*d-(L*D+P*(v-u))*d+P*(2*theta+A0)+2*P*math.sqrt(theta*(theta+A0+delta*d))
        opt=minimize_scalar(f,bounds=(0.,D-u*P/L),method='bounded',options={'xatol':1e-13})
        return opt.fun,opt.x
    # Even reversible work cannot exceed the maximum contact-limited power.
    bound=L*D*D/(4*TH)
    P=brentq(lambda p:margin(p)[0],1e-12,bound,xtol=1e-12)
    residual,d=margin(P); A0=(H*TH+C*TC-P)/S
    m=math.sqrt((theta+A0+delta*d)/theta)
    cp=zt*m/(TM*(1+m)**2); K=P/(cp*d*d); q=L*(D-d)+v*P
    return dict(Pmax_W_m2=P,dT_K=d,m=m,K_W_m2K=K,Qhot_W_m2=q,eta=P/q,minimum_quadratic_residual=residual)

if __name__=='__main__':
    sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
    import actual_contacts
    out={'model':'exact algebra for constant ZT=1.2, alpha=1, R=TM/(ZT K)',
         'contacts':dict(H=H0,C=C0,TH=TH0,TC=TC0),'comparisons':[]}
    for P in [0.1,1.,5.,10.]:
        start=time.perf_counter(); new=te_at_power(P); newtime=time.perf_counter()-start
        start=time.perf_counter(); old=actual_contacts.te_at_power(P); oldtime=time.perf_counter()-start
        item=dict(target_P=P,analytic=new,actual_contacts=old,all_K_roots_at_optimum=roots_at_power(P,new['m']),
                  analytic_seconds=newtime,old_seconds=oldtime,
                  relative_eta_difference=(new['eta']/old['eta']-1),relative_K_difference=(new['K_W_m2K']/old['K_W_m2K']-1))
        out['comparisons'].append(item); print(json.dumps(item),flush=True)
    out['global_maximum_power']=te_max_power()
    out['extra_power_checks']=[dict(P=P,analytic=te_at_power(P),actual_contacts=actual_contacts.te_at_power(P))
                               for P in [20.,21.1718,21.7851]]
    out['derivation']={
        'symbols':'S=H+C,u=C/S,v=H/S,L=HC/S,D=TH-TC,theta=TM/ZT,A0=(H TH+C TC-P)/S,delta=u-1/2',
        'fixed_P_m':'L d^2-[L D+P(v-u)+P(1/2-u)/m]d+P[theta m+2theta+A0+(theta+A0)/m]=0',
        'temperature_and_K':'Th=A0+u d,Tc=A0-v d,K=P TM(1+m)^2/(ZT m d^2)',
        'branch_selection':'Qhot=L(D-d)+vP strictly decreases with d; larger positive physical d root has maximal efficiency at fixed P,m.',
        'load_elimination':'For fixed d, minimize residual over all m>0 at m^2=(theta+A0+delta d)/theta. The larger root of that minimized residual is global maximal physical d, hence maximal eta.',
        'scope':'Numerical validation of this constant-property TE model only; no material or FE physical-advantage certification.'}
    Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
