# Joint compatibility by dual-kernel lifting

2026-10-10. Status: an exact conditional-sampling operation with a proved acquisition route for a structured, growing-dimension class. No historic breakthrough, general constraint solver, or publication novelty is claimed. The earlier pivot-chart proposal was independently derived and then identified as established locally-linearly-dependent-operator machinery; it is not the positive claim here.

## 1. What was compared

Three different primitives were considered before selecting the third.

1. **Violation-count spectrum.** For Boolean constraints, the polynomial `E[t^(number of violations)]` has only `m+1` coefficients and its constant coefficient detects global compatibility. This retains the correct global event, but neither its coefficients nor its update after a new correlated constraint are acquired by knowing the old spectrum. The representation's small scalar range hides the contraction problem. No acquisition theorem was found, so this was not promoted.
2. **Global solution charts.** For bilinear equations `x^T A_i y=b_i`, try to acquire one `x` for which all rows `x^T A_i` are independent, yielding a common right inverse for every target. A large-field tangent step and a binary-safe upper-triangular pivot step can be proved. The latter was found to coincide with the proof of Proposition 3.6 of de Seguins Pazzis (2014). A strong binary coordinate trap is retained below, but this branch is not a new primitive.
3. **Dual-kernel lifting.** Keep every fiber, including singular and exceptional fibers, and correct its multiplicity by sampling a dual constraint combination. A positive counting identity turns all future choices into an exact joint law. The selected mathematical gate was: can this law be acquired without enumerating all combinations or all assignments, and is it preserved under nontrivial conditioning?

The answer to that selected gate is positive under a natively verifiable rank envelope. The envelope's limitations remain substantial.

## 2. Input and the compact state

Let `F_q` be a finite field. Inputs are:

- matrices `A_1,...,A_m` of size `p by n`;
- vectors `c_1,...,c_m in F_q^n`;
- a function `g:F_q^p -> F_q^m` given by an efficiently evaluable circuit or algorithm;
- an integer `R` with a verified proof that every nonzero `lambda in F_q^m` satisfies `rank A_lambda >= R`, where `A_lambda=sum_i lambda_i A_i`.

Define `F(x)` to be the `m by n` matrix whose row `i` is `x^T A_i+c_i^T`. We want to sample uniformly from the *whole* finite set

    S_g = {(x,y): F(x)y=g(x)}.

There is no restriction on the degree of `g`, and there is no assumption that its coordinates factor locally. This is a one-sided affine system, not a generic polynomial system. The representation retains the actual common matrices and the full target circuit, not marginal risks.

Section 7 gives a polynomial-time procedure to acquire a valid `R` from raw square matrices in a fixed, verified extension-field coordinate system. Merely promising or numerically checking high rank is not counted as acquisition.

## 3. One exact trial

Put

    alpha = (q^m-1) q^(-R),       C = 1+alpha.

Perform the following trial independently until it succeeds.

1. Draw a dual vector `lambda` with

       P(lambda=0)=1/C,
       P(lambda=l)=q^(-R)/C for each l != 0.

2. For `lambda != 0`, compute `r_lambda=rank A_lambda` and keep the branch with probability `q^(R-r_lambda)`; otherwise restart. For `lambda=0`, keep it automatically and put `r_lambda=0`.
3. Solve the affine linear system

       A_lambda^T x = -c_lambda,       c_lambda=sum_i lambda_i c_i.

   If inconsistent, restart. Otherwise draw `x` uniformly from **all** its solutions. This inconsistency rejection is indispensable when `c` is nonzero.
4. Solve `F(x)y=g(x)`. If inconsistent, restart. Otherwise draw `y` uniformly from all its solutions and output `(x,y)`.

No normalized rank-weight partition function is computed. No prior enumeration of nonzero dual vectors is performed.

## 4. Exact law, including singular fibers

For a fixed dual vector and a point satisfying its affine system, the probability of reaching that point in a trial is

    (q^(-r_lambda)/C) q^(-(p-r_lambda)) = q^(-p)/C.

This formula also holds for `lambda=0`. The dual vectors that admit a given `x` are precisely the kernel of the map `lambda -> lambda^T F(x)`. If `r_x=rank F(x)`, that kernel has `q^(m-r_x)` elements. Consequently,

    P(trial reaches x) = q^(m-r_x-p)/C.

If `F(x)y=g(x)` is consistent, its fiber has `q^(n-r_x)` points. Thus **every individual solution pair**, irrespective of its fiber rank, has the same one-trial output probability:

    P(trial outputs (x,y)) = q^(m-p-n)/C.                 (1)

Conditioning on success therefore gives the exact uniform distribution on `S_g`. Singular fibers have not been deleted, approximately reweighted, or assumed absent. They receive exactly the extra mass required by their larger number of solutions.

Let

    W_g = q^(m-p-n) |S_g|.

