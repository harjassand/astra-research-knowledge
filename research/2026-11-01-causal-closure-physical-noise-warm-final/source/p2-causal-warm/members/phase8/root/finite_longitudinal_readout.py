"""Finite QND ancilla preparation/readout with an actually retained hot bus.

Single oscillator, intrinsic port k0 and separately opened readout port kr(t).
All fresh inputs have the stated homogeneous white thermal occupation nb.
The receiver rejects the one initial-mode response exactly in the linear model.
Finite up/down ramps, force and storage loss are included.  This is a declared
direct-port effective model, not an adiabatic elimination of the Phase7 converter.
"""
from pathlib import Path
import json
import numpy as np
from scipy.integrate import solve_ivp, simpson
from scipy.optimize import brentq
from scipy.special import ndtr, log_ndtr

HERE=Path(__file__).resolve().parent

def ramp(t,T,r=.1):
    if t<0 or t>T:return 0.
    if t<r:return np.sin(np.pi*t/(2*r))**2
    if t>T-r:return np.sin(np.pi*(T-t)/(2*r))**2
    return 1.

def evaluate(T,force=3.,kr=1.,k0=1.e-4,eta=.5,nb=.1,points=12001):
    def controls(t):
        w=ramp(t,T)
        return kr*w,force*w
    def fun(t,y):
        kout,u=controls(t); k=k0+kout
        return [-k*y[0]/2,-k*y[1]/2+u]
    t=np.linspace(0,T,points)
    sol=solve_ivp(fun,[0,T],[1.,0.],t_eval=t,rtol=2.e-11,atol=1.e-13,max_step=.025)
    if not sol.success:raise RuntimeError(sol.message)
    port=np.array([controls(s)[0] for s in t]); u=np.array([controls(s)[1] for s in t])
    initial=np.sqrt(port)*sol.y[0]; signal=np.sqrt(port)*sol.y[1]
    gram=simpson(initial**2,x=t); overlap=simpson(initial*signal,x=t)
    proj=signal-initial*overlap/gram
    N=simpson(proj**2,x=t)
    logq=float(log_ndtr(-2*np.sqrt(eta*N)/np.sqrt(1+2*eta*nb)))
    q=float(np.exp(logq))
    loggamma=-np.log(2.)-2*(2*nb+1)*N
    e=q+np.exp(2*loggamma-logq)
    return dict(T=T,force_cap=force,readout_rate_cap=kr,intrinsic_loss=k0,eta=eta,nb=nb,
       ramp=.1,N_eff=float(N),raw_output_displacement_energy=float(simpson(signal**2,x=t)),
       q_homodyne=q,CP_bad_weight=float(e),initial_mode_residual=float(simpson(initial*proj,x=t)),
       retained_amplitude_contraction=float(sol.y[0,-1]),
       retained_conditional_displacement=float(sol.y[1,-1]),
       integrated_force=float(simpson(u,x=t)),
       integrated_damping=float(simpson(port+k0,x=t)),
       peak_conditional_photons=float(max(sol.y[1]**2)),
       comment='True QND single-qubit Z instrument; rank-one good projection permits actual X feedforward reset.')

def main():
    rows=[]
    for kr in [1.,4.]:
        for target in [1.e-4,1.e-6,1.e-8]:
            T=brentq(lambda z:evaluate(z,kr=kr,points=3001)['CP_bad_weight']-target,.3,30.,xtol=1.e-10)
            row=evaluate(T,kr=kr);row['target']=target;rows.append(row)
    out=dict(model='Finite direct readout port, same warm white occupation in both ports; fixed homodyne phase plus signed classical weighting.',rows=rows,
       all_interval_scope='Each listed T includes both switching ramps. Data-control pulses, feedforward and quantum waiting must be added by the actual consumer. No reset/cooldown inserted.',
       failure_scope='Unknown poles, unequal/colored fresh fields, amplifier memory and nonzero data forces during readout are not erased by this calculation.')
    (HERE/'finite_longitudinal_readout_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
