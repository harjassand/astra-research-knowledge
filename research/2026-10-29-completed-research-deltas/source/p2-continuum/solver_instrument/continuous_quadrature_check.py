#!/usr/bin/env python3
import json
from continuous_galerkin import run,OUT
if __name__=='__main__':
    r,b,y=run([0.,.3,.6],2,steps=80,quad_order=8,label='continuous_three_K2_q8')
    old=json.loads((OUT/'continuous_three_K2_receipt.json').read_text())
    r['quadrature_comparison']={
      'previous_order':old['quadrature_order'],
      'previous_residual_integral':old['residual_integral_diagnostic'],
      'absolute_difference':abs(r['residual_integral_diagnostic']-old['residual_integral_diagnostic']),
      'scope':'Convergence diagnostic, not an interval quadrature certificate.'}
    (OUT/'continuous_three_K2_q8_receipt.json').write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps(r['quadrature_comparison'],indent=2))
