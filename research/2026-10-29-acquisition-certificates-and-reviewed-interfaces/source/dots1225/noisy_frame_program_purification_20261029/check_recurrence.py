import json, sympy as s
from decimal import Decimal, getcontext
from pathlib import Path
getcontext().prec=60
src=json.loads(Path('producer-workspace/check_growth_pollution.json').read_text())
x=s.symbols('x'); vf=s.sympify(src['infidelity']); mf=s.sympify(src['expected_minus_records'])
rows=[]
for eta in [s.Rational(1,100),s.Rational(1,10),s.Rational(1,2)]:
 xx=eta/(8+eta); vexact=vf.subs(x,xx); mexact=mf.subs(x,xx)
 v=Decimal(str(s.N(vexact,65))); mu=Decimal(str(s.N(mexact,65))); pm=Decimal(str(s.N((8+eta)/18,65))); C=Decimal(1); k=0; samples=[]
 for target in [Decimal('0.01'),Decimal('0.0001'),Decimal('0.000001')]:
  while v>target:
   D=2-2*v+Decimal(9)*v*v/8
   C*=4/D; v=v*(1+v/8)/D;k+=1
  samples.append(dict(target=str(target),level=k,v=str(v),base_programs=str(C),expected_source_calls=str(C*mu/pm),transducer_trace_bound=str(8*v/(Decimal(16)/27-2*v))))
 rows.append(dict(eta=str(eta),label_dark=str(xx),initial_infidelity=str(s.N(vexact,20)),base_expected_calls=str(s.N(mexact/((8+eta)/18),20)),targets=samples))
# Exact dense tensor check, diagonal and rotated mixed states.
import numpy as np
rng=np.random.default_rng(103); maxres=0.
for d in [2,3,9]:
 S=np.zeros((d*d,d*d))
 for i in range(d):
  for j in range(d):S[i*d+j,j*d+i]=1
 P=(np.eye(d*d)+S)/2
 for _ in range(5):
  z=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d)); rho=z@z.conj().T;rho/=np.trace(rho)
  out=P@np.kron(rho,rho)@P;out=out.reshape(d,d,d,d);reduced=np.einsum('abcb->ac',out)
  maxres=max(maxres,float(np.linalg.norm(reduced-(rho+rho@rho)/2)))
assert maxres<1e-12
Path(__file__).with_suffix('.json').write_text(json.dumps(dict(rows=rows,max_swap_identity_residual=maxres),indent=2)+'\n')
print(json.dumps(dict(rows=rows,max_swap_identity_residual=maxres),indent=2))
