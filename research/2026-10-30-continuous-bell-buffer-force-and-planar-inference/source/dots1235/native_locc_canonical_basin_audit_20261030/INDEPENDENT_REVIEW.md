# Independent actual canonical-basin interface review

2026-10-30. Reviewer: `producer-workspace/audit_topology_free_noise`.

## Verdict and scope

**PASS for the actual structural interface** in `ACTUAL_CANONICAL_BASIN_INTERFACE.md`, SHA-256 `33ff57063184e8386ed412ce11cfb1b72e6c1e058fe239c5993fd89afc745f3b`.

This certifies the nominal/noise system-leg support, outer-radius crossing energy, raw/discount commutation, protected Bell-module and clean initialization premises stated there. It does not certify the separate compressed-circuit boundary telescope, inner spectral killing theorem, continuous noise bounds, or whole logical lifetime. Source/dependency copies and exact hashes are in `reviewed_sources/` and `SOURCE_MANIFEST.json`.

## 1. Radius and both-sided crossing strip

Choose a fixed deterministic minimum-physical-weight representative separately in the two CSS sectors for each raw relative syndrome. Their weight sum r is a function of that syndrome alone. For a relative Pauli edge f of CSS weight at most ell, adding f to the old representative is a candidate at the new syndrome, while applying f again gives the reverse comparison. Thus `|r(delta')-r(delta)|<=ell`, without a trajectory, logical-class or stabilizer-history assumption.

For `P0=1_(r<r0 N)`, every nonzero matrix element of a local leg crossing its boundary has both endpoint radii within `[r0 N-ell,r0 N+ell]`. The upper endpoint, not only the lower, must lie below the common confinement radius. The fixed strict margin on r0 and a sufficiently large N ensure this for the finite union of support sizes used in the proof. No graph partner/topology condition is needed for this elementary radius statement; it does not independently enlarge the governing noise class.

A minimum same-syndrome representative is in particular reduced under stabilizers. The accepted confinement bound therefore applies to both canonical endpoints in this strip. Summing the two sector inequalities with the common minimum h gives `U>=h r`; all additional apparatus-debt terms in E are nonnegative. Consequently the complete crossing strip obeys

`E>=U>=h(r0 N-ell_max)`.

There is no inference from low syndrome energy globally to absence of logical error, and no replacement of the radius projector by an energy cutoff.

## 2. Actual commutations and fixed supports

In the accepted exact forest frame, U is a local commuting raw-relative-stabilizer function, mechanical history projectors are DATA independent, and false-token terms are diagonal functions of raw Alice stabilizers and actual computational value/validity registers. Thus E and V commute P0, including arbitrary absolute-syndrome superpositions.

The A/C matrices have only controller/tag/monitor off-diagonals. Their DATA controls are diagonal raw-syndrome/program-truth functions, as is the normalized useful decrement. Hence every exact discount C_h commutes P0. Its product V_c and positive square roots/inverses do also. No analogous commutation is asserted for the later debt/activity/exposure dressing.

Every physical local system leg is first put through the actual bounded-depth forest frame. Raw-V similarity adds only a fixed incident family of local commuting energy terms. Exact commuting discount similarities add only factors that fail to commute the original leg; all disjoint factors cancel. The raw-reference debt/activity witnesses are fixed finite-support polynomials chosen before the weak Bob LOAD and proof t. The exposure witness is the full physical polynomial with its finite pinching/support enlargement, not the withdrawn private-process witness. Thus all Xi and actual framed system legs have bounded support independent of N and the later small parameters.

Their finite Pauli expansion on DATA and matrix-unit expansion on auxiliaries bounds the relative CSS edge weight by a fixed ell_max. Both laboratories and both CSS sectors must be counted; using twice the union DATA support is safe. The expansion is algebraic, never a stochastic Pauli model, and no number of coefficients is charged as a probability factor.

Because E is a bounded-incidence sum of commuting bounded local terms, a local Xi has a fixed energy bandwidth and energy-conjugated norm bound from the incident summands. `[P0,E]=0` gives `||exp(theta E) P0 Xi P0 exp(-theta E)||<=||exp(theta E) Xi exp(-theta E)||`. The corresponding V_c local weighted bound follows by exact cancellation of the commuting distant C factors and uniform local inverse bounds. This does not use a global condition number and does not claim that P0 Xi P0 is spatially local in the ordinary tensor-product sense.

