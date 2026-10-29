import json,time,sys,sympy as s
from pathlib import Path
sys.path.insert(0,'producer-workspace/quaternion_oracle_controller_20261029')
from quartic_sos_oracle import bank_polynomial
from macaulay_template import matrices
r=Path(__file__).parent;q=s.symbols('q0:4');bank=json.load(open('producer-workspace/bank_one_axis.json'));f=bank_polynomial(bank,0);F=sum(s.Rational(c.numerator,c.denominator)*s.prod(q[i]**e[i] for i in range(4)) for e,c in f.items());H=[s.diff(F,v) for v in q]
st=time.time();M,E=matrices(H,q);print('matrices',time.time()-st,flush=True);den=E.det(method='domain-ge');print('den',time.time()-st,den!=0,flush=True);assert den!=0
num=M.det(method='domain-ge');value=s.cancel(num/den);assert value.q==1
(r/'actual_macaulay_value.json').write_text(json.dumps(dict(resultant_of_unscaled_gradient_at_lambda0=str(value),denominator_determinant=str(den),numerator_determinant=str(num),seconds=time.time()-st,scope='One actual bank edge resultant scalar at lambda0. Not a polynomial resultant, derivative extractor, or global optimizer.'),indent=2)+'\n');print('completed',time.time()-st,flush=True)
