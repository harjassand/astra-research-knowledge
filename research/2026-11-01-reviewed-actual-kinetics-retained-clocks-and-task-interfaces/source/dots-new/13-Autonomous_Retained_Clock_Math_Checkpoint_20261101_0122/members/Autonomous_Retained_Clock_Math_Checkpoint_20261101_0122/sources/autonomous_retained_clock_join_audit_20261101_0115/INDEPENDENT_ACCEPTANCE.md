# Independent full-join acceptance: autonomous retained clock

Date: 2026-11-01. Auditor: `producer-workspace/audit_sampled_clock_process`.

**PASS, actual-class mathematical theorem only.** No source correction is needed.
This accepts the full autonomous retained-clock join with the exact dependency
interfaces below. It does not extend a numerical parser, certify an executable,
remove rate-enclosure costs, or establish a physical processor/control service.

Frozen root:
`sampled_clock_process_pending_20261101/AUTONOMOUS_RETAINED_CLOCK_JOIN_ROOT.md`,
SHA-256 `93cde665c830d62ad5c89ae0ff99ae666b2c6912eca845c7a813a9f25bbed3b7`.

## 1. Exact dependency bindings and scope of acceptance

These sources were read and their indicated bindings were checked during the
audit before the workspace transport incident recorded in Section 10:

* Reference global odd-current/inverse/renewal theorem:
  `retained_state_renewal_clock_20261101/GLOBAL_ODD_MODE_AND_RENEWAL_CANDIDATE.md`,
  SHA `4a8110be17507c8f0552a6ff5553e7b8f5caecfc94808900a4a05fda31cc1892`.
* Its independent source-bound theorem acceptance:
  `retained_state_renewal_clock_20261101/audit_global_odd_renewal_20261101_0105/SOURCE_BOUND_ACCEPTANCE.md`,
  SHA `adae18f170a955bcd658d94e618425cd22dab7aaa114093036016b1f7f172837`.
  It accepts the actual reference global inverse-form construction and baseline
  domain receiving, NOT added circulation. This audit does not misattribute the
  circulation extension to that baseline receipt.
* Sharp neutral-vector theorem:
  `neutral_processing_clock_pending_20261101/NEUTRAL_VECTOR_AND_PATH_SHARP_V2.md`,
  SHA `8da465ed3817a2e5cf0088cd0efba23e056a148422bf5a3120b96606a960a403`.
  Its independent acceptance text was also read.
* Actual autonomous capacity source:
  `sampled_clock_process_pending_20261101/AUTONOMOUS_NEUTRAL_CAPACITY_ROOT.md`,
  SHA `17e122c905e45297967ee33c845577e55c9209b3481136181f4f4cdb1064c50a`.
* Its independent actual-model/capacity/count receipt, authored immediately
  before this audit:
  `autonomous_neutral_capacity_audit_20261101_0108/INDEPENDENT_PROOF_RECEIPT.md`,
  SHA `28776ab3f5e72d1012a6e0fdb1193c4e5af8e71f1205291d113dc8eb8c4c6f24`.
* Finite path root SHA
  `d1eb7f96cd68e1c681baa4907f888265dbd16a233096d9a345a53003d53e4979`,
  controlling path audit SHA
  `592b28cb65e75da7f4ea4274754147892c1e1cb56ddf3dc25cda6ae3afc73bfe`,
  and the frozen hysteretic join SHA
  `28afdb7a36927f4f2cca01727274edef91c7ac4d4d27acb5aaf4d88f40be376d`
  with audit SHA
  `8433eb17083ef430d3e94b82615aa86f220396eadb2958db5ce018d742178591`
  were independently audited earlier in this same thread. The present proof
  rechecks their constants and initialization in the nonreversible setting.

No experimental or numerical checks replace the mathematical argument here.

## 2. Actual circulation class and an explicit admissible subfamily

Let the received original generator be G0, with positive finite invariant
density proportional to rho=exp(-beta v(y)U(z)), constant SPD mobility
D=diag(1,M_z), and reference closed symmetric form E. Add the fixed autonomous
operator C=c dot grad with c smooth, compactly supported, c_y=0, and
div(rho c)=0. The original proper Lyapunov function has bounded-above G0 drift;
its added CV is bounded on compact support. Hence the perturbed SDE is
nonexplosive. Smooth local coefficients give its unique actual law.

The first-order perturbation is form bounded:

    |<Cu,v>| <= sqrt(beta)||D^(-1/2)c||_infinity sqrt(E(u))||v||_2.

