#!/usr/bin/env python3
"""Exact finite-dimensional propagation for a specified crossed-spin receiver.

The receiver starts with an R,A singlet. At spin j it applies the normalized
crossed rational L operator on A_j,E. The complement is retained coherently as
the upper fused spin j+1/2. This implements a genuine CPTP receiver, but its
recovery performance is a question, not an assumption. Classical branch
history is deliberately coarse-grained to the current j.
"""
import argparse
import json
import math
from pathlib import Path
import numpy as np

I=np.eye(2,dtype=complex)
X=np.array([[0,1],[1,0]],dtype=complex)
Y=np.array([[0,-1j],[1j,0]],dtype=complex)
Z=np.diag([1,-1]).astype(complex)
PAULIS=[I,X,Y,Z]

def spin_matrices(j):
    d=round(2*j+1)
    ms=j-np.arange(d)
    plus=np.zeros((d,d),dtype=complex)
    for col,m in enumerate(ms):
        if col>0:
            plus[col-1,col]=math.sqrt(j*(j+1)-m*(m+1))
    return [(plus+plus.T)/2,(plus-plus.T)/(2j),np.diag(ms)]

def tensors(j,theta):
    d=round(2*j+1)
    dot=sum(np.kron(a,b) for a,b in zip(spin_matrices(j),PAULIS[1:]))
    pp=(dot+(j+1)*np.eye(2*d))/(2*j+1)
    pm=np.eye(2*d)-pp
    u=1/math.tan(theta)
    g=u*u+(j+1.5)**2
    K=((u+1j*(j-.5))*pp+(u-1j*(j+1.5))*pm)/math.sqrt(g)
    C=np.zeros((2*d,d+1),dtype=complex)
    for col in range(d+1):
        M=j+.5-col
        for e,shift in [(0,-.5),(1,.5)]:
            m=M+shift
            idx=round(j-m)
            if 0<=idx<d:
                coef=math.sqrt((j+M+.5)/(2*j+1)) if e==0 else math.sqrt((j-M+.5)/(2*j+1))
                C[2*idx+e,col]=coef
    L=math.sqrt(2*(2*j+1)/g)*C.conj().T
    err=np.linalg.norm(K.conj().T@K+L.conj().T@L-np.eye(2*d))
    assert err<1e-10,err
    return K,L

def cg_maps(j):
    d=round(2*j+1)
    maps={}
    for direction in [-1,1]:
        jp=j+direction*.5
        if jp<0:continue
        dp=round(2*jp+1)
        C=np.zeros((2*d,dp),complex)
        for col in range(dp):
            M=jp-col
            for e,shift in [(0,-.5),(1,.5)]:
                m=M+shift
                idx=round(j-m)
                if 0<=idx<d:
                    if direction==1:
                        coef=math.sqrt((j+M+.5)/(2*j+1)) if e==0 else math.sqrt((j-M+.5)/(2*j+1))
                    else:
                        coef=-math.sqrt((j-M+.5)/(2*j+1)) if e==0 else math.sqrt((j+M+.5)/(2*j+1))
                    C[2*idx+e,col]=coef
        maps[direction]=C.conj().T
    assert np.linalg.norm(sum(a.conj().T@a for a in maps.values())-np.eye(2*d))<1e-11
    return maps

def input_collision(rho,theta):
    d=rho.shape[0]//8
    r=np.kron(rho,I/2).reshape(2,2,2,d,2,2,2,2,d,2)
    kp=[0,4,2,3,1,5,6,7,8,9]
    bp=[0,1,2,3,4,5,9,7,8,6]
    both=[0,4,2,3,1,5,9,7,8,6]
    c,s=math.cos(theta),math.sin(theta)
    r=c*c*r+s*s*r.transpose(both)+1j*c*s*(r.transpose(kp)-r.transpose(bp))
    return r.reshape(8,2*d,8,2*d)

def action(r,K):
    return np.einsum('ij,ajbk,lk->aibl',K,r,K.conj(),optimize=True)

