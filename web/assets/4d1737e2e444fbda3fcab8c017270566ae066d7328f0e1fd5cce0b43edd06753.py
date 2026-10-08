"""Finite diagnostics for family272. No separability conclusion from tolerances.

The source Kraus operators are reconstructed directly from blocksZ.
"""
import json
from pathlib import Path
import numpy as np

B = np.array([
 [[6,0,0,0],[0,6,0,0],[0,0,6,0],[0,0,0,6],[0,0,0,0],[0,0,0,0]],
 [[-12,0,0,0],[0,-6,0,0],[0,0,6,0],[0,0,0,12],[-6,0,6,6],[-6,-6,6,0]],
 [[0,6,-2,0],[6,6,0,2],[-2,0,10,0],[0,2,0,24],[0,0,0,6],[0,-6,6,-6]],
 [[0,0,-4,-3],[0,-2,-3,-4],[-4,-3,11,6],[-3,-4,6,25],[6,6,0,0],[0,-6,6,6]]
], dtype=float)
Q = B.transpose(1,2,0)
syms = [(i,j) for i in range(4) for j in range(i,4)]
weds = [(i,j) for i in range(4) for j in range(i+1,4)]
U = np.zeros((16,10)); V = np.zeros((16,6))
for a,(i,j) in enumerate(syms):
    U[4*i+j,a] = 1 if i==j else 1/np.sqrt(2)
    if i!=j: U[4*j+i,a] = 1/np.sqrt(2)
for a,(i,j) in enumerate(weds):
    V[4*i+j,a] = 1/np.sqrt(2); V[4*j+i,a] = -1/np.sqrt(2)
C = np.array([[0,0,0,0,0,1],[0,0,0,0,-1,0],[0,0,0,1,0,0],
              [0,0,1,0,0,0],[0,-1,0,0,0,0],[1,0,0,0,0,0]], dtype=float)
K = np.array([V.T@np.kron(q,r)@U for q in Q for r in Q])

def superop(kraus):
    # matrix entry indexed (a,b),(i,j) and C-order vectorization
    return np.einsum('rai,rbj->abij',kraus,kraus.conj()).reshape(
        kraus.shape[1]**2,kraus.shape[2]**2)

def choi(s,di,do):
    return s.reshape(do,do,di,di).transpose(2,0,3,1).reshape(di*do,di*do)

def pt(j,di,do):
    return j.reshape(di,do,di,do).transpose(0,3,2,1).reshape(di*do,di*do)

def diagnostic(s,di,do):
    j=choi(s,di,do); j=j/np.trace(j)
    eig=np.linalg.eigvalsh(j)
    peig=np.linalg.eigvalsh(pt(j,di,do))
    realignment=j.reshape(di,do,di,do).transpose(0,2,1,3).reshape(di*di,do*do)
    singular=np.linalg.svd(realignment,compute_uv=False)
    return dict(input_dim=di,output_dim=do,
                rank_estimate=int(np.count_nonzero(eig>1e-10)),
                min_eig=float(eig[0]),max_eig=float(eig[-1]),
                min_pt_eig=float(peig[0]),realignment_norm=float(singular.sum()),
                purity=float(eig@eig))

def main():
    a=superop(K)
    b=superop(np.array([(C@k).T for k in K]))
    out={"status":"numerical diagnostics only", "kraus_rank_histogram":{
        str(rank):int(sum(np.linalg.matrix_rank(k,tol=1e-7)==rank for k in K))
        for rank in range(7)},"maps":{}}
    for name,s,di,do in [('A',a,10,6),('B',b,6,10),('BA',b@a,10,10),
                         ('AB',a@b,6,6),('ABA',a@b@a,10,6),
                         ('BAB',b@a@b,6,10),('BABA',b@a@b@a,10,10)]:
        out['maps'][name]=diagnostic(s,di,do)
    Path(__file__).with_name('numerical.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__': main()
