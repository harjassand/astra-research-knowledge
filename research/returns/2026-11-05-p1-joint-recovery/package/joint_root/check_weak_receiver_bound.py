"""Dense checks of the general weak-reader environmental contraction.

This checks exact local identities and norm inequalities, not the general
martingale proof or an optimal receiver policy.
"""
from pathlib import Path
import json
import numpy as np
from scipy.linalg import expm

def opnorm(a):
    return float(np.linalg.svd(a, compute_uv=False)[0])

def main():
    rng=np.random.default_rng(519426)
    z=np.diag([1.,-1.])
    bell=np.array([1.,0.,0.,1.])/np.sqrt(2)
    phi=np.outer(bell,bell)
    ze=np.kron(z,np.eye(2))
    obs=1j*(ze@phi-phi@ze)
    cases=[]
    for m in [1,2,3,4]:
        # Retain an extra coherent flag and allow arbitrary strong receiver-only
        # isometry V. No flag is measured in this check.
        raw=rng.normal(size=(2*m,m))+1j*rng.normal(size=(2*m,m))
        v,_=np.linalg.qr(raw)
        wbar=np.kron(v,np.eye(2))
        raw=rng.normal(size=(4*m,4*m))+1j*rng.normal(size=(4*m,4*m))
        h=(raw+raw.conj().T)/2
        h/=opnorm(h)
        dimension=8*m
        perm=[]
        for source in range(2):
            for memory in range(m):
                for carrier in range(2):
                    for purifier in range(2):
                        perm.append(((carrier*m+memory)*2+source)*2+purifier)
        swap=np.eye(dimension)[perm]
        j=np.kron(np.eye(2*m),bell[:,None])
        obig=np.kron(np.eye(4*m),obs)
        oinput=np.kron(np.eye(2*m),obs)
        for theta in [.01,.04,.2,.7,1.2]:
            c,s=np.cos(theta),np.sin(theta)
            u=c*np.eye(dimension)+1j*s*swap
            uth=2*np.sin(theta/2)
            a0=j.conj().T@u.conj().T@oinput@u@j
            for kappa in [.3,1.,2.]:
                w=expm(1j*kappa*theta*h)@wbar
                delta=opnorm(w-wbar)
                wbig=np.kron(np.eye(2),np.kron(w,np.eye(2)))
                q=wbig.conj().T@obig@wbig-oinput
                b=j.conj().T@q@j
                a=j.conj().T@u.conj().T@(oinput+q)@u@j
                remainder=a-a0-b
                bmem=np.trace(b.reshape(2,m,2,m),axis1=0,axis2=2)/2
                cases.append({
                    'm':m,'theta':theta,'kappa':kappa,'actual_delta':delta,
                    'source_identity_residual':opnorm(a0-c*s*np.kron(z,np.eye(m))),
                    'receiver_only_residual':opnorm(b-np.kron(np.eye(2),bmem)),
                    'q_norm_excess':max(0.,opnorm(q)-2*delta),
                    'b_norm_excess':max(0.,opnorm(b)-2*delta),
                    'remainder_norm_excess':max(0.,opnorm(remainder)-4*delta*uth),
                    'effective_norm_excess':max(0.,opnorm(a)-(c*s+2*delta+4*delta*uth)),
                    'isometry_residual':opnorm(w.conj().T@w-np.eye(2*m))
                })
    metrics={k:max(x[k] for x in cases) for k in cases[0] if k.endswith(('residual','excess'))}
    result={'scope':'60 local dense isometry tests with coherent flags and arbitrary receiver-only isometries; not a recovery optimum',
            'cases':len(cases),'summary':metrics,'results':cases}
    Path('joint_root/weak_receiver_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'cases':len(cases),**metrics},indent=2))
    assert max(metrics.values())<1e-11

if __name__=='__main__':
    main()
