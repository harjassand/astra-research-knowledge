"""Independent reconstruction from family272's integer pencil.

All source formula indices are zero based. Superoperators use C-order
matrix-unit flattening, and Choi ordering is (input, output).
No candidate-originator code or data is imported.
"""
import json
from pathlib import Path
import numpy as np

M = np.array([
 [[6,0,0,0],[0,6,0,0],[0,0,6,0],[0,0,0,6],[0,0,0,0],[0,0,0,0]],
 [[-12,0,0,0],[0,-6,0,0],[0,0,6,0],[0,0,0,12],[-6,0,6,6],[-6,-6,6,0]],
 [[0,6,-2,0],[6,6,0,2],[-2,0,10,0],[0,2,0,24],[0,0,0,6],[0,-6,6,-6]],
 [[0,0,-4,-3],[0,-2,-3,-4],[-4,-3,11,6],[-3,-4,6,25],[6,6,0,0],[0,-6,6,6]]
], dtype=object)

SYM = [(i,j) for i in range(4) for j in range(i,4)]
WEDGE = [(i,j) for i in range(4) for j in range(i+1,4)]

def transpose_super(n):
    return np.eye(n*n, dtype=object)[np.arange(n*n).reshape(n,n).T.ravel()]

def choi(F, n, m):
    return F.reshape(m,m,n,n).transpose(2,0,3,1).reshape(n*m,n*m)

def build_exact():
    G = [[M[i].T @ M[j] for j in range(4)] for i in range(4)]
    for i in range(4):
        for j in range(4):
            assert np.array_equal(G[i][j], G[j][i])
            assert np.array_equal(G[i][j], G[i][j].T)
    U0 = np.zeros((16,10),dtype=object)
    V0 = np.zeros((16,6),dtype=object)
    for t,(i,j) in enumerate(SYM):
        U0[4*i+j,t]=1
        if i != j:
            U0[4*j+i,t]=1
    for t,(i,j) in enumerate(WEDGE):
        V0[4*i+j,t]=1
        V0[4*j+i,t]=-1
    K = np.zeros((6,6),dtype=object)
    for col,(i,j) in enumerate(WEDGE):
        k,l = [t for t in range(4) if t not in (i,j)]
        seq = [i,j,k,l]
        sign=(-1)**sum(seq[r]>seq[s] for r in range(4) for s in range(r+1,4))
        K[WEDGE.index((k,l)),col]=sign
    assert np.array_equal(K.T,K) and np.array_equal(K@K,np.eye(6,dtype=object))
    C=np.kron(K,K)
    A0 = np.zeros((36,100),dtype=object)
    # A0 = V0^T (L tensor L)(U0 X U0^T) V0 = 2 S(D X D).
    for i,pair1 in enumerate(SYM):
        terms1 = [pair1] if pair1[0]==pair1[1] else [pair1, pair1[::-1]]
        for j,pair2 in enumerate(SYM):
            terms2 = [pair2] if pair2[0]==pair2[1] else [pair2, pair2[::-1]]
            image = np.zeros((16,16),dtype=object)
            for a,b in terms1:
                for c,d in terms2:
                    image += np.kron(G[a][c],G[b][d])
            A0[:,10*i+j]=(V0.T@image@V0).ravel()
    assert np.array_equal(A0@transpose_super(10),A0)
    assert np.array_equal(transpose_super(6)@A0,A0)
    h=[1 if i==j else 2 for i,j in SYM]
    # 4 Ad_(D^-2) has diagonal factors 4/(h_i h_j), all integral.
    weights=np.array([4//(u*v) for u in h for v in h],dtype=object)
    Q4=(A0*weights)@A0.T
    F4=Q4@C@A0  # F4 = 32 ABA composed with Ad_D.
    assert np.array_equal(F4@transpose_super(10),F4)
    assert np.array_equal(transpose_super(6)@F4,F4)
    return A0,K,F4,Q4

def run():
    A0,K,F4,Q4=build_exact()
    df=np.array([1. if i==j else np.sqrt(2.) for i,j in SYM])
    filt=np.outer(df,df).ravel()
    A=.5*np.asarray(A0,dtype=float)/filt
    C=np.asarray(np.kron(K,K),dtype=float)
    B=A.T@C
    ABA=A@B@A
    BAB=B@A@B
    assert np.allclose(BAB,ABA.T@C,atol=2000,rtol=2e-15)
    assert np.allclose(np.asarray(F4,dtype=float),32*ABA*filt,atol=1000000,rtol=2e-15)
    report={"basis_sym":SYM,"basis_wedge":WEDGE,
            "max_abs_A0":int(np.max(np.abs(A0))),
            "max_abs_F4":int(np.max(np.abs(F4))),
            "map_identity":"F4 = 32 ABA composed with Ad_D; D=diag(1 diagonal, sqrt(2) offdiagonal)",
            "transpose_invariance_exact":True,"K_symmetric_involution_exact":True,
            "BAB_relation":"BAB=(ABA)^dagger composed with Ad_K"}
    for name,F,n,m in [('A',A,10,6),('BA',B@A,10,10),('ABA',ABA,10,6),('BAB',BAB,6,10),('F4',np.asarray(F4,dtype=float),10,6)]:
        J=choi(F,n,m)
        J=J/np.trace(J)
        eig=np.linalg.eigvalsh((J+J.T)/2)
        PT=J.reshape(n,m,n,m).transpose(0,3,2,1).reshape(n*m,n*m)
        peig=np.linalg.eigvalsh((PT+PT.T)/2)
        R=J.reshape(n,m,n,m).transpose(0,2,1,3).reshape(n*n,m*m)
        report[name]={"min_eig":float(eig[0]),"max_eig":float(eig[-1]),
                      "min_PT_eig":float(peig[0]),"realignment_norm":float(np.linalg.svd(R,compute_uv=False).sum()),
                      "purity":float(np.sum(eig**2)),"rank_above_1e-10":int(sum(eig>1e-10))}
    out=Path(__file__).parent
    (out/'independent_diagnostics.json').write_text(json.dumps(report,indent=2)+'\n')
    np.savez(out/'independent_numeric_maps.npz',A=A,B=B,ABA=ABA,BAB=BAB,F4=np.asarray(F4,dtype=float))
    (out/'F4_integer_superoperator.json').write_text(json.dumps(F4.tolist())+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__': run()
