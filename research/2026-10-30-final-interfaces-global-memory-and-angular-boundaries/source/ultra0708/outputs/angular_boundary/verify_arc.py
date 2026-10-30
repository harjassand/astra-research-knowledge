"""Direct exact symbolic check of the rational arc primitive. Requires SymPy.

Does not import acquisition code or use a numerical solver. Positivity at
the center is checked by the separate stdlib receive_boundary.py.
"""
from pathlib import Path
import sympy as S,json,time,signal
signal.alarm(180)
p=Path(__file__).parent;start=time.perf_counter()
data=json.loads((p/'arc_data.json').read_text());seed=json.loads((p/'seed_299_301.json').read_text())
tau,t=S.symbols('tau t',real=True);A=S.symbols('a b c d',real=True);a,b,c,d=A
def unpack(co):return sum(S.Integer(x)*tau**i for i,x in enumerate(co))
vi=[S.cancel(unpack(f['num'])/unpack(f['den'])) for f in data['functions']]
D=S.lcm_list([S.denom(x) for x in vi]);scaled=[S.cancel(x*D) for x in vi]
assert D.subs(tau,S.Rational(1,30))!=0 and all(S.denom(x)==1 for x in scaled)
P=[]
for rows in data['primitive_basis']:
    pp=0
    point={}
    for row in rows:
        powers=row['powers'];co=sum(S.Rational(n,dd)*scaled[i] for i,n,dd in row['weights'])
        pp+=co*S.prod(x**e for x,e in zip(A,powers))
        val=S.cancel(co.subs(tau,S.Rational(1,30))/D.subs(tau,S.Rational(1,30)))
        if val:point[tuple(powers)]=val
    actual={tuple(row[:4]):S.Rational(row[4],row[5]) for row in seed['P'][len(P)]}
    assert point==actual;P.append(S.expand(pp))
P=S.Matrix(P);J=S.Matrix([[0,0,-1,0],[0,0,0,-1],[1,0,0,0],[0,1,0,0]])
assert all(S.expand(x)==0 for x in P.jacobian(A)*J*S.Matrix(A)+J.T*P)
sgn=(1,-1,-1,1);swap=(1,0,3,2)
for i in range(4):
    assert S.expand(sgn[i]*P[i].subs(dict(zip(A,[sgn[j]*A[j] for j in range(4)])),simultaneous=True)+P[i])==0
    assert S.expand(P[swap[i]].subs(dict(zip(A,[A[j] for j in swap])),simultaneous=True)+P[i])==0
B=1-3*tau*tau;den=1+3*tau*tau;beta=B/den;r=4-12*tau/den
T=sum(x*x for x in A);q=a*d-b*c;X=a*a+c*c-b*b-d*d
F=T*T+4*(r-1)*q*q+4*beta*q*X
H=(den*S.hessian(F,A)).applyfunc(S.expand)
W=S.zeros(4)
for i in range(4):
    for j in range(i+1,4):
        W[i,j]=S.expand(T*(S.diff(P[j],A[i])-S.diff(P[i],A[j]))-2*(A[i]*P[j]-A[j]*P[i]))
        W[j,i]=-W[i,j]
mod=S.Poly(S.expand(B*B*(1-t*t)**2-(1-4*tau+3*tau*tau)*den*(1+t*t)**2),t).primitive()[1].as_expr()
domain=S.QQ.frac_field(tau);mp=S.Poly(mod,t,domain=domain)
K=[-B*(tau*(1-t*t)+den*t*t)*(1+t*t),
   B*t*(den-tau*(1-t*t))*(1+t*t),
   B*B*t*(1-t*t)-tau*den*t*(1+t*t)**2,
   B*B*t*t*(1-t*t)+tau*den*(1+t*t)**2]
K=[S.Poly(x,t,domain=domain).rem(mp) for x in K]
kp=[]
for x in K:
    powers=[S.Poly(1,t,domain=domain)]
    for e in range(1,7):powers.append((powers[-1]*x).rem(mp))
    kp.append(powers)
def evaluate(ex):
    ans=S.Poly(0,t,domain=domain)
    for powers,co in S.Poly(ex,*A).terms():
        val=S.Poly(co,t,domain=domain)
        for i,e in enumerate(powers):
            if e:val=(val*kp[i][e]).rem(mp)
        ans=(ans+val).rem(mp)
    return ans
def rem(ex):return S.Poly(ex,t,domain=domain).rem(mp)
HR=H.subs({a:1,b:t,c:0,d:0})
for i in range(4):assert rem(sum(HR[i,j]*K[j].as_expr() for j in range(4))).is_zero
KT=evaluate(T);KX=evaluate(X);KZ=evaluate(2*q)
kappa=2*tau/B;mm=(1-4*tau+3*tau*tau)/den;sigma=4*mm/(1+mm)**2
assert rem(KX.as_expr()-kappa*KZ.as_expr()).is_zero
assert rem(KZ.as_expr()**2-sigma*KT.as_expr()**2).is_zero
print('primitive, symmetries, acoustic geometry checked',time.perf_counter()-start,flush=True)
Hv=[evaluate(H[i,0]+t*H[i,1]) for i in range(4)]
Wv=[evaluate(W[i,0]+t*W[i,1]) for i in range(4)]
zero=S.Poly(0,t,domain=domain);Ch=[zero for _ in range(6)];p1=(0,1,3,4);p2=(1,2,4,5)
DD=S.Poly(D,t,domain=domain);de=S.Poly(den,t,domain=domain);tt=S.Poly(t,t,domain=domain)
for i in range(4):
    hh=(DD*KT*KT*Hv[i]).rem(mp);ww=(de*Wv[i]).rem(mp).mul_ground(S.Rational(1,2))
    Ch[p1[i]]=(Ch[p1[i]]+hh+tt*ww).rem(mp)
    Ch[p2[i]]=(Ch[p2[i]]+tt*hh-ww).rem(mp)
