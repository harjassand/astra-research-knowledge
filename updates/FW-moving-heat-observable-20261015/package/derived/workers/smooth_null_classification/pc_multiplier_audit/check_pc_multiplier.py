#!/usr/bin/env python3
"""Independent exact audit of determinant-support multiplier obstruction.

No imports from, execution of, or mutations to author/repository proof files.
"""
from pathlib import Path
from itertools import combinations_with_replacement
import hashlib
import json
import sympy as s

OUT = Path(__file__).resolve().parent
a,b,c,d,t,k,alpha,beta = s.symbols('a b c d t k alpha beta')
x=s.Matrix([a,b,c,d])
u=a*a+c*c
v=b*b+d*d
w=a*b+c*d
q=a*d-b*c
r=u-v
F=s.expand(u*u+v*v+s.Rational(166,3)*u*v-s.Rational(460,9)*w*w-s.Rational(52,9)*q*r)
DF=s.Matrix([s.diff(F,xx) for xx in x])
HF=s.hessian(F,x)
J=s.hessian(q,x)

def at(expr,vec):
    return expr.subs(dict(zip(x,vec)), simultaneous=True)

def rem(expr):
    return s.rem(s.expand(expr), P, k)

def zero(expr):
    assert s.expand(expr)==0

# Homogeneity, invariances, and exact quartic line expansion.
zero(at(F,t*x)-t**4*F)
zero(-c*s.diff(F,a)-d*s.diff(F,b)+a*s.diff(F,c)+b*s.diff(F,d))
swap=s.Matrix([b,a,d,c])
zero(at(F,swap)-F)
zero(at(q,swap)+q)
vv=s.Matrix(s.symbols('v0:4'))
line=s.Poly(s.expand(at(F,x+t*vv)-F-t*DF.dot(vv)),t)
zero(line.nth(2)-(vv.T*HF*vv)[0]/2)
zero(line.nth(3)-at(DF,vv).dot(x))
zero(line.nth(4)-at(F,vv))

# A general homogeneous quadratic rotation-invariant, swap-antisymmetric
# multiplier is exactly alpha*q+beta*(u-v).
mons=[x[i]*x[j] for i,j in combinations_with_replacement(range(4),2)]
coeff=s.symbols('l0:10')
lam=sum(cc*mm for cc,mm in zip(coeff,mons))
rot=-c*s.diff(lam,a)-d*s.diff(lam,b)+a*s.diff(lam,c)+b*s.diff(lam,d)
eq=s.Poly(rot,*x).coeffs()+s.Poly(s.expand(at(lam,swap)+lam),*x).coeffs()
CM,_=s.linear_eq_to_matrix(eq,coeff)
assert CM.rank()==8
assert len(CM.nullspace())==2
L=alpha*q+beta*r
zero(-c*s.diff(L,a)-d*s.diff(L,b)+a*s.diff(L,c)+b*s.diff(L,d))
zero(at(L,swap)+L)

# Contact identities, with no use of approximate roots.
P=17*k**4-314*k*k+17
AA=s.Matrix([203-17*k*k,k*(85*k*k-1551),2*k*(944-51*k*k),134])
RR=s.Matrix([1,k,0,0])
qA=rem(at(q,AA))
rA=rem(at(r,AA))
assert qA==185744-11024*k*k
zero(rA-s.Rational(6,13)*qA)
assert s.gcd(P,qA)==1
assert s.Poly(P,k).count_roots(-s.oo,s.oo)==4
cofR=at(s.Matrix([s.diff(q,xx) for xx in x]),RR)
assert cofR==s.Matrix([0,0,-k,1])
contact_hessian=at(HF,AA)*RR
assert all(rem(z)==0 for z in contact_hessian-s.Rational(3968,39)*qA*cofR)
assert rem((RR.T*at(HF,AA)*RR)[0])==0
zero(at(q,RR))

# The PSD support Hessian must annihilate RR, forcing this relation.
alpha_value=s.Rational(3968,39)-s.Rational(6,13)*beta
Lb=s.expand(L.subs(alpha,alpha_value))
assert all(rem(z)==0 for z in contact_hessian-at(Lb,AA)*cofR)

