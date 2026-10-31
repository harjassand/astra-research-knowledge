"""Exact small-space noise channels and a contained-leakage circuit bound.

Code projection and physical Pauli twirling are explicit benchmark resources.
This program does not substitute them for the separately constructed noisy
apparatus, or infer a device error rate from its small matrix residuals.
"""
from pathlib import Path
import json
import numpy as np
from scipy.linalg import expm, norm

ROOT=Path(__file__).resolve().parent
I=np.eye(3,dtype=complex)
n=np.diag([2.,1.,0.]); nb=2*I-n
v=np.column_stack(([0,1,0],np.array([1,0,1])/np.sqrt(2))).astype(complex)
q=np.array([1,0,-1],complex)/np.sqrt(2)
p=v@v.conj().T
jx=np.array([[0,1,0],[1,0,1],[0,1,0]],complex)/np.sqrt(2)
X=np.array([[0,1],[1,0]],complex); Z=np.diag([1.,-1.]); Y=np.array([[0,-1j],[1j,0]])
paulis=[np.eye(2),X,Y,Z]

def twirled(k):
    d=len(k)
    ps=paulis if d==2 else [np.kron(a,b) for a in paulis for b in paulis]
    weights=np.array([abs(np.trace(a.conj().T@k)/d)**2 for a in ps])
    return dict(pass_probability=float(weights.sum()),
                erasure_probability=float(1-weights.sum()),
                accepted_nonidentity_probability=float(weights[1:].sum()))

def main():
    rows=[]
    for e in [.1,.03,.01,.003,.001]:
        A=2*e; B=e
        full=expm(-.5*(A*n+B*nb))
        k=v.conj().T@full@v
        exact=np.exp(-(A+B)/2)*np.diag([1,np.cosh((A-B)/2)])
        assert norm(k-exact)<1e-13
        balanced=twirled(k)
        dual=twirled(np.diag([np.exp(-A/2),np.exp(-B/2)]))
        rows.append(dict(epsilon=e,balanced=balanced,dual_rail=dual,
                         late_leakage_amplitude=float(norm((I-p)@full@v,2)),
                         quartic_coefficient=balanced['accepted_nonidentity_probability']/e**4,
                         expected_quartic_coefficient=float(np.exp(-(A+B))/256)))
    w=np.kron(v,v); hc=np.kron(n,n)
    ideal=np.diag([-1,1,1,1]).astype(complex)
    gate=[]
    for delta in [.1,.03,.01,.003,.001]:
        full=expm(-1j*(np.pi+delta)*hc)
        k=ideal.conj().T@(w.conj().T@full@w)*np.exp(1j*delta)
        expected=np.diag([1,np.cos(delta),np.cos(delta),
                          np.exp(1j*delta)*(3+np.exp(-4j*delta))/4])
        assert norm(k-expected)<1e-13
        out=twirled(k); dr=twirled(np.diag([1,1,1,np.exp(-1j*delta)]))
        gate.append(dict(delta=delta,balanced=out,dual_rail=dr,
                         quartic_coefficient=out['accepted_nonidentity_probability']/delta**4,
                         erasure_quadratic_coefficient=out['erasure_probability']/delta**2))
    # Arbitrary single-excitation correlated loss is a decisive counterexample.
    corr=[]
    for xi in [.03,.01,.003,.001]:
        gamma=2*.05*I+2*xi*jx
        assert np.linalg.eigvalsh(gamma)[0]>0
        k=np.exp(.05)*(v.conj().T@expm(-gamma/2)@v)
        expected=expm(-xi*X)
        assert norm(k-expected)<1e-13
        corr.append(dict(xi=xi,logical_filter_norm=float(norm(k-np.eye(2),2)),
                         coefficient=float(norm(k-np.eye(2),2)/xi)))
    # A deterministic transfer-matrix example resolves the circuit-length
    # risk: accepted leakage is linear, its in-code feedback is quadratic.
    stream=[]
    for eta in [.02,.01,.005]:
        a=.4*eta**2; b=.7*eta; c=.6*eta; r=.2
        U=expm(-.17j*X)
        M=np.zeros((3,3),complex)
        M[:2,:2]=U+a*Z; M[:2,2]=[b,0]; M[2,:2]=[0,c]; M[2,2]=r
        # Restore a scalar attenuation so this benchmark is a contraction.
        alpha=1/max(1.,norm(M,2))
        contraction=alpha*M
        assert norm(contraction,2)<1+1e-12
        d=a+b*c/(1-r)
        for count in [1,10,100]:
            full=np.linalg.matrix_power(M,count)[:,:2]
            err=float(norm(full[:2]-np.linalg.matrix_power(U,count),2))
            leak=float(norm(full[2:],2))
            eb=(1+d)**count-1; lb=c*(1+d)**(count-1)/(1-r)
            assert err<=eb+1e-12 and leak<=lb+1e-12
            stream.append(dict(eta=eta,cells=count,attenuation_per_cell=alpha,
                               relative_in_code_error=err,in_code_bound=eb,
                               relative_leakage_amplitude=leak,leakage_bound=lb))
    result=dict(code_number_compression_error=float(norm(v.conj().T@n@v-np.eye(2))),
                passive_control_X_error=float(norm(v.conj().T@jx@v-X)),
                idle_channels=rows,kerr_control_channels=gate,
                kerr_quartic_limit=19/64,kerr_erasure_quadratic_limit=5/4,
                correlated_outlet_failure=corr,stream_bound=stream,
                scope='Exact finite benchmark operators; actual code checks, randomization, sensors and native-control errors are separate charged operations.')
    (ROOT/'balanced_gate_noise_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
