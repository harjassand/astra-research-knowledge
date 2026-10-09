import json,itertools
from fractions import Fraction as F
c=json.load(open('work/hidden_equilibrium/certificate.txt'))
v=[[F(t) for t in row] for row in c['points']];fa=[[F(t) for t in row] for row in c['facets']]
dot=lambda x,y:sum(a*b for a,b in zip(x,y))
sub=lambda x,y:[a-b for a,b in zip(x,y)]
verts=[]
for i,p in enumerate(v):
    constraints=fa+[[F(0)]+sub(p,q) for q in v if q!=p]
    vs=[]
    for a,b in itertools.combinations(constraints,2):
        det=a[1]*b[2]-a[2]*b[1]
        if not det:continue
        y=[(-a[0]*b[2]+a[2]*b[0])/det,(-a[1]*b[0]+a[0]*b[1])/det]
        if not all(l[0]+dot(l[1:],y)>=0 for l in constraints):continue
        if y in vs:continue
        vs.append(y)
    for y in vs:
        delta=1-dot(y,y);d2=dot(sub(y,p),sub(y,p))
        if delta==0:
            assert d2==0;continue
        verts.append({'i':i,'y':list(map(str,y)),'ratio':float(d2)**.5/float(delta),'ratio2':str(d2/delta**2)})
print('max',max(verts,key=lambda r:r['ratio']))
print(sorted([r['ratio'] for r in verts]))
# Rational C=16/5?
C=F(16,5)
print('C=16/5 exact',all(F(r['ratio2'])<=C*C for r in verts))
json.dump({'constant':str(C),'verified':all(F(r['ratio2'])<=C*C for r in verts),'vertices':verts},open('work/discrete_critic/GEOMETRY_CHECK.json','w'),indent=2)
