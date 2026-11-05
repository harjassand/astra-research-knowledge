#!/usr/bin/env python3
"""Evaluate root's exact balanced-Petz acquisition ledger from saved states."""
import argparse,json
from pathlib import Path
import numpy as np
import scipy.linalg as la

P=[np.array([[0,1],[1,0]],complex),np.array([[0,-1j],[1j,0]],complex),np.diag([1.,-1.])]

def visibility_split(rho,m):
    a=rho.reshape(2,2,m,2,2,m)
    sigma=np.einsum('rsmrsn->mn',a)
    w,v=la.eigh((sigma+sigma.conj().T)/2)
    inv=np.zeros_like(w);good=w>1e-12;inv[good]=w[good]**(-.25)
    lift=np.kron(np.eye(2),(v*inv)@v.conj().T)
    total=0.;acquired=0.
    for p in P:
        signal=np.einsum('rq,raqb->ab',p,rho.reshape(2,2*m,2,2*m))
        balanced=np.sqrt(2)*lift@signal@lift
        tr_s=np.einsum('sisj->ij',balanced.reshape(2,m,2,m))
        acquired+=np.vdot(tr_s,tr_s).real/6
        total+=np.vdot(balanced,balanced).real/3
    return float(acquired),float(total-acquired),sigma

def evaluate(states,theta,m):
    b=np.sin(theta)**4;r=1-b;n=len(states)-1
    data=[];aold=0.;qold=1.
    for k,rho in enumerate(states):
        branches=rho if rho.ndim==3 else [rho]
        splits=[visibility_split(branch,m) for branch in branches]
        a=sum(x[0] for x in splits);q=sum(x[1] for x in splits)
        entry=dict(step=k,a=a,q=q,total=a+q)
        if k:
            entry['loss_P']=aold+b*qold-a
            entry['loss_Q']=r*qold-q
            entry['weighted_loss']=entry['loss_P']+(1-r**(n-k))*entry['loss_Q']
        data.append(entry);aold=a;qold=q
    loss=sum(x.get('weighted_loss',0) for x in data)
    summary=dict(theta=theta,m=m,n=n,final_a=aold,final_q=qold,
                 petz_twirl_error=.75*(1-aold),decoder_error_lower=.75*(1-np.sqrt(max(aold,0))),
                 weighted_loss=loss,ledger_residual=aold-(1-r**n-loss),
                 min_loss_P=min(x['loss_P'] for x in data[1:]),min_loss_Q=min(x['loss_Q'] for x in data[1:]),
                 q_half_life=next((x['step'] for x in data if x['q']<=.5),None),
                 q_one_tenth_life=next((x['step'] for x in data if x['q']<=.1),None))
    return dict(summary=summary,steps=data)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('policy');p.add_argument('--theta',type=float,required=True);p.add_argument('--m',type=int,required=True);p.add_argument('--out')
    a=p.parse_args();states=np.load(a.policy)['states'];result=evaluate(states,a.theta,a.m)
    if a.out:Path(a.out).write_text(json.dumps(result,indent=2))
    print(json.dumps(result['summary'],indent=2))
