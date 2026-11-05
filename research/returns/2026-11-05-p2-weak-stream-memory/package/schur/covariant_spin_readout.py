#!/usr/bin/env python3
"""Exact optimal covariant qubit readout from a qubit tensor spin-J memory.
Input q is the possibly subnormalized reference/memory Choi state, in order
reference qubit, receiver qubit, spin-J (highest m first).
"""
import math,json
from pathlib import Path
import numpy as np
from fusion_probe import cg_maps,PAULIS

def embeddings(j):
    d=round(2*j+1);out={}
    for direction,Cdag in cg_maps(j).items():
        k=j+direction*.5;dk=round(2*k+1)
        C=Cdag.conj().T.reshape(d,2,dk).transpose(1,0,2).reshape(2*d,dk)
        for sign,Ddag in cg_maps(k).items():
            ell=k+sign*.5;dl=round(2*ell+1)
            D=Ddag.conj().T.reshape(dk,2,dl).transpose(1,0,2).reshape(2*dk,dl)
            out[(round(2*ell),round(2*k))]=np.kron(np.eye(2),C)@D
    return out

def time_reversal(j):
    d=round(2*j+1);T=np.zeros((d,d),complex)
    for m in range(d):T[d-1-m,m]=(-1)**m
    return T

def optimal_readout(q,j,return_choi=False):
    d=round(2*j+1);M=2*d
    if q.ndim==4:q=q.reshape(2*M,2*M)
    Q=np.kron(PAULIS[2],np.eye(M));inv=Q@q@Q.conj().T
    W=embeddings(j);twoj=round(2*j);blocks={}
    for ell in sorted(set(a for a,b in W)):
        ks=sorted(k for e,k in W if e==ell)
        B=np.array([[np.trace(W[(ell,k)].conj().T@inv@W[(ell,kp)])/(ell+1)
                     for kp in ks] for k in ks])
        blocks[ell]=(ks,(B+B.conj().T)/2)
    if j==0:
        choice=max(blocks,key=lambda e:blocks[e][1][0,0].real)
        fe=float(blocks[choice][1][0,0].real)
        Dblocks={e:np.array([[2/(e+1) if e==choice else 0]],complex) for e in blocks}
        params={'total_spin_choice':choice/2}
    else:
        dm=2*j;dp=2*j+2;dj=2*j+1;B=blocks[twoj][1]
        aa=float(blocks[twoj-2][1][0,0].real) if twoj>=2 else 0.0
        cc=float(blocks[twoj+2][1][0,0].real)
        A=dm*(B[0,0].real-aa);C=dp*(B[1,1].real-cc)
        H=math.sqrt(dm*dp)*abs(B[0,1])
        cand=[(1.,0.),(1.,1.)]
        if j>=1:cand.extend([(0.,0.),(0.,1.)])
        if C<0 and 0<=-H/C<=1:cand.append((1.,float(-H/C)))
        if j>=1 and A<0 and 0<=-H/A<=1:cand.append((float(-H/A),1.))
        r,t=max(cand,key=lambda z:A*z[0]**2+C*z[1]**2+2*H*z[0]*z[1])
        x,y=r*r,t*t;fe=float((dm*aa+dp*cc+A*x+C*y+2*H*r*t)/2)
        phase=-float(np.angle(B[0,1])) if H>1e-30 else 0.0
        off=math.sqrt(dm*dp)*r*t*np.exp(1j*phase)/dj
        Dblocks={twoj:np.array([[dm*x/dj,off],[off.conjugate(),dp*y/dj]])}
        if j>=1:Dblocks[twoj-2]=np.array([[dm*(1-x)/(2*j-1)]])
        Dblocks[twoj+2]=np.array([[dp*(1-y)/(2*j+3)]])
        params={'x':x,'y':y,'shared_block_phase':phase}
    result={'optimal_entanglement_fidelity':fe,'branch_probability':float(np.trace(q).real),'parameters':params}
    if return_choi:
        Cdec=np.zeros((2*M,2*M),complex)
        for ell,Dblock in Dblocks.items():
            ks=blocks[ell][0]
            for a,k in enumerate(ks):
                for b,kp in enumerate(ks):Cdec+=Dblock[a,b]*W[(ell,k)]@W[(ell,kp)].conj().T
        T=np.kron(np.eye(2),np.kron(time_reversal(.5),time_reversal(j)))
        Cdec=T.conj().T@Cdec@T
        result['decoder_choi']=Cdec
        result['direct_fidelity']=float(np.trace(q.T@Cdec).real/2)
        result['TP_residual']=float(np.linalg.norm(np.trace(Cdec.reshape(2,M,2,M),axis1=0,axis2=2)-np.eye(M)))
    return result

def verify():
    rng=np.random.default_rng(20261104);records=[]
    for j in [0,.5,1,1.5,2,3]:
        d=round(2*j+1);M=2*d;W=embeddings(j)
        for rep in range(8):
            q=np.zeros((2*M,2*M),complex)
            for ell in sorted(set(a for a,b in W)):
                ks=sorted(k for e,k in W if e==ell)
                Z=rng.normal(size=(len(ks),len(ks)))+1j*rng.normal(size=(len(ks),len(ks)))
                B=Z@Z.conj().T
                for a,k in enumerate(ks):
                    for b,kp in enumerate(ks):q+=B[a,b]*W[(ell,k)]@W[(ell,kp)].conj().T
            q/=np.trace(q);Y=np.kron(PAULIS[2],np.eye(M));q=Y@q@Y.conj().T
            r=optimal_readout(q,j,True);err=abs(r['direct_fidelity']-r['optimal_entanglement_fidelity'])
            mineig=float(np.linalg.eigvalsh(r['decoder_choi']).min())
            assert err<1e-11,(j,err,r)
            assert r['TP_residual']<1e-11
            assert mineig>-1e-11
            records.append({'J':j,'fidelity_formula_residual':err,'TP_residual':r['TP_residual'],'minimum_decoder_choi_eigenvalue':mineig})
        bell=np.array([1,0,0,1],complex)/math.sqrt(2)
        q=np.kron(np.outer(bell,bell.conj()),np.eye(d)/d)
        r=optimal_readout(q,j,True)
        assert abs(r['optimal_entanglement_fidelity']-1)<1e-11
    result={'scope':'48 random finite covariant Choi states plus six identity-with-spin-gauge channels; exact formula and constructed decoder CP/TP checks.',
            'max_fidelity_formula_residual':max(r['fidelity_formula_residual'] for r in records),
            'max_TP_residual':max(r['TP_residual'] for r in records),'records':records}
    Path(__file__).with_name('covariant_spin_readout_receipt.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='records'},indent=2))

if __name__=='__main__':verify()
