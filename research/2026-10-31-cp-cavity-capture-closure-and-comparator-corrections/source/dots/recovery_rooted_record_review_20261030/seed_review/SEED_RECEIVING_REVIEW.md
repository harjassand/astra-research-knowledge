# Independent seed receiving review: genuine classical outcomes only

30 October 2026. Frozen sources: GENUINE_CLASSICAL_SEED_RECEIVING.md and SEED_MIXED_RESET_SUBSET_LEMMA.md, copied beside this review. See SOURCE_HASHES.txt. The earlier positive-source manuscript and its actual independent receipt were read, including their reset hypotheses.

## Verdict

**PASS for the fixed-size, scheduled atomic seed receiving interface WITH the explicit mixed-reset repair.** The main source's bare invocation of the old all-reset lemma was not sufficient: raw latches are not reset. The new mixed-reset note supplies the missing argument correctly. The quantitative fixed-hardware form below also earns the stated positive-power noise plus reset-residual dependence.

This assumes a supplied GENUINE classical instrument outcome m, exact conditional raw registers |m>, declared actual target-reset reservoirs, and the stated bounded-leg/incident-cb noise model. It does not manufacture that classical instrument boundary from coherent pointers. It does not prove the full quantum receiving theorem, native seed/controller initialization, phase retention, protected final software/readout or autonomous scheduling.

## 1. Exact input and reset hypotheses

Conditional on an actual complete classical outcome m, the raw registers' rank-one |m> support factors them from the rest of the joint state. Targets, DATA, bath and reference can be arbitrary and mutually correlated. Their conditional state may depend arbitrarily on m. Constants below are uniform in that state and in m; no later error independence is assumed.

The accepted source reset proof uses resets on EVERY projector entering its scalar Jensen contraction. It cannot directly reset a moment containing idle raw-bit defects. The reviewed new note instead uses a time-dependent target penalty and a fixed raw penalty; it is a genuine extension, not a relabeling of the original hypothesis.

The noise assumptions remain substantial: tensor locality on the declared system legs with arbitrary bath coefficients, per-site incident adjoint-cb strength, centered HP contributions, and a well-defined positive/CPTP total propagator. An unspecified noisy gate scheduler or only a global total norm bound would not suffice.

## 2. Mixed moment proof, including idle raw exposure

For selected raw R and target A indices, use

 F(t)=exp[theta sum_R B_i+theta_T(t) sum_A B_i].

Choose theta_T'=kappa(1-exp(-theta_T)). The nominal target replacement-reset adjoint is exactly

 L_reset*F=-kappa(1-exp(-theta_T))(sum_A B_i)F.

Thus partial_t F+L_reset*F=0. No nominal reset acts on raw bits. Initially raw defects vanish and arbitrary targets give expectation at most exp(theta_0 |A|), including arbitrary target/bath/reference correlations.

