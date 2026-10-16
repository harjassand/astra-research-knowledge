# Charging randomizer control: two conditional extensions and their obstructions

Date: 2026-10-15. Bounded mathematical follow-on. No hardware measurements, installations, author-code execution, or edits to the previously proved theorem packets.

## Result first

There are two different sufficient interfaces; neither is implied by ordinary gate infidelity.

1. **Exact stochastic CP contamination.** If every control has a qualified full-process decomposition into an exact private reference operation of scalar weight `1-epsilon` and an arbitrary local CPTP operation of weight `epsilon`, then the homogeneous parent subset budget is

   `p_CP = min(1, q_ref + f_control)`.

   For `c` fixed padded initial/final control slots and `N ~ Pois(mu)`, `mu=m gamma t`, the exact charged control-flag probability is

   `f_control = 1 - (1-epsilon)^c exp(-mu epsilon)`.

   A count cap with overflow charged as a whole-parent fault gives

   `f_M = 1 - (1-epsilon)^c exp(-mu) sum_{n=0}^M [mu(1-epsilon)]^n/n!`.

   This is a genuine mixed-subset statement, not an assumption that weak errors and control faults are independent.

2. **Coherent, covariant control residuals.** An exact ideal CP branch is unnecessary if the actual full dilation differs from the ideal randomizer reference by additive local, private-parent residual Hamiltonians of bounded action. The actual global-character effects obey

   `effect(all selected parent characters nonzero) <= (sqrt(q_ref) + b_rms)^(2 |S|) I`.

   Here `b_rms^2 >= E b_i(eta_i)^2`, and `b_i` is the total joint residual action of parent i, including every qualified initial/update/final control discrepancy. For a per-control action `u` and Poisson count,

   `b_rms <= u sqrt((c+mu)^2+mu)`.

   This second statement becomes a support/memory theorem ONLY if the actual residual retains the same initial-frame conjugation/character-to-memory-Pauli relation. Arbitrary seed-dependent residuals can create undetected zero-character damage.

The coherent interface can charge finite-width internal randomizer ramps: an exact, initial-seed-independent control path differs from its instantaneous reference only on the ramp supports, and ambient-coupling mismatch has action at most `2 J times total ramp length`. This observation does **not** qualify faulty initial/final wrappers, corrupted frame records, an arbitrary compiler, or finite controller hardware.

The strongest honest conclusion is conditional improvement. At fixed total reservation, a real parameter regime beats the old `a_old^2` bound whenever the appropriate explicitly charged inequality below holds. No supplied experiment or gate data establishes that regime.

## 1. Notation and imported contract

Use `tau` for the fixed TOTAL gadget reservation, including correction, resets, boundary controls, internal gates, and all tails. Let `t<=tau` be the fixed randomization/noise interval. The reference has m private initial-frame generator bits and independent rate-gamma telegraph updates per generator. Write

`B(J,gamma,t) = 1/2 {exp(-gamma t)[cosh(d t)+(gamma/d)sinh(d t)]-1}`,
`d=sqrt(gamma^2+4J^2)`,
`q_ref=min(1,a_ref^2,m B(J,gamma,t))`.

`a_ref` bounds integrated reference coupling action; all actions are dimensionless, with hbar=1. The reference effect theorem is the actual complete GLOBAL Fourier-Kraus theorem, conditional only on source geometric primitives. Private update histories stay averaged. Its common-dilation/additivity/deletion hypotheses, finite shared bath, arbitrary joint input/reference, and support/cleanliness contract remain in force.

Reference contract included here: `../reference/DIRECT_FOURIER_INDEPENDENT_AUDIT.md`, `../reference/SCHEDULED_MEMORY_COMPOSITION_GATE_AUDIT.md`, and `../reference/SCHEDULED_FINITE_DURATION_MEMORY_THEOREM.md`. Contextual source work also included the earlier tracked-control report and qualified noisy-correction-core interface/theorem; those broader contextual files are not duplicated in this addendum.

