"""SDP screen for non-Weyl rank>=3 frames; numerical search only, not evidence."""
from __future__ import annotations
import cvxpy as cp
import numpy as np


def hermitian_basis(d):
    out = [np.eye(d, dtype=complex) / np.sqrt(d)]
    # Diagonal traceless basis, Gram-Schmidt in exact pattern.
    for k in range(1, d):
        v = np.zeros(d)
        v[:k] = 1
        v[k] = -k
        v = v / np.sqrt(k * (k + 1))
        out.append(np.diag(v).astype(complex))
    for i in range(d):
        for j in range(i + 1, d):
            a = np.zeros((d,d), complex)
            a[i,j] = a[j,i] = 1 / np.sqrt(2)
            out.append(a)
            b = np.zeros((d,d), complex)
            b[i,j] = -1j / np.sqrt(2)
            b[j,i] = 1j / np.sqrt(2)
            out.append(b)
    assert len(out) == d*d
    return out


def coefficients(basis, A):
    return np.array([np.trace(F.conj().T @ A).real for F in basis])


def frame_projector(basis, mats):
    U = np.array([coefficients(basis, A) for A in mats])
    # Orthonormalize in ordinary HS norm, keep the same subspace.
    q, r = np.linalg.qr(U.T)
    rank = np.linalg.matrix_rank(r, tol=1e-8)
    return q[:,:rank], rank


def cartan(basis, d, U=None):
    if U is None:
        U = np.eye(d)
    diag = []
    for k in range(1,d):
        v = np.zeros(d)
        v[:k] = 1
        v[k] = -k
        v = v / np.sqrt(k*(k+1))
        diag.append(U @ np.diag(v) @ U.conj().T)
    return diag


def frame_list(d):
    b = hermitian_basis(d)
    I = np.eye(d)
    frames = {"full_traceless": b[1:]}
    if d == 3:
        w = np.exp(2j*np.pi/3)
        F = np.array([[w**(j*k) for k in range(3)] for j in range(3)],complex)/np.sqrt(3)
        frames["two_MUB_cartans"] = cartan(b,d) + cartan(b,d,F)
        # Spin-one vector observables J_x,J_y,J_z (spin-1 irrep).
        Jz=np.diag([1,0,-1]).astype(complex)
        Jp=np.array([[0,np.sqrt(2),0],[0,0,np.sqrt(2)],[0,0,0]],complex)
        Jm=Jp.conj().T
        Jx=(Jp+Jm)/2
        Jy=(Jp-Jm)/(2j)
        frames["spin1_vector"]=[Jx,Jy,Jz]
        # Complete embedded qubit Bloch subspace on levels 0,1.
        X=np.array([[0,1],[1,0]],complex)
        Y=np.array([[0,-1j],[1j,0]],complex)
        Z=np.diag([1,-1]).astype(complex)
        for name,A2 in zip("XYZ",[X,Y,Z]):
            A=np.zeros((3,3),complex); A[:2,:2]=A2
            frames.setdefault("embedded_qubit_bloch",[]).append(A)
        # Three noncommuting adjacent coherences and a diagonal contrast.
        frames["adjacent_coherences"]=[frames["embedded_qubit_bloch"][0],
             np.array([[0,0,0],[0,0,1],[0,1,0]],complex),
             np.array([[0,0,0],[0,0,-1j],[0,1j,0]],complex)]
    if d == 4:
        w=np.exp(2j*np.pi/4)
        F=np.array([[w**(j*k) for k in range(4)] for j in range(4)],complex)/2
        frames["two_MUB_cartans"] = cartan(b,d)+cartan(b,d,F)
    return b, frames


