import sympy as s, json
from pathlib import Path
B=s.Rational(3);A=B+s.Rational(35,24);C=6*B+1;E=-4*B-1;L=-4*B-s.Rational(5,2);M=-4*B
M11=s.Matrix([[12*A,0,0,3*L],[0,2*C+2*E,-L,0],[0,-L,4*A,0],[3*L,0,0,2*C]])
M12=s.Matrix([[0,2*C+2*E,-L,0],[2*C+2*E,0,0,M],[-L,0,0,E],[0,M,E,0]])
M22=s.Matrix([[2*C+2*E,0,0,M],[0,12*B,-3*M,0],[0,-3*M,2*C,0],[M,0,0,4*B]])
t=s.Rational(11);ks=[t,t+s.Rational(25,6),0,0,t,t+s.Rational(8,3)]
K=s.zeros(4);n=0
for i in range(4):
 for j in range(i+1,4): K[i,j]=ks[n];K[j,i]=-ks[n];n+=1
Q=M11.row_join(M12+K).col_join((M12-K).row_join(M22))
null=Q.nullspace();print('rank',Q.rank(),'null',null,flush=True)
_,piv=Q.rref();T=Q.extract(piv,piv);mins=[s.factor(T[:j,:j].det()) for j in range(1,len(piv)+1)]
print('piv',piv,'minors',mins,flush=True)
assert all(m>0 for m in mins)
for v in null: assert Q*v==s.zeros(8,1)
a,b,c,d=s.symbols('a b c d');xx=s.Matrix([a,b,c,d]);u=a*a+c*c;v=b*b+d*d;w=a*b+c*d;q=a*d-b*c
F=s.expand(A*u*u+B*v*v+C*u*v+E*w*w+L*q*u+M*q*v)
alt=3*((b+c)**2+(d-a)**2)**2+s.Rational(35,24)*u*u+q*q-s.Rational(5,2)*q*u
assert s.expand(F-alt)==0
HH=s.hessian(F,xx);I=s.Matrix([1,0,0,1]);R=s.Matrix([0,1,0,0]);H_I=HH.subs({a:1,b:0,c:0,d:1});Q_I=(xx.T*H_I*xx)[0]
assert s.expand(Q_I-(s.Rational(1,2)*(3*a-2*d)**2+s.Rational(5,6)*c*c-q))==0
print('F(I)',F.subs({a:1,b:0,c:0,d:1}),'H_R null',HH.subs({a:0,b:1,c:0,d:0}).nullspace(),flush=True)
assert HH.subs({a:0,b:1,c:0,d:0})*I==s.zeros(4,1)
tau=s.symbols('tau');Ci=sum(s.diff(F,xx[j])*I[j] for j in range(4));print('cubic along kernel',s.factor(Ci.subs({c:0,d:s.Rational(3,2)*a})),flush=True)
assert s.expand(Ci.subs({c:0,d:s.Rational(3,2)*a})+s.Rational(5,12)*a**3)==0
out={'F_coeffs':list(map(str,[A,B,C,E,0,0,L,M,0])),'K':list(map(str,K)),'Q':list(map(str,Q)),'nullspace':[[str(z) for z in v] for v in null],'principal_indices':list(piv),'principal_minors':list(map(str,mins)),'F_at_I':'-1/24'}
Path(__file__).with_name('tangent_certificate.json').write_text(json.dumps(out,indent=2))
