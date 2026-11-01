#!/usr/bin/env python3
"""A source-derived multi-event/channel discriminator with retained memory.

This integrates the acquired physical jump amplitudes on finite CPU grids. It
is not the scalable quantum circuit and does not test the entire error theorem.
The initial bath is vacuum; the Choi comparison includes every qubit input and
an untouched reference, with a noncommuting system control between windows.
"""
import json,math,time
from pathlib import Path
import numpy as np
from loss_clock import CoupledBath,dyadic_cells,expm,norm
P=Path(__file__).resolve().parent

def source_channel(b,t,res):
    K0=b.nojump(t)
    channel=np.kron(K0.conj(),K0)
    cells=dyadic_cells(t,b.R,res)
    histories=1
    for lo,hi in cells:
        s=(lo+hi)/2
        mass=max(0.,b.event_cdf(hi)-b.event_cdf(lo))
        weight=mass/b.w(s)**2
        jump=b.L@b.nojump(s)
        one=b.nojump(t-s)@jump
        channel+=weight*np.kron(one.conj(),one)
        histories+=1
        for lo2,hi2 in dyadic_cells(t-s,b.R,res):
            s2=(lo2+hi2)/2
            mass2=max(0.,b.event_cdf(hi2)-b.event_cdf(lo2))
            weight2=mass2/b.w(s2)**2
            two=b.nojump(t-s-s2)@b.L@b.nojump(s2)@jump
            channel+=weight*weight2*np.kron(two.conj(),two)
            histories+=1
    return channel,histories

def reduced_choi(phi,b):
    db=b.d;v=np.zeros((db,db),complex);v[0,0]=1.
    J=np.zeros((4,4),complex)
    for i in range(2):
        for j in range(2):
            rho=np.zeros((2,2),complex);rho[i,j]=1
            z=(phi@np.kron(rho,v).reshape(-1,order='F')).reshape((2*db,2*db),order='F')
            z=np.einsum('aibi->ab',z.reshape(2,db,2,db))
            J[2*i:2*i+2,2*j:2*j+2]=z/2
    return J

def reset_super(phi,b):
    db=b.d;v=np.zeros((db,db),complex);v[0,0]=1
    z=np.zeros((4,4),complex)
    for i in range(2):
        for j in range(2):
            rho=np.zeros((2,2),complex);rho[i,j]=1
            out=(phi@np.kron(rho,v).reshape(-1,order='F')).reshape((2*db,2*db),order='F')
            out=np.einsum('aibi->ab',out.reshape(2,db,2,db))
            z[:,i+2*j]=out.reshape(-1,order='F')
    return z

def choi_sys(phi):
    J=np.zeros((4,4),complex)
    for i in range(2):
        for j in range(2):
            J[2*i:2*i+2,2*j:2*j+2]=phi[:,i+2*j].reshape(2,2,order='F')/2
    return J

def tn(x):return float(np.linalg.svd(x,compute_uv=False).sum())

if __name__=='__main__':
    b=CoupledBath(40);t=.35;d=2*b.d
    sy=np.array([[0,-1j],[1j,0]],complex)
    us=expm(-.47j*sy);u=np.kron(us,np.eye(b.d));ctrl=np.kron(u.conj(),u)
    lig=np.kron(np.eye(d),b.G)+np.kron(b.G.conj(),np.eye(d))+np.kron(b.L.conj(),b.L)
    exact=expm(lig*t);Jref=reduced_choi(exact@ctrl@exact,b)
    reset=reset_super(exact,b);Jreset=choi_sys(reset@np.kron(us.conj(),us)@reset)
    data={'scope':'Finite source-weighted zero/one/two-jump quadrature per window; not a fault-tolerant circuit or independent audit.',
          'R':b.R,'window_duration':t,'total_time':2*t,'initial_bath':'vacuum','system_control':'exp(-0.47 i sigma_y)',
          'reset_bath_between_windows_Choi_trace_distance':tn(Jreset-Jref)/2,
          'exact_Choi_trace':float(np.trace(Jref).real),'refinements':[]}
    for res in [4,8,16]:
        start=time.time();approx,hist=source_channel(b,t,res);J=reduced_choi(approx@ctrl@approx,b)
        err=2*tn(J-Jref)
        data['refinements'].append({'resolution':res,'CPU_history_terms_per_window':hist,
         'Choi_trace':float(np.trace(J).real),'diamond_upper_from_numerical_Choi':err,
         'seconds':time.time()-start})
        print(json.dumps(data['refinements'][-1]),flush=True)
    errors=[x['diamond_upper_from_numerical_Choi'] for x in data['refinements']]
    assert all(y<x for x,y in zip(errors,errors[1:]))
    assert errors[-1]<data['reset_bath_between_windows_Choi_trace_distance']/5
    lam=(float(np.linalg.norm(b.c))*2*t)**2
    data['proved_probability_of_three_or_more_actual_jumps_over_both_windows_upper']=lam**3/math.factorial(3)
    data['warning']='Finite quadrature map need not be exactly TP. Choi upper is a diagnostic comparing this explicit approximation to the exact finite-cutoff channel; the compiler proof separately constructs an unconditional CPTP implementation.'
    (P/'results'/'retained_process_check.json').write_text(json.dumps(data,indent=2)+'\n')
    print('PASS: retained full-input process with noncommuting intermediate control; refinement reduces error.',flush=True)
