"""Finite dense checks of the retained-subset Gram identity.

The proof is analytic; these floating-point checks only check normalization
and the recurrence for small instances. They are not memory lower bounds.
"""
import numpy as np
import itertools, json
from pathlib import Path
from spectrum import swap_matrix

paulis=[np.array([[0,1],[1,0]],complex),np.array([[0,-1j],[1j,0]],complex),np.diag([1.,-1.])]

def ptrace(a,keep,q):
    a=a.reshape([2]*(2*q))
    for t in reversed(range(q)):
        if t not in keep:
            a=np.trace(a,axis1=t,axis2=t+a.ndim//2)
    return a.reshape(2**len(keep),2**len(keep))

def check(n,theta,keep):
    d=2**n
    u=np.eye(2*d,dtype=complex)
    for j in range(1,n+1):
        w=swap_matrix(n+1,0,j)
        u=np.cos(theta)*u+1j*np.sin(theta)*(w@u)
    k=len(keep)
    bs=[ptrace(u@np.kron(p,np.eye(d))@u.conj().T,keep,n+1)/2**(n+1-k) for p in paulis]
    gram=np.array([[np.trace(a.conj().T@b)/2**k for b in bs] for a in bs])
    residual,alpha=1.,0.
    b=np.sin(theta)**4
    for j in range(1,n+1):
        if j in keep:
            alpha+=b*residual
            residual*=1-b
        else:
            residual*=np.cos(theta)**4
    return float(np.max(np.abs(gram-alpha*np.eye(3))))

def iid_alpha(theta,N,loss):
    b=np.sin(theta)**4
    g=1-np.cos(theta)**4
    rate=(1-loss)*b+loss*g
    return (1-loss)*b*(-np.expm1(N*np.log1p(-rate)))/rate

if __name__=='__main__':
    errs=[]
    for n in range(1,6):
        for theta in [.1,.4,.9]:
            for bits in itertools.product([False,True],repeat=n):
                keep=[j+1 for j,x in enumerate(bits) if x]
                errs.append(check(n,theta,keep))
    rows=[]
    for theta in [.1,.2,.4]:
        for loss in [0.,1e-5,1e-4,1e-3,.01]:
            N=int(np.ceil(np.log(.75/.01)/(-np.log1p(-np.sin(theta)**4))))
            a=iid_alpha(theta,N,loss)
            b=np.sin(theta)**4
            g=1-np.cos(theta)**4
            ainf=(1-loss)*b/((1-loss)*b+loss*g)
            rows.append(dict(theta=theta,loss=loss,N=N,visibility=a,error_explicit=.75*(1-a),error_converse=.75*(1-np.sqrt(a)),asymptotic_error_explicit=.75*(1-ainf),asymptotic_error_converse=.75*(1-np.sqrt(ainf))))
    result=dict(cases=len(errs),max_gram_entry_error=max(errs),rows=rows)
    print(json.dumps(result,indent=2))
    with Path(__file__).with_name('erasure_results.json').open('w') as f:
        json.dump(result,f,indent=2)
