"""Exact 2-data+1-ancilla instrument audit after bath elimination.
Uses independent explicit ancilla amplitudes vs claimed sector CP decomposition.
Includes unequal complex static gains, thermal noise and orientation frame.
"""
import json
from pathlib import Path
import numpy as np

z=np.array([[1,1],[1,-1],[-1,1],[-1,-1]])
s=np.prod(z,axis=1)
z1=z[:,0]

def channel(g1,g2,ga,Gx,Gy,nb,frame=True,randomized=True):
    theta=np.pi/4*np.real(np.array([np.conj(g1)*ga,np.conj(g2)*ga]))
    phase=z@theta
    v=2*nb+1
    dz=z@np.array([g1,g2])
    C=np.exp(-.5*v*Gx*abs(dz[:,None]-dz[None,:])**2+1j*Gx*np.imag(np.conj(dz[None,:])*dz[:,None]))
    pA=-np.expm1(-2*v*Gy*abs(ga)**2)/2
    # m=0 means X+, so reported parity is -; m=1 means X-, parity+.
    got=[np.zeros((4,4),complex),np.zeros((4,4),complex)]
    orientations=[(1,.5),(-1,.5)] if randomized else [(1,1.)]
    for orientation,psign in orientations:
        raw=[np.cos(orientation*phase),1j*np.sin(orientation*phase)]
        for m in range(2):
            corr=z1**m
            if frame and orientation<0:corr=corr*s
            for b,pb in [(0,1-pA),(1,pA)]:
                a=corr*raw[m^b]
                got[m]+=psign*pb*np.outer(a,a.conj())*C
    pred=[np.zeros((4,4),complex),np.zeros((4,4),complex)]
    deltas=theta-np.pi/4
    rows=[]
    for sector in [1,-1]:
        P=(s==sector).astype(float)
        pD=-np.expm1(-2*v*Gx*abs(g1+sector*g2)**2)/2
        pCal=np.sin(deltas[0]+sector*deltas[1])**2
        rows.append(dict(sector=sector,pD=float(pD),pCal=float(pCal)))
        for f,pf in [(0,1-pCal),(1,pCal)]:
            for b,pb in [(0,1-pA),(1,pA)]:
                shat=sector*(-1)**(f+b);m=int(shat==1)
                for d,pd in [(0,1-pD),(1,pD)]:
                    a=P*z1**(d+b)
                    pred[m]+=pf*pb*pd*np.outer(a,a)
    maxdiff=max(np.max(abs(a-b)) for a,b in zip(got,pred))
    cross=max(np.max(abs(a*(s[:,None]!=s[None,:]))) for a in got)
    return dict(max_element_error=float(maxdiff),max_cross_sector=float(cross),pA=float(pA),theta=list(theta),sectors=rows)

if __name__=='__main__':
    params=dict(g1=.99*np.exp(.02j),g2=1.015*np.exp(-.013j),ga=1.01*np.exp(.01j),Gx=.05,Gy=.07,nb=.1)
    ans={'stress_complex_gains':{k:([v.real,v.imag] if isinstance(v,complex) else v) for k,v in params.items()},
         'correct_orientation_frame':channel(**params),
         'failure_omitted_frame':channel(**params,frame=False),
         'failure_no_randomization':channel(**params,randomized=False),
         'ideal_gain_small_physical_noise':channel(g1=1,g2=1,ga=1,Gx=5.111729043210151e-6,Gy=1.616992006316965e-5,nb=0)}
    assert ans['correct_orientation_frame']['max_element_error']<1e-13
    assert ans['failure_omitted_frame']['max_cross_sector']>1e-3
    Path(__file__).with_name('one_bus_parity_instrument_checks.json').write_text(json.dumps(ans,indent=2)+'\n')
    print(json.dumps(ans,indent=2))