Weighted divergence-freeness makes it skew. The forms E minus/plus <Cu,v> are
closed sector Markov forms on the common reference domain. Both annihilate
the constant on both sides; thus the actual semigroup and its adjoint preserve
1, and the SAME pi is invariant. Their SDE generators are G0+C and G0-C.
This is actual propagation, not just a formal skew symbol.

For the displayed subfamily

    c_z=a phi(y) chi(U(z)) J grad U(z),  c_y=0,

constant skew J gives `grad U dot J grad U=0` and
`trace(J Hess U)=0`. Thus both div_z c and c dot grad rho vanish. Coercivity of
U makes the support compact in z, while phi makes it compact in y. The field is
smooth and bounded at every fixed finite amplitude. Both h and psi depend only
on y, so Ch=Cpsi=0, including weak/form interpretation at slab joins. Since
C*=-C, neutrality also holds on the other side.

This class includes fixed state-dependent autonomous drifts, not an external
observation-driven feedback protocol. Parameter-dependent amplitude can grow
arbitrarily across models while remaining finite for each actual SDE; the error
proof uses cancellation, not a uniform bound on that amplitude. Model admission
and implementation costs are not thereby free.

## 3. Global mean-zero energy equations: where reversibility is and is not used

Reference connected ellipticity makes constants the only zero-energy functions.
Restricting to H0={f:integral f d pi=0} gives a positive injective reference
operator A. The accepted GLOBAL odd-current receipt, not a killed inverse
transplant, supplies the nonzero scalar trial psi=2h-1 and

    E(psi)/||psi||_2^2 <= k,
    k ||A^(-1/2)psi||_2^2/||psi||_2^2 <=1+epsilon.

Both actual orientations preserve H0 because pi is invariant. Reference
self-adjointness is used in the inverse-form/storage inequality; actual
self-adjointness is NOT required or asserted.

Set e=psi/||psi||_2 and write an actual evolution with either sign of C as
u=c_scalar e+x, x perpendicular to e. Common-form weak energy solutions give

    c_scalar'=-a c_scalar+y,
    a=E(e),  y=-E(e,x),
    (1/2)||x(T)||^2 + integral_0^T E(x)
       <= integral_0^T c_scalar y.

Indeed the scalar C term is zero by C*e=0, the hidden skew self-term is zero,
and the mixed term is zero by Ce=0. This is valid on the common form domain;
operator-domain membership of the piecewise-smooth trial is unnecessary.
Autonomy removes a chronological scheduling issue, and both signs still satisfy
the same equations. The compact bounded form perturbation supplies the actual
energy-solution regularity, rather than assuming it from notation.

Put qref=||A^(-1/2)e||^2 and d=a qref-1. Reference Cauchy gives
0<=d<=epsilon and k/a-1<=epsilon. The accepted storage calculation yields

    ||x(T)||^2<=d/4,
    |c_scalar(T)-exp(-aT)|<=d/2,
    ||u(T)-exp(-aT)e||<=sqrt(d(1+d))/2.

The rate change satisfies
`sup_T |exp(-aT)-exp(-kT)|<=epsilon/exp(1)`. Therefore

    ||P_t psi-exp(-kt)psi||_2 <=||psi||_2 G(epsilon),
    G(epsilon)=sqrt(epsilon(1+epsilon))/2+epsilon/exp(1).

The NORMALIZED actual stationary correlation is
`c_processed(t)=<psi,P_t psi>/||psi||_2^2`. Its scalar error is at most

    d/2+epsilon/exp(1)
       <=(1/2+1/exp(1))epsilon <=epsilon.

This is a storage estimate for the processed semigroup, not an illicit use of
its reversible spectral representation. In particular the audit never uses
`||P_t psi||^2=<psi,P_(2t)psi>` for the nonreversible process.

## 4. Actual forward committor and stationary intensity

The accepted autonomous capacity receipt treats the NEW forward committor q,
with q=1 on A, 0 on B. On bounded slab truncations set w_R=q_R-h with zero
boundary trace. The weak equation, Ch=0, and skewness give

    E_R(w_R,w_R)=-E_R(h,w_R),
    E_R(q_R)=E_R(h)-E_R(w_R)<=E_R(h).

Extending q_R by h outside the truncation gives global form-domain functions
of energy at most C0=1/(beta Rbarrier). Meanwhile the unchanged Y equation and
outward drift on |Y|<b imply, by stopping Y^2,

    E_(y,z) tau_S <= beta(b^2-y^2)/2.

