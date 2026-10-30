"""Coarse scalar-area leakage filter and a state-dependent-gain failure."""
from pathlib import Path
import json,math
import numpy as np
from scipy.linalg import expm
HERE=Path(__file__).resolve().parent
def norm(a):return float(np.linalg.norm(a,2))

def main():
    q=np.diag([2.,-2.,0.,0.,0.,0.]);pc=np.diag([1.,1.,0.,0.,0.,0.]);pa=np.eye(6)-pc
    zc=np.diag([1.,-1.,0.,0.,0.,0.]);zm=np.diag([1.,-1.])
    plus=np.array([1.,1.])/math.sqrt(2);minus=np.array([1.,-1.])/math.sqrt(2)
    initial=np.kron(np.eye(6),plus[:,None]);rows=[]
    for a in [math.pi/8,math.pi/4,3*math.pi/8,.271*math.pi]:
        u=expm(-1j*a*np.kron(q,zm))
        k0=np.kron(np.eye(6),plus[None,:])@u@initial
        k1=np.kron(np.eye(6),minus[None,:])@u@initial
        rows.append(dict(area=a,no_operator_residual=norm(k0-pa-math.cos(2*a)*pc),
            yes_operator_residual=norm(k1+1j*math.sin(2*a)*zc),
            adjacent_false_acceptance=norm(k1@pa),
            state_independent_code_probability=math.sin(2*a)**2))
    history=[math.pi/8,.271*math.pi,3*math.pi/8,math.pi/6]
    gamma=1.;success=0.;repeats=[]
    for j,a in enumerate(history,1):
        success+=gamma**2*math.sin(2*a)**2
        gamma*=math.cos(2*a)
        repeats.append(dict(probes=j,accepted_probability=success,unverified_code_probability=gamma**2,
            qualified_upper_bound=2.**(-j)))
    # Initial logical/gauge Bell state, gain area depends on gauge.
    weights=np.sin(2*np.array([math.pi/8,math.pi/4]))**2
    posterior=weights/weights.sum()
    result=dict(scope='Physical Q_D Z_meter instrument on all six N=2 data configurations. Scalar area may be unknown; a quantum gain is a different resource.',
        actual_meter_checks=rows,nonconstant_scalar_history=repeats,
        correlated_quantum_gain_failure=dict(initial_logical_probabilities=[.5,.5],
            accepted_logical_probabilities=posterior.tolist(),
            conditional_logical_trace_distance=float(np.abs(posterior-.5).sum()/2)))
    (HERE/'coarse_filter_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
