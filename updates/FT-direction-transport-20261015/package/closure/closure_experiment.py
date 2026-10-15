"""Forward-only port completion for static linear networks.

This is a synthetic mathematical test, NOT a physical experiment. The tested
protocol receives only source-to-sensor measurements. Matrix access is confined
to the simulated plant and independent reference calculations.

Dependencies: Python 3.10+, NumPy, SciPy. Run: python closure_experiment.py
"""
from __future__ import annotations
import json
from pathlib import Path
from typing import Callable
import numpy as np
from scipy.linalg import lu_factor, lu_solve

ROOT = Path(__file__).resolve().parent

def port_complete(H: np.ndarray, Y: np.ndarray, z: np.ndarray,
                  port_rows: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Recover sensed components of A^{-T} c using only forward observations.

    H = P.T A^{-1} P, Y = sensed A^{-1} P, z = sensed A^{-1} c.
    Requires A = R + P K P.T with R symmetric, and nonsingular A and H.
    H, Y and z must come from the SAME loaded operating condition.
    """
    H, Y, z = np.asarray(H), np.asarray(Y), np.asarray(z)
    r = H.shape[0]
    if H.shape != (r, r) or Y.shape[1] != r or Y.shape[0] != z.size:
        raise ValueError('Inconsistent measurement dimensions')
    invH = np.linalg.solve(H, np.eye(r))
    D = invH.T - invH  # loaded Schur complement's transpose defect
    # Two small solves avoid constructing the inverse in the estimator itself.
    alpha = np.linalg.solve(H, z[port_rows])
    beta = np.linalg.solve(H, (H.T - H) @ alpha)
    return z + Y @ beta, D

def plant(seed: int, n: int = 64, m: int = 30):
    rng = np.random.default_rng(seed)
    R = np.diag(rng.uniform(.4, 1.2, n))
    # A sparse resistor network with a connected backbone plus hidden loops.
    edges = [(i, (i+1) % n) for i in range(n)]
    edges += [tuple(rng.choice(n, 2, replace=False)) for _ in range(2*n)]
    for i, j in edges:
        g = rng.uniform(.2, 1.5)
        R[i,i] += g; R[j,j] += g; R[i,j] -= g; R[j,i] -= g
    all_control = [(i,j) for i in range(12) for j in range(i+1,12)]
    idx = rng.choice(len(all_control), m, replace=False)
    controls = [all_control[k] for k in idx]
    V = np.zeros((n,m))
    for k,(i,j) in enumerate(controls):
        V[i,k] = 1; V[j,k] = -1
    p = rng.uniform(.1,.5,m)
    R += (V*p) @ V.T
    ports = np.arange(12,16)
    P = np.eye(n)[:,ports]
    C = rng.normal(size=(4,4)); C = 2*(C-C.T)
    A = R + P @ C @ P.T
    b = np.eye(n)[:,0]
    c = np.eye(n)[:,16]
    sensors = np.arange(17)
    return A,b,c,P,sensors,ports,V,p

def run(seed: int, noise: float = 0., hidden_defect: float = 0.):
    A,b,c,P,sensors,ports,V,p = plant(seed)
    if hidden_defect:
        A[30,31] += hidden_defect; A[31,30] -= hidden_defect
    lu = lu_factor(A)
    # Exact prototype uses 1 + r + 1 settled source profiles.
    measured = lu_solve(lu, np.column_stack([b,P,c]))[sensors,:]
    rng = np.random.default_rng(100000+seed)
    if noise:
        # Per-entry additive Gaussian noise, scaled to each profile's RMS.
        # This is an assumed noise model, not estimated from experimental data.
        measured += rng.normal(size=measured.shape)*noise*np.sqrt(
            np.mean(measured**2,axis=0,keepdims=True))
    x_s = measured[:,0]; Y = measured[:,1:-1]; z = measured[:,-1]
    H = Y[ports,:]
    lam_s,D_est = port_complete(H,Y,z,ports)
    V_s = V[sensors,:]
    grad = -(V_s.T @ x_s)*(V_s.T @ lam_s)
    naive = -(V_s.T @ x_s)*(V_s.T @ z)
    x = lu_solve(lu,b)
    ref_lam = np.linalg.solve(A.T,c)
    ref = -(V.T @ x)*(V.T @ ref_lam)
    norm = lambda v: float(np.linalg.norm(v))
    relative = lambda v: norm(v-ref)/max(norm(ref),1e-300)
    direction = np.random.default_rng(seed+20000).normal(size=len(p))
    direction /= norm(direction)
    E = (V*direction) @ V.T
    h = 1e-5
    fd = (c @ np.linalg.solve(A+h*E,b)-c @ np.linalg.solve(A-h*E,b))/(2*h)
    deriv = ref @ direction
    B = np.eye(4)+D_est@H
    return {
        'seed':seed,'noise_rms_fraction':noise,'hidden_defect':hidden_defect,
        'corrected_gradient_relative_error':relative(grad),
        'uncorrected_gradient_relative_error':relative(naive),
        'sensed_adjoint_relative_error':norm(lam_s-ref_lam[sensors])/norm(ref_lam[sensors]),
        'directional_fd_absolute_error':float(abs(fd-deriv)),
        'condition_H':float(np.linalg.cond(H)),
        'condition_correction':float(np.linalg.cond(B)),
        'determinant_correction':float(np.linalg.det(B)),
        'port_defect_error':float(np.linalg.norm(D_est-P.T@(A.T-A)@P)),
        'n_states':64,'n_parameters':30,'n_sensed_states':17,
        'source_profiles':6,'scalar_field_readings':102,
    }

def analytic_pair():
    records=[]
    v=np.array([1.,-1.,0.]); b=np.array([2.,-1.,0.]);c=np.array([0.,0.,1.])
    for k in [-1.,1.]:
        A=np.eye(3)+np.outer(v,v)
        A[1,2]+=k;A[2,1]-=k
        x=np.linalg.solve(A,b); z=np.linalg.solve(A,c)
        P=np.eye(3)[:,[1,2]];Y=np.linalg.solve(A,P);H=P.T@Y
        lam,D=port_complete(H,Y,z,np.array([1,2]))
        g=-float(v@x)*float(v@lam)
        records.append({'k':k,'baseline_state':x.tolist(),
                        'output_derivative':g,
                        'uncorrected_derivative':-float(v@x)*float(v@z),
                        'exact_derivative':k/(3+2*k*k)})
    return records

def indistinguishable_acquisition_pair():
    """Identical complete measured data, but opposite action gradients.

    The pair VIOLATES the declared support assumption, so this is not a
    counterexample to port completion. It proves that the specified acquisitions
    do not certify that support assumption, even with full-state readout.
    """
    eye = np.eye(5)
    b, c = eye[:,0], eye[:,1]
    P = eye[:,[2,4]]
    v = eye[:,0] - eye[:,3]
    records = []
    responses = []
    for sign in [-1.,1.]:
        A = eye + sign*np.outer(eye[:,1],eye[:,3])
        M = np.linalg.solve(A,np.column_stack([b,P,c]))
        responses.append(M)
        x, Y, z = M[:,0], M[:,1:3], M[:,-1]
        lam, D = port_complete(P.T@Y,Y,z,np.array([2,4]))
        reference = np.linalg.solve(A.T,c)
        true_grad = -float(v@x)*float(v@reference)
        estimated_grad = -float(v@x)*float(v@lam)
        assert np.allclose(true_grad,-sign)
        assert np.allclose(estimated_grad,0.)
        records.append({
            'sign':sign,'matrix':A.tolist(),
            'minimum_symmetric_part_eigenvalue':float(np.linalg.eigvalsh((A+A.T)/2).min()),
            'measured_response_matrix':M.tolist(),
            'true_adjoint':reference.tolist(),
            'true_derivative':true_grad,
            'support_assumed_estimate':estimated_grad,
        })
    assert np.array_equal(responses[0],responses[1])
    return {'status':'EXACT CONSTRUCTED COUNTEREXAMPLE TO SUPPORT CERTIFICATION, NOT TO THE THEOREM',
            'maximum_observed_difference':float(np.abs(responses[0]-responses[1]).max()),
            'records':records}

def main():
    records=[run(s) for s in range(100)]
    noisy={str(a):[run(s,noise=a) for s in range(50)] for a in [1e-5,1e-3,1e-2]}
    missed=[run(s,hidden_defect=2.) for s in range(50)]
    def stats(rs):
        return {k:{'median':float(np.median([r[k] for r in rs])),
                   'max':float(np.max([r[k] for r in rs]))}
                for k in ['corrected_gradient_relative_error',
                          'uncorrected_gradient_relative_error',
                          'sensed_adjoint_relative_error',
                          'directional_fd_absolute_error','condition_H','condition_correction']}
    result={'status':'SYNTHETIC ONLY; no physical validation or novelty claim',
            'exact_100_networks':stats(records),
            'assumed_noise_50_networks_each':{k:stats(v) for k,v in noisy.items()},
            'missed_hidden_nonreciprocity_50_networks':stats(missed),
            'opposite_action_pair':analytic_pair(),
            'indistinguishable_acquisition_pair':indistinguishable_acquisition_pair(),
            'records':records,'noisy_records':noisy,'missed_defect_records':missed}
    (ROOT/'synthetic_results.json').write_text(json.dumps(result,indent=2))
    print(json.dumps({k:v for k,v in result.items() if 'records' not in k},indent=2))

if __name__=='__main__':main()
