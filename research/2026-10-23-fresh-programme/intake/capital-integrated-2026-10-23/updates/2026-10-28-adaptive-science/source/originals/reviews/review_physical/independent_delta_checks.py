"""Warm delta checks; imports no producer code and reruns no old check suite."""
from fractions import Fraction as Q
from itertools import permutations
from pathlib import Path
import json
import mpmath as mp

mp.mp.dps=90
HERE=Path(__file__).resolve().parent
rows=[]

def mm(x):
    return mp.mpf(x.numerator)/x.denominator if isinstance(x,Q) else mp.mpf(x)

def g(w):return (w/mp.sinh(w))**2 if w else mp.mpf(1)

def objective(e):
    return mp.quad(g,[0,e[0]])+sum(mp.quad(g,[e[i],e[i+1]]) for i in range(1,len(e),2))

def endpoints(t,A,B):
    s2=(t+A+mp.sqrt((t+A)**2-4*B*t))/2
    return [mp.sqrt(B*t/s2),mp.sqrt(t),mp.sqrt(s2)]

def star(mass,springs):
    m=list(map(mm,mass));k=list(map(mm,springs));n=len(m)
    L=mp.matrix(n)
    for j,z in enumerate(k,1):
        L[0,0]+=z;L[j,j]+=z;L[0,j]-=z;L[j,0]-=z
    D=mp.matrix([[L[i,j]/mp.sqrt(m[i]*m[j]) for j in range(n)]for i in range(n)])
    P=D.copy();P[0,0]+=4
    al=list(mp.eigsy(D,eigvals_only=True));be=list(mp.eigsy(P,eigvals_only=True))
    assert abs(al[0])<mp.mpf('1e-70')
    e=[mp.sqrt(be[0])]
    for i in range(1,n):e.extend([mp.sqrt(al[i]),mp.sqrt(be[i])])
    C=sum(mj*mj/kj for mj,kj in zip(m[1:],k))
    assert abs(sum(m)-2)<mp.mpf('1e-70')
    assert abs(sum(be)-sum(al)-4)<mp.mpf('1e-65')
    assert abs(sum(x*x for x in be)-sum(x*x for x in al)-(16+8*sum(k)))<mp.mpf('1e-60')
    return e,C

def fit(e):
    # Four coefficients of the cubic in squared frequency; last is constant.
    mat=mp.matrix([[w*w,w**4,w**6,1]for w in e[:4]])
    la,a,b,nu=mp.lu_solve(mat,mp.matrix([-w**3*g(w)for w in e[:4]]))
    w=e[-1]
    return w**3*g(w)+la*w*w+a*w**4+b*w**6+nu,(nu,la,a,b)

pend=endpoints(mp.mpf(40),mp.mpf(4),mp.mpf(2))
jpend=objective(pend)
la,mu,eta=mp.lu_solve(mp.matrix([[w*w,2*w**4,-1]for w in pend]),
                         mp.matrix([-w**3*g(w)for w in pend]))
R10=g(mp.mpf(10))+la/10+2*mu*10-eta/1000
G=Q(1,75)
gamma=mm(2*1000*G*G/(1-4*G))
assert R10<0 and mu<0 and eta>0

def small_split(eps):
    v=mp.mpf(100);C=mp.mpf(1)/20
    k=(1-eps)**2/(C-eps/v)
    tr=v+eps*v+k*(1+1/(1-eps))
    pair=2*v*k/(1-eps)
    disc=mp.sqrt(tr*tr-4*pair)
    a1=(tr-disc)/2;a2=(tr+disc)/2
    poly=lambda x:x**3-(tr+4)*x*x+(pair+4*(v+k/(1-eps)))*x-4*v*k/(1-eps)
    beta=[mp.findroot(poly,start)for start in [mp.mpf('1.9'),mp.mpf('42.1'),mp.mpf(100)]]
    e=[mp.sqrt(beta[0]),mp.sqrt(a1),mp.sqrt(beta[1]),mp.sqrt(a2),mp.sqrt(beta[2])]
    return objective(e),eps*v+k

dJ=mp.diff(lambda z:small_split(z)[0],mp.mpf(0))
dK=mp.diff(lambda z:small_split(z)[1],mp.mpf(0))
assert abs(dJ-gamma*R10)<mp.mpf('1e-65') and abs(dK-64)<mp.mpf('1e-65')
eps=Q(1,10000);H=eps*100;k=(1-eps)**2/(Q(1,20)-eps/100)
assert eps*eps/H+(1-eps)**2/k==Q(1,20)
e,c=star([1,eps,1-eps],[H,k]);jsplit=objective(e)
assert jpend>jsplit and abs(c-mp.mpf(1)/20)<mp.mpf('1e-70')
rows.append({'case':'R44 exact small split','cost_exact':str(H+k),'C_exact':'1/20',
             'gamma':mp.nstr(gamma,55),'dJ_direct':mp.nstr(dJ,55),
             'dJ_gamma_R10':mp.nstr(gamma*R10,55),'dkappa':mp.nstr(dK,55),
             'J_finite':mp.nstr(jsplit,55),'gain':mp.nstr(jpend-jsplit,55)})

# New extended family: independently reconstruct the two extreme new budgets.
def capped_star(h,cap):
    C=mp.mpf(1)/20;b=1-h
    H=(C*cap-1+2*h+mp.sqrt((1-2*h-C*cap)**2-4*C*cap*h*h))/(2*C)
    e,c=star([1,h,b],[H,cap-H])
    res,coef=fit(e)
    return res,e,H,c,coef

