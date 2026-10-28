"""Root independent univariate symbolic curvature check for three cuts."""
from pathlib import Path
import sympy as s,json
OUT=Path(__file__).resolve().parent;SRC=OUT.parents[1]/'explicit_convex_interface'
raw=json.loads((SRC/'EXACT_PROFILE_OBSTRUCTION.json').read_text());t=s.symbols('t');rows=[]
for row in raw['rows']:
    a,b,c,d,ss=[s.Rational(x)+t*s.Rational(v) for x,v in zip(row['point'],row['direction'])]
    u=a*a+c*c;v=b*b+d*d;w=a*b+c*d;q=a*d-b*c;T=u+v;x=u-v;y=2*w;z=2*q;gap=ss-q
    F=s.Rational(55220381,10**10)*(u*u+v*v)+s.Rational(114430029,625000000)*u*v-s.Rational(801761987,5000000000)*w*w+s.Rational(118849817,4000000000)*q*(u-v)
    p=s.Rational(6222019,200000000)*x**3+s.Rational(1686519911,10**10)*x*x*z+s.Rational(81172813,2000000000)*x*z*z+s.Rational(1726116771,10**10)*z**3+s.Rational(128626163,5000000000)*x*y*y+s.Rational(373321239,2000000000)*y*y*z
    den=s.Poly(T*T+gap*gap,t);D0,D1,D2=[den.nth(i) for i in range(3)];assert D0>0;values=[]
    for num in [F*T*T+p*gap,T*T*gap*gap,gap*gap*(ss*ss+T*T)]:
        nn=s.Poly(num,t);N0,N1,N2=[nn.nth(i) for i in range(3)]
        values.append(s.factor(2*N2/D0-2*N1*D1/D0**2+2*N0*D1**2/D0**3-2*N0*D2/D0**2))
    assert values==list(map(s.Rational,row['curvatures']));rows.append(values)
weights=list(map(s.Rational,raw['positive_weights']));assert all(w>0 for w in weights) and sum(weights)==1
weighted=[s.factor(sum(weights[i]*rows[i][j] for i in range(3))) for j in range(3)]
assert weighted==list(map(s.Rational,raw['weighted_curvature_coefficients']))
assert weighted[1:]==[0,0] and weighted[0]<-s.Rational(3,20)
result={'status':'ROOT_INDEPENDENT_THREE_CUT_PROFILE_PASS','weighted_constant':str(weighted[0]),'parameters_cancelled_exactly':True,
        'scope':'Only the displayed rational profile; no general smooth-lift exclusion.'}
(OUT/'PROFILE_REPLAY.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'])
