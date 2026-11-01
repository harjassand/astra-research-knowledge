"""Sufficient input-cap Duhamel budgets; deliberately not hardware lower bounds.
Residual H=sum chi_j Z_j n+(K/2)n(n-1).
The reference linear dynamics may populate above the input cap.
"""
import json,math
from pathlib import Path

def moments(N=320,B=1.502,nb=.1):
    A=math.sqrt(N)+B
    F={m:sum(math.comb(m,k)*A**(m-k)*math.sqrt(math.factorial(k))*nb**(k/2) for k in range(m+1)) for m in range(1,5)}
    n=math.sqrt(F[2]**2+F[1]**2)
    nn=math.sqrt(F[4]**2+4*F[3]**2+2*F[2]**2)
    return dict(input_cap=N,maximum_controlled_displacement=B,fresh_thermal_nb=nb,annihilation_power_norm_bounds=F,n_norm_bound=n,n_nminus1_norm_bound=nn)

if __name__=='__main__':
    m=moments();rows=[]
    for T in [1.84,4.472,10.984]:
        for eps in [1e-5,1e-4,1e-3]:
            rows.append(dict(exposure_time=T,allocated_dilation_amplitude=eps,sum_chi_max=eps/(T*m['n_norm_bound']),K_max=2*eps/(T*m['n_nminus1_norm_bound'])))
    pumping=[]
    for alpha in [100,1000,10000]:
        for force in [1.43988243322,2.76946536902,3.]:
            pumping.append(dict(alpha_over_g=alpha,F_over_g=force,xi_upper=1.,Touzard_chi_eff_over_g_lower=force**2/alpha))
    out=dict(moment_bounds=m,budgets=rows,pumped_transmon_relation=pumping,
      conventions='T is in1/g; chi_eff denotes coefficient of Z n, half the q†q n coefficient in Touzard. ForceF=ζ/2. Relationχ_eff=F²/(α|ξ|²) follows their effective model.',
      conclusion='These sufficient worst-cap budgets are not hardware lower bounds. Failure excludes using the unmitigated demonstrated pumping route as evidence for the present certificate; it does not prove no echo/symmetry/better weighted proof can work.')
    Path(__file__).with_name('microscopic_residual_budget_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
