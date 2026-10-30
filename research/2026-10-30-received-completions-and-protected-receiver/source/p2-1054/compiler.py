"""Exact calibrated dirty-spin mediator compiler, constructed in this turn.

Conventions: R_j(t)=exp(-i*t*P_j), normalized involutions.
Sequences are stored in matrix-product order (rightmost executes first).
Only the signed native A, B, C handles are used.
"""
import math
import numpy as np
from functools import reduce

I=np.eye(2,dtype=complex)
X=np.array([[0,1],[1,0]],dtype=complex)
Y=np.array([[0,-1j],[1j,0]],dtype=complex)
Z=np.diag([1.,-1.]).astype(complex)
def kron(*xs): return reduce(np.kron,xs)
def spin(v): return sum(x*p for x,p in zip(v,[X,Y,Z]))
def controls(v):
    return [kron(X,I,spin(v[0])),kron(I,X,spin(v[1])),kron(Y,I,spin(v[2]))]

def inv(seq): return [(j,-a) for j,a in reversed(seq)]

def merge(seq, tol=1e-14):
    out=[]
    for j,a in seq:
        if abs(a)<tol: continue
        if out and out[-1][0]==j:
            a+=out.pop()[1]
        if abs(a)>=tol: out.append((j,float(a)))
    return out

def bisector_angles(theta,s):
    """N1=s*F+r*E, N2=s*F-r*E. N1(a)N2(b)N1(a)=F(theta).

    Requires |theta|<=pi/2 and |sin(theta)|<=2s, using the positive cosine
    branch for beta. E and F are anticommuting Hermitian involutions.
    """
    assert 0 < s <= 1+1e-12
    assert abs(theta)<=math.pi/2+1e-12
    z=math.sin(theta)/(2*s)
    assert abs(z)<=1+1e-12,(theta,s,z)
    beta=math.asin(max(-1,min(1,z)))
    k=2*s*s-1
    alpha=.5*(math.atan2(s*math.sin(theta),math.cos(theta))-
              math.atan2(k*math.sin(beta),math.cos(beta)))
    return alpha,beta

def subdivisions(theta,s, margin=0.8):
    # Keep away from the inverse-sine endpoint for stable calibration.
    cap=math.asin(min(1.,2*margin*s))
    cap=min(cap,math.pi/2)
    return max(1,math.ceil(abs(theta)/cap))

def cross_rotation(phi,s23,margin=.8):
    """exp(-i phi Y1 X2 (n2 cross n3).sigma / s23)."""
    m=subdivisions(phi,s23,margin)
    a,b=bisector_angles(phi/m,s23)
    word=[(1,math.pi/4),(2,a),(1,-math.pi/2),(2,-b),
          (1,math.pi/2),(2,a),(1,-math.pi/4)]
    return merge(word*m)

def target_rotation(theta,s23,kappa,margin=.8):
    """exp(-i theta Z1 X2), kappa=n1.(n2 cross n3)>0."""
    d=kappa/s23
    m=subdivisions(theta,d,margin)
    a,b=bisector_angles(theta/m,d)
    word=[(0,math.pi/4)]+cross_rotation(a,s23,margin)+[(0,-math.pi/2)]+\
         cross_rotation(-b,s23,margin)+[(0,math.pi/2)]+\
         cross_rotation(a,s23,margin)+[(0,-math.pi/4)]
    return merge(word*m)

def unitary(seq,gs):
    U=np.eye(gs[0].shape[0],dtype=complex)
    for j,a in seq:
        U=U@(np.cos(a)*np.eye(len(U))-1j*np.sin(a)*gs[j])
    return U

def inspect(v,theta=math.pi/4):
    v=np.asarray(v,dtype=float);v=v/np.linalg.norm(v,axis=1)[:,None]
    gs=controls(v)
    s=np.linalg.norm(np.cross(v[1],v[2]));k=float(np.linalg.det(v))
    if k<=0: v[0]*=-1;gs=controls(v);k=-k
    seq=target_rotation(theta,s,k)
    target=np.cos(theta)*np.eye(8)-1j*np.sin(theta)*kron(Z,X,I)
    error=np.linalg.norm(unitary(seq,gs)-target,ord=2)
    return {'s23':s,'kappa':k,'pulses':len(seq),'action':sum(abs(a) for _,a in seq),
            'error':error,'sequence':seq}

if __name__=='__main__':
    rng=np.random.default_rng(270130)
    examples=[np.eye(3),np.array([[1,0,0],[.3,np.sqrt(.91),0],[.2,.4,np.sqrt(.8)]]),
              np.array([[1,0,0],[0,1,0],[0,.3,np.sqrt(.91)]]),
              np.array([[1,0,0],[0,1,0],[.2,0,np.sqrt(.96)]])]
    for v in examples:
        r=inspect(v); print({k:v for k,v in r.items() if k!='sequence'})
    maxerr=0.;maxp=0
    for _ in range(300):
        v=rng.normal(size=(3,3));v/=np.linalg.norm(v,axis=1)[:,None]
        if abs(np.linalg.det(v))<.015: continue
        r=inspect(v,theta=rng.uniform(-math.pi/2,math.pi/2))
        maxerr=max(maxerr,r['error']);maxp=max(maxp,r['pulses'])
    print('random_check_max_error',maxerr,'max_pulses',maxp)
