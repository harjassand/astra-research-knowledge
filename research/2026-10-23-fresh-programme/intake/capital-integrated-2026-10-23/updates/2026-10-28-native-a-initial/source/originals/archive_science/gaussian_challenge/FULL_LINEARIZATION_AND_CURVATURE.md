# Full Gaussian Stein linearization: an obstruction, a coercive replacement, and its remaining gap

Derived in this chat from the frozen CASE and S3 sections 16–18, S4, and S12. These are mathematical results about an analytical correction interface. They do not supply an acquired Gaussian-mean sampler, a value-only PDE solver, or a historical novelty claim.

## 1. Conditional source preservation creates exponential ill-conditioning even at an exact Gaussian

Let `G,Z` be independent standard scalar Gaussians, choose `0<a<1`, and put `b=sqrt(1-a^2)`. The source `h(G)=aG` is a globally Lipschitz conservative field and

`X=aG+bZ ~ N(0,1)`

is already exactly Gaussian. Its joint Gaussian Stein field is `(a,b)`.

Retain S3's conditional-in-Z restriction: a correction is `u=delta_Z J`, so `E_Z u=0` for every G. The full linearized symmetric Stein residual (scalar symmetry is automatic) is

`L(u,J)=a partial_G u+b partial_Z u+bJ`.

Since `partial_Z delta_Z=N_Z+1`, this is

`LJ = b(N_Z+2)J+a delta_Z partial_G J`.                 (1)

Write `e_{n,m}=He_n(G)He_m(Z)/sqrt(n!m!)` for the orthonormal joint probabilists' Hermite basis. Equation (1) preserves total chaos degree `n+m`, and

`L e_{n,m}=b(m+2)e_{n,m}+a sqrt(n(m+1))e_{n-1,m+1}`.

Take the norm-one residual `R_N=e_{N,0}`. The unique degree-N solution of `LJ=-R_N` is

`J_N=sum_{k=0}^N c_k e_{N-k,k}`,

`c_k= -b^(-1)(-a/b)^k sqrt(binomial(N,k))/((k+1)(k+2))`. (2)

Proof: `2b c_0=-1`, and the remaining rows give

`b(k+2)c_k+a sqrt((N-k+1)k)c_{k-1}=0`.

Consequently

`||J_N||_2^2=b^(-2) sum_k binomial(N,k)(a^2/b^2)^k / ((k+1)^2(k+2)^2)`

and, because every denominator is at most `(N+1)^2(N+2)^2`,

`||J_N||_2 >= b^(-N-1)/((N+1)(N+2))`.                 (3)

Also `||u_N||_2^2=sum_k(k+1)c_k^2 >= ||J_N||_2^2`.

Every L2 solution has the same degree-N component, since the finite matrix on that chaos is triangular with nonzero diagonal. Thus adding other chaos components cannot evade the lower bound. In particular no inverse bounded in ordinary Gaussian L2, or bounded with any fixed finite number of Sobolev derivatives of the residual, exists in this conditional-Z class: a fixed derivative loss grows only polynomially in N, whereas (3) grows exponentially.

**Meaning.** S3 correctly observed that the source derivative is unbounded and therefore a naive Neumann series is unjustified. Equations (1)–(3) prove something sharper: the desired uniform inverse in that particular conditional-centering class is actually false, even at a harmless affine exact-Gaussian baseline. This is an obstruction to that inverse theorem, not to N687. The chosen arbitrary Hermite residual is not asserted to be an actually generated nonlinear source residual. A method can avoid the obstruction by using a smaller compatible residual class, by changing its norm to charge exponential source regularity, or by changing the correction class.

## 2. Joint centering removes the affine obstruction

Use the orthogonal coordinates

`x=aG+bZ`, `s=bG-aZ`.

They are independent standard Gaussians. For any residual `R(x,s)`, apply the S3 baseline Gaussian Hodge inverse in x with s held as a parameter. It gives `(u_0,J_0)` with

`delta_x J_0=u_0`, `sym(J_0+(D_xu_0)^T)=-R`.

Pull back the correction, and set `J=J_0(a,b)`. Then

`delta_(G,Z) J=u`,

`sym[(a,b)D_(G,Z)u^T+J(a,b)^T]=-R`.

The joint divergence makes the correction globally centered. It need not be centered conditional on the old G. The S3 bounds now apply without the exponential growth:

`||u||_2 <= (1/2)||R||_2`,

`||D_xu||_2 <= ||R||_2`,

`||J||_2 <= (2+sqrt(2))||R||_2`.

The same argument works in d dimensions for symmetric A with `||A||op<1`, `B=(I-A^2)^(1/2)`, output `x=AG+BZ`, and retained coordinate `s=BG-AZ`. The block transformation is orthogonal because A and B commute.

This is a diagnostic, not a new affine mean sampler: an affine source already exposes its mean through `g(0)`.

