# Independent cost-envelope delta review

**Status: PASS for the stated envelope and resource-class consequence.**
23 October 2026, Australia/Brisbane.
Reviewer branch: `/root/cycle11_scalar_pressure`.

## Exact scope

This is a bounded independent check of the new general-tilt resource envelope,
its closed optimizer, the transition to the dimension ceiling, the b=0 formula,
and the interface linking the retained Cycle10 code to the sublinear-depth
resource class. It is not a repeat audit of the inherited arbitrary-reference
coding theorem, not a review of every other new statement in the manuscript,
and not external certification or a historical-priority finding.

## Reviewed version

The main source was being edited concurrently. This review is bound to the
following frozen snapshots and the exact selected-section hash, not to later
unreviewed versions:

- `reviewed/COST_AND_RESOURCE_SECTIONS.tex.txt` — 6751 bytes; SHA256 `36cb022cc3d94d48d082638122ccee7b7b7172bacd056f114eea0ce3c0e1dfd7`.
- `reviewed/ENTROPY_DRIFT_AND_DEPTH_COST.tex` — 35221 bytes; SHA256 `3afdc8e4b7028eac14317a8bb875b88698eb04201c8b36e8f4b8fa8d751fd2d8`.
- `reviewed/INHERITED_CODE_DEPTH_BUDGET.tex` — 7228 bytes; SHA256 `dddc42af6fa44d8e486d7dec806f9ec1ba6c0f7deda663950c7e51850d9b04a2`.

The earlier observed typographical form `r_{A_n}^{,2}` in the depth-budget
source was reported to the principal and is absent from the reviewed corrected
version. The factor is `r_{A_n}^2`, as required by the inherited positive-block
bound. This is a notation repair, not a change to the resource argument.

## 1. General-tilt resource envelope

For a reliable unassisted code with limiting mean-depth expenditure at most
v>=0, the theorem's finite-N input entropy inequality and the general tilt give,
for every fixed lambda>0,

    R <= [ln f_lambda(b)+lambda v]/ln 2,
    f_lambda(b)=3b+(1-b)(exp(lambda)+2exp(-lambda)).

Here a finite initial mean is retained, and the actual tau_pi has mean 1/2.
The result uses the same all-N input state and one evolving bath; no repeated
fresh-channel factorization is needed. If the depth sequence does not converge,
the statement remains valid when `limsup Delta_N/N <= v`. Thus the natural
precise interpretation of “limiting expenditure at most v” is a limsup bound.
For asymptotic reliable rates expressed as a liminf, the inequality still follows
pointwise before taking limits.

The endpoint lambda=0 is justified by continuity from positive lambda, or simply
by the qutrit dimension bound. `f_0=3`, independent of b. Taking the infimum over
lambda>=0 therefore yields exactly the stated **upper envelope** C_b(v).
No equality or achievability of this envelope was found in the source, and none
follows merely from solving its minimization.

## 2. Interior optimizer and transition

Put `a=1-b` and work with natural-log objective

    F(lambda)=ln[3b+a(exp(lambda)+2exp(-lambda))]+lambda v.

For a>0 its second derivative is the strictly positive variance of the support
{-1,+1}, additionally with a zero point when b>0, under positive exponential
weights. Therefore F is strictly convex for all finite lambda.

At lambda=0,

    F'(0)=v-a/3.

Consequently the constrained minimum is at lambda=0 when v>=a/3. The value is
log2(3), exactly as stated. At v=a/3 the endpoint is the unique minimizer when
a>0. If a=0, f_lambda is constantly 3: lambda=0 is a minimizer for every v>=0,
and for v=0 every lambda is a minimizer. The text does not incorrectly assert
uniqueness in that degenerate case.

For 0<=v<a/3, F'(0)<0 and F'(lambda)->1+v>0 as lambda->infinity. Strict
convexity gives one interior minimizer. Setting z=exp(lambda) in F'=0 gives

    a(1+v)z^2+3bv z-2a(1-v)=0.

Its positive root is exactly

    z=[sqrt(9b^2v^2+8a^2(1-v^2))-3bv]/[2a(1+v)].

The parameter range guarantees v<1, so the positive root exists. Evaluating
the quadratic at z=1 gives 3v-a<0, and its leading coefficient is positive;
thus this root has z>1 and belongs to the required lambda>0 domain. At v=0,
z=sqrt(2), giving C_b(0)=log2[3b+2sqrt(2)a]=c(b).

## 3. Endpoint b=0

