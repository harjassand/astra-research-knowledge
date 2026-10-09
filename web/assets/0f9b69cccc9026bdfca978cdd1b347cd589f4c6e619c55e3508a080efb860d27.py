#!/usr/bin/env python3
"""Independent Lyapunov CP--KMS quadratic-form falsification search.

Every tested direction specifies a legal KMS generator, rather than an
arbitrary PSD Hilbert--Schmidt matrix. Numerical diagnostics are not proof.
"""
from pathlib import Path
import json
import numpy as np

HERE=Path(__file__).resolve().parent


def hermitian_basis(d):
    bs=[]
    for i in range(d):
        for j in range(i):
            x=np.zeros((d,d),complex)
            x[i,j]=x[j,i]=1/np.sqrt(2)
            bs.append(x)
            x=np.zeros((d,d),complex)
            x[i,j]=1j/np.sqrt(2)
            x[j,i]=-1j/np.sqrt(2)
            bs.append(x)
    for k in range(1,d):
        x=np.zeros((d,d),complex)
        x[np.arange(k),np.arange(k)]=1/np.sqrt(k*(k+1))
        x[k,k]=-k/np.sqrt(k*(k+1))
        bs.append(x)
    return np.array(bs)


def gram(basis,C,D):
    result=np.einsum('iab,bc,jcd,da->ij',basis,C,basis,D)
    return ((result+result.T)/2).real


def evaluate(sigma, rho, basis):
    vals,U=np.linalg.eigh(rho)
    if vals.min()<=0:
        raise ValueError('rho not faithful')
    R=(U*np.sqrt(vals))@U.conj().T
    logs=(U*np.log(vals))@U.conj().T-np.diag(np.log(sigma))
    s=np.diag(np.sqrt(sigma))
    d=np.power(sigma,.25)
    X=rho/np.outer(d,d)
    Y=logs*np.outer(d,d)
    C=(X@Y+Y@X)/2-2*rho
    Z=2*C/(np.sqrt(sigma)[:,None]+np.sqrt(sigma)[None,:])
    F=gram(basis,s,Z)-gram(basis,X,Y)+2*gram(basis,R,R)
    W=2*rho/(np.sqrt(sigma)[:,None]+np.sqrt(sigma)[None,:])
    E=gram(basis,s,W)-gram(basis,R,R)
    es,Q=np.linalg.eigh(E)
    fs,V=np.linalg.eigh(F)
    scale=max(1,np.linalg.norm(F,2),np.linalg.norm(E,2))
    out={"F_min":float(fs[0]),"scale":float(scale),"E_min":float(es[0]),
         "F_direction":V[:,0].tolist()}
    keep=es>1e-9*max(1,es[-1])
    if keep.any():
        inverse=Q[:,keep]/np.sqrt(es[keep])
        relative=inverse.T@(F+2*E)@inverse
        rs,vec=np.linalg.eigh(relative)
        out['min_J_over_E']=float(rs[0])
        out['ratio_direction']=(inverse@vec[:,0]).tolist()
    return out


def state(rng,d,purity_kind):
    A=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d))
    if purity_kind==0:
        raw=A@A.conj().T
    else:
        raw=np.outer(A[:,0],A[:,0].conj())
        eps=[.01,.1,.3,.7][purity_kind-1]
        raw=(1-eps)*raw/np.trace(raw).real+eps*np.eye(d)/d
    return raw/np.trace(raw).real


def serialize_complex(A):
    return [[[float(z.real),float(z.imag)] for z in row] for row in A]


def main():
    rng=np.random.default_rng(6006301)
    records=[]
    counts={}
    for dA,dB,num in [(3,1,6000),(2,2,6000),(3,2,2500),(4,1,2500)]:
        d=dA*dB
        basisA=hermitian_basis(dA)
        basis=basisA if dB==1 else np.array([np.kron(B,np.eye(dB)) for B in basisA])
        best=None
        for k in range(num):
            expA=rng.uniform(-6,0,dA)
            expA[0]=0
            weightsA=10**expA
            sigmaA=weightsA/weightsA.sum()
            if dB>1:
                expB=rng.uniform(-4,0,dB)
                expB[0]=0
                weightsB=10**expB
                sigmaB=weightsB/weightsB.sum()
                sigma=np.kron(sigmaA,sigmaB)
            else:
                sigmaB=np.array([1.])
                sigma=sigmaA
            rho=state(rng,d,k%5)
            ev=evaluate(sigma,rho,basis)
            score=ev.get('min_J_over_E',np.inf)
            if best is None or score<best['min_J_over_E']:
                best=dict(ev,dA=dA,dB=dB,index=k,sigmaA=sigmaA.tolist(),
                          sigmaB=sigmaB.tolist(),rho=serialize_complex(rho))
            if ev['F_min'] < -1e-8*ev['scale']:
                counter=dict(ev,dA=dA,dB=dB,index=k,sigmaA=sigmaA.tolist(),
                             sigmaB=sigmaB.tolist(),rho=serialize_complex(rho))
                records.append(counter)
                print(json.dumps({"counterexample_candidate":counter},indent=2))
                break
        else:
            k=num-1
        counts[f'{dA}x{dB}']=k+1
        records.append(dict(best,record_kind='best_ratio_in_scope'))
    result={'status':'FINITE_NUMERICAL_SEARCH_ONLY','seed':6006301,
            'no_sibling_cycle06_read':True,'states_per_scope':counts,
            'records':records,'universal_status':'UNRESOLVED'}
    (HERE/'quadratic_search.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'states_per_scope':counts,
                      'best_ratios':[{'scope':f"{r['dA']}x{r['dB']}",
                                      'ratio':r.get('min_J_over_E'),
                                      'F_min':r['F_min']} for r in records]},indent=2))


if __name__=='__main__':
    main()
