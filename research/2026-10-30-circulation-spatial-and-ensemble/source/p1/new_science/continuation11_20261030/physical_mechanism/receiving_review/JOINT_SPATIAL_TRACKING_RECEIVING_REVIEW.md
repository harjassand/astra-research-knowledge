# Actual-file receiving check: joint spatial current tracking

30 October 2026. Review by the existing physical-mechanism role. No new
workers, simulations or fixtures were added. The constructive native-gear
alternatives were completed before this receiving check.

## Exact reviewed input

`JOINT_SPATIAL_TRACKING_AND_NONLINEAR_PROGRAM.md`

SHA256:
`dd815be2bc16a734d377f8a141dc117383ff6c6357650a690e55f3d43a2d84ae`

The exact bytes are preserved as
`JOINT_SPATIAL_TRACKING_AND_NONLINEAR_PROGRAM_dd815be2bc16.md` in this
directory, with `JOINT_SPATIAL_REVIEWED_INPUT.json`.

Supporting inputs actually read in this check:

- `ELASTIC_CARRIER_LAYER_AND_DENSITY_LAW.md`, SHA256
  `7f3ecd1fcc7ac70b451fe10a206fd0df17d0bc679dbd90e7f85bc307ea31606a`;
- its binding `ELASTIC_LAYER_CORRECTIONS.md`, SHA256
  `b8b8dcf06013b559b558499aa1428117f22c83516add9440a16e211bc18ca72e`;
- the actual round-10 `UNTUNED_PARTIAL_THERMAL_CARRIER.md` and this role's
  preserved `PARTIAL_REFRESH_FORCE_WORK.md`.

The first two are dependencies, not a reopening of the sibling's separate
elastic-layer review. Bertini et al.,
<https://arxiv.org/pdf/math/0512394>, was reopened to check the empirical
integrated-current and volume-speed receiving scope. The native LDP remains
an explicitly supplied external theorem with its own initial conditions;
it is not derived by the source-bracket assumptions in this draft.

## Verdict

The normalized source calculation, stopped delayed recursion, directional-net
argument and enlarged force-cap scaling support the claimed joint tracking
at speed $N^2$. I found no factor-of-$N$ or stopping-time error in that core.
The explicit larger cap is material: the earlier one-row $K/N$ force cap
would not prove the new claim by this first-cap argument.

Acceptance is scoped to a genuinely joint fresh thermal-source contract.
Please state that contract explicitly as described in Section 4 below. The
actual forces must also retain the full-block-old information restriction
when the separate physical-work result is invoked. The draft does not yet
contain that separate work proof, so this receipt is not acceptance of a
future work file.

There is one useful correction to the optional discretization explanation:
raw activity/count bounds alone do not give the small spatial sampling error
claimed by a naive derivative estimate. The compact-set argument in the draft
is sufficient. Section 5 below supplies a direct source-martingale replacement
if a super-volume polynomial-domain argument is preferred.

## 1. Source normalization and row dependence

On macroscopic time, a native horizontal jump has normalized size $N^{-2}$,
while a row has intensity $O(N^3)$. Its predictable bracket is consequently
$O(N^{-1})$. Distinct rows have no simultaneous horizontal-count jump; their
states and intensities may still be arbitrarily dependent.

For the target, the exact finite jump quotient has entries bounded in absolute
value by $C(S_N)_{yj}+\delta_{yj}$. Positivity and the unit row/column sums give
a bounded Euclidean operator norm. This also works when different jump marks
use different intermediate values of $\psi_z$: replace a test vector by its
absolute values, apply that nonnegative matrix bound, and sum the column
intensities. A common deterministic Jacobian for all marks is not required.

The second-order coordinate drift is bounded by

\[
 C N^3 N^{-4}\sum_j(S_N)_{yj}^2\le C/N.
\]

Thus the vector variance proxy is indeed $C\|v\|_2^2/N$, without independent
native row laws. The range $|\theta|\|v\|_2\le cN^2$ follows from the actual
bounded jump. The draft correctly explains that its displayed exponential
bound means the compensated supermartingale inequality; if its right-hand
quadratic integral is random, it belongs inside the exponential compensator
unless a deterministic bound has first been taken.

## 2. Exact block recursion and predictable stopping

Summing the physical finite-cell identity over $L_N$ complete cells gives
gain

\[
 \alpha_y=(\mu_y/p)K_N\delta_N.
\]

The corrector sign is right: $e=e'-c$, so the actual old-error force contributes
$-\alpha e'_{m-1}+\alpha(c_{m-1}-\eta_{m-1})$. The summed fresh thermal variance
after division by $N^4$ is $O(L_N/N^3)=O(\delta_N/N)$, consistent with the
target source. A first zero block is harmless because
$K_N\delta_N\to0$; equivalently set the unused prehistory to zero and treat the
first block separately.

