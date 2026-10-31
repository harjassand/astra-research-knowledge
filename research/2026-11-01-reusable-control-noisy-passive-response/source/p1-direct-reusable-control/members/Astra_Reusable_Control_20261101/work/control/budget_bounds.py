#!/usr/bin/env python3
"""Exact sufficient uniform budgets. These are NOT information lower bounds."""
from fractions import Fraction as F
from math import factorial,comb,log10
from pathlib import Path
import json

def bounds(q,k):
    A=sum((q**j/F(factorial(j)) for j in range(k+1)),F(0))
    e=q**k/F(factorial(k))/A
    B=sum((F(a)*q**(a+b-1)/F(factorial(a-1)*factorial(b))
           for a in range(1,k+1) for b in range(max(0,k+1-a),k+1)),F(0))
    C=comb(2*k-1,k)
    deterministic=C*A*A*e+(C+1)*B+e
    return A,e,B,C,deterministic

def main():
    tau=F(1,100); rows=[]
    for q in [F(1,10),F(1),F(3)]:
        for k in range(1,120):
            A,e,B,C,z=bounds(q,k)
            if z<=tau/2:break
        else:raise RuntimeError('no budget found')
        xi=tau/(4*C*A*A)
        assert z+2*C*A*A*xi<=tau
        nodes=comb(1000+k,k)
        rows.append({'q':str(q),'target_width':str(tau),'r_equals_k':k,
                     'node_radius_exact':str(xi),'node_radius_float':float(xi),
                     'deterministic_allowance_exact':str(z),
                     'n1000_number_settings':str(nodes),'n1000_log10_settings':log10(nodes)})
    demo=2*F(1,10**6)*comb(11,6)*(sum((F(4)**j/F(factorial(j)) for j in range(4)),F(0)))**2
    report={'scope':'sufficient uniform bound; n>r, not source-specific lower costs',
            'rows':rows,'full_degree_demo_generic_uniform_width_exact':str(demo),
            'full_degree_demo_generic_uniform_width_float':float(demo)}
    p=Path(__file__).with_name('budget_results.json');p.write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
