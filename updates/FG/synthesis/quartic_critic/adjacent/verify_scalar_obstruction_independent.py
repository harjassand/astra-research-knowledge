#!/usr/bin/env python3
"""Independent scalar-PSD-Gram obstruction; no worker code/data imported.

The obstruction concerns output-rotation-invariant bilinear SOS channels,
not arbitrary nonnegative corrected densities or quasiconvexity.
"""
from pathlib import Path
import itertools
import json
import sympy as S

HERE=Path(__file__).resolve().parent
L,J=S.symbols("L J",real=True)
m=L**4-48*L**2+384
jp=J**2+(S.Rational(3,8)*L*L-8)*J+1
gb=S.groebner([m,jp],J,L,order="lex",domain=S.QQ)
def red(poly):return gb.reduce(S.expand(poly))[1]
monfield=[J**e*L**d for e in range(2) for d in range(4)]

a,b,c,d=S.symbols("a b c d",real=True);x=S.Matrix([a,b,c,d]);h=S.symbols("h0:6",real=True)
B1=S.Matrix([h[0],h[1],h[3],h[4]]);B2=S.Matrix([h[1],h[2],h[4],h[5]])
first=S.Matrix([a,c]);second=S.Matrix([b,d])
X=S.Matrix([h[0],h[3]]);Y=S.Matrix([h[1],h[4]]);Z=S.Matrix([h[2],h[5]])
def cross(p,q):return p[0]*q[1]-p[1]*q[0]
zp=S.Matrix([first.dot(X),first.dot(Z),second.dot(Y),cross(first,Y),cross(second,X),cross(second,Z)])
zm=S.Matrix([-second.dot(Z),-second.dot(X),-first.dot(Y),cross(second,Y),cross(first,Z),cross(first,X)])
u,v,w,q=first.dot(first),second.dot(second),first.dot(second),cross(first,second)
F=u*u+v*v+4*w*w+4*q*q+L*q*(u+v)
HF=S.hessian(F,x);energy=(B1.T*HF*B1+B2.T*HF*B2)[0]
xpairs=list(itertools.combinations_with_replacement(range(4),2));hpairs=list(itertools.combinations_with_replacement(range(6),2))
fpairs=list(itertools.combinations(range(4),2));spairs=list(itertools.combinations_with_replacement(range(6),2))
exps=[tuple(2 if k==i==j else int(k==i)+int(k==j) for k in range(4))+tuple(2 if k==p==q else int(k==p)+int(k==q) for k in range(6)) for i,j in xpairs for p,q in hpairs]
lookup={e:i for i,e in enumerate(exps)}
def coeff(poly):
    z=S.zeros(210,1)
    for e,c in S.Poly(S.expand(poly),tuple(x)+h).terms():z[lookup[e]]=c
    return z
scalar_polys=[(zp[i]*zp[j]+zm[i]*zm[j])*(1 if i==j else 2) for i,j in spairs]
scalar_columns=S.Matrix.hstack(*[coeff(p) for p in scalar_polys])

# All homogeneous quadratic two-forms, with full exterior closedness.
ww=S.symbols("w0:60");xmons=[x[i]*x[j] for i,j in xpairs]
forms={ij:sum(ww[10*n+k]*mm for k,mm in enumerate(xmons)) for n,ij in enumerate(fpairs)}
def om(i,j):return forms[(i,j)] if i<j else -forms[(j,i)]
closure=[]
for i,j,k in itertools.combinations(range(4),3):
    p=S.expand(S.diff(om(j,k),x[i])-S.diff(om(i,k),x[j])+S.diff(om(i,j),x[k]))
    closure.extend(p.coeff(z) for z in x)
cl,_=S.linear_eq_to_matrix(closure,ww)
assert cl.rank()==15
N=S.Matrix.hstack(*cl.nullspace());assert N.cols==45
OO=S.Matrix.hstack(*[coeff(mm*(B1[i]*B2[j]-B1[j]*B2[i])) for i,j in fpairs for mm in xmons])
closed=OO*N
assert closed.rank()==45
fullrank=scalar_columns.row_join(-closed).rank()
assert fullrank==60
print("PASS full closed-form dimension45; scalar quotient rank15; feasible common6 family dimension6.",flush=True)

# Construct an explicit six-dimensional affine family using five invariant
# primitives. Dimension comparison above makes it complete even against
# arbitrary, noninvariant closed quadratic two-forms.
gg=S.symbols("g0:21");cc=S.symbols("c0:5")
G=S.zeros(6)
for (i,j),z in zip(spairs,gg):G[i,j]=G[j,i]=z
theta=S.Matrix([-c,-d,a,b]);zeta=S.Matrix([-b,a,-d,c]);thetaa=S.Matrix([-c,d,a,-b])
prim=[(u+v)*theta,q*theta,(u+v)*zeta,q*zeta,(u-v)*thetaa]
alpha=sum((co*p for co,p in zip(cc,prim)),S.zeros(4,1))
omega=alpha.jacobian(x).T-alpha.jacobian(x)
eq=coeff(energy+(B1.T*omega*B2)[0]-(zp.T*G*zp+zm.T*G*zm)[0])
mat,rhs=S.linear_eq_to_matrix(list(eq),gg+cc)
sol=next(iter(S.linsolve((mat,rhs))))
free=sorted(set().union(*(z.free_symbols for z in sol))-{L},key=str)
assert len(free)==6
template=G.subs(dict(zip(gg+cc,sol)))
assert S.Matrix([[template[i,j].diff(z) for z in free] for i,j in spairs]).rank()==6
base=template.subs(dict.fromkeys(free,0));derivatives=[template.diff(z) for z in free]

