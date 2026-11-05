#!/usr/bin/env python3
"""Finite diagnostics of unitary spin-J receivers with pure initialized memory.
No recovery law is assumed. The source remains the fixed homogeneous qubit.
"""
import math,json,argparse
from pathlib import Path
import numpy as np
from scipy import sparse
from fusion_probe import spin_matrices,PAULIS

def source_receiver_kraus(j,theta,v,rotation_angle=None):
    d=round(2*j+1)
    dot=sum(np.kron(a,b) for a,b in zip(spin_matrices(j),PAULIS[1:]))
    B=dot+.5*np.eye(2*d)
    if rotation_angle is None:
        R=(v*np.eye(2*d)+1j*B)/math.sqrt(v*v+(j+.5)**2)
    else:
        a=j+.5
        R=math.cos(rotation_angle*a)*np.eye(2*d)+1j*math.sin(rotation_angle*a)*B/a
    W=np.zeros((4*d,4*d),complex)
    c,s=math.cos(theta),math.sin(theta)
    for a in range(2):
        for m in range(d):
            for e in range(2):
                col=(a*d+m)*2+e
                W[col,col]+=c
                W[(e*d+m)*2+a,col]+=1j*s
    W=np.kron(np.eye(2),R)@W
    W=W.reshape(2*d,2,2*d,2)
    return [W[:,eo,:,ei]/math.sqrt(2) for eo in range(2) for ei in range(2)]

def expand_kraus(ks,kdim,d):
    outs=[]
    for K in ks:
        ii,jj=np.where(abs(K)>1e-14)
        rr=[];cc=[];vv=[]
        for r0 in range(2):
            for ref in range(kdim):
                rr.extend((((r0*2+ii//d)*kdim+ref)*d+ii%d).tolist())
                cc.extend((((r0*2+jj//d)*kdim+ref)*d+jj%d).tolist())
                vv.extend(K[ii,jj].tolist())
        size=4*kdim*d
        outs.append(sparse.csr_matrix((vv,(rr,cc)),shape=(size,size)))
    return outs

def petz_fe(rho,kdim,d):
    q=rho.reshape(2,2,kdim*d,2,2,kdim*d)
    q=np.trace(q,axis1=1,axis2=4)
    sig=np.trace(q,axis1=0,axis2=2)
    eig,U=np.linalg.eigh((sig+sig.conj().T)/2)
    inv=np.zeros_like(eig)
    mask=eig>max(1e-14,eig.max()*1e-12)
    inv[mask]=1/np.sqrt(eig[mask])
    im=(U*inv)@U.conj().T
    val=0.0
    for p in PAULIS:
        a=2*np.einsum('xy,xayb->ab',p,q,optimize=True)
        val+=np.trace(im@a@im@a).real/16
    return float(val)

def run(j,theta,ratio,n,purified=False):
    d=round(2*j+1);kd=d if purified else 1
    v=ratio/math.tan(theta)
    ks=expand_kraus(source_receiver_kraus(j,theta,v),kd,d)
    bell=np.array([1,0,0,1],complex)/math.sqrt(2)
    if purified:
        mem=np.zeros(d*d,complex)
        for m in range(d):mem[m*d+(d-1-m)]=(-1)**m/math.sqrt(d)
    else:
        mem=np.zeros(d,complex);mem[0]=1
    psi=np.kron(bell,mem);rho=np.outer(psi,psi.conj())
    rows=[];best=(.0,0)
    times=set(range(1,min(n,10)+1))|set(range(20,n+1,20))|{n}
    for t in range(1,n+1):
        nr=np.zeros_like(rho)
        for K in ks:
            tmp=K@rho
            nr+=(K@tmp.conj().T).conj().T
        rho=nr
        if t in times:
            fe=petz_fe(rho,kd,d)
            rows.append([t,fe])
            if fe>best[0]:best=(fe,t)
    return {'J':j,'theta':theta,'rapidity_ratio':ratio,'purified_spin_pair':purified,
            'N':n,'best_sampled_petz_fe':best[0],'best_sampled_time':best[1],
            'final_trace':float(np.trace(rho).real),'samples':rows}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--theta',type=float,default=.3)
    p.add_argument('--j',type=float,default=2);p.add_argument('--n',type=int,default=600)
    p.add_argument('--ratio',type=float,default=1);p.add_argument('--purified',action='store_true')
    a=p.parse_args();result=run(a.j,a.theta,a.ratio,a.n,a.purified)
    name=f'spin_frame_J{a.j}_theta{a.theta}_v{a.ratio}_pur{int(a.purified)}.json'
    Path(__file__).with_name(name).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='samples'},indent=2))
