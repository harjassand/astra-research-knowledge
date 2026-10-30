"""A rational four-atom minor-matching measure with a negative Jensen gap.

This makes the failed all-base minor-support extension explicit. It is
not a gradient Young measure: the accepted quasiconvex seed forbids its
negative gap. No such compatibility is silently assumed.
"""
from pathlib import Path
import json
import sympy as s

OUT=Path(__file__).resolve().parent
CASE=OUT.parents[2]/'cases'/'angular'
data=json.loads((CASE/'seed_299_301.json').read_text())
beta=s.Rational(data['beta']);r=s.Rational(data['r'])
cut=data['nonpc'];A=s.Matrix(list(map(s.Rational,cut['A'])))
directions=[s.Matrix(list(map(s.Rational,cut[key]))) for key in ('Rplus','Rminus')]
def det(V):return V[0]*V[3]-V[1]*V[2]
def energy(V):
    a,b,c,d=V;T=sum(z*z for z in V);q=det(V);X=a*a+c*c-b*b-d*d
    return T*T+4*(r-1)*q*q+4*beta*q*X
u=s.symbols('u')
parameters=[]
for R in directions:
    poly=s.Poly(s.expand(energy(R+u*A)),u)
    c0,c1,c2=[poly.nth(j) for j in range(3)]
    B=c2-c1*c1/(4*c0)
    parameters.append((R,c0,c1,B,det(R)))
upper=parameters[0][3]/parameters[0][4]
lower=parameters[1][3]/parameters[1][4]
gamma=lower-upper;assert gamma>0
for exponent in range(1,100):
    delta=s.Rational(1,2**exponent);pairs=[]
    for R,c0,c1,B,dr in parameters:
        total=-c1/(2*c0)
        if total>=0:pos,neg=total+delta,-delta
        else:pos,neg=delta,total-delta
        variance=-pos*neg
        wp=-neg/(pos-neg);wn=pos/(pos-neg)
        assert pos>0 and neg<0 and wp>0 and wn>0
        assert wp+wn==1 and wp*pos+wn*neg==0
        pairs.append((pos,neg,variance,wp,wn))
    correction=sum(parameters[i][1]*pairs[i][2]/abs(parameters[i][4]) for i in range(2))
    if correction<gamma/2:break
else:raise AssertionError('No rational variance scale found')
vp,vm=pairs[0][2],pairs[1][2];dp,dm=parameters[0][4],parameters[1][4]
theta=-vm*dm/(vp*dp-vm*dm);assert 0<theta<1
atoms=[]
for mixture,(R,c0,c1,B,dr),(pos,neg,var,wp,wn) in zip((theta,1-theta),parameters,pairs):
    for tt,weight in ((pos,wp),(neg,wn)):
        atoms.append((mixture*weight,A+tt*R))
assert sum(w for w,V in atoms)==1
assert sum((w*V for w,V in atoms),s.zeros(4,1))==A
assert sum(w*det(V) for w,V in atoms)==det(A)
gap=s.factor(sum(w*energy(V) for w,V in atoms)-energy(A))
assert gap<0
ka=s.Rational(20,299)
X=A[0]**2+A[2]**2-A[1]**2-A[3]**2
assert X-ka*2*det(A)!=0
record={'base_A':list(map(str,A)),
    'atom_weights':[str(w) for w,V in atoms],
    'atom_matrices':[list(map(str,V)) for w,V in atoms],
    'mean_equals_A_exact':True,'determinant_moment_equals_det_A_exact':True,
    'Jensen_gap_exact':str(gap),'Jensen_gap_decimal':float(gap),
    'rational_small_step':str(delta),'opposite_support_gap':str(gamma),
    'base_outside_acoustic_planes':True,
    'not_a_gradient_Young_measure':'Its negative Jensen gap violates the accepted quasiconvexity of F.',
    'scientific_role':'Exact obstruction to extending the new singular-mean estimate to all means using only first moments and determinant moments.'}
(OUT/'moment_obstruction.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({'atoms':4,'step':str(delta),'mean_exact':True,'det_moment_exact':True,
                  'negative_Jensen_gap':str(gap),'gap_decimal':float(gap)},indent=2))
