# Whole finite-device receiving with a common unbounded free bath
30 October 2026. Construction of a single model-extension receiver. Independent review required. This does not change the finite hardware, supplied source domains, reset resource, or logical tasks of any received theorem.

## 0. Statement and frozen foundations
Fix a device size N and a finite scheduled duration. The physical SYSTEM consists of finitely many finite-dimensional native sites and the actual finite protected-factory/record helpers. It may have polynomially many sites, not only O(N) DATA. Let B be a separable Hilbert space. Supply a bath-only strongly continuous normal CPTP semigroup V_t on trace class, with possibly unbounded generator B_0. All remaining dynamics have the form B_0+K(t), with K pointwise strongly measurable on trace class and an integrable completely bounded trace-norm majorant on every finite interval. Assume the ACTUAL full propagators are CP/TP on every subinterval. The native/local perturbations retain their stated finite-system support and incident complete-norm budgets. All unbounded dynamics are in this SAME supplied bath-only base; system-bath interactions are cb-BOUNDED. No low-energy input restriction replaces that condition.

Under these premises the following already accepted finite-device results receive the same bath extension, with unchanged error formulas and native/code constants, except a possible factor2 in the local perturbation budget for the explicit centering convention in §1:

1. Native global energy/BUSY memory, its fixed code cut, full-versus-killed comparison and exact unknown-logical factor.
2. CP/TNI scheduled FT, actual finite dirty resets, known-target factory, top-down physical quantum output, native warm boot, and concurrent known-resource factory beside unknown native data.
3. Actual protected destructive rank-one CSS/Bell instrument, including genuine protected physical-leaf erasure into the EXCLUDED reset reservoir; distributed protected-classical Pauli feedforward; and their already accepted measurement-survivor common-source handoff.

This receives their original TYPES of input/channel domains and target scopes, not arbitrary initial logical/bath assignments. On the enlarged auxiliary algebra containing this infinite B, supply a NORMAL common source channel J=Id_logical tensor J_aux (or the original explicitly allowed classical direct sum), with the same basin/hard support and dual operator energy/BUSY envelopes for EVERY normalized input and finite-reference extension. A concrete finite-bath preparation channel, or a bound proved only for its particular finite-bath state, has no automatic unique extension to this new input algebra. Initial source error certificates must also be completely/reference-uniform on that declared enlarged domain. The finite-system safe-support embeddings and positive repairs constructed below do extend normally; this does not construct an unspecified initial J. It does not assert an additional teleportation/cycle theorem unless its separate finite-device receipt and matching chart are supplied. In particular the known-target factory is not promoted to an arbitrary unknown-input factory.

