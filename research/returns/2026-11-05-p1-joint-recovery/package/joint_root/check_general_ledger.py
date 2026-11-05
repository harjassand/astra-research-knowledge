"""Finite exact-state tests of the arbitrary-CPTP acquisition ledger."""
from pathlib import Path
import json
import numpy as np
P=[np.eye(2,dtype=complex),np.array([[0,1],[1,0]],complex),np.array([[0,-1j],[1j,0]],complex),np.diag([1.,-1.]).astype(complex)]

def power(a,p):
    v,u=np.linalg.eigh((a+a.conj().T)/2)
    mask=v>max(1e-13,float(v.max())*1e-12)
    w=np.zeros_like(v)
    w[mask]=v[mask]**p
    return (u*w)@u.conj().T

def tr_source(a):
    d=a.shape[-1]//2
    return np.trace(a.reshape(2,d,2,d),axis1=0,axis2=2)

def split_norms(images):
    inv=power(images[0],-.25)
    a=q=0.
    for x in images[1:]:
        z=inv@x@inv
        zp=np.kron(np.eye(2)/2,tr_source(z))
        a+=np.vdot(zp,zp).real/3
        q+=np.vdot(z-zp,z-zp).real/3
    return float(a),float(q)

def petz_fidelity_from_kraus(images):
    # Extract actual channel Kraus matrices from its normalized Choi matrix,
    # form the physical Petz Kraus matrices and compose them.
    d=images.shape[-1]
    choi=sum(np.kron(p.T,x) for p,x in zip(P,images))/2
    w,v=np.linalg.eigh((choi+choi.conj().T)/2)
    ks=[np.sqrt(2*t)*v[:,j].reshape(2,d).T for j,t in enumerate(w) if t>1e-13]
    inv=power(images[0],-.5)
    rs=[k.conj().T@inv/np.sqrt(2) for k in ks]
    return float(sum(abs(np.trace(r@k))**2 for r in rs for k in ks)/4)

def unitary_step(m,theta):
    d=4*m
    perm=[(c*m+b)*2+a for a in range(2) for b in range(m) for c in range(2)]
    return np.cos(theta)*np.eye(d)+1j*np.sin(theta)*np.eye(d)[perm]

def run(m,theta,n,record,mixed,kcount,seed):
    rng=np.random.default_rng(seed)
    if mixed:
        z=rng.normal(size=(m,m))+1j*rng.normal(size=(m,m))
        sigma=z@z.conj().T
        sigma/=np.trace(sigma)
    else:
        v=rng.normal(size=m)+1j*rng.normal(size=m)
        v/=np.linalg.norm(v)
        sigma=np.outer(v,v.conj())
    branches=[np.array([np.kron(p/2,sigma) for p in P])]
    u=unitary_step(m,theta)
    b=np.sin(theta)**4
    r=1-b
    history=[]
    a_prev,q_prev=0.,1.
    factor_error=0.
    for j in range(1,n+1):
        emitted=[np.array([u@np.kron(x,np.eye(2)/2)@u.conj().T for x in images]) for images in branches]
        a_minus,q_minus=np.sum([split_norms(x) for x in emitted],axis=0)
        next_branches=[]
        for grown in emitted:
            z=rng.normal(size=(kcount*m,2*m))+1j*rng.normal(size=(kcount*m,2*m))
            v,_=np.linalg.qr(z)
            ks=[np.kron(np.eye(2),v[k*m:(k+1)*m]) for k in range(kcount)]
            children=[np.array([k@x@k.conj().T for x in grown]) for k in ks]
            next_branches.extend(children if record else [np.sum(children,axis=0)])
        branches=next_branches
        a,q=np.sum([split_norms(x) for x in branches],axis=0)
        for x in branches:
            factor_error=max(factor_error,np.max(abs(x[0]-np.kron(np.eye(2)/2,tr_source(x[0])))))
        history.append({"j":j,"a":float(a),"q":float(q),"ell_p":float(a_minus-a),"ell_q":float(q_minus-q),
                        "collision_residual":float(max(abs(a_minus-a_prev-b*q_prev),abs(q_minus-r*q_prev)))})
        a_prev,q_prev=a,q
    loss=sum(x['ell_p']+(1-r**(n-x['j']))*x['ell_q'] for x in history)
    source_f=sum(petz_fidelity_from_kraus(x) for x in branches)
    memory_f=sum(petz_fidelity_from_kraus(np.array([tr_source(y) for y in x])) for x in branches)
    return {"m":m,"theta":theta,"n":n,"record":record,"mixed_initialization":mixed,"kraus_count":kcount,
            "seed":seed,"branches":len(branches),"a":float(a),"q":float(q),"weighted_loss":float(loss),
            "ledger_residual":float(abs(a-(1-r**n-loss))),
            "minimum_recorded_loss":min(min(x['ell_p'],x['ell_q']) for x in history),
            "source_product_residual":float(factor_error),"petz_memory_residual":float(abs(memory_f-(1+3*a)/4)),
            "petz_source_grant_residual":float(abs(source_f-(1+3*(a+q))/4)),"history":history}

def main():
    results=[]
    seed=825901
    for m in [2,3,4]:
        for theta in [.04,.3,.8,1.4]:
            for record in [False,True]:
                for mixed in [False,True]:
                    seed+=1
                    results.append(run(m,theta,3,record,mixed,2,seed))
    summary={"scope":"48 finite random CPTP tests; recorded/unrecorded outcomes; pure/mixed initialization; not an optimized receiver",
             "cases":len(results),"max_ledger_residual":max(x['ledger_residual'] for x in results),
             "max_collision_residual":max(y['collision_residual'] for x in results for y in x['history']),
             "max_source_product_residual":max(x['source_product_residual'] for x in results),
             "max_petz_memory_residual":max(x['petz_memory_residual'] for x in results),
             "max_petz_source_grant_residual":max(x['petz_source_grant_residual'] for x in results),
             "minimum_recorded_loss":min(x['minimum_recorded_loss'] for x in results)}
    Path(__file__).with_name('general_ledger_checks.json').write_text(json.dumps({"summary":summary,"results":results},indent=2))
    print(json.dumps(summary,indent=2))

if __name__=='__main__': main()
