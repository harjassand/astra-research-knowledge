"""Check the proposed averaged logical operation against explicit CPTP recovery.

No learned axis or physical experiment is claimed here. This is the initial
forward-map falsification object, using small matrix exponentials only.
"""
from pathlib import Path
import json
import numpy as np


I=np.eye(2,dtype=complex)
X=np.array([[0,1],[1,0]],complex)
Y=np.array([[0,-1j],[1j,0]],complex)
Z=np.diag([1.,-1.]).astype(complex)
PAULI=(X,Y,Z)


def expm(A):
    """Small scaling/squaring Taylor exponential, independent of eigenspaces."""
    A=np.asarray(A)
    norm=float(np.linalg.norm(A,ord=np.inf))
    scale=max(0,int(np.ceil(np.log2(norm/.4)))) if norm else 0
    B=A/(2**scale)
    E=np.eye(A.shape[0],dtype=np.result_type(A,float)); term=E.copy()
    for j in range(1,45):
        term=term@B/j
        E=E+term
        if np.linalg.norm(term,ord=np.inf)<1e-18:
            break
    for _ in range(scale):
        E=E@E
    return E


def cross(v):
    x,y,z=v
    return np.array([[0,-z,y],[z,0,-x],[-y,x,0]],float)


def bloch_eta(theta,n,gamma,dt):
    G=2*theta*cross([0,0,1])+2*gamma*(np.outer(n,n)-np.eye(3))
    M=expm(dt*G)
    return complex(M[0,0],M[0,1])


def sensor_super(theta,n,gamma,dt):
    H=theta*Z
    N=sum(v*s for v,s in zip(n,PAULI))
    L=-1j*(np.kron(I,H)-np.kron(H.T,I))+gamma*(np.kron(N.conj(),N)-np.eye(4))
    return expm(dt*L)


def apply_sensor(S,rho):
    out=np.zeros((4,4),complex)
    for a in range(2):
        for b in range(2):
            rr=[a,2+a]; cc=[b,2+b]
            block=rho[np.ix_(rr,cc)]
            out[np.ix_(rr,cc)]=(S@block.reshape(4,order='F')).reshape(2,2,order='F')
    return out


def logical_cycle(theta,n,gamma,dt,rho,record=False):
    V=np.zeros((4,2),complex); V[0,0]=V[3,1]=1
    P=V@V.conj().T; Q=np.eye(4)-P; E=np.kron(X,I)
    physical=apply_sensor(sensor_super(theta,n,gamma,dt),V@rho@V.conj().T)
    branches=[V.conj().T@P@physical@P@V,
              V.conj().T@E@Q@physical@Q@E@V]
    return branches if record else sum(branches)


def pair_factor(theta,n,gamma,dt):
    return bloch_eta(theta,n,gamma,dt)*bloch_eta(-theta,n,gamma,dt).conjugate()


def check():
    rng=np.random.default_rng(2402601)
    max_channel_error=0.; max_symmetry_error=0.; max_bound_ratio=0.
    cases=0
    E00=np.diag([1.,0.]).astype(complex); E11=np.diag([0.,1.]).astype(complex)
    E01=np.array([[0,1],[0,0]],complex)
    for _ in range(40):
        theta=float(rng.uniform(-1.3,1.3)); gamma=float(rng.uniform(.1,1.4)); dt=float(rng.uniform(.01,.8))
        a,c=rng.uniform(-.3,.3,size=2); b=np.sqrt(1-a*a-c*c)
        n=np.array([b,c,a]); n0=np.array([1.,0.,0.])
        eta=bloch_eta(theta,n,gamma,dt)
        for rho,wanted in ((E00,E00),(E11,E11),(E01,eta*E01)):
            err=float(np.max(np.abs(logical_cycle(theta,n,gamma,dt,rho)-wanted)))
            max_channel_error=max(max_channel_error,err)
        # Explicit composition of the two recovered cycles and logical X pulses.
        first=logical_cycle(theta,n,gamma,dt,E01)
        second=logical_cycle(-theta,n,gamma,dt,X@first@X)
        paired=X@second@X
        F=pair_factor(theta,n,gamma,dt)
        max_channel_error=max(max_channel_error,float(np.max(np.abs(paired-F*E01))))
        for nn in (np.array([b,c,-a]),np.array([b,-c,a])):
            max_symmetry_error=max(max_symmetry_error,abs(F-pair_factor(theta,nn,gamma,dt)))
        C=4*np.sqrt(2)*gamma*dt+8*gamma*gamma*dt*dt
        ratio=abs(F-pair_factor(theta,n0,gamma,dt))/(C*(a*a+c*c))
        max_bound_ratio=max(max_bound_ratio,ratio)
        assert ratio<=1+1e-11
        cases+=1

    gamma,dt,theta=1.,.15,.4
    e=np.array([1.,0.,0.]); paired0=pair_factor(theta,e,gamma,dt); eta0=bloch_eta(theta,e,gamma,dt)
    scaling=[]
    for s in (.1,.03,.01,.003,.001):
        n=np.array([np.sqrt(1-s*s),s,0.])
        scaling.append({'s':s,'unpaired_error_over_s':abs(bloch_eta(theta,n,gamma,dt)-eta0)/s,
                        'paired_error_over_s_squared':abs(pair_factor(theta,n,gamma,dt)-paired0)/(s*s)})
    # Exact theta=0 noise-only formula, including finite dt.
    n=np.array([np.sqrt(.96),.2,0.]); p=(1-np.exp(-2*gamma*dt))/2
    known=1-4*p*(1-p)*n[1]**2
    assert abs(pair_factor(0,n,gamma,dt)-known)<2e-14
    assert max_channel_error<3e-13 and max_symmetry_error<3e-13

    out={'status':'PASS','random_forward_map_cases':cases,'max_cptp_bloch_or_pair_discrepancy':max_channel_error,
         'max_separate_reflection_discrepancy':max_symmetry_error,'max_observed_bound_ratio':max_bound_ratio,
         'misalignment_scaling':scaling,'noise_only_exact_pair_formula_error':abs(pair_factor(0,n,gamma,dt)-known),
         'scope':'Averaged logical channels after syndrome-record erasure; no instrument-level or hardware claim.'}
    Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':
    check()