Governing local sources/receipts (all under producer-workspace/57d8dd795b13 unless absolute):
- recovery_infinite_bath_cavities_20261030/ROOT_UNBOUNDED_FREE_BATH.md, SHA256 25ead9254477707014505c1d91ba62e8e3e4143fe9fff09fd546caf10be904a5; independent review in recovery_quantum_control_20261030/review_unbounded_bath/INDEPENDENT_REVIEW.md, SHA256 1d63ef28d417a5c17a5b96a5659531450d9d85e29738ea5215d922fb461fced6.
- producer-workspace/INDEPENDENT_REVIEW.md, especially §§6–10, and producer-workspace/INDEPENDENT_REVIEW.md, especially its relative common-bath perturbation and scalar moment argument.
- recovery_consumer_receiving_review_20261030/frozen_sources/Q_AND_RECEIVER_GLOBAL_MEMORY_CONTRACT.md; producer-workspace/WHOLE_RECEIPT.md; actual hardware producer-workspace/UNIFIED_GENERATOR_INTERFACE.md.
- recovery_cp_cavity_review_20261030/tni/INDEPENDENT_REVIEW.md and TRACE_FACTOR_COMPLETION.md; recovery_standard_ft_review_20261030/INDEPENDENT_REVIEW.md.
- recovery_complete_factory_review_20261030/INDEPENDENT_REVIEW.md (3388f65ef041ab5868f62a7123a68c3cbc7d2ed4fa7c59e310d88836481fef92) and BINDING_COMPLETIONS.md (2048c62a3f875c64208cb5e338e133c50c1b0cb9d11cca19f94396275dcd3267).
- recovery_quantum_control_20261030/CONCURRENT_FACTORY_NATIVE_RECEIVING.md (b2643b8826515377495e98c3fb75e0c43eb7b9d217eb60c2d0388442dd060dcd), its corrected full-k resource addendum, and review_concurrent_factory/INDEPENDENT_REVIEW.md (8e178e13a2c7fb4cdd2d7d7dcab0a7bebcda136d18e48e9c315cd0c0e8d3b535).
- recovery_native_measurement_20261030/review/FINAL_HASH_RECEIPT.md, binding DESTRUCTIVE_CSS_MEASUREMENT.md (1008c6622d2c5d489b27f913de4dd7ff7a5a47d381dfb93d35da44f7f2e7efd1), ACTUAL_PROTECTED_ERASURE.md (211f17ac7b51efb9a44312bb73ea8005ffc9a452e20c0151eb6f5d928e21dd91), and FULL_OUTCOME_CONDITIONED_INSTRUMENT.md (c3c2f8f7ed19a1694c51d16ca0e1fbb9ca5ec4ad03589c6bbcc929a896d2bfc9). DIRECT_ERASURE_BINDING.md in that review directory is binding.
- recovery_native_feedforward_20261030/review/FINAL_HASH_RECEIPT.md, binding receiving/WHOLE_DISTRIBUTED_FEEDFORWARD.md (1a3499a696ea422eb6a29156f9588457ac6a6497263fcdaeb796a384e053e08b).
- recovery_measurement_survivor_handoff_20261030/review/FINAL_HASH_RECEIPT.md, binding MEASUREMENT_SURVIVOR_FEEDFORWARD.md (3b902901c3807fc4c9cc49e11de37dc0e94764838648eeeba14faee0ef078e40).

The earlier finite-bath receipts are not edited. This new receiver states precisely which proofs now extend and why.

## 1. Conservative bath-only terms and an optional centering repair
The native moment proofs require bath-only terms to annihilate system-only observables. This is automatic for the free CPTP base. It is also automatic for a bounded bath-only term D_B with D_B^*(I)=0; separate CP of D_B is unnecessary. If the full bounded decomposition is

 K=L_nom+D_B+sum_e N_e,

with L_nom conservative, normal HP local N_e but not individually centered, full TP gives D_B^*(I)+sum_e N_e^*(I)=0, almost everywhere. The latter identity follows on the predual from trace preservation on every subinterval and the mild equation, by scalar Lebesgue differentiation on a countable dense set. Alternatively it may be included explicitly as the conservative decomposition convention.

Write A_e=N_e^*(I), a bounded self-adjoint operator on the same finite system support and B, and J_A(X)=(AX+XA)/2. Set

 N'_e=N_e-J_(A_e),
 D'_B=D_B+sum_e J_(A_e)=D_B-J_(D_B^*(I)).             (U1)

Then N'_e and D'_B annihilate trace. The sum correction in D'_B is bath-only by the full conservative identity. Each N'_e has the same assigned system support, is normal HP, and has complete norm <=2||N_e||. All sums converge in norm under the finite-system incident bound after bath-only terms have been separated. The ACTUAL generator is unchanged; D'_B need not separately generate a CP map. It contributes zero to system-only observables. The common-base cavity lemma still uses B_0 as its base and includes D'_B as a bounded perturbation, so no positivity of the recentered pieces is smuggled in.

Thus choose native/FT thresholds using eta'=2eta if recentering was needed; if the original convention already centers these terms, eta'=eta. After a killed compression, local terms may again become noncentered, precisely as allowed by the CP/TNI cavity lemma. Do not recenter a killed process by returning its lost trace.

