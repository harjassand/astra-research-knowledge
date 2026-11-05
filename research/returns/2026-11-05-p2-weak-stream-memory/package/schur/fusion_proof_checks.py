#!/usr/bin/env python3
"""Finite checks of the exact pair-label formulas, not a target reader test."""
import math,json
from pathlib import Path
import numpy as np

def swap(n,a,b):
    out=np.zeros((2**n,2**n),complex)
    for v in range(2**n):
        bits=[(v>>(n-1-k))&1 for k in range(n)]
        bits[a],bits[b]=bits[b],bits[a]
        w=sum(t<<(n-1-k) for k,t in enumerate(bits))
        out[w,v]=1
    return out

Z=np.diag([1,-1]).astype(complex)
results=[]
for theta in [.1,.3,.6,1.0]:
    c,s=math.cos(theta),math.sin(theta);x=s*s
    b=x*x*(2-x)**2/2
    h=(1-x)**2*(1+2*x)
    q=1-x*x+x**4/2
    for k in [1,2,3]:
        n=2*k;D=2**(n+1);I=np.eye(D)
        A=np.kron(Z,np.eye(2**n))
        for j in range(1,n+1):
            U=c*I+1j*s*swap(n+1,0,j)
            A=U@A@U.conj().T
            if j%2==0:
                P=swap(n+1,j-1,j)
                A=(A+P@A@P)/2
        B=np.trace(A.reshape(2,2**n,2,2**n),axis1=0,axis2=2)/2
        p=float(np.trace(B@B).real/(2**n))
        total=float(np.trace(A@A).real/D)
        expected=b*sum(h**j for j in range(k))
        results.append({'theta':theta,'pairs':k,'bath_gram':p,'formula_bath_gram':expected,
                        'total_gram':total,'formula_total_gram':expected+h**k,
                        'bath_error':abs(p-expected),'total_error':abs(total-expected-h**k)})
    P=swap(3,1,2);Ps=(np.eye(8)-P)/2;Pt=(np.eye(8)+P)/2
    U=(c*np.eye(8)+1j*s*swap(3,0,2))@(c*np.eye(8)+1j*s*swap(3,0,1))
    leak=float(np.linalg.norm(Ps@U@Pt,2))
    assert abs(leak-math.sqrt(3)*x/2)<1e-12
assert max(r['bath_error'] for r in results)<1e-12
assert max(r['total_error'] for r in results)<1e-12
data={'scope':'Finite 2,4,6-carrier matrix verification of derived pair-label identities.',
      'weak_limit_error_floor':.75*(1-math.sqrt(2/3)),
      'results':results}
target=Path(__file__).with_name('fusion_proof_receipt.json')
target.write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps({'max_bath_error':max(r['bath_error'] for r in results),
                  'max_total_error':max(r['total_error'] for r in results),
                  'weak_limit_error_floor':data['weak_limit_error_floor']},indent=2))
