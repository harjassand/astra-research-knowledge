# Independent receiving audit: spectral first-exit flags
2026-10-30. Verdict: **PASS the fixed-stage algebra and conditional local weighted-strip mechanism; REPAIR the abstract counting presentation; NOT a full capture theorem.** No positive physical fault process is supplied or needed.

## Frozen sources
- `recovery_classical_capture_20261030/ROOT_SPECTRAL_FLAG_EXPANSION.md`, SHA256 `63f561a5e528f016f43e8c4d8fe7f11d0379ed4da4b76ddd6f5bfb318e1cbdc7`.
- Companion `ROOT_EDGE_ENERGY_PHASE_COMPLETION.md`, SHA256 `0909f59636ad34d7987d17d260b8e094cdffaa66d224b66ffca38e82f91eca0b`.
- Actual strict payload `NATIVE_MAJORITY_PAYLOAD.md`, SHA256 `65cecd2d3d67b1f4da5a21877c8432209c2e635d4944ad8d39899b630216d614`.
- Local acquisition `NOISY_ACQUISITION_MIXED_ANIMALS.md`, SHA256 `624930ec769344dd37d593639f160efd7ae55a9cc1c7d97a362a59f4f71d2a55`.
- Nested graph SHA256 `261724122bcdc734d0f05271337de2f950b3ca3b35cd5c6f06f6e231dfdf1e76`.

## 1. Exact identity: accepted with initial-corner qualification
For X=P_R X P_R, resolving both output legs of L(X) by the complete orthogonal E_alpha family proves the stated K_D + sum Gamma identity. Output of Gamma_(J|D) lies in the remaining P_(R\J) corner. Consequently the finite triangular ODE sums to the actual master equation; uniqueness establishes equality. Reentry does not undo an analytic mark. Complete-loss spectral compression is crucial: no spatial cross-boundary dissipator is removed.

**Required correction:** rho0 must be P_S-supported for the stated initialization. Otherwise v_empty already violates its domain, and the summation proof does not apply. An exact alternative is initial sector decomposition v_D(0)=sum_(alpha union beta=D) E_alpha rho0 E_beta, with initial weighted norm/support law proved separately. This can contain signed/coherent components.

Minor precision: individual E_alpha L(.) E_beta need not be HP, but their complete union-J sum *is* HP when L is HP, since swapping alpha,beta preserves J. None is asserted positive.

Finite-dimensional test `check_triangular.py` uses a generic two-record joint Hamiltonian and joint Lindblad gain. At t=.7, sum error is 2.23e-16 and corner error zero. Nonempty flag components have minimum eigenvalues about -.027, -.271, -.238. This checks the bookkeeping and directly illustrates why positive-history interpretations are false; it is not a proof of infinite-bath existence.

## 2. Local weighted source strips: accepted conditionally
Define ||X||_F=||F^(1/2) X F^(1/2)||_1, including arbitrary auxiliaries. For each finite-system-leg term, an output Q_j from input P_j forces the corresponding input leg into the q-boundary strip. Dropping F_j on that leg gives exp(-b_j/2), b_j=s(delta n_j-q), or b_j=s h(delta n_j-q) for edge energy. If both legs cross, the estimate is stronger. Splitting different newly marked records across the ket and bra still multiplies all their half-barrier factors. There is no need for all exits on the same side.

Remaining weights require the advertised bounded relative-congruence estimate; diagonality and bounded changes of h/U provide it. A bounded-support system-leg expansion of a joint HP perturbation preserves the bath cb norms, up to fixed finite-body dimension constants. Every local term contributes only subsets of the bounded set of records it touches, so a **uniform in D** per-record coefficient envelope r_j(t)<=C n_j(t) can be obtained from the physical incidence budget. Bath-only and selected-record-disjoint terms have zero Gamma. Norms of the full unselected apparatus must not enter.

The edge-energy companion repairs a real potential mismatch: the strict external-majority rule can increase H, so padded-majority H drift is not transferable. All actual flips decrease U; the padded correcting set remains active; H>=U/d yields the claimed negative U exp(sU) drift. Expansion gives U>=hH on the source strip, and U changes by at most qd under a local leg. This validates the proposed atomic specialization, not its separately unfinished native compiler.

## 3. Time-varying CP comparison: repair necessary
For fixed weights, K_D^*F_R<=a_D F_R correctly bounds the complete weighted norm of the CP compressed propagator, including signed inputs. For moving weights the necessary hypothesis is

    partial_t F_R(t) + K_D(t)^* F_R(t) <= a_D(t) F_R(t).

The derivative cannot be omitted from a claim involving F_R(s) -> F_R(t). Counterexample: K=0, F(t)=exp(t)I, a=0; the asserted bound without the derivative is false. Changes of corner/coordinates must be implemented as explicit maps or in a consistently transported frame; ordinary fixed-corner CP propagation does not establish them.

