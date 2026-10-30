# Independent review: joint operator source and global activity cut

2026-10-30. Reviewer: `producer-workspace/audit_topology_free_noise`.

## Verdict and exact scope

**SCOPED PASS for both root operator lemmas under their explicit receiving contracts.** They supply (i) an actual positive joint killed comparison in place of the old Poisson record filter and (ii) a full-state fixed/exogenous-time macroscopic activity tail under bounded-body continuous joint noise. They do not themselves prove the actual two-lab return hypotheses, bind the Q memory/noise theorem, or certify the finite teleportation/receiver endpoint. Those must be instantiated and whole-reviewed separately.

Frozen sources:

* `JOINT_OPERATOR_SOURCE_COMPOSITION.md`: `2bc35816f92df42855acc4074490d880886f414a82c6ffd881949e0ac4cff1bc`.
* `GLOBAL_ACTIVITY_DENSITY_LEMMA.md`: `18e4f3c986cb68fd519d5c1476c17f8f6f1d86a3682f40466e4527f936901d40`.

Exact copies and inventory are saved alongside this receipt. The accepted continuous Bell-memory whole receipt `82f2db0ec91027598d1b401e04d523256198cf3a7420356a6b1905061f32e5c6` remains unchanged. This review does not import the earlier native recipient's stochastic record argument or promote its noise scope.

## 1. Global activity potential: positivity and the correct logarithmic scale

Assume the stated ACTUAL fast generator with all relevant LOADs removed has local positive witnesses `alpha A_h<=Z_h<=A_h`, drift `L_fast*Z_h<=-r A_h`, and `[Z_h,A_g]=0` for every pair. The A_h commute and have bounded local incidence. These are substantive hardware hypotheses; the generic lemma does not derive them from a classical reachability graph.

On a joint activity sector let m be the number of active owners. Every inactive witness is zero on that whole sector. Every active factor `exp(delta Z_h/2)` has singular values between `exp(alpha delta/2)` and `exp(delta/2)`. Multiplicativity of minimum singular values and submultiplicativity of the maximum, not commutation among the Z_h, give

`exp(alpha delta m) I<=Y*Y<=exp(delta m) I`.

All factors reduce the joint sectors, so globally `exp(alpha delta M)<=G<=exp(delta M)` and `[G,M]=0`. Also `[Y,M]=0`. This proves the required operator comparison even with noncommuting overlapping witnesses within a sector.

For the physical unital fast generator, the local relative Taylor lemma has zero killing at order zero and first derivative `L_fast*(sum Z_h)`. Its uniformly finite cones give

`Y^-* L_fast*(G) Y^-1 <= -r delta M+C delta^2 N I`.

Complete LOAD generators are individually identity-annihilating. Their relative expression vanishes at delta=0, and its local derivative is bounded by the LOAD rate. Thus their total contribution is `C delta lambda_max N` (or a sum of the actual Alice/Bob rates), not `C lambda_max N`. Complete source losses must be retained; a guarded LOAD is not replaced by an atomic `lambda(Phi-Id)` attempt. This derivative estimate remains uniform because the witnesses were fixed for the zero-LOAD reference before selecting small LOAD rates.

The bounded-body joint perturbation gives `C eta N` through the same finite-cone/cb argument as below. Congruencing back and using commutation with M yields

`L_full*G <= -r delta M G+C(delta^2+delta lambda_max+eta)N G`.

Since `log G<=delta M`, the negative term is at most `-r G log G`. For a positive trace-one actual state, spectral Jensen gives

`x'<=-r x log x+C(delta^2+delta lambda_max+eta)N x`, `x=Tr(G rho)`.

The activity proof potential G may be DATA dependent and need not commute the physical forest. To interpret the tail physically it is enough that the actual count M commutes the forest; apply the operator estimate in that exact frame. No stronger G/forest commutation is assumed.

There is no missing factor 1/delta in the stationary logarithmic bound: the factor delta in the drift cancels the one in `log G<=delta M`. From all-FREE initialization x(0)=1, scalar comparison gives the stronger transient bound `log x<=C(delta^2+delta lambda_max+eta)N(1-exp(-rt))`, with r absorbed into C if desired. Hence the frozen coarse bound and its tail exponent follow.