assert all(x.is_zero for x in Ch)
# Rebuild the full continuing density directly from the primitive, and
# check the supplied continuing lift as polynomial identities.
continued=json.loads((p/'continuing_matrices.json').read_text())
zp=S.Poly(0,b,d,domain=domain);Tc=S.Poly((1+b*b+d*d)**2,b,d,domain=domain)
HC=[[S.Poly(H[i,j].subs({a:1,c:0}),b,d,domain=domain).mul_ground(domain.from_sympy(1/den)) for j in range(4)] for i in range(4)]
WC=[[S.Poly(W[i,j].subs({a:1,c:0}),b,d,domain=domain).mul_ground(domain.from_sympy(1/D)) for j in range(4)] for i in range(4)]
CA=[[zp for _ in range(6)] for _ in range(6)]
for pp in (p1,p2):
    for i in range(4):
        for j in range(4):CA[pp[i]][pp[j]]+=Tc*HC[i][j]
for i in range(4):
    for j in range(4):
        term=WC[i][j].mul_ground(S.Rational(1,2));CA[p1[i]][p2[j]]+=term;CA[p2[j]][p1[i]]+=term
def unpack_matrix(raw):
    return [[S.Poly(sum(S.sympify(co,locals={'tau':tau})*b**ib*d**id_ for ib,id_,co in ent),b,d,domain=domain) for ent in row] for row in raw]
CG=unpack_matrix(continued['C']);MG=unpack_matrix(continued['M'])
assert CA==CG
assert CG==[list(row) for row in zip(*CG)] and MG==[list(row) for row in zip(*MG)]
for key,matrix in (('C',CG),('M',MG)):
    for i,row in enumerate(matrix):
        for j,poly in enumerate(row):
            actual=S.Poly(sum(S.Rational(n,dd)*b**ib*d**id_ for ib,id_,n,dd in seed['matrices'][key]['entries'][i][j]),b,d)
            assert S.Poly(poly.as_expr().subs(tau,S.Rational(1,30)),b,d)==actual
KG=[S.Poly(S.sympify(x,locals={'tau':tau,'b':b,'d':d}),b,d,domain=domain) for x in continued['kernel']]
assert KG[0]==S.Poly(1,b,d,domain=domain)
wp=S.Poly(b*b+d*d+2*kappa*d-1,b,d,domain=domain)
gp=S.Poly(S.Integer(7059192361)*(d*d-sigma*(1-kappa*d)**2),b,d,domain=domain)
cp00=sum((KG[i]*CA[i][j]*KG[j] for i in range(6) for j in range(6)),zp)
assert cp00==wp*wp*MG[0][0]+wp*gp*MG[0][1].mul_ground(2)+gp*gp*MG[1][1]
for j in range(1,6):
    assert sum((KG[i]*CA[i][j] for i in range(6)),zp)==wp*MG[0][j+1]+gp*MG[1][j+1]
    for i in range(1,6):assert CA[i][j]==MG[i+1][j+1]
print('full continuing density and lift checked',time.perf_counter()-start,flush=True)
# The zero ideal is nonsingular at the certified center.
k0=kappa.subs(tau,S.Rational(1,30));s0=sigma.subs(tau,S.Rational(1,30))
gg=d*d-s0*(1-k0*d)**2;ee=1-d*d-2*k0*d
assert S.discriminant(gg,d)!=0 and S.resultant(gg,ee,d)!=0
assert S.discriminant(mp.as_expr().subs(tau,S.Rational(1,30)),t)!=0
# Invertibility of the lower block in the entire four-dimensional zero
# algebra pays continuation of the polynomial kernel, including conjugates.
ww=b*b+d*d+2*k0*d-1
def zero_reduce(ex):
    rr=S.rem(S.expand(ex),ww,b)
    return S.expand(sum(S.rem(co,gg,d)*b**pw[0] for pw,co in S.Poly(rr,b).terms()))
basis=(S.Integer(1),b,d,b*d)
literalC=seed['matrices']['C']['entries'];operator=S.zeros(20)
for i in range(1,6):
    for j in range(1,6):
        entry=sum(S.Rational(n,dd)*b**ib*d**id_ for ib,id_,n,dd in literalC[i][j])
        for col,x in enumerate(basis):
            pp=S.Poly(zero_reduce(entry*x),b,d)
            for row,y in enumerate(basis):operator[4*(i-1)+row,4*(j-1)+col]=pp.coeff_monomial(y)
from sympy.polys.matrices import DomainMatrix
assert DomainMatrix.from_Matrix(operator).det()!=0
print(json.dumps({'literal_seed_match':True,'generic_symmetries':True,
  'generic_closed_acoustic_zero_constraints':True,'generic_acoustic_geometry':True,
  'full_continuing_density_and_lift':True,
  'continuing_lift_matches_literal_center':True,
  'simple_zero_ideal_at_center':True,'lower_block_invertible_in_zero_algebra':True,'seconds':time.perf_counter()-start,
  'scope':'Exact rational-function identities and full continuing lift. The explicit interval is checked separately by quantify_arc.py.'},indent=2))
