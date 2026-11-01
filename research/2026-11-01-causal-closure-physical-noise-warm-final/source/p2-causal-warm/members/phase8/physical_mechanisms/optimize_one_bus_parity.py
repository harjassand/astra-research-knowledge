"""Declared 2-function smooth family, total physical bus-force cap.
Not a global control/resource optimum. All 3 actual Z-force actuators charged.
"""
import json
from pathlib import Path
import numpy as np
from scipy.optimize import minimize_scalar,brentq
from double_closed_hot_bus import loop

def fastest(ratio,cap=3.,kappa=1e-4):
    return brentq(lambda T:loop(T=T,kappa=kappa,points=4001,balance_ratio=ratio)['peak_total_force_parity']-cap,.2,20.)

def objective(logratio):
    ratio=np.exp(logratio);T=fastest(ratio)
    d=loop(T=T,points=4001,balance_ratio=ratio);G=np.diag(d['gram_real'])
    return (1-np.exp(-8*G[0]))/2+(1-np.exp(-2*G[1]))/2

if __name__=='__main__':
    opt=minimize_scalar(objective,bounds=(-1.5,1.),method='bounded',options={'xatol':1e-8})
    r=np.exp(opt.x); T=fastest(r)
    # Round time UP and use a modest margin; discretized cap not a strict interval proof.
    T_safe=np.ceil(T*1000)/1000+.001
    ans={'optimization_family':'fixed X,Y trigonometric shapes; one scale ratio and shortest cap-satisfying T', 'force_cap':3.,'optimized_ratio':float(r),'optimized_T_raw':float(T)}
    for key,ratio,Ti in [('optimized_safe',r,T_safe),('balanced_safe',1.,np.ceil(fastest(1.)*1000)/1000+.001),('equal_error_safe',1/np.sqrt(2),np.ceil(fastest(1/np.sqrt(2))*1000)/1000+.001)]:
        d=loop(T=Ti,balance_ratio=ratio,points=100001);G=np.diag(d['gram_real'])
        d['p_data_even_vacuum']=float(-np.expm1(-8*G[0])/2)
        d['p_data_odd_vacuum']=0.
        d['p_ancilla_Z_vacuum']=float(-np.expm1(-2*G[1])/2)
        d['total_union_bound_vacuum']=d['p_data_even_vacuum']+d['p_ancilla_Z_vacuum']
        d['p_data_even_nb01']=float(-np.expm1(-8*1.2*G[0])/2)
        d['p_ancilla_Z_nb01']=float(-np.expm1(-2*1.2*G[1])/2)
        d['max_total_force_margin']=3-d['peak_total_force_parity']
        assert d['peak_total_force_parity']<3
        ans[key]=d
    Path(__file__).with_name('one_bus_parity_results.json').write_text(json.dumps(ans,indent=2)+'\n')
    print(json.dumps(ans,indent=2))
