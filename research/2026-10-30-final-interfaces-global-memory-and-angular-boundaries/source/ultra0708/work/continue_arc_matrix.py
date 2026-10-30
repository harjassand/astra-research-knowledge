"""Construct the actual continuing polynomial lift, using acoustic geometry."""
from pathlib import Path
import sympy as S,json,time,signal
signal.alarm(180)
start=time.perf_counter();here=Path(__file__).parent;out=here.parent/'outputs/angular_boundary'
tau,b,d=S.symbols('tau b d',real=True);field=S.QQ.frac_field(tau)
cv=field.from_sympy;ex=field.to_sympy;zero=field.zero;one=field.one
B=1-3*tau*tau;den=1+3*tau*tau;beta=B/den;r=4-12*tau/den
kappa=2*tau/B;mu=(1-4*tau+3*tau*tau)/den;sigma=4*mu/(1+mu)**2
ka,mm,ss=map(cv,(kappa,mu,sigma));D0=ss/(1-ss*ka*ka);D1=-2*ss*ka/(1-ss*ka*ka)
def bmul(x,y):
    a,c=x;bb,dd=y
    return (a*bb+c*dd*D0,a*dd+c*bb+c*dd*D1)
def plus(x,y):return tuple(a+bb for a,bb in zip(x,y))
def neg(x):return tuple(-a for a in x)
def scal(x,c):return tuple(a*c for a in x)
def times(x,y):
    E,F=(x[0],x[2]),(x[1],x[3]);G,H=(y[0],y[2]),(y[1],y[3])
    a=bmul(E,G);bb=bmul(bmul(F,H),(1-D0,-D1-2*ka))
    cc=bmul(E,H);dd=bmul(F,G)
    return (a[0]+bb[0],cc[0]+dd[0],a[1]+bb[1],cc[1]+dd[1])
def inve(x):
    assert x[1]==0 and x[3]==0
    a,c=x[0],x[2];det=a*(a+c*D1)-c*c*D0
    assert det!=0
    return ((a+c*D1)/det,zero,-c/det,zero)
unit=(one,zero,zero,zero);bv=(zero,one,zero,zero);dv=(zero,zero,one,zero)
e=times(bv,bv)
lamminus=plus(scal(plus(unit,scal(dv,-ka)),2*mm/(1+mm)),neg(unit))
rho=times(lamminus,times(bv,inve(e)));rho2=times(rho,rho)
vaux=scal(times(rho,inve(plus(unit,rho2))),cv(B/tau))
eta1=plus(times(vaux,plus(bv,neg(rho))),dv)
eta2=plus(plus(times(vaux,dv),neg(bv)),rho)
eta=times(eta2,inve(eta1))
kv=[unit,rho,rho2,eta,times(eta,rho),times(eta,rho2)]
def to_poly(x):return S.Poly(ex(x[0])+ex(x[1])*b+ex(x[2])*d+ex(x[3])*b*d,b,d,domain=field)
K=list(map(to_poly,kv));print('geometric kernel',time.perf_counter()-start,flush=True)
seed=json.loads((out/'seed_299_301.json').read_text())
for kk,rows in zip(K,seed['kernel']):
    actual=S.Poly(sum(S.Rational(n,dd)*b**ib*d**id_ for ib,id_,n,dd in rows),b,d)
    at=S.Poly(kk.as_expr().subs(tau,S.Rational(1,30)),b,d)
    assert actual==at
arc=json.loads((out/'arc_data.json').read_text());raw=json.loads((here/'angular_family.json').read_text())
vi=[]
for f in arc['functions']:
    nn=sum(S.Integer(x)*tau**i for i,x in enumerate(f['num']));dd=sum(S.Integer(x)*tau**i for i,x in enumerate(f['den']))
    vi.append(S.cancel(nn/dd))
a,c,be,rr=S.symbols('a c beta r',real=True);vv=[S.Symbol(n,real=True) for n in raw['variables']]
loc={str(x):x for x in (a,b,c,d,be,rr,*vv)};sub={a:1,c:0,be:beta,rr:r,**dict(zip(vv,vi))}
C=[[S.Poly(S.sympify(x,locals=loc).subs(sub),b,d,domain=field) for x in row] for row in raw['C']]
wp=S.Poly(b*b+d*d+2*kappa*d-1,b,d,domain=field)
gp=S.Poly(S.Integer(7059192361)*(d*d-sigma*(1-kappa*d)**2),b,d,domain=field)
zz=S.Poly(0,b,d,domain=field)
cp00=sum((K[i]*C[i][j]*K[j] for i in range(6) for j in range(6)),zz)
first=[sum((K[i]*C[i][j] for i in range(6)),zz) for j in range(1,6)]
print('continuing density',time.perf_counter()-start,flush=True)
q1,rem0=cp00.div(wp);q2,rem1=q1.div(wp)
cc,rem=rem0.div(gp*gp);assert rem.is_zero
bb,rem=rem1.div(gp);assert rem.is_zero
M=[[zz for _ in range(7)] for _ in range(7)];M[0][0]=q2;M[0][1]=M[1][0]=bb.mul_ground(S.Rational(1,2));M[1][1]=cc
for j,f in enumerate(first,1):
    pp,rr=f.div(wp);qq,rem=rr.div(gp);assert rem.is_zero
    M[0][j+1]=M[j+1][0]=pp;M[1][j+1]=M[j+1][1]=qq
for i in range(1,6):
    for j in range(1,6):M[i+1][j+1]=C[i][j]
def packed(mat):
    rows=[]
    for row in mat:
        rr=[]
        for poly in row:
            rr.append([[ib,id_,str(co)] for (ib,id_),co in poly.terms()])
        rows.append(rr)
    return rows
for i in range(7):
    for j in range(7):
        expected=S.Poly(sum(S.Rational(n,dd)*b**ib*d**id_ for ib,id_,n,dd in seed['matrices']['M']['entries'][i][j]),b,d)
        assert S.Poly(M[i][j].as_expr().subs(tau,S.Rational(1,30)),b,d)==expected
result={'C':packed(C),'M':packed(M),'kernel':[str(x.as_expr()) for x in K],
        'seconds':time.perf_counter()-start,'scope':'Actual continuing rational polynomial lift; exact center match and all division identities checked.'}
(here/'continuing_matrices.json').write_text(json.dumps(result))
print('continuing lift checked',result['seconds'],flush=True)