Throughout, all internal control operations lie inside the SAME fixed parent patch and total interval. Counts/times are exogenous, unaffected by quantum outcomes or faults. Any abort or exceptional schedule is implemented by a declared local fallback ending by the reserved deadline. There is no delayed control tail. No physical support or controller record is made available merely because a final Kraus representation has a label.

## 2. What a local CP effect alone really proves

Suppose there is a compatible CAUSAL CP instrument at each executed slot e, with fault branch `F_e`, good branch `G_e`, `F_e+G_e` CPTP, and

`F_e^*(I)<=epsilon_e I`

uniformly on the complete current data/bath/controller input, after every allowed previous classical history. This is stronger than a marginal probability on a calibration input or a marginal end-of-experiment fault label.

For a fixed schedule, the probability of a fault at a slot, conditional on any history of its causal flags, is at most epsilon_e. For each fixed initial joint state, successive independent uniforms therefore couple the entire fault-flag process below independent Bernoulli flags of parameters epsilon_e. No independence of the physical noise maps or bath is assumed. Consequently the increasing event that each of several disjoint parent slot-sets contains a fault has effect

`effect(all parents i faulty) <= product_i [1-product_{e in i}(1-epsilon_e)] I`.

This is an operator inequality because it holds for every initial joint vector; untouched references do not change the uniform instrument premise. The weaker union bound `product_i sum_{e in i} epsilon_e` also follows directly by choosing one fault slot per parent. Independent exogenous parent schedules can be averaged afterward.

**This controls control-fault labels only.** It does not establish that the nonfault branches preserve the private telegraph model, that a zero character is correct, or that combining the control-only bound with the reference weak-effect bound gives a product for their union. Bath filters and no-fault controller records can change the selected-path dependence. Two separate marginal/subset bounds do not by themselves supply the mixed bound.

## 3. Theorem A: exact stochastic-contamination interface

### A1. Required whole-process decomposition

At every qualified control slot, in the actual common reference/toggling coordinates, require

`R_e = (1-epsilon) R_e^0 + epsilon R_e^1`.

Both branch maps are normalized CPTP on the full joint current space. `R_e^0` is EXACTLY the intended private reference operation, including its allowed bath/controller action and timing. It cannot merely have the correct reduced data action. `R_e^1` may be arbitrary on the declared full parent memory patch and persistent bath. The scalar epsilon is independent of input, prior histories, initial frame values, and selected update paths; the decomposition holds uniformly at every allowed causal history.

Initial and final frame slots are included. Use c genuinely fixed, padded slots; if implementing an identity requires no operation, the conservative decomposition may pad its fault branch with an identical ideal map. Do not claim an exact physical failure probability from such padding: the formula is the exact mass of the chosen charged CP flag. Variable boundary counts require the corresponding expectation instead.

Require, additionally, that after fixing any outside-parent paths, seeds and scalar fault flags, replacing every control of selected healthy parents by its reference branch yields the same additive private reference interface for those selected parents. This is a full-process deletion/covariance condition. Laboratory seed independence alone does not prove it after a change of frame. Outside faults may naturally interact with the shared bath, but cannot read selected private classical seeds or clocks, corrupt their trusted bookkeeping, or introduce extra selected-path dependence.

The equality is a statement about time-aligned full-process operations. For nonzero-width gates it must cover ambient evolution and concurrent shared-bath dynamics over their supports. An isolated gate-channel calibration, a point-event replacement, or an endpoint unitary match is not enough.

### A2. Proof of the mixed subset bound

Keep all causal control-fault labels in a complete actual Kraus family and Fourier-transform the independent initial frame coordinates. Scalar branch weights are independent of those initial coordinates. Let `C_i` mean parent i has a control fault. On `C_i=0`, let `Q_i` mean its actual reference weak Fourier character is nonzero. Mark parent i when `C_i OR Q_i`.

For selected S, partition its marked event by the EXACT control-fault subset `F subset S`; put `W=S\F`.

