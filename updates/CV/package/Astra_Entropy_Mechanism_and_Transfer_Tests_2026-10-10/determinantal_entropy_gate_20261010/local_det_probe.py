#!/usr/bin/env python3
"""Near-vacuum finite Fock-superposition probes, emphasizing high purity."""
import json, math
from pathlib import Path
import numpy as np
import probe


def main():
    M=300; G=2.0
    ts=(0.1,0.3,1.0,3.0,10.0,30.0,100.0,300.0,1000.0)
    epsilons=(0.02,0.05,0.1,0.2)
    bs=(0,1,-1,1j,-1j)
    rows=[]
    for m in (1,2,3,4,6):
      for b in bs:
       for eps in epsilons:
        f=np.zeros(m+1,complex);f[0]=1;f[m]=eps;f/=np.linalg.norm(f)
        g=np.zeros(m+1,complex);g[0]=1;g[m]=eps*b;g/=np.linalg.norm(g)
        psi=probe.output_triangle_cutoff(f,g,G,M)
        rho=psi@psi.conj().T
        rho=(rho+rho.conj().T)/2
        vals=np.maximum(0,np.linalg.eigvalsh(rho))
        tr=float(vals.sum()); p2=float(vals@vals);p3=float(vals@(vals*vals))
        e3=(tr**3-3*tr*p2+2*p3)/6
        tail=probe.tails(f,g,G,M)
        eps_rho=2*math.sqrt(tail['probability_bound'])
        gaps={}; lowers={}
        for t in ts:
          lhs=float(np.log1p(t*vals).sum())
          rhs,thermal_tail=probe.thermal_logdet(G,t,cut=len(vals)+1000)
          gap=lhs-rhs
          err=t*eps_rho+thermal_tail
          gaps[str(t)]=gap;lowers[str(t)]=gap-err
        rows.append({"m":m,"b_over_a":[complex(b).real,complex(b).imag],"epsilon":eps,
                     "purity_cut":p2,"third_moment_cut":p3,"e3_gap_cut":e3-probe.thermal_e3(G),
                     "e3_gap_lower_bound":e3-probe.thermal_e3(G)-eps_rho/2,
                     "logdet_gaps_cut":gaps,"logdet_lower_bounds":lowers,
                     "min_sampled_logdet_lower_bound":min(lowers.values()),
                     "min_sampled_t":min(lowers,key=lowers.get),
                     "tail_probability_bound":tail['probability_bound'],
                     "rho_trace_norm_error_bound":eps_rho,
                     "output_total_photon_cutoff_M":M})
    out={"G":G,"M":M,"t_grid":ts,"epsilons":epsilons,"m_values":[1,2,3,4,6],
         "relative_b_values":[[complex(b).real,complex(b).imag] for b in bs],"rows":rows}
    path=Path(__file__).with_name('local_det_results.json')
    path.write_text(json.dumps(out,indent=2))
    print('cases',len(rows))
    print('purity range',min(r['purity_cut'] for r in rows),max(r['purity_cut'] for r in rows))
    print('e3 min lower',min(r['e3_gap_lower_bound'] for r in rows))
    w=min(rows,key=lambda r:r['min_sampled_logdet_lower_bound'])
    print('min determinant lower',w['min_sampled_logdet_lower_bound'],'m',w['m'],'b',w['b_over_a'],'epsilon',w['epsilon'],'t',w['min_sampled_t'])
    print('worst tail prob',max(r['tail_probability_bound'] for r in rows))
    print('wrote',path)

if __name__=='__main__':main()