## 3. A non-affine coercive variational inverse

Let Q have a standard Gaussian law on R^n. Let `X: R^n -> R^d`, and let `B: R^n -> R^(d x n)` satisfy rowwise

`delta B=X-mu`.

Define `tau=B(DX)^T`. Assume

`sym tau >= c I_d`, `||tau||op<=T0`, `||B||op<=M`,      (4)

for positive deterministic c,T0,M. Smoothness may initially be assumed; the construction extends to the closed Gaussian divergence graph domain below.

For a symmetric residual matrix field `R in L2`, seek a **symmetric** matrix field S and set

`J=SB`, `u=delta(SB)`.

On symmetric test fields define

`a(S,T)=E[delta(SB) dot delta(TB)]+E< S tau,T >_F`.    (5)

The Hilbert space is the closed graph domain of `S -> delta(SB)`, with norm squared `||S||_2^2+||delta(SB)||_2^2`.

Gaussian integration by parts gives

`< sym[B(Du)^T+J(DX)^T], T > = a(S,T)`.              (6)

The form need not be symmetric, but

`a(S,S)=||u||_2^2+E tr(S^2 sym tau)`

`          >= ||u||_2^2+c||S||_2^2`.                 (7)

It is continuous in the graph norm using the upper bound on tau. The coercive variational theorem therefore gives a unique S satisfying

`a(S,T)=-E<R,T>` for every symmetric T.

Equivalently, it solves the full linearized Stein equation in distributions:

`sym[B(Du)^T+J(DX)^T]=-R`.                          (8)

The quantitative bounds are

`||S||_2 <= ||R||_2/c`,

`||u||_2 <= ||R||_2/(2sqrt(c))`,

`||J||_2 <= M||R||_2/c`.                            (9)

To obtain the middle inequality, write `U^2+cS0^2<=R0 S0` from (7), and maximize `R0 S0-cS0^2` over `S0>=0`. No factor involving dimension, Hermite degree, or derivatives of B occurs in (9).

The graph operator is closed by taking its maximal Gaussian distributional divergence domain. Smooth fields give a dense test core under the stated initial regularity; alternatively the Hilbert space can be defined as the graph closure of that core. The weak equation and the norm estimates require no pointwise evaluation of a derivative oracle.

### Application to the N687 analytical source field

Normalize the final noise to one and suppose h is a conservative field with Lipschitz constant ell<1. Let K be its canonical Gaussian Stein kernel, so `delta_G K=h-mu`, `||K||op<=ell`. Start with

`X=h(G)+Z`, `B=[K,I]`.

Then

`tau=I+K(Dh)^T`,

`sym tau >= (1-ell^2)I`,

`||tau||op<=1+ell^2`, `||B||op<=sqrt(1+ell^2)`.

Thus the full source derivative can be absorbed into a coercive principal operator. The argument need not treat `K D_G` as a small bounded perturbation on L2.

### What this does not yet prove

The variational solution controls u and J, and controls only the symmetric combination in (8). It does **not** automatically control the full horizontal derivative `B(Du)^T`, its skew part, or the nonlinear product `J(Du)^T`. A positive pushforward `X+u` has the algebraic quadratic residual from S3 only when the relevant chain rule and product are justified. A dimension-controlled horizontal Korn/regularity estimate, or a different gauge controlling this product directly, is still required.

Neither B nor the variational solve is supplied to a value-only algorithm. In particular expanding `delta(SB)` introduces `S(X-mu)`; treating this as runtime arithmetic would silently use the unknown mean. The displayed theorem is an analytical inverse, not an acquired compiler.

## 4. Why a source-dependent affine coordinate rotation cannot simply repair the non-affine case

For `B=[K,I]`, define the horizontal vector fields

`V_i=partial_(Z_i)+sum_j K_ij(G) partial_(G_j)`.

For a constant K these commute and can be aligned with fixed coordinates. A nonconstant conservative canonical K can have nonzero brackets outside their span.

Choose a C-infinity compactly supported function psi(x,y) that equals `x^2 y/2` on a neighborhood of `(1,0)`. Put

`K=eta Hess psi`, `g=delta_G K=eta grad[(N_G-1)psi]`.

The field g is a smooth, globally Lipschitz gradient. Its Lipschitz constant is finite because it is compactly supported; eta can make that constant arbitrarily small. K is the canonical conservative Stein kernel of g: the identity `delta Hess psi=grad[(N_G-1)psi]` holds, and the Gaussian Hermite decomposition (or the resolvent formula) identifies the canonical Hessian solution uniquely up to potentials with zero Hessian.

In the displayed neighborhood,

`K=eta [[y,x],[x,0]]`,

`[V_1,V_2]=eta^2 (y partial_x-x partial_y)`.

