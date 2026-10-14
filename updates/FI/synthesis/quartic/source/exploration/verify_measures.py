import sympy as s,json
from pathlib import Path
a,b,c,d=s.symbols('a b c d');vs=(a,b,c,d);X=s.Matrix(vs);u=a*a+c*c;v=b*b+d*d;q=a*d-b*c
F=s.expand(3*(u+v-2*q)**2+s.Rational(35,24)*u*u+q*q-s.Rational(5,2)*q*u)
DF=s.Matrix([s.diff(F,z) for z in vs]);HF=s.hessian(F,vs);I=s.Matrix([1,0,0,1]);R=s.Matrix([0,1,0,0]);S=s.Matrix([1,0,0,s.Rational(3,2)])
w=s.Rational(1,10**6);m=s.Integer(9);t=s.Rational(9,2)*m*m*w/(1-s.Rational(3,2)*w);Rt=s.Matrix([0,1,t,0])
atoms=[Rt,-Rt,m*S,-2*m*S];weights=[(1-s.Rational(3,2)*w)/2]*2+[w,w/2]
def ev(P,V):return P.subs(dict(zip(vs,V)))
mean=sum((pr*V for pr,V in zip(weights,atoms)),s.zeros(4,1));detmean=sum(pr*ev(q,V) for pr,V in zip(weights,atoms))
C=sum((pr*V*V.T for pr,V in zip(weights,atoms)),s.zeros(4));H=sum((pr*ev(HF,V) for pr,V in zip(weights,atoms)),s.zeros(4));bv=sum((pr*ev(DF,V) for pr,V in zip(weights,atoms)),s.zeros(4,1));cv=sum(pr*ev(F,V) for pr,V in zip(weights,atoms))
h=(I.T*H*I)[0];bi=(bv.T*I)[0];bg=-bi/h;gap=s.factor(cv-bi**2/(2*h))
mins=[s.factor(H[:j,:j].det()) for j in range(1,5)]
assert mean==s.zeros(4,1) and detmean==0 and C.rank()==2
assert all(v>0 for v in mins) and gap<0
print('bounded law gap',gap,float(gap),'background coefficient',bg,flush=True)
print('h',h,'bI',bi,'c',cv,flush=True)
# Actual compatible concentrating construction, with F0=u^2+v^2.
x,y,r=s.symbols('x y r',positive=True);k=y*(1-y)
f1=2*x;f2=1-x
intervals=[(f1,0,s.Rational(1,3)),(f2,s.Rational(1,3),1)]
def integrate(P):
 out=0
 for ff,lo,hi in intervals:
  aa=s.diff(ff,x)*k;bb=ff*s.diff(k,y)
  pol=s.expand(P.subs({a:aa,b:bb,c:0,d:0}))
  out+=s.integrate(s.integrate(pol,(x,lo,hi)),(y,0,1))
 return s.factor(out)
F0=u*u+v*v;D0=s.Matrix([s.diff(F0,z) for z in vs]);H0=s.hessian(F0,vs)
hp=s.Matrix(4,4,lambda i,j:integrate(H0[i,j]));bp=s.Matrix([integrate(e) for e in D0]);cp=integrate(F0);m4p=integrate((u+v)**2)
assert hp==s.diag(s.Rational(4,5),s.Rational(16,27),s.Rational(4,15),s.Rational(16,81))
assert bp==s.Matrix([s.Rational(2,35),0,0,0]);assert cp==s.Rational(247,14175);assert m4p==s.Rational(41,2025)
hall=s.diag(0,6,0,2)+r*hp;ball=s.sqrt(r)*bp;loss=s.simplify((ball.T*hall.inv()*ball)[0]/2)
assert loss==s.Rational(1,490)
print('compatible pulse loss',loss,'fourth moment',s.Rational(1,2)+m4p,flush=True)
Path(__file__).with_name('measure_verification.json').write_text(json.dumps({'bounded_nongradient_law':{'weights':list(map(str,weights)),'atoms':[[str(z) for z in V] for V in atoms],'determinant_mean':str(detmean),'covariance_rank':C.rank(),'positive_H_minors':list(map(str,mins)),'directional_minimum_gap':str(gap),'directional_background_coefficient':str(bg)},'compatible_concentration':{'spike_H':list(map(str,hp)),'spike_b':list(map(str,bp)),'spike_F':str(cp),'spike_M4':str(m4p),'loss':str(loss)}},indent=2))