Nonexplosion and this finite exit identify q_R with a sequence converging to
the actual exit committor. Weak global form compactness and strong L2 convergence
earn E(q)<=C0 without presupposing finite committor energy.

Local elliptic/flat-boundary regularity gives genuine continuous boundary
finite-variation terms in localized Itô--Tanaka; this is not inferred merely
from an abstract zero-energy Fukushima term. In a two-sided stationary process
the retained label exists. Its conditional distribution given X uses the
backward committor of G0-C, generally different from q.

Let I=1 on last-visited A and 0 on last-visited B. At a completed transition
F=(q-I)^2 jumps from 1 to 0. At boundary local-time support q-I is zero except
at isolated switching instants, which continuous local time does not charge.
Thus

    F_T-F_0=M_T+2 integral_0^T Gamma(q)(X_t)dt-N_T.

The martingale bracket has expectation at most 8T E(q)/Ztot. Stopping at count m
and compact exits first gives E N_stop<=1+2T E(q)/Ztot; Fatou earns count
integrability before unstopping. Actual augmented stationarity then gives

    E_stationary N_T=2T E(q)/Ztot<=2T C0/Ztot.

No forward/backward committor equality and no detailed balance were used.

## 5. Initialization, units, and all slab normalizations

Let the two unnormalized basin masses equal M, slab mass be S_mass, and

    Ztot=2M+S_mass,
    eta=S_mass/M,
    s=S_mass/Ztot,
    C=1/pi(A)=Ztot/M=2+eta=2/(1-s).

In particular C s=eta. The new diffusion has the SAME invariant pi, so these
values do not change under the admitted circulation. Exact once-only Gibbs|A
initialization is the stationary augmented law conditioned on X0 in A, where
the retained sign and Z=sign(psi) are both +1. Its augmented and entire forward
path density is bounded by C relative to stationarity.

This conditioning destroys stationarity; the count equality is NOT reused
under Gibbs|A. Instead stationary bad-event probabilities are transferred by
the full-path density factor C. There are no post-crossing resets.

The reference rate is

    lambda=1/T0=C0/M,  k=2lambda,
    x=lambda Delta,  r=exp(-k Delta)=exp(-2x).

Actual intensity satisfies the stronger inequality

    2C0/Ztot=(1-s)lambda<=lambda.

Discarding 1-s is conservative and leads to the frozen error formula.

## 6. Nonreversible grid and cluster calculation, with constants

Because psi has the correct basin values and Z=sign(psi),
`|Z-psi|<=1_S`, so `||Z-psi||_2<=sqrt(s)` and `||psi||_2<=1`. Markov L2
contraction, not reversibility, gives

    ||P_Delta Z-rZ||_2
      <=||psi||_2 G(epsilon)+(1+r)sqrt(s)
      <=delta=G(epsilon)+2sqrt(s).

The actual-history KL proof therefore gives entire Z-grid TV at most

    sqrt[C n delta^2/(2(1-r^2))]
      =sqrt[C n delta^2/(2(1-exp(-4x)))].

The invariant unconditional marginal density bound is used after conditional
Jensen. No bounded-density claim given entire label histories is made. L and Z
agree at time zero under Gibbs|A; the other n grid mismatches cost at most
`C n s=n eta`.

For the STATIONARY process, no reversibility is needed for

    E[psi(X0)psi(XDelta)]=<psi,P_Delta psi>.

The processed scalar upper bound and the L1 slab replacement imply

    E Z0 ZDelta <=r+epsilon+2s.

Thus the Z endpoint-flip probability is at least
`(1-r-epsilon)/2-s`. The retained label differs from Z only in the slab at
either endpoint, costing another 2s, and hence

    P_stationary(L0!=LDelta)>=(1-r-epsilon)/2-3s.

For integer N, `2 1_{N>=2}<=N-1_{N odd}`. Its odd indicator is exactly the
retained endpoint-flip indicator. With EN_Delta<=x and
`(1-exp(-2x))/2>=x-x^2`, this gives

    P_stationary(N_Delta>=2)<=x^2/2+epsilon/4+3s/2.

Stationary augmentation gives this bound in every bin. Full-future-path
domination transfers the UNION to the actual initialized law, costing

    C n x^2/2+C n epsilon/4+(3/2)n eta.

For the reference CTMC the flip rate is lambda=k/2, its bin count is Poisson(x),
and its separate union cost is n x^2/2. Adding grid, slab, actual cluster, and
reference cluster errors gives EXACTLY

    sqrt[C n delta^2/(2(1-exp(-4x)))]
      +(C+1)n x^2/2+C n epsilon/4+(5/2)n eta,

