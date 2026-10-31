# A scoped precision-cost construction for reusable resolvents

## Scientific conclusion

Imperfect vector experiments can acquire a small reusable inverse representation
when a numerical spectral-tail promise is part of the input class. The unknown
direction and amplitude are learned. Variable precision separates the cost of
discovering a direction from the cost of refining its effect. Under a
whole-vector tolerance cost proportional to `tau^(-p)`, the costs are
`n^(p/2)` and `epsilon^(-p)`, additively, at constant confidence.

This is useful auxiliary capital, not a claimed new frontier result. Noisy power
iteration and low-rank resolvent formulas are established machinery. The strongest
fixed-precision analysis already gives the same polynomial scaling, with extra
logarithmic repetition. Moreover, if the tail promise must itself be acquired,
an additional hidden mode of size `epsilon` forces precision work at least
`n^(p/2) epsilon^(-p)`. The favorable additive law must not be advertised as a
general self-certifying low-rank learning theorem.

## 1. Exact input/output/cost contract

The unknown real symmetric `n x n` matrix is

\[
B=\lambda uu^T+E,\qquad \|u\|=1,\quad 1\le\lambda\le2,
\quad Eu=0,\quad \|E\|\le\beta\le\epsilon/8,
\quad 0<\epsilon\le1/4.
\]

`u`, `lambda`, and `E` are unknown. The spectral-tail bound is a supplied class
promise, not a learned certificate. `E` may have arbitrary full rank on
`u^perp`; no exact algebraic low-rank property is assumed.

For any chosen `v` and requested `tau>0`, the source returns

\[
\mathcal O_\tau(v)=Bv+e,\qquad \|e\|\le\tau\|v\|.
\]

Errors may be adversarial and adaptive. The contract allows arbitrary requested
accuracy. Define **precision work** `W=sum tau_t^(-p)`, for fixed `p>0`.
This cost law is a model assumption. It does not follow from merely knowing
that source errors are bounded. For an experimental implementation that obtains
accuracy by independent repeated measurements, the statistical assumptions and
confidence factors needed to realize this oracle must be charged separately.
The cost is for a whole-vector response; reading one response still costs `n`
scalar words. If one replication measures all `n` components, total physical
or arithmetic measurement work can include another factor `n`.

Output: a unit vector `uhat`, scalar `lambdahat in [1,2]`, and the executable rule

\[
G_\mu b=\frac b\mu-
\frac{\widehat\lambda}{\mu(\mu+\widehat\lambda)}
\widehat u(\widehat u^Tb),\qquad \mu\ge1.
\]

One acquisition event guarantees

\[
\sup_{\mu\ge1}\|G_\mu-(\mu I+B)^{-1}\|<\epsilon.
\]

Thus every later right-hand side and shift, including adaptively chosen ones,
satisfies `||G_mu b-(mu I+B)^(-1)b|| <= epsilon ||b||`, without new source access.
This is an absolute operator-norm guarantee. It is not a relative guarantee for
arbitrary scalar functionals that nearly cancel, and not a guarantee for every
rational expression.

## 2. Acquisition theorem

For `0<delta<1`, a fully specified noisy-power procedure has success probability
at least `1-delta`, uniformly over all permitted adaptive source errors. It uses

\[
Q=O(\log n\log(1/\delta)+\log(1/\epsilon))
\]

source actions and precision work

\[
W=O_p\bigl(n^{p/2}\log(1/\delta)+\epsilon^{-p}\bigr).
\]

Storage is `O(n)` words. Additional real arithmetic costs `O(nQ)` before
deployment. Each future full-vector solve costs `O(n)` arithmetic and no source
action. A scalar query `a^T G_mu b` costs the vector inner products actually
needed; its cost is not assumed constant.

### 2.1 Noisy angle recurrence

Write a unit current vector as `v=a u+w`, `w perpendicular u`, and let
`T=||w||/|a|`. For `y=Bv+e`, `||e||<=tau`, its normalized successor has

\[
\tan\angle(y,u)
\le \frac{\beta T+\tau/|a|}{\lambda-\tau/|a|}
\tag{1}
\]