## 4. Correct counting lemma, allowing D-dependent rates
The exact exponential coefficient formula in the source is immediate for state-independent subset rates, but is not justified by merely writing c_(J,D). The desired weaker product bound has a direct proof and does not require that formula.

Fix first-bad stages k_j and discard paths that mark j outside its allowed stage. Put a nonnegative norm majorant x_D on the remaining exact signed paths. Remove the pathwise CP growth factor and each newly marked barrier exp(-b_j/2); let the resulting majorant satisfy

    x_D' <= sum_(nonempty J subset D) c_(J,D\J)(t) x_(D\J).

Assume common envelopes, valid for every D,

    sum_(J containing j) c_(J,D)(t) <= r_j(t),
    integral r_j <= R_j.

Stop each record's envelope at the end of its prescribed first-bad stage. For 0<z_j<=1, G(t)=sum_D x_D(t) product_(j in D)z_j obeys

    G' <= [sum_j z_j r_j(t)] G.

Indeed z_J<=z_j for any j in J and summing incidence only overcounts positive terms. Thus

    x_S(T) <= G(0) exp(sum_j z_j R_j) product_j z_j^-1
             <= G(0) e^|S| product_j(1+R_j),

with z_j=(1+R_j)^-1. This proof handles history/state dependence and simultaneous bounded-body exits without treating flags as physical probabilities.

The initial G(0) is load-bearing. For good-corner initialization it is ||rho0||_(F_S), not automatically one. A usable joint seed law must bound it or allocate its exponential cost against the barrier. Arbitrary initial energy O(n_seed) is not harmless merely because seed size is called a fixed constant: increasing the seed to shrink the claimed error can increase that cost at the same exponential order.

For a prescribed stage tuple, surviving selected records incur CP growth only until their first mark, so geometric fixed-duration growth gives integral n_j(t)dt<=C0 n_(k_j). With R_j<=C n_(k_j), barriers beat growth at small eta if the actual transport constants leave a positive exponent. Independent summation over k_j then gives the claimed product of convergent geometric-stage series. This conclusion remains conditional on common envelopes, successful stage transport, and the initial factor. No final-volume charge is necessary in this conditional lemma.

## 5. Endpoint cuts require their own counting estimate
A simultaneous endpoint projection can mark arbitrarily many records; it is not a q-body generator insertion. Naively its coefficients are at most 3^|J| (three non-all-good ket/bra choices per newly marked record), and their incidence sum is exponential in the number of records. Therefore the continuous-time incidence lemma cannot simply be applied to that projection.

Repair: if the actual CP stage map has a complete joint F_in -> F_out bound, apply the new cut on the output, provided F_out,j is at least exp(b_j) on the ENTIRE Q_j range (not merely the local source boundary strip); then each Q_j output leg supplies the output half-barrier. For exp(sH) this is automatic; for edge energy it needs the graph Cheeger bound through all minority sizes up to n/2, or an explicitly sufficient substitute. The endpoint norm-majorant insertion then has a product generating multiplier bounded by

    product_(eligible j)(1+3 z_j)

(up to explicitly established local constants). This is at most exp(3 sum_j z_j). Repeated eligible endpoints add their counts to R_j; the number before stage k_j is at most a constant times n_(k_j). The coefficient bound thus keeps the same polynomial form. This argument **does not establish** the required F_in -> F_out bound for reset/copy/graph replacement and must not be used as if it did.

## 6. Remaining scope
No contradiction found in the central spectral-cut replacement for fine spatial cavities. It is a useful exact linear-map tool under real CP complete-loss propagators, broad joint HP perturbations, and uniform local budgets.

Still unearned: global phase-energy transport through arbitrary dirty targets, reset ramps, copy, and new graph/cut; initial unknown-bit seed support law; coherent reference-label retention and disposal without a factor exponential in all records; receiving genuinely bad ports by the quantum hot-support theorem; strict native implementation with its physical observable. The localized animal acquisition estimates are not substitutes for global phase-energy transport. The source correctly labels these as separate, and this audit does not accept full record capture or an end-to-end memory theorem.

## 7. Parent's same-phase endpoint criterion (received after main audit)
The union-of-two-basins cut alone does not certify preservation of the previously captured bit. The proposed repair is valid as a deterministic endpoint implication: if the retained old vertices are still within delta_old n_old of their old phase, the new good cut allows at most delta_new n_new errors, n_new<=g n_old, and delta_new<(1-delta_old)/g, then a new good consensus cannot be the opposite old phase. It would disagree with at least (1-delta_old)n_old retained old vertices, exceeding the new cut. The old phase itself must remain analytically fixed during the stage; bounded local legs cannot bridge separated old basins when n_old(1-2delta_old)>q, and any actual old exit must already be marked. Retaining old vertices without maintaining their old basin/phase is insufficient. A PRE-chart cut explicitly relative to the old phase is an alternative. This checks the implication, not implementation of its hypotheses during all stages.