capped at 1. No hidden factor-of-two, initialization, or slab normalization
correction is needed.

## 7. What the resulting coupling proves

Couple the finite grids and extend via their correct conditional path laws.
On successful grid/slab coupling and the complements of BOTH cluster events,
the two retained paths have equal endpoints and at most one jump in every bin.
They therefore have the same number/order/direction of transitions, and each
paired jump time lies in the same width-Delta bin. Its time error is at most
Delta. Finite stationary count intensity excludes deterministic-time jump
atoms; domination transfers that fact to Gibbs|A. CTMC jumps also have no such
atoms. A piecewise-linear increasing time change pairs all jumps, fixes the
horizon endpoints, and displaces time by at most Delta.

This is a finite-horizon timestamp-jitter/Skorokhod coupling, NOT TV of exact
continuous jump-time laws or an exact iid holding-time claim at finite size.
Actual reverse journeys remain part of the wall clock.

For fixed scaled horizon H=n x, G(epsilon)=O(sqrt(epsilon)), eta and s
exponentially small, and C=2+eta bounded. The grid term is
O(sqrt(epsilon+s)/x), while cluster contributions are O(x+epsilon/x+s/x).
Taking x of order epsilon^(1/4) yields vanishing failure and scaled timing
error Delta/T0=x. These constants do not depend on circulation strength or
shape beyond exact class admission. This supports the stated mathematical
uniformity, not uniform input-processing or physical actuation cost.

## 8. Boundaries not crossed by this acceptance

* The symmetric inverse-form source is reference data. No processed inverse
  certificate, detailed balance, or inherited reversible committor is assumed.
* A fixed arbitrary time-dependent protocol can preserve pi and have neutral
  grid estimates without a stationary augmented count law. This autonomous
  continuous-clock proof does not transfer to it. Phase augmentation or a
  controller changes the model and initial law and requires new receiving.
* Approximate divergence-free or approximate-neutral controls require new error
  bounds; no energy injection or neutrality defect is hidden in G(epsilon).
* The displayed rates and spacing use exact ideal scalar quantities. A rational
  consumer must charge rate error in BOTH grid and cluster estimates. The older
  baseline-only numerical/rational consumer is not promoted to this class by
  the mathematical join.
* No parser, executable budget, observed-state feedback, arbitrary computational
  functionality, calibration, preparation algorithm, sensor, or hardware claim
  is approved.
* For the constant diffusion covariance 2D/beta and bounded compact c, the usual
  finite-horizon Girsanov relative-path entropy, with common initialization, is
  `(beta/4) E_processed integral c^T D^(-1)c dt`. This is a mathematical path
  action, not energy in joules. Under stationary initialization it grows
  quadratically with a scalar amplitude for a nonzero fixed drift shape, while
  the neutral task-error certificate is unchanged. Thus amplitude-independent
  task accuracy does not establish free actuation.

The supplied local Lee--Seo scope note was read. The acceptance claims no first
nonreversible metastable clock or Markov-chain limit. This audit checks the
present mathematical join, not a new external literature search; stated prior
machinery and scope distinctions remain credited, not promoted into novelty.

## 9. Exact disposition

The reference global-current theorem now has its independent acceptance, and
the added autonomous model/capacity/count and sharp neutral-vector interfaces
are earned as detailed above. **No mathematical blocker remains for this
actual autonomous class theorem.** Physical/numerical receiving remains outside
the claimed deliverable, not a missing proof silently counted as completed.

## 10. Operational provenance and recovery

At approximately 01:14 UTC an exec call failed before process creation with an
exec-server transport disconnect. A minimal pwd probe then succeeded, but recent
November proof directories were absent while older workspace contents remained,
consistent with a replaced/rolled-back execution workspace. This was not a
permission denial. One source-read retry after the successful probe returned
ordinary missing-file errors; no permission escalation or bypass occurred.

The exact frozen root, sharp theorem, baseline theorem, and baseline acceptance
had already been successfully read and hashed before the incident. This new
directory contains a recovered root snapshot reconstructed from the successful
tool output; its hash is checked against the supplied frozen root hash. The
receipt's math does not depend on claiming that absent originals were re-read
after the incident. Root and the baseline reviewer were promptly notified.

Original-source locations remain untouched by this audit. Final rehash of those
locations requires their restoration; the recovered snapshot and current audit
are independently hash-bound here. Earlier dependency hashes are explicitly
pre-incident bindings, not fabricated claims of current filesystem availability.
