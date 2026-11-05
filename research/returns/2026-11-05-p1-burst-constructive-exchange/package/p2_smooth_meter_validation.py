"""Independent full 19-state ODE check of the lifted smooth-meter formula."""
import json
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from p2_slew_direct_sine_arm import slew_meter,as_numpy


def validate(k=.1,profile='cubic'):
    n=19; E=np.eye(n); C=np.zeros((n,n))
    C[np.arange(2,10),np.arange(2,10)]=.01
    C[np.arange(10,18),np.arange(10,18)]=1e-6
    D=np.zeros((n,n)); D[1,1]=2
    for j in range(8):
        for L,a,u in ((1/64,0,1),(3/32,1,0),(1/64,1,-1)):
            def fun(t,z):
                A=np.zeros((n,n)); A[0,1]=1; A[1,0]=-k
                A[1,1]=-1; A[1,18]=1
                v=t/L; f=3*v*v-2*v*v*v if profile=='cubic' else v
                g=a+u*f
                A[1,2+j]=-g; A[10+j,0]=g
                for i in range(8): A[10+i,2+i]=.01
                EE=z[:n*n].reshape(n,n); CC=z[n*n:].reshape(n,n)
                return np.concatenate([(A@EE).ravel(),
                    (A@CC+CC@A.T+D).ravel()])
            sol=solve_ivp(fun,(0,L),np.concatenate([E.ravel(),C.ravel()]),
                          method='DOP853',rtol=1e-13,atol=1e-15)
            E=sol.y[:n*n,-1].reshape(n,n); C=sol.y[n*n:,-1].reshape(n,n)
    G,S,cross,Cm,H=[as_numpy(z) for z in slew_meter(k,profile=profile)]
    read=np.zeros((8,n)); read[np.arange(8),np.arange(10,18)]=64/7
    errors={'gain':float(np.max(abs(G-read@E[:,[0,1,18]]))),
        'observation_covariance':float(np.max(abs(S-read@C@read.T))),
        'cross_covariance':float(np.max(abs(cross-read@C[:,:2]))),
        'source_covariance':float(np.max(abs(Cm-C[:2,:2]))),
        'source_gain':float(np.max(abs(H-E[:2,[0,1,18]])))}
    assert max(errors.values())<1e-10
    return {'k':k,'coupling_profile':profile,'maximum_absolute_errors':errors}


if __name__=='__main__':
    result={'method':'Independent full 19-state time-varying ODE against exact '
                    'ramp matrix exponentials; directed intervals separately '
                    'certify the entire stiffness domain.',
            'rows':[validate(profile=p) for p in ('linear','cubic')]}
    path=Path(__file__).with_suffix('.json')
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