The success probability is `W_g/C`, so expected trials are `C/W_g` when the solution set is nonempty. This is a correctness identity, not by itself a polynomial running-time claim. If there are no solutions, an unbounded implementation would never succeed; the certified regimes below exclude that case. Outside those regimes the procedure is not a decision algorithm and must not be presented as one.

## 5. Constant expected acquisition, arbitrary nonlinear g

A matrix `F(x)` is row-deficient exactly when some nonzero dual vector satisfies the affine system in step 3. Vectors differing by a nonzero scalar define the same event. There are `(q^m-1)/(q-1)` projective dual lines, and each event has probability at most `q^(-R)` under uniform `x`. Hence

    P_x[rank F(x)<m] <= alpha/(q-1).

Every full-row-rank fiber is consistent for every value of `g(x)`, regardless of how nonlinear `g` is. Therefore

    W_g >= 1-alpha/(q-1),
    E[trials] <= (1+alpha)/(1-alpha/(q-1)).                (2)

If `R>=m+1`, then `alpha<1/q`; (2) is strictly less than 3 for every `q>=2`. In particular, this theorem establishes that every target circuit has some compatible pair in this high-rank regime.

This is a high-*collective*-rank resource: each nonzero combination of constraints must retain many independent directions. Individual matrix ranks are insufficient. The resource can occur at growing `m,p,n` and with dense interaction, but it is a strong pseudorandomness/nondegeneracy condition. It should not be described as a general escape from weak-interaction-type hypotheses.

### Better threshold for pure bilinear fixed targets

If `c=0` and `g(x)=b` is constant, `R>=m` suffices for fewer than 4 expected trials.

For `b=0`, every final fiber is consistent; `W_0=sum_lambda q^(-rank A_lambda)>=1`, while `C<2`, so fewer than 2 trials suffice.

For `b!=0`, character orthogonality gives

    W_b = sum_lambda chi(-lambda dot b) q^(-rank A_lambda).

On one nonzero projective line, the sum over scalar multiples is `q-1` if the line is orthogonal to `b`, and `-1` otherwise. Exactly `q^(m-1)` lines are nonorthogonal. Hence

    W_b >= 1-q^(m-1-R) >= 1-1/q,
    E[trials] < 2/(1-1/q) <= 4.

The projective grouping is necessary for this stronger `R=m` conclusion; an ungrouped absolute-value bound is too weak at `q=2`.

## 6. Closure under actual joint conditioning

The representation is closed under the following operation, with an explicit rank charge.

Take an affine restriction `x=x_0+P u`, where `P` has full column rank and codimension `a`. Impose also

    D y = h(x),

where `D` has full row rank `k` and `h` is any efficiently evaluable function. Choose a right inverse `E` of `D` and a basis matrix `Q` for `ker D`. Every satisfying `y` is uniquely

    y=E h(x)+Q v.

Substitution gives another system of the same form:

    F'(u)v=g'(u),
    F'(u)=F(x_0+P u)Q,
    g'(u)=g(x_0+P u)-F(x_0+P u)E h(x_0+P u).

The new coefficient matrices are `P^T A_i Q`. They obey

    rank(sum_i lambda_i P^T A_i Q) >= R-a-k.              (3)

Equation (3) follows by losing at most `k` rank on restricting the domain and at most `a` on projecting the image. The map `(u,v)->(x,y)` is one-to-one onto the conditioned set, so a uniform new sample pushes forward to the exact uniform conditioned joint law. If `R-a-k>=m+1`, the fewer-than-three-trials guarantee survives.

This handles dense nonlinear feedback into a subset of the `y` coordinates, not only independent coordinate fixing. It does not allow uncharged identification of all variables or arbitrary new polynomial constraints. Adding constraint rows is also exact, but a rank envelope must be acquired for the *expanded span* and the increased output dimension must be charged.

### Why the charge cannot be omitted

Over `F_2`, let `A` be a nonsingular alternating matrix of even size `n`, and consider `x^T A y=1`. The unrestricted system has `(2^n-1)2^(n-1)` solutions and collective rank `n`. After the graph restriction `y=x`, every left side is zero, so the conditioned problem is impossible. This is not a sampler failure: the unrestricted rank resource has been consumed by the identification. No universal uncharged feedback-closure theorem is available.

## 7. Native rank-envelope acquisition

For square `n by n` matrices, fix a verified representation `K=F_(q^n)` of `F_q^n`. Every `F_q`-linear map has a unique linearized-polynomial representation

    L_i(z)=sum_(j=0)^(n-1) a_(ij) z^(q^j),        a_(ij) in K.

The coefficients are acquired from the matrix by solving one Moore interpolation system over `K`; the same inverse can be reused for all input matrices. No low-degree representation is supplied as an oracle. Reconstructing the matrix from the coefficients checks the conversion exactly.

Check that the input matrices are linearly independent over `F_q`; otherwise reject this positive-rank certificate. Let `s` be the largest coefficient index occurring among any `L_i`. Every nonzero `F_q`-linear combination is a nonzero ordinary polynomial of degree at most `q^s`. Its kernel therefore has at most `q^s` points, so its matrix rank is at least

    R=n-s.                                               (4)

