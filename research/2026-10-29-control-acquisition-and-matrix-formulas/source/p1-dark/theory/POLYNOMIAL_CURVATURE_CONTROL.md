# Certified control from the curvature of the acquired polynomial

28 October 2026. This addresses a control-certificate limitation of the
already acquired law: a useful uniform value error need not give a sharp
global bound through the unconstrained Bernstein coefficient hypograph.
The construction below uses the actual acquired polynomial, its exact
derivatives and an exactly certified upper Hessian bound. It acquires no
source derivative and makes no new source call.

Governing local inputs read directly:

- `theory/SIMPLEX_LAW_ACQUISITION.md`, especially sections 1--4 and 6--8.
- `code/simplex_law.py`, the acquired nodal polynomial, Bernstein transform
  and uniform error computation.
- `code/hypograph_control.py`, the existing task bound and finite-command
  convention.
- `code/run_lattice_experiments.py`, including its raw-to-J offset removal,
  interval processing and post-decision source checks.

The premise is a polynomial p of degree at most k on

    D={u in R^n: u_i>=0, sum_i u_i<=delta},

represented by acquired rational degree-k Bernstein coefficients b_alpha,
and a proved uniform error

    |J(u)-p(u)|<=E for every u in D.                  (1)

Here J is the positive source conductance, not the raw R=3/2+J. The prior
acquisition theorem provides (1) including calibration and requested-versus-
actual DAC error. Every formula below remains conditional on those source
and acquisition premises. Polynomial interpolation alone does not establish
them. All prices c are known and may be arbitrary real numbers.

## 1. Exact Bernstein Hessian coefficients

Let lambda_0=1-sum u_i/delta and lambda_i=u_i/delta for i=1,...,n. Write

    p(u)=sum_(|alpha|=k) b_alpha B_alpha^k(lambda),
    B_alpha^k(lambda)=k!/(product alpha_i!) product lambda_i^alpha_i.

The e_i below are coordinate unit vectors in n+1 barycentric coordinates;
e_0 represents the unused-dose coordinate. Differentiating in physical u_i
corresponds to `(partial_lambda_i-partial_lambda_0)/delta`. Consequently

    partial_i p(u)=(k/delta) sum_(|beta|=k-1)
        (b_(beta+e_i)-b_(beta+e_0)) B_beta^(k-1)(lambda).       (2)

For k>=2, differentiating again gives

    Hess p(u)=sum_(|gamma|=k-2) B_gamma^(k-2)(lambda) H_gamma,  (3)

where the symmetric n-by-n matrix has entries

    H_(gamma,ij)=k(k-1)/delta^2 *
        [b_(gamma+e_i+e_j)-b_(gamma+e_i+e_0)
         -b_(gamma+e_0+e_j)+b_(gamma+2e_0)].                  (4)

This includes i=j without changing multiplicities: the first coefficient
then has index gamma+2e_i and the two middle terms coincide. The factors
k(k-1) already arise from differentiation. There is no extra factor two
on a repeated index.

Every weight in (3) is nonnegative and their sum is one. Therefore, if an
acquired rational number mu>=0 satisfies

    mu I-H_gamma is positive semidefinite for every gamma,   (5)

then

    Hess p(u)<=mu I for every u in D.                        (6)

For k=1 the Hessian is zero and mu=0 is sufficient. A constant polynomial
has the same trivial certificate. For k=2 there is one constant Hessian.
For k=3 there are exactly n+1 coefficient matrices and they are the actual
Hessians at the simplex vertices, so (5) is also necessary for a given mu
to bound the Hessian everywhere. For higher degrees (5) is sufficient and
can be conservative because Bernstein coefficients need not be attained.

## 2. Acquiring mu by a rational certificate

A numerical eigensolver may propose a candidate near
`max(0,max_gamma lambda_max(H_gamma))`. It must not establish (5). Round the
proposal to a declared rational grid and test every matrix mu I-H_gamma by
exact rational arithmetic. If a test fails, enlarge the rational candidate
and repeat. The final recorded mu and the successful exact checks establish
the bound; the eigensolver's accuracy or convergence is irrelevant to validity.

