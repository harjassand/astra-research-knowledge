import sympy as s,json,itertools
from pathlib import Path
root=Path('producer-workspace/four_program_extension')
z=json.loads((root/'certificate.json').read_text());B=s.Matrix(z['B']);ex=[tuple(x) for x in z['exponents']];idx={x:i for i,x in enumerate(ex)}
rows=[]
for t in itertools.product(range(4),repeat=4):rows.append(B[idx[tuple(t.count(i) for i in range(4))],:])
T=s.Matrix.vstack(*rows);blocks=[T[64*i:64*(i+1),:] for i in range(4)]
u=s.zeros(9,1)
for i in [0,4,8]:u[i]=1
P=u*u.T/3
S=s.kronecker_product(s.eye(9),P)+s.kronecker_product(P,s.eye(9))
# Compute partial traces using entrywise Frobenius products.
def inner(A,B):return sum(a*b for a,b in zip(A,B))
C0=s.Matrix(4,4,lambda i,j:s.Rational(16,3)*inner(blocks[i],blocks[j]))
BS=[b*S for b in blocks]
C1=s.Matrix(4,4,lambda i,j:s.Rational(16,3)*inner(BS[i],blocks[j]))
# ideal input P tensor P returns q0^tensor4 with p16/27
C2=s.diag(s.Rational(16,27),0,0,0)
v=s.symbols('v');a=v/8;b=1-9*v/8
O=(a*a*C0+a*b*C1+b*b*C2).applyfunc(s.factor)
assert O==s.diag(O[0,0],O[1,1],O[1,1],O[1,1])
p=s.factor(s.trace(O));w=s.factor(3*O[1,1]/p)
res=dict(C0=str(C0),C1=str(C1),output=str(O),success=str(p),infidelity=str(w),small_v_slope=str(s.limit(w/v,v,0)),values=[dict(input_error=float(x),success=float(p.subs(v,x)),output_error=float(w.subs(v,x))) for x in [s.Rational(0),s.Rational(1,1000),s.Rational(1,100),s.Rational(1,10),s.Rational(8,9)]])
Path(__file__).with_suffix('.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res,indent=2))
