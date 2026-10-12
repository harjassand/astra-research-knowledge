"""Finite diagnostics for the local exact-null certificate and far-end escape.
Not a general proof, interval certification, or a laboratory experiment.
"""
from __future__ import annotations
import json, math
from pathlib import Path
import numpy as np
from scipy.linalg import eigh
from check_core import construct, oneparticle

OUT=Path(__file__).parent

def run() -> None:
    rng=np.random.default_rng(583019)
    count=0
    def check(condition: bool, label: str) -> None:
        nonlocal count
        if not bool(condition):
            raise AssertionError(label)
        count += 1
    max_ratio=0.0
    for dim in [2,3,5,9]:
      for scale in [1.8,0.12,0.003]:
       for trial in range(6):
        Z=rng.normal(size=(dim,dim))+1j*rng.normal(size=(dim,dim))
        C=(Z+Z.conj().T)/2
        C*=scale/np.linalg.norm(C,2)
        es,Q=eigh(C); weights=abs(Q[0,:])**2
        mu2=np.dot(weights,es**2)
        for h in [.1,.5]:
            p=np.dot(weights,1-np.cos(h*es))/2
            check(p+2e-15>=h*h*mu2/8,'short-time second-moment bound')
            for T in [1.,7.,23.]:
                ts=np.linspace(0,T,81)
                Fs=np.exp(-1j*ts[:,None]*es[None,:])@weights
                Dloc=.5*np.sqrt((1-abs(Fs)**2)**2+abs(1-Fs)**2)
                Dvecsq=1-Fs.real
                bound=4*T*T*p/(h*h)
                check(np.max(Dloc**2)<=bound+2e-12,'local trajectory certificate')
                check(np.max(Dvecsq)<=T*T*mu2/2+2e-12,'vector residual bound')
                if bound>1e-14:
                    max_ratio=max(max_ratio,float(np.max(Dloc**2)/bound))
    # Nontrivial exactly agreeing generator outside the predictive subspace.
    for dim in [3,5,9]:
        C=np.zeros((dim,dim))
        block=rng.normal(size=(dim-1,dim-1))
        block=(block+block.T)/2
        block*=1.7/np.linalg.norm(block,2)
        C[1:,1:]=block
        es,Q=eigh(C); weights=Q[0,:]**2
        for t in [.1,.5,13,107]:
            F=np.dot(weights,np.exp(-1j*t*es))
            check(abs(F-1)<1e-12,'exact-null outside-subspace freedom')
    endpoint=[]
    for d in [1,2,4,8,16]:
      for eta in ['0.125','0.04']:
        c=construct(d,eta)
        for rounded in [False,True]:
            C0,C1,_,q=oneparticle(c,rounded)
            ev0,Q0=eigh(C0); ev1,Q1=eigh(C1)
            w0=Q0[d,:]**2; w1=Q1[d,:]**2
            for t in [.01,1/32]:
                F0=np.dot(w0,np.exp(-1j*t*ev0)); F1=np.dot(w1,np.exp(-1j*t*ev1))
                diff=abs(F0.imag-F1.imag)
                check(diff>=t/4-1e-12,'far-end one-qubit signal')
                endpoint.append({'d':d,'eta':eta,'rounded':rounded,'t':t,'signal':float(diff)})
    # A finite, explicitly encoded instance. Floating rounding is diagnostic only.
    c=construct(4,'0.125'); C0,C1,perm,q=oneparticle(c,True)
    b=int(round(-math.log2(q)))
    ints0=np.rint(C0/q).astype(np.int64)
    check(np.max(abs(C0-ints0*q))==0,'exact binary encoding of example')
    example={
      'status':'finite dyadic example from numerical construction, not an interval-certified compiler',
      'd':4,'eta':'1/8','T':int(c['T']),'qubits':10,
      'labels':['L0','L1','L2','L3','L4','R0','R1','R2','R3','R4'],
      'denominator_power_of_two':b,
      'C_good_integer_numerators':ints0.tolist(),
      'reflection_permutation':perm.tolist(),
      'C_bad_definition':'P C_good P^T using the displayed permutation',
      'H_definition':'onsite (1+C_xx)*n_x; edge C_xy*(sigma+_x sigma-_y+h.c.); plus n_x*n_y on each nonzero edge',
      'candidate':'K=sum_x n_x',
      'initial_state':'|+> on L0, |0> everywhere else',
      'prediction':'reduced L0 density trajectory on [0,T]'
    }
    (OUT/'example_d4.json').write_text(json.dumps(example,indent=2))
    report={'status':'PASS','scope':'finite floating-point diagnostics only','seed':583019,
            'assertions':count,'maximum_certificate_ratio':max_ratio,
            'endpoint_checks':endpoint}
    (OUT/'interface_diagnostics.json').write_text(json.dumps(report,indent=2))
    print(json.dumps({k:v for k,v in report.items() if k!='endpoint_checks'},indent=2))

if __name__=='__main__':
    run()