The event is the spectral projector of the actual M at a fixed/exogenous time. From the lower comparison for G,

`Tr[1_(M>=mu N)rho] <= exp{-[alpha delta mu-C(delta^2+delta lambda_max+eta)]N}`.

Choose fixed delta small compared with mu, then all relevant positive LOAD rates small, then eta small compared with delta mu. No historical record, independent clocks, adaptive stopping-time or uniform maximum-over-time claim is implied.

## 2. Moving partners and a common retained bath

The receiving noise contract must be the explicit instantaneous one: fixed system-body cardinality q and `||N_e(u)^*||_cb<=eta c_e(u)`, with `sup_u sup_x sum_(e:x in supp_e(u)) c_e(u)<=C_inc`. Nonempty counted supports give total norm O(N eta). A count-only degree bound with unconstrained weights is insufficient. Moving partners are allowed; the sum is taken at each time, not over separate time suprema.

The nominal witness graph and color depth remain fixed. Any q-site noise term meets a bounded union of q fixed witness neighborhoods, even if the sites are far apart. Relative conjugation therefore costs a fixed norm factor; summing costs O(N eta). Noise geometry is not used to color separated moment products, because this is one global positive potential. Normal finite-system-leg cb expansion permits arbitrary retained bath correlations and reference amplification; no finite bath dimension or positive Kraus decomposition of the HP perturbation is needed. Bath-only terms annihilate G.

If local pieces are not individually identity-annihilating, the accepted HP centering at at most twice the joint norm is available when their sum annihilates identity. It preserves total physical evolution and support. The assumed normal interval-CPTP/domain and actual compression regularity remain required; norm bounds alone do not construct an unbounded-bath propagator.

## 3. Joint killing: one actual positive process

During waiting the nominal AB and Q system generators act on disjoint physical machines. The analysis projectors P_AB and P_Q are system-only and commute, as do each witness and the other projector. Let `P=P_AB P_Q`. The actual joint generator, including all coupling noise and retained bath, is compressed at P with complete losses. Its existence as a CP/TNI process is a receiving assumption.

For either positive witness F, `[F,P]=0`. For a P-supported state, replacing its full drift by the P-killed drift subtracts a nonnegative outgoing contribution. This follows directly from conditional positivity of the actual infinitesimal CPTP map on `Q F Q>=0`; it does not depend on a positive decomposition of the signed perturbations. If the single-machine estimate is already written for its own killed generator, the additional other-machine cut gives the same conclusion, since the two projections commute and the witness commutes both.

The single-machine operator/moment inequalities apply to this joint killed state only with the declared reference/bath-uniform receiving contract. This is not an inference from two reduced output fidelities. The other machine's nominal terms annihilate the witness. Centered perturbations with no support on that machine likewise annihilate it; cross-machine perturbations are counted at their actual joint norm. Treating the other machine as auxiliary does not authorize ignoring its coupling noise or requiring a separately positive decomposition of its noise pieces. The actual full joint propagator remains the one used for comparison.

Each moment uses the same subnormalized joint state and mass at most one, so its Jensen/linear scalar argument remains valid. No product of the two witnesses or their already summed drifts is needed. Fixed comparable block sizes change only constants.

## 4. Joint exits and the Q receiving theorem

For any joint bounded system leg J,

`I-P_AB P_Q <= (I-P_AB)+(I-P_Q)`.

Apply the single-machine leg leakage bounds to the same positive joint killed state. A joint system leg has a finite AB/Q matrix-unit expansion, or may be bounded by its uniform similarity on the acted-on machine with the other system retained. All coefficient counts depend on fixed q-site dimension only. Thus the two individual moment-controlled exit bounds add with a fixed constant. The finite bath-map expansion and trace-norm Cauchy-Schwarz then give an O(N) weighted boundary source; full CPTP propagation contracts its forward Duhamel integral.

This yields a direct complete-trace-norm comparison with the **positive joint killed channel**, of the stated polynomial(N)(1+T) exponential form. It does not assert positivity of actual-minus-killed. No native SUCCESS/Poisson record is attached to a broad coherent-noise generator, and no old source-record filter is reused.

