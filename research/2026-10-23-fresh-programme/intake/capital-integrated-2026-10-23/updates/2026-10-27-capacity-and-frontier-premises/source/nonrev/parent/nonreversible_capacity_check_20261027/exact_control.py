"""Independent exact nonreversible normalizer and dual-residual control."""
from fractions import Fraction as F
from pathlib import Path
import json
H=[[F(3),F(-2),F(-1)],[F(-1),F(3),F(-2)],[F(-2),F(-1),F(3)]]
HT=list(map(list,zip(*H)));u=[F(1),F(0),F(-1)]
def dot(x,y):return sum(a*b for a,b in zip(x,y))
def apply(a,x):return [dot(row,x) for row in a]
assert all(sum(row)==0 for row in H) and all(sum(row)==0 for row in HT)
x=[F(0),F(-2,7),F(-3,7)]
assert apply(H,x)==u
I=dot(u,x);Ra=F(3);p=F(1,3)+F(2,3)*F(2,3)
assert I==F(3,7) and p==F(7,9) and 1/(Ra*I)==p
alpha=F(3,14);y=z=[alpha*v for v in u]
r=[a-b for a,b in zip(u,apply(H,y))]
s=[a-b for a,b in zip(u,apply(HT,z))]
assert dot(r,r)==dot(s,s)==F(1,14)
gap=F(9,2) # Symmetric part is complete-graph Laplacian, edge weight3/2.
Ihat=dot(u,y)+dot(z,r);radius=F(1,14)/gap
assert Ihat==F(87,196) and radius==F(1,63)
assert Ihat-radius<=I<=Ihat+radius
old_lower=2*dot(u,y)-dot(y,apply(H,y))
assert old_lower==Ihat and old_lower>I
floor=gap*2/(4*Ra**2)
assert floor==F(1,4) and floor<=I
out={'scope':'exact nonreversible three-state control; no large/physical claim',
 'true_exit_law_probability':str(p),'true_I':str(I),'dual_center':str(Ihat),
 'dual_radius':str(radius),'coercive_denominator_floor':str(floor),
 'reversible_one_sided_shortcut':'FALSE: proposed lower exceeds truth',
 'normalizer_and_dual_residual':'PASS'}
Path(__file__).with_name('EXACT_CONTROL.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
