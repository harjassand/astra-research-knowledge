# Actual-file receiving check: spatial action, stopped moments and carrier work

30 October 2026. Completed by the existing physical-mechanism role. This
receipt extends the earlier spatial-tracking review to the actual saved work
note and receives its binding clarifications. No new worker, fixture or
simulation was added; predecessor inputs and the earlier receipt remain
unchanged.

## Exact reviewed versions and verdict

The following exact inputs were read in full and preserved byte for byte in
this directory. `SPATIAL_WORK_REVIEWED_INPUTS.json` records their source paths,
sizes and snapshot names.

| Actual input | SHA256 |
| --- | --- |
| `SPATIAL_TRACKING_AND_WORK_CLARIFICATIONS.md` | `220c8232cb3f97fb352d8e76b60fa9b855d219fb5e9c930925941c71db050241` |
| `SPATIAL_ACTION_WORK_AND_APPARATUS_SCOPE.md` | `e2c45f5ff21e15e69cca4a815a7ecf322e5b7ababe95ce9c951301a4ead7e904` |

The binding note accompanies the previously reviewed tracking theorem,
SHA256 `dd815be2bc16a734d377f8a141dc117383ff6c6357650a690e55f3d43a2d84ae`.
The original review and its exact snapshot are preserved separately. The
present check uses the accepted elastic-layer and finite-cell suppliers as
dependencies; it does not reopen their separate validation. The actual
round-10 `PARTIAL_REFRESH_FORCE_WORK.md`, SHA256
`b9e869b0daa990896a0ed316d7040a40438d93868da6701e7ac3a67913215bbb`,
was reread to verify the work identity against the true displacement port.

**Verdict: accepted at the stated mathematical and physical-model scope.**
No remaining load-bearing error was found in the stopped second-moment
argument, retained-memory work formula, sustained-mean lower bound or
interior-density action contraction. The binding clarifications resolve the
specific requests in the earlier spatial-tracking receipt. Acceptance is
for signed mean carrier-force work and the declared conditional readout,
source, force and initialization interfaces. It is not an acceptance of an
order-volume complete apparatus-energy budget or a manufactured instrument.

## 1. Receipt of the binding corrections

All four changes are substantive and correctly scoped.

* The thermal supplier is now explicitly joint: sources for distinct
  carriers, rows and periods are independent conditional on the available
  past. A family of fresh scalar marginals alone would not supply the joint
  volume exponent. The common-noise counterexample in the earlier receipt
  remains a genuine exclusion from the theorem.
* The direct interpolation argument now uses the native martingale domain
  $\max_y\sup_t|h_y(t)|\le N^\gamma$, with $1/2<\gamma<1$ and failure exponent
  $N^{1+2\gamma}$. This supplies both the small spatial sampling error
  $O(N^{\gamma-1})$ and an adequate domain for logarithmic-mode Fourier
  evaluation. Raw absolute activity alone has not been substituted for it.
* The complete held force, including the error represented by $\eta$, is
  measurable at the start of the previous block. The observation envelope
  $C/K_N$ can itself consume order-$N^2$ carrier work. The $O(NK_N)$ term is
  the filtered martingale contribution, with no general noise-only promise.
* The programmed shear is the row-mean horizontal component. Its vorticity
  does not replace the native within-row and vertical contributions. Density
  comparisons use the same actual native force and initial law.

These clarifications should continue to travel with the preserved original
tracking and work notes. They do not require changing their reviewed bytes.

## 2. Stopped second moments: why future success is not being conditioned on

Work row by row, conditional on any admissible fixed kinetic class. Write
$\alpha_y=(\mu_y/p)K_N\delta_N$. Its deterministic Green kernel satisfies

\[
 \sum_j g_{y,j}\le C/\alpha_y,
 \qquad \sum_j g_{y,j}^2\le C/\alpha_y,
 \qquad \alpha_y\sum_j g_{y,j}\le C.
\]

