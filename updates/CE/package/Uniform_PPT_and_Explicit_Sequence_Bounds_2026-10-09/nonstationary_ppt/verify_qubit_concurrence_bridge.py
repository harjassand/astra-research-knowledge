"""Bounded checks for the qubit-concurrence exponential-approximation proof.
These test algebraic interfaces, not optimal convex roofs or universal constants.
"""
import json
from pathlib import Path
import numpy as np
rng=np.random.default_rng(261009)

def conc(v,d):
    M=v.reshape(2,d)
    s=np.linalg.svd(M,compute_uv=False)
    return float(2*s[0]*s[1])

def ptA(rho,d):return rho.reshape(2,d,2,d).transpose(2,1,0,3).reshape(2*d,2*d)
def sqrtpsd(rho):
    w,U=np.linalg.eigh(rho)
    return (U*np.sqrt(np.maximum(w,0)))@U.conj().T

cov_errors=[];product_slacks=[]
for d in [2,3,4,6]:
    for j in range(25):
        v=rng.normal(size=2*d)+1j*rng.normal(size=2*d)
        v/=np.linalg.norm(v)
        A=rng.normal(size=(2,2))+1j*rng.normal(size=(2,2))
        if j%5==0:A[:,1]=A[:,0]*(.3+.7j)
        out=np.kron(A,np.eye(d))@v
        cov_errors.append(abs(conc(out,d)-abs(np.linalg.det(A))*conc(v,d)))
        U,s,Vh=np.linalg.svd(v.reshape(2,d),full_matrices=False)
        product=np.kron(U[:,0],Vh[0,:])
        err=np.sum(np.abs(np.linalg.eigvalsh(np.outer(v,v.conj())-np.outer(product,product.conj()))))
        product_slacks.append(np.sqrt(2)*conc(v,d)-err)
assert max(cov_errors)<1e-12
assert min(product_slacks)>-1e-12

flag_records=[]
for d,r in [(2,1),(4,1),(4,2),(6,2),(6,3),(8,4)]:
    U=np.linalg.qr(rng.normal(size=(d,2*r))+1j*rng.normal(size=(d,2*r)))[0]
    V=np.column_stack([np.concatenate([U[:,j],U[:,r+j]])/np.sqrt(2) for j in range(r)])
    X=rng.normal(size=(r,r))+1j*rng.normal(size=(r,r))
    tau=X@X.conj().T;tau/=np.trace(tau)
    rho=V@tau@V.conj().T
    measured=np.linalg.eigvalsh(ptA(rho,d))[0]
    expected=-np.linalg.eigvalsh(tau)[-1]/2
    assert abs(measured-expected)<1e-12
    flag_records.append(dict(d=d,flag_rank=r,partial_transpose_min=float(measured),expected=float(expected)))

# Explicit 2x4 PPT matrices, verified by both PSD and partial-transpose spectra.
# The test does not use or claim an entanglement certification for these matrices.
peel_records=[]
for b in [.1,.3,.7,.9]:
    rho=np.diag([b,b,b,b,(1+b)/2,b,b,(1+b)/2]).astype(complex)
    for p,q in [(0,5),(1,6),(2,7)]:rho[p,q]=rho[q,p]=b
    rho[4,7]=rho[7,4]=np.sqrt(1-b*b)/2
    rho/=7*b+1
    er,U=np.linalg.eigh(rho)
    assert er[0]>-1e-12 and np.linalg.eigvalsh(ptA(rho,4))[0]>-1e-12
    support=U[:,er>1e-10]
    candidates=[]
    for _ in range(100):
        z=rng.normal(size=support.shape[1])+1j*rng.normal(size=support.shape[1])
        v=support@z;v/=np.linalg.norm(v)
        candidates.append((conc(v,4),v))
    c,v=min(candidates,key=lambda x:x[0])
    assert c<1-1e-5
    pinv=(U[:,er>1e-10]/er[er>1e-10])@U[:,er>1e-10].conj().T
    p=.5/np.vdot(v,pinv@v).real
    rem=rho-p*np.outer(v,v.conj())
    ev,Q=np.linalg.eigh(rem)
    W=np.column_stack([np.sqrt(p)*v,Q*np.sqrt(np.maximum(ev,0))])
    total=sum(conc(W[:,j],4) for j in range(W.shape[1]))
    assert total<1-1e-5
    P,ss,Vh=np.linalg.svd(W,full_matrices=True)
    coiso=P@Vh[:8,:]
    assert np.linalg.norm(coiso@coiso.conj().T-np.eye(8))<1e-12
    assert np.linalg.norm(sqrtpsd(rho)@coiso-W)<1e-7
    eps=1e-8
    rhoprime=(1-eps)*rho+eps*np.eye(8)/8
    Wprime=sqrtpsd(rhoprime)@coiso
    lifted=sum(conc(Wprime[:,j],4) for j in range(Wprime.shape[1]))
    assert lifted<1
    peel_records.append(dict(parameter=b,range_vector_concurrence=c,peeled_weight=float(p),ensemble_upper_bound=float(total),lifted_ensemble_bound=float(lifted),min_eigenvalue=float(er[0]),min_pt_eigenvalue=float(np.linalg.eigvalsh(ptA(rho,4))[0])))

result=dict(seed=261009,pure_filter_cases=len(cov_errors),max_covariance_error=max(cov_errors),min_product_distance_slack=min(product_slacks),bell_flag_cases=flag_records,ppt_peeling_cases=peel_records,all_checks_passed=True,scope='Algebraic concurrence covariance, pure-state separable-distance bound, Bell-flag NPT spectrum, and finite PPT ensemble peeling/lifting. No convex-roof optimization or universal c_d is computed.')
Path(__file__).with_name('qubit_concurrence_bridge_verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['bell_flag_cases','ppt_peeling_cases']},indent=2))
