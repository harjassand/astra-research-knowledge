"""Exact rational, very conservative, public trace-rate threshold.

Outputs a symbolic bound L>=2**b; it NEVER constructs that huge integer.
No spectral matrix, Gamma evaluation, numerical integration or external
package is used. See quantitative_rate.txt Sections 8.3--8.5.

Run: python3 outputs/research/sol_attractive_critical/rate_certificate.py
Optional parameters are exact rational strings, e.g. --tau 1/50.
This certifies the internally proved candidate's scalar arithmetic, not
external mathematical validity or a feasible physical experiment.
"""
import argparse
from fractions import Fraction as F
import json


def ceiling(x):
    return -((-x.numerator)//x.denominator)


def certificate(j, tau, B, gmin, gmax, alpha, beta, eb_floor):
    assert j > 0 and tau > 0 and B >= 0 and 0 < gmin <= gmax
    assert 0 < beta < alpha < F(1,384) and 0 < eb_floor <= 2
    c = min(gmin/96, j/72)
    a = tau*c
    C = 2+1/(j*tau)
    b = 1+C+tau*(B+c)
    k = 1+(1+gmax)/2*(1+F(45,16)*(1+1/j))
    d = 1+2*gmax*(1+1/j)
    A = (1+d)*k*(1+1/(18*j))
    Z = k*(1+1/(18*j))
    T = 6+Z
    D = 1+1/gmin+2*(1+1/j)
    E0 = 2+3*gmax/j
    L0 = E0+2*D+D*D
    E = 8*(1+A)**2+512*j+4*gmax
    U = 2*A+A*A+E+2*T+T*T
    fm = D+1+U+L0
    htau = 4+(tau+3)**2/tau
    O = htau*(1+fm)
    cr = 2*b/a+2+1/(192*a)
    q0 = 1+1/(1728*tau*j)
    C1 = 24*(1+O)+4*(1+1/a)
    C2 = tau*B+1+C+F(1,3)
    C3 = C2+q0+cr+(cr+1)/6
    C0 = C1+2*(cr+1)
    drate = C0+2+cr*C3+F(7,6)*cr
    delta = F(1,384)-alpha
    s_rate = max(F(4),4*cr*cr,(drate/delta)**4)
    # log x <= x supplies an exact rational upper bound on the additional
    # log-chain threshold  log(4/eb_floor)/(alpha-beta).
    s_joint = max(s_rate,4/(eb_floor*(alpha-beta)))
    b_rate, b_joint = ceiling(2*s_rate), ceiling(2*s_joint)
    # log(2)>=1/2, so L>=2**b implies log L>=b/2>=s_*.
    return {
        "status":"EXACT-RATIONAL-ARITHMETIC-CERTIFICATE",
        "scientific_status":"INTERNALLY-PROVED-CANDIDATE; external validity UNKNOWN",
        "inputs":{key:str(value) for key,value in {
            "J":j,"tau":tau,"B":B,"g_min":gmin,"g_max":gmax,
            "alpha":alpha,"copy_exponent_beta":beta,"continuum_EB_floor":eb_floor}.items()},
        "uniform_trace_bound":"Delta_L <= L**(-alpha) for L >= 2**rate_exponent",
        "rate_exponent":str(b_rate),
        "joint_chain_exponent":str(b_joint),
        "joint_consequence":"For n=floor(L**beta), continuum transport loss 2*n*Delta_L <= EB_floor/2 whenever L >= 2**joint_chain_exponent.",
        "selected_thermal_floor_gate":"The EB consequence requires the supplied EB floor to be a proved continuum floor for the selected states. The default 5e-21 is proved only at J=1,tau=1/50,lambda=0,g=.1 and .1+.1/sqrt(n); arbitrary changed model parameters do not inherit that floor.",
        "constants":{key:str(value) for key,value in {
            "c":c,"a":a,"C_upper":C,"logA_upper":b,"F_star_upper":fm,
            "c_r_upper":cr,"D_rate_upper":drate}.items()},
        "construction_cost":"Fixed number of exact rational operations in the bit length of public rational parameters. Huge power 2**b is symbolic, never materialized. No Galerkin/spectrum oracle.",
        "limitation":"Deliberately enormous sufficient threshold; not a practical margin, energy-accuracy result or external theorem validation."
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    defaults = {"J":"1","tau":"1/50","B":"0","g_min":"1/10","g_max":"1/5",
                "alpha":"1/768","beta":"1/1536","eb_floor":"1/200000000000000000000"}
    for key,value in defaults.items():
        parser.add_argument("--"+key.replace("_","-"),default=value,type=F)
    args=parser.parse_args()
    result=certificate(args.J,args.tau,args.B,args.g_min,args.g_max,args.alpha,args.beta,args.eb_floor)
    print(json.dumps(result,indent=2))