provided the denominator is positive. This follows by bounding the component
along `u` below by `lambda|a|-tau` and the orthogonal component above by
`beta||w||+tau`. Normalization does not change the ratio.

### 2.2 Discovery phase

Draw a uniform random unit vector. Its squared overlap `X=|u^T v|^2` has
`E X=1/n` and `E X^2=3/[n(n+2)]<=3/n^2`. Paley--Zygmund gives

\[
\Pr\{|u^Tv|\ge1/(2\sqrt n)\}\ge3/16.
\]

On this event its angle tangent is at most `T_0=2 sqrt(n)`.
Let `alpha=1/32`, use the conservative tail bound `beta_0=1/4`, and maintain

\[
\tau_t=\frac{\alpha}{\sqrt{1+T_t^2}},\qquad
T_{t+1}=\frac{\beta_0T_t+\alpha}{1-\alpha}.
\tag{2}
\]

If the actual tangent is at most `T_t`, then `|a|>=1/sqrt(1+T_t^2)`, hence
`tau_t/|a|<=alpha`. Equation (1) proves the induction. The recurrence ratio is
`8/31<1`; its fixed point is `1/23<1/8`. Therefore after `O(log n)` iterations
the tangent bound is at most `1/8`.

The precision work of this phase is

\[
\sum_t\tau_t^{-p}
=\alpha^{-p}\sum_t(1+T_t^2)^{p/2}
=O_p(n^{p/2}+\log n)=O_p(n^{p/2}).
\]

The last estimate uses fixed `p>0` and `n>=2`; constants may depend on `p`.

Test the candidate with one more action at `tau_test=1/128` and accept it if
`v^T O_tau_test(v)>=3/4`. A successful discovery has true Rayleigh quotient at
least `(64-1/4)/65>0.98`, so it passes even with the allowed test error.
Conversely, any accepted candidate has true Rayleigh quotient at least
`95/128`. Since this quotient is at most `2 a^2+(1/4)(1-a^2)`, acceptance implies

\[
a^2\ge\frac{95/128-1/4}{2-1/4}=9/32,
\qquad \tan\angle(v,u)<2.
\]

Thus the test protects later refinement even when the random start did not
satisfy the favorable overlap event. A zero or numerically unusable iterate
can simply reject that start; it cannot occur on a favorable start under the
stated effective error bound. Repeat independent starts at most
`ceil(log(delta)/log(13/16))` times. Adversarial errors cannot invalidate the
success event for a favorable start, so failure probability is at most `delta`.

### 2.3 Refinement phase

Start with `T_0=2`. At each step request

\[
\tau_t=\frac{T_t}{16\sqrt{1+T_t^2}},\qquad T_{t+1}=T_t/2.
\tag{3}
\]

If the actual tangent is at most `T_t<=2`, then
`tau_t/|a|<=T_t/16`. Equation (1) yields

\[
\tan\angle(y,u)
\le\frac{(1/4+1/16)T_t}{1-T_t/16}
\le\frac{5}{14}T_t<\frac12T_t.
\]

Continue until `T_t<=epsilon/8`. The work is

\[
\sum_t\tau_t^{-p}
=16^p\sum_t(1+T_t^{-2})^{p/2}=O_p(\epsilon^{-p}),
\]

because the inverse tangent grows geometrically. The number of actions is
`O(log(1/epsilon))`.

### 2.4 Amplitude and the reusable inverse

With the refined unit vector `uhat`, request one action at tolerance `epsilon`
and clip its Rayleigh quotient to `[1,2]`, defining `lambdahat`. If
`s=sin angle(uhat,u)<=epsilon/8`, clipping cannot increase amplitude error, and

\[
|\widehat\lambda-\lambda|
\le(\lambda+\beta)s^2+\epsilon
\le\epsilon+(9/4)(\epsilon/8)^2.
\tag{4}
\]

Let `B_0=lambda u u^T`. For every `mu>=1`, the resolvent identity and
`beta<=1/4` give

\[
\|(\mu I+B)^{-1}-(\mu I+B_0)^{-1}\|
\le\frac\beta{\mu(\mu-\beta)}\le\frac43\beta.
\]