## 2. Existence of system-only killed processes and all processor cavities
Every native forest, canonical code chart and cut is a bounded finite-SYSTEM operator tensored with identity on B. In particular P commutes with V_t and preserves the free generator domain in the autonomous case. Restricted to the corner P, the bath base is still the same semigroup. Let Q_(t,s)(X)=P T_(t,s)(PXP)P on that corner. It is normal CP/TNI. Its zero and first Dyson terms match the bounded-perturbation mild propagator for

 B_0+K_P(t),      K_P(X)=P K(t)(PXP)P.

The same first-order matching/product proof as the accepted unbounded-bath lemma applies (the embedding/restriction here are corner inclusion/compression instead of maximally mixed extension/partial trace). Thus the complete-loss killed propagator is CP/TNI on ALL trace-class inputs in the corner, with original losses retained. No unbounded generator has been differentiated or normalized by hand.

The processor cavity reductions use only finite active gate blocks, chosen as unions of current intended blocks. They commute the common free bath base. The accepted lemma gives actual normal CP/TNI cavities and convex interpolants, and the same inclusive local fault law. This also applies to the actual native-killed process: its cut is processor-independent during the admitted waiting stages; bounded compression does not enlarge processor support or norm. Nominal native system generators and other helper dynamics may have large total bounded norm, but their processor-complement parts disappear from the differentiated local fault terms. At active-space schedule switches concatenate the finitely many actual intervals; no change of bath or physical projection is performed.

All limits are for a FIXED finite system and fixed finite horizon. No thermodynamic limit, finite bath cutoff or dimension limit is used.

## 3. Native finite-system drift becomes a mild expectation inequality
For fixed N each native witness W (global F, BUSY G, raw energy functions and finite proof pullbacks) is a BOUNDED finite-system operator, though its norm may be exponential in N. The accepted local relative estimates do not estimate it by that global norm. The free adjoint fixes it exactly:

 V_t^*(W tensor I_B)=W tensor I_B.

For any actual full or killed positive trace-class evolution, the mild equation consequently gives

 Tr(W rho(t))-Tr(W rho(s))
       = integral_s^t Tr(K(u)^*(W) rho(u)) du,          (U2)

with the appropriate corner restriction and complete-loss bounded K for killed evolution. The same identity holds with finite reference ampliations. Expectations are locally absolutely continuous; differential inequalities hold almost everywhere. No initial state needs finite bath energy, membership in D(B_0), or a norm derivative under V_t.

The actual native algebraic drift inequalities are finite-system operator inequalities with arbitrary normal bath coefficients. Their extension here is literal tensor/normal-map receiving, not a finite-dimensional-bath approximation. The global audit §6 already uses bounded finite system/proof cones and joint cb norms; §9 explicitly expands only finite SYSTEM matrix units and assumes no finite bath dimension or bath coefficient-sum bound. The BUSY receipt likewise uses finite-depth system-only gates and local relative congruences. Their system-only finite controller inverses, dirty resolvents, guarded proof maps and finite-depth forest factors do not involve the bath generator. Bath-only terms in §1 vanish; local weak terms retain the same relative bound C eta' N W.

For the killed energy drift, use the RECEIVED commutation [F,P]=0. For any positive state in the corner, removing the outside diagonal block after one actual CP step cannot increase its F expectation: Tr(F P T(rho_P)P)<=Tr(F T(rho_P)). The common-base mild first-order identity therefore gives the same full drift upper bound for the killed corner, with original outgoing loss retained. This is not an assumption that each local HP summand is CP. The BUSY drift is still used on the full evolution and transferred once at the endpoint, as in the finite receiver.

For the killed energy law let x=Tr(F rho_P), sigma=T_*(rho_P), and V_G the finite-system positive raw potential. T is the actual system-only normal unital CP proof map. Its predual remains positive and trace-preserving on the joint trace class. The scalar spectral measure of V_G on sigma is a FINITE spectral measure for each N even with an infinite bath. Thus the same scalar Jensen inequality

 Tr(V_G log(V_G) sigma)>=x log(x/Tr sigma)>=x log x