# Independently reconstruct both exact scalar discriminant cuts.
data=[]
for kind,A0,V0 in [
    ('upper',s.Matrix([-6,-3,-1,6]),s.Matrix([1,-2,0,1])),
    ('lower',s.Matrix([2,0,0,1]),s.Matrix([3,0,0,-2])),
]:
    FV=at(F,V0)
    hess=(V0.T*at(HF,A0)*V0)[0]
    cubic=at(DF,V0).dot(A0)
    cut=s.expand(2*FV*hess-cubic*cubic-4*at(Lb,A0)*FV*at(q,V0))
    C0=cut.subs(beta,0)
    Cb=-s.diff(cut,beta)
    assert s.Poly(cut,beta).degree()==1
    bound=s.factor(C0/Cb)
    assert FV>0
    if kind=='upper':
        assert C0==-s.Rational(1142144,27)
        assert Cb==s.Rational(14560,3)
        assert bound==-s.Rational(35692,4095)
    else:
        assert C0==s.Rational(957266072,1053)
        assert Cb==-s.Rational(1465992,13)
        assert bound==-s.Rational(119658259,14843169)
    data.append({'kind':kind,'A':list(A0),'V':list(V0),'F_V':FV,'hessian':hess,
                 'cubic':cubic,'C0':C0,'Cb':Cb,'bound':bound,'cut':cut})

upper,lower=data
gap=s.factor(lower['bound']-upper['bound'])
assert gap>0
ratio=s.factor(-lower['Cb']/upper['Cb'])
wu,wl=s.fraction(ratio)
assert wu>0 and wl>0
combined=s.factor(wu*upper['cut']+wl*lower['cut'])
assert beta not in combined.free_symbols and combined<0

# The Hessian support tests on determinant +/-1 directions give a global
# quadratic-size bound on every possible multiplier, independent of selection
# regularity. Record their exact quadratic bounding polynomials.
I=s.Matrix([1,0,0,1])
reflection=s.Matrix([1,0,0,-1])
assert at(q,I)==1 and at(q,reflection)==-1
lower_bound=s.expand(-(reflection.T*HF*reflection)[0]/2)
upper_bound=s.expand((I.T*HF*I)[0]/2)
assert s.Poly(lower_bound,*x).total_degree()==2
assert s.Poly(upper_bound,*x).total_degree()==2

# Ordinary PC's graph has full convex hull in lifted space.
hh=s.Matrix(s.symbols('h0:4'))
zero((at(q,x+hh)+at(q,x-hh))/2-q-at(q,hh))

def strings(z):
    if isinstance(z,dict):return {key:strings(val) for key,val in z.items()}
    if isinstance(z,list):return [strings(val) for val in z]
    return str(z) if isinstance(z,s.Basic) else z

result=strings({
    'status':'INDEPENDENT_EXACT_AUDIT_PASS',
    'F':F,
    'averaged_quadratic_multiplier_dimension':2,
    'contact_polynomial':P,
    'contact_determinant':qA,
    'contact_relation':'alpha+6 beta/13=3968/39',
    'cuts':data,
    'strict_bound_gap':gap,
    'positive_combination_weights':[wu,wl],
    'negative_combination_value':combined,
    'unrestricted_multiplier_quadratic_lower_bound':lower_bound,
    'unrestricted_multiplier_quadratic_upper_bound':upper_bound,
    'exclusions':['Second-order Peano support selection at origin',
                  'C2 support selection at origin','Polynomial support selection of any degree',
                  'Convex polynomial lift in entries and determinant',
                  'SOS polyconvexity in arXiv:2604.11124 Definition 2.5',
                  'Lifted SOS polyconvexity in that paper Definition 2.4'],
    'ordinary_polyconvexity':'UNKNOWN',
    'quasiconvexity':'UNKNOWN',
    'scope':'Internal analytic reconstruction and exact algebra. Not a non-polyconvexity proof, gradient-law witness, novelty certificate, or external validation.',
})
result['script_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
(OUT/'EXACT_AUDIT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
