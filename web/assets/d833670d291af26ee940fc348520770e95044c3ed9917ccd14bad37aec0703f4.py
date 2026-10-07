"""Owned exact arithmetic checks; ten-second hard cap; no peer code."""
from fractions import Fraction as F
from math import comb, factorial
from itertools import permutations
from pathlib import Path
import json, hashlib, signal, time
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent
COUNT = 0


def timeout(_signum, _frame):
    raise TimeoutError("admitted ten-second campaign cap")


def check(condition, message):
    global COUNT
    COUNT += 1
    if not condition:
        raise AssertionError(message)


def trim(p):
    p = list(p)
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p


def add(*ps):
    out = [F(0)] * max(map(len, ps))
    for p in ps:
        for i, c in enumerate(p):
            out[i] += c
    return trim(out)


def scale(p, s):
    return trim([s * c for c in p])


def mul(p, q):
    out = [F(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            out[i + j] += a * b
    return trim(out)


def deriv(p):
    return trim([i * p[i] for i in range(1, len(p))] or [F(0)])


def value(p, x):
    ans = F(0)
    for c in reversed(p):
        ans = ans * x + c
    return ans


def bernstein(K, r):
    if not 0 <= r <= K:
        return [F(0)]
    return [F(0)] * r + [F(comb(K, r) * comb(K-r, j) * (-1)**j)
                            for j in range(K-r+1)]


def coefficients(K, nu):
    return [nu, -K-2*nu, F(K-1)], [F(0), nu, 1-nu, F(-1)]


def apply_L(p, a, D):
    return add(mul(a, deriv(p)), mul(D, deriv(deriv(p))))


def zero(n):
    return [[F(0) for _ in range(n)] for _ in range(n)]


def transpose(A):
    return [list(row) for row in zip(*A)]


def mm(A, B):
    C = zero(len(A))
    for i, row in enumerate(A):
        for k, a in enumerate(row):
            if a:
                for j, b in enumerate(B[k]):
                    if b:
                        C[i][j] += a*b
    return C


def ms(A, a):
    return [[a*x for x in row] for row in A]


def ma(*As):
    return [[sum(A[i][j] for A in As) for j in range(len(As[0]))]
            for i in range(len(As[0]))]


def kron(A, B):
    return [[a*b for a in rowA for b in rowB] for rowA in A for rowB in B]


def jm(N):
    A = zero(2**N)
    for r in range(2**N):
        for k in range(N):
            if r & (1 << k):
                A[r ^ (1 << k)][r] += 1
    return A


def dicke(N, r):
    A = zero(2**N)
    inds = [i for i in range(2**N) if i.bit_count() == r]
    for i in inds:
        for j in inds:
            A[i][j] = F(1, comb(N, r))
    return A


def diss(L, rho):
    Lt = transpose(L)
    H = mm(Lt, L)
    return ma(mm(mm(L, rho), Lt), ms(mm(H, rho), F(-1, 2)),
              ms(mm(rho, H), F(-1, 2)))


def permuted(rho, perm):
    N = len(perm)
    mapping = [sum(((i >> perm[j]) & 1) << j for j in range(N))
               for i in range(2**N)]
    A = zero(2**N)
    for i in range(2**N):
        for j in range(2**N):
            A[mapping[i]][mapping[j]] = rho[i][j]
    return A


def density_integral(K, p, nu):
    # Shift y=nu+x; every power has exponent <=-2, so there is no log.
    out = F(0)
    for t, c in enumerate(p):
        if not c:
            continue
        for j in range(t+1):
            power = j-K-1
            out += c*comb(t, j)*(-nu)**(t-j) * (
                (nu+1)**power - nu**power) / power
    return out


def campaign():
    nus = [F(0), F(1, 7), F(1), F(3), F(17, 4), F(101)]
    bernstein_cases = moment_cases = factorial_cases = 0
    for K in range(1, 21):
        for nu in nus:
            a, D = coefficients(K, nu)
            check(value(D, F(0)) == value(D, F(1)) == 0, "diffusion endpoints")
            check(value(a, F(0)) == nu and value(a, F(1)) == -nu-1,
                  "inward drift endpoints")
            for r in range(K+1):
                p = bernstein(K, r)
                rhs = add(scale(bernstein(K, r+1), (nu+1)*(r+1)*(K-r)),
                          scale(bernstein(K, r-1), nu*r*(K-r+1)),
                          scale(p, -(nu+1)*r*(K-r+1)-nu*(r+1)*(K-r)))
                check(apply_L(p, a, D) == rhs, "Bernstein forward chain")
                bernstein_cases += 1
            for ell in range(K+1):
                p = [F(0)]*ell + [F(1)]
                rhs = [F(0)]*(ell+2)
                if ell:
                    rhs[ell-1] = nu*ell**2
                    rhs[ell] = -ell*(K-ell+1+nu*(ell+1))
                    rhs[ell+1] = ell*(K-ell)
                check(apply_L(p, a, D) == trim(rhs), "ordinary moment generator")
                if ell == K:
                    check(len(apply_L(p, a, D)) <= K+1, "degree-K closure")
                moment_cases += 1
                vals = [F(comb(r, ell), comb(K, ell)) if r >= ell else F(0)
                        for r in range(K+1)]
                for r in range(K+1):
                    lhs = F(0)
                    if r < K:
                        lhs += nu*(r+1)*(K-r)*(vals[r+1]-vals[r])
                    if r:
                        lhs += (nu+1)*r*(K-r+1)*(vals[r-1]-vals[r])
                    rhsval = F(0)
                    if ell:
                        lower = F(comb(r, ell-1), comb(K, ell-1)) if r >= ell-1 else F(0)
                        upper = F(comb(r, ell+1), comb(K, ell+1)) if ell < K and r >= ell+1 else F(0)
                        rhsval = nu*ell**2*lower - ell*(K-ell+1+nu*(ell+1))*vals[r] + ell*(K-ell)*upper
                    check(lhs == rhsval, "finite chain factorial normalization")
                    factorial_cases += 1

    grid_cases = 0
    for K in range(1, 9):
        for nu in [F(0), F(1, 7), F(3)]:
            a, D = coefficients(K, nu)
            Amax, Dmax = nu+1+F(K-1, 4), (nu+1)/4
            for M in [1, 2, 3, 7]:
                h = F(1, M)
                for i in range(M+1):
                    x = i*h
                    aa, dd = value(a, x), value(D, x)
                    qp = dd/h**2 + max(aa, 0)/h
                    qm = dd/h**2 + max(-aa, 0)/h
                    check(qp >= 0 and qm >= 0, "positive grid rates")
                    check((i != 0 or qm == 0) and (i != M or qp == 0), "zero outward rate")
                    for ell in range(K+1):
                        p = [F(0)]*ell+[F(1)]
                        gh = F(0)
                        if i < M:
                            gh += qp*((x+h)**ell-x**ell)
                        if i:
                            gh += qm*((x-h)**ell-x**ell)
                        f2 = ell*(ell-1) if ell >= 2 else 0
                        f4 = ell*(ell-1)*(ell-2)*(ell-3) if ell >= 4 else 0
                        bound = Amax*f2*h/2 + Dmax*f4*h**2/12
                        check(abs(gh-value(apply_L(p, a, D), x)) <= bound, "uniform polynomial grid remainder")
                        grid_cases += 1

    full_matrix_cases = 0
    for N in range(1, 5):
        L = jm(N)
        for r in range(N+1):
            rho = dicke(N, r)
            dminus, dplus = diss(L, rho), diss(transpose(L), rho)
            down = ma(ms(dicke(N, r-1), r*(N-r+1)), ms(rho, -r*(N-r+1))) if r else zero(2**N)
            up = ma(ms(dicke(N, r+1), (r+1)*(N-r)), ms(rho, -(r+1)*(N-r))) if r < N else zero(2**N)
            check(dminus == down and dplus == up, "full matrix standard Lindblad rate")
            for nu in nus:
                check(ma(ms(dminus, nu+1), ms(dplus, nu)) == ma(ms(down, nu+1), ms(up, nu)), "full thermal Lindblad factor")
                full_matrix_cases += 1

    pair_cases = 0
    singlet = zero(4)
    singlet[1][1] = singlet[2][2] = F(1, 2)
    singlet[1][2] = singlet[2][1] = F(-1, 2)
    for N in range(2, 5):
        for b in range(1, N//2+1):
            K = N-2*b
            P = [[F(1)]]
            for _ in range(b):
                P = kron(P, singlet)
            LN, LK = jm(N), jm(K)
            for r in range(K+1):
                rho = dicke(K, r)
                embedded = kron(P, rho)
                check(diss(LN, embedded) == kron(P, diss(LK, rho)), "singlet collective lowering decoupling")
                check(diss(transpose(LN), embedded) == kron(P, diss(transpose(LK), rho)), "singlet collective raising decoupling")
                twirl = zero(2**N)
                for perm in permutations(range(N)):
                    twirl = ma(twirl, permuted(embedded, perm))
                twirl = ms(twirl, F(1, factorial(N)))
                check(sum(twirl[i][i] for i in range(2**N)) == 1, "pair twirl normalization")
                for j in range(N-1):
                    p = list(range(N))
                    p[j], p[j+1] = p[j+1], p[j]
                    check(permuted(twirl, p) == twirl, "Schur twirl permutation invariance")
                Jz = zero(2**N)
                for i in range(2**N):
                    Jz[i][i] = F(2*i.bit_count()-N, 2)
                J2 = ma(mm(Jz, Jz), ms(mm(transpose(LN), LN), F(1, 2)), ms(mm(LN, transpose(LN)), F(1, 2)))
                jval = F(K, 2)
                check(mm(J2, twirl) == ms(twirl, jval*(jval+1)), "twirl fixed total-spin support")
                pair_cases += 1

    stationary_cases = 0
    for K in range(1, 11):
        for nu in [F(1, 7), F(1), F(3), F(17, 4)]:
            Z = density_integral(K, [F(1)], nu)
            z = nu/(nu+1)
            S = sum(z**r for r in range(K+1))
            for r in range(K+1):
                p = density_integral(K, bernstein(K, r), nu)/Z
                check(p == z**r/S, "diffusion geometric stationary populations")
                stationary_cases += 1

    a, D = coefficients(2, F(1))
    p = bernstein(2, 0)
    correct = value(apply_L(p, a, D), F(1, 2))
    wrong = value(add(mul(a, deriv(p)), scale(mul(D, deriv(deriv(p))), F(1, 2))), F(1, 2))
    check(correct != wrong, "wrong sqrt(Gamma D) factor control must fail")
    return {
        "bernstein_polynomial_cases": bernstein_cases,
        "ordinary_moment_cases": moment_cases,
        "finite_chain_factorial_cases": factorial_cases,
        "positive_grid_consistency_cases": grid_cases,
        "full_matrix_thermal_cases": full_matrix_cases,
        "singlet_embedding_twirl_cases": pair_cases,
        "stationary_density_population_cases": stationary_cases,
        "wrong_noise_factor_control": {"correct": str(correct), "wrong": str(wrong), "status": "FAILS as intended"},
    }


if __name__ == "__main__":
    signal.signal(signal.SIGALRM, timeout)
    signal.alarm(10)
    started = time.perf_counter()
    result = {"status": "ACTIVE"}
    try:
        result.update(campaign())
        result["status"] = "PASS"
    except BaseException as exc:
        result.update(status="FAIL", error=f"{type(exc).__name__}: {exc}")
    finally:
        signal.alarm(0)
        result.update(counted_exact_checks=COUNT, elapsed_seconds=time.perf_counter()-started,
                      hard_seconds_cap=10, utc=datetime.now(timezone.utc).isoformat(),
                      script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                      scope="finite exact algebra/matrix/grid/embedding checks; not all-time integration, compiler execution, or hardware")
        (HERE / "exact_thermal_checks.json").write_text(json.dumps(result, indent=2)+"\n")
        print(json.dumps(result, indent=2))
    if result["status"] != "PASS":
        raise SystemExit(1)
