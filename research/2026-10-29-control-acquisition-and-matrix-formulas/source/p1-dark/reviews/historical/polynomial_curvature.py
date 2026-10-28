"""Exact global control bounds from an acquired polynomial's curvature.

Floating-point optimization and eigenvalues propose commands and a bound.
Rational matrix checks and polynomial evaluations alone certify the result.
No physical source or source gradient is queried here.
"""
from fractions import Fraction as F
from math import factorial, prod
import numpy as np
from scipy.optimize import minimize
import simplex_law as sl
import hypograph_control as hc


def increment(alpha, *indices):
    out = list(alpha)
    for i in indices:
        out[i] += 1
    return tuple(out)


def positive_definite(matrix):
    """Exact Schur elimination; return strictly positive pivots or None."""
    a = [list(row) for row in matrix]
    pivots = []
    for j in range(len(a)):
        pivot = a[j][j]
        if pivot <= 0:
            return None
        pivots.append(pivot)
        for i in range(j + 1, len(a)):
            for ell in range(i, len(a)):
                a[i][ell] -= a[i][j] * a[j][ell] / pivot
                a[ell][i] = a[i][ell]
    return pivots


def multinomial(alpha):
    out = factorial(sum(alpha))
    for a in alpha:
        out //= factorial(a)
    return out