## 3. The protected object is a Bell-target module

Let Omega_s denote the accepted matched signed Bell vector in the common absolute syndrome sector s. The module is the coherent span of `(I tensor R_delta) Omega_s` for radius below r0 N, tensored with arbitrary apparatus/bath/reference states. This target is fixed: it is not all logical states of the enlarged bilateral code space.

The signed Bell relation moves an Alice Pauli through Omega_s to Bob, with a transpose and an absolute-sector shift. For `P_A tensor P_B`, the relative edge is f=`P_A^T P_B` up to phase. Starting from delta and ending at delta', both inside P0, the Pauli `R_delta f R_delta'` has zero syndrome and weight bounded by `2 r0 N+ell_max<d_N`. It must therefore be a stabilizer rather than a nontrivial logical operator. Its sign on the shifted sector is absorbed in the auxiliary gauge/bath coefficient.

This proves that every compressed bounded-support Pauli leg, and hence every compressed local operator by finite linear expansion, maps the module into itself. It covers arbitrary absolute-syndrome coherence and arbitrary retained bath coefficients. No positive fault record is needed for this exact span statement.

For self-adjoint Xi, invariance makes the module reducing for `P0 Xi P0` inside P0. Its exponentials, adjoints and products preserve it; so do spectral functions of the resulting self-adjoint witness. Raw E and V_c already preserve it by their syndrome/controller form. Thus the compressed proof circuit and inner spectral projector, if otherwise correctly constructed, do not leave the protected Bell module.

The same edge argument must include actual Hamiltonian, jump, complete-loss and noise system legs in the chosen finite support bound. The local complete loss has the same support as its bundle, so it is not omitted by checking jumps only. A finite-system-leg expansion also handles joint bath maps without a bath-dimensional Pauli expansion. This proves only the support/factorization premise, not the analytical trace-norm boundary estimate for those maps.

## 4. Fixed final decoder and reference meaning

The accepted ideal relative decoder measures both complete syndromes, applies the fixed minimum representative of their difference to Bob, and uses matched signed-sector decoders. On every vector in this module it extracts the **same** pure encoded Bell state. Remaining syndrome-dependent stabilizer phases and all controller/bath/reference amplitudes stay in the auxiliary factor. This is the scheduled addendum's section 5 algebra, independent of a scheduled fault-record proof.

Accordingly a module-preserving killed channel can have a Bell factor with an arbitrary trace-decreasing gauge/reference map. Comparison with the full physical channel and its preserved reference marginal still requires the separate killed-channel approximation theorem. The claim is a Bell-target/gauge-input channel bound, not identity protection of arbitrary unknown bilateral logical input. No target gate is inserted into the recovery and no physical/noisy final decoder is claimed.

## 5. Initialization

With actual clean I/W0/P0 engines, no own tags, empty channels, Alice IDLE and Bob FLUSH_SEND(0), all mechanical, semantic and activity flags vanish. On the ideal Bell-target module with delta=0, U and every current decrement vanish. Positive own-corner debt/activity witnesses therefore annihilate the initialized range, and the exposure factor does too because a_h=0. Every A/C discount is identity there. Compression by P0 leaves this range unchanged. Hence the initial compressed dressed witness has eigenvalue one on it, and its initial moment is exactly one, uniformly over the allowed gauge/reference states.

Arbitrary initially occupied classical pipes allowed in an older stochastic theorem are not imported here. A source-error initialization requires its own small support/moment and common-module envelope. Sparse source Pauli errors enter the module only after the usual distance comparison with their canonical representatives; average pair fidelity alone is not that envelope. No claim of bare arbitrary dirty-input protection or asynchronous source acquisition is added.

## Remaining whole-proof obligations

The actual local service/first-order receipts and this structural receipt are compatible, but they are not by themselves a continuous-memory theorem. The compressed-circuit telescope, inner/outer spectral separation, norm-controlled joint noise, killed comparison, initialization/source budgets and final reference error must be assembled and freshly reviewed in one frozen manuscript. The actual grouped finite-dimensional two-site Hamiltonians, onsite resolved resets, measured classical interparty transport, finite queues/clocks and ideal forest/relative encoded output restrictions remain in force.
