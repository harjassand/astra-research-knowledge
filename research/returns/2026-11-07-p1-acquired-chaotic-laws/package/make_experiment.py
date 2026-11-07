"""SOURCE-AWARE synthetic one-step experiment, separate from the learner.

The actual smooth source is the formula below, not a floating-point lookup.
The reported outputs are finite integers; rigorous sine rounding plus bounded
deterministic disturbances warrant the declared positive observation error.
No physical observations or physical-cost measurements are claimed.
"""
from fractions import Fraction as F
from math import factorial
from pathlib import Path
import hashlib
import json
import time
import numpy as np
from exact_core import floor, dyadic_round

ROOT = Path(__file__).resolve().parent
Q = 1 << 30
q = 16
loop_steps = 32
d = 4
REPORT_COUNT = 0
A = np.array([[2,1,0,0],[1,1,0,0],[0,0,2,1],[0,0,1,1]], dtype=np.int64)
b = [F(1, 7), F(1, 11), F(1, 13), F(1, 17)]


def atan_interval(inv, n):
    s = sum((F((-1)**j, (2*j+1)*inv**(2*j+1)) for j in range(n)), F(0))
    next_term = F((-1)**n, (2*n+1)*inv**(2*n+1))
    return min(s, s+next_term), max(s, s+next_term)


def sine_integer_table(amplitude=F(1,4096)):
    # Machin identity pi = 16 atan(1/5) - 4 atan(1/239).
    a, bnd = atan_interval(5, 70), atan_interval(239, 20)
    pi_lo, pi_hi = 16*a[0]-4*bnd[1], 16*a[1]-4*bnd[0]
    pi_mid = dyadic_round((pi_lo + pi_hi) / 2, 140)
    pi_err = max(abs(pi_mid-pi_lo), abs(pi_mid-pi_hi))
    assert F(3) < pi_lo < pi_hi < F(22, 7)
    out = []
    proof = []
    for j in range(32):
        k = j if j <= 16 else j-32
        if k > 8:
            k = 16-k
        if k < -8:
            k = -16-k
        z = pi_mid * F(k, 16)
        approx = sum(((-1)**r*z**(2*r+1)/factorial(2*r+1)
                      for r in range(24)), F(0))
        error = abs(z)**49 / factorial(49) + pi_err * F(abs(k), 16)
        scaled_lo, scaled_hi = (approx-error) * Q*amplitude, (approx+error) * Q*amplitude
        nlo, nhi = floor(scaled_lo+F(1,2)), floor(scaled_hi+F(1,2))
        assert nlo == nhi
        out.append(nlo)
        proof.append({"phase_index":j,"rounded_integer":nlo,
                      "enclosure_width":str(scaled_hi-scaled_lo)})
    return np.array(out,dtype=np.int64), {"machin_pi_lower":str(pi_lo),
        "machin_pi_upper":str(pi_hi),"sine_rounding_certificates":proof}


def reports(z, sine):
    """Input z/32; a unique deterministic bounded error per input."""
    global REPORT_COUNT
    REPORT_COUNT += len(z)
    affine = (z @ A.T) * (Q//32)
    affine += np.array([floor(t*Q+F(1,2)) for t in b],dtype=np.int64)
    phase = np.column_stack([(z[:,(i+1)%d]+z[:,(i+2)%d])%32 for i in range(d)])
    nonlinear = sine[phase]
    # No randomness and no averaging: the errors may be correlated/adversarial.
    code = z @ np.array([17,113,721,1709],dtype=np.int64)
    errors = np.column_stack([((code*(37+2*i)+(i+1)*467)%2049)-1024
                             for i in range(d)])
    return ((affine+nonlinear+errors)%Q).astype(np.uint32)


def main():
    started=time.perf_counter()
    sine, proof = sine_integer_table()
    grid = np.indices((q,)*d,dtype=np.int64).reshape(d,-1).T
    ygrid = reports(2*grid,sine).reshape((q,)*d+(d,))
    loops=[]
    for j in range(d):
        ys=np.empty((loop_steps,d),dtype=np.uint32)
        # Reuse reports literally; no repeated source evaluation is uncharged.
        ys[::2]=ygrid[tuple(slice(None) if axis==j else 0 for axis in range(d))]
        z=np.zeros((loop_steps//2,d),dtype=np.int64)
        z[:,j]=2*np.arange(loop_steps//2)+1
        ys[1::2]=reports(z,sine)
        loops.append(ys)
    loops=np.stack(loops)
    # The origin and even loop points reuse existing grid records.
    unique_calls=q**d+d*(loop_steps//2)
    assert REPORT_COUNT == unique_calls
    np.savez_compressed(ROOT/"observations.npz",grid=ygrid,loops=loops)
    # Vector Euclidean error <= 2*(1024+1)/Q, including both roundings.
    native_error=F(2*1025,Q)
    eta=F(1,1<<18)
    assert native_error < eta
    # Elementary supplied smoothness guards, using pi < 22/7 and sqrt(2)<10/7.
    two_pi=F(44,7)
    lguard=4*F(1,4096)*two_pi*F(10,7)
    m2guard=4*F(1,4096)*two_pi**2*2
    m3guard=4*F(1,4096)*two_pi**3*2*F(10,7)
    assert F(21,8)+lguard < 3
    assert m2guard < F(1,10)
    assert m3guard < F(3,4)
    contract={"dimension":d,"grid_side":q,"loop_steps":loop_steps,
              "output_denominator":Q,"B":"3","M2":"1/10","M3":"3/4",
              "effective_euclidean_error":str(eta),
              "unique_one_step_queries":unique_calls,
              "returned_scalar_count":d*unique_calls,
              "source_class":"stationary C3 map on the declared closed torus state",
              "preparation":"exact rational software preparation; no physical preparation claimed",
              "readout":"30-bit coordinate outputs with fixed deterministic bounded errors",
              "no_true_homology_or_formula_supplied_to_learner":True}
    (ROOT/"contract.json").write_text(json.dumps(contract,indent=2)+"\n")
    proof.update({"source_formula":"F_i(x)=(A x)_i+b_i+sin(2*pi*(x_(i+1)+x_(i+2)))/4096 mod 1; indices cyclic",
        "true_A":A.tolist(),"true_b":[str(t) for t in b],
        "max_native_euclidean_error_bound":str(native_error),
        "declared_error":str(eta),"residual_Lipschitz_guard":str(lguard),
        "second_derivative_guard":str(m2guard),"third_derivative_guard":str(m3guard),
        "unique_one_step_queries":unique_calls,
        "executed_native_forward_evaluations":REPORT_COUNT,
        "observation_sha256":hashlib.sha256((ROOT/"observations.npz").read_bytes()).hexdigest(),
        "wall_seconds":time.perf_counter()-started})
    (ROOT/"SOURCE_CHECK.json").write_text(json.dumps(proof,indent=2)+"\n")
    print(json.dumps({"queries":unique_calls,"scalar_reports":d*unique_calls,
                      "effective_error":str(eta),"generation_seconds":proof["wall_seconds"]}))


if __name__=="__main__":
    main()