The exact rank-one inverse of `mu I+B_0` has coefficient
`c(lambda,mu)=lambda/[mu(mu+lambda)]`. On the admitted rectangle,
`c<=2/3` and `|partial c/partial lambda|=1/(mu+lambda)^2<=1/4`.
The distance between the rank-one orthogonal projectors is exactly `s`.
Consequently

\[
\|G_\mu-(\mu I+B)^{-1}\|
\le\frac43\beta+\frac23s+\frac14|\widehat\lambda-\lambda|
\le\frac\epsilon2+\frac{9\epsilon^2}{1024}<\epsilon.
\tag{5}
\]

This single deterministic bound after the acquisition event covers every
future shift and load. No union bound over future queries is needed.

## 3. Precision-work lower bounds and the certification obstruction

The following derivation is elementary but its originality is not established.
The foundations collaborator has the main formal lower-bound treatment.

Consider `B=theta uu^T` versus `B=0`, with a uniformly random unit `u`.
On a query `v` at tolerance `tau`, the rank-one source can return zero whenever
`|u^T v|<=tau||v||/theta`. Along an all-zero transcript, the entire adaptive
query sequence is fixed by the algorithm's own randomness; the hidden `u`
has not been revealed. For each fixed query direction, spherical concentration
bounds failure of masking by `2 exp(-c n tau^2/theta^2)` (with universal constants
and harmless small-dimension changes).

If `W=sum tau_i^(-p)`, use the elementary bound

\[
e^{-z}\le C_p z^{-p/2}
\]

to obtain a total probability of any unmasked answer at most
`C_p theta^p n^(-p/2) W`. Hence constant-confidence discovery requires

\[
W=\Omega_p(n^{p/2}\theta^{-p}).
\tag{6}
\]

For a theorem restricted to the one-large-mode class, compare two unknown
directions (or condition on being in that class), not `B=0` as an admitted
parameter. The all-zero source transcript can be valid for many distinct
directions. Their inverse operators have a constant separation, so a single
compiled inverse cannot satisfy all of them. This supplies the same lower
scale for the promised class.

Even after the direction is known, two amplitudes separated by `C epsilon`
have inverse operators separated by more than `2 epsilon` for an appropriate
fixed constant `C`. If every requested tolerance exceeds half that amplitude
separation, a common midpoint response is admissible on every query. Therefore
at least one request needs tolerance `O(epsilon)`, costing `Omega(epsilon^(-p))`.
Together with (6), the constant-confidence upper theorem is polynomially sharp:
`Omega(n^(p/2)+epsilon^(-p))` versus `O(n^(p/2)+epsilon^(-p))`.

This last scalar argument is meant for sufficiently small epsilon so the two
amplitudes remain in `[1,2]`; fixed larger epsilon changes constants only.

If the numerical tail promise is removed, compare a purported completed model
with one that has an additional unknown rank-one mode of amplitude
`theta=C epsilon` in an unseen orthogonal direction. Resolvent operators differ
by more than `2 epsilon` at `mu=1`, for appropriate `C` and sufficiently small
epsilon. Equation (6), now in the remaining ambient dimension, forces

\[
W=\Omega_p(n^{p/2}\epsilon^{-p}).
\tag{7}
\]

Thus learning or validating that **no other epsilon-relevant mode exists** is
more expensive than refining an already located large mode. The positive
theorem does not supply such a certificate. A naive high-precision residual
probe upper bound can also be too conservative for a full-rank small tail;
no matching general self-certification upper theorem is claimed here.

## 4. Strong conventional comparison and corrected failed comparison

The Noisy Power Method already treats adaptive perturbations and separates total
noise from noise projected on the unknown principal subspace. Its random-start
conditions explicitly include an inverse-square-root ambient dimension factor.
With only a norm bound on adversarial noise, its sufficient uniform precision
is of order `min(epsilon,1/sqrt(n))`, not `epsilon/sqrt(n)`.

Consequently a fixed-precision power implementation with a fixed spectral gap
has precision work `O_p((n^(p/2)+epsilon^(-p)) log(n/epsilon))`. The variable
schedule above avoids spending the strictest precision at every step; this
removes logarithmic repetition. It does **not** supply a polynomial improvement
over the strongest conventional method. An initial comparison using the product
`epsilon/sqrt(n)` as baseline was overly conservative and has been corrected.