At `(1,0)` this is nonzero and purely source-directed. A linear combination of the V_i can have zero Z component only when all coefficients are zero. The bracket is therefore outside their horizontal span. A coordinate change cannot turn these fields into coordinate partial derivatives, or even into a distribution spanned by commuting coordinate fields, because diffeomorphisms preserve Lie brackets and involutivity.

This is a genuine C1,1 conservative counterfamily to that coordinate-straightening shortcut. It does not defeat the variational inverse or the Gaussian-mean target. It identifies the curvature that a multi-dimensional nonlinear estimate must handle.

## 5. Scalar all-order positive correction: analytical closure with a clear acquisition barrier

For d=1 the nonlinear product can be closed exactly. Let `V=B dot grad`, `delta B=X-mu`, and `tau=VX=1+R` with `||R||infinity=rho<1`. Define the Gaussian-adjoint operator

`V*=X-mu-V`.

The identities `V V*=V* V+tau` and `u=V*S` turn the full linear equation into

`(V*V+2tau)S=-R`.                                  (10)

This is a scalar positive-killing resolvent. The Dirichlet form `E(Vf)^2` and `tau>=1-rho` yield, by truncation/maximum-principle testing,

`||S||infinity <= rho/[2(1-rho)]`.                   (11)

The same statement follows from the killed Markov semigroup when a classical diffusion is available. Equation (10), interpreted in its closed form domain, is enough; no numerical PDE oracle is postulated.

Set

`u=delta(SB)`, `X+=X+u`, `B+=(1+S)B`.

Then `delta B+=X+-mu`. Equation (10) gives `Vu+S tau=-R`, so the exact new Stein coefficient is

`tau+=(1+S)(tau+Vu)`

`       =1-SR-S^2 tau`.

Hence

`rho+ <= rho^2(3-rho)/[4(1-rho)^2]`.                 (12)

For `rho<=1/4`, the multiplicative constant on rho squared is at most `11/9`, and `||S||infinity<=1/6`. The corrections are globally centered; their L2 norms obey (9). Their sum converges because (12) is quadratic. Multiplication of B by the positive bounded factors `(1+S)` preserves comparable closed Dirichlet forms. The sequence has an L2 limit, and the Stein identities converge to the standard Gaussian identity. Thus the limiting law is `N(mu,1)`.

For each finite stage, the scalar Stein equation gives the full-law bound

`TV(Law(X_n),N(mu,1)) <= 2 rho_n`.

This follows by testing smooth bounded functions and the standard one-dimensional Gaussian Stein derivative bound, then approximating bounded measurable tests. It is not inferred from finite moments. One can also retain only the exact Stein residual estimate (12) if avoiding any density regularity shortcut; the chain rules follow in the horizontal Sobolev domain because `Vu=-R-S tau` is bounded.

This is an all-order positive **analytical** correction, not an implemented value-only algorithm. Its resolvent drift contains `X-mu`, or equivalently the unacquired divergence of B. It consequently cannot be used to claim N687. In multiple dimensions, the vector elasticity and horizontal curvature enter before (12); they are not hidden in a scalar calculation.

## 6. Executed checks and comparison

`check_full_linearization.py` verifies the exact Hermite recurrence with rational arithmetic for `a=3/5`, `b=4/5`, and reports normalized inverse norms without relying on floating cancellation. It also symbolically verifies the local Lie bracket, the identity `g=delta Hess psi`, and the scalar quadratic residual formula. These checks support the algebra; the proofs above establish the infinite-dimensional statements.

Ordinary competitors remain unchanged. A scalar affine source requires only `g(0)`; no speed advantage is claimed there. The supplied fixed-positive-exponent compiler and Gaussian-cloud correction have stronger acquired end-to-end contracts than this analytical inverse. The contribution is a precise failure of one proposed inverse theorem and an alternative non-affine coercive formulation with an identified nonlinear and acquisition gap.

A targeted primary-source comparison found related, but differently scoped, regularity machinery. [Carrapatoso, Dolbeault, Hérau, Mischler and Mouhot, arXiv:2012.06347](https://arxiv.org/abs/2012.06347) establish weighted Euclidean Korn inequalities with constants depending on the weight's geometry. [Isangulova, arXiv:2111.13967v2, section 5.1, Lemma 11](https://arxiv.org/pdf/2111.13967) gives a coercive estimate for a specific horizontal operator on the first Heisenberg group, modulo its finite-dimensional kernel. Neither result, as stated, supplies an estimate uniform over arbitrary canonical K, Gaussian source geometry, and dimension. No theorem from these papers is used without its hypotheses in the proofs above.

**Exact next scientific obligations:** establish a dimension-controlled nonlinear product estimate for the joint-divergence variational inverse, and realize the correction using original g values without evaluating mu, K, or a conditional expectation for free. A scalar PDE representation or an unacquired orthogonal chart does not discharge either obligation.
