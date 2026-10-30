"""Exact conservative radius from coefficient Lipschitz and eigenvalue bounds."""
from pathlib import Path
from fractions import Fraction as R
from math import comb,lcm
import sympy as S,json,time,signal
signal.alarm(180)
start=time.perf_counter();here=Path(__file__).parent;out=here.parent/'outputs/angular_boundary'
tau=S.Symbol('tau',real=True);center=S.Rational(1,30);radius=R(1,1000)
data=json.loads((here/'continuing_matrices.json').read_text());seed=json.loads((out/'seed_299_301.json').read_text())
cache={}
def fraction(x):return R(int(x.p),int(x.q))
def bound(expression):
    if expression in cache:return cache[expression]
    expr=S.cancel(S.sympify(expression,locals={'tau':tau}))
    nn,dd=S.fraction(expr);pp=S.Poly(nn,tau,domain=S.QQ).shift(center);qq=S.Poly(dd,tau,domain=S.QQ).shift(center)
    n=max(pp.degree(),qq.degree(),0)
    pco=[fraction(pp.nth(i)) for i in range(n+1)];qco=[fraction(qq.nth(i)) for i in range(n+1)]
    p0,q0=pco[0],qco[0];assert q0
    qs=sum((abs(qco[j])*radius**(j-1) for j in range(1,n+1)),R(0))
    hden=min(radius,abs(q0)/(2*qs)) if qs else radius
    # (p(z)q0-p0 q(z))/z, bounded on the reference interval.
    rr=sum((abs(pco[j]*q0-p0*qco[j])*radius**(j-1) for j in range(1,n+1)),R(0))
    lip=2*rr/(q0*q0)
    cache[expression]=(hden,lip)
    return hden,lip
hden=radius;max_sum=R(0)
arc=json.loads((out/'arc_data.json').read_text())
for ff in arc['functions']:
    nn=sum(S.Integer(x)*tau**i for i,x in enumerate(ff['num']));dd=sum(S.Integer(x)*tau**i for i,x in enumerate(ff['den']))
    hh,_=bound(str(nn/dd));hden=min(hden,hh)
b,d=S.symbols('b d',real=True)
for kk in data['kernel']:
    for co in S.Poly(S.sympify(kk,locals={'tau':tau,'b':b,'d':d}),b,d).coeffs():
        hh,_=bound(str(co));hden=min(hden,hh)
for key in ('C','M'):
    for row in data[key]:
        for entry in row:
            total=R(0)
            for _,_,co in entry:
                hh,lip=bound(co);hden=min(hden,hh);total+=lip
            max_sum=max(max_sum,total)
    print('coefficient bounds',key,'unique',len(cache),'seconds',time.perf_counter()-start,flush=True)
# Tensor degree (6,6) Bernstein transform amplification on these rectangles
# is <=3^6: b ranges in [0,1], d in [-1,1], and |left_d|+width_d<=3.
Lmax=729*max_sum

def unpack_matrix(raw):return [[{(ib,id_):R(n,dd) for ib,id_,n,dd in ent if n} for ent in row] for row in raw]
CM=unpack_matrix(seed['matrices']['C']['entries']);MM=unpack_matrix(seed['matrices']['M']['entries'])
def matrices(mat,box):
    n=len(mat);lb,ub,ld,ud=box;power={}
    for i in range(n):
        for j in range(i,n):
            pp={}
            for (ib,id_),co in mat[i][j].items():
                for a in range(ib+1):
                    for b in range(id_+1):
                        ee=a,b
                        pp[ee]=pp.get(ee,R(0))+co*comb(ib,a)*lb**(ib-a)*(ub-lb)**a*comb(id_,b)*ld**(id_-b)*(ud-ld)**b
            power[i,j]=pp
    for u in range(7):
        for v in range(7):
            aa=[[R(0) for _ in range(n)] for _ in range(n)]
            for (i,j),pp in power.items():
                aa[i][j]=aa[j][i]=sum((co*R(comb(u,a),comb(6,a))*R(comb(v,b),comb(6,b)) for (a,b),co in pp.items() if a<=u and b<=v),R(0))
            yield aa
def eigen_lower(mat):
    n=len(mat);den=lcm(*(x.denominator for row in mat for x in row));a=[[int(x*den) for x in row] for row in mat];prev=1
    for k in range(n):
        pivot=a[k][k];assert pivot>0
        for i in range(k+1,n):
            for j in range(i,n):
                val=a[i][j]*pivot-a[i][k]*a[k][j];assert val%prev==0
                a[i][j]=a[j][i]=val//prev
        prev=pivot
    det=R(pivot,den**n);trace=sum(mat[i][i] for i in range(n));assert trace>0
    return det/trace**(n-1)
lam=None;count=0
for aa in matrices(MM,tuple(map(R,seed['cover']['local_box']))):
    ll=eigen_lower(aa);lam=ll if lam is None else min(lam,ll);count+=1
for leaf in seed['cover']['leaves']:
    if leaf['proof']=='M':continue
    for aa in matrices(CM,tuple(map(R,leaf['box']))):
        lam=min(lam,eigen_lower(aa));count+=1
assert count==6321 and lam>0
print('center eigenvalue bounds',count,'seconds',time.perf_counter()-start,flush=True)
beta=(1-3*tau*tau)/(1+3*tau*tau);rr=4-12*tau/(1+3*tau*tau);z=S.Symbol('z')
def F(a,b,c,d):
    T=a*a+b*b+c*c+d*d;q=a*d-b*c;X=a*a+c*c-b*b-d*d
    return T*T+4*(rr-1)*q*q+4*beta*q*X
bounds=[]
for A in ((0,55,-4,0),(1,0,0,-2)):
    pp=S.Poly(S.expand(F(A[0]+36*z,A[1],A[2],A[3]+35*z)),z)
    c0,c1,c2=[pp.nth(i) for i in range(3)]
    bounds.append(S.cancel((c2-c1*c1/(4*c0))/(A[0]*A[3]-A[1]*A[2])))
gap=S.cancel(bounds[1]-bounds[0]);gap0=fraction(gap.subs(tau,center));assert gap0>0
hh,Lgap=bound(str(gap))
limit=min(radius,hden,hh,lam/(14*Lmax),gap0/(2*Lgap))
exponent=0
while R(1,2**exponent)>limit:exponent+=1
delta=R(1,2**exponent)
assert 7*Lmax*delta<=lam/2 and Lgap*delta<=gap0/2 and delta<=hden and delta<=hh
result={'center':'1/30','delta_power_of_two':exponent,'delta':str(delta),
        'reference_radius':str(radius),'coefficient_matrices':count,
        'eigenvalue_lower_bound':str(lam),'bernstein_coefficient_Lipschitz_bound':str(Lmax),
        'coefficient_denominator_radius':str(hden),'gap_denominator_radius':str(hh),
        'nonpc_gap_at_center':str(gap0),'nonpc_gap_Lipschitz_bound':str(Lgap),
        'seconds':time.perf_counter()-start,
        'scope':'Exact sufficient radius for this fixed rational primitive and cover; deliberately conservative, not an optimal interval or a whole-boundary theorem.'}
(out/'arc_radius_certificate.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('eigenvalue_lower_bound','bernstein_coefficient_Lipschitz_bound','coefficient_denominator_radius','gap_denominator_radius','nonpc_gap_Lipschitz_bound')},indent=2),flush=True)
