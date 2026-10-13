"""Executed explicit OR-of-bins receiver in inherited G106 all-bath model.

Source modules are imported read-only with bytecode disabled. No terminal
qutrit projector is applied. Each bin has a physical homodyne threshold; an
accepted density operator is propagated into the next bin. Per-bin analog Z
feedforward is a specified, record-dependent unitary. This is a Floquet-secular
finite-dimensional float model, not device validation. Pump ramps are tested
separately and are not silently credited as zero-error pulses here.
"""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
import argparse
import copy
import hashlib
import json
import os
import time
import numpy as np
from scipy import sparse as sp
from scipy.sparse.linalg import expm_multiply
from scipy.special import ndtri

SOURCE=Path('/Users/harjas/Documents/Codex/2026-10-13/astra-genesis-civilization-enabling-breakthrough-discovery')
sys.path.insert(0,str(SOURCE/'work/phase5/quantum_operation'))
import floquet_record_instrument as f
ROOT=Path(__file__).resolve().parent


def initial_state(nf):
    d=nf*nf
    z=np.zeros(10*d,complex)
    z[0]=1;z[5*d]=1;z[7*d]=1;z[9*d]=1
    return z


def split_rows(rows,nparts):
    total=sum(r['dt'] for r in rows)
    groups=[[] for _ in range(nparts)]
    elapsed=0.
    for row in rows:
        remaining=row['dt']
        while remaining>1e-12:
            j=min(nparts-1,int((elapsed+1e-10)/total*nparts))
            dt=min(remaining,total*(j+1)/nparts-elapsed)
            groups[j].append(dict(row,dt=dt))
            remaining-=dt;elapsed+=dt
    return groups


def bin_receivers(rows,receiver,nparts,alpha):
    groups=split_rows(rows,nparts)
    lam=np.array([complex(*pair) for pair in receiver['linear_lambda_per_us']])
    # Carrier matrix element required for exact linear baseline integration.
    # Set by caller after model construction, not inferred from a hidden state.
    v=np.array(receiver['carrier_ladder_amplitude'])
    state=np.zeros(3,complex)
    per_alpha=1-(1-alpha)**(1/nparts)
    ans=[]
    for group in groups:
        norm=np.sqrt(sum(r['w']**2*r['dt'] for r in group))
        baseline=0.
        for row in group:
            row['w']/=norm
            dt=row['dt'];drive=row['drive']
            integral=state*(1-np.exp(-lam*dt))/lam+v*drive*(dt/lam-(1-np.exp(-lam*dt))/lam**2)
            baseline+=row['w']*2*np.sqrt(f.ETA*f.KAPPA)*np.real(np.exp(-1j*row['theta'])*(v[0]*integral[0]+v[2]*integral[2])/2)
            state=state*np.exp(-lam*dt)+v*drive*(1-np.exp(-lam*dt))/lam
        ans.append((group,float(baseline+ndtri(1-per_alpha))))
    return ans,per_alpha


