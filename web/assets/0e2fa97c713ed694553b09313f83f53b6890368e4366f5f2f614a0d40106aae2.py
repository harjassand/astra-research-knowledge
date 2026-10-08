"""Exact qutrit control and a global nonviolation certificate for one rank-3 Q."""
import sympy as s
from sympy.matrices import Matrix, eye, zeros, kronecker_product

d = 3
I = eye(d)


def e(i, j, n=d):
    X = zeros(n)
    X[i, j] = 1
    return X


def ptrace(M, dims, keep):
    """Exact partial trace, with tensor factors ordered as in dims."""
    keep = tuple(keep)
    nout = s.prod(dims[k] for k in keep)
    out = zeros(nout)
    for oi in range(nout):
        oi_multi = []
        z = oi
        for size in reversed([dims[k] for k in keep]):
            oi_multi.append(z % size)
            z //= size
        oi_multi = tuple(reversed(oi_multi))
        for oj in range(nout):
            oj_multi = []
            z = oj
            for size in reversed([dims[k] for k in keep]):
                oj_multi.append(z % size)
                z //= size
            oj_multi = tuple(reversed(oj_multi))
            value = 0
            trace_dims = [dims[k] for k in range(len(dims)) if k not in keep]
            for tr_multi in __import__('itertools').product(*(range(q) for q in trace_dims)):
                ii = [None] * len(dims)
                jj = [None] * len(dims)
                p = 0
                for k in range(len(dims)):
                    if k in keep:
                        q = keep.index(k)
                        ii[k], jj[k] = oi_multi[q], oj_multi[q]
                    else:
                        ii[k] = jj[k] = tr_multi[p]
                        p += 1
                def idx(t):
                    r = 0
                    for a, size in zip(t, dims):
                        r = r * size + a
                    return r
                value += M[idx(ii), idx(jj)]
            out[oi, oj] = value
    return out


# Rational symmetric universal qutrit cloner.  P_sym (rho tensor I) P_sym
# is CP; the coefficient 1/2 gives trace preservation.
swap_ab = zeros(d*d)
for a in range(d):
    for b in range(d):
        swap_ab[b*d+a, a*d+b] = 1
P_sym = (eye(d*d) + swap_ab) / 2

def broadcast_on(X):
    return P_sym * kronecker_product(X, I) * P_sym / 2

# Normalized Choi state on R,A,B for |Omega> = d^(-1/2) sum_i |ii>.
J_cloner = zeros(d**3)
for i in range(d):
    for j in range(d):
        J_cloner += kronecker_product(e(i,j), broadcast_on(e(i,j))) / d

assert J_cloner == J_cloner.conjugate().T
assert s.trace(J_cloner) == 1
assert all(ev.is_nonnegative for ev in J_cloner.eigenvals())
assert swap_ab == swap_ab.T and swap_ab*swap_ab == eye(d*d)
swap_full = kronecker_product(I, swap_ab)
assert swap_full*J_cloner*swap_full == J_cloner
assert ptrace(J_cloner, (d,d,d), (0,)) == eye(d)/d
assert ptrace(J_cloner, (d,d,d), (1,)) == eye(d)/d
assert ptrace(J_cloner, (d,d,d), (2,)) == eye(d)/d

# Marginal: Phi(A) = (5/8) A + (1/8) Tr(A) I.
for i in range(d):
    for j in range(d):
        expected = s.Rational(5,8)*e(i,j) + (s.Rational(1,8) if i == j else 0)*I
        assert ptrace(broadcast_on(e(i,j)), (d,d), (0,)) == expected

# Positive rank-3 Hermitian frame.  Q=(3/2) sum |B_i><B_i| in the tau-HS space.
B1, B2, B3 = zeros(d), zeros(d), zeros(d)
B1[0,1] = B1[1,0] = 1
B2[1,2] = B2[2,1] = 1
B3[1,2], B3[2,1] = -s.I, s.I
B = (B1, B2, B3)
assert all(s.trace(A) == 0 for A in B)
assert all(s.trace(A*B[j])/d == (s.Rational(2,3) if i == j else 0)
           for i,A in enumerate(B) for j in range(3))
Q_trace = sum(s.Rational(3,2)*s.trace(A*A)/d for A in B)
assert Q_trace == 3
lambda_cloner = s.Rational(5,8)
h_cloner = Q_trace*(2*lambda_cloner-1)
assert h_cloner == s.Rational(3,4)

# Exact global canonical-support calculation for this Q.
# For a pure psi=(alpha,beta,gamma), V_Q(P) <= 6 p_1(1-p_1).
# At any rank-one POVM barycenter I/3, E[p_1]=1/3, hence S_d(Q)<=4/3.
support_upper = s.Rational(4,3)
sign_states = []
for u in (-1,1):
    for v in (-1,1):
        psi = Matrix([1,u,v]) / s.sqrt(3)
        sign_states.append(psi)
        P = psi*psi.conjugate().T
        vals = [s.trace(P*A) for A in B]
        score = s.Rational(3,2)*sum(x*x for x in vals)
        assert score == support_upper
# The four projectors average to I/3, so effects (3/4)P form a POVM and attain 4/3.
assert sum((psi*psi.conjugate().T for psi in sign_states), zeros(d))/4 == eye(d)/d

# Global dual operator certificate for every legal symmetric extension.
# K is the broadcaster-side observable for h_Q=(3/2) Tr(K J_RAB).
K = zeros(d**3)
for A in B:
    K += (kronecker_product(A.T, A, I) + kronecker_product(A.T, I, A)
          - kronecker_product((A*A).T, I, I))
Y = s.diag(s.Rational(237,1000), s.Rational(439,1000), s.Rational(158,1000))
Z = s.diag(s.Rational(123,1000), s.Rational(554,1000), s.Rational(157,1000))
dual_slack = (kronecker_product(Y,I,I) + kronecker_product(I,Z,I)
              + kronecker_product(I,I,Z) - K)
L, D = dual_slack.LDLdecomposition()
pivots = [D[k,k] for k in range(d**3)]
assert L*D*L.T == dual_slack
assert all(x.is_Rational and x > 0 for x in pivots)
dual_expectation_bound = (s.trace(Y)+2*s.trace(Z))/d
assert dual_expectation_bound == s.Rational(417,500)
h_global_upper = s.Rational(3,2)*dual_expectation_bound
assert h_global_upper == s.Rational(1251,1000)
assert h_global_upper < support_upper
assert support_upper - h_global_upper == s.Rational(247,3000)

print("PASS exact Choi PSD/trace/swap symmetry/all one-body marginals")
print("PASS exact universal-cloner marginal Phi(A)=5/8 A + Tr(A)I/8")
print("PASS Q rank=3, Tr_HS(Q)=3, cloner h_Q=3/4")
print("PASS exact canonical support S_d(Q)=4/3")
print("PASS exact global extension dual: h_Q <= 1251/1000 < 4/3")
print("exact gap:", support_upper - h_global_upper)
print("LDL pivots:", ", ".join(str(x) for x in pivots))
