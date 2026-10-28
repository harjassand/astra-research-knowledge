"""Literal independent replay of the actual two-point penalty obstruction."""
from pathlib import Path
import sympy as s,json
out=Path(__file__).resolve().parent
alpha=s.sqrt(110)/240
U=s.Matrix([[alpha*s.Rational(12,5),-alpha*s.Rational(12,5)],[-s.Rational(1,25),-s.Rational(1,25)]])/s.sqrt(s.Rational(3591,10000))
V=s.Matrix([[1,s.sqrt(110)/2],[1,-s.sqrt(110)/2]])
A=s.diag(36,35)/s.sqrt(2521)
def energy(B):
    a,b,c,d=list(B);q=a*d-b*c
    return s.expand((a*a+b*b+c*c+d*d)**2+s.Rational(252,25)*q*q+s.Rational(99,25)*q*(a*a+c*c-b*b-d*d))
t,m=s.symbols('t m',real=True)
fp=energy(A+U*s.diag(t,-t)*V);fm=energy(A+U*s.diag(-t,t)*V)
expr=s.Poly(s.simplify((fp+fm)/2-energy(A)+2*m*t*t*(1+4*t*t)),t)
L=s.Rational(59139344,45264555);d4=s.Rational(17245888,12895281)
assert s.expand(expr.as_expr()-2*(m-L)*t*t-(d4+8*m)*t**4)==0
gap=s.factor((L-1)**2/(d4+8))
assert gap==s.Rational(192509769794521,19131170106699400)>0
for ij in [(0,0),(0,1),(1,0),(1,1)]:
    E=s.zeros(2);E[ij]=1;B=U*E*V
    assert s.simplify(B.det())==0 and s.simplify(sum(x*x for x in B))==1
    assert s.simplify(energy(B))==1
record={'status':'INDEPENDENT_LITERAL_PENALTY_REPLAY_PASS','required_M':str(L),'offplane_quartic_budget':'1',
        'value_loss_for_0_leq_M_leq_1':str(gap),
        'scope':'value-preserving construction only; no arbitrary recentering exclusion or target QC decision'}
(out/'REPLAY.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