class CurvatureLaw:
    def __init__(self, law):
        assert law.k >= 2 and law.bernstein_coefficients is not None
        self.law = law
        self.coefficients = dict(zip(law.alphas, law.bernstein_coefficients))
        self.grad_alphas = list(sl.compositions(law.k - 1, law.n + 1))
        self.hess_alphas = list(sl.compositions(law.k - 2, law.n + 1))
        b = self.coefficients
        self.grad = [
            [F(law.k, 1) / law.delta * (b[increment(a, i + 1)] - b[increment(a, 0)])
             for i in range(law.n)] for a in self.grad_alphas]
        scale = F(law.k * (law.k - 1), 1) / law.delta**2
        self.hess = [
            [[scale * (b[increment(a, i + 1, j + 1)]
                       - b[increment(a, i + 1, 0)]
                       - b[increment(a, 0, j + 1)]
                       + b[increment(a, 0, 0)])
              for j in range(law.n)] for i in range(law.n)]
            for a in self.hess_alphas]
        # A numerical eigenvalue is only a proposal; every matrix is verified.
        eigen_proposal = max(0.0, max(float(np.linalg.eigvalsh(
            np.array([[float(x) for x in row] for row in matrix]))[-1])
            for matrix in self.hess))
        unit = F(1, 1 << 30)
        mu = F(int(np.ceil(eigen_proposal * (1 << 30))) + 1, 1 << 30)
        self.verification_attempts = 0
        self.pivots = None
        for attempt in range(2):
            self.verification_attempts += 1
            pivots = []
            for matrix in self.hess:
                checked = positive_definite([
                    [(mu if i == j else F(0)) - matrix[i][j]
                     for j in range(law.n)] for i in range(law.n)])
                if checked is None:
                    break
                pivots.append(checked)
            if len(pivots) == len(self.hess):
                self.pivots = pivots
                break
            mu = max(F(0), max(matrix[i][i] + sum(abs(matrix[i][j])
                     for j in range(law.n) if j != i)
                     for matrix in self.hess for i in range(law.n))) + unit
        assert self.pivots is not None
        self.mu = mu
        self.float_coeff = np.array([float(x) for x in law.bernstein_coefficients])
        self.float_grad = np.array([[float(x) for x in row] for row in self.grad])
        self.node_exponents = np.array(law.alphas, dtype=int)
        self.grad_exponents = np.array(self.grad_alphas, dtype=int)
        self.node_mult = np.array([multinomial(a) for a in law.alphas], dtype=float)
        self.grad_mult = np.array([multinomial(a) for a in self.grad_alphas], dtype=float)

    def weights(self, u, alphas):
        lam = [1 - sum(u) / self.law.delta] + [x / self.law.delta for x in u]
        return [F(multinomial(a)) * prod(x**p for x, p in zip(lam, a))
                for a in alphas]

    def exact_value_gradient(self, u):
        w = self.weights(u, self.law.alphas)
        wg = self.weights(u, self.grad_alphas)
        p = hc.dot(w, self.law.bernstein_coefficients)
        gradient = [sum((t * row[i] for t, row in zip(wg, self.grad)), F(0))
                    for i in range(self.law.n)]
        return p, gradient

    def float_value_gradient(self, u):
        lam = np.concatenate(([1 - np.sum(u) / float(self.law.delta)],
                              u / float(self.law.delta)))
        w = self.node_mult * np.prod(lam**self.node_exponents, axis=1)
        wg = self.grad_mult * np.prod(lam**self.grad_exponents, axis=1)
        return float(w @ self.float_coeff), wg @ self.float_grad

    def propose(self, prices, initial, utility, bits=20):
        costs = np.array([float(x) for x in prices])
        evaluations = {"value": 0, "gradient": 0}

        def fun(u):
            evaluations["value"] += 1
            p, _ = self.float_value_gradient(u)
            return -(p if utility == "conductance" else -1 / p) + costs @ u

        def jac(u):
            evaluations["gradient"] += 1
            p, gradient = self.float_value_gradient(u)
            return -(gradient if utility == "conductance" else gradient / p**2) + costs

        answer = minimize(fun, np.array([float(x) for x in initial]), jac=jac,
                          method="SLSQP", bounds=[(0, float(self.law.delta))] * self.law.n,
                          constraints={"type": "ineq", "fun": lambda u: float(self.law.delta) - np.sum(u),
                                       "jac": lambda u: -np.ones(self.law.n)},
                          options={"maxiter": 100, "ftol": 1e-12})
        values = [F(str(max(0.0, float(x)))) for x in answer.x]
        if sum(values) > self.law.delta:
            values = [x * self.law.delta / sum(values) for x in values]
        actual = hc.finite_command(values, bits)
        assert all(x >= 0 for x in actual) and sum(actual) <= self.law.delta
        return {"command": actual, "optimizer_success_not_certificate": bool(answer.success),
                "optimizer_message": str(answer.message), "iterations": int(answer.nit),
                "evaluations": evaluations, "source_readings": 0}

    def certificate(self, x, prices, baseline_lower, utility):
        p, gradient = self.exact_value_gradient(x)
        assert p > 0 and all(a >= 0 for a in x) and sum(x) <= self.law.delta
        factor = F(1) if utility == "conductance" else 1 / p**2
        linear = [factor * a - c for a, c in zip(gradient, prices)]
        vertices = [[F(0)] * self.law.n]
        for i in range(self.law.n):
            v = [F(0)] * self.law.n
            v[i] = self.law.delta
            vertices.append(v)
        excess = []
        for v in vertices:
            dx = [a - b for a, b in zip(v, x)]
            excess.append(hc.dot(linear, dx) + factor * self.mu * hc.dot(dx, dx) / 2)
        E = self.law.uniform_bounds()["interpolation_uniform_error"]
        upper = hc.phi(p, utility) - hc.dot(prices, x) + max(excess) + factor * E
        prediction = self.law.predict(x)
        j_lower = max(baseline_lower, prediction["intersection_interval"][0])
        lower = hc.phi(j_lower, utility) - hc.dot(prices, x)
        assert upper >= lower
        return {"command": x, "prices": prices, "utility": utility,
                "polynomial_value": p, "polynomial_gradient": gradient,
                "upper_hessian_bound": self.mu, "vertex_excess": excess,
                "certified_J_lower": j_lower, "objective_lower_without_baseline": lower,
                "global_objective_upper_without_baseline": upper,
                "continuous_simplex_regret": upper - lower,
                "extra_source_readings": 0}