def partial_trace_expr(J,d,keep):
    # J acts on R,A,B, each d-dimensional; return the partial trace over omitted factors.
    dims=(d,d,d)
    keep=tuple(keep)
    kout=int(np.prod([dims[k] for k in keep]))
    rows=[]
    for oi in range(kout):
        outidx=[]; z=oi
        for k in reversed(keep):
            outidx.append(z%d); z//=d
        outidx=tuple(reversed(outidx))
        row=[]
        for oj in range(kout):
            outj=[]; z=oj
            for k in reversed(keep):
                outj.append(z%d); z//=d
            outj=tuple(reversed(outj))
            val=0
            for traceidx in np.ndindex(*(dims[k] for k in range(3) if k not in keep)):
                ii=[None]*3; jj=[None]*3
                p=0
                for k in range(3):
                    if k in keep:
                        q=keep.index(k); ii[k]=outidx[q]; jj[k]=outj[q]
                    else:
                        ii[k]=jj[k]=traceidx[p]; p+=1
                def lin(ix): return (ix[0]*d+ix[1])*d+ix[2]
                val=val+J[lin(ii),lin(jj)]
            row.append(val)
        rows.append(row)
    return cp.bmat(rows)


def run(d, frame_name, mats):
    basis, _ = frame_list(d)
    U, rank = frame_projector(basis, mats)
    n=d**3
    # It is enough to optimize over real Choi matrices here: each listed Q is
    # invariant under entrywise conjugation, so average a feasible broadcaster
    # with its conjugate without changing feasibility or the objective.
    J=cp.Variable((n,n), symmetric=True)
    constraints=[J >> 0]
    # Symmetry of the two output systems A,B.
    perm=[]
    for r in range(d):
        for a in range(d):
            for b in range(d):
                perm.append((r*d+a)*d+b)
    # swap sends (r,a,b) -> (r,b,a)
    S=np.zeros((n,n))
    for r in range(d):
        for a in range(d):
            for b in range(d):
                S[(r*d+b)*d+a,(r*d+a)*d+b]=1
    constraints += [S@J@S.T == J]
    J_RA=partial_trace_expr(J,d,(0,1))
    J_R=partial_trace_expr(J,d,(0,))
    J_A=partial_trace_expr(J,d,(1,))
    Id=np.eye(d)/d
    constraints += [J_R == Id, J_A == Id]
    # Vectorized real linear map from J_RA to the Hermitian-basis transfer R.
    # R[b,a] = d Tr((Fa.T tensor Fb) J_RA); J_RA is real by conjugation twirl.
    n2=d*d
    L=np.zeros((n2*n2,n2*n2))
    for a,Fa in enumerate(basis):
        for b,Fb in enumerate(basis):
            W=np.kron(Fa.T,Fb)
            row=b+a*n2
            for p in range(n2):
                for q in range(n2):
                    L[row,q+p*n2]=d*W[p,q].real
    R=cp.reshape(L @ cp.vec(J_RA,order="F"),(n2,n2),order="F")
    constraints += [R == R.T, R >> 0]
    # U columns specify a tau-orthonormal frame A_i=sqrt(d)*sum_a U[a,i] F_a.
    obj=2*cp.trace(U.T @ R @ U)-rank
    prob=cp.Problem(cp.Maximize(obj),constraints)
    try:
        prob.solve(solver="CLARABEL",tol_gap_abs=1e-8,tol_feas=1e-8,tol_gap_rel=1e-8,max_iter=300)
    except cp.error.SolverError:
        prob.solve(solver="SCS",eps=2e-6,max_iters=30000,verbose=False)
    print(f"d={d} frame={frame_name} rank={rank} status={prob.status} max_h={prob.value}")
    if J.value is not None:
        j=np.array(J.value)
        rv=np.array(R.value)
        print("  min_eig_J",np.linalg.eigvalsh((j+j.conj().T)/2).min(),
              "swap",np.max(np.abs(S@j@S.T-j)),"R_eig",np.linalg.eigvalsh(rv).min(),
              "marg",max(np.max(np.abs(np.array(x.value)-Id)) for x in [J_R,J_A]))
        print("  eig_selected",np.linalg.eigvalsh(U.T@rv@U))


if __name__ == '__main__':
    d=3
    _, frames=frame_list(d)
    run(d,"adjacent_coherences",frames["adjacent_coherences"])