One exact PSD test is rational LDL elimination, including singular pivots:

1. At each remaining symmetric Schur complement, reject a negative diagonal
   pivot. A positive pivot admits the usual exact Schur complement update.
2. If the pivot is zero, every remaining entry in that pivot row/column must
   be zero; otherwise the corresponding 2-by-2 principal minor is negative
   and the matrix is not PSD. Delete a zero row/column and continue.
3. If all pivots satisfy these conditions, the successive congruences prove
   positive semidefiniteness.

A tiny negative pivot is still negative; it cannot be clipped to zero. A
zero pivot cannot simply be skipped while retaining nonzero off-diagonal
entries. Strict positive definiteness, obtained by a small rational margin,
is an optional simpler certificate, not a physical premise.

The procedure always has a finite rational fallback. For example take

    mu=max(0,max_(gamma,i)[H_(gamma,ii)+sum_(j!=i)|H_(gamma,ij)|]). (7)

Gershgorin's bound gives every maximum eigenvalue <=mu. Equivalently, a
strict rational increment above (7) gives symmetric strict diagonal
dominance for mu I-H_gamma and hence positive definiteness. Formula (7)
can be much looser than a numerical proposal plus exact verification. Its
availability prevents failure of the proposal routine from becoming an
unjustified certificate.

There are `binom(n+k-2,k-2)` coefficient matrices when k>=2. Assembly costs
O(n^2) coefficient operations per matrix and exact dense LDL uses O(n^3)
rational arithmetic operations per matrix. Bit complexity depends on the
acquired rational coefficient sizes. For the n=12,k=3 case there are only
13 matrices of order 12. No hidden source quantity enters these computations.

## 3. A global conductance-price upper bound from one candidate

Let x be any feasible candidate. Integrating (6) along the segment from x
to u proves

    p(u)<=p(x)+grad p(x)^T(u-x)+(mu/2)||u-x||_2^2.             (8)

In particular this uses the gradient of the acquired polynomial, not the
unknown source gradient. Define the simplex vertex set
`V={0,delta e_1,...,delta e_n}` in physical n-dimensional coordinates and

    M_J(x)=max_(v in V) [(grad p(x)-c)^T(v-x)
                         +(mu/2)||v-x||_2^2].                (9)

The quadratic expression is convex in u because mu>=0. If u is a convex
combination of the vertices, convexity bounds its value by the corresponding
combination of vertex values and hence their maximum. Thus (8) and (1) give

    max_(u in D) [J(u)-c^T u]
        <=U_J(x):=p(x)-c^T x+M_J(x)+E.                      (10)

The nonnegativity of mu matters for this vertex argument. A negative
upper-curvature value, even if valid for a concave polynomial, cannot be
inserted into (9) with only vertex maximization: a concave quadratic can
attain its maximum in the interior. Using mu=max(0,mu_proposed) avoids that
mistake.

For a rigorous actual-command value enclosure `[J_lo(x),J_hi(x)]`, take

    L_J(x)=J_lo(x)-c^T x,
    regret_J(x)<=max(0,U_J(x)-L_J(x)).                        (11)

The predictor's interval intersection, the baseline lower bound and any
valid Jensen lower bound may be intersected to strengthen J_lo. Merely
using p(x)-E also works. Since (9) bounds the quadratic at x, its exact
maximum is nonnegative. An implementation may include zero in the maximum
as a defensive convenience.

For mu=0, (9) is the usual first-order simplex gap for the acquired concave
polynomial. For nonzero mu the additional geometric allowance is at most
`mu delta^2`, since the squared Euclidean diameter of D is 2delta^2. This
does not assert that mu itself is dimension-independent or small.

## 4. Compliance-price upper bound without another law acquisition

For any j0>0 and any actual J>0,

    -1/J <= -2/j0+J/j0^2.                                  (12)

The difference of right and left sides is exactly
`(J-j0)^2/(J j0^2)>=0`. This is a global tangent upper bound for the increasing
concave scalar utility -1/J.

