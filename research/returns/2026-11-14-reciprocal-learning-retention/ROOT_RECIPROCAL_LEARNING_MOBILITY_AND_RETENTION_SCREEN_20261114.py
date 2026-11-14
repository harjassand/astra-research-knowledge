"""Original conditional thermodynamic diagnostic for physical learning states.

Not a universal memory bound or material fit. Assumes constant reciprocal
dissipative Onsager coefficients, a flat state free energy, one isothermal bath,
and the SAME always-on mobility while writing and retaining an observable.
The numerical matrices are INTRODUCED dimensionless examples. No producer
code/data, experiment, or stochastic Monte Carlo evidence is used.
"""
from fractions import Fraction as F
from pathlib import Path
import json
import math

KB = 1.380649e-23  # exact SI definition, J/K


def dot(a,b):return sum(x*y for x,y in zip(a,b))
def mv(a,b):return [dot(row,b) for row in a]
def transpose(a):return [list(row) for row in zip(*a)]


def normal_quantile(p):
    lo,hi=-12.0,12.0
    for _ in range(90):
        mid=(lo+hi)/2
        if .5*(1+math.erf(mid/math.sqrt(2)))<p:lo=mid
        else:hi=mid
    return (lo+hi)/2


def rational_json(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,list):return [rational_json(y) for y in x]
    if isinstance(x,dict):return {k:rational_json(v) for k,v in x.items()}
    return x


