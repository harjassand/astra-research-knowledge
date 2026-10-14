"""Exact finite checks accompanying PROOF.txt; not an analytic formalization."""
from pathlib import Path
import hashlib
import json
import sympy as s

OUT = Path(__file__).resolve().parent
records = []


def zero(expression):
    assert s.expand(expression) == 0, expression


def record(name, **data):
    records.append({"name": name, "passed": True, **data})
    print(name, "PASS", flush=True)


def jet_tools(k):
    q = [[s.Symbol(f"q_{j}_{a}") for a in range(2)] for j in range(2*k+1)]

    def D(expression):
        return s.expand(sum(s.diff(expression, q[j][a])*q[j+1][a]
                            for j in range(2*k) for a in range(2)))

    def euler(p):
        result = []
        for a in range(2):
            component = 0
            for j in range(k+1):
                term = s.diff(p, q[j][a])
                for _ in range(j):
                    term = D(term)
                component += (-1)**j*term
            result.append(s.expand(component))
        return result

    return q, D, euler


for k in range(1, 4):
    q, D, euler = jet_tools(k)
    args = [x for row in q[:k+1] for x in row]
    p = s.Function(f"p{k}")(*args)
    ep = euler(p)
    for a in range(2):
        for b in range(2):
            zero(s.diff(ep[a], q[2*k][b])
                 -(-1)**k*s.diff(p, q[k][a], q[k][b]))
            for c in range(2):
                zero(s.diff(ep[a], q[2*k][b], q[2*k][c]))
    record("arbitrary smooth highest-jet Hessian coefficient", order=k)

    lower = [x for row in q[:k] for x in row]
    avec = [s.Function(f"a{k}_{a}")(*lower) for a in range(2)]
    bfun = s.Function(f"b{k}")(*lower)
    affine = sum(avec[a]*q[k][a] for a in range(2))+bfun
    ea = euler(affine)
    for a in range(2):
        for b in range(2):
            target = (-1)**k*(s.diff(avec[a], q[k-1][b])
                             -s.diff(avec[b], q[k-1][a]))
            zero(s.diff(ea[a], q[2*k-1][b])-target)
            for c in range(2):
                zero(s.diff(ea[a], q[2*k-1][b], q[2*k-1][c]))
    record("arbitrary smooth affine highest-jet skew coefficient", order=k)

    H = s.Function(f"H{k}")(*lower)
    null = euler(D(H))
    for component in null:
        zero(component)
    record("arbitrary smooth total derivative has zero Euler derivative", order=k)

z1,z2,q1,q2,v1,v2 = s.symbols("z1 z2 q1 q2 v1 v2", real=True)
A = [0, -s.cos(z1)]
curvature = s.diff(A[1],z1)-s.diff(A[0],z2)
assert curvature == s.sin(z1)
detvq=v1*q2-v2*q1
area_density = s.Rational(1,2)*(z1*q2-z2*q1)
area_euler = [s.diff(area_density,z1)-s.diff(s.diff(area_density,q1),z1)*q1
              -s.diff(s.diff(area_density,q1),z2)*q2,
              s.diff(area_density,z2)-s.diff(s.diff(area_density,q2),z1)*q1
              -s.diff(s.diff(area_density,q2),z2)*q2]
zero(area_euler[0]*v1+area_euler[1]*v2-detvq)
record("oriented area first variation and nonconstant curvature example")

a,b,c,d,e,f,g,h = s.symbols("a b c d e f g h", real=True)
B=s.Matrix([[a,b],[c,d]])
X=s.Matrix([[e,f],[g,h]])
cof=s.Matrix([[d,-c],[-b,a]])
zero((B+X).det()-B.det()-s.trace(cof.T*X)-X.det())
zero(((B+X).det()+(B-X).det())/2-B.det()-X.det())
record("determinant-affine support and finite convex-lift two-point identity")

r=s.symbols("r", real=True)
integrand=(s.Rational(1,4)+r*r)**2-(4/s.sqrt(3))*(s.Rational(1,4)+r*r)*r/2
action=s.simplify(2*s.integrate(integrand,(r,0,1)))
zero(action-(s.Rational(103,120)-s.sqrt(3)/2))
margin=s.Rational(3,4)-s.Rational(103,120)**2
assert margin==s.Rational(191,14400)>0
record("negative entry action and exact sign", action=str(action), margin=str(margin))

sigma=s.symbols("sigma", real=True)
zero((4*(1-sigma)-1).subs(sigma,s.Rational(3,4)))
zero((4*sigma-3).subs(sigma,s.Rational(3,4)))
record("quartic strip and Slobodeckij critical exponents", exponent="3/4")

sources = [
    Path("/Users/harjas/Downloads/ASTRA_Universal_Compensation/UNIVERSAL_PROFILE_OBSTRUCTIONS.md"),
    Path("/Users/harjas/Downloads/ASTRA_Universal_Compensation/verify_universal_obstructions.py"),
    OUT/"PROOF.txt",
    Path(__file__).resolve(),
]
receipt = {
    "repo_pin": "00631610750c708263d5cf6d812ebbb8edc77335",
    "scope": "finite exact symbolic checks; analytic oscillation, localization, and trace compactness are not formalized",
    "all_passed": True,
    "records": records,
    "sha256": {str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
    "novelty": "UNKNOWN",
    "external_mathematical_review": "UNKNOWN",
}
(OUT/"CHECK_RECEIPT.json").write_text(json.dumps(receipt,indent=2)+"\n")
print(f"{len(records)} exact check groups passed; receipt saved.",flush=True)
