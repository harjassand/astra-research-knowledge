"""Exact family algebra and a rational compatible Fourier diagnostic.

This verifies the listed identities and the specified map. It does not verify
the universal conformal inequality, a numerical optimizer, or historical novelty.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib, json, math
import sympy as sp

ROOT=Path(__file__).resolve().parent
checks=[]
def check(name, value):
    assert bool(value), name
    checks.append(name)

def add(x,y):return (x[0]+y[0],x[1]+y[1])
def sub(x,y):return (x[0]-y[0],x[1]-y[1])
def mul(x,y):return (x[0]*y[0]-x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def sc(k,x):return (k*x[0],k*x[1])
def plus(A,B):
    C=dict(A)
    for k,x in B.items():C[k]=add(C.get(k,(0,0)),x)
    return {k:x for k,x in C.items() if x!=(0,0)}
def minus(A,B):return plus(A,{k:sc(-1,x) for k,x in B.items()})
def scale(k,A):return {f:sc(k,x) for f,x in A.items() if sc(k,x)!=(0,0)}
def conv(A,B):
    C={}
    for (i,j),x in A.items():
        for (k,l),y in B.items():
            f=(i+k,j+l);C[f]=add(C.get(f,(0,0)),mul(x,y))
    return {k:x for k,x in C.items() if x!=(0,0)}
def avgprod(A,B):
    z=(0,0)
    for (i,j),x in A.items():z=add(z,mul(x,B.get((-i,-j),(0,0))))
    assert z[1]==0
    return z[0]
def energy(fields,L):
    a,b,c,d=fields
    u=plus(conv(a,a),conv(c,c));v=plus(conv(b,b),conv(d,d))
    j=minus(conv(a,d),conv(b,c))
    Hbase=plus(conv(minus(a,d),minus(a,d)),conv(plus(b,c),plus(b,c)))
    return F(avgprod(Hbase,Hbase),8*L**4)+F(avgprod(j,j)+avgprod(u,j),L**4)

a,b,c,d,s,m,n=sp.symbols('a b c d s m n',real=True)
u=a*a+c*c;v=b*b+d*d;S=u+v;delta=u-v;j=a*d-b*c
J=((a-d)**2+(b+c)**2)**2/8+j*j+u*j
C=2*j*(2*a+d)+u*(a+d)
Q=(2*a+d)**2+c*c
check('J1 invariant expansion',sp.expand(J-S*S/8-sp.Rational(3,2)*j*j-delta*j/2)==0)
check('J1 coercivity identity',sp.expand(J-S*S/12-u*v/6-sp.Rational(3,2)*(j+delta/6)**2)==0)
check('conformal cubic derivative',sp.expand(C-sp.diff(J,a)-sp.diff(J,d))==0)
shift=J.subs({a:a+s,d:d+s}, simultaneous=True)
check('pointwise conformal expansion with determinant correction',sp.expand(shift-2*s**4-5*s**3*a-3*s**3*d-J-s*C-s*s*(Q+3*j))==0)

M=sp.Matrix([[m*m+7*n*n,-6*m*n,2*m*n,m*m-3*n*n],[-6*m*n,7*m*m+n*n,-3*m*m+n*n,2*m*n],[2*m*n,-3*m*m+n*n,3*m*m+n*n,2*m*n],[m*m-3*n*n,2*m*n,2*m*n,m*m+3*n*n]])/4
z=sp.symbols('z',real=True)
acoustic=sp.diff(J.subs({c:c+z*m,d:d+z*n},simultaneous=True),z,2).subs(z,0)/2
check('independent rank-one acoustic matrix',sp.expand(acoustic-(sp.Matrix([a,b,c,d]).T*M*sp.Matrix([a,b,c,d]))[0])==0)
C0=M[:2,:2];D0=M[:2,2:];E0=M[2:,2:]
Sch=(E0-D0.T*C0.inv()*D0).applyfunc(sp.factor)
den=7*(m*m+n*n)**2
Sch_expected=sp.Matrix([[3*m*m*(m**4+3*m*m*n*n+4*n**4),6*m*n*(m**4+m*m*n*n+n**4)],[6*m*n*(m**4+m*m*n*n+n**4),3*n*n*(4*m**4+3*m*m*n*n+n**4)]])/den
check('acoustic positive top block determinant',sp.factor(C0.det()-7*(m*m+n*n)**2/16)==0)
check('acoustic Schur matrix',all(sp.factor(x)==0 for x in Sch-Sch_expected))
check('acoustic Schur determinant',sp.factor(Sch.det()-9*m**4*n**4/(7*(m*m+n*n)**2))==0)

aa,bb,cc=sp.symbols('aa bb cc',positive=True)
check('convex quartic fourth-order Bregman identity',sp.expand(cc+bb+3*bb**2/(8*cc)-cc/3-3*(bb+4*cc/3)**2/(8*cc))==0)
kappa=3*j+delta/2
sigma=sp.Matrix([(S/2+j)*c-kappa*b,(S/2-j)*d+kappa*a])
check('row stress formula',all(sp.expand(x)==0 for x in sigma-sp.Matrix([sp.diff(J,c),sp.diff(J,d)])))

x,y=sp.symbols('x y',real=True)
reference=J.subs({a:1+x,b:y,c:0,d:1},simultaneous=True)-2-5*x
check('reference scalar energy',sp.expand(reference-4*x*x-x**3-(x*x+y*y)**2/8)==0)
check('reference positive margin',sp.expand(reference-x*x-(x*x+y*y)**2/24-x*x*(x+6)**2/12-(2*x*x*y*y+y**4)/12)==0)
stress_ref=sigma.subs({a:1+x,b:y,c:0,d:1},simultaneous=True)
stress_expected=sp.Matrix([-y*(3+4*x+x*x/2-y*y/2),3+7*x+5*x*x+x**3/2-x*y*y/2])
check('reference stress polynomial',all(sp.expand(q)==0 for q in stress_ref-stress_expected))
bad=J.subs({a:1+x,b:0,c:0,d:1-2*x},simultaneous=True)-3*(1+x)*(1-2*x)
check('cofactor stress trial deficit polynomial',sp.expand(bad+1-2*x+x**3-sp.Rational(97,8)*x**4)==0)
eps=F(1,32);m2=F(5,8);m3=F(3,8);m4=F(99,128)
dual_deficit=m3*eps**3-F(97,8)*m4*eps**4
check('compatible first-row cofactor stress deficit',dual_deficit==F(2685,2**30))
reference_gap=4*m2*eps**2+m3*eps**3+m4*eps**4/8
check('same first-row exact minimum positive',reference_gap==F(2633827,2**30))

denominator=1000
frozen_path=ROOT/'EXACT_FOURIER_DIAGNOSTIC.json'
if frozen_path.exists():
    # Replay the frozen rational potential without trusting the optimizer.
    potential_modes=json.loads(frozen_path.read_text())['potential_modes']
else:
    raw=json.loads((ROOT/'FOURIER_DIAGNOSTIC_m6.json').read_text())['results'][0]
    pot={}
    for label,coef in zip(raw['labels'],raw['coefficients']):
        out,k,l,phase=label
        key=(out,k,l)
        pot.setdefault(key,[0,0])[0 if phase=='sin' else 1]=int(round(coef/math.hypot(k,l)*denominator))
    potential_modes=[{'component':out+1,'kx':k,'ky':l,'sin_numerator':si,'cos_numerator':co,'denominator':denominator} for (out,k,l),(si,co) in sorted(pot.items()) if si or co]
fields=[{} for _ in range(4)]
seen=set()
for rec in potential_modes:
    out=rec['component']-1;k=rec['kx'];l=rec['ky'];si=rec['sin_numerator'];co=rec['cos_numerator']
    assert rec['denominator']==denominator and out in [0,1] and (k>0 or k==0 and l>0)
    assert all(type(v) is int for v in [k,l,si,co]) and (out,k,l) not in seen
    seen.add((out,k,l))
    for row,freq in [(2*out,k),(2*out+1,l)]:
        val=(freq*si,freq*co)
        if val!=(0,0):
            fields[row][(k,l)]=val;fields[row][(-k,-l)]=(val[0],-val[1])
L=2*denominator
fa,fb,fc,fd=fields
check('rounded Fourier mean gradient exactly zero',all(A.get((0,0),(0,0))==(0,0) for A in fields))
all_freq=set().union(*[set(A) for A in fields])
check('rounded Fourier exact differential compatibility',all(sc(k[1],fa.get(k,(0,0)))==sc(k[0],fb.get(k,(0,0))) and sc(k[1],fc.get(k,(0,0)))==sc(k[0],fd.get(k,(0,0))) for k in all_freq))
fu=plus(conv(fa,fa),conv(fc,fc));fv=plus(conv(fb,fb),conv(fd,fd));fj=minus(conv(fa,fd),conv(fb,fc))
fS=plus(fu,fv);fdelta=minus(fu,fv);fq=plus(scale(2,fa),fd);ft=plus(fa,fd)
check('rounded Fourier determinant mean exactly zero',fj.get((0,0),(0,0))==(0,0))
A4=energy(fields,L)
A4_second=F(avgprod(fS,fS),8*L**4)+F(3*avgprod(fj,fj)+avgprod(fdelta,fj),2*L**4)
check('rounded Fourier two independent J formula evaluations',A4==A4_second)
C3=F(2*avgprod(fj,fq)+avgprod(fu,ft),L**3)
C3_expanded=F(avgprod(conv(fa,fa),fa)+5*avgprod(conv(fa,fa),fd)-4*avgprod(conv(fa,fb),fc)+avgprod(conv(fc,fc),fa)+2*avgprod(conv(fd,fd),fa)-2*avgprod(conv(fb,fc),fd)+avgprod(conv(fc,fc),fd),L**3)
check('rounded Fourier two independent cubic evaluations',C3==C3_expanded)
Q2=F(avgprod(fq,fq)+avgprod(fc,fc),L**2)
ratio=C3*C3/(4*A4*Q2)
check('rounded Fourier stronger two-thirds estimate fails',ratio>F(2,3))
check('rounded Fourier actual target not violated',ratio<1)
sopt=-C3/(2*Q2);Emin=A4-C3*C3/(4*Q2)
bigL=L*sopt.denominator
shifted=[scale(sopt.denominator,A) for A in fields]
for index in [0,3]:shifted[index]=plus(shifted[index],{(0,0):(sopt.numerator*L,0)})
direct_energy=energy(shifted,bigL)-2*sopt**4
check('rounded Fourier actual optimized-background energy exactly replayed',Emin==direct_energy and Emin>0)
witness={'status':'compatible rational Fourier counterexample only to the stronger C3^2 <= (8/3) A4 Q2; NOT a counterexample to C3^2 <= 4 A4 Q2','domain':'(R / 2 pi Z)^2, normalized average','potential_definition':'phi^component = sum (sin_numerator sin(kx*x+ky*y)+cos_numerator cos(kx*x+ky*y))/denominator','potential_modes':potential_modes,'A4':str(A4),'C3':str(C3),'Q2':str(Q2),'ratio_C2_over_4AQ':str(ratio),'ratio_decimal':float(ratio),'stronger_inequality_gap_C2_minus_8AQ_over_3':str(C3*C3-F(8,3)*A4*Q2),'optimized_scalar_background':str(sopt),'optimized_Jensen_energy':str(Emin),'optimized_Jensen_energy_decimal':float(Emin),'gradient_mean':['0','0','0','0'],'determinant_mean':'0','verification':'exact Gaussian-integer Fourier convolution; no numerical quadrature or PSD tolerances'}
(ROOT/'EXACT_FOURIER_DIAGNOSTIC.json').write_text(json.dumps(witness,indent=2)+'\n')
receipt={'status':'PASS','checks':checks,'number_of_checks':len(checks),'scope':'exact algebraic identities, independent ROC matrix algebra, and the specified compatible Fourier map; NOT the universal conformal estimate','exact_diagnostic_sha256':hashlib.sha256((ROOT/'EXACT_FOURIER_DIAGNOSTIC.json').read_bytes()).hexdigest(),'rounded_ratio_decimal':float(ratio),'actual_optimized_energy_decimal':float(Emin),'cofactor_stress_dual_deficit':str(dual_deficit),'same_first_row_actual_minimum_minus_2':str(reference_gap)}
(ROOT/'VERIFICATION_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