def main():
    # Flows (Q, xdot) = [[G,C],[C^T,M]] * (p,A), A=-grad_x F.
    G=[[F(2),F(0)],[F(0),F(3)]]
    Ginv=[[F(1,2),F(0)],[F(0),F(1,3)]]
    C=[[F(1,5),F(1,10)],[F(-1,10),F(3,10)]]
    Ct=transpose(C)
    minimum_M=[[dot(Ct[i],mv(Ginv,Ct[j])) for j in range(2)] for i in range(2)]
    excess=[[F(1,100),F(3,1000)],[F(3,1000),F(1,50)]]
    assert excess[0][0]>0 and excess[0][0]*excess[1][1]-excess[0][1]**2>0
    M=[[minimum_M[i][j]+excess[i][j] for j in range(2)] for i in range(2)]
    a=[F(1),F(-1,2)]
    b=mv(C,a)
    theta=dot(b,mv(Ginv,b))
    eta=dot(a,mv(M,a))
    assert theta==F(77,2400)
    assert eta-theta==F(3,250)
    # Minimum-energy constant pressure for unit mean observable change in
    # normalized time1. This optimality is only the fixed linear model.
    p=[x/theta for x in mv(Ginv,b)]
    change=dot(b,p)
    work=dot(p,mv(G,p))
    assert change==1
    assert work*theta==1
    ratio=work*eta
    assert ratio>=1
    # Complete-square identity checks the thermodynamic closure, not just a
    # sampled positive-entropy claim.
    max_identity_error=F(0)
    for k in range(13):
        force=[F(k-6,7),F((3*k)%11-5,9)]
        affinity=[F((5*k)%13-6,8),F(4-k,10)]
        flux_q=[x+y for x,y in zip(mv(G,force),mv(C,affinity))]
        flux_x=[x+y for x,y in zip(mv(Ct,force),mv(M,affinity))]
        dissipation=dot(force,flux_q)+dot(affinity,flux_x)
        shifted=[x+y for x,y in zip(force,mv(Ginv,mv(C,affinity)))]
        square=dot(shifted,mv(G,shifted))+dot(affinity,mv(excess,affinity))
        max_identity_error=max(max_identity_error,abs(dissipation-square))
        assert dissipation>=0
    assert max_identity_error==0
    # A declared one-way, noiseless update Q=p, xdot=p with no affinity
    # backreaction or mobility gives negative entropy production at p=1,A=-2.
    triangular_dissipation=F(1)*F(1)+F(-2)*F(1)
    assert triangular_dissipation==-1

    temperature=298.15  # INTRODUCED reference temperature, not a measurement
    cases=[]
    z99=normal_quantile(.995)
    for write,hold,error in [(1.0,86400.0,.01),(.001,86400.0,.001),
                             (.001,365.25*86400,.001),
                             (1e-6,10*365.25*86400,.01)]:
        energy=2*KB*temperature*hold/(write*error**2)
        cases.append({"write_s":write,"hold_s":hold,"relative_RMS_error":error,
                      "necessary_drive_work_J_flat_always_on_model":energy,
                      "necessary_drive_work_J_for_99pct_Gaussian_endpoint":energy*z99**2,
                      "meaning":"Endpoint only, not pathwise reliability, measured retention, or a universal memory requirement."})
    # A kinetic gate changes M between write and retention. Thermodynamics
    # permits C_off=0, M_off=r*M_on; actual gate mechanism/work are NOT supplied.
    gates=[]
    for rho in [1.0,1e-3,1e-6]:
        gates.append({"hold_to_write_mobility_ratio":rho,
                      "relative_hold_variance_at_same_write":rho,
                      "qualifier":"The always-on inequality cannot be applied unchanged across this gate. Gate work and retention mechanism are unknown."})
    result={
        "status":"CONDITIONAL_RECIPROCAL_LINEAR_DISSIPATIVE_MODEL_NOT_UNIVERSAL_BOUND",
        "scope":["One isothermal bath; overdamped, reciprocal, purely dissipative Onsager coupling.",
                 "Even state coordinates, no magnetic/gyroscopic/Casimir or active chemostat channel omitted.",
                 "Constant G,C,M while teaching and retaining; flat state free energy and a locally linear useful observable y=a^T x.",
                 "No reflecting barrier, metastable well, nonlinear threshold or retention gate in the always-on calculation."],
        "closure":{
            "law":"[Q,xdot]=[[G,C],[C^T,M]]*[p,A], A=-grad F",
            "entropy_production":"T sigma = p^T Q + A^T xdot",
            "necessary_schur_condition":"M-C^T G^-1 C is positive semidefinite",
            "noise_covariance_of_state":"2 k_B T M dt",
            "flat_observable_noise":"Var_hold=2 k_B T a^T M a * t_hold",
            "write_retention_inequality":"W_drive * Var_hold >= 2 k_B T (mean_delta_y)^2 t_hold/t_write",
            "scope_of_work":"Mean work through the declared pressure/flow channels for flat F. Instruments, preparation, mode changes, other work reservoirs and physical fabrication are not supplied."},
        "introduced_matrix_example":{"G":G,"C":C,"M_minimum":minimum_M,
                                     "M":M,"observable_a":a,"theta":theta,"eta":eta,
                                     "optimal_normalized_pressure":p,"unit_change_work":work,
                                     "bound_ratio":ratio,"exact_square_identity_error":max_identity_error},
        "incomplete_one_way_counterexample":{"p":1,"A":-2,"Q":1,"xdot":1,
                                             "T_sigma":-1,
                                             "limit":"This refutes closure of this declared noiseless one-way law over unrestricted affinities, not all irreversible/active/nonlinear learning mechanisms."},
        "introduced_reference_temperature_K":temperature,"Gaussian_endpoint_z99":z99,
        "illustrative_parameter_cases":cases,"gate_counterexample":gates,
        "limits":["Schur complements and fluctuation-dissipation are established physics; no novelty claim is made.",
                  "A protected nonlinear memory or a change of mobility can evade the constant always-on model without violating thermodynamics.",
                  "No actual gate, state-energy landscape, material range, sensor error, full teaching controller or usable bulk device is constructed.",
                  "This constrains a candidate physical implementation; it does not invalidate earlier conditional state-control algebra."],
    }
    out=Path(__file__).with_suffix('.json');out.write_text(json.dumps(rational_json(result),indent=2,sort_keys=True)+'\n')
    print(json.dumps({"output":str(out),"matrix_theta":str(theta),"matrix_eta":str(eta),
                      "bound_ratio":str(ratio),"one_way_T_sigma":-1,
                      "introduced_cases":cases,"z99":z99},indent=2))


if __name__=='__main__':main()