- Sum all Fourier labels on F and on other unselected parents. Parseval replaces them by their seed averages.
- Fix their exogenous paths and scalar fault patterns. Sum all genuine quantum/dilation outcomes without normalization.
- Every parent in W has only exact reference controls. Its branch is multiplied by a scalar no-fault weight depending on its own update history, but not its initial frame. This weight lies in [0,1].
- At fixed W histories, drop these scalar weights from the POSITIVE Fourier effects. Only then average the W histories. The reference theorem bounds the remaining effect by `q_ref^|W| I`, uniformly in the fixed outside background.
- Sum the scalar flag weights and independent paths on F. They give `f_control^|F|` in the homogeneous case.

Thus the term is bounded by `q_ref^|W| f_control^|F| I`. Summing F gives `(q_ref+f_control)^|S| I`. The trivial complete-channel bound permits capping the homogeneous parameter at one.

This proof never says that healthy-parent clocks retain rate gamma after conditioning, and never normalizes a no-fault quantum record. The actual healthy-clock law is biased toward fewer updates. An optional correctly reparameterized refinement is recorded in the independent audit if separately verified; the primary theorem needs none.

### A3. Exact counts, caps and feasible-time events

For `N~Pois(mu)`, `mu=m gamma t`, the no-fault scalar mass is

`S_0=(1-epsilon)^c E(1-epsilon)^N=(1-epsilon)^c exp(-mu epsilon)`.

Therefore `f_control=1-S_0 <= epsilon(c+mu)`. The bound pays for the final inverse. A full multi-generator frame need not be one gate: c counts its qualified elementary implementation.

If counts above M are charged as whole-parent failures, without renormalization,

`S_M=(1-epsilon)^c exp(-mu) sum_{n=0}^M [mu(1-epsilon)]^n/n!`,
`f_M=1-S_M`.

This combines the Poisson tail and control faults without double counting. The weak-parent proof drops the additional acceptance indicator, so `q_ref+f_M` is valid. Expected executed updates under a stop-at-M fallback are `E min(N,M)`; the successful path count law is NOT obtained by replacing mu with that mean.

More generally let `A(eta)` be an own-path, initial-seed-independent feasibility event. If the actual protocol equals the reference on A and uses only a declared local fallback otherwise, use

`f_A=1-(1-epsilon)^c E[(1-epsilon)^N 1_A]`.

For aggregate Poisson rate `lambda=m gamma`, minimum update spacing delta, boundary exclusion margin beta, and cap M, define A by `t_1>=beta`, `t_N<=t-beta`, consecutive gaps at least delta, and `N<=M`. For `t>=2 beta`,

`S_A=(1-epsilon)^c exp(-lambda t) [1+sum_{n=1}^M {lambda(1-epsilon)}^n [t-2 beta-(n-1)delta]_+^n/n!]`.

The ordered-time simplex is translated by `t_k -> t_k-beta-(k-1)delta`; its volume is the displayed power divided by n!. This formula certifies only that specific spacing rule. A physical design must choose beta/delta to cover its full gate supports. A convenient looser cost is

`f_A <= epsilon(c+lambda t)+Pr(N>M)+2 lambda beta+lambda^2 t delta`,

capped at one. Dropping, delaying, or overlapping updates without this declared exceptional branch changes the reference protocol.

## 4. Theorem B: coherent residual action, without an ideal CP branch

### B1. Effect hypotheses

In ONE common finite-dimensional dilation, suppose

`H_actual(f,eta,t') = H_reference(f,eta,t') + sum_i R_i(f_i,eta_i,t')`.

Each R_i is Hermitian, supported within its fixed parent interval, depends only on its own private initial frame and update path plus conditioned exogenous parameters, and has a uniform-in-input action bound

`integral ||R_i(f_i,eta_i,t')|| dt' <= b_i(eta_i)`.

