# Received neutral processing: finite and near-reference normalized means

**Local mathematical proof/audit package — no upload.**
The independently accepted result closes the mean question under the full
common-form/two-source certificate. It does not infer means from absolute CDF
accuracy alone and does not enlarge any physical or executable interface.

## Accepted results

Let the reference killed symmetric generator A act in the SAME finite measure
m used by the actual killed process. Write M=m(A_set)>0 and

    Q_D=<1_D,A^(-1)1_D><=B_total=(sqrt(B_A)+sqrt(B_S))^2.

The inverse is a form, not necessarily an ordinary inverse vector. Under the
explicit two-sided sub-Markov/common-energy receiving below,

    E_{m(.|A_set)} tau_B <=4 Q_D/M <=4 B_total/M.

No global spectral gap is required. The constant 4 is proved, not optimized.

For actual and reference absolute survival errors delta_a,delta_r around
exp(-kt), and qbar=k B_total/M>=1, the sharper join gives

    k E tau_B <=1+4(qbar-1)+2 sqrt(8(delta_a+delta_r)),

intersected with 4qbar. For 0<delta_a<1,

    k E tau_B >=1-delta_a[1+log(1/delta_a)].

The exact finite-window bounds in the sharp source can be tighter. In the
neutral-clock normalization qbar=1+epsilon and common error bound
Delta=(7/8)epsilon+rho+sqrt(rho(1+rho)), a safe specialization is

    k0 E tau_B <=1+4 epsilon+8 sqrt(Delta).

**Controlling convergence qualification:** the conclusion is k E tau_B ->1,
or equivalently E tau_B/(1/k)->1, uniformly over received protocols as the
normalized errors vanish. If k itself tends to zero, this does NOT alone
prove the unscaled difference E tau_B-1/k tends to zero. The audit's explicit
qualification controls ambiguous shorthand in the unchanged sharp source.

## Actual-process receiving is part of the theorem

The killed propagators P_{s,t} and P_{s,t}^* must BOTH be positive sub-Markov
with respect to the same m. The chronological forward constant-source paths
P_{s,s+r}^*1_D and reversed-backward paths P_{t-r,t}1_D must BOTH have actual
weak-energy representatives satisfying

    d||w(r)||^2/dr <=-2 E(w(r),w(r)).

Full common-domain forms earn this for arbitrary H initial data; 1_D need
not lie in the killed form domain at time zero. Merely having the scalar port
inequality for one trial h, formal skewness, or an unreceived operator does
not earn these premises. Both independent source-current bounds B_A and B_S
are required for the full-source join.

A self-contained received example is included in
`neutral_processing_clock_pending_20261101/PASSIVE_PORT_CLOCK_ROOT_V2.md`,
section 6: the constant-SPD Langevin model with a smooth compact transverse
weighted-divergence-free field and predetermined locally bounded amplitude.
Its proper Lyapunov estimate earns global existence; full common-measure
invariance, common-domain transport bounds, and both form signs/time
orientations earn the stronger mean premises. Arbitrary singular drifts,
state-selected feedback, or mobility descriptions are not admitted by analogy.
Neutrality of h is needed for the CDF clock, but is not needed for the mean
bound after full two-sided common energy is earned.

## Reading and evidence

1. `test_processed_clock_lifetime_20261101_0043/COMMON_FORM_UNIFORM_MEAN_ROOT.md`
   — self-contained reference heat-content, squared-norm envelope, midpoint
   chronology, and 4Q proof.
2. `neutral_processing_clock_pending_20261101/SHARP_MEAN_FROM_COMMON_FORM_ROOT.md`
   — exact reference-tail/clock join, interpreted with the qualification above.
3. `audit_common_form_and_sharp_mean_20261101_0059/INDEPENDENT_ACCEPTANCE.md`
   — independent PASS for both theorems and the weaker-interface countermodel.
   Its checker passed **1,268 exact rational regressions** and exact source
   hashes; these are regression evidence, not substitutes for the proofs or
   numerical implementations of the full receiver.
4. `EXACT_REVERISBLE_LIFETIME_COUNTERMODEL.md` in the test directory — an
   actual reversible chain with fixed trial a,q_h,rho and unbounded actual
   mean, but diverging B_S. It does not pass the full-current interface. Its
   historical final open-question paragraph is superseded by the new theorem
   and the controlling audit receipt; original bytes remain unchanged.
5. `TIME_DEPENDENT_MIXING_CAN_STRICTLY_INCREASE_MEAN.md` and
   `PULSE_FIRST_VARIATION_ADDENDUM.md` — supplementary exact derivations
   showing a predetermined fixed-rate reversible mixing pulse can increase
   mean above reference Q_D. They independently PASS in the separate included
   `audit_action_pulse_boundaries_20261101_0102/INDEPENDENT_ACCEPTANCE.md`,
   section 2; the rare-gadget near-clock embedding in the copied test README
   is explicitly OUTSIDE that acceptance. The accepted three-state pulse
   does not contradict 4Q or assert an unbounded ratio.
6. `neutral_processing_clock_pending_20261101/PROCESSING_ACTION_COST_ROOT.md`
   — optional standard Girsanov path-action identity, separately accepted in
   section 1 of the same supplemental receipt. Controlling qualification:
   growth of path-law KL is NOT a conclusion that total variation tends to
   one or optimal testing error vanishes. This is not work/heat in joules, a
   device power receipt, or a physical entropy-production certificate.

Earlier frozen source status lines saying review was pending are superseded
only to the precise extent stated in the included source-bound audit receipts.

All copied sources are byte-bound in `SOURCE_MANIFEST.json` and the package
hash list. The two older ZIPs are included unchanged ONLY so the original
independent checker's old-archive integrity checks replay without alteration;
they are not implicit proof premises, newly promoted claims, or replacements
for the self-contained receiving above. No old archive or source was edited.

## Replay

From this package's root after extraction:

    python audit_common_form_and_sharp_mean_20261101_0059/check_exact.py

This rechecks source hashes, all 1,268 exact identities, and both prior ZIPs.
The external ZIP verification receipt records a clean extraction/replay.

## Strict scope

No second/exponential moment, relative extreme-tail accuracy, mean transfer
from arbitrary total-variation preparation error, iid restart, physical
sampler/control/calibration/acquisition, arbitrary feedback, or quantum-fault
claim follows. This is exact-real conditional mathematics, not a numerical
receiver or an executable source interface. Ordinary spectral/semigroup-energy,
Schur/passivity and Cauchy--Schwarz methods retain full prior credit; historical
novelty is not claimed. No external state was changed or upload performed.
