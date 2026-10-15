"""Independent exact Laurent/Fourier checks for the late resonance state."""
from pathlib import Path
from fractions import Fraction as F
import json
import sympy as S

ROOT = Path(__file__).resolve().parent
checks = []


def report(name, details):
    checks.append({"name":name,"status":"PASS","details":details})
    print("PASS:",name,flush=True)


def add(*polys):
    z = {}
    for poly in polys:
        for k,v in poly.items():
            z[k] = z.get(k,F(0))+v
    return {k:v for k,v in z.items() if v}


def scale(poly, c):
    return {k:c*v for k,v in poly.items() if c*v}


def mul(p, q):
    z = {}
    for k,v in p.items():
        for ell,w in q.items():
            key = tuple(a+b for a,b in zip(k,ell))
            z[key] = z.get(key,F(0))+v*w
    return {k:v for k,v in z.items() if v}


def power(p, n):
    z = {(0,0):F(1)}
    for _ in range(n):
        z = mul(z,p)
    return z


def mean(poly):
    return poly.get((0,0),F(0))


def hessian_modes(modes, amplitudes):
    out = [{}, {}, {}]
    for (kx,ky),amp in zip(modes,amplitudes):
        for pos, coefficient in enumerate((-kx*kx,-kx*ky,-ky*ky)):
            block = {(kx,ky):F(amp*coefficient,2),(-kx,-ky):F(amp*coefficient,2)}
            out[pos] = add(out[pos],block)
    return out


def quartic(p,q,r):
    terms = [(8667,4,0,0),(18792,3,0,1),(576,2,2,0),(16416,2,0,2),
             (1440,1,2,1),(6912,1,0,3),(56,0,4,0),(576,0,2,2),(1152,0,0,4)]
    return scale(add(*(scale(mul(mul(power(p,i),power(q,j)),power(r,k)),F(c))
                       for c,i,j,k in terms)), F(1,1944))


def point_K(v):
    p,q,r=v
    return F(8667*p**4+18792*p**3*r+576*p*p*q*q+16416*p*p*r*r+1440*p*q*q*r
             +6912*p*r**3+56*q**4+576*q*q*r*r+1152*r**4,1944)


def exact_coeffs(modes):
    jets=[(-kx*kx,-kx*ky,-ky*ky) for kx,ky in modes]
    alpha=[F(5,24)*j[0]**2 for j in jets]
    beta=[F(3,8)*point_K(j) for j in jets]
    gamma=[]
    for i,j in ((0,1),(0,2),(1,2)):
        plus=tuple(a+b for a,b in zip(jets[i],jets[j]))
        minus=tuple(a-b for a,b in zip(jets[i],jets[j]))
        gamma.append((point_K(plus)+point_K(minus)-2*point_K(jets[i])-2*point_K(jets[j]))/8)
    p=[j[0] for j in jets];q=[j[1] for j in jets]
    cubic=-F(5,36)*sum(q[i]*p[(i+1)%3]*p[(i+2)%3] for i in range(3))
    cubic-=F(5,27)*q[0]*q[1]*q[2]
    return alpha,beta,gamma,cubic


modes=((1,1),(1,2),(2,3))
p,q,r=hessian_modes(modes,(1,1,1))
assert mean(power(p,2)) == 9
assert mean(mul(q,power(p,2))) == -9
assert mean(power(q,3)) == -18
assert mean(add(scale(mul(q,power(p,2)),9),scale(power(q,3),4))) == -153
report("Explicit resonant base moments",{"p_squared":"9","q_p_squared":"-9","q_cubed":"-18","T":"-153"})

for modes in (((1,1),(1,2),(2,3)),((3,-4),(3,-3),(6,-7)),((1,-2),(2,1),(3,-1))):
    amps=(1,2,3)
    p,q,r=hessian_modes(modes,amps)
    alpha,beta,gamma,cubic=exact_coeffs(modes)
    quad_expected=sum(a*A*A for a,A in zip(alpha,amps))
    cubic_expected=cubic*amps[0]*amps[1]*amps[2]
    quartic_expected=sum(b*A**4 for b,A in zip(beta,amps))
    quartic_expected+=gamma[0]*amps[0]**2*amps[1]**2
    quartic_expected+=gamma[1]*amps[0]**2*amps[2]**2
    quartic_expected+=gamma[2]*amps[1]**2*amps[2]**2
    assert F(5,12)*mean(power(p,2)) == quad_expected
    assert -F(5,162)*mean(add(scale(mul(q,power(p,2)),9),scale(power(q,3),4))) == cubic_expected
    assert mean(quartic(p,q,r)) == quartic_expected
report("Independent exact Laurent integration of three triads",{"amplitudes":[1,2,3],"count":3})

alpha,beta,gamma,cubic=exact_coeffs(((3,-4),(3,-3),(6,-7)))
sq=(F(5,12),F(11,20),F(1,30))
Q=sum(a*s for a,s in zip(alpha,sq))
D=sum(b*s*s for b,s in zip(beta,sq))+gamma[0]*sq[0]*sq[1]+gamma[1]*sq[0]*sq[2]+gamma[2]*sq[1]*sq[2]
ratio=cubic*cubic*sq[0]*sq[1]*sq[2]/(4*Q*D)
assert ratio == F(398644400,446444401849) and ratio < F(1,1000)
report("Selected triad ratio is exact",{"ratio":str(ratio),"strict_upper":"1/1000"})

a,b,c,d,s,tau=S.symbols("a b c d s tau",real=True)
u=a*a+c*c;v=b*b+d*d;j=a*d-b*c
G=3*(u+v-2*j)**2+S.Rational(35,24)*u*u+j*j-S.Rational(5,2)*j*u
variables=(a,b,c,d)
identity={a:1,b:0,c:0,d:1}
curve={a:1+S.Rational(2,3)*s,b:0,c:0,d:1+s}
gradient=S.Matrix([S.diff(G,z).subs(identity) for z in variables])
increment=S.Matrix([S.Rational(2,3)*s,0,0,s])
W=S.expand(G.subs(curve)-G.subs(identity)-(gradient.T*increment)[0]+s*s/3)
assert S.factor(W) == s**3*(7*s-30)/243
report("No local determinant-affine tangent support at I",{"forced_tau":"1/2","remainder":str(S.factor(W)),"negative_range":"0<s<30/7"})

receipt={"status":"PASS","groups":len(checks),"checks":checks,
         "scope":"exact finite Laurent and matrix calculations, not universal QC",
         "negative_compatible_witness":"NOT_ESTABLISHED","novelty":"UNKNOWN"}
(ROOT/"late_exact_checks.json").write_text(json.dumps(receipt,indent=2)+"\n")