The bound is uniform in f_i and other admissible parameters. All selected residuals can be scaled or deleted independently in the same dilation. For every deletion/interpolation, unselected terms remain independent of selected parents' private variables except through their declared own terms. The reference selected-parent theorem remains valid with arbitrary such fixed outside evolution and prescribed selected-seed-independent interventions.

Assume independent parent paths and `E b_i(eta_i)^2 <= b_rms^2`. A deterministic bound b gives `b_rms=b`. No CP stochastic error model is assumed.

### B2. Proof of the effect theorem

For selected S, independently interpolate its residuals by parameters z_i in [0,1]. The multivariable fundamental theorem of calculus is the exact identity

`U_actual = sum_{F subset S} integral_[0,1]^F partial_F U_(z_F,0_(S\F)) dz_F`.

Other residuals remain at full strength. Work in the Hilbert space of the complete initial-frame Fourier Kraus array acting on an arbitrary input vector, including the square roots of all classical path weights and all ordinary dilation outcomes. The desired effect is its squared projected norm.

Fix a summand F, and write W=S\F. Its mixed derivative is the sum of time-ordered Duhamel integrals with one insertion `-i R_i` for each i in F. All residuals of W are deleted. Drop F's nonzero-Fourier projections, an L2 contraction, and average their initial seeds by Parseval. Fix their private paths.

For fixed insertion times and interpolation values, divide each insertion by its operator-norm envelope. Every resulting contraction has a unitary dilation with a fresh finite ancilla and a deferred final projection. These prescribed dilations depend on F's fixed variables, not W's private variables. The whole extended evolution therefore satisfies W's reference additive interface. Its chosen, unnormalized contraction-outcome effect is at most the full outcome-summed effect, hence at most `q_ref^|W| I`.

Minkowski's inequality over the insertion integrals gives norm at most

`q_ref^(|W|/2) product_{i in F} b_i(eta_i)`.

There is NO factorial: the derivative's order simplices partition the product of the distinct insertion-time intervals. This remains true for overlapping/nested intervals and noncommuting bath operators. All bath factors remain chronological.

Now average F's independent paths in L2. This contributes `product_{i in F} sqrt(E b_i^2)`, not `product E b_i`. Finally apply Minkowski over F. The resulting norm is at most `(sqrt(q_ref)+b_rms)^|S|` times the input norm. Squaring proves

`effect(all chi_i!=0 for i in S) <= (sqrt(q_ref)+b_rms)^(2|S|) I`.

Cap the homogeneous parameter at one. If an independently established ACTUAL action theorem supplies action `a_actual`, the same Kraus family also permits

`p_coherent=min(1,a_actual^2,(sqrt(q_ref)+b_rms)^2)`.

Do not substitute the old reference action for `a_actual` unless its bound is still true after adding control errors.

### B3. Essential support hypothesis

The effect theorem above is not by itself a memory theorem. For the existing character-support proof, require

`R_i(g_i,eta_i,t')=Ad(g_i)[R_i,eta_i(t')]`

(up to the consistent conjugation convention), with the bracket independent of the INITIAL g_i. It may depend on its own entire update history as specified by the physical causal model. Every affected memory/ancilla support must be included in the frame's full detection/zero-character qualification, reservation and geometry. Full Pauli initial frames on the complete bounded support are one sufficient algebraic choice; merely retaining the old stabilizer group without checking its enlarged support is not.

Then every Pauli factor from the actual reference-plus-residual interaction has the same initial-frame character as its memory Pauli. The existing termwise completion argument survives. If this covariance fails, a seed-independent residual memory rotation can sit entirely in the zero character. The effect bound remains true but no longer certifies correctness.

### B4. What finite-width ramps actually establish

An illustrative sufficient internal-control model is an exact intended local drive path `C_eta(t')`, independent of the initial frame g, acting after g. Let V be the fixed laboratory coupling, independent of both private coordinates. In its exact control frame the actual noise is

`g^dagger C_eta(t')^dagger V(t') C_eta(t') g`.