holds, with the zero-state case by continuity. Inserting the received drift in U2 proves the identical log-moment inequality and solution. BUSY uses the same scalar argument. All barrier/warm parameter gaps and the pointwise, fixed-request-time interpretation are unchanged. An infinite bath does not produce an anytime stopping theorem.

## 4. Full-versus-killed boundary and exact native logical identity
In the common-base Duhamel comparison, B_0 commutes P and has NO outgoing block. The difference source between the full propagator and the included killed one is therefore built solely from the bounded local terms. Both propagators are complete contractions by §§0,2. For a q-site term, choose finite system matrix units and write its predual action as a finite sum of system matrix-unit legs tensored with coefficient maps on the bath trace class. Coefficient maps are normal on the dual, with complete norms bounded by the joint cb norm up to a fixed finite-system constant. The number of coefficients depends on q/site dimension, not dim B. There is no bath-basis expansion.

For each outgoing system leg the same native boundary-source restriction applies. For a positive trace-class rho, the off-diagonal trace norm satisfies the usual Hilbert-Schmidt factorization/Cauchy bound, e.g. ||R rho||_1<=sqrt(Tr(R rho)) sqrt(Tr rho) for a projector R. This identity is valid on separable infinite Hilbert space. Applying normal bounded bath coefficient maps preserves its norm estimate. Hence the accepted polynomial(N)(1+T)exp(-cN) full/killed bound follows unchanged from §3 moments, uniformly with references. Bath-only generator norms and helper-only nominal terms do not enter this boundary budget because they have no old-cut outgoing blocks.

Inside the finite system basin, each local Pauli/matrix-unit edge has the SAME canonical logical identity by the received distance/representative proof. Bath coefficients remain arbitrary normal maps. Consequently the entire bounded killed generator, and hence its mild Dyson propagator with identity logical free base, factors EXACTLY as Id_logical tensor a CP/TNI auxiliary evolution. This uses the native correctable-span theorem, not merely CP/TNI or a bath-only cut. Product-bank cuts and common-reference statements are obtained in the same finite system chart, with the original bank-union costs.

## 5. Actual ordinary FT/factory/reset algebra has no finite-bath step
The local inclusive complete-norm law is now supplied by §2 and the accepted 25ead925 lemma. All disjoint rectangle recursions, prefix-free top-down output stages, grouped physical resource-region predicates, exact signed cardinality sieves and their mixed conjunctions are FINITE sums for fixed N and concatenation depth. They are algebraic sums of normal predual maps and use complete contractions, not Choi matrices of the bath. Their bounds therefore remain identical, with no bath dimension factor.

The common code decoder/intertwiner is a finite-system isometry. The KL identity for finite supported system errors has the form V^* E_a^* E_b V=c_ab I_logical. With arbitrary bath coefficients it is a finite sum of the same system identities times normal coefficient maps; extension to trace-class inputs follows by linearity and continuity. This proves the entire common two-sided sparse module, not just pointwise logical fidelities. Arbitrary-input child totalization is the same supplied finite-code gadget identity. Exact field arithmetic, inverse encoder and the mixed qudit-to-qubit transfer are unchanged finite system gates.

The global target-synthesis comparison uses a common finite-system syndrome chart and fixed CPTP inverse extension. The actual output has trace <=1 even on a killed process, giving ||K_aux||_1<=1+b_comp for every normalized positive extended input. Replacing the known target with the same signed syndrome coefficient costs (1+b_comp)epsilon_synth; subsequent maps are normal CP/TNI contractions. This requires no finite-dimensional bath state or maximally entangled bath Choi probe.

Actual replacement primitives are STILL the supplied system-only Lindblad resets with their excluded Markov reservoirs. Their intended finite-time system channel differs from exact replacement by <=2exp(-kappa tau) completely, including entangled infinite retained inputs. Isolated intended gates factor from the earned complement CP/TNI propagator; exact-target cavity receiving pays this discrepancy and all duration noise. The reset does not reset the modeled B. Native ready boot, grouped DATA+lock/monitor regions and old-bank concurrent receiving all remain exactly as in their receipts.