This is established linearized-polynomial/rank-metric-code mathematics. The contribution under test is the exact joint sampling and conditioning operation that consumes the certificate, not the bound (4) or Gabidulin code structure.

The certificate can handle `s,m,n` all growing, for example `s` and `m` both proportional to `n` with `n-s>=m+1`. It is neither a fixed matrix-rank theorem nor a bounded-width decomposition. It is nevertheless a structured-coordinate certificate, not a universal way to certify the true minimum combination rank.

### Verified acquisition boundary

The exact script supplies a six-dimensional example with three matrices. Before an invertible change of `x` and `y` bases, Moore interpolation certifies `R=4`. After a stored invertible scramble `A_i -> P^T A_i Q`, the ranks of all seven nonzero combinations are unchanged:

    5, 5, 6, 4, 5, 5, 5.

But interpolation in the same canonical extension-field basis has degree 5, so this certificate returns only `R=1`. The full matrices, basis transformations, coefficients and ranks are in `EXACT_RESULTS.json`.

This does not prove that no better acquisition algorithm exists. It proves that the supplied simple acquisition rule does not recognize the intrinsic resource under general hidden basis changes. Known, explicit basis transformations can carry the old certificate forward. Recovering useful hidden structure from arbitrary raw inputs was not solved.

## 8. Exact random bits and arithmetic cost

The proposal has a finite exact implementation. Draw an integer uniformly from a set of size `q^R+q^m-1`. Allocate `q^R` outcomes to `lambda=0` and one outcome to each nonzero vector (using base-q coordinates). Standard binary rejection draws this integer with expected `O((R+m) log q)` unbiased bits. If `lambda!=0`, its acceptance probability is `q^(-(r_lambda-R))`; draw `r_lambda-R` independent field elements and accept precisely when they are all zero. Uniform kernel/fiber samples use free-coordinate field elements after Gaussian elimination.

Each trial forms one matrix combination, computes its rank and an affine kernel, evaluates `F(x)` and `g(x)`, and solves one more linear system. A loose bound is

    poly(m,p,n) field operations + one evaluation of g,
    O((m+p+n) log q) expected random bits,

using `R<=min(p,n)` and exact finite-field arithmetic. In the certified regimes, expected total work is less than three or four times that trial bound. Gaussian elimination, the input circuit, the field representation, and rank-envelope verification are all charged. There is no exponentially large precision parameter.

For the square-map certifier, one may use `O(n^3+m n^2)` extension-field operations for a reusable interpolation solve, plus reconstruction and ordinary independence tests. An irreducible defining polynomial is verified; a representation can also be constructed by a randomized search with verification. Finding a particularly favorable hidden field basis is not included in this bound.

## 9. Exact verification

Run `python verify_dual_kernel.py`. It uses integer arithmetic and Python `Fraction`, with no floating-point evidence.

Seven systems were checked by summing the **actual proposal/acceptance/kernel probabilities** over every dual vector and every point, and then comparing the probability of every satisfying pair:

- Binary systems with `n=3,m=2` and `n=5,m=3`, including distinct singular-fiber ranks and all nonzero targets.
- A binary `n=6,m=3` case, its bi-affine modification, and a one-sided nonlinear target modification that changes the exceptional `x=0` fiber.
- A ternary `n=2,m=2` case.
- A binary seven-dimensional system after the nonlinear graph restriction `y_0=x_0 x_1`, leaving six free `y` coordinates and certified residual rank 4.

All seven exact-law checks passed. The worst exact expected trial counts in these cases are, respectively,

    7/3, 30/13, 92/61, 92/61, 92/61, 17/8, 92/61.

These finite tests supplement the all-dimension proof. They do not establish novelty or broad practical speed.

## 10. What remains missing

This is a concrete positive operation with a complete law, a resource-sensitive closure theorem, and a native acquisition procedure for a structured class. It is not the foundational transformation requested by the overall program.

- General minimum-rank certification has not been acquired.
- The positive certificate rests on classical rank-metric structure and can disappear under an unknown change of coordinates.
- The high-rank promise is a strong global nondegeneracy hypothesis; no generic SAT, discrepancy, or arbitrary polynomial compatibility problem is solved.
- General nonlinear sharing consumes or destroys the free affine fibers. The diagonal alternating example falsifies uncharged closure.
- A targeted primary-source check found the pivot-chart antecedent and standard rank-metric ingredients, plus prior exact sampling for one quadratic equation. It did not establish the publication novelty of the particular multi-constraint sampler or its closure theorem. Absence from this short search is not novelty evidence.

The next mathematically meaningful gate is acquisition of a comparably economical positive dual envelope after general constraint composition, without invoking a minimum-rank oracle or requiring an exposed rank-metric coordinate system. No such theorem is asserted here.
