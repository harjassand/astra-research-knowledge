"""Independent NumPy-2.5 recomputation; no SciPy or acquired code execution."""
import hashlib
import json
from pathlib import Path
import numpy as np

BASE=Path(__file__).resolve().parent
X=np.array([[0,1],[1,0]],complex)
Z=np.diag([1,-1])
I=np.eye(2)


def mm(a,b):
    return np.einsum('ij,jk->ik',a,b,optimize=False)


def exp_h(h):
    e,v=np.linalg.eigh(h)
    return np.einsum('ij,j,kj->ik',v,np.exp(-1j*e),v.conj(),optimize=False)


def herm(v,d):
    h=np.diag(v[:d]).astype(complex)
    k=d
    for i in range(d):
        for j in range(i+1,d):
            h[i,j]=v[k]+1j*v[k+1]
            h[j,i]=h[i,j].conjugate()
            k+=2
    return h


def build(v,d,kind):
    if kind=='seed':
        hs=[herm(p,d) for p in v.reshape(3,d*d)]
        for i in (1,2):
            hs[i]/=max(1.,np.linalg.norm(hs[i],2))
        return np.kron(np.eye(4),hs[0]),np.kron(np.kron(X,I),hs[1]),np.kron(np.kron(I,X),hs[2])
    h=np.zeros((4*d,4*d),complex)
    for i in range(4):
        h[i*d:(i+1)*d,i*d:(i+1)*d]=herm(v[i*d*d:(i+1)*d*d],d)
    blocks=v[4*d*d:].reshape(4,2,d,d)
    vs=[np.zeros_like(h),np.zeros_like(h)]
    for k,(i,j) in enumerate([(0,2),(1,3),(0,1),(2,3)]):
        b=blocks[k,0]+1j*blocks[k,1]
        b/=max(1.,np.linalg.norm(b,2))
        vs[k//2][i*d:(i+1)*d,j*d:(j+1)*d]=b
        vs[k//2][j*d:(j+1)*d,i*d:(i+1)*d]=b.conj().T
    return h,*vs


def evaluate(hs,actions,slices,split):
    d=hs[0][0].shape[0]//4
    z1=np.repeat([1,1,-1,-1],d)
    z2=np.repeat([1,-1,1,-1],d)
    out=np.zeros(4*d)
    out[3*d:]=1
    effect=np.diag(out).astype(complex)
    residual=0.
    unitarity=0.
    for k in reversed(range(len(hs))):
        h0,v1,v2=hs[k]
        for z,vi,odd in [(z1,v1,True),(z2,v1,False),(z1,v2,False),(z2,v2,True)]:
            zz=z[:,None]*vi*z[None,:]
            residual=max(residual,np.linalg.norm(zz-(-vi if odd else vi),2))
        residual=max(residual,np.linalg.norm(z1[:,None]*h0*z1[None,:]-h0,2),
                     np.linalg.norm(z2[:,None]*h0*z2[None,:]-h0,2),
                     max(0.,np.linalg.norm(v1,2)-1),max(0.,np.linalg.norm(v2,2)-1))
        h=actions[k][0]*v1+actions[k][1]*v2
        u=exp_h(h+(0 if split else h0))
        if split:
            u=mm(exp_h(h0),u)
        unitarity=max(unitarity,np.linalg.norm(mm(u.conj().T,u)-np.eye(4*d),2))
        effect=mm(mm(u.conj().T,effect),u)
        if k==2*slices:
            effect=(effect+z2[:,None]*effect*z2[None,:])/2
        elif k==slices:
            effect=(effect+z1[:,None]*effect*z1[None,:])/2
    vals=np.linalg.eigvalsh(effect[:d,:d])
    return dict(probability=float(vals[-1]),hypothesis_residual=float(residual),
                unitarity_residual=float(unitarity),all_finite=bool(np.all(np.isfinite(effect))))


def main():
    rows=[]
    for path in sorted(BASE.glob('search_*.json')):
        info=json.loads(path.read_text())
        args=info['args']
        kind,d=args['kind'],args['d']
        slices=args.get('slices',1)
        split=args.get('split_free',False)
        stem=f'candidate_{kind}_d{d}_a{args["action"]}'
        cp=BASE/(stem+f'_s{slices}_f{int(split)}.npy')
        if not cp.exists():
            cp=BASE/(stem+'.npy')
        v=np.load(cp)
        nseg=3*slices
        width=(3 if kind=='seed' else 12)*d*d
        hs=[build(vv,d,kind) for vv in v.reshape(nseg,width)]
        result=evaluate(hs,info['actions'],slices,split)
        old=max(info['results'],key=lambda r:r['ratio'])
        result.update(receipt=path.name,candidate=cp.name,
                      starts=len(info['results']),max_recorded_ratio=old['ratio'],
                      delta_probability=result['probability']-old['probability'],
                      kind=kind,d=d,slices=slices,split_free=split)
        rows.append(result)
    optimized=[]
    for path in sorted(BASE.glob('optimized_sink_[0-9].npz')):
        dat=np.load(path)
        hs=[(np.kron(np.eye(4),dat['h'][k]),
             np.kron(np.kron(X,I),dat['a'][k,0]),
             np.kron(np.kron(I,X),dat['a'][k,1])) for k in range(3)]
        row=evaluate(hs,[[.35,.35]]*3,1,False)
        row['candidate']=path.name
        optimized.append(row)
    q=1-np.cos(.35)**2*np.cos(.70)**2
    c=np.sin(.35)**2+np.sin(.70)**2
    report=dict(python_runtime='python3 default, NumPy '+np.__version__,
                recomputation='independent model assembly, Hermitian eig exponentials, explicit einsum',
                search_candidates=rows,optimized_sink_candidates=optimized,
                per_schedule=dict(Q=float(q),C=float(c),product_Q=float(q*q),
                                  anchored=float(q*c),old_product_C=float(c*c)),
                warning='Finite diagnostics only; not universal proof or exact refutation.')
    (BASE/'verification_receipt.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':
    main()
