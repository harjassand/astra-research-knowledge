"""Independent construction-team stress diagnostic, no import of author code.
Not a proof or receiving review. Symmetric-output Stinespring isometries certify
self-compatibility; mixes and common output unitaries preserve it.
"""
import json, math
from pathlib import Path
import numpy as np
from scipy.linalg import expm
rng=np.random.default_rng(610291654)
I=np.eye(2,dtype=complex)
P=np.array([[[0,1],[1,0]],[[0,-1j],[1j,0]],[[1,0],[0,-1]]],complex)
S=np.array([[1,0,0],[0,1/np.sqrt(2),0],[0,1/np.sqrt(2),0],[0,0,1]],complex)
base=np.array([[1,0],[0,0],[0,1]],complex)
def bloch(kraus):
    f=lambda X:sum((K@X@K.conj().T for K in kraus),np.zeros((2,2),complex))
    t=np.array([np.trace(p@f(I)).real/2 for p in P])
    T=np.array([[np.trace(p@f(q)).real/2 for q in P] for p in P])
    return T,t

def app(T,t,X):
    d=X.shape[0]//2; Z=X.reshape(2,d,2,d)
    C0=np.einsum('aiaj->ij',Z)
    C=np.array([np.einsum('ab,biaj->ij',p,Z) for p in P])
    Y=np.kron(I,C0)/2
    for i,p in enumerate(P):Y+=np.kron(p,t[i]*C0+np.einsum('j,jab->ab',T[i],C))/2
    return Y

def choi(T,t):
    v=np.array([1,0,0,1],complex)/np.sqrt(2)
    # app applies to first factor; resulting Choi ordering output,input.
    return app(T,t,np.outer(v,v.conj()))

def pt(J):return J.reshape(2,2,2,2).transpose(2,1,0,3).reshape(4,4)
def trace_dist(A,B):return np.sum(abs(np.linalg.eigvalsh((A-B+(A-B).conj().T)/2)))/2

def construct(T,t):
    M=np.eye(3)-T;s=np.linalg.solve(M,t)
    vals,vecs=np.linalg.eig(T.T)
    cand=[j for j,z in enumerate(vals) if abs(z.imag)<1e-9 and z.real>=.99]
    if not cand:return np.zeros((3,3)),s,np.linalg.inv(M),s,'far',None
    j=cand[0];lam=float(vals[j].real);g=1-lam
    w=vecs[:,j].real;w/=np.linalg.norm(w)
    z=np.eye(3)[np.argmin(abs(w))];v=z-w*np.dot(w,z);v/=np.linalg.norm(v)
    O=np.column_stack([w,v,np.cross(w,v)])
    A=O.T@T@O;ss=O.T@s;B=A[1:,1:];a=A[1:,0]
    h=np.linalg.solve(lam*np.eye(2)-B,a);n=np.r_[1,h];k=1-16*g
    TF0=k*np.outer(n,[1,0,0]);TF=O@TF0@O.T;tf=s-TF@s
    D=np.linalg.inv(np.eye(2)-B)
    L0=np.zeros((3,3));L0[0,0]=16;L0[1:,0]=(16*np.eye(2)-D)@h;L0[1:,1:]=D
    L=O@L0@O.T
    ends=[s+k*(q-w@s)*(O@n) for q in [-1,1]]
    return TF,tf,L,s,'near',ends

