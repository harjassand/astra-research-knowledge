"""Exact coefficient acquisition and outward rational integral certificates.

No numerical eigensystem, fitted dynamics, random samples, or floating-point
result is a premise of admission. Floats appear only in display diagnostics.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as F
from math import isqrt, prod
from time import perf_counter
import json
import sympy as sp


class Unknown(ValueError):
    pass


def rat(x):
    """Strict rational decoding: no float, bool, or noncanonical alias."""
    if type(x) is int:
        return sp.Rational(x)
    if type(x) is str:
        z = F(x)
        if str(z) != x:
            raise Unknown("noncanonical rational")
        return sp.Rational(z.numerator, z.denominator)
    raise Unknown("coefficient must be integer or canonical rational string")


def decode(raw):
    if type(raw) is not dict or set(raw) != {"n", "terms"}:
        raise Unknown("raw input schema")
    n = raw["n"]
    if type(n) is not int or n < 3:
        raise Unknown("prototype needs n>=3")
    if type(raw["terms"]) is not list:
        raise Unknown("term list required")
    seen, terms = set(), {}
    for rec in raw["terms"]:
        if type(rec) is not dict or set(rec) != {"powers", "coefficient"}:
            raise Unknown("term schema")
        ps = rec["powers"]
        if type(ps) is not list or len(ps) != n:
            raise Unknown("power vector")
        if any(type(k) is not int or k < 0 for k in ps):
            raise Unknown("nonnegative integer powers required")
        p = tuple(ps)
        if p in seen:
            raise Unknown("duplicate monomial")
        seen.add(p)
        a = rat(rec["coefficient"])
        if not a or sum(p) > 6:
            raise Unknown("zero or excess-degree term")
        terms[p] = a
    if not terms or max(map(sum, terms)) != 6:
        raise Unknown("needs degree six")
    return n, terms


def encode(expr, xs):
    pp = sp.Poly(expr, *xs)
    return {"n": len(xs), "terms": [
        {"powers": list(p), "coefficient": str(c)}
        for p, c in pp.terms()]}


def sparse_fixture(m):
    n = m + 1
    terms = []
    for i in range(m):
        k = sp.Rational(1, 2) + sp.Rational(i, m-1)
        for yp, a in [(0, (1+k)/2), (2, -k), (4, k/2)]:
            ps = [0]*n
            ps[0], ps[i+1] = yp, 2
            terms.append({"powers": ps, "coefficient": str(a)})
    return {"n": n, "terms": terms}


def dense_fixture(m):
    """Only the expanded coefficients are returned to the acquisition path."""
    n = m+1
    xs = sp.symbols(f"x0:{n}")
    x = sp.Matrix(xs)
    vv = sp.Matrix(range(1, n+1))
    Q = sp.eye(n)-2*vv*vv.T/(vv.dot(vv))
    ell = Q[:, 0]
    kap = [sp.Rational(1,2)+sp.Rational(i,m-1) for i in range(m)]
    H = Q*sp.diag(0,*kap)*Q.T
    P = sp.eye(n)-ell*ell.T
    y = ell.dot(x)
    expression = sp.expand(((x.T*P*x)[0]+(1-y*y)**2*(x.T*H*x)[0])/2)
    return encode(expression, xs)


def try_sparse(n, terms):
    top = [p for p in terms if sum(p) == 6]
    common = [min(p[j] for p in top) for j in range(n)]
    candidate = [j for j,k in enumerate(common) if k == 4]
    if len(candidate) != 1:
        return None
    j = candidate[0]
    kap, expected = [], {}
    for i in range(n):
        if i == j:
            continue
        ps = [0]*n
        ps[j], ps[i] = 4, 2
        k = 2*terms.get(tuple(ps), 0)
        if k <= 0:
            return None
        kap.append(k)
        for yp, a in [(0,(1+k)/2), (2,-k), (4,k/2)]:
            ps = [0]*n
            ps[j], ps[i] = yp, 2
            expected[tuple(ps)] = a
    if terms != expected:
        return None
    return {"ell": [sp.Integer(int(i==j)) for i in range(n)],
            "kappa": kap, "route": "raw_sparse_coefficient_identity",
            "matrix_operations": 0, "gcd_calls": 0}


def acquire(raw):
    start = perf_counter()
    n, terms = decode(raw)
    out = try_sparse(n, terms)
    if out is None:
        xs = sp.symbols(f"x0:{n}")
        x = sp.Matrix(xs)
        pp = sp.Poly.from_dict(terms, xs)
        top = sp.Poly.from_dict({p:a for p,a in terms.items() if sum(p)==6}, xs)
        gg = top
        gcd_calls = 0
        for z in xs:
            gg = sp.gcd(gg, top.diff(z)); gcd_calls += 1
        ll = gg.sqf_part()
        if ll.total_degree() != 1 or ll.TC() != 0:
            raise Unknown("no unique repeated linear factor")
        vec = sp.Matrix([ll.coeff_monomial(z) for z in xs])
        norm = sp.sqrt(vec.dot(vec))
        if norm.is_Rational is not True:
            raise Unknown("algebraic unit normalization not implemented")
        ell = vec/norm
        first = next(c for c in ell if c)
        if first < 0:
            ell = -ell
        y = ell.dot(x)
        quot, rem = sp.div(2*top.as_expr(), y**4, *xs)
        if rem != 0 or sp.Poly(quot,*xs).total_degree()!=2:
            raise Unknown("highest part factor failure")
        H = sp.hessian(quot,xs)/2
        if H != H.T or H*ell != sp.zeros(n,1):
            raise Unknown("fiber matrix or null direction failure")
        P = sp.eye(n)-ell*ell.T
        expected = ((x.T*P*x)[0]+(1-y*y)**2*(x.T*H*x)[0])/2
        if sp.Poly(pp.as_expr()-expected,*xs) != sp.Poly(0,*xs):
            raise Unknown("full coefficient identity failed")
        try:
            _, D = (H+ell*ell.T).LDLdecomposition(hermitian=False)
        except Exception as exc:
            raise Unknown("LDL pivot failure") from exc
        if any(D[i,i] <= 0 for i in range(n)):
            raise Unknown("nonpositive Gaussian fiber")
        # For this prototype's generic path, rational roots are a backend
        # convenience, not a theorem assumption. It returns UNKNOWN if they
        # cannot be acquired; never substitutes floating eigenvalues.
        lam = sp.Symbol("lam")
        cp = H.charpoly(lam).as_poly()
        factors = sp.factor_list(cp)[1]
        kap = []
        zero_count = 0
        for fac, mult in factors:
            if fac.degree()!=1:
                raise Unknown("nonrational determinant-product backend not implemented")
            root = -fac.nth(0)/fac.nth(1)
            if root == 0:
                zero_count += mult
            elif root > 0:
                kap += [root]*mult
            else:
                raise Unknown("characteristic root not positive")
        if zero_count!=1 or len(kap)!=n-1:
            raise Unknown("fiber dimension mismatch")
        # Check the factorization, not a root finder tolerance.
        if sp.expand(lam*prod(lam-k for k in kap)-cp.as_expr())!=0:
            raise Unknown("characteristic factor verification failed")
        out={"ell":list(ell),"kappa":sorted(kap),
             "route":"exact_multivariate_gcd_full_identity_LDL_charpoly",
             "gcd_calls":gcd_calls,"matrix_operations":n**3}
    out.update(n=n,m=n-1,raw_terms=len(terms),
               acquisition_seconds=perf_counter()-start,
               max_input_rational_bits=max(max(abs(int(a.p)).bit_length(),int(a.q).bit_length()) for a in terms.values()))
    out["ell"]=[str(a) for a in out["ell"]]
    out["kappa"]=[str(a) for a in out["kappa"]]
    return out


def sqrt_bounds(a:F,p:int):
    """Integer endpoints for sqrt(a)*2**p, exact/outward."""
    assert a >= 0
    k = isqrt((a.numerator << (2*p))//a.denominator)
    exact = k*k*a.denominator == (a.numerator << (2*p))
    return k, k if exact else k+1


@dataclass
class Integrator:
    kappas: list[F]
    precision: int

    def __post_init__(self):
        if len(self.kappas)<2 or any(k<=0 for k in self.kappas):
            raise Unknown("positive fiber constants and m>=2 required")
        self.cache={}
        self.product_factors=0
        self.max_integer_bits=0

    def point(self,y:F):
        if y in self.cache:
            return self.cache[y]
        v=(1-y*y)**2
        # Do not simplify after each multiply: the exact numerator and
        # denominator products are faster and their bit sizes are charged.
        nums=[]; dens=[]
        for k in self.kappas:
            a=1+k*v
            nums.append(a.numerator); dens.append(a.denominator)
        nn,dd=prod(nums),prod(dens)
        self.product_factors+=len(nums)
        self.max_integer_bits=max(self.max_integer_bits,nn.bit_length(),dd.bit_length())
        D=F(nn,dd)
        q=sqrt_bounds(1/D,self.precision)
        w=sqrt_bounds(D,self.precision)
        self.cache[y]=(q,w)
        return q,w

    def monotone_integral(self,a:F,b:F,N:int,which:int):
        """Darboux bounds; caller supplies intervals with no v turning point."""
        assert a<b and N>0
        h=(b-a)/N
        prev=self.point(a)[which]
        low=up=0
        for j in range(1,N+1):
            cur=self.point(a+j*h)[which]
            low+=min(prev[0],cur[0])
            up+=max(prev[1],cur[1])
            prev=cur
        unit=F(1,1<<self.precision)
        return h*low*unit,h*up*unit

    def tail(self,T:F):
        m=len(self.kappas)
        d=prod(self.kappas)
        _,root_hi=sqrt_bounds(1/d,self.precision)
        return F(root_hi,1<<self.precision)*(1-1/(T*T))**(-m)*T**(1-2*m)/(2*m-1)


def interval_json(pair):
    return {"lower":str(pair[0]),"upper":str(pair[1]),
            "lower_display":float(pair[0]),"upper_display":float(pair[1])}


def certify(acquisition,beta=F(1),quad_relative=F(1,100),max_grid=131072):
    if not isinstance(beta,F) or beta<=0 or not isinstance(quad_relative,F) or quad_relative<=0:
        raise Unknown("positive exact beta and quadrature tolerance required")
    start=perf_counter()
    ks=[F(k) for k in acquisition["kappa"]]
    m=len(ks)
    p=max(192,4*m+128)
    ii=Integrator(ks,p)
    b=F(1,2)
    T=F(2)
    # Lower mass from a fixed interval; this is used only for a paid tail
    # cutoff, not as an assumed amount of probability at the basin.
    seed=ii.monotone_integral(F(1),F(5,4),32,0)[0]
    while ii.tail(T)>quad_relative*seed/8:
        T*=2
    N=64
    while True:
        left=ii.monotone_integral(b,F(1),N,0)
        right=ii.monotone_integral(F(1),T,N*int(2*(T-1)),0)
        mass=(left[0]+right[0],left[1]+right[1]+ii.tail(T))
        rr=ii.monotone_integral(F(0),b,N,1)
        resistance=(2*rr[0],2*rr[1])
        if mass[0]>0 and resistance[0]>0 and (mass[1]*resistance[1]) <= (1+quad_relative)*(mass[0]*resistance[0]):
            break
        N*=2
        if N>max_grid:
            raise Unknown("quadrature grid budget exhausted")
    factor=1+F(8,9)/beta
    free=(1/(beta*mass[1]*resistance[1]),1/(beta*mass[0]*resistance[0]))
    full=(free[0]/factor,free[1])
    return {"schema":"entropic_capacity.v1","n":m+1,"m":m,
            "beta":str(beta),"b":str(b),"ell":acquisition["ell"],
            "basins":"ell.x <= -b and ell.x >= b", "observable":"cap_mu(A,B)/mu(A)",
            "not_claimed":"arbitrary-state MFPT, fixed-deadline CDF, exact projected Markov dynamics",
            "mass_A_unnormalized":interval_json(mass),
            "resistance":interval_json(resistance),
            "free_energy_rate":interval_json(free),
            "full_diffusion_rate":interval_json(full),
            "universal_factor":str(factor),"cutoff_T":str(T),
            "tail_upper":str(ii.tail(T)),"grid_N":N,"precision_bits":p,
            "exact_point_evaluations":len(ii.cache),"product_factors":ii.product_factors,
            "max_integer_bits":ii.max_integer_bits,"integration_seconds":perf_counter()-start,
            "quad_ratio":float(mass[1]*resistance[1]/(mass[0]*resistance[0]))}


def main():
    reports=[]
    for m in [2,4,16,64,128]:
        raw=sparse_fixture(m)
        acquired=acquire(raw)
        cert=certify(acquired)
        reports.append({"acquisition":acquired,"certificate":cert})
        print(json.dumps({"m":m,"rate":cert["full_diffusion_rate"]["lower_display"],
                          "upper":cert["full_diffusion_rate"]["upper_display"],
                          "N":cert["grid_N"],"points":cert["exact_point_evaluations"],
                          "seconds":cert["integration_seconds"]}),flush=True)
    with open("capacity_results.json","w") as f:
        json.dump(reports,f,indent=2)
    dense=dense_fixture(4)
    with open("dense_raw_input.json","w") as f:
        json.dump(dense,f,indent=2)
    got=acquire(dense)
    with open("dense_acquisition.json","w") as f:
        json.dump(got,f,indent=2)
    print("dense acquisition",got)


if __name__=="__main__":
    main()
