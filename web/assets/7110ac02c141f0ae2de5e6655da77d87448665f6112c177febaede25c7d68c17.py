"""Exact transcription audit for ORTHOGONAL_PROOF.txt.

The all-dimensional argument is analytic in that file. This program checks
symbolic coefficient identities for arbitrary d, and embeds them exactly in
the actual three-register matrices in d=2,3,4. It does not prove unrestricted
EB rounding or establish prior-art novelty. Requires Python and SymPy only.
"""
import json
from pathlib import Path
import sympy as sp

d, u = sp.symbols('d u', positive=True, real=True)
x = sp.Symbol('x')
G = sp.Matrix([[1, 1/d, 1/d], [1/d, 1, 1/d], [1/d, 1/d, 1]])
KP = sp.Matrix([[1, 1/d, 1/d], [1/d, 1, 1/d], [0, 0, 0]])
KF = sp.Matrix([[1, 0, 1], [0, 1, 1], [1, 1, 0]])
KA = d**2/2*KP-d/2*KF
KS = d**2/2*KP+d/2*KF-2*sp.eye(3)

def zero(M):
    assert M.applyfunc(sp.simplify) == sp.zeros(*M.shape)

zero(G*KP-KP.T*G)
zero(G*KF-KF.T*G)
antisym = sp.Matrix([1, -1, 0])
zero(KA*antisym-d*(d-2)/2*antisym)
zero(KS*antisym-(d*d/2-2)*antisym)

# Columns are u=x+y and w. No orthonormal-basis assumption is made.
B = sp.Matrix([[1, 0], [1, 0], [0, 1]])
KA2 = sp.Matrix([[d*d/2, 0], [-d, 0]])
KS2 = sp.Matrix([[d*d/2+d-2, d], [d, -2]])
zero(KA*B-B*KA2)
zero(KS*B-B*KS2)
G2 = B.T*G*B
zero(G2*KA2-KA2.T*G2)
zero(G2*KS2-KS2.T*G2)

cpA = sp.factor(KA2.charpoly(x).as_expr())
cpS = sp.factor(KS2.charpoly(x).as_expr())
assert sp.simplify(cpA-x*(x-d*d/2)) == 0
expectedS = x*x-(d*d/2+d-4)*x-2*d*d-2*d+4
assert sp.simplify(cpS-expectedS) == 0
Lplus = (d*d+2*d-8+d*sp.sqrt(d*d+4*d+20))/4
Lminus = (d*d+2*d-8-d*sp.sqrt(d*d+4*d+20))/4
assert sp.simplify(expectedS.subs(x,Lplus)) == 0
assert sp.simplify(expectedS.subs(x,Lminus)) == 0
assert sp.expand((d+4)**2-(d*d+4*d+20)) == 4*(d-1)

# Exact projector/swap actions and the whole three-register embeddings.
checks = []
for dd in (2,3,4):
    N = dd**3
    ix = lambda r,a,b: (r*dd+a)*dd+b
    PA, PB, FA, FB = (sp.zeros(N) for _ in range(4))
    for r in range(dd):
        for a in range(dd):
            for b in range(dd):
                col = ix(r,a,b)
                FA[ix(a,r,b),col] = 1
                FB[ix(b,a,r),col] = 1
                if r == a:
                    for k in range(dd):
                        PA[ix(k,k,b),col] = sp.Rational(1,dd)
                if r == b:
                    for k in range(dd):
                        PB[ix(k,a,k),col] = sp.Rational(1,dd)
    E = sp.zeros(N,3*dd)
    for v in range(dd):
        for k in range(dd):
            E[ix(k,k,v),v] = 1
            E[ix(k,v,k),dd+v] = 1
            E[ix(v,k,k),2*dd+v] = 1
    KPdd = sp.kronecker_product(KP.subs(d,dd),sp.eye(dd))
    KFdd = sp.kronecker_product(KF,sp.eye(dd))
    Gdd = sp.kronecker_product(G.subs(d,dd),sp.eye(dd))
    zero((PA+PB)*E-E*KPdd)
    zero((FA+FB)*E-E*KFdd)
    zero(E.T*E-dd*Gdd)
    zero(PA*PA-PA)
    zero(PB*PB-PB)
    zero(FA*FA-sp.eye(N))
    zero(FB*FB-sp.eye(N))
    WA = dd*dd/sp.Integer(2)*(PA+PB)-dd/sp.Integer(2)*(FA+FB)
    WS = dd*dd/sp.Integer(2)*(PA+PB)+dd/sp.Integer(2)*(FA+FB)-2*sp.eye(N)
    zero(WA-WA.T)
    zero(WS-WS.T)
    zero(WA*E-E*sp.kronecker_product(KA.subs(d,dd),sp.eye(dd)))
    zero(WS*E-E*sp.kronecker_product(KS.subs(d,dd),sp.eye(dd)))
    # The star annihilating polynomials contain also all possible S3
    # complement eigenvalues of F_RA+F_RB, namely -2,-1,1,2.
    rootsA = [sp.Integer(0),sp.Rational(dd*dd,2),sp.Rational(dd*(dd-2),2)]
    rootsA += [sp.Rational(dd*t,2) for t in (-2,-1,1,2)]
    polyA = sp.prod(x-r for r in set(rootsA))
    rootsS = [sp.Rational(dd*dd,2)-2]
    rootsS += [sp.Rational(dd*t,2)-2 for t in (-2,-1,1,2)]
    polyS = expectedS.subs(d,dd)*sp.prod(x-r for r in set(rootsS))
    for W,poly in ((WA,polyA),(WS,polyS)):
        Z = sp.zeros(N)
        for coeff in sp.Poly(poly,x).all_coeffs():
            Z = Z*W+coeff*sp.eye(N)
        zero(Z)
    checks.append({'d':dd,'matrix_dimension':N,'contraction_rank':E.rank(),
                   'antisymmetric_annihilator':str(sp.factor(polyA)),
                   'symmetric_annihilator':str(sp.factor(polyS)),
                   'exact_zero_checks_passed':True})

# Orbit and cloner identities, including physical finite-precision clamping.
z = 1-(d-1)*u
mua = (1-z)/(d-1)
mus = (d*(1+z)-2)/((d-1)*(d+2))
assert sp.simplify(mua-u) == 0
assert sp.simplify(mus-(2-d*u)/(d+2)) == 0
assert sp.simplify(mus.subs(u,1/(d+1))-1/(d+1)) == 0
lamcl = (d+2)/(2*(d+1))
assert sp.simplify((1-1/(d+1))/(1-lamcl)-2) == 0

result = {
    'status':'EXACT-TRANSCRIPTION-CHECKS-PASSED',
    'scientific_scope':'O(d)-covariant analytic theorem only; novelty UNKNOWN',
    'sympy_version':sp.__version__,
    'symbolic_antisymmetric_charpoly':str(cpA),
    'symbolic_symmetric_charpoly':str(cpS),
    'symbolic_L_plus':str(Lplus),
    'gram_selfadjointness_passed':True,
    'rounding_symbolic_identities_passed':True,
    'small_dimension_exact_checks':checks
}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
