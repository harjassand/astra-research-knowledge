"""Exact sparse primal/dual GMRES certificate for a nonreversible local chain.

All arithmetic determining intervals is integer/Fraction arithmetic. Float
fields are descriptive only. No full matrix is assembled by certify().
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import json
import math
import platform
import resource
import sys
import time

sys.dont_write_bytecode = True


def box(x):
    x = F(x)
    return {"num_hex": hex(x.numerator), "den_hex": hex(x.denominator),
            "num_bits": abs(x.numerator).bit_length(),
            "den_bits": x.denominator.bit_length(), "approx": float(x)}


def unbox(d):
    return F(int(d["num_hex"], 16), int(d["den_hex"], 16))


def solve(matrix, rhs):
    """Exact elimination; only small GMRES normal matrices here."""
    n = len(rhs)
    a = [list(map(F, row)) + [F(b)] for row, b in zip(matrix, rhs)]
    for j in range(n):
        pivot = next((i for i in range(j, n) if a[i][j]), None)
        if pivot is None:
            raise ValueError("Dependent Krylov vectors; no silent inversion")
        a[j], a[pivot] = a[pivot], a[j]
        v = a[j][j]
        a[j] = [x / v for x in a[j]]
        for i in range(n):
            if i != j and a[i][j]:
                v = a[i][j]
                a[i] = [x - v * y for x, y in zip(a[i], a[j])]
    ans = [row[-1] for row in a]
    assert all(sum((F(x) * y for x, y in zip(row, ans)), F(0)) == b
               for row, b in zip(matrix, rhs))
    return ans


def sqrt_upper(q, bits=256):
    """Smallest dyadic multiple of 2^-bits >= sqrt(q), exactly."""
    q = F(q)
    if q < 0:
        raise ValueError("Negative square-root argument")
    target = q.numerator << (2 * bits)
    t = math.isqrt(target // q.denominator)
    if t * t * q.denominator < target:
        t += 1
    ans = F(t, 1 << bits)
    assert ans * ans >= q
    if t:
        assert F(t - 1, 1 << bits) ** 2 < q
    return ans


class Operator:
    """Independent single-spin heat baths plus all adjacent directed cycles.

    Low pair bit is i, high bit is i+1. Semantic cycle (x_i,x_j):
    00 -> 10 -> 11 -> 01 -> 00. A=D*(-Q), inner weights are W*w.
    """
    successor = (1, 3, 0, 2)
    predecessor = (2, 0, 3, 1)

    def __init__(self, n, theta=F(1, 4), gamma=F(1, 2)):
        if type(n) is not int or n < 2:
            raise ValueError("Integer n >= 2 required")
        if type(theta) not in (int, F) or type(gamma) not in (int, F):
            raise TypeError("Exact rational parameters required")
        self.n, self.theta, self.gamma = n, F(theta), F(gamma)
        if not 0 < self.theta < 1 or self.gamma < 0:
            raise ValueError("0 < theta < 1 and gamma >= 0 required")
        theta, gamma = self.theta, self.gamma
        self.a, self.b = 0, (1 << n) - 1
        self.W, self.N = theta.denominator ** n, theta.numerator ** n
        self.rho = F(self.N, self.W)
        self.weights = [theta.numerator ** j * theta.denominator ** (n-j)
                        for j in range(n+1)]
        self.spin_rational = [theta/(1+theta), 1/(1+theta)]
        self.cycle_rational = [gamma*theta**2, gamma*theta,
                               gamma*theta, gamma]
        self.D = math.lcm(*(q.denominator for q in
                            self.spin_rational + self.cycle_rational))
        self.spin = [int(self.D*q) for q in self.spin_rational]
        self.cycle = [int(self.D*q) for q in self.cycle_rational]
        assert all(q*self.D == k for q, k in
                   zip(self.spin_rational+self.cycle_rational,
                       self.spin+self.cycle))
        self.Ra = n*self.spin_rational[0] + (n-1)*self.cycle_rational[0]
        self.Rmax = n*self.spin_rational[1] + (n-1)*gamma
        self.gap = F(1)
        self.local_terms = {"primal": 0, "dual": 0}
        self.scatter_updates = {"primal": 0, "dual": 0}
        self.applications = {"primal": 0, "dual": 0}

    def weight(self, x):
        return self.weights[x.bit_count()]

    def inner(self, v, z):
        if len(v) > len(z):
            v, z = z, v
        return sum(self.weight(x)*value*z.get(x, 0) for x, value in v.items())

    def apply(self, vector, adjoint=False):
        """Full backward A or weighted-adjoint A* on finite support.

        Scatter from f(x) uses ALL predecessor states and incoming rates.
        For A* these predecessors are reversed. This is not forward law
        propagation. Stationarity keeps the adjoint diagonal unchanged.
        """
        direction = "dual" if adjoint else "primal"
        sources = self.successor if adjoint else self.predecessor
        out = {}
        n = self.n
        for x, value in vector.items():
            if not value:
                continue
            ones = x.bit_count()
            diagonal = (n-ones)*self.spin[0] + ones*self.spin[1]
            for i in range(n):
                bit = (x >> i) & 1
                y = x ^ (1 << i)
                out[y] = out.get(y, 0) - self.spin[1-bit]*value
            for i in range(n-1):
                pair = (x >> i) & 3
                source_pair = sources[pair]
                y = x ^ ((pair ^ source_pair) << i)
                diagonal += self.cycle[pair]
                out[y] = out.get(y, 0) - self.cycle[source_pair]*value
            out[x] = out.get(x, 0) + diagonal*value
        self.applications[direction] += 1
        self.local_terms[direction] += len(vector)*(2*n-1)
        self.scatter_updates[direction] += len(vector)*(2*n)
        out = {x: v for x, v in out.items() if v}
        assert sum(self.weight(x)*v for x, v in out.items()) == 0
        return out

    def support(self, v, degree):
        max_distance = max(min(x.bit_count(), self.n-x.bit_count()) for x in v)
        assert max_distance <= degree
        ball_bound = min(1 << self.n,
                         2*sum(math.comb(self.n,j) for j in range(degree+1)))
        return {"nonzeros": len(v), "degree": degree,
                "largest_distance_from_a_or_b": max_distance,
                "two_ball_upper_bound": ball_bound,
                "largest_value_bits": max(abs(q).bit_length() for q in v.values())}


def gram(op, vectors):
    return [[op.inner(v, z) for z in vectors] for v in vectors]


def coefficients_and_residual(g, k):
    # Exact weighted least squares, equivalent to unrestarted GMRES.
    matrix = [[g[i+1][j+1] for j in range(k)] for i in range(k)]
    rhs = [g[i+1][0] for i in range(k)]
    alpha = solve(matrix, rhs)
    beta = [F(1)] + [-x for x in alpha]
    norm2 = sum((beta[i]*beta[j]*g[i][j]
                 for i in range(k+1) for j in range(k+1)), F(0))
    assert norm2 >= 0
    return alpha, norm2


def at_degree(op, primal, dual, k):
    gp, gd = gram(op, primal), gram(op, dual)
    cross = [[op.inner(z, v) for v in primal] for z in dual]
    alpha, r2 = coefficients_and_residual(gp, k)
    beta, s2 = coefficients_and_residual(gd, k)
    uy = sum((alpha[j]*gp[0][j] for j in range(k)), F(0))
    zr = sum((beta[i]*(cross[i][0] - sum(
              (alpha[j]*cross[i][j+1] for j in range(k)), F(0)))
              for i in range(k)), F(0))
    scale = op.W**2 * op.N
    estimate = op.D*(uy+zr)/scale
    radicand = r2*s2/(scale*op.gap)**2
    radius = sqrt_upper(radicand)
    return {"estimate": estimate, "radius": radius, "radicand": radicand,
            "alpha": alpha, "beta": beta, "r2": r2, "s2": s2,
            "gram_primal": gp, "gram_dual": gd, "cross": cross}


def certify(n, theta=F(1,4), gamma=F(1,2), epsilon=F(1,1000),
            degree_cap=3, progress=True, return_internal=False):
    started = time.perf_counter()
    if type(epsilon) not in (int,F):
        raise TypeError("Exact rational epsilon required")
    epsilon = F(epsilon)
    op = Operator(n, theta, gamma)
    if not 0 < epsilon < 1 or type(degree_cap) is not int or degree_cap < 1:
        raise ValueError("0 < epsilon < 1 and positive integer degree cap required")
    primal = [{op.a: op.N, op.b: -op.W}]
    dual = [dict(primal[0])]
    scale = op.W**2 * op.N
    assert op.inner(primal[0],primal[0]) == scale*(1+op.rho)
    mu = op.gap*(1+op.rho)/(4*op.Rmax**2)
    lo, hi = mu, (1+op.rho)/op.gap
    records = []
    for k in range(1, degree_cap+1):
        primal.append(op.apply(primal[-1]))
        dual.append(op.apply(dual[-1], adjoint=True))
        data = at_degree(op, primal, dual, k)
        raw_lo = data["estimate"]-data["radius"]
        raw_hi = data["estimate"]+data["radius"]
        lo, hi = max(lo, raw_lo), min(hi, raw_hi)
        assert 0 < lo <= hi
        plo, phi = op.rho/(op.Ra*hi), op.rho/(op.Ra*lo)
        moment_bits = max(abs(g).bit_length() for key in
            ("gram_primal", "gram_dual", "cross") for row in data[key] for g in row)
        coeffs = data["alpha"] + data["beta"]
        record = {"degree": k, "I_lower": box(lo), "I_upper": box(hi),
            "estimate": box(data["estimate"]), "radius": box(data["radius"]),
            "radius_squared_exact": box(data["radicand"]),
            "p_lower": box(plo), "p_upper": box(phi),
            "relative_width": float(hi/lo-1),
            "primal_support": op.support(primal[-1],k),
            "dual_support": op.support(dual[-1],k),
            "primal_residual_norm2_scaled": box(data["r2"]),
            "dual_residual_norm2_scaled": box(data["s2"]),
            "primal_coefficients": [box(x) for x in data["alpha"]],
            "dual_coefficients": [box(x) for x in data["beta"]],
            "moment_largest_bits": moment_bits,
            "coefficient_largest_numerator_bits": max(abs(x.numerator).bit_length() for x in coeffs),
            "coefficient_largest_denominator_bits": max(x.denominator.bit_length() for x in coeffs),
            "local_term_evaluations": dict(op.local_terms),
            "scatter_updates": dict(op.scatter_updates),
            "seconds": time.perf_counter()-started}
        records.append(record)
        if progress:
            print(json.dumps({"n":n,"degree":k,"relative_width":record["relative_width"],
                    "support_each":len(primal[-1]),"seconds":record["seconds"]}), flush=True)
        if hi/lo <= 1+epsilon:
            break
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    rss_bytes = rss if platform.system()=="Darwin" else 1024*rss
    result = {"status": "TARGET_MET" if hi/lo <= 1+epsilon else "CERTIFIED_BUT_TARGET_NOT_MET",
        "method":"ordinary exact weighted GMRES plus primal/dual coercivity residual",
        "n":n, "theta":str(op.theta), "gamma":str(op.gamma),
        "epsilon":str(epsilon), "degree_cap":degree_cap, "degree":k,
        "full_state_count":str(1 << n), "rho":box(op.rho),
        "R_a":box(op.Ra), "Rmax":box(op.Rmax), "symmetric_gap_lower":box(op.gap),
        "positive_I_lower_prior":box(mu), "I_lower":box(lo), "I_upper":box(hi),
        "p_lower":box(plo), "p_upper":box(phi),
        "relative_width":float(hi/lo-1), "degrees":records,
        "rate_scale_D":str(op.D), "rate_scale_bits":op.D.bit_length(),
        "weight_scale_W_bits":op.W.bit_length(), "source_N_bits":op.N.bit_length(),
        "input_rate_maximum_bits":max(q.bit_length() for q in op.spin+op.cycle),
        "operator_applications":dict(op.applications),
        "local_term_evaluations":dict(op.local_terms), "scatter_updates":dict(op.scatter_updates),
        "stored_vector_entries":sum(map(len,primal))+sum(map(len,dual)),
        "peak_process_RSS_bytes":rss_bytes, "seconds":time.perf_counter()-started,
        "python":sys.version, "platform":platform.platform(),
        "scope":"Supplied exact rational nonreversible model and proved symmetric gap. No physical validation, new rarity class, priority or practical advantage asserted."}
    return (result,(op,primal,dual,data)) if return_internal else result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, required=True)
    parser.add_argument("--theta", type=F, default=F(1,4))
    parser.add_argument("--gamma", type=F, default=F(1,2))
    parser.add_argument("--epsilon", type=F, default=F(1,1000))
    parser.add_argument("--degree-cap", type=int, default=3)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = certify(args.n,args.theta,args.gamma,args.epsilon,args.degree_cap)
    args.output.write_text(json.dumps(result,indent=2)+"\n")
    print(result["status"],result["p_lower"]["approx"],result["p_upper"]["approx"],flush=True)
