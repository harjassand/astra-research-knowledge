#!/usr/bin/env python3
"""Positive-rate exact kernel checks plus an ordinary complex-balanced control."""
from pathlib import Path
from fractions import Fraction as F
import json
from four_nc_axis_kernel import run
P=Path(__file__).resolve().parent

def main():
    cases=[(8,9,(1,2,3,5),(2,1,4,3),F(37,11),F(3,13)),
       (10**12,10**12,(1,2,3,5),(2,1,4,3),2,1),
       (10**12,10**15,(1,2,3,5),(2,1,4,3),2,1),
       (10**12,10**12,(1,1,1,1),(1,1,1,1),1,1),
       (8,9,(1,1,1,1),(10**9,)*4,2,1)]
    rows=[]
    for a,d,alpha,beta,kf,kb in cases:
        r=run(a,d,alpha,beta,kf,kb);rows.append(r)
        print(json.dumps({'axes':[str(a),str(d)],'core_rates':r['core_rates'],
          'eta_cube':r['eta_ratio_cube_exact'],'full_formula_replayed':r['exact_complete_Q_formula_replayed'],
          'time_plus_U_increment':r['mean_physical_time_plus_U_increment'],
          'exact_sign':r['exact_sign_mean_physical_time_plus_U_increment']}))
    (P/'results/four_nc_axis_varied_rates.json').write_text(json.dumps({'fixtures':rows,
      'scope':'Exact positive-rate kernel/formula/cubic-sign checks; core1/unit case is an ordinary complex-balanced control.'},indent=2)+'\n')

if __name__=='__main__':main()