Their final positive target-specific projections are finite-system projections tensored with bath identity. Subnormalized gentle compression and normal KL charts give the same warm sources, full retained trace errors, and CP/TNI auxiliary factors. Compressing the finite-system operator envelope F<=exp(gN)exp(sE) on the SAME support gives dual operator warm bounds on the ENTIRE declared auxiliary input algebra, including infinite retained B. The next CPTP chart is the fixed embedding of that safe support; the current comparison map is TNI INTO it. No survival normalization is introduced.

## 6. Measurement, protected erasure and outcome-conditioned repairs
Use the FINAL measurement receipt and its actual protected-erasure completion, not the rejected retained-copy shortcut. Capture, sanitization, bottom-up encoding, padded finite GPT decoding, protected copying, and recursive physical-leaf erasure consist of finite system circuits for each N. Their bad predicates and common Pauli/KL identities are the same finite sums received in §5.

The direct erasure induction contracts good child logical factors to trace. Treat the union of incoming ket-exceptional, bra-exceptional and bad-erasure children as arbitrary, with size at most2r_res+k_bad<d_code. In a Heisenberg test against ANY bounded retained-output observable, expand only the finite child/system legs. Coefficients are bounded bath/auxiliary operators; no finite bath basis is chosen. Finite-code local indistinguishability then makes the upper logical factor scalar, with an arbitrary normal retained auxiliary map. Normality and trace-class duality identify the FULL retained output map. Thus actual good erasure removes the copied logical coherence in the infinite modeled retained bath just as in the finite model, but ONLY because the reset's dissipative reservoir is excluded. Retaining a closed unitary dilation of that reservoir still invalidates this conclusion.

All outcome labels are finite in number for fixed N. The true rank-one measured projectors, legal fixed input-basis/maximally-mixed logical probes, finite logical partial traces, output-label compressions, and CP/TNI auxiliary repairs are normal maps. The complete norm of a controlled classical direct sum is the maximum block norm on its trace-class direct-sum domain; no number-of-outcomes factor is introduced. Positivity of a repaired auxiliary map is proved by its construction from an actual normal CP map, not by a finite-bath Choi matrix. The trace-effect/positive-factor arguments use bounded effects A^*(I) and complete contraction and therefore extend verbatim.

The actual measurement-survivor and distributed-feedforward proofs use ONE killed process, the same system-only support cuts, one BUSY transfer and legal common-chart probes. Sections2–5 supply precisely these statements with the new B. Their existing full retained-bath CP/TNI error formulas and source-domain qualifications are consequently unchanged. Classicality requires actual protected erasure; outcome-conditioned auxiliaries remain permitted. No independent fresh bath, actual fault-label trajectory, rare-outcome division, arbitrary probe outside the source domain, or ideal physical detector is added.

## 7. Conclusion and strict boundary
Every bath-sensitive step of the NAMED finite-device contracts is now supplied: actual full/killed/cavity existence, native drift and scalar moments, normal common logical modules, signed complete-norm recursion, positive source projection, and outcome-conditioned repairs. Their constants depend on the finite hardware, local cb interaction budgets and actual durations, not on free bath energy, dimension or ||B_0||. The original known-target/unknown-encoded-input/source and warm-gap conditions remain, with the NORMAL enlarged-domain source premise of §0. No arbitrary finite-bath source assignment is silently extended.

This is one extension under a STRONG structural hypothesis: a specified common bath-only C0 CP semigroup plus bounded local perturbations and total CP-divisible propagation. It is not arbitrary unbounded noise, unrestricted oscillator coordinate coupling, an inference from finite tomography, a cutoff theorem, a thermodynamic system limit, a physical reset-reservoir derivation, or a claim of historical novelty. Ordinary bounded-interaction non-Markovian FT already admits broad arbitrary baths; the current result closes this CP-cavity/native receiving hypothesis only. No previously rejected ATG, herald, rail freshness, code-margin or output-instrument shortcut is revived.
