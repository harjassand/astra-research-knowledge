"""Original fixed-case algebra checks; no optimizer, sweep, or acquired code."""
import json
from fractions import Fraction as F
import numpy as np

def exact_value(p,q,eta):
    Q=p+q-p*q
    if p*q==0: return Q
    z=eta*np.sqrt(p*q*(1-p)*(1-q))
    c=min(1.,z/(p*q))
    return Q-p*q*c*c+2*z*c

def exp_herm(h,a):
    w,v=np.linalg.eigh(h)
    return (v*np.exp(-1j*a*w))@v.conj().T

def witness(p,q,eta):
    c=1. if p*q==0 else min(1.,eta*np.sqrt((1-p)*(1-q)/(p*q)))
    v=np.array([0.,c,np.sqrt(max(0.,1-c*c))])
    z=np.array([1.,0.,0.]);e=np.array([0.,1.,0.])
    U=exp_herm(np.outer(z,v)+np.outer(v,z),np.arcsin(np.sqrt(p)))
    psi=U@z;rho=np.outer(psi,psi.conj())
    Z=np.diag([1.,-1.,-1.])
    rho=eta*rho+(1-eta)*(rho+Z@rho@Z)/2
    W=exp_herm(np.outer(z,e)+np.outer(e,z),np.arcsin(np.sqrt(q)))
    out=W@rho@W.conj().T
    return float(np.trace(out[1:,1:]).real)

cases=[(0.,.25,.5),(.25,0.,.5),(1.,.25,.5),(.25,1.,.5),
       (.25,.25,0.),(.25,.25,.1),(.25,.25,.5),(.25,.25,1.),
       (.7,.6,.2),(.7,.6,1.),(.01,.09,.1),(.3,.2,.7)]
res=[{'p':p,'q':q,'eta':eta,'formula':exact_value(p,q,eta),
      'witness':witness(p,q,eta)} for p,q,eta in cases]
maxerr=max(abs(x['formula']-x['witness']) for x in res)
assert maxerr<1e-12
p=q=F(1,4);eta=F(1,2);Q=p+q-p*q
# For c=1, sqrt[pq(1-p)(1-q)]=3/16 exactly.
opt=Q-p*q+2*eta*F(3,16)
assert Q==F(7,16) and opt==F(9,16) and opt-Q==F(1,8)
eta2=F(1,4);c2=F(3,4)
opt2=Q-p*q*c2*c2+2*eta2*F(3,16)*c2
mixture2=(1-eta2)*Q+eta2*F(3,4)
assert opt2==F(121,256) and mixture2==F(132,256)
print(json.dumps({'maximum_witness_residual':maxerr,
                  'exact_interior_example':{'eta':str(eta2),'overlap':str(c2),'optimal_F':str(opt2),'mixture_bound':str(mixture2)},
                  'exact_rational_obstruction':{'ideal_Q':str(Q),'optimal_F':str(opt),'excess':str(opt-Q)},
                  'fixed_cases':res},indent=2))
