"""Symbolic continuation of the curved-boundary zero constraints.

This writes a family only after exact rational-function identities pass.
"""
from pathlib import Path
import sympy as S,json,time,signal
signal.alarm(210)
p=Path(__file__).parent
tau,t=S.symbols('tau t',real=True)
be=(1-3*tau*tau)/(1+3*tau*tau);rv=4-12*tau/(1+3*tau*tau)
mod=S.expand((1-3*tau*tau)**2*(1-t*t)**2-(1-4*tau+3*tau*tau)*(1+3*tau*tau)*(1+t*t)**2)
mod=S.Poly(mod,t).primitive()[1].as_expr()
domain=S.QQ.frac_field(tau)
def red(x):return S.rem(S.Poly(x,t,domain=domain),S.Poly(mod,t,domain=domain)).as_expr()
start=time.perf_counter()
a,b,c,d=S.symbols('a b c d',real=True);A=S.Matrix([a,b,c,d])
T=sum(x*x for x in A);q=a*d-b*c;X=a*a+c*c-b*b-d*d
F=T*T+4*(rv-1)*q*q+4*be*q*X
HR=S.hessian(F,A).subs({a:1,b:t,c:0,d:0})
print('modulus',S.factor(mod),flush=True)
B=1-3*tau*tau;den=1+3*tau*tau
K=S.Matrix([-B*(tau*(1-t*t)+den*t*t)*(1+t*t),
            B*t*(den-tau*(1-t*t))*(1+t*t),
            B*B*t*(1-t*t)-tau*den*t*(1+t*t)**2,
            B*B*t*t*(1-t*t)+tau*den*(1+t*t)**2]).applyfunc(red)
content=S.gcd_list([S.Poly(x,t,domain=domain).content() for x in K]);K=K.applyfunc(lambda x:S.cancel(x/content))
print('kernel acquired',time.perf_counter()-start,flush=True)
assert all(red(x)==0 for x in HR*K)
kappa=2*tau/(1-3*tau*tau)
mm=(1-4*tau+3*tau*tau)/(1+3*tau*tau)
sigma=4*mm/(1+mm)**2
KT=red(sum(x*x for x in K));KX=red(K[0]**2+K[2]**2-K[1]**2-K[3]**2)
KZ=red(2*(K[0]*K[3]-K[1]*K[2]))
assert red(KX-kappa*KZ)==0 and red(KZ*KZ-sigma*KT*KT)==0
raw=json.loads((p/'angular_family.json').read_text());v=[S.Symbol(n,real=True) for n in raw['variables']]
beta,r=S.symbols('beta r',real=True);loc={str(x):x for x in (a,b,c,d,beta,r,*v)}
C=S.Matrix([[S.sympify(x,locals=loc) for x in row] for row in raw['C']])
C=C.subs({beta:be,r:rv});h=S.Matrix([1,t,t*t,0,0,0])
fixed=json.loads((p/'near_endpoint/boundary_rational.json').read_text())
free_values={x:S.Rational(fixed[str(x)]) for x in v[3:]}
C=C.subs(free_values);v=v[:3]
modp=S.Poly(mod,t,domain=domain)
kp=[]
for x in K:
    xx=S.Poly(x,t,domain=domain);powers=[S.Poly(1,t,domain=domain)]
    for power in range(1,7):powers.append((powers[-1]*xx).rem(modp))
    kp.append(powers)
def evaluate_modular(ex):
    value=S.Poly(0,t,domain=domain)
    for powers,co in S.Poly(ex,*A).terms():
        term=S.Poly(co,t,domain=domain)
        for i,power in enumerate(powers):
            if power:term=(term*kp[i][power]).rem(modp)
        value=(value+term).rem(modp)
    return value
# Separate the ten linear pieces before substituting the algebraic kernel.
equations=[];vv=[None]+v;zero=dict.fromkeys(v,0)
pieces=[]
for parameter in vv:
    vec=(C*h).subs(zero) if parameter is None else (C*h).diff(parameter)
    rows=[]
    for ex in vec:
        val=evaluate_modular(ex)
        rows.append([S.factor(val.nth(i)) for i in range(4)])
    pieces.append(rows)
    (p/'generic_acoustic_pieces.json').write_text(json.dumps({'variables':list(map(str,v)),'pieces':[[[str(x) for x in rr] for rr in pp] for pp in pieces]}))
    print('piece',parameter,'seconds',time.perf_counter()-start,flush=True)
M=S.Matrix([[pieces[j+1][row][power] for j in range(len(v))] for row in range(6) for power in range(4)])
rhs=S.Matrix([-pieces[0][row][power] for row in range(6) for power in range(4)])
aug=M.row_join(rhs)
from sympy.polys.matrices import DomainMatrix
rr,pivots=DomainMatrix.from_Matrix(aug).convert_to(domain).rref()
rr=rr.to_Matrix()
rank=len(pivots);print('rank',rank,'seconds',time.perf_counter()-start,flush=True)
assert all(j<len(v) for j in pivots)
solution=list(v)
for row,pivot in enumerate(pivots):
    solution[pivot]=S.factor(rr[row,-1]-sum(rr[row,j]*v[j] for j in range(len(v)) if j not in pivots))
assert all(S.cancel(x)==0 for x in M*S.Matrix(solution)-rhs)
for variable,expr in zip(v,solution):
    assert S.cancel(expr.subs(tau,S.Rational(1,30))-S.Rational(fixed[str(variable)]))==0
out={'tau':str(tau),'modulus':str(mod),'rank':rank,'pivots':list(pivots),
     'variables':list(map(str,v)),'solution':list(map(str,solution)),
     'fixed_coefficients':{str(k):str(v) for k,v in free_values.items()},
     'checks':{'HR_K_zero':True,'Hopf_zero_equations':True,'all_24_constraints':True,'matches_literal_seed':True},
     'seconds':time.perf_counter()-start}
(p/'generic_acoustic_jets.json').write_text(json.dumps(out,indent=2)+'\n')
print('saved',out['seconds'],flush=True)