The unknown values are fixed proof coefficients; their evaluation is not an
operation required of the controller. Stop the martingale innovations
predictably before the first observation-envelope violation or proposed
cap activation. Use the convolution of these stopped innovations as a
comparison process at every deterministic potential endpoint. It agrees
with the physical recursion up to the first failure. Its second moment is
bounded without conditioning on eventual success:

\[
 E\left|\sum_j g_{y,j}\xi^{\rm stopped}_{y,m-1-j}\right|^2
 \le {C\delta_N\over N}\sum_j g_{y,j}^2
 \le {C\over NK_N}.
\]

Orthogonality here is the martingale-difference identity in the actual
filtration. Independent native row histories are not needed. The joint
thermal-source premise supplies the spatial theorem; the scalar estimate
above also uses its correct row marginal. If a failure is detected inside a
block, the same argument uses stopped stochastic integrals rather than
conditioning a completed block on a later event.

The pathwise bounded target drift contributes at most
$C\delta_N\sum_jg_{y,j}\le C/K_N$. The stopped observation term contributes
at most $\alpha_y(C/K_N)\sum_jg_{y,j}\le C/K_N$. These estimates do not ask
that the drift or observation bias be independent of the native state.

For the analytic current corrector, the globally capped mechanical system
has the actual pathwise decomposition

\[
 z_{y,k}=G_{y,k}+N\sum_{i<k}M_y^{k-1-i}d_yF_{y,i},
 \qquad |z_{y,k}-G_{y,k}|\le CNa_N.
\]

The unforced $G_{y,k}$ has Gaussian marginal covariance $NI$ under the
declared preparation, even though it need not be independent of feedback.
On a polynomial number of cells its squared maximum has expectation
$O(N\log N)$. Consequently

\[
 E\sup_m|c_{y,m}|^2
 \le C\left({a_N^2\over N^2}+{\log N\over N^3}\right).
\]

The factor $\alpha_y\sum g_{y,j}$ is bounded, so convolution with the
corrector does not amplify this order. The final subtraction $e=e'-c$ has
the same bound. This establishes the right-hand side of work-note (3) for
the stopped comparison.

There is also a valid unconditional completion. The actual force remains
capped after failure. Native absolute counts are bounded by a bounded-rate
counting process with polynomial moments over the horizon. The specified
target has bounded first derivatives and therefore at most linear growth
in those counts. Stable mechanical states and their summed displacements
also have polynomial fourth moments under a capped force. Thus, for the
whole-protocol failure event $H_N$,

\[
 E[e_{y,m}^2\mathbf1_{H_N}]
 \le (Ee_{y,m}^4)^{1/2}\Pr(H_N)^{1/2}
 \le \operatorname{poly}(N)\Pr(H_N)^{1/2}.
\]

The already established super-volume failure bound makes this
superpolynomially small. On the complementary event one bounds the physical
error by the unconditioned stopped comparison. This proves the claimed
unconditional second-moment estimate without changing a martingale law by
postselection.

On success the force is the displayed linear command; on failure it is
bounded by $a_N$. Therefore

\[
 EF_{y,m}^2
 \le {CK_N^2\over N^2}
       \left(Ee_{y,m-1}^2+{C\over K_N^2}\right)
       +a_N^2\Pr(H_N)
 \le {C\over N^2}+{CK_N\over N^3}+o(N^{-2}).
\]

The corrector terms are smaller under the stated parameter choice and
$K_N=o(\sqrt N)$. Arbitrarily large uncapped force faults would invalidate
this completion; they are expressly outside the actual theorem.

## 3. The work formula retains the real momentum term

For one row, let $Z_m=z_{mL}$ and use the work-note notation $Q=M^L$,
$v=\sum_{j<L}M^jd$, and $w=k^T(I-Q)$. The exact physical cell gives

\[
 Z_{m+1}=QZ_m+NvF_m+\Xi_m,
\]

\[
 \Delta A_m+k^T(Z_{m+1}-Z_m)
   =N\mu L F_m+\text{fresh thermal sum}.
\]

