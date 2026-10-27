"""Independent exact check of weights, backward orientation and residual scope."""
from fractions import Fraction as F
from pathlib import Path
import json
w=[F(1),F(1,2),F(1,4)];rho=w[-1]
H=[[F(2),F(-1),F(-1)],[F(-2),F(4),F(-2)],[F(-4),F(-4),F(8)]]
u=[rho,F(0),F(-1)];gap=F(3)
def apply(v):return [sum(a*b for a,b in zip(row,v)) for row in H]
def dot(a,b):return sum(x*y*z for x,y,z in zip(w,a,b))
def cert(y):
    hy=apply(y);r=[a-b for a,b in zip(u,hy)]
    lower=(2*dot(u,y)-dot(y,hy))/rho
    return lower,lower+dot(r,r)/(rho*gap)
# All three unnormalised conductances are1; weighted gap>=3/max(w)=3.
for i in range(3):
    assert sum(H[i])==0
    for j in range(3):assert w[i]*H[i][j]==w[j]*H[j][i]
assert dot(u,[F(1)]*3)==0
hu=apply(u);s=dot(u,u)/dot(u,hu);first=[s*x for x in u]
lo,hi=cert(first);truth=F(1,6)
assert (lo,hi)==(F(25,168),F(5,28)) and lo<=truth<=hi
assert cert([x+7 for x in first])==(lo,hi)
basis=[u,hu];hb=list(map(apply,basis))
a00=dot(basis[0],hb[0]);a01=dot(basis[0],hb[1]);a11=dot(basis[1],hb[1])
b0=dot(basis[0],u);b1=dot(basis[1],u);det=a00*a11-a01*a01
c0=(b0*a11-b1*a01)/det;c1=(a00*b1-a01*b0)/det
y=[c0*x+c1*z for x,z in zip(*basis)]
assert cert(y)==(truth,truth)
# Independent two-boundary hitting equation: middle h=1/2, exit law equal.
p=F(1,2)+F(1,2)*F(1,2)
assert rho/(2*truth)==p==F(3,4)
out={'scope':'exact finite arithmetic check; all-state proof in PROOF.md',
 'weighted_backward_symmetry':'PASS','constant_component_irrelevance':'PASS',
 'one_step_integral_interval':list(map(str,(lo,hi))),
 'two_step_exact_integral':str(truth),'independent_exit_law_probability':str(p),
 'gap_lower_bound':str(gap)}
Path(__file__).with_name('EXACT_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
