#!/usr/bin/env python3
"""Exact identity controls; no PSD scan and no global theorem certificate."""
import hashlib
import json
import pathlib
import time
import sympy as sp

started = time.perf_counter()
checks = []

def zero(expr, name):
    reduced = sp.simplify(sp.expand(sp.expand_log(sp.expand(expr), force=True)))
    assert reduced == 0, (name, reduced)
    checks.append(name)

def matrix_zero(mat, name):
    for i in range(mat.rows):
        for j in range(mat.cols):
            zero(mat[i, j], f"{name}[{i},{j}]")

I = sp.I
X = sp.Matrix([[0, 1], [1, 0]])
Y = sp.Matrix([[0, -I], [I, 0]])
Z = sp.diag(1, -1)
X4, Y4, Z4 = [sp.kronecker_product(P, sp.eye(2)) for P in [X, Y, Z]]

# A faithful explicit joint state with known eigenbasis. No optimization.
R = sp.Matrix([[sp.Rational(3, 5), -sp.Rational(4, 5)],
               [sp.Rational(4, 5), sp.Rational(3, 5)]])
T = sp.Matrix([[sp.Rational(3, 5), 4*I/5], [4*I/5, sp.Rational(3, 5)]])
U = sp.diag(1, 1, 1, -1) * sp.kronecker_product(R, T)
matrix_zero(U.H*U-sp.eye(4), "joint eigenbasis unitary")
lambdas = [sp.Rational(1, 2), sp.Rational(1, 4), sp.Rational(1, 5), sp.Rational(1, 20)]
zero(sum(lambdas)-1, "faithful density normalization")
rho = (U*sp.diag(*lambdas)*U.H).applyfunc(sp.expand)
q = (U*sp.diag(*[sp.sqrt(p) for p in lambdas])*U.H).applyfunc(sp.expand)
ell = (U*sp.diag(*[sp.log(p) for p in lambdas])*U.H).applyfunc(sp.expand)
matrix_zero(q*q-rho, "actual full square root")
assert rho[:2, 2:] != rho[:2, 2:].H
checks.append("joint off-diagonal block not Hermitian")
assert rho[:2, :2]*rho[2:, 2:] != rho[2:, 2:]*rho[:2, :2]
checks.append("joint diagonal blocks do not commute")

alpha = sp.log(2)
A, B, c, h = 3/(2*sp.sqrt(2)), 1/(2*sp.sqrt(2)), sp.Rational(5, 4), sp.Rational(3, 4)
a = sp.Rational(3, 7)
kap = sp.Symbol("kappa", real=True)
N = X4+a*Z4
V = (a*a+c)*sp.eye(4)-h*Z4+2*a*(B/A)*X4
K = A*X4+I*B*Y4+a*Z4
S = sp.kronecker_product(sp.diag(2**sp.Rational(1, 4), 2**sp.Rational(-1, 4)), sp.eye(2))
D = (S*V*S.inv()).applyfunc(sp.simplify)
matrix_zero((D+D.H)/2-K.H*K, "physical drift Lyapunov identity")
Lrho = ((D*rho+rho*D.H)/2-K*rho*K.H).applyfunc(sp.expand)
zero(sp.trace(Lrho), "physical generator trace annihilation")
J = sp.trace(Lrho*(ell-alpha*Z4))
E = sp.trace(V*rho)-sp.trace(N*q*N*q)
direct = J-kap*E

XX, YY, ZZ = [(U.H*P*U).applyfunc(sp.expand) for P in [X4, Y4, Z4]]
dalpha = 2*alpha*h/c-kap*(1-1/c)
paired = 0
for i in range(4):
    for j in range(i+1, 4):
        p, qlambda = lambdas[i], lambdas[j]
        w = p+qlambda
        beta = sp.log(p/qlambda)/2
        t = (p-qlambda)/w
        m = 2*beta*t
        n = 1-2*sp.sqrt(p*qlambda)/w
        P = h*beta+(alpha*c-kap*h/2)*t
        Q = 2*B*beta+(alpha-kap*B)/A*t
        M = sp.Matrix([[A*A*m-kap*n+B*B*dalpha, -P, A*m-kap*n],
                       [-P, B*B*m+A*A*dalpha, -Q],
                       [A*m-kap*n, -Q, m-kap*n]])
        v = sp.Matrix([XX[i,j], I*YY[i,j], a*ZZ[i,j]])
        paired += w*(v.H*M*v)[0]
remainder = dalpha*sum(lambdas[i]*(B*B*abs(XX[i,i])**2+A*A*abs(YY[i,i])**2) for i in range(4))
zero(direct-paired-remainder, "full physical J-kappa E equals spectral kernel identity")

# Independent exact cross orientations from the full Pauli products.
cross_xy = sum((lambdas[i]-lambdas[j])*sp.im(sp.conjugate(XX[i,j])*YY[i,j])
               for i in range(4) for j in range(i+1,4))
cross_zy = sum((lambdas[i]-lambdas[j])*sp.im(sp.conjugate(ZZ[i,j])*YY[i,j])
               for i in range(4) for j in range(i+1,4))
zero(cross_xy+sp.trace(rho*Z4), "XY commutator orientation")
zero(cross_zy-sp.trace(rho*X4), "ZY commutator orientation")

root = pathlib.Path(__file__).resolve().parent
result = {"status": "PASS", "purpose": "exact identity controls only; kernel PSD unproved",
          "checks": len(checks), "check_names": checks,
          "elapsed_seconds": time.perf_counter()-started,
          "invocation": "python3 work/agents/tensor_frame_sol/cycle08_complete_qubit/check_independent_spectral_kernel_fast.py",
          "sympy_version": sp.__version__,
          "script_sha256": hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()}
(root/"independent_spectral_kernel_fast_checks.json").write_text(json.dumps(result, indent=2)+"\n")
print(json.dumps({k: result[k] for k in ["status", "checks", "elapsed_seconds", "purpose"]}))
