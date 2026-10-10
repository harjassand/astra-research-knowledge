"""Small exact identity check for the independent review; not an ODE benchmark."""
import json
import sympy as sp

t = sp.symbols("t", real=True)
I2 = sp.eye(2)
A = sp.Matrix([[t, 1], [1, -t]])
P = (I2 + A / sp.sqrt(1 + t * t)) / 2
order = 5

def coefficient(M, k):
    return M.applyfunc(lambda v: sp.diff(v, t, k).subs(t, 0) / sp.factorial(k))

def zero(M):
    return all(sp.simplify(v) == 0 for v in M)

As = [coefficient(A, k) for k in range(order + 1)]
Ps = [coefficient(P, k) for k in range(order + 1)]
P0, A0 = Ps[0], As[0]
Q0 = I2 - P0

def off(X):
    return P0 * X * Q0 + Q0 * X * P0

def linear_map(X):
    return P0 * X * P0 + Q0 * X * Q0 + off(A0 * X - X * A0)

basis = []
for i in range(2):
    for j in range(2):
        E = sp.zeros(2)
        E[i, j] = 1
        basis.append(E)

def vec(M):
    return sp.Matrix(list(M))

L = sp.Matrix.hstack(*(vec(linear_map(E)) for E in basis))
computed = [P0]
checks = []
for k in range(1, order + 1):
    Sk = sum((computed[j] * computed[k - j] for j in range(1, k)), sp.zeros(2))
    Rk = -sum((As[j] * computed[k - j] - computed[k - j] * As[j]
               for j in range(1, k + 1)), sp.zeros(2))
    Dk = -P0 * Sk * P0 + Q0 * Sk * Q0
    rhs = Dk + off(Rk)
    Xk = sp.Matrix(2, 2, list(L.inv() * vec(rhs)))
    computed.append(Xk)
    checks.append(zero(Xk - Ps[k]))

Q = I2 - P
K = sp.I * (sp.diff(P, t) * P + sp.diff(Q, t) * Q)
intertwining = zero(K * P - P * K - sp.I * sp.diff(P, t))
hermitian = zero(K - K.conjugate().T)
result = {
    "model": "H(t)=[[t,1],[1,-t]], positive projector, center 0",
    "ambient_operator_dimension": 4,
    "ambient_operator_squared_singular_values": [str(x) for x in (L.T * L).eigenvals().keys()],
    "jet_orders_checked": order,
    "jet_coefficient_equalities": checks,
    "connection_intertwining_sign": intertwining,
    "connection_hermitian_on_real_axis": hermitian,
    "all_passed": all(checks) and intertwining and hermitian,
    "scope": "Exact symbolic identities only; no propagation implementation or performance claim."
}
print(json.dumps(result, indent=2))
assert result["all_passed"]
