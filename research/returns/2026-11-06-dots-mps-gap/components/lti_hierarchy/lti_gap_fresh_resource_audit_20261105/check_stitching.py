"""Fresh implementation. Does not import the candidate's scripts or data."""
import json, time
import numpy as np
from numpy.linalg import eigh, norm

def psd_power(a,p):
    ev,u=eigh((a+a.conj().T)/2)
    if ev.min()<=0: raise ValueError(ev)
    return (u*ev**p)@u.conj().T

def tensor(seed,d=3,D=2):
    rng=np.random.default_rng(seed)
    a=rng.normal(size=(d,D,D))+1j*rng.normal(size=(d,D,D))
    inv=psd_power(sum(x@x.conj().T for x in a),-.5)
    a=np.array([inv@x for x in a])
    sig=np.eye(D)/D
    for _ in range(2000):
        nxt=sum(x.conj().T@sig@x for x in a)
        if norm(nxt-sig)<2e-15:break
        sig=nxt
    sig=nxt/np.trace(nxt)
    return a,sig

def gamma(a,L):
    D=a.shape[1]
    products=[np.eye(D)]
    for _ in range(L):products=[x@y for x in products for y in a]
    return np.array([x.reshape(-1) for x in products])

def maps(a,sig,L):
    g=gamma(a,L)
    gram=g.conj().T@g
    v=g@psd_power(gram,-.5)
    s=np.kron(np.eye(a.shape[1]),psd_power(sig,.5))
    dec=s@np.linalg.solve(gram,g.conj().T)
    enc=g@np.linalg.inv(s)
    return v,dec,enc,gram

def pair_action(x,h,i,d,N):
    shape=x.shape
    y=x.reshape([d]*N+list(shape[1:]))
    y=np.moveaxis(y,[i,i+1],[0,1])
    sh=y.shape
    y=(h@y.reshape(d*d,-1)).reshape(sh)
    y=np.moveaxis(y,[0,1],[i,i+1])
    return y.reshape(shape)

def run(seed,ell):
    d,D=3,2
    a,sig=tensor(seed,d,D)
    v2,_,_,_=maps(a,sig,2)
    h=np.eye(d*d)-v2@v2.conj().T
    H3=np.kron(h,np.eye(d))+np.kron(np.eye(d),h)
    vals=eigh(H3)[0]
    if np.count_nonzero(vals<1e-10)!=D*D:raise ValueError('Improper small parent')
    v,dec,_,gram=maps(a,sig,ell)
    w,_,w0,_=maps(a,sig,2*ell)
    code,_,_,_=maps(a,sig,ell+1)
    def make(decoder,encoder):
        left=np.einsum('aep,psc->aesc',decoder.reshape(D,D,d**ell),code.reshape(d**ell,d,D*D))
        right=np.einsum('fbq,tqd->tfbd',decoder.reshape(D,D,d**ell),code.reshape(d,d**ell,D*D))
        out=np.einsum('jfe,aesc,tfbd->tjsabcd',encoder.reshape(d**(2*ell),D,D),left,right,optimize=True)
        return out.reshape(d**(2*ell+2),D*D,D**4)
    k=make(v.conj().T,w)
    k0=make(dec,w0)
    N=2*ell+2
    hk=pair_action(k,h,0,d,N)+pair_action(k,h,N-2,d,N)
    hk0=pair_action(k0,h,0,d,N)+pair_action(k0,h,N-2,d,N)
    def opnorm(x):return norm(x.reshape(-1,D**4),2)
    kf=k.reshape(-1,D**4)
    return {
      'seed':seed,'ell':ell,'sigma_eigenvalues':eigh(sig)[0].tolist(),
      'parent_H3_gap':float(vals[D*D]),
      'isometry_error':float(norm(kf.conj().T@kf-np.eye(D**4),2)),
      'ideal_seam_residual':float(opnorm(hk0)),
      'actual_compressed_seam_square_norm':float(opnorm(hk)**2),
      'actual_ideal_map_distance':float(opnorm(k-k0)),
      'gram_product_distance':float(norm(gram-np.kron(np.eye(D),sig),2)),
      'gram_wrong_transpose_distance':float(norm(gram-np.kron(np.eye(D),sig.T),2)),
      'bound_HK_by_two_map_difference':bool(opnorm(hk)<=2*opnorm(k-k0)+1e-11),
    }

if __name__=='__main__':
    start=time.perf_counter()
    rows=[run(seed,ell) for seed in [1729,2718,3141] for ell in [2,3,4]]
    output={'results':rows,'seconds':time.perf_counter()-start,'numpy':np.__version__}
    with open('fresh_stitching_results.json','w') as f:json.dump(output,f,indent=2)
    print(json.dumps(output,indent=2))
