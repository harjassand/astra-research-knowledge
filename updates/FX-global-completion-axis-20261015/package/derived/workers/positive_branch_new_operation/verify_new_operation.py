#!/usr/bin/env python3
"""Exact algebra checks for the nonlocal-operation investigation.

The analytic arguments are written in REPORT.md.  This checks identities,
not universal quasiconvexity, the recent Burkholder claim, or historical novelty.
"""

import itertools
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
checks = []


def zero(name, expr):
    val = sp.factor(sp.cancel(sp.expand(expr)))
    assert val == 0, (name, val)
    checks.append({"name": name, "status": "PASS"})


def main():
    r = sp.Symbol("r", positive=True)
    t = sp.Symbol("t", real=True)
    a, b, c, d = avars = sp.symbols("a b c d", real=True)
    u = a*a+c*c
    j = a*d-b*c
    H = ((a-d)**2+(b+c)**2)**2
    F = 3*r/(8*(r+2))*H + r*(r-1)/6*u*u + j*j + r*u*j
    alpha = 3*r/(8*(r+2))
    zero("J_r exact flat shear", F.subs({a:1, b:t, c:0, d:1})
         - F.subs({a:1, b:0, c:0, d:1}) - alpha*t**4)

    # In a signed SVD frame A=diag(x,k*x), x>0, -1<k<1, k!=0.
    # R=[[aa,bb],[cc,-k*aa]], with bb*cc=-k*aa^2.
    x = sp.Symbol("x", positive=True)
    k, aa, bb, cc = sp.symbols("k aa bb cc", real=True)
    rho = (1+k*k)*aa*aa+bb*bb+cc*cc
    lp = 2*x*aa
    lpp = 2*((1-3*k*k)*aa*aa+bb*bb+cc*cc)/(1-k*k)
    # Differentiate s=lambda+j^2/lambda implicitly at lambda=x^2.
    zero("largest singular-square first derivative",
         (1-k*k)*lp-2*x*(1-k*k)*aa)
    zero("largest singular-square second derivative",
         (1-k*k)*lpp+2*k*k/x**2*lp**2-2*rho)
    D2 = 2*lp**2+2*x*x*(1-k)*lpp
    formula = 4*x*x/(1+k)*((3+2*k-3*k*k)*aa*aa+bb*bb+cc*cc)
    zero("Burkholder trace-free shear second derivative", D2-formula)
    plus = 4*x*x/(1+k)*((3+4*k-3*k*k)*aa*aa+(bb+cc)**2)
    minus = 4*x*x/(1+k)*(3*(1-k*k)*aa*aa+(bb-cc)**2)
    rankone_relation = bb*cc+k*aa*aa
    zero("positive determinant positivity decomposition",
         plus-formula-8*x*x/(1+k)*rankone_relation)
    zero("negative determinant positivity decomposition",
         minus-formula+8*x*x/(1+k)*rankone_relation)
    # 3+4k-3k^2 >= 3 on [0,1].
    zero("positive determinant scalar lower bound",
         (3+4*k-3*k*k)-3-k*(4-3*k))

    # The coincident-singular-value endpoints need separate expansions.
    tp, rho0 = sp.symbols("tp rho0", positive=True)
    lam = x*x+rho0*tp*tp/2+tp*sp.sqrt(rho0)*sp.sqrt(4*x*x+rho0*tp*tp)/2
    bp = lam*lam-2*x*x*lam
    bn = lam*lam+2*x*x*lam
    zero("positive conformal second variation",
         sp.limit(2*(bp+x**4)/(tp*tp), tp, 0, dir="+")-2*x*x*rho0)
    zero("negative conformal symmetric first cusp",
         sp.limit(2*(bn-3*x**4)/tp, tp, 0, dir="+")-8*x**3*sp.sqrt(rho0))

    # Exact compatible periodic failure of scalar-potential projection
    # monotonicity, for every r>0. Independent polynomial trigonometric means.
    sx,cx,sy,cy,PA,PB = sp.symbols("sx cx sy cy PA PB", real=True)
    phix = -2*PA*(cx*cx-sx*sx)*cy-2*PB*sx*sy*cy
    phiy = 2*PA*sx*cx*sy+2*PB*cx*(cy*cy-sy*sy)
    det0 = phix*cy-phiy*cx
    norm0 = cx*cx+cy*cy
    norm1 = phix*phix+phiy*phiy

    def scalar_mean(i,j):
        if i % 2 or j % 2:
            return sp.S(0)
        m,n = i//2,j//2
        return sp.factorial(2*m)*sp.factorial(2*n)/(4**(m+n)*sp.factorial(m)*sp.factorial(n)*sp.factorial(m+n))

    def trig_mean(ex):
        return sp.expand(sum(co*scalar_mean(i,j)*scalar_mean(k,l)
                             for (i,j,k,l),co in sp.Poly(sp.expand(ex),sx,cx,sy,cy).terms()))

    beta = r*(r-1)/6
    coeffs = [sp.Rational(5,4)*alpha+sp.Rational(3,8)*beta,
              trig_mean((r*cx*cx-4*alpha*norm0)*det0),
              (4*alpha+1)*trig_mean(det0*det0)+2*alpha*trig_mean(norm0*norm1)
              +2*beta*trig_mean(cx*cx*phix*phix),
              -4*alpha*trig_mean(det0*norm1)+r*trig_mean(phix*phix*det0),
              alpha*trig_mean(norm1*norm1)+beta*trig_mean(phix**4)]
    coeffs = [sp.factor(co.subs({PA:r-4*alpha,PB:-4*alpha})) for co in coeffs]
    claimed = [r*(2*r*r+2*r+11)/(32*(r+2)),
               -r*r*(2*r*r+2*r+5)/(8*(r+2)**2),
               r*r*(64*r**5+128*r**4+1224*r**3+932*r*r+2569*r+1320)/(384*(r+2)**3),
               3*r**4*(2*r+1)*(8*r*r+26*r+29)/(64*(r+2)**4),
               3*r**5*(512*r**6+1536*r**5+2824*r**4+3088*r**3+6174*r*r+4886*r+7305)/(4096*(r+2)**5)]
    for n,(computed,claim) in enumerate(zip(coeffs,claimed)):
        zero("compatible scalar projection energy coefficient %d" % n,computed-claim)
    for n in [0,2,3,4]:
        numerator,denominator = sp.fraction(coeffs[n])
        for polynomial in [numerator,denominator]:
            coefficients = sp.Poly(polynomial,r).all_coeffs()
            assert all(co >= 0 for co in coefficients) and any(co > 0 for co in coefficients)
        checks.append({"name":"projection coefficient %d positive on r>0" % n,"status":"PASS"})
    delta = -coeffs[1]
    for pp in sp.fraction(delta):
        coefficients = sp.Poly(pp,r).all_coeffs()
        assert all(co >= 0 for co in coefficients) and any(co > 0 for co in coefficients)
    C0,_,C2,C3,C4 = coeffs
    eps_formula = delta*C0/(2*(delta**2+C0*(C2+C3+C4+delta)))
    dd,ee,ss = sp.symbols("dd ee ss",positive=True)
    denominator = dd*dd+ee*(ss+dd)
    eps0 = dd*ee/(2*denominator)
    zero("universal epsilon upper bound by delta",dd/(2*(ss+dd))-eps0
         -dd**3/(2*(ss+dd)*denominator))
    zero("universal epsilon positivity-energy upper bound",ee/(2*dd)-eps0
         -ee*ee*(ss+dd)/(2*dd*denominator))
    zero("universal epsilon below one half",sp.Rational(1,2)-eps0
         -(dd*dd+ee*ss)/(2*denominator))
    er1 = sp.factor(sum(co.subs(r,1)*t**n for n,co in enumerate(coeffs)))
    zero("r=1 periodic energy polynomial",er1-(325*t**4+448*t**3+2464*t*t-512*t+640)/4096)
    p1=phix.subs({PA:sp.Rational(1,2),PB:-sp.Rational(1,2)})
    q1=phiy.subs({PA:sp.Rational(1,2),PB:-sp.Rational(1,2)})
    direct = F.subs({r:1,a:t*p1,b:t*q1,c:cx,d:cy},simultaneous=True)
    zero("r=1 energy regenerated directly from J_r",trig_mean(direct)-er1)
    gap = sp.factor(er1.subs(t,0)-er1.subs(t,sp.Rational(1,10)))
    zero("r=1 exact scalar projection increase",gap-sp.Rational(52159,8192000))
    radius = gap/26
    zero("positive radius gap guarantee",gap-13*radius-gap/2)
    assert 0 < radius < 1
    assert sp.Rational(125,16)+2+3 < 13
    assert sp.sqrt(2)+1 < sp.Rational(5,2)
    assert 2*sp.sqrt(2) < 3
    checks.append({"name":"positive-cap energy-continuity constants valid","status":"PASS"})

    # Pointwise radial clipping is not the projection of a scalar potential:
    # psi=sin(x)sin(y), radius 1/2, at x=pi/6,y=pi/3.
    xx,yy = sp.symbols("xx yy",real=True)
    psi = sp.sin(xx)*sp.sin(yy)
    gx,gy = sp.diff(psi,xx),sp.diff(psi,yy)
    length = sp.sqrt(gx*gx+gy*gy)
    clipped_curl = sp.diff(gy/(2*length),xx)-sp.diff(gx/(2*length),yy)
    curl_value = sp.simplify(clipped_curl.subs({xx:sp.pi/6,yy:sp.pi/3}))
    zero("naive clipping nonzero curl exact value",curl_value-2*sp.sqrt(3)/(5*sp.sqrt(10)))
    assert curl_value != 0
    checks.append({"name":"naive clipped field is incompatible","status":"PASS"})
    projection_record = {
        "status":"compatible projection-monotonicity counterexample, NOT QC counterexample",
        "domain":"[0,2*pi]^2 with normalized periodic average",
        "map":"v_epsilon=(epsilon*phi,psi), psi=sin(x)+sin(y), phi=-2*cos(x)*cos(y)*((r-4*alpha)*sin(x)+4*alpha*sin(y))",
        "alpha":"3*r/(8*(r+2))",
        "energy_coefficients_in_epsilon":[str(co) for co in coeffs],
        "universal_small_positive_epsilon":str(eps_formula),
        "universal_energy_lower_bound":"C0/2",
        "universal_projection_increase_lower_bound":"delta*epsilon/2",
        "r1_explicit_epsilon":"1/10",
        "r1_original_energy":str(er1.subs(t,sp.Rational(1,10))),
        "r1_zero_projected_energy":str(er1.subs(t,0)),
        "r1_zero_projection_increase":str(gap),
        "r1_positive_gradient_cap_radius":str(radius),
        "r1_positive_cap_projection_increase_lower_bound":str(gap/2),
        "positive_cap_argument":"Every feasible projected first gradient has norm<=radius; a uniform 13*radius energy-continuity bound proves the increase without needing explicit projected potential.",
        "naive_pointwise_clipping_curl":str(curl_value),
        "quasiconvexity_of_J_r":"UNKNOWN",
    }
    (ROOT/"PROJECTION_COUNTEREXAMPLE.json").write_text(json.dumps(projection_record,indent=2)+"\n")

    # Independently verify the compatible three-wave moment identities
    # symbolically, for arbitrary six real amplitudes and all r.
    fbar = sp.cancel(24*(r+2)*F)
    T = {}
    for ii in itertools.product(range(4), repeat=4):
        coeff = sp.diff(fbar, *(avars[i] for i in ii))/24
        if coeff != 0:
            T[ii] = coeff
    p0,p1,q0,q1,z0,z1 = sp.symbols("p0 p1 q0 q1 z0 z1", real=True)
    W = [sp.Matrix([p0,0,p1,0]), sp.Matrix([0,q0,0,q1]),
         sp.Matrix([z0,z0,z1,z1])]

    def quartic(v0,v1,v2,v3):
        vv = (v0,v1,v2,v3)
        return sp.expand(sum(co*sp.prod(vv[n][ii[n]] for n in range(4))
                             for ii,co in T.items()))

    A = sp.Rational(3,8)*sum(quartic(w,w,w,w) for w in W)
    A += sp.Rational(3,2)*sum(quartic(W[i],W[i],W[j],W[j])
                              for i in range(3) for j in range(i))
    basis = [sp.eye(4)[:,i] for i in range(4)]
    K = sp.Matrix(4,4,lambda i,j: 3*sum(quartic(basis[i],basis[j],w,w) for w in W))
    cv = sp.Matrix([6*quartic(e,*W) for e in basis])
    X,Y = sp.symbols("X Y", nonzero=True)
    V = W[0]*(X+1/X)/2+W[1]*(Y+1/Y)/2+W[2]*(X*Y+1/(X*Y))/2
    substitution = dict(zip(avars,V))
    constant = lambda ex: sp.expand(ex).coeff(X,0).coeff(Y,0)
    zero("three-wave fourth moment", constant(fbar.subs(substitution, simultaneous=True))-A)
    for i in range(4):
        zero("three-wave cubic moment %d" % i,
             constant(sp.diff(fbar,avars[i]).subs(substitution, simultaneous=True))-cv[i])
    for i in range(4):
        for j0 in range(i+1):
            zero("three-wave quadratic moment %d,%d" % (i,j0),
                 constant(sp.diff(fbar,avars[i],avars[j0]).subs(substitution, simultaneous=True))/2
                 -K[i,j0])
    record = {
        "status":"PASS",
        "checks":checks,
        "proof_scope":"exact identities for Burkholder shear obstruction, compatible scalar projection counterexample, and compatible moment reduction",
        "quasiconvexity_of_J_r":"UNKNOWN",
        "recent_external_Burkholder_QC_claim_verified":False,
        "universal_QC_counterexample_found":False,
        "historical_priority":"NOT_CLEARED",
    }
    (ROOT/"EXACT_VERIFICATION.json").write_text(json.dumps(record,indent=2)+"\n")
    print(json.dumps(record,indent=2))


if __name__ == "__main__":
    main()
