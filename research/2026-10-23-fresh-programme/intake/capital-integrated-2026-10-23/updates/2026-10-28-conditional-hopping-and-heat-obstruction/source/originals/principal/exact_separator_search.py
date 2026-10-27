from pathlib import Path
import numpy as np,json
from cone_bridge import heat
OUT=Path(__file__).parent
d=np.load(OUT/'interfaces.npz');Q=d['Q']

def skew_completion(p,steps=50000):
    ij=np.triu_indices(8);wt=np.where(ij[0]==ij[1],1.,np.sqrt(2.))
    def vec(M):return M[ij]*wt
    def mat(v):
        M=np.zeros((8,8));M[ij]=v/wt;M[(ij[1],ij[0])]=v/wt;return M
    A=np.column_stack([vec(q) for q in Q[9:]])
    Ai=np.linalg.pinv(A);M0=np.einsum('i,ijk->jk',p,Q[:9]);anchor=vec(M0)
    y=anchor.copy();dual=y*0
    for it in range(steps):
        xx=anchor+A@(Ai@(y-dual-anchor));lam,V=np.linalg.eigh(mat(xx+dual))
        yp=vec((V*np.maximum(lam,1e-4))@V.T);dual+=xx-yp
        if np.linalg.norm(xx-yp)<1e-10:break
        y=yp
    k=Ai@(xx-anchor)
    return k,float(np.linalg.eigvalsh(M0+np.einsum('i,ijk->jk',k,Q[9:]))[0]),it

if __name__=='__main__':
    rows=[]
    for p in [np.array([1,1,16,-13,0,0,4,-4,0.]),np.array([1,1,11.5,-9.25,0,0,4,-4,0.]),np.array([1,1,112,-107.2,0,0,-6,6,0.])]:
        k,ev,it=skew_completion(p)
        rec,xx,du=heat(d,p,steps=30000)
        rec.update(p=p.tolist(),k=k.tolist(),acoustic_min=ev,acoustic_iterations=it,status='NUMERICAL_ONLY')
        print(json.dumps(rec),flush=True);rows.append(rec)
        np.savez(OUT/f'symmetric_{len(rows)-1}.npz',p=p,k=k,heat=xx,dual=du)
    (OUT/'symmetric_results.json').write_text(json.dumps(rows,indent=2)+'\n')