For b=0, the optimizer is

    z=sqrt[2(1-v)/(1+v)],  0<=v<=1/3.

Write p=(1+v)/2. The optimizing three-symbol Gibbs weights are
`(1-p,p/2,p/2)`, with average displacement `2p-1=v`. Substitution into the
objective gives

    C_0(v)=h2(p)+p=h2((1+v)/2)+(1+v)/2.

At v=1/3, p=2/3 and the value is log2(3), agreeing continuously with the
constant branch for v>=1/3. This is an entropy/dimension upper comparator;
it is not a proof that reliable quantum codes attain all these rate-cost points.

## 4. Exact resource-class linkage

The main source defines Q_sub using the **actual tau_pi**, vanishing full-diamond
error, all N forward calls, and final mean depth o(N) on the encoded maximally
mixed logical input. This is explicitly an added resource constraint.

The upper follows because the initial mean is fixed at 1/2, so the displacement
per call tends to zero in that class. The reliable-transmission input-entropy
lemma and the new all-input entropy--drift upper then give R<=c(b). There is no
charge-preserving or isometric-encoder restriction in this upper interface.

The matching retained code has fixed beta, k and rho before the outer horizon
n; it uses N=nk calls. The new depth-budget lemma invokes the **actual joint
operator overflow bound** for the inherited isometric encoder, with

    delta_n=2 r_{A_n}^2 (n+1)^(-16),
    A_n=floor(log2(n+1)),  r_{A_n}<4(n+1).

This is strong enough for a supremum over logical inputs. The proof does not
infer a uniform statement from average-code overflow, and does not confuse
the mathematical auxiliary normalization with the physical encoder.

The low-depth part has actual support below A_n+N after N calls. Combining
this with overflow gives the mean contribution at most

    H_n+(A_n+N)delta_n.

For the actual depth-diagonal tau_pi, the high-depth part has mass
`3^(-(A_n+1))` and first moment `(A_n+3/2)3^(-(A_n+1))`. Conservation bounds its
final contribution by

    (A_n+N+3/2)3^(-(A_n+1)).

No bath truncation, measurement, reset or postselection is performed. This is
a positive analytic decomposition of the actual initializer.

Since nu=log2(3)>1, these additional terms are respectively O_k(n^-13) and
O_k(n^(1-nu)), hence o(1). Fixed inner rank and Lyapunov constants give
H_n=O_beta(log n). The same code therefore belongs to Q_sub, in fact with a
uniform logical-input mean-depth bound. A retained reference does not alter
this bath-marginal bound; decoder operations do not change the unconditioned
bath marginal. Padding at most k-1 calls changes depth by at most k-1 and does
not affect already emitted marginals, so it does not spoil the rate/error or
o(N) resource condition.

The all-normal pointwise **reliability** guarantee is distinct from the new
mean-depth statement, which is asserted at tau_pi only. The explicit normal
infinite-mean initializer in the contribution correctly prevents extending the
latter moment statement to every normal initializer.

## 5. Sharp-order conclusion and limitations

Combining the retained lower with the new upper gives

    (ln 2)/2^20 * beta^2
      <= Q_sub(beta,tau_pi)-3/2
      <= log2(1+d_* beta^2),
    d_*=3/(2sqrt(2))-1>0,

for every fixed 0<beta<=1/32. Thus the small-angle excess is Theta(beta^2),
with beta varied only outside the coding limit. The constants are positive and
independent of beta. Allowing arbitrary temporal length in the upper is a real
strengthening over the previous fixed-window construction.

This proves the order in the specified resource class, not the exact leading
coefficient, exact resource-cost curve, unrestricted capacity, feedback capacity,
or efficient code realization. The source states these distinctions explicitly.
A reliable code outside this resource class may spend positive linear depth;
the present conclusion does not exclude it. Nor does depth growth alone prove
extensive logical-reference leakage or complementary entropy.

## Bounded new algebra diagnostic

`cost_envelope_check.py` independently substitutes the closed root, checks
stationarity/endpoint dominance and the b=0 entropy identity in 42 declared
cases at 90 decimal digits. The analytic convexity proof supplies the all-
parameter result; the diagnostic is a guard against algebra/sign transcription.
Its exact output and reviewed source identities are in `cost_envelope_check.json`.
Observed script-body runtime was approximately 0.033 seconds. Discovery,
inference, integration and total review costs are unknown.

No old scientific suite or capacity audit was rerun. No substantive correction
to the selected envelope or resource-class claim is requested.
