from fractions import Fraction as F
from pathlib import Path
import json,hashlib
import multiface as M,receive_certificate as R
root=Path(__file__).resolve().parent;checks=0
for depth in [0,1,64,1100,3000]:
 x=F(7,3)
 for _ in range(depth):x={'op':'mul','args':[x]}
 assert R.evaluate_expression(x,max_depth=2*depth+2,max_nodes=4*depth+10)==F(7,3);checks+=1
 if depth>64:
  try:R.evaluate_expression(x)
  except M.BudgetRefusal:checks+=1
  else:raise AssertionError('default depth guard bypassed')
  try:R.evaluate_expression(x,max_depth=2*depth+2,max_nodes=10)
  except M.BudgetRefusal:checks+=1
  else:raise AssertionError('node guard bypassed')
# Wide tree and mixed postorder operations; exact arithmetic without recursion.
x={'op':'mul','args':[{'op':'pow','base':F(2,3),'exponent':2},{'op':'mul','args':[F(3,2),F(9,4)]}]}
assert R.evaluate_expression(x)==F(3,2);checks+=1
assert R.evaluate_expression({'op':'mul','args':[1]*5000},max_nodes=6000)==1;checks+=1
try:R.evaluate_expression({'op':'pow','base':2,'exponent':1000},max_power_bits=10)
except M.BudgetRefusal:checks+=1
else:raise AssertionError('power bit guard')
for bad in [True,1.5,{'op':'pow','base':2,'exponent':True},{'op':'pow','base':2,'exponent':-1},{'op':'mul','args':1}]:
 try:R.evaluate_expression(bad)
 except ValueError:checks+=1
 else:raise AssertionError('malformed expression domain')
result=dict(status='PASS_SAME_AUTHOR_ITERATIVE_EXPRESSION_AND_RAISED_DEPTH_REGRESSIONS',checks=checks,bindings={f:hashlib.sha256((root/f).read_bytes()).hexdigest() for f in ['receive_certificate.py','check_iterative_expression.py']})
(root/'iterative_expression_results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
