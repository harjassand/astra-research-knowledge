"""Actual pole variation; no state-uniform small-error claim follows.
Complex incoming/outgoing coefficients multiply arbitrary old a/a^dag.
"""
import json
from pathlib import Path
import numpy as np
from scipy.integrate import simpson
from double_closed_hot_bus import loop


def actual_coefficients(T=1.28,kappa_nom=1e-4,kappa_actual=1e-4,detuning=0.,points=40001,balance_ratio=1.):
    d=loop(kappa=kappa_nom,T=T,points=points,balance_ratio=balance_ratio)
    A,B,c=d['coefficients'];t=np.linspace(0,T,points);q=np.pi*t/T;dq=np.pi/T
    sn=np.sin(q);cs=np.cos(q);ef=np.exp(kappa_nom*t/2)
    X=sn**2*np.sin(2*q);Xp=dq*(2*sn*cs*np.sin(2*q)+2*sn**2*np.cos(2*q))
    Y=sn**2*(np.cos(2*q)+.5);Yp=dq*(2*sn*cs*(np.cos(2*q)+.5)-2*sn**2*np.sin(2*q))
    x=A*ef*X;xp=A*ef*(Xp+kappa_nom*X/2)
    y=B*(ef*Y-c*ef*X);yp=B*(ef*(Yp+kappa_nom*Y/2)-c*ef*(Xp+kappa_nom*X/2))
    fs=[1j*(xp+kappa_nom*x/2),-(yp+kappa_nom*y/2)]
    incoming=np.array([-1j*simpson(np.exp((-kappa_actual/2+1j*detuning)*t)*f,x=t) for f in fs])
    outgoing=np.array([-1j*simpson(np.exp(-(kappa_actual/2+1j*detuning)*(T-t))*f,x=t) for f in fs])
    return dict(kappa_nom=kappa_nom,kappa_actual=kappa_actual,detuning=detuning,T=T,balance_ratio=balance_ratio,
        incoming_abs=list(np.abs(incoming)),outgoing_abs=list(np.abs(outgoing)),
        incoming_real=list(incoming.real),incoming_imag=list(incoming.imag),
        outgoing_real=list(outgoing.real),outgoing_imag=list(outgoing.imag))


if __name__=='__main__':
    ans=[]
    for ka,de in [(1e-4,0),(0.9e-4,0),(1.1e-4,0),(1e-4,1e-4),(1e-4,1e-3),(1e-4,1e-2),(1e-4,.1),(1.1e-4,1e-3)]:
        ans.append(actual_coefficients(kappa_actual=ka,detuning=de))
    parity=[]
    for ka,de in [(1e-4,0),(0.9e-4,0),(1.1e-4,0),(1e-4,1e-4),(1e-4,1e-3),(1e-4,1e-2),(1e-4,.1),(1.1e-4,1e-3)]:
        parity.append(actual_coefficients(T=1.84,balance_ratio=.7498337568074147,kappa_actual=ka,detuning=de))
    ans={'two_qubit_per_actuator_schedule':ans,'one_bus_total_force_parity_schedule':parity}
    Path(__file__).with_name('hot_bus_pole_sensitivity_results.json').write_text(json.dumps(ans,indent=2)+'\n')
    print(json.dumps(ans,indent=2))