def accepted_bin(model,value,rows,probe,threshold,nfreq,span=28.):
    nf=model['nf'];d=nf*nf;dim=10*d
    k=2*np.pi*np.fft.fftfreq(nfreq,d=span/nfreq)
    values=np.tile(value,(nfreq,1)).ravel()
    Ik=sp.eye(nfreq,format='csr');K=sp.diags(-1j*k);K2=sp.diags(-k*k/2)
    for row in rows:
        L=f.liouvillians(model,probe,row['drive'],False)
        M=f.measurement_matrix(model,row['theta'],False)
        G=sp.kron(Ik,L)+row['w']*sp.kron(K,M)+row['w']**2*sp.kron(K2,sp.eye(dim,format='csr'))
        traceA=row['dt']*(nfreq*L.diagonal().sum()+row['w']**2*(-k*k/2).sum()*dim)
        values=expm_multiply(G.tocsr()*row['dt'],values,traceA=traceA)
    fourier=values.reshape(nfreq,dim)
    integral=np.empty(nfreq,complex)
    integral[0]=(threshold+span/2)/span
    integral[1:]=(np.exp(1j*k[1:]*threshold)-np.exp(-1j*k[1:]*span/2))/(1j*k[1:]*span)
    out=integral@fourier
    # Carry a real, implementable analog phase correction into the next bin.
    # A bin record is then discarded, retaining only pass/fail and Z update.
    grid=4096
    padded=np.zeros((grid,d),complex);pos=nfreq//2
    padded[:pos]=fourier[:pos,9*d:]
    padded[-(nfreq-pos):]=fourier[pos:,9*d:]
    dens=np.fft.fftshift(np.fft.ifft(padded,axis=0),axes=0)*grid/span
    y=(np.arange(grid)-grid//2)*span/grid
    traces=np.trace(dens.reshape(grid,nf,nf),axis1=1,axis2=2)
    dens*=np.exp(-1j*np.angle(traces))[:,None]
    edge=int(np.searchsorted(y,threshold)-1);dy=span/grid
    frac=(threshold-y[edge])/dy
    at=dens[edge]+frac*(dens[edge+1]-dens[edge])
    out[9*d:]=np.trapezoid(dens[:edge+1],y[:edge+1],axis=0)+(dens[edge]+at)*(threshold-y[edge])/2
    # Fourier densities should define a CP accepted map up to float error.
    minpop=0.;minmatrix=0.
    for off in [0,3*d,6*d]:
        for q in range(3):
            mat=out[off+q*d:off+(q+1)*d].reshape(nf,nf)
            minmatrix=min(minmatrix,float(np.linalg.eigvalsh((mat+mat.conj().T)/2).min()))
            minpop=min(minpop,float(np.trace(mat).real))
    return out,{'minimum_accepted_population':minpop,'minimum_accepted_block_eigenvalue':minmatrix}


def metrics(z,nf):
    d=nf*nf
    p=[];ph=[]
    for off in [0,3*d,6*d]:
        p.append([float(np.trace(z[off+q*d:off+(q+1)*d].reshape(nf,nf)).real) for q in range(3)])
        ph.append(float(sum(np.dot(np.arange(nf),np.diag(z[off+q*d:off+(q+1)*d].reshape(nf,nf))).real for q in range(3))))
    pacc=(sum(p[0])+sum(p[1]))/2
    leakage=(p[0][1]+p[1][1])/2
    coherence=float(np.trace(z[9*d:].reshape(nf,nf)).real)
    overlap=(p[0][0]+p[1][2]+2*coherence)/4
    choi=np.diag(np.array(p[:2]).ravel()/2).astype(complex)
    choi[0,5]=choi[5,0]=coherence/2
    return {'acceptance_mixed_code':pacc,'accepted_terminal_e_mass_per_input':leakage,
            'accepted_Choi_infidelity':1-overlap/pacc,
            'diagnostic_only_code_projected_infidelity':1-overlap/(pacc-leakage),
            'prepared_e_flag_probability':1-sum(p[2]),
            'accepted_output_g_e_f_by_initial_g_f_e':p,
            'accepted_cavity_photons_per_input_by_initial_g_f_e':ph,
            'accepted_mean_cavity_photons_mixed_code':(ph[0]+ph[1])/(2*pacc),
            'minimum_accepted_Choi_eigenvalue':float(np.linalg.eigvalsh(choi).min())}


def no_decay_model(model):
    out=copy.deepcopy(model)
    out['channels']={bath:{key:a for key,a in channels.items() if key[0]==key[1]} for bath,channels in model['channels'].items()}
    out['loss']=np.zeros_like(model['loss'])
    for channels in out['channels'].values():
        for (qi,qo,ell),a in channels.items():out['loss'][qi]+=np.sum(abs(a)**2,axis=0)
    return out


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--nf',type=int,default=16)
    parser.add_argument('--nfreq',type=int,default=80)
    parser.add_argument('--parts',type=int,nargs='+',default=[1,2,4])
    parser.add_argument('--false-positive',type=float,default=.02)
    parser.add_argument('--jump-efficiency',type=float,default=0.)
    parser.add_argument('--collect-intrinsic-b',action='store_true')
    parser.add_argument('--output',default='BINNED_RESULTS.json')
    args=parser.parse_args();start=time.perf_counter()
    f.ecr.MEASURED_HALF_GE_CAVITY_SHIFT_MHZ=.5
    g=f.ecr.calibrate_g()
    model=f.make_model(args.nf,2503.,217.28013507543088,g)
    rows,receiver=f.schedule(model,3.,5.,.8,24,8)
    receiver['carrier_ladder_amplitude']=[float(a[0,1].real) for a in model['carrier']]
    # Explicit frequency-resolved jump-photon veto: zero detected photons is
    # accepted. Keep TOTAL anticommutator loss, reduce only recycling by1-eta.
    # This assumes ideal transition-frequency filters with zero carrier false
    # clicks. It is an optimistic model of additional receiver hardware.
    if args.jump_efficiency:
        for bath in (['a','b'] if args.collect_intrinsic_b else ['a']):
            for key,a in model['channels'][bath].items():
                if key[0]!=key[1]:model['channels'][bath][key]=a*np.sqrt(1-args.jump_efficiency)
    cases=[]
    for parts in args.parts:
        bins,per_alpha=bin_receivers(rows,receiver,parts,args.false_positive)
        values=initial_state(args.nf);checks=[]
        for i,(group,threshold) in enumerate(bins):
            values,check=accepted_bin(model,values,group,receiver['probe_MHz'],threshold,args.nfreq)
            checks.append(check)
            print(json.dumps({'parts':parts,'bin':i,'metrics':metrics(values,args.nf)}),flush=True)
        cases.append({'parts':parts,'bin_thresholds':[thr for _,thr in bins],
                      'nominal_false_positive_per_bin':per_alpha,'metrics':metrics(values,args.nf),'positivity_checks':checks})
    # Matched control charges the same finite drive/reset waveform, but removes
    # q-changing transitions to check the claimed detector FPR independently.
    control=[]
    clean=no_decay_model(model)
    for parts in args.parts:
        bins,_=bin_receivers(rows,receiver,parts,args.false_positive)
        values=initial_state(args.nf)
        for group,threshold in bins:values,_=accepted_bin(clean,values,group,receiver['probe_MHz'],threshold,args.nfreq)
        m=metrics(values,args.nf)
        control.append({'parts':parts,'metrics':m})
    source_files=['floquet_record_instrument.py','floquet_erasure_readout.py','echoed_curvature_readout.py']
    receipts={name:hashlib.sha256((SOURCE/'work/phase5/quantum_operation'/name).read_bytes()).hexdigest() for name in source_files}
    result={'status':'EXPLICIT_FINITE_BIN_RECEIVER_IN_FLOAT_FLOQUET_SECULAR_MODEL_NOT_DEVICE_VALIDATION',
            'runtime_seconds':time.perf_counter()-start,'arguments':vars(args),'G_MHz':g,
            'candidate':'preferred300','no_echo':True,'source_hashes':receipts,
            'model_diagnostics':model['diagnostics'],
            'cases':cases,'no_q_transition_detector_controls':control,
            'scope':'Finite3us read,.8us reset; every inherited cavity and intrinsic-b jump harmonic is charged. OR detector and analog phase feedforward only. No terminal qutrit-state postselection. Pump ramps and physical bias noise remain unacquired and are not credited.'}
    (ROOT/args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'result':str(ROOT/args.output),'runtime_seconds':result['runtime_seconds']}),flush=True)


if __name__=='__main__':main()