Suppose j0=p(x)>0. Combining (12), `J(u)<=p(u)+E`, and (8) gives

    M_Z(x)=max_(v in V) [(grad p(x)/j0^2-c)^T(v-x)
                         +(mu/(2j0^2))||v-x||_2^2],         (13)

    max_(u in D) [-1/J(u)-c^T u]
        <=U_Z(x):=-1/p(x)-c^T x+M_Z(x)+E/p(x)^2.           (14)

Again the maximized quadratic is convex and vertex maximization is valid.
For a positive actual-command lower bound J_lo(x),

    L_Z(x)=-1/J_lo(x)-c^T x,
    regret_Z(x)<=max(0,U_Z(x)-L_Z(x)).                        (15)

The monotonicity of -1/J makes the lower endpoint the correct choice in
(15). A positive warranted baseline can replace a nonpositive noisy
interval endpoint. The baseline term Z(0), if present in the task reward,
is common to every action and cancels from regret.

If p(x)<=0, formula (14) must not be used. One may retain the existing
hypograph certificate, or choose any independently known positive j0 and
use the unsimplified valid constant

    -2/j0+p(x)/j0^2-c^T x

in place of `-1/p(x)-c^T x` in (14), with every other occurrence of p(x)^2
replaced by j0^2. A global source lower bound together with E smaller than
that bound suffices to ensure p(x)>0 everywhere, but this is not necessary
when the candidate's own polynomial value is directly positive.

The separate acquired -Z polynomial can also be given its own version of
(10). Neither that direct route nor (14) universally dominates the other:
they have different approximation and curvature errors. Taking the smaller
of independently valid upper bounds is legitimate.

## 5. Exact O(n) vertex maximum

For any gradient vector a and nonnegative scalar nu define

    q0=-a^T x+(nu/2)||x||_2^2,
    qi=q0+delta a_i+(nu/2)delta^2-nu delta x_i.

The maximum of q0,q1,...,qn is exactly
`max_(v in V)[a^T(v-x)+(nu/2)||v-x||^2]`. For (9), use
`a=grad p(x)-c`, `nu=mu`; for (13), use
`a=grad p(x)/j0^2-c`, `nu=mu/j0^2`. Thus the final global control bound
requires no nonconvex maximization after the acquired derivatives and mu
certificate are available.

## 6. Proposal, comparison and finite physical commands

SLSQP or another numerical optimizer may propose x using only p and known
prices. Its stopping message does not certify the task. Convert the proposal
to a legal actual DAC command, recompute p(x), grad p(x), the interval lower
bound and the vertex bound at that exact command, and retain all arithmetic
or interval-rounding error. The derivative formula (2) and the acquired
rational coefficients allow this last calculation without floating ambiguity.

For several feasible candidates and several valid global upper bounds, one
may take the largest valid candidate lower reward and the smallest valid
global upper reward. This is safe even if the winning upper bound was
constructed around a different candidate: every upper bound controls the
same global optimum. The best candidate is the one associated with the
winning lower bound. Keep the old hypograph bound if the new curvature
bound is loose. A fixed rule that picks the smaller bound is not selective
source-truth tuning.

There is no source-gradient recovery claim. A polynomial derivative can be
a poor approximation to a true source derivative while this certificate
remains valid: the uniform value enclosure relates the true function to p,
and exact curvature bounds only control p itself. Likewise p need not be
concave, and an inaccurate proposal only makes the certified regret larger.
This is the obstruction removed by the construction.

The additional costs are coefficient assembly, eigensolver proposals, exact
PSD checks, candidate optimization and exact evaluation. Additional physical
source readings are zero if the previous law and calibration remain valid.
Actual deployment still pays all active setting writes, preparation,
settling, integration if required, and reset. A dense candidate can use more
than the k controls active in each acquisition node; those use costs remain
explicit. No hardware operation is performed by this analysis.

An equally informed conventional polynomial or semidefinite certification
method can use the identical record and algorithm. No universal superiority,
new photon bound, physical calibration achievement or independent whole-proof
audit follows. The root experiment code records the attained mu, exact PSD
verification and resulting certificates separately from this analytic proof.