The response kernel is nonnegative and has a squared sum of order
$1/\alpha_y$, uniformly over the declared compact row parameter set. The
fixed unknown values are permissible proof coefficients; the controller does
not need to evaluate them.

Stop the innovations predictably before the first proposed capped command
or a past-record observation-envelope violation. The exact recursion and
its convolution agree with the physical process up to that stopping time.
For a fixed potential first-occurrence time the stopped convolution has the
same bracket bound; a union over times then bounds first occurrence. This is
not conditioning the innovations on eventual success.

The corrector envelope can be imposed by an event inclusion:

\[
 \Pr\{\text{large error}\}
 \le\Pr\{\text{bad corrector envelope}\}
   +\Pr\{\text{large stopped martingale convolution}\}.
\]

No conditional Gaussian law on the good-envelope event is needed. The
pathwise capped-state decomposition in the actual supplier applies even
after the stop. Its deterministic displacement is $O(Na_N)$, compared with
the Gaussian threshold $N^2/K_N$. For the concrete choice in the draft this
is safely smaller. The Gaussian tail exponent is $N^3/K_N^2$.

The preserved finite-cell within-period solution also bounds the *true*
partial-period displacement by $C(|z_k|+N|F|)$, with fresh neutral coordinates
included. This is the needed bridge between cell endpoints; the analytic
corrector is not an instantaneous measured current.

## 3. Volume exponent and cap calculation

For a unit direction at a block endpoint, the filtered bracket proxy is
$C/(NK_N)$ and its jump bound is $C/N^2$. Thus

\[
 \Pr\{|v\cdot U|>x\}
 \le2\exp[-c\min\{NK_Nx^2,N^2x\}].
\]

A $1/2$-net costs $5^N$. At the required spatial norm threshold
$x=\varepsilon\sqrt N/2$, the quadratic exponent is $N^2K_N$, not $NK_N$.
The net entropy $O(N)$ and polynomial number of blocks are negligible.
The stated $K_N=o(\sqrt N)$ is consistent with the bounded-jump range at
this threshold.

For a proposed cap activation the scalar threshold is
$x\asymp Na_N/K_N$. The scalar Bernstein exponents become

\[
 N^3a_N^2/K_N,\qquad N^3a_N/K_N.
\]

With $a_N=N^{-1/4}$ the first is $N^{5/2}/K_N$ and dominates volume when
$K_N=o(\sqrt N)$. The corrector exponent divided by volume is
$N/K_N^2\to\infty$. The observation-failure contract already has the required
volume speed. These facts justify the draft's first-cap estimate.

By contrast, $a_N=K_N/N$ would put this first-cap threshold at order one and
would give only exponent $NK_N$. That would not be a super-volume first-cap
proof for the stated gains. The revised cap is not cosmetic.

Within a block the deterministic normalized current increment is at most
$CNa_N\delta_N=o(1)$. The vector maximal martingale estimate gives exponents
$N^2/\delta_N$ and $N^{5/2}$ at a fixed spatial error. Both are super-volume.
Together with the actual partial-cell bound this proves full-time tracking,
not just a result on the held timestamps. It does not prove a CLT.

## 4. Make joint bath freshness explicit

The collective thermal innovations for different rows must be jointly fresh
with a uniformly bounded covariance operator; independent standard Gaussian
inputs across rows and cell periods are the direct sufficient supplier.
The preserved statement that each scalar innovation is a fresh standard
Gaussian, read as a marginal statement only, is insufficient for the spatial
theorem. Add an explicit sentence to the integrated apparatus statement.

The necessity is concrete. With identical row parameters, zero native target
and the same fresh scalar Gaussian used in every row, the row errors can be
identical. Their spatial normalized Euclidean error is then the one-row
error, whose probability has exponent $NK_N$, not $N^2K_N$. Every row's
scalar marginal cell law can still be correct. Independent initial row
states do not remove the later common-noise contribution.

If the phrase "fresh independent thermal coordinates" is understood to
include all rows in the actual supplier, this condition is already intended.
Writing it explicitly makes the actual volume theorem unambiguous and keeps
the earlier common-versus-independent control distinction intact.

## 5. Smoothing and discrete physical evaluation

The actual operation $S$ is the correct repair for nonlinear composition in
a weak current topology. Horizontal averaging maps the current distribution
continuously to a vertical distribution; analytic convolution maps it to
smooth functions. The specified nonlinear composition is continuous on
compact sets, while the raw $-h$ term is linear. With the actual native good
LDP and the stated compatible path topology, contraction therefore applies.

