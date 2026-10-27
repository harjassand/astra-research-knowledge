import sympy as s
from pathlib import Path
import json
m,b,k=s.symbols('m b k',positive=True)
f=4*b/(m+3)-1/m-(b-1)
expected=(m-1)*(3-(b-1)*m)/(m*(m+3))
assert s.simplify(f-expected)==0
beta=1+3/k
assert s.simplify(1/beta-k/(k+3))==0
assert s.simplify(1-2/beta-(3-k)/(k+3))==0
assert ((3-k)/(k+3)).subs(k,s.Rational(9,5))==s.Rational(1,4)
report={'status':'PASS','gradient_factorization_exact':True,'source_contraction':'k/(k+3)','VALUE_margin_for_k_below_3':'(3-k)/(k+3)','nine_fifths_margin':'1/4','scope':'constants only; full two-face/integral argument needs independent receipt'}
Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