The actual application must pin Q's accepted theorem, its canonical/energy projector, its arbitrary encoded-input identity module, its live-BUSY interface and its noise assumptions. A graph-scoped memory receipt cannot by its name alone supply a moving-partner q-body theorem. The intended global-exponential/bounded-body receiving theorem, or a separately proved extension, is required. This is an explicit remaining instantiation condition, not an unresolved algebraic defect in the generic joint lemma.

## 5. Exact common module with an unknown encoded input

AB supplies the fixed encoded Bell target with its shared-syndrome gauge; Q supplies an unknown **already encoded** logical state, possibly entangled with an external reference. The initial resource/apparatus/bath channel must be fixed independently of that unknown logical input as stated. Arbitrary initially logical-dependent bath information is not inferred.

Each compressed joint local leg expands into products of AB and Q local legs. The respective canonical distance arguments make the AB leg preserve its one-target Bell/gauge module and the Q leg act as logical identity on its correctable module. Therefore their joint linear span has one correlated auxiliary/bath coefficient but no unknown-logical dependence introduced by the noise. The same statement holds for the complete losses and compressed Hamiltonians. The joint killed output consequently has the coherent source module required by the signed-Bell contraction, not merely a small decoded Bell error on an unrelated marginal.

This does not strengthen AB to arbitrary bilateral logical identity. The distinction is essential: preserving its fixed Bell vector is sufficient when the unknown logical factor is carried by Q and Q's compressed legs preserve that factor.

## 6. Activity must be filtered after the joint killed comparison

Let rho be the actual waiting output and sigma the positive joint killed output, with `||rho-sigma||_1<=epsilon`. Let Pi be the actual controller/tag cap, after combining separately earned AB ACTIVE and Q BUSY tails. If its actual bad mass is at most p, then

`Tr[(I-Pi)sigma]<=p+epsilon`.

Gentle compression for the positive subnormalized sigma gives

`||sigma-Pi sigma Pi||_1<=2 sqrt(p+epsilon)`.

Thus the physical state is close to one positive source channel with both the module and the sparse-prefix cap. No `[Pi,P_AB]` assumption is needed. The filter is not inserted into the waiting dynamics, and the filtered state need not remain in the inner spectral basin. Waiting has ended at this cut; only the outer correctable module and actual physical prefix support are used next. Pi must commute the forest frame/outer canonical radius and preserve that module, as required in the source note.

The square root weakens the exponential rate but preserves an exponential bound for the allowed storage horizon; polynomial and `(1+T)` factors can be enlarged harmlessly. No CP domination is used to transfer the effect bound.

**Source-error qualification:** if a source-bad preparation branch is not initially FREE or not in the common module, split off that positive bad instrument first and charge its mass linearly. Perform the activity moment, joint kill and gentle filter on the admitted good subchannel. Otherwise applying the displayed gentle bound to a tail containing eta_source could introduce sqrt(eta_source), contrary to a claimed linear source error. The parent has confirmed the separate-positive-source convention for the eventual endpoint. The generic lemma itself asserts the clean-FREE initial condition.

## 7. Noncircular physical rates and what is still required

For BOTH AB labs, construct physical return/activity witnesses with both LOADs absent and all actual fast quantum/classical/FIFO terms retained. Fix the endpoint's finite durations and acceptable physical prefix/error budget first; choose the activity density and proof delta. Choose a small **positive** Alice LOAD rate meeting activity and finite-ramp budgets, and then hold it fixed. Only at that rate construct/recompute Bell-memory service and exposure constants. Choose the smaller Bob LOAD, Bell proof strengths and final noise afterward. There is no requirement that Bell-memory constants stay uniform as Alice LOAD tends to zero.

The Q initialization/live-prefix/ramp parameters must be included in the same finite-window budget. Old forward C **and inverse B** payloads, Q first initiation/payloads, separate old/new controller factors, carrier truth, actual physical Bell measurement/pulse, and the positive warm receiver channel still need the fresh actual endpoint proof. The whole result is not obtained by replacing the word "stochastic" in an earlier manuscript.

These two root lemmas are sufficient operator interfaces once the stated actual receiving contracts are independently earned. No bare unknown-input initializer, free entanglement source, adaptive access theorem, physical decoder, passive storage, practical threshold or computational advantage is accepted here. No author source was changed and no external publication occurred.
