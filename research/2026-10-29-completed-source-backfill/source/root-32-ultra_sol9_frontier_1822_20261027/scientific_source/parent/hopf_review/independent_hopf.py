"""Root literal SymPy/Fraction audit; no producer code/maps or stored cuts."""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import hashlib,json,time
import sympy as s
START=time.perf_counter();OUT=Path(__file__).resolve().parent
a,b,c,d,t=s.symbols('a b c d t',real=True);vars=(a,b,c,d)
u=a*a+c*c;v=b*b+d*d;q=a*d-b*c
F=s.expand((u+v)**2+s.Rational(252,25)*q*q+s.Rational(99,25)*q*(u-v))
H=s.hessian(F,vars)
co,si,x,y,z,zz=s.symbols('C S x y z w',real=True)
base={a:x*co-y*si,b:x*si+y*co,c:z*co-zz*si,d:z*si+zz*co}
X=s.Matrix([co,si,0,0])
actual=s.expand((X.T*H*X)[0].subs(base,simultaneous=True)/2)
expected=6*x*x+2*y*y+2*z*z+s.Rational(302,25)*zz*zz+s.Rational(99,25)*(3*(co*co-si*si)*x*zz-(co*co-si*si)*y*z-4*co*si*y*zz)
rem=s.rem(s.Poly(actual-expected,co),s.Poly(co*co+si*si-1,co)).as_expr()
assert s.expand(rem)==0
beta=s.Rational(99,100);r=s.Rational(88,25);h=s.symbols('h',real=True)
N11=1-beta**2*h;N22=2*r-1-3*beta**2*h
detN=s.expand(N11*N22-4*beta**2*(1-h))
vertex=s.solve(s.diff(detN,h),h)[0];minimum=s.factor(detN.subs(h,vertex))
assert 0<vertex<1 and minimum==s.Rational(7,2500)
assert s.factor(N11.subs(h,1))==s.Rational(199,10000)>0
assert s.expand(N11+N22-(s.Rational(176,25)-4*beta**2*h))==0
# trace N<=176/25 and min eig(N)>=det(N)/trace(N)>=7/17600.
# Completing x,z squares has T=D^-1 B, ||T||<=beta<1.
# |v|²+|w|²<=2|v+Tw|²+3|w|², giving coefficient>=7/26400.
acoustic_coefficient_margin=Q(7,26400)
roc_box=acoustic_coefficient_margin/420

def rat(x):return Q(int(s.numer(x)),int(s.denom(x)))
poly={e:rat(cc) for e,cc in s.Poly(F,*vars).terms()}
def monomial(A,e):
    p=Q(1)
    for aa,ee in zip(A,e):p*=aa**ee
    return p
def value(A):return sum(cc*monomial(A,e) for e,cc in poly.items())
def determinant(A):return A[0]*A[3]-A[1]*A[2]
A=tuple(map(Q,(36,0,0,35)))
increments=[(Q(-264,28745),Q(-63481,114980),Q(5771,143725),Q(528,28745)),
            (Q(0),Q(11,20),Q(-1,25),Q(0)),
            (Q(12,5),Q(0),Q(0),Q(-24,5))]
weights=[Q(5749,11542),Q(1,2),Q(11,5771)]
atoms=[tuple(aa+xx for aa,xx in zip(A,inc)) for inc in increments]
assert all(w>0 for w in weights) and sum(weights)==1
assert all(sum(w*inc[j] for w,inc in zip(weights,increments))==0 for j in range(4))
assert sum(w*determinant(inc) for w,inc in zip(weights,increments))==0
assert sum(w*determinant(atom) for w,atom in zip(weights,atoms))==determinant(A)
J=sum(w*value(atom) for w,atom in zip(weights,atoms))-value(A)
assert J==Q(-13534664264487807,296890944920312500)<0
sensitivity={}
for aa in range(5):
    for bb in range(5-aa):
        for cc in range(5-aa-bb):
            e=(aa,bb,cc,4-aa-bb-cc)
            sensitivity[e]=sum(w*monomial(atom,e) for w,atom in zip(weights,atoms))-monomial(A,e)
assert len(sensitivity)==35
W=sum(abs(c) for c in sensitivity.values())
nonpc_box=-J/(2*W);full_box=min(roc_box,nonpc_box)
assert J+full_box*W<0 and acoustic_coefficient_margin-210*full_box>0
def enc(x):
    if isinstance(x,(Q,s.Rational)):return str(x)
    if isinstance(x,dict):return {str(k):enc(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [enc(v) for v in x]
    return x
result={'status':'INDEPENDENT_LITERAL_AND_RATIONAL_PASS','claim':'Strict ROC and actual non-PC on a full35 box; no QC classification',
        'literal_acoustic_rotation_identity':True,'determinant_N':str(detN),
        'vertex':vertex,'minimum_det_N':minimum,'N11_lower':s.Rational(199,10000),
        'acoustic_t2_margin':acoustic_coefficient_margin,'weights':weights,'atoms':atoms,
        'jensen_defect':J,'monomial_sensitivities':sensitivity,'sensitivity_l1':W,
        'ROC_full35_radius':roc_box,'nonPC_full35_radius':nonpc_box,
        'joint_full35_radius':full_box,'runtime_seconds':time.perf_counter()-START}
(OUT/'INDEPENDENT_HOPF.json').write_text(json.dumps(enc(result),indent=2)+'\n')
print('J',float(J),'sensitivity',float(W),'ROC box',roc_box,'nonPC box',float(nonpc_box),'joint',float(full_box))
print('runtime',result['runtime_seconds'])