The ideal reference replaces C_eta by the corresponding piecewise-constant Pauli eta. If the two agree outside the finite ramp supports, their difference is initial-g-covariant and has norm at most `2J` on those supports. Thus

`b_i <= 2J times total ramp length`.

An additional joint drive/control residual must be added with its own verified action; it is not bounded by 2J automatically. This covers ambient drift during EXACT finite-width internal rotations, under the whole-compiler premise. It leaves initial/final frame implementation, tracking and classical privacy ideal unless they separately satisfy the same full support/covariance/action contract. Matching endpoints alone does not supply that contract.

With one uniform qualified residual action u for every counted initial/update/final slot, `b_i<=u(c+N_i)`. For Poisson mean mu,

`b_rms <= u sqrt((c+mu)^2+mu)`.

The variance term is required. Replacing it by `u E(c+N)` inside the squared effect is generally unjustified. With a deterministic count cap or fixed control schedule, use the appropriate bounded second moment; exceptional schedules still require an explicit local CP bad branch, not a fictitious coherent-path flag.

## 5. Deterministic finite-resource alternative

A separate reference protocol avoids Poisson tails and arbitrarily close events. Split t into M fixed cells of lengths delta_l, and choose independent fair frame values per generator in every cell. Express these values by the first fair bit and M-1 independent fair flip increments. Internal ideal updates occur only at the fixed boundaries.

For each witness generator the combined bra/ket correlation kernel is one when every cell contains an even insertion count, and zero otherwise. The initial-bit Fourier condition makes the first-cell parity even once the other cell parities are even. The positive Dyson majorant therefore is exactly

`B_det = 1/2 [product_l cosh(2J delta_l)-1]`.

For equal cells,

`B_det=1/2 [cosh(2Jt/M)^M-1] <= 1/2 [exp(2(Jt)^2/M)-1]`,
`q_det=min(1,a_ref^2,m B_det)`.

The identity also follows from `E sinh^2(J sum_l delta_l xi_l)`; `xi_1=1`, later relative frame values are independent fair signs. The inequality uses `log cosh x<=x^2/2`.

The actual flip count is `N~Bin(K,1/2)`, `K=m(M-1)`, with maximum K. It is independent of initial frame bits but correlated with the weak path. The CP proof drops the healthy weights before averaging, so nevertheless

`f_det=1-(1-epsilon)^c(1-epsilon/2)^K`,
`p_CP,det=min(1,q_det+f_det)`.

For covariant coherent per-slot action u,

`b_rms <= u sqrt((c+K/2)^2+K/4)`,
`p_coherent,det <= min(1,(sqrt(q_det)+b_rms)^2)`

and an independently valid actual action bound may also be used. Deterministic upper-count accounting `b<=u(c+K)` is simpler and more conservative.

Finite-width boundary layers can be placed inside this SAME t, rather than adding random latency, provided their full supports fit between adjacent fixed boundaries. For serial generator ramps of width delta, a sufficient separation condition is `m delta < t/M`, with correctly reserved endpoint margins. This is a timing condition, not an error or privacy certificate. The protocol is established iid randomized-decoupling territory; no novelty is claimed for the protocol.

## 6. When the paid bound really beats action squared

Let `a_old^2<1` be the old certified bound for the comparison protocol, with the SAME complete reservation/geometry if one wants a direct budget comparison. The exact sufficient tests are

- CP: `q_ref + f_control < a_old^2`.
- Coherent: `sqrt(q_ref)+b_rms < a_old`.

They define nonempty mathematical regimes, not measured hardware regimes. For any fixed finite reference rate or deterministic M with `q_ref<a_old^2`, sufficiently small qualified epsilon or residual action satisfies the appropriate strict inequality. Increasing rate indefinitely at fixed nonzero control error does not: the CP flag mass tends to one and coherent accumulated action grows.

For a concrete symbolic existence certificate with `a_old=a_ref=Jt>0`, choose a finite M so that

`(m/2)[exp(2a_old^2/M)-1] < a_old^2/4`.