True work is $F_m\Delta A_m$. It is not force times the corrected current.
The complete old-force filtration gives $E(F_m\Xi_{m-1})=0$, whereas
$E(F_mQZ_{m-1})$ generally survives. Substituting the previous block
recursion yields exactly

\[
 \begin{aligned}
 EW_y={}&N(\mu_yL-k_y^Tv_y)\sum_m EF_{y,m}^2\\
 &+Nw_yv_y\sum_mE(F_{y,m}F_{y,m-1})\\
 &+\sum_{m\ge1}E[F_{y,m}w_yQ_yZ_{y,m-1}].
 \end{aligned}
\]

The zero initial force removes the separate initial-state term. The sign
and indices in work-note (5) are correct. In particular, the last term
cannot be set to zero merely because future thermal sources are fresh.

Uniform cell stability gives $|kv|+|wv|\le C$ and $\|Q\|\le Ce^{-cL}$.
Cauchy--Schwarz bounds the adjacent-force sum by
$S_y=\sum_mEF_{y,m}^2$. The capped-state estimate gives the explicit
remainder bound

\[
 \left|\sum_{m\ge1}E[F_{y,m}w_yQ_yZ_{y,m-1}]\right|
 \le CB a_Ne^{-cL}(\sqrt N+Na_N).
\]

It stays exponentially small after summing all $N$ rows. Hence

\[
 N(\mu_yL-C)S_y-\varepsilon_y
 \le EW_y\le N(\mu_yL+C)S_y+\varepsilon_y.
\]

This verifies both the retained-memory formula and its claimed large-block
consequence. It does not assert exact finite-block positivity. Fixed row
parameters with warranted uniform positive mobility/stability margins are
load-bearing; arbitrary particlewise pulse-angle disorder is not supplied.

For $B=O(N^2/L)$, the force-square estimate gives order $N$ work per row
from bounded drift or observation bias, and order $K_N$ from the filtered
martingale term. Thus the full carrier-force expectation is
$O(N^2+NK_N)$. Setting the force to zero on a terminal partial block leaves
zero drive work there; the actual remaining displacement is still counted.

## 4. Sustained-mean lower bound and the carrier-number comparison

Let $J_y=EA_y$ over the complete-block physical horizon
$T_*=BLp=\Theta(N^2)$. Summed true current obeys

\[
 J_y=N\mu_yL\sum_mEF_{y,m}-r_y,
 \qquad r_y=k_y^T(EZ_{y,B}-EZ_{y,0})=O(Na_N).
\]

Cauchy--Schwarz gives

\[
 S_y\ge{(J_y+r_y)^2\over B N^2\mu_y^2L^2}.
\]

Combining this with the two-sided work bound and the uniform positive
mobility bounds gives, for a fixed macroscopic horizon,

\[
 EW_y\ge {cJ_y^2\over N^3}-{Ca_N^2\over N}
                 -\operatorname{poly}(N)e^{-cL}.
\]

For example, use $(J_y+r_y)^2\ge J_y^2/2-r_y^2$; no assumption that
every individual mean current is bounded away from zero is required. On
summing rows and writing $v_y^A=J_y/N^2$, this proves the stated
$cN\sum_y(v_y^A)^2-o(N^2)$ lower bound. A force-free short terminal interval
changes the relevant mean by an endpoint term of the same harmless order.

With $R_N$ carriers per row at the same finite-cell mobility port, replace
$N$ by $R_N$ in its response and work identities. The same order-one row
flow requires order $N^2/R_N$ work per row, hence $N^3/R_N$ for a positive
fraction of rows. This is a real carrier-number/drive-work tradeoff, not a
work saving at fixed hardware. Its lower bound is about a sustained mean,
not a future rare-history event selected after deployment.

For unknown fixed classes, apply the calculation conditional on a class
with the warranted initial law, or retain uniform lower/upper mobility
constants. Averaging a random mobility into a coefficient without that
argument would be unjustified; the reviewed note does not do so.

## 5. Action contraction and the preserved density law

