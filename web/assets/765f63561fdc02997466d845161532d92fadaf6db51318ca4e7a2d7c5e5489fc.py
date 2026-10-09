#!/usr/bin/env python3
"""One fixed operator-block identity check, not a state catalogue or proof."""
from pathlib import Path
import json
import numpy as np

HERE=Path(__file__).resolve().parent
sx=np.array([[0,1],[1,0]],complex)
sz=np.diag([1.,-1.]).astype(complex)
X=np.kron(sx,np.eye(2))
Z=np.kron(sz,np.eye(2))
alpha=np.log(3.)
c,h=np.cosh(alpha),np.sinh(alpha)
A,k=np.cosh(alpha/2),np.tanh(alpha/2)
ss=np.sqrt(np.array([.9,.1]))
dd=np.power(np.array([.9,.1]),.25)
s=np.repeat(ss,2)
d=np.repeat(dd,2)


def direct(rho,q,ell,a):
    N=X+a*Z
    V=2*(N@np.diag(s)@N)/(s[:,None]+s[None,:])
    def H(t):
        return (V@t+t@V)/2-N@t@N
    r=rho/np.outer(d,d)
    Lrho=H(r)*np.outer(d,d)
    J=np.trace(Lrho@(ell-alpha*Z)).real
    E=np.trace(q@H(q)).real
    assert abs(np.trace(Lrho))<1e-12
    return J,E


def blocks(rho,q,ell):
    R00,R01,R10,R11=rho[:2,:2],rho[:2,2:],rho[2:,:2],rho[2:,2:]
    t=np.exp(-alpha)*R00-np.exp(alpha)*R11
    G0=np.block([[t,c*R01-R10],[c*R10-R01,-t]])
    off=-t
    G1=np.block([[-(R01+R10),off],[off,R01+R10]])/A
    G2=rho-Z@rho@Z
    jj=[np.trace(g@(ell-alpha*Z)).real for g in [G0,G1,G2]]
    ee=[np.trace((c*np.eye(4)-h*Z)@rho-X@q@X@q).real,
        (2*k*np.trace(X@rho)-2*np.trace(X@q@Z@q)).real,
        (1-np.trace(Z@q@Z@q)).real]
    return np.array(jj),np.array(ee)


def f_ray(r):
    return (4/3)*(r-1)*np.arctanh(r)+alpha*(8-5*r)/3-(4/3)*(1-r)-.5*(1-np.sqrt(1-r*r))


def main():
    U=np.array([[1,1,1,1],[1,1j,-1,-1j],[1,-1,1,-1],[1,-1j,-1,1j]],complex)/2
    pp=np.array([.46,.27,.18,.09])
    rho=(U*pp)@U.conj().T
    q=(U*np.sqrt(pp))@U.conj().T
    ell=(U*np.log(pp))@U.conj().T
    jj,ee=blocks(rho,q,ell)
    errors=[]
    for a in [-1.,0.,1.,2.]:
        j,e=direct(rho,q,ell,a)
        errors.append(max(abs(j-jj@np.array([1,a,a*a])),abs(e-ee@np.array([1,a,a*a]))))
    assert max(errors)<1e-12
    assert jj[2]>=4*ee[2]-1e-12
    ray_n=(np.sqrt(3)/2)*X+.5*Z
    rr=.99
    rho_ray=(np.eye(4)+rr*ray_n)/4
    vv,ww=np.linalg.eigh(rho_ray)
    q_ray=(ww*np.sqrt(vv))@ww.conj().T
    ell_ray=(ww*np.log(vv))@ww.conj().T
    j,e=direct(rho_ray,q_ray,ell_ray,0.)
    assert abs(j-2*e-f_ray(rr))<1e-12
    failed_shortcut_gap=(f_ray(.989)+f_ray(.991))/2-f_ray(.99)
    assert failed_shortcut_gap<0
    result={'status':'PASS_FINITE_IDENTITY_DIAGNOSTIC_ONLY',
            'fixed_joint_states_checked':1,'noise_values_for_same_state':4,
            'largest_block_formula_error':float(max(errors)),
            'ray_formula_error':float(abs(j-2*e-f_ray(rr))),
            'failed_stronger_MI_shortcut_gap_numeric':float(failed_shortcut_gap),
            'counterexample_scope':'Stronger zero-marginal-buffer shortcut only; complete weak endpoint NOT refuted',
            'nonlinear_reference_endpoint':'UNRESOLVED','random_state_catalogues':0}
    (HERE/'block_identity_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