The first discretization route in the draft—uniform approximation on native
exponentially tight compact sets—is valid, using the usual exhaustion of
compact sets with arbitrarily large exit exponents. It must not be replaced
by one fixed good set with only $e^{-cN^2}$ failure.

For the alternative count-range sentence, distinguish two errors. An
exponentially accurate Fourier truncation controls convolution evaluation
on a polynomial raw count range. It does not by itself supply a small
row-sampling/interpolation error after nonlinear composition: the elementary
bound also contains the spatial derivative of $\psi(S h_N)$, and raw absolute
activity permits norms of $h_N$ growing as $N$ or larger under loose count
cutoffs. A direct small-error assertion needs another estimate.

A convenient constructive replacement follows from the native hypotheses
already supplied. For any fixed $\gamma\in(1/2,1)$, apply the native scalar
martingale maximum bound to each row on the macroscopic horizon. Its bounded
drift is $O(1)$ and its bracket is $O(1/N)$, so

\[
 \Pr\{\max_y\sup_{t\le T}|h_y(t)|>N^\gamma\}
 \le\operatorname{poly}(N)
       \exp[-cN^{1+2\gamma}].
\]

The bounded-jump branch has an even larger exponent for this range of
$\gamma$. This is super-volume. On this domain convolution and its spatial
derivatives are $O(N^\gamma)$, and the bounded derivatives of $\psi$ give
row-sampling error $O(N^{\gamma-1})\to0$. Exponentially accurate Fourier
truncation still gives the desired $o(1/K_N)$ evaluation accuracy. This closes
the optional direct-domain route without importing a stronger native current
topology or making a rare conditioning argument.

The prescribed $\psi=v(y)t$ fixes the **row-mean instantaneous horizontal
current** to $v(y)$. Its shear component has vorticity $-v'(y)$. The complete
output current retains the native within-row fluctuations and vertical flow;
its entire vorticity is not generally $-v'(y)$. The draft's final limitations
already preserve that distinction, but the word "component" would prevent
overreading the preceding sentence.

## 6. Physical work applicability: do not import the ideal diffusion identity

The separate ordinary-governor note has the exact diffusion-port identity
$EW=N\mu E\int F^2dt$. The present physical supplier is the partial-refresh
finite cell. Its true work is instead

\[
 W=\sum_{y,m}F_{y,m}\Delta A_{y,m},
\]

and the earlier delayed-block calculation gives, with
$S_y=\sum_mEF_{y,m}^2$,

\[
 EW=\sum_y N\mu_yL_NS_y
       +O\!\left(N\sum_yS_y\right)+\varepsilon_N,
\]

\[
 |\varepsilon_N|\le C\sum_y B_Na_N r_0^{L_N}
                         (\sqrt N+Na_N).
\]

This formula extends from the dilute count to $R=N$ directly; its proof is
algebraic and its remainder remains exponentially small in $L_N$. It keeps
the actual endpoint/momentum work. It is not an exact finite-block
nonnegativity statement.

Its information premise is stronger than "before this block's future
source": the complete actual force for block $m$ must be measurable with
respect to the start-of-block-$(m-1)$ record, or have the corresponding
conditional independence from the last block's innovation. This is intended
by the draft's held-record command. It must include any actuation-command
error folded into $\eta$. A new error chosen using the just-completed momentum
cannot silently inherit the old-force work cancellation.

For the held-record policy and the supplied observation envelope, the stopped
response yields the expected force-square bound

\[
 EF_{y,m}^2\le C/N^2+C K_N/N^3
                  +a_N^2\Pr\{\text{any failure}\}.
\]

Consequently the natural integrated operating-work upper bound is
$O(N^2)+O(NK_N)$ on the $N^2$ physical horizon. Worst capped-force polynomial
prefactors are negligible against the super-volume failures. A sustained
nonzero spatial field has an order-$N^2$ lower bound by the same actual-current
identity and Cauchy–Schwarz, with the bounded endpoint term retained.

One qualification is essential for a separate *noise-only* statement:
$|\eta|\le C/K_N$ can create a deterministic force error of order $1/N$ and
therefore order-$N^2$ work even when the target drift vanishes. To claim only
$O(NK_N)$ noise work, an observation error bound at the finer scale
$O((NK_N)^{-1/2})$ in normalized row displacement, or an adequate moment
condition, is needed. The current $O(N^2)+O(NK_N)$ loaded upper bound is not
affected.

Thermal preparation/retirement, the extensive carrier population, growing
relative-force bandwidth, local timestamped sensing and global convolution
evaluation remain real costs. This receipt does not identify them with
mechanical force work or certify an apparatus.