AA=S.Matrix([[12+8*J,16*J,-2*J],[16,8+12*J,-1-3*J],[-2*L*L,-L*L*(1+3*J),4+8*J]])
rho,sigma,chi=(AA.adjugate()*S.Matrix([-3-J,-2,0])).applyfunc(red)
D=red(AA.det())
vp=S.Matrix([L*rho,L*J*rho,L*J*sigma,-J*chi,-D,-J*D]).applyfunc(red)
vm=S.Matrix([L*J*sigma,L*sigma,L*rho,D,J*chi,chi]).applyfunc(red)
lin=S.Matrix.hstack(*[(M*vp).col_join(M*vm) for M in derivatives]).applyfunc(red)
target=(-base*vp).col_join(-base*vm).applyfunc(red)

def cv(vec):
    return S.Matrix([S.Poly(red(p),J,L,domain=S.QQ).coeff_monomial(mm) for p in vec for mm in monfield])
linear=S.Matrix.hstack(*[cv(mm*lin[:,i]) for i in range(6) for mm in monfield])
right=cv(target)
fieldsol=next(iter(S.linsolve((linear,right))))
assert not set().union(*(z.free_symbols for z in fieldsol))
values=[sum(fieldsol[8*i+n]*mm for n,mm in enumerate(monfield)) for i in range(6)]
face=template.subs(dict(zip(free,values))).applyfunc(red)
assert (face*vp).applyfunc(red)==S.zeros(6,1)
assert (face*vm).applyfunc(red)==S.zeros(6,1)
negative=red(face[2:5,2:5].det())
assert negative==74*L*L-768
assert 74*S.Rational(51,5)-768<0
print("PASS forced common6 Gram has exact negative principal minor74L^2-768.",flush=True)

# All-real uniqueness: isolate roots afresh to55 decimal places and verify
# a selected6x6 minor has a sign. Algebraic gauge membership is not assumed.
boxes=S.Poly(m,L).intervals(eps=S.Rational(1,10**55))
Kbox=next((p,q) for (p,q),multiplicity in boxes if S.Rational(31849,10000)<p<q<S.Rational(3185,1000))
jpoly=J**4+2*J**3-24*J*J+2*J+1
jboxes=S.Poly(jpoly,J).intervals(eps=S.Rational(1,10**55))
jp0,jq0=next((p,q) for (p,q),multiplicity in jboxes if S.Rational(1,4)<p<q<S.Rational(13,50))
eps=S.Rational(1,10**45);Jbox=(jp0-eps,jq0+eps)
def box(poly):
    lower=upper=S.Rational(0)
    for exponents,c in S.Poly(S.expand(poly),L,J,domain=S.QQ).terms():
        ll=Kbox[0]**exponents[0]*Jbox[0]**exponents[1]
        hh=Kbox[1]**exponents[0]*Jbox[1]**exponents[1]
        aa,bb=(c*ll,c*hh) if c>=0 else (c*hh,c*ll)
        lower+=aa;upper+=bb
    return lower,upper
assert box(jp.subs(J,Jbox[0]))[0]>0
assert box(jp.subs(J,Jbox[1]))[1]<0
mid={L:sum(Kbox)/2,J:sum(Jbox)/2}
rows=list(lin.subs(mid).T.rref()[1]);assert len(rows)==6
determinant=red(lin[rows,:].det(method="domain-ge"))
detbounds=box(determinant)
assert detbounds[0]>0 or detbounds[1]<0
print("PASS explicit6x6 minor excludes0 at the real root; unique for all real gauges.",flush=True)

# Exact domain/output actions reduce every scalar12 PSD Gram to common6.
rot={a:b,b:-a,c:d,d:-c,h[0]:h[2],h[1]:-h[1],h[2]:h[0],h[3]:h[5],h[4]:-h[4],h[5]:h[3]}
refl={a:a,b:-b,c:-c,d:d,h[0]:h[0],h[1]:-h[1],h[2]:h[2],h[3]:-h[3],h[4]:h[4],h[5]:-h[5]}
assert (zp.subs(rot,simultaneous=True)+zm).applyfunc(S.expand)==S.zeros(6,1)
assert (zm.subs(rot,simultaneous=True)-zp).applyfunc(S.expand)==S.zeros(6,1)
assert (zp.subs(refl,simultaneous=True)-zp).applyfunc(S.expand)==S.zeros(6,1)
assert (zm.subs(refl,simultaneous=True)+zm).applyfunc(S.expand)==S.zeros(6,1)
assert S.expand(F.subs(rot,simultaneous=True)-F)==0
assert S.expand(F.subs(refl,simultaneous=True)-F)==0
out={"status":"PASS","closed_two_form_dimension":45,"closed_scalar_combined_rank":fullrank,"scalar_quotient_rank":15,"common6_gauges":6,
     "all_real_uniqueness":{"rows":rows,"determinant":str(determinant),"nonzero_interval":list(map(str,detbounds)),"K_interval":list(map(str,Kbox)),"j_interval":list(map(str,Jbox))},
     "forced_gram_matrix":[[str(z) for z in row] for row in face.tolist()],"negative_principal_minor":str(negative),
     "scalar12_group_actions":True,"scope":"No PSD Gram using only output-SO2-invariant bilinear scalar channels (all12 dot/cross channels), even with arbitrary closed homogeneous-quadratic omega and constant positive diffusion metric after averaging. No claim about non-SOS corrected densities, nonlinear/nonlocal flows, unrestricted tensor channels or quasiconvexity."}
(HERE/"SCALAR_OBSTRUCTION_INDEPENDENT_RESULTS.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"status":"PASS","negative_minor":str(negative),"all_real_uniqueness_rows":rows}))