For the concrete exclusion rate convention in the work note, the native
diffusive flux is $-D_\alpha\partial_\alpha\rho$ and the weak-force drift is
$D_\alpha\chi F_\alpha$. Right/left rate $D_\alpha$ gives noise mobility
$2D_\alpha\chi$, so the displayed action coefficient $1/4$ is consistent.
The previously read empirical-current theorem of Bertini et al.,
<https://arxiv.org/pdf/math/0512394>, is an external LDP input with its own
initial-law and topology premises; the source-bracket bound alone is not an
LDP proof.

For $\psi(y,t,z)=v(y)t$, the output instantaneous horizontal row mean is
$v(y)$. At a fixed admissible output history its native preimages are

\[
 j^{\rm native}=(j_x+u(y,t),j_y).
\]

This modification has zero spatial divergence, so it changes neither the
continuity equation nor the density history. With $w=(D_x\chi)^{-1}$, the
only variable quadratic is

\[
 \int_0^1 w(a_x+u)^2dx
 =\int_0^1wa_x^2dx+2u\ell+u^2r.
\]

Its minimizer is $u=-\ell/r$ and its minimum subtracts $\ell^2/r$.
The sign, factor and rowwise weighting of work-note (2) are therefore
correct. Nonnegativity follows directly from weighted Cauchy--Schwarz.
This is a pushforward of the native path action, not restriction of native
current to the output constraint. Minimization over all output currents
recovers the native density-path action because every native current has
an implemented image.

The explicit algebra is accepted for densities separated from zero and one,
as the note stipulates. At boundary densities, use the actual lower
semicontinuous rate and preimage contraction, not formal division of
possibly divergent $\ell$ and $r$. The auxiliary density contributes the
physical offset $+1$; it does not change the exclusion mobility to
$\chi(\rho+1)$. The nonlinear target uses the executed smoothing and the
full contraction theorem rather than this special quadratic formula.

Neither this action calculation nor exponential equivalence implies a CLT,
finite-$N$ equality of composite density paths, or the previous round's
rare-arming total-variation statement. The reviewed text keeps these scopes
separate.

## 6. Physical and retained-record limits of the acceptance

The work result is for signed actual force work on the charged carriers.
It is not, by itself, a bound on every unrecovered positive actuator
exchange, field-source loss or the complete apparatus budget. The reviewed
ledger expressly includes the missing preparation, fresh-source retirement,
sensing, clock, logic/communication, switching/field and reliability terms.
Its order-$N^2$ estimate controls only the carrier-drive term. Energy
recovery and double counting require an actual apparatus ledger.

The sensing contract is also an assumption with a real supplier obligation.
Common held timestamps, the complete polarization contribution to row
displacement, actual conditional noise tails and whole-protocol failure
superexponential at speed $N^2$ are required. A low-frequency spectrum or
fixed confidence level does not establish that contract. The work note
explicitly says that no end-to-end reliable logical apparatus was built in
this round; acceptance does not weaken that limitation.

The conditional statements apply only when conditioning on an old record
retains the declared initial-law, freshness, source, mobility and readout
hypotheses. An old record exposing every exact prepared relative coordinate
does not retain the bounded-density preparation premise. Future bath-noise
postselection is not allowed. Unknown fixed-class path actions must be
treated conditionally or as an actual mixture, rather than replacing them
by the action of an averaged coefficient. These restrictions were already
present in the supporting accepted inputs and remain binding.

Ordinary feedback is a strong comparator at this port. The candidate
addition is the complete physical-model conjunction stated by root, not a
new generic governor, a newly discovered thermodynamic bound, or historical
priority for active current control. The supplied carrier layer preserves
native bulk histories by isolation and asymptotically uniform added density;
it does not accomplish material advection or useful passive work transfer.

## Closing status

The two exact reviewed versions are accepted together, with the preceding
conditional and resource scope. No further source edit, new test or optional
predecessor review was required for this receipt. The constructive ordinary
gear and governor files, their checks and the earlier receiving review remain
unchanged.
