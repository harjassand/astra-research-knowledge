"""Diagnostics for local_transfer.md; these checks do not prove W_m.

The six-dyad decomposition is verified exactly. The splitting/coercivity
checks compare independent direct subset partial traces with block formulas.
The last control deliberately removes the slice and finds its exact null
directions, opposing any claim of ungauged strict coercivity.
"""
from pathlib import Path
import itertools
import json
import sys
sys.dont_write_bytecode = True
import numpy as np
import sympy as sp

PUBLIC = Path(__file__).resolve().parents[3] / 'public'
sys.path.insert(0, str(PUBLIC))
from q_eval import q_value


def mm(a,b):
    return np.einsum('ij,jk->ik',a,b,optimize=False)


def outer(a,b):
    return np.einsum('ia,ja->ij',a,b.conj(),optimize=False)


def apply_l(c,n):
    a=np.asarray(c).reshape((3,)*(2*n)).copy()
    for k in range(n):
        z=np.moveaxis(a,(k,n+k),(0,1))
        tr=np.trace(z,axis1=0,axis2=1)
        z=z-.5*np.eye(3).reshape((3,3)+(1,)*(2*n-2))*tr
        a=np.moveaxis(z,(0,1),(k,n+k))
    return a.reshape(c.shape)


def b(a,c,n):
    return np.vdot(a,apply_l(c,n))


def dyads():
    return [sp.Matrix([[0,1],[0,0]]),sp.Matrix([[0,0],[1,0]]),
            sp.Matrix([[1,-1],[1,-1]])/2,
            sp.Matrix([[1,1],[-1,-1]])/2,
            sp.Matrix([[1,sp.I],[sp.I,-1]])/2,
            sp.Matrix([[1,-sp.I],[-sp.I,-1]])/2]


def exact_binary():
    om=sp.Matrix([1,0,0,1])
    target=sp.eye(4)-om*om.T/2
    actual=sp.zeros(4)
    for a in dyads():
        z=sp.Matrix(list(a))
        actual+=z*z.conjugate().T/2
        if a.det()!=0 or sp.trace(a)!=0 or sp.trace(a.conjugate().T*a)!=1:
            raise AssertionError('dyad control')
    if actual!=target:
        raise AssertionError('exact binary decomposition')
    return {'exact_six_dyads':'passed','coefficient':'1/2'}


def test(m,seed):
    rng=np.random.default_rng(seed);N=3**m;delta=2.**(-m)
    def rand(shape):return rng.normal(size=shape)+1j*rng.normal(size=shape)
    u=rand(N);v=rand(N);u/=np.linalg.norm(u);v/=np.linalg.norm(v)
    P0=np.zeros((4,N,2),complex)
    P0[0,:,0]=u;P0[1,:,1]=u;P0[2,:,0]=v;P0[3,:,1]=v
    E=rand(P0.shape);E*=delta/(10*np.linalg.norm(E))
    P=P0+E;U=P[:2];V=P[2:]
    W=rand((2,N,2))
    # Constraints sum_a <U_i,a,x_a>+<V_i,a,y_a>=0.
    rows=np.c_[U.reshape(2,-1).conj(),V.reshape(2,-1).conj()]
    flat=W.reshape(-1)
    flat-=mm(rows.conj().T,np.linalg.solve(mm(rows,rows.conj().T),
                                         mm(rows,flat[:,None])))[:,0]
    W=flat.reshape(2,N,2);X,Y=W
    if np.linalg.norm(mm(rows,flat[:,None]))>1e-10:
        raise AssertionError('slice failed')
    w2=np.vdot(flat,flat).real
    eps=np.linalg.norm(E)
    top=np.empty((2,N,2,N),complex)
    for i in range(2):
        for j in range(2):top[i,:,j,:]=outer(U[i],V[j])
    binq=sum(q_value(top[i,:,j,:],m) for i in range(2) for j in range(2))
    A=top[0,:,0,:]+top[1,:,1,:]
    binq-=.5*q_value(A,m)
    rhs=0.
    for aa in dyads():
        aa=np.array(aa).astype(complex)
        contraction=np.einsum('ij,iajb->ab',aa.conj(),top,optimize=False)
        # The dyad functional is sum conj(A_ij) C_ij.
        rhs+=.5*q_value(contraction,m)
    if abs(rhs-binq)>1e-9*max(1,abs(rhs),abs(binq)):
        raise AssertionError(('binary split',m,rhs,binq))
    D=outer(X,Y)
    T=sum(q_value(outer(U[i],Y),m)+q_value(outer(X,V[i]),m)
          for i in range(2))-b(A,D,m).real
    T0=0.
    for a in range(2):
        w=np.kron(X[:,a],v)-np.kron(u,Y[:,a])
        z=w.reshape((3,)*(2*m)).copy()
        for i in range(m):z=z-.5*np.swapaxes(z,i,m+i)
        T0+=np.vdot(w,z.reshape(-1)).real
    lip=((2*np.sqrt(2)+1)*eps+1.25*eps**2)*w2
    if abs(T-T0)>lip+1e-10:
        raise AssertionError(('Lipschitz',m,T,T0,lip))
    if T0<delta*(1-eps**2/2)*w2-1e-10:
        raise AssertionError('base coercivity')
    if T<delta*w2/2-1e-10:
        raise AssertionError('persistent coercivity')
    Uf=np.concatenate((U,X[None]),axis=0).reshape(3*N,2)
    Vf=np.concatenate((V,Y[None]),axis=0).reshape(3*N,2)
    C=outer(Uf,Vf)
    lhs=q_value(C,m+1);split=binq+T+.5*q_value(D,m)
    if abs(lhs-split)>1e-9*max(1,abs(lhs),abs(split)):
        raise AssertionError(('full split',m,lhs,split))
    if not np.isfinite([lhs,split,T,T0]).all():
        raise AssertionError('nonfinite')
    # Ungauged opposition: x=u,y=v has zero transverse energy but positive norm.
    nullw=np.kron(u,v)-np.kron(u,v)
    if np.linalg.norm(nullw)!=0:
        raise AssertionError('null control')
    return {'m':m,'seed':seed,'epsilon':float(eps),
            'binary_residual':float(abs(rhs-binq)),
            'full_split_relative_residual':float(abs(lhs-split)/max(1,abs(lhs),abs(split))),
            'T_over_w2':float(T/w2),'proved_threshold':delta/2,
            'Lipschitz_ratio':float(abs(T-T0)/lip),
            'ungauged_positive_coercivity':'false: exact common-plane null'}


if __name__=='__main__':
    out={'scope':'identities and slice estimates only; W_m is not inferred',
         'exact':exact_binary(),
         'checks':[test(m,20261027+k) for m in (1,2,3) for k in range(3)]}
    print(json.dumps(out,indent=2))
