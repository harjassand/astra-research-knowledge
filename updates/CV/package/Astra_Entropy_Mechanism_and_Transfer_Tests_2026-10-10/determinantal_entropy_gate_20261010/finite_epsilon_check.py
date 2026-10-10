#!/usr/bin/env python3
"""Check the gain-2 local e3 coefficient against finite-epsilon outputs."""
import json, math
from pathlib import Path
import numpy as np
import probe


def coefficient(m,a,b):
    A=((4/7)**m+(2/7)**m+(1/7)**m)/7-((2/3)**m+(1/3)**m)/3+4/21
    R=((4/7)**m+(2/7)**m+(-6/7)**m)/7-((2/3)**m+(-2/3)**m)/3
    C=2**(-m/2)*R
    return float(A*(abs(a)**2+abs(b)**2)+2*C*(a*b).real),float(A),float(C)


def e3(rho):
    x=np.trace(rho).real
    x2=np.trace(rho@rho).real
    x3=np.trace(rho@rho@rho).real
    return (x**3-3*x*x2+2*x3)/6


def main():
    epsilons=(0.1,0.05,0.025)
    pairs={1:[(1,0),(1,1),(1,1j)],
           2:[(1,0),(1,1),(1,-1),(1,1j)],
           3:[(1,0),(1,1),(1,-1),(1,1j)],
           4:[(1,0),(1,1),(1,1j)]}
    M=180; G=2.0; rows=[]
    for m,ablist in pairs.items():
      for a,b in ablist:
        target,A,C=coefficient(m,a,b)
        for eps in epsilons:
          f=np.zeros(m+1,complex); f[0]=1; f[m]=eps*a; f/=np.linalg.norm(f)
          g=np.zeros(m+1,complex); g[0]=1; g[m]=eps*b; g/=np.linalg.norm(g)
          psi=probe.output_triangle_cutoff(f,g,G,M)
          rho=psi@psi.conj().T
          gap=float(e3(rho)-probe.thermal_e3(G))
          tb=probe.tails(f,g,G,M)
          trerr=2*math.sqrt(tb['probability_bound'])
          rows.append({"m":m,"a":[complex(a).real,complex(a).imag],"b":[complex(b).real,complex(b).imag],
                       "epsilon":eps,"predicted_quadratic_coefficient":target,
                       "A_m":A,"C_m":C,"e3_gap_cut":gap,"gap_over_epsilon_squared":gap/eps**2,
                       "output_total_photon_cutoff_M":M,"tail_probability_bound":tb['probability_bound'],
                       "rho_trace_norm_error_bound":trerr,"e3_gap_error_bound":trerr/2,
                       "normalized_coefficient_error_bound":trerr/(2*eps**2)})
    out={"gain_G":G,"seed":"none (deterministic fixtures)","input_family":"normalized (|0>+epsilon*a|m>) tensor (|0>+epsilon*b|m>)",
         "epsilons":epsilons,"output_total_photon_cutoff_M":M,"rows":rows}
    path=Path(__file__).with_name('finite_epsilon_results.json')
    path.write_text(json.dumps(out,indent=2))
    for m in pairs:
      rowsm=[r for r in rows if r['m']==m]
      print('m',m)
      for r in rowsm:
        print(' ',tuple(r['a']),tuple(r['b']),'eps',r['epsilon'],'target',r['predicted_quadratic_coefficient'],
              'gap/eps²',r['gap_over_epsilon_squared'],'errbound',r['normalized_coefficient_error_bound'])
    print('wrote',path)

if __name__=='__main__':main()