For each centered HP term, factor off unaffected positive factors. The affected factor has spectrum in [1,exp(q' theta)] whenever theta_T<=theta. The same cb relative congruence as in the accepted source receipt gives

 N*F <= C eta exp(a theta)(|R|+|A|)F.

Only terms meeting the selected subset contribute. No source-volume multiplier appears. During fixed-depth CNOT copying the ideal interaction picture only enlarges support/incidence by finite constants; use their maximum a and appropriate integrated constant Gamma. Nominal DATA/bath-only evolution commutes this test. All raw waiting time, resets and copy time are included.

At the common final exponent theta, Markov on the actual commuting defect projectors gives

 Pr[all selected input defects] <= p0^(|R|+|A|),
 p0=exp[-theta+theta_0+eta Gamma exp(a theta)].

This is a positive spectral bound, not a signed-HP fault trajectory. The final ideal CNOT is a basis permutation, so these input-defect projectors give the claimed deterministic classical copy relation, including coherent error superpositions.

## 3. Stronger fixed-reset-duration parameter formula

Fix the actual reset duration t_R, define p_reset=exp(-kappa t_R), and choose the ANALYSIS initial exponent

 theta_0=log[1+(exp(theta)-1)p_reset].

Then theta_T(t_R)=theta exactly, and

 exp(-theta+theta_0)=p_reset+(1-p_reset)exp(-theta).

Consequently

 p0 <= [p_reset+(1-p_reset)exp(-theta)] exp[eta Gamma exp(a theta)].

For a eta Gamma<1, take exp(a theta)=1/(a eta Gamma). This yields the explicit bound

 p0 <= exp(1/a) p_reset+(e a eta Gamma)^(1/a).

Gamma includes reset waiting and copy exposure and is fixed with the hardware. The displayed exponent 1/a is not necessarily one. For useful bounds choose eta smaller and p_reset small enough that p0<1. One may alternatively use the fixed-theta calibration in the new source; both are valid. A fixed nominal reset residual is not O(eta) without a declared calibration change.

Fix n0 and all seed/root weight constants FIRST; then calibrate reset duration, then choose eta small enough for the desired moment margin. The large finite n0 makes the depth/lightcone constants and w_max potentially enormous, but does not introduce dependence on the number of records or computation horizon.

## 4. Record cones and exponential seed weights

Distinct seed blocks have disjoint IDEAL input cones C_j. Shared-bath or multi-record noise is already included in the all-subset bound; it does not require the cones' physical errors to be independent. OR expansion and disjointness give p_seed=c0 p0 for specified sets of bad cones. Require this parameter below one before using it as a useful tail bound.

On the zero-defect cone the actual ideal-copy output is consensus m_j. The diagonal W_j therefore has the stated vacuum value. On the finite seed block let w_max be its actual finite operator norm bound, including animal counting and all chosen root/phase parameters. Because W_j and A_j commute,

 W_j<=w_vac+(w_max-w_vac)A_j

is an operator inequality. Expanding the positive product proves A_seed=w_vac+(w_max-w_vac)p_seed, with the exponential n0 cost fully retained. The coefficient cannot be dropped simply because n0 is called a constant. The stated order of calibration can make log A_seed small even when w_max is very large.

The same expansion with specified bad cones L disjoint from remaining weighted records R gives exactly

 Tr[W_R product_{j in L} A_j rho] <=p_seed^|L| A_seed^|R|.

It uses the joint subset law, not products of separately proved expectations.

## 5. Signed initial flags and complete-map interpretation

The initial phase-good projector must really contain exact consensus relative to m, so Q_j<=A_j in the same chart. For ket-bad set L and bra-bad set L', the weighted Cauchy-Schwarz bound is

 ||W_R^(1/2) P_L rho P_L' W_R^(1/2)||_1
 <=sqrt[Tr(W_R P_L rho)Tr(W_R P_L' rho)].

Dropping other commuting good constraints only increases these positive effects. If L union L'=D, the exponent (|L|+|L'|)/2 is at least |D|/2. There are at most 3^|D| non-all-good ket/bra choices. This proves (3 sqrt(p_seed))^|D| A_seed^|R| for the exact signed initial union component. These are norm bounds, not positive probabilities assigned to signed components.

For fixed m, regard target/DATA/bath/reference degrees of freedom as INPUT to the actual seed CPTP map; adjoin only the exact raw |m>. The moment argument is uniform on this entire input space. It therefore yields the stated adjoint effect inequalities. A common Stinespring dilation expresses each weighted cross map as a partial trace of A X B†, whose complete trace norm is bounded by ||A|| ||B||. The two norms squared are precisely the two bounded effects. This earns the map-level CS statement rather than extrapolating from one positive input.

The arbitrary conditional bath is not declared independent of an unknown logical input inside a fictitious fixed logical channel. It is retained in the map's input domain. Composing with the supplied genuine instrument branches and averaging over m preserves the uniform bound.

## Conclusion

The explicit mixed-reset source plus the seed's joint weighted/cone algebra supplies the claimed INITIAL moment and signed-flag interface for supplied classical outcomes. The important import mismatch is repaired and the raw latch's noisy waiting exposure is paid. No whole-volume factor, per-record gentle-error sum, independent-target assumption or immutable physical reference latch is used. Later atomic growth/phase theorems and quantum/native receiving retain their separate hypotheses and reviews.