for cap,start in [('20.01',('.00025','.00027')),('100',('.16','.17'))]:
    kap=mp.mpf(cap)
    h=mp.findroot(lambda z:capped_star(z,kap)[0],tuple(map(mp.mpf,start)))
    res,e,H,c,coef=capped_star(h,kap)
    assert abs(res)<mp.mpf('1e-65') and coef[0]<0<coef[3]
    assert abs(c-mp.mpf(1)/20)<mp.mpf('1e-65')
    rows.append({'case':'R44 extended budget '+cap,'h':mp.nstr(h,60),
                 'H':mp.nstr(H,60),'J':mp.nstr(objective(e),60),
                 'largest_frequency':mp.nstr(e[-1],30)})

def joint(de,h):
    A=4-de;B=2*h/(h+de)
    den=B*(mp.mpf(21)/40-1/B+de/(h*(h+de)))
    t=(A-B)/den
    c=(B*t+(t+A)*(h+de)-t*h)/4
    kap=t+h-c
    # Independent simplified resource identity, useful for derivative audit.
    simplified=((A-B)**2/den+de*(h-4+de))/4
    assert abs(kap-simplified)<mp.mpf('1e-65')
    e=endpoints(t,A,B)+[mp.sqrt(h),mp.sqrt(h+de)]
    return e,kap,t,c,B

de,h=mp.findroot(lambda d,z:(joint(d,z)[1]-mp.mpf('20.02'),fit(joint(d,z)[0])[0]),
                 (mp.mpf('.00577'),mp.mpf('73.34')))
e,kap,t,c,B=joint(de,h);res,coef=fit(e)
d=B*t*(h+de)/4
sg1=(c-mp.sqrt(c*c-4*d))/2;sg2=(c+mp.sqrt(c*c-4*d))/2
k1=(h*t-d-kap*sg1)/(sg2-sg1);k2=kap-k1
m1=k1/sg1;m2=k2/sg2
assert min(k1,k2,m1,m2)>0
ee,C=star([1,m1,m2],[k1,k2])
assert max(abs(x-y)for x,y in zip(e,ee))<mp.mpf('1e-65')
assert abs(C-mp.mpf(1)/20)<mp.mpf('1e-65')
assert abs(kap-mp.mpf('20.02'))<mp.mpf('1e-65')
kd=mp.diff(lambda z:joint(z,h)[1],de)
kh=mp.diff(lambda z:joint(de,z)[1],h)
assert kd>0 and kh>0 and coef[0]<0<coef[3]
jopt=objective(ee)
assert mp.mpf('1.142045199292380356594718')<jopt<mp.mpf('1.142045199292393889573449')
rows.append({'case':'R79 nested joint optimum','delta':mp.nstr(de,70),'H':mp.nstr(h,70),
             'kappa_delta':mp.nstr(kd,55),'kappa_H':mp.nstr(kh,55),
             'masses':[mp.nstr(z,55)for z in [1,m1,m2]],
             'springs':[mp.nstr(z,55)for z in [k1,k2]],'J':mp.nstr(jopt,70),
             'gain':mp.nstr(jpend-jopt,65),'dual_nu_lambda_a_b':[mp.nstr(z,55)for z in coef]})

# Independently derive the exact rational cell's characteristic polynomials
# by a generic determinant, rather than using the producer's specialized co.
def padd(a,b):
    z=[Q(0)]*max(len(a),len(b))
    for i,v in enumerate(a):z[i]+=v
    for i,v in enumerate(b):z[i]+=v
    return z
def pmul(a,b):
    z=[Q(0)]*(len(a)+len(b)-1)
    for i,v in enumerate(a):
        for j,w in enumerate(b):z[i+j]+=v*w
    return z
def char(A):
    z=[Q(0)]
    for p in permutations(range(3)):
        s=sum(p[i]>p[j]for i in range(3)for j in range(i+1,3))
        term=[Q((-1)**s)]
        for i in range(3):term=pmul(term,[-A[i][p[i]],Q(int(i==p[i]))])
        z=padd(z,term)
    return z
m2=Q('0.000513557966');m1=1-m2;k1=Q('19.98226783251');k2=Q('0.03763216749')
mass=[Q(1),m1,m2]
L=[[k1+k2,-k1,-k2],[-k1,k1,Q(0)],[-k2,Q(0),k2]]
D=[[L[i][j]/mass[i]for j in range(3)]for i in range(3)]
P=[z[:]for z in D];P[0][0]+=4
cp0,cpp=char(D),char(P)
tr0=k1+k2+k1/m1+k2/m2;pair0=2*k1*k2/(m1*m2)
assert cp0==[0,pair0,-tr0,1]
assert cpp==[-4*k1*k2/(m1*m2),pair0+4*(k1/m1+k2/m2),-(tr0+4),1]
C=m1*m1/k1+m2*m2/k2;kap=k1+k2
assert C<Q(1,20) and kap<Q('20.02')
e,c=star(mass,[k1,k2]);jr=objective(e)
assert jopt<jr<jpend
rows.append({'case':'R79 exact rational parts','C_exact':str(C),'C_margin_exact':str(Q(1,20)-C),
             'kappa_exact':str(kap),'kappa_margin_exact':str(Q('20.02')-kap),
             'alpha_characteristic_ascending':list(map(str,cp0)),
             'beta_characteristic_ascending':list(map(str,cpp)),
             'J':mp.nstr(jr,65),'gain':mp.nstr(jpend-jr,60),
             'gap_above_optimum':mp.nstr(jr-jopt,60)})

(HERE/'independent_delta_checks.json').write_text(json.dumps(rows,indent=2)+'\n')
print('PASS: new small-split derivatives and finite cell; extreme extended family points;')
print('      independent nested optimum, positive matrix realization, and rational margins/polynomials.')
for r in rows:print(r['case'],r.get('J',r.get('gain','')))