Randomized Nyström preconditioning already constructs low-rank preconditioners
from source actions, with rank controlled by effective dimension, and includes
adaptive rank selection. It should remain a primary conventional competitor.
This note does not improve its generality or establish a practical advantage.

The model here has uniformly well-conditioned shifted systems:
`mu I+B` has eigenvalues in `[mu-beta,mu+2]`. Ordinary iterative solvers therefore
already solve one load quickly. The point is reusing an experimentally learned
formula for many subsequent loads without returning to the source. A practical
advantage requires enough later tasks to amortize acquisition and a genuinely
expensive experimental source. In a real arithmetic implementation the learned
formula is `O(n)` per full-vector output; it cannot remove output cost.

## 5. Finite arithmetic scope

The proof above uses exact arithmetic outside source errors. All errors in
products, vector sums, dot products and normalization can instead be included in
the effective `tau` budget by reserving, for example, half the budget for them.
On successful discovery paths, denominators are bounded below at scale
`n^(-1/2)`; on refinement paths they are bounded below by a constant.
Conventional scaled vector arithmetic therefore only requires a number of
mantissa bits polynomial in `log n + log(1/epsilon)` to meet the chosen budgets.
However, this note does not contain a fully specified correctly rounded
implementation or bit-operation theorem. The included program uses float64.
The real-arithmetic source-action and precision-work theorem is the proved scope.

## 6. Numerical illustration

`variable_precision.py` creates an unknown top mode of eigenvalue 1.4 plus a
generic fixed tail `P diag(d) P`, `|d_i|<=epsilon/8`. The tail is generally full
rank on the complement. The learner only receives source outputs and supplied
class constants. Experimental errors have their maximum permitted norm and are
directed to reduce the mode overlap and increase the tail component.

The comparison fixes every baseline action to the **minimum tolerance actually
required anywhere in the variable schedule**. This is a strong, fair
fixed-precision baseline for this construction, not a polynomially weaker
product-tolerance straw baseline. Both receive the same starting vectors.

Selected output (`p=2`, one successful start in these seeded instances):

| n | epsilon | source actions | variable work | fixed work | measured inverse error at mu=1 |
|---:|---:|---:|---:|---:|---:|
| 64 | 0.10 | 14 | 1.702e6 | 1.468e7 | 0.01269 |
| 128 | 0.10 | 15 | 1.984e6 | 1.573e7 | 0.01266 |
| 256 | 0.10 | 15 | 2.546e6 | 1.574e7 | 0.01268 |
| 128 | 0.03 | 17 | 2.296e7 | 2.852e8 | 0.003752 |
| 128 | 0.01 | 18 | 9.008e7 | 1.208e9 | 0.001247 |

These large work numbers include conservative proof constants. They are not
measured runtime or sample counts. All ten runs (five variable and five fixed)
passed the finite direct operator-norm check against (5). This numerical check
does not establish the universal theorem, robustness for every error sequence,
or a scientific application advantage. The analytical proof supplies the stated
universal result.

## 7. Primary sources

1. Moritz Hardt and Eric Price, **The Noisy Power Method: A Meta Algorithm with
   Applications**, NeurIPS 2014. Author PDF:
   https://www.mit.edu/~ecprice/papers/npm.pdf . Relevant locations: Figure 1,
   Corollary 1.1 and its discussion, Theorem 2.4. This supplies the strong
   conventional method and the random-start noise distinction. The explicit
   variable-precision schedule here is proved directly above; no novelty claim
   for the schedule is made.
2. Zachary Frangella, Joel A. Tropp, and Madeleine Udell, **Randomized Nyström
   Preconditioning**, SIAM Journal on Matrix Analysis and Applications 44(2),
   718--752 (2023), DOI 10.1137/21M1466244. Author PDF:
   https://tropp.caltech.edu/papers/FTU23-Randomized-Nystrom-SIMAX.pdf . Relevant
   locations: Theorem 1.1, Corollary 1.2, and section 5.4 on adaptive rank choice.

Retrieval was performed on 31 October 2026. Source webpages and PDFs support
the attribution/comparison claims only; the theorem in this note is separately
proved and scoped above.
