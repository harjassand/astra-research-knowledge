from pathlib import Path
import sympy as s,json,time
base=Path('work/cycle6/c02_s01/axial');d=s.symbols('delta',real=True);t=s.symbols('t')
start=time.perf_counter();cases=[]
for N in range(2,13):
 m=N//2;odd=N%2
 if not odd:
  polys=[s.chebyshevt(j,1+2*t) for j in range(m+1)]
  values=[s.Rational(s.binomial(N,m),s.binomial(N,m+j))*s.exp(-d*j*j/N) for j in range(m+1)]
 else:
  polys=[s.Integer(1)]
  if m:polys.append(1+4*t)
  for j in range(1,m):polys.append(s.expand(2*(1+2*t)*polys[j]-polys[j-1]))
  values=[s.Rational(s.binomial(N,m+1),s.binomial(N,m+1+j))*s.exp(-d*j*(j+1)/N) for j in range(m+1)]
 moments=[s.Integer(1)]
 for j in range(1,m+1):
  P=s.Poly(polys[j],t)
  moments.append(s.simplify((values[j]-sum(P.nth(a)*moments[a] for a in range(j)))/P.nth(j)))
 for j in range(1,m+1):
  expr=s.diff(moments[j],d)+(j*(j+odd)*moments[j]+j*(j-s.Rational(1,2))*moments[j-1])/N
  assert s.simplify(expr)==0
  a=s.rf(s.Rational(1,2),j)*s.factorial(m-j)/s.factorial(m)
  assert s.simplify(moments[j].subs(d,0)-a)==0
 cases.append({'N':N,'degree':m,'beta_prime_initial_moments':'EXACT','triangular_ODE':'EXACT'})
weights=[s.Rational(16,81),s.Rational(2,3),s.Integer(1),s.Rational(2,3),s.Rational(16,81)]
Z=sum(weights)
coherent=s.Rational(216,221);endpoint=s.Rational(5,442)
for k in range(5):
 mixture=coherent*s.binomial(4,k)/16+(endpoint if k in (0,4) else 0)
 assert mixture==weights[k]/Z
x={'status':'PASS','scope':'Finite symbolic controls for complete written cosh/moment/ODE reduction; no all-N separability proof',
   'cases':cases,'N4_endpoint_mixture':{'coherent_p_half':'216/221','each_endpoint':'5/442','status':'EXACT'},
   'elapsed_seconds':time.perf_counter()-start}
(base/'COSH_TRANSFORM_CHECKS.json').write_text(json.dumps(x,indent=2)+'\n')
print(json.dumps(x,indent=2))
