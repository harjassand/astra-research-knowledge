import sympy as s,json
from pathlib import Path
z,t=s.symbols('z t',positive=True)
I=(z*s.log(z)-z+1)/(z-1)**2
assert s.limit(I,z,1)==s.Rational(1,2)
# Elementary integral can be checked by a direct antiderivative.
F=-(t/(z-1))+(z/(z-1)**2)*s.log(1+(z-1)*t)
assert s.simplify(s.diff(F,t)-(1-t)/(1+(z-1)*t))==0
assert s.simplify(F.subs(t,1)-F.subs(t,0)-I)==0
Im=s.simplify(I.subs(z,s.Rational(1,2)));IM=s.simplify(I.subs(z,2))
assert s.simplify(IM-Im/2-(3*s.log(2)-2))==0
assert s.simplify(Im/(4*IM)-(1-s.log(2))/(2*(2*s.log(2)-1)))==0
lo=2*sum(s.Rational(1,3)**(2*j+1)/s.Integer(2*j+1) for j in range(3))
assert lo==s.Rational(842,1215)
assert 3*lo-2==s.Rational(32,405)>0
out={'scope':'mEX<=X<=MEX, arbitrary finite reference and arbitrary marginal condition number, m>0','I':'(z logz-z+1)/(z-1)^2; I(1)=1/2','deficit_coefficient':'I(M)-I(m)/2','relative_entropy_coefficient':'I(m)/(4I(M))','half_two_band':{'deficit':'3log2-2>32/405','contraction':'(1-log2)/(2(2log2-1))<1/2'},'status':'PASS exact scalar receiver; noncommuting metric/source proof in theorem'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
