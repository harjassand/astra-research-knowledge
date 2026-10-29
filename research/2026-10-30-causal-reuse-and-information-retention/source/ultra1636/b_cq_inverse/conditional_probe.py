"""Actual BKM conditional comparison on one prescribed binary cq channel.

This is a proposal-only finite arithmetic calculation, not a state certificate.
The parameter continuation is the fixed family of two reference blocks with
equal eigenvalues and variable relative eigenvectors; no new channel is used.
"""
import json
import time
from pathlib import Path
import numpy as np
from scipy.linalg import eigh

HERE=Path(__file__).resolve().parent

def bkm_matrix(base, tangents):
    ev,U=eigh(base)
    if ev.min()<=0: raise ValueError('positive baseline required')
    a=ev[:,None]; b=ev[None,:]
    coef=np.empty_like(a+b)
    close=np.abs(a-b)<=1e-10*np.maximum(a,b)
    np.divide(np.log(a)-np.log(b),a-b,out=coef,where=~close)
    coef[close]=(2/(a+b))[close]
    T=np.array([U.conj().T@H@U for H in tangents])
    return np.einsum('aij,bij,ij->ab',T.conj(),T,coef).real

def matrices(A,B):
    # Exact source tau0=|0><0|, tau1=|+><+| in the displayed basis.
    tau0=np.array([[1.,0],[0,0]])
    tau1=np.ones((2,2))/2
    basis=[np.eye(2)/np.sqrt(2),np.diag([1.,-1])/np.sqrt(2),
           np.array([[0.,1],[1,0]])/np.sqrt(2),
           np.array([[0.,-1j],[1j,0]])/np.sqrt(2)]
    Z=np.zeros((2,2),complex)
    # Trace-zero pair basis: common identity removed.
    pairs=[(basis[0]/np.sqrt(2),-basis[0]/np.sqrt(2))]
    pairs += [(b,Z) for b in basis[1:]]+[(Z,b) for b in basis[1:]]
    tin=[np.block([[a,Z],[Z,b]]) for a,b in pairs]
    tout=[np.kron(tau0,a)+np.kron(tau1,b) for a,b in pairs]
    tref=[a+b for a,b in pairs]
    Mi=bkm_matrix(np.block([[A,Z],[Z,B]]),tin)
    Mo=bkm_matrix(np.kron(tau0,A)+np.kron(tau1,B),tout)
    Mr=bkm_matrix(A+B,tref)
    return Mi,Mo,Mr,pairs

def proposal(A,B):
    Mi,Mo,Mr,pairs=matrices(A,B)
    Ci=(Mi-Mr+Mi.T-Mr.T)/2
    Co=(Mo-Mr+Mo.T-Mr.T)/2
    w,U=eigh(Ci)
    keep=w>1e-9*w.max()
    W=U[:,keep]/np.sqrt(w[keep])
    vals,vec=eigh(W.T@Co@W)
    v=W@vec[:,0]
    H0=sum((x*p[0] for x,p in zip(v,pairs)),np.zeros((2,2),complex))
    H1=sum((x*p[1] for x,p in zip(v,pairs)),np.zeros((2,2),complex))
    return {'minimum_conditional_retention':float(vals[0]),
            'maximum_conditional_reverse':float(1/vals[0]),
            'ci_eigenvalues':w.tolist(),
            'half_comparison_min_eigenvalue':float(eigh(Co-.5*Ci,eigvals_only=True)[0]),
            'H0_real':H0.real.tolist(),'H0_imag':H0.imag.tolist(),
            'H1_real':H1.real.tolist(),'H1_imag':H1.imag.tolist(),
            'all_D_half_min_eigenvalue':float(eigh(Mo-.5*Mi,eigvals_only=True)[0])}

def main():
    begin=time.perf_counter()
    # Three scales of one analytic small-eigenvalue continuation. The angle is
    # fixed pi/4; commuting endpoints are included as mathematical controls.
    R=np.array([[1.,-1],[1,1]])/np.sqrt(2)
    records=[]
    for e in [1/10,1/100,1/10000]:
        A=np.diag([1.,e]); B=R@A@R.T
        out=proposal(A,B)
        records.append({'small_eigenvalue':e,'reference_rotation':'pi/4',**out})
    out={'status':'UNTRUSTED_BINARY64_PROPOSAL_ONLY','fixed_channel':'0,+',
         'family':'A=diag(1,e), B=R(pi/4) A R*', 'records':records,
         'seconds_after_imports':time.perf_counter()-begin}
    (HERE/'CONDITIONAL_PROBE.json').write_text(json.dumps(out,indent=2)+'\n')
    for r in records:
        print(r['small_eigenvalue'],r['maximum_conditional_reverse'],
              r['half_comparison_min_eigenvalue'])

if __name__=='__main__': main()