stats={'cases':0,'near':0,'far':0,'max_singular_compatibility_excess':0.,'max_fixed_residual':0.,'max_deficit_identity_residual':0.,'min_F_choi_eigenvalue':1.,'min_F_PPT_eigenvalue':1.,'max_endpoint_norm':0.,'max_near_L_operator_norm':0.,'max_reference_identity_residual':0.,'max_error_ratio':0.,'max_prior_radius':0.,'max_nonnormal_commutator_norm':0.}
for i in range(900):
    eps=10**rng.uniform(-5.5,-.2) if i<700 else 1.
    Z=base+eps*(rng.normal(size=(3,2))+1j*rng.normal(size=(3,2)))
    Q,R=np.linalg.qr(Z);V=S@Q
    ks=[V.reshape(2,2,2)[:,b,:] for b in range(2)]
    # Slight output gauge produces genuinely nonnormal recovered-like affine maps.
    angle=eps*rng.normal(size=3)
    U=expm(-.5j*np.einsum('j,jab->ab',angle,P))
    ks=[U@K for K in ks]
    T,t=bloch(ks)
    # Tiny pure replacements tilt the stationary prior along the preserved mode.
    if i%3==0:
        weight=10**rng.uniform(-5,-.7)
        axis=np.array([0,0,1.]) if i%2 else rng.normal(size=3)
        axis/=np.linalg.norm(axis)
        T=(1-weight)*T;t=(1-weight)*t+weight*axis
    TF,tf,L,s,kind,ends=construct(T,t)
    if np.linalg.norm(s)>1+1e-6:raise AssertionError(('nonphysical prior',i,s))
    J=choi(TF,tf)
    sv=np.linalg.svd(T,compute_uv=False)
    stats['cases']+=1;stats[kind]+=1
    stats['max_singular_compatibility_excess']=max(stats['max_singular_compatibility_excess'],sv[0]**2+sv[1]**2-1)
    stats['max_fixed_residual']=max(stats['max_fixed_residual'],np.linalg.norm(TF@s+tf-s))
    stats['max_deficit_identity_residual']=max(stats['max_deficit_identity_residual'],np.linalg.norm(np.eye(3)-TF-L@(np.eye(3)-T)))
    stats['min_F_choi_eigenvalue']=min(stats['min_F_choi_eigenvalue'],float(np.linalg.eigvalsh(J)[0]))
    stats['min_F_PPT_eigenvalue']=min(stats['min_F_PPT_eigenvalue'],float(np.linalg.eigvalsh(pt(J))[0]))
    stats['max_prior_radius']=max(stats['max_prior_radius'],float(np.linalg.norm(s)))
    stats['max_nonnormal_commutator_norm']=max(stats['max_nonnormal_commutator_norm'],float(np.linalg.norm(T@T.T-T.T@T)))
    if ends:
        stats['max_endpoint_norm']=max(stats['max_endpoint_norm'],*[float(np.linalg.norm(x)) for x in ends])
        stats['max_near_L_operator_norm']=max(stats['max_near_L_operator_norm'],float(np.linalg.norm(L,2)))
    for d in [1,2,3]:
        A=rng.normal(size=(2*d,2*d))+1j*rng.normal(size=(2*d,2*d));rho=A@A.conj().T;rho/=np.trace(rho)
        r=rho-app(T,t,rho);f=rho-app(TF,tf,rho)
        # Zero-trace-A input r makes app(L,0,r) implement L(I)=0.
        diff=np.linalg.norm(f-app(L,np.zeros(3),r))
        stats['max_reference_identity_residual']=max(stats['max_reference_identity_residual'],float(diff))
        den=trace_dist(rho,app(T,t,rho));num=trace_dist(rho,app(TF,tf,rho))
        if den>1e-13:stats['max_error_ratio']=max(stats['max_error_ratio'],float(num/den))
assert stats['max_singular_compatibility_excess']<1e-10
assert stats['max_deficit_identity_residual']<1e-8
assert stats['min_F_choi_eigenvalue']>-1e-7
assert stats['min_F_PPT_eigenvalue']>-1e-7
assert stats['max_endpoint_norm']<1+1e-7
assert stats['max_near_L_operator_norm']<24
assert stats['max_reference_identity_residual']<1e-8
Path(__file__).with_name('PARENT_GEOMETRY_CHECKS.json').write_text(json.dumps(stats,indent=2)+'\n')
print(json.dumps(stats,indent=2))
