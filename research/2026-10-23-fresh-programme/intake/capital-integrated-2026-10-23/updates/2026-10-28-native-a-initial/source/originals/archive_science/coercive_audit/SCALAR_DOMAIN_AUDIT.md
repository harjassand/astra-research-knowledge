# Scalar all-order correction: domain audit

27 October 2026. This audits the scalar construction developed by the
gaussian_challenge colleague within the same chat. It is not a value-only
implementation or a historical novelty assertion.

Let gamma be the underlying finite-dimensional Gaussian measure. Let
V=B dot D be a closable derivation with the chain/product rules on a dense
core, B bounded, and Gaussian adjoint

    V* = m - V,       m=X-mu,       Vm=tau.

Suppose m is in L2 and tau is bounded with

    tau=1+R,       ||R||infinity=rho<1.

These conditions hold initially for the scalar source construction
X=h(G)+Z, B=(K(G),1), with bounded weak h', bounded C1 K, and ell<1.
The same conclusions may be obtained first for smooth tame fields and
then by the horizontal energy closure described below.

## 1. The useful form identity

For bounded core S, integration by parts applied to V(m S^2) gives

    E m^2 S^2 = E tau S^2 + 2 E[m S VS].

Consequently

    ||V*S||_2^2 = ||VS||_2^2 + E tau S^2.      (1)

The scalar coercive inverse therefore has the symmetric Dirichlet form

    E[VS VT] + 2 E[tau ST] = -E[RT].         (2)

This is more useful than asserting a Feynman–Kac diffusion without proving
that the degenerate diffusion is complete. Equation (2), on the closed
horizontal Sobolev space, suffices.

## 2. The maximum principle uses truncation tests

Set c=1-rho and A=rho/(2c). Use T=(S-A)_+ in (2), by the Markov chain rule
for the closed derivative. On {S>A}, 2 tau S >= 2cA=rho. Since -R<=rho,

    E[1_{S>A}|VS|^2] + 2c E[(S-A)_+^2] <= 0.

Thus S<=A. The negative-part test gives S>=-A, so

    ||S||infinity <= rho/[2(1-rho)].           (3)

Identity (1) and bounded S imply u=V*S=mS-VS is in L2. This also shows
that the solution of the Dirichlet problem belongs to the divergence
graph space used by the matrix construction. In a complete proof,
truncation/localization justifies (1) for this weak solution; the factors
m,VS are L2 and S,tau are bounded, so all displayed products are integrable.

## 3. Exact weak residual update

Equation (2) is equivalently

    Vu + S tau = -R,
    u=V*S.

Put

    X+=X+u,        B+=(1+S)B,        V+=(1+S)V.

Divergence gives delta B+=X+-mu, hence the mean is unchanged. Horizontal
chain/product rules give

    tau+=V+X+=(1+S)(tau+Vu),
    tau+-1 = -S R - S^2 tau.                   (4)

This is a pointwise-a.e./horizontal-weak identity, rather than a moment
identity. Combining (3) and (4),

    rho+ <= rho^2(3-rho)/[4(1-rho)^2].         (5)

For rho<=1/4,

    rho+ <= (11/9)rho^2,
    ||S||infinity <= (2/3)rho,
    ||u||_2 <= rho/sqrt(3).                    (6)

The last bound is the variational energy estimate with c>=3/4.

## 4. Iteration and the exact law

To iterate, retain the closed horizontal calculus, rather than silently
requiring full smoothness of every S. Each V+ is a bounded positive scalar
multiple of V: when rho<=1/4, 1+S lies in [5/6,7/6]. The corresponding
horizontal graph norms are equivalent. Product and chain rules, the
divergence relation and identity (1) continue by closure. This is the
regularity framework that must accompany the scalar theorem.

Writing C=11/9, induction gives

    rho_j <= C^(-1) (C rho_0)^(2^j).

Thus sum_j ||S_j||infinity and sum_j ||u_j||_2 are finite. The positive
pushforwards X_j converge in L2 to a random variable X_infinity. For every
smooth bounded scalar test f with bounded derivative,

    E[(X_j-mu)f(X_j)] = E[tau_j f'(X_j)].

Since tau_j tends uniformly to 1, pass to the limit to obtain the ordinary
Gaussian Stein characterization. Therefore X_infinity has exactly law
N(mu,1). Every finite iterate already has

    TV(Law(X_j),N(mu,1)) <= 2 rho_j,            (7)

using the bounded derivative of the scalar normal Stein solution for
indicators, with the conservative bound ||f'||infinity<=2.

## 5. Boundaries

The theorem is analytical. Its inverse uses the unknown mean through
V*=X-mu-V; alternatively it uses the unacquired divergence of the coupled
field B. The resulting exact normal law does not acquire either resource
from finitely many h values. The maximum principle is scalar; it does not
remove the matrix commutator or prove a matrix L-infinity estimate.

Equation (7) is a complete scalar-law consequence under the stated domain
conditions, not evidence for a high-dimensional joint-law theorem from
scalar marginal tests. No query, arithmetic or practical-speed advantage
over the packet's existing scalar/bounded stochastic factories follows.
