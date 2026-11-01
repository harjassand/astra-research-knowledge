"""Finite smooth damped hot-bus loop; all integrals include ramps.
Effective H=sum Z_j(f_j a^dag + f_j^* a), L=sqrt(kappa) a.
No oscillator truncation is used in this waveform computation.
"""
import json
from pathlib import Path
import numpy as np
from scipy.integrate import simpson
from scipy.optimize import brentq


def loop(kappa=1.e-4,T=4.,theta=np.pi/4,points=20001,balance_ratio=1.):
    t=np.linspace(0,T,points); q=np.pi*t/T; dq=np.pi/T
    sin=np.sin(q); cos=np.cos(q)
    X=sin**2*np.sin(2*q)
    Xp=dq*(2*sin*cos*np.sin(2*q)+2*sin**2*np.cos(2*q))
    Y=sin**2*(np.cos(2*q)+.5)
    Yp=dq*(2*sin*cos*(np.cos(2*q)+.5)-2*sin**2*np.sin(2*q))
    ef=np.exp(kappa*t/2)
    x=ef*X; xp=ef*(Xp+kappa*X/2)
    y=ef*Y; yp=ef*(Yp+kappa*Y/2)
    dot=simpson(x*y,x=t); nx=simpson(x*x,x=t)
    c=dot/nx
    y=y-c*x; yp=yp-c*xp
    ny=simpson(y*y,x=t)
    area=simpson(x*yp-y*xp,x=t)
    # Balanced two fresh-noise channels, with positive desired ZZ area.
    A=np.sqrt(abs(theta/area)*np.sqrt(ny/nx))
    B=np.sign(theta/area)*np.sqrt(abs(theta/area)*np.sqrt(nx/ny))
    A*=balance_ratio; B/=balance_ratio
    x*=A; xp*=A; y*=B; yp*=B
    f1=1j*(xp+kappa*x/2)
    f2=-(yp+kappa*y/2)
    bet=np.stack([x,1j*y]); forces=np.stack([f1,f2])
    gram=kappa*np.array([[simpson(np.conj(bet[j])*bet[k],x=t) for k in range(2)] for j in range(2)])
    incoming=np.array([simpson(np.exp(-kappa*t/2)*f,x=t) for f in forces])
    outgoing=np.array([simpson(np.exp(kappa*t/2)*f,x=t) for f in forces])
    area=simpson(x*yp-y*xp,x=t)
    noise=np.real(np.diag(gram))
    return dict(T=T,kappa=kappa,balance_ratio=balance_ratio,theta=float(area),peak_total_force_parity=float(np.max(np.sqrt(4*np.abs(f1)**2+np.abs(f2)**2))),peak_total_force_gate=float(np.max(np.sqrt(np.abs(f1)**2+np.abs(f2)**2))),peak_force=list(np.max(np.abs(forces),axis=1)),
        peak_slew=list(np.max(np.abs(np.gradient(forces,t,axis=1)),axis=1)),
        integrated_displacement=list(noise/kappa),
        p_vacuum=list(-np.expm1(-2*noise)/2),
        p_thermal_n01=list(-np.expm1(-2*1.2*noise)/2),
        max_pair_displacement_squared=float(np.max(x*x+y*y)),max_parity_displacement_squared=float(np.max(4*x*x+y*y)),
        gram_real=gram.real.tolist(),gram_imag=gram.imag.tolist(),
        incoming_real=incoming.real.tolist(),incoming_imag=incoming.imag.tolist(),
        outgoing_real=outgoing.real.tolist(),outgoing_imag=outgoing.imag.tolist(),
        endpoints=bet[:,[0,-1]].tolist() if False else float(np.max(abs(bet[:,[0,-1]]))),
        raw_mean_X=float(simpson(X,x=t)),raw_mean_Y=float(simpson(Y,x=t)),
        coefficients=[float(A),float(B),float(c)])


def run():
    ans={}
    ans['four_time_units']=loop(T=4.)
    ans['conservative_force_cap3']=loop(T=1.28)
    for force_cap in [1.,2.,3.]:
        T=brentq(lambda T:max(loop(T=T,points=4001)['peak_force'])-force_cap,.1,20.,xtol=1e-10)
        ans['cap_'+str(force_cap)]=loop(T=T)
    for item in ans.values():
        assert abs(item['theta']-np.pi/4)<1e-10
        assert max(np.abs(item['incoming_real'])+np.abs(item['incoming_imag']))<1e-10
        assert max(np.abs(item['outgoing_real'])+np.abs(item['outgoing_imag']))<1e-10
        assert max(abs(np.asarray(item['gram_imag']).ravel()))<1e-12
    p=Path(__file__).with_name('double_closed_hot_bus_results.json')
    p.write_text(json.dumps(ans,indent=2)+'\n')
    print(json.dumps(ans,indent=2))
if __name__=='__main__':run()