For example any integer `M>2a_old^2/log(1+a_old^2/(2m))` works. Then either

`epsilon(c+K/2)<3a_old^2/4`

suffices for the CP model, or

`u sqrt((c+K/2)^2+K/4) < a_old/2`

suffices for the coherent model. These are dimensionless inequalities, not invented gate-performance numbers. Stronger slack may be chosen.

For pure ambient mismatch in exact internal ramps, with boundaries still exact and ramp action bounded deterministically by `2J K delta`, taking `delta<t/(4K)` gives residual action below `a_old/2`; impose the spacing/margin conditions as well. This mathematical limit may demand growing drive strength. No fixed bandwidth, bounded-power, or actual gate-noise assumption guarantees it.

At small reference action and large M, `q_det ~ m a_ref^2/M`. The CP union envelope balances this against `epsilon mM/2`; the coherent envelope balances its square root against accumulated residual action. These describe optimizing sufficient bounds only. Costs may depend on rate, width or pulse amplitude, and must then be optimized with those actual dependencies.

## 7. Memory composition and duration accounting

For Theorem A, a control-fault parent is arbitrary over its ENTIRE reserved patch and interval. It is not merely a clean endpoint birth. Apply the already audited whole-gadget bad-parent support treatment, including any omitted correction at the start, and recompute guarded support, parent windows and coloring if needed. Theorem B with the actual character-support covariance can retain the pulse character completion proof only on its genuinely qualified full support.

With the appropriate full-interval geometry, the inherited sufficient budget has the form

`d0(tau)+mu_int(tau) p <= q_star^Q`,
`d0(tau)=delta_ideal+2DN kappa^2 tau(Delta+2tau)+F nu(Delta+2tau)+N kappa tau`,
`mu_int(tau)<=kappa N(Delta+2tau)`.

Every initial/final gate, ramp, reset and fallback must fit in tau. If control implementation enlarges tau or the reserved supports, the old constants are not automatically reusable. A valid comparison then is

`d0_new + mu_int,new p_new < d0_old + mu_old a_old^2`,

with a common already-qualified contour target, or a separately requalified geometry. Merely lowering p while increasing duration/conflict costs does not establish a better memory regime. No lifetime theorem follows from a global finite-horizon norm correction alone.

## 8. Norm-only fallback when privacy or character support is absent

If a full joint, time-aligned Hamiltonian comparison only certifies a total residual action `A(eta)` on feasible paths, Duhamel gives `||U_actual-U_reference||<=A(eta)`. For unitary channels, including an untouched reference, their diamond distance is at most twice this operator distance. Subsequent CPTP operations contract it. Averaging, and allowing arbitrary output on a declared exceptional event E, therefore gives

`||Phi_actual-Phi_reference||_diamond <= min(2, 2 E[1_(not E) A(eta)] + 2 Pr(E))`.

For a per-control action u, a conservative one-parent replacement is `2u(c+E N)+2Pr(E)`. Over an entire experiment the sum counts every relevant parent/control. This is an operational global error bound; it generally grows with spacetime volume and cannot be substituted as a local-stochastic parameter. It does not create an exact good CP subchannel, enforce initial-frame covariance, or turn an arbitrary Kraus label into a support certificate. Deriving a different coherent fault-path memory theorem would require its own proof.

For an uncapped Poisson implementation, the count formulas describe almost-surely finite pathwise operations on the retained finite quantum space, followed by a classical path average. They do not provide a uniformly bounded physical controller/record implementation. The capped or fixed-M protocols are the finite-resource alternatives; discarded mathematical fault records are not promised as accessible online registers.

## 9. Scope and stopping point

The task supplies exact conditional tradeoffs and explicit reasons why weaker input interfaces are insufficient. The CP branch theorem is internally independently audited; the coherent theorem has a separate proof audit in this directory. Neither establishes generic noisy-control hardware or a new autonomous memory model. The next gate is stated in `NEXT_GATE.md`; bounded self-authored checks are in `check_control_cost.py` and `checks.json`.
