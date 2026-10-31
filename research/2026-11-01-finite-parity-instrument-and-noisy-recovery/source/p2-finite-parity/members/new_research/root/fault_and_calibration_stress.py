"""Finite-time stress tests of root's exact parity-emission construction.

Solve every conditional coherent trajectory with the *nominal* physical
pulses. Retain every emitted port and final oscillator. Compare the two
same-parity branches after the same physical X-fault history. This detects
information leakage missed by a stationary/perfect-label calculation.

For no X fault, the calculation also resolves actual control miscalibration.
The overlap is UNCONDITIONAL (entire record discarded); it is not a lower
bound against an arbitrary receiver with record/history-informed feedback.
Known deterministic phases can be corrected; visibility cannot be restored
by a final unitary without such side information.
"""
from __future__ import annotations
from pathlib import Path
import json,sys
import numpy as np
from scipy.integrate import solve_ivp, simpson

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'finite_operation'))
from exact_cascade_parity import Model,waveforms

def run(m,flip_qubit=None,flip_time=None,du=0.,dw=0.,dchi=0.,common_detuning=0.,samples=5001):
    # All four branches. Logical Z labels follow an actual X history.
    zs=np.array([[1,1],[1,-1],[-1,1],[-1,-1]])
    ke,kc,kb,ki=m.ke,m.kc,m.kb,m.ki
    ae=(ke+kb)/2; ac=(kc+ki)/2
    times=np.linspace(0,m.T,samples)
    if flip_time is not None:times=np.unique(np.r_[times,flip_time])
    vals=np.zeros((len(times),4,2),complex)
    boundaries=[0,m.T] if flip_time is None else [0,flip_time,m.T]
    initial=np.zeros((4,2),complex)
    for seg in range(len(boundaries)-1):
        start,end=boundaries[seg:seg+2]
        labels=zs.copy()
        if seg>0:labels[:,flip_qubit]*=-1
        def rhs(t,v):
            v=v.reshape(4,2); b,c=v[:,0],v[:,1]
            f=waveforms(m,t)
            db=-ae*b-1j*(1+du)*f['u']*labels[:,1]
            dc=-(ac+1j*(m.chi*(1+dchi)*labels[:,0]+common_detuning))*c-np.sqrt(ke*kc)*b-1j*(1+dw)*f['w']*labels[:,1]
            return np.c_[db,dc].ravel()
        inds=np.where((times>=start)&(times<=end))[0]
        sol=solve_ivp(rhs,[start,end],initial.ravel(),t_eval=times[inds],method='DOP853',rtol=1e-10,atol=1e-12)
        if not sol.success:raise RuntimeError(sol.message)
        vv=sol.y.T.reshape(-1,4,2)
        vals[inds]=vv;initial=vv[-1]
    b,c=vals[:,:,0],vals[:,:,1]
    main=np.sqrt(ke)*b+np.sqrt(kc)*c
    by=np.sqrt(kb)*b;inside=np.sqrt(ki)*c
    rows=[]
    for i,j in [(0,3),(1,2)]:
        dm=main[:,i]-main[:,j]
        db=by[:,i]-by[:,j];di=inside[:,i]-inside[:,j]
        Dmain=float(simpson(abs(dm)**2,x=times)/2)
        Dloss=float(simpson(abs(db)**2+abs(di)**2,x=times)/2)
        Dfinal=float(np.sum(abs(vals[-1,i]-vals[-1,j])**2)/2)
        D=Dmain+Dloss+Dfinal
        rows.append({'initial_parity':int(zs[i,0]*zs[i,1]),
                     'D_main':Dmain,'D_hidden':Dloss,'D_terminal':Dfinal,
                     'discard_record_visibility':float(np.exp(-D)),
                     'discard_record_phase_flip_probability':float(-np.expm1(-D)/2),
                     'lost_main_only_D':float((1-m.eta)*Dmain),
                     'real_main_difference_energy':float(simpson(dm.real**2,x=times)),
                     'max_terminal_photons':float(max(np.sum(abs(vals[-1,i])**2),np.sum(abs(vals[-1,j])**2)))})
    return rows

def main():
    m=Model(T=8,ke=1,kc=10,chi=5,eta=.5,assignment_error=.001)
    out={'model':m.__dict__,'nominal':run(m),'calibration':[],'single_X':[]}
    for name,kw in [('source_amplitude',{'du':.01}),('counterdrive_amplitude',{'dw':.01}),
                    ('dispersive_shift',{'dchi':.01}),('common_detuning',{'common_detuning':.05}),
                    ('both_drive_amplitudes',{'du':.01,'dw':.01}),
                    ('all_three_gains',{'du':.01,'dw':.01,'dchi':.01})]:
        row={'error':name,'parameters':kw,'pairs':run(m,**kw)}
        out['calibration'].append(row)
        print(name,[p['discard_record_phase_flip_probability'] for p in row['pairs']])
    for q in (0,1):
        for fraction in (.1,.25,.5,.75,.9):
            row={'physical_qubit':q+1,'time_fraction':fraction,'pairs':run(m,flip_qubit=q,flip_time=m.T*fraction)}
            out['single_X'].append(row)
            print('X',q+1,fraction,[p['discard_record_phase_flip_probability'] for p in row['pairs']])
    Path(__file__).with_name('fault_and_calibration_results.json').write_text(json.dumps(out,indent=2))

if __name__=='__main__':main()