def petz_entanglement_fidelity(states):
    total=0.0
    probs={}
    for key,rho in states.items():
        twj=key[0] if isinstance(key,tuple) else key
        d=twj+1
        # Trace source S, retaining reference R0 and receiver R,A_j.
        q=rho.reshape(2,2,2*d,2,2,2*d)
        q=np.trace(q,axis1=1,axis2=4)
        # Remaining order R0,receiver,R0',receiver'.
        sigma=np.trace(q,axis1=0,axis2=2)
        eig,U=np.linalg.eigh((sigma+sigma.conj().T)/2)
        inv=np.zeros_like(eig)
        active=eig>max(1e-15,float(eig.max())*1e-12)
        inv[active]=1/np.sqrt(eig[active])
        im=(U*inv)@U.conj().T
        F=[]
        for p in PAULIS:
            a=2*np.einsum('xy,xayb->ab',p,q,optimize=True)
            F.append(a)
        fe=sum(np.trace(im@a@im@a).real for a in F)/16
        total+=fe
        label=str(twj/2)
        probs[label]=probs.get(label,0.0)+float(np.trace(sigma).real)
    return total,probs

def run(theta,n,prune=0.0,mode='crossed',history=False):
    # R0,S Bell and receiver R,A singlet; order R0,S,R,A.
    bell=np.array([1,0,0,1],complex)/math.sqrt(2)
    singlet=np.array([0,1,-1,0],complex)/math.sqrt(2)
    psi=np.kron(bell,singlet)
    states={(1,'') if history else 1:np.outer(psi,psi.conj())}
    cache={}
    lost=0.0
    results=[]
    for step in range(1,n+1):
        nxt={}
        for key,rho in states.items():
            twj=key[0] if history else key
            hist=key[1] if history else ''
            j=twj/2
            if twj not in cache:cache[twj]=tensors(j,theta) if mode=='crossed' else cg_maps(j)
            r=input_collision(rho,theta)
            branches=[]
            if mode=='crossed':
                K,L=cache[twj]
                suc=action(r,K).reshape(8,twj+1,2,8,twj+1,2)
                suc=np.trace(suc,axis1=2,axis2=5).reshape(8*(twj+1),8*(twj+1))
                fail=action(r,L).reshape(8*(twj+2),8*(twj+2))
                branches=[(twj,'0',suc),(twj+1,'1',fail)]
            else:
                for direction,L in cache[twj].items():
                    qp=twj+direction
                    state=action(r,L).reshape(8*(qp+1),8*(qp+1))
                    branches.append((qp,'+' if direction>0 else '-',state))
            for q,letter,state in branches:
                outkey=(q,hist+letter) if history else q
                if outkey in nxt:nxt[outkey]+=state
                else:nxt[outkey]=state
        states={}
        for q,state in nxt.items():
            prob=float(np.trace(state).real)
            if prob<prune:lost+=prob
            else:states[q]=state
        if step in {1,2,3,5,10,20,30,50,100,n}:
            fe,probs=petz_entanglement_fidelity(states)
            results.append({'step':step,'petz_entanglement_fidelity':fe,'total_trace':sum(probs.values()),
                            'pruned_trace_bound':lost,'max_retained_spin':max(k[0] if history else k for k in states)/2,
                            'retained_classical_histories':len(states),
                            'spin_probabilities':probs})
    return {'theta':theta,'N':n,'receiver':mode,'full_classical_history':history,
            'status':'finite diagnostic, not a target-performance theorem','results':results}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--theta',type=float,default=.6)
    p.add_argument('--n',type=int,default=20)
    p.add_argument('--prune',type=float,default=1e-13)
    p.add_argument('--mode',choices=['crossed','project'],default='crossed')
    p.add_argument('--history',action='store_true')
    args=p.parse_args()
    out=run(args.theta,args.n,args.prune,args.mode,args.history)
    target=Path(__file__).with_name('fusion_probe_'+args.mode+('_history' if args.history else '')+'_'+str(args.theta).replace('.','p')+'.json')
    target.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='results'},indent=2))
    for r in out['results']:
        print(json.dumps({k:v for k,v in r.items() if k!='spin_probabilities'}))
