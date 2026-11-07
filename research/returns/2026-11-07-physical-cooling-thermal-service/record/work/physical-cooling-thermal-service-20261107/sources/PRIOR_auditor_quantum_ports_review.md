# Version-bound hostile audit: encoded quantum ports

7 November 2026. Reviewed frozen inputs:

- `quantum_ports_closure.md`, SHA-256 **d6d9ba449dc6dae53489cb53055a013ecc5650d65154e83cb65a675df2c36fdd**.
- `quantum_ports_coherent_decoder_addendum.md`, SHA-256 **42a0c93e06a1dad901a8066613080356cee1229e8305342f58699fbf8a527681**.

Both hashes were recomputed. I inspected the actual CFG v3 primary text of Definition 22, Lemma 29 and its proof, Lemmas 40–42 and their equations, as well as the previous complete thermal-service/subsystem proof. The frozen notes are not edited.

## 1. Verdict and necessary parameter precision

**PASS: the encoded-port WRITE/READ gap is CLOSED for the stated isolated-staging hybrid model**, using the coherent decoder addendum and the simultaneous parameter choice in Section 5 below. No unresolved algebraic port gap remains at that scope.

The qualification in the frozen closure note that one may add a final dwell must be read with a fixed thermal margin: a dwell cannot lower a moment coefficient below nu_eq. Choose the final capture cutoff FIRST, then beta/eta to place nu_eq below it. Also choose the admitted WRITE postenergy no larger than the core service's postenergy ceiling. These are compatible existential choices, not extra size-dependent resources; Section 5 gives explicit simultaneous inequalities.

The closure requires actual staging isolation, CFG independent stochastic circuit faults and its classical primitives, matched parallel short links, and already-computationally-encoded quantum ports. It is not arbitrary-bath polynomial-time encoding, a vanishing-error bare input/output theorem, a microscopic derivation of the thermal reservoir, or a practical advantage claim.

## 2. Exact CFG deduction and positive auxiliary maps

CFG Lemma 40, equation (128), is a full-module diamond estimate: an encoded realization of an ideal circuit Phi acts, up to `2|Phi|(cp)^l`, as Phi on logical payload and an auxiliary channel on the entire computational gauge. Hence arbitrary computational-gauge/input/reference correlations are allowed. A reduced logical fidelity test would not substitute for this result.

The coherent-decoder addendum stays inside its proved core: pure ancilla preparation, unitary gates and unused final work. One may apply Lemma 40 to the unitary circuit retaining all work, then trace the unwanted encoded output blocks. This avoids any stronger assumption about gauge factorization through adaptive measured classical feedback. Actual discarded-work noise cannot signal to the retained output once its interactions are off.

Lemma 42 is an EXACT positive output-interface mixture on the whole computational module, with bad probability <=2cp and good map id_payload tensor trace_gauge. Lemma 41 supplies an input-interface approximation <=2(cp)^l to a code-supported CPTP channel with a positive good/bad mixture and bad probability <=cp. Its good logical marginal is exactly identity; rank-one Choi support forces its gauge extension to be fixed and logical-independent. This identity-extension statement remains valid when the input is entangled with an external reference.

Independent interface circuits give scalar product flags independent of the payload state. Conditional bad maps may act on payload sites in A and their auxiliary systems. Good maps act identically on the remaining payload sites, even with arbitrary pre-existing gauge correlations. Thus every support branch is CP, has the stated complete intensity bound `p_0^|T|`, and its Pauli system legs have support A with arbitrary auxiliary coefficients. No fictitious reduced local-stochastic channel or product-gauge replacement is needed.

The exponential support tail and moment follow from the positive all-subset expansion exactly as in the note. For CP maps their diamond norm equals their worst-case trace mass, so the intensity bound is reference-uniform. Truncating the positive flag branches costs their actual mass. The full physical output need not be globally close to the ideal encoded state.

One-sided composition gives WRITE error `2S_E(cp)^l` and READ error `2(N+S_D)(cp)^l`: apply Lemma 40 and only the relevant physical output/input interfaces. There is no new bare LOGICAL endpoint in either construction. The operational Theorem 53 conclusion is not silently upgraded to the complete statement; its ingredients prove the stronger needed assertion directly. No physical U_total dagger is appended at READ.

## 3. Common-span decoder and polynomial implementation

The capture error must be combined with the memory error BEFORE correction. With the note's notation the physical Pauli span has representative weight

`w_*=B_link C_0 u_f+B_link q alpha+rho`.

Requiring `D_E w_*<u_dec`, `w_*+C_0u_dec<delta`, `2w_*<delta`, and the Tanner radius margins makes the canonical correction and every combined error differ only by a stabilizer. The condition is on the whole coherent span, including syndrome off-diagonals and bath/reference coefficients; it does not separately correct two individually tolerable error lists.

The fully coherent decoder is valid. Extract commuting syndrome coherently. Unroll K_N=O(N) full passes of O(N) finite local hub visits. Reversibly compute each selected decreasing move into fresh history, uncompute temporary evaluation before changing syndrome, then apply the controlled Pauli and its syndrome XOR. If a whole pass with U>0 made no update, its static syndrome would have an active hub which was visited, a contradiction. Therefore at most K_N passes clear U on the promise. Once U=0, all remaining visits are identity.

The basin source/target argument makes each accepted move canonical-logically neutral. Stored labels and phases depend on syndrome, hence belong to the auxiliary channel. This proves the complete promised-module identity on arbitrary logical/gauge/bath/reference correlations, followed by the known Clifford unencoder and work trace. It does not require a global minimum-weight decoding oracle; the minimum representatives are analytical frame choices only.

There are O(N^2) constant-size visits and history qubits, an O(N^2)-gate sequential Clifford unencoder, and width/depth <=O(N^2). Counting all waiting locations gives **S_D=O(N^4)**. Use this corrected addendum value, not the frozen main note's earlier O(N^3) estimate. Pure-state encoder width O(N) and depth <=O(N^2) give the stated conservative S_E=O(N^3).

## 4. Both SWAPs and the actual bath

WRITE's ideal parallel SWAP moves the redundant payload from staging S to physical memory M and moves the arbitrary old M state to S. It does not move or replace B. During the actual short interval, expand ALL memory Hamiltonian/cooling/Lamb-shift/bath/link errors around that ideal SWAP and actual auxiliary-only CPTP propagators. A partial/suffix SWAP spreads each physical leg to a bounded number of payload cells; the old hardware and B are arbitrary auxiliary coefficients. The low-order common-span argument and positive 2delta repair therefore apply with identity logical action on the incoming payload. No ready or Gibbs state of old M is needed.

READ works in reverse. The payload moves from M to staging S, while B's physical couplings remain attached to the original M cells. After links turn off, B and old M can remain correlated with captured S but have no further interaction with it. Staging complete bounds can include them as mathematical references. Their actual independent CPTP evolution is composed on the reference factor and contracted; it is not claimed that B is physically inert or that its own correlations are preserved.

The same observation permits initial logical/B/computational-gauge correlations: the long staging channels are tensor-separated from actual memory/B evolution, so complete estimates hold on their correlated input. A shared inaccessible memory coupled to staging faults would violate this premise. Tracing B out would not repair such a violation.

The matched N parallel links and fixed payload-incident integrated norm are genuine primitives. Purely auxiliary processor/idling dynamics may be retained in auxiliary-only CPTP propagators; interactions reaching the N payload cells must obey the actual bounded-support/incident budget. The polynomial size of staging cannot be ignored if it physically creates unbounded payload coupling. Slow serial transfer cannot replace the charged parallel SWAP. These requirements are stated in the hybrid contract.

## 5. One explicit compatible port/cooling parameter order

Let u_post^svc and u_pre^svc be the core service's fixed post/pre ceilings, with the physical code/energy constants already fixed. Choose all NEW capture/port margins before temperature/noise strengths:

1. Choose `0<u_dec<min(u_post^svc,u_c/4,delta/(16C_0))`, also `u_dec<h r_0/4` in the Tanner version.
2. Choose a fixed `wbar<min(u_dec/(2D_E),delta/16,r_0/(8c_r))`; omit the r_0 clause in the energy-only version.
3. Choose `u_f<min(u_dec/4,wbar/(4B_link C_0))`, `alpha<wbar/(4B_link q)`, and `rho<wbar/4`.

Then `w_*<3wbar/4`, `D_Ew_*<u_dec`, `w_*+C_0u_dec<delta`, `2w_*<delta`, and the radius margins hold strictly. The WRITE link has no original memory-payload error term: ideal matched SWAP transports each incoming output-interface error to the corresponding memory site without spread. Its admitted endpoint weight is bounded by `rho+B_link q alpha<=w_*`, so its energy is below u_dec and therefore below u_post^svc. This ensures its initial dwell is covered by the core service's stated outer-barrier exponent.

4. Now choose beta sufficiently large and eta sufficiently small that

   `nu_eq <= (s/4) min(u_f,u_pre^svc)`.

   For example allocate the thermal upward source and perturbation source separately below the corresponding fixed fraction of a times this minimum. This is possible under the structural theorem and fixes ONE physical generator for the entire cycle.
5. Choose a final dwell satisfying

   `exp(-a tau_f/s)<=u_f/(4u_post^svc)`.

   Starting from the service post ceiling, the final coefficient is then at most `s u_f/2`; its energy-filter tail is at most `exp(-s u_f N/2+O(1))` and its gentle complete cost at most `2exp(-s u_f N/4+O(1))`. This dwell is charged in T. An existing sufficiently long lower-energy dwell also suffices. A dwell alone CANNOT fix nu_eq>=s u_f; Step 4 is essential.
6. Choose staging p with `cp<1` and `2cp<rho` (or `3cp<rho` if invoking the literal operational Theorem 53). Choose link integrated noise/calibration/fault budgets below the alpha bound, then the parallel link duration/peak strength. Any shared physical p must satisfy all finite positive bounds simultaneously. All choices are independent of N,T,G.

This order makes the frozen existential port inequalities and the core thermal service simultaneously valid. No progressively smaller temperature, fault rate or faster N-dependent pulse is needed. Actual constants may be extremely poor.

## 6. Complete composition and overhead

Carry all retained flag branches, link surrogates, energy filters and killed cooling maps CP/TNI, without normalization or postselection. Their composition has the intended logical action tensor an actual auxiliary CP/TNI map on the promised common module. For arbitrary initial correlations its LR deficit is positive, with trace equal to lost mass. Compare once at the end with the actual trace-preserving process. This proves the claimed error addition without a fictitious bath reset or a factor depending on reference dimension.

The conservative port budget in (P.10) safely covers both FT approximations, positive interface tails, 2delta link repairs and the final gentle filter. The filter's square-root exponent remains. The extra initial/final cooling dwells use the compatible margins in Section 5 and are included in the core HOLD time. There is one WRITE and one READ; no fault-tolerant decoder is inserted after each short HOLD.

With S_E=O(N^3), S_D=O(N^4), fixed r=cp<1 and desired internal error exp(-c_F N),

`l >= [c_F N+log(2(S_E+S_D+N))+O(1)]/|log r| = O(N)`.

The computational scheme's length/gadget/interface sizes are polynomial in l; l is an ACCURACY parameter, not a number of concatenation levels. Hence active locations, peak workspace, protected-port qubits and durations are polynomial in N. All waiting locations count. The cost of quantum/classical routing, noisy idles, resets, actual staging isolation and N parallel matched links remains. There is no constant full-cycle space overhead claim.

## 7. Final scoped conclusion

An arbitrary reference-entangled logical payload PROVIDED IN THE COMPUTATIONAL CODE can be noisily encoded into thermal DATA, loaded through a short same-bath link, protected/processed at the core theorem, captured through another such link, and recovered into the computational code with exponentially small complete error at polynomial port overhead. Initial logical/gauge/B correlations are permitted under the stated isolation and channel premises. Li's literal selected CCZ products retain their zero-complement logical initialization conditions.

The direct CFG lemma deduction avoids Theorem 53's weaker operational metric and any physical inverse of the long computation. The coherent decoder removes the potentially unjustified adaptive-feedback factorization and corrects S_D to O(N^4). The explicit parameter order resolves the final equilibrium-density issue. **No remaining algebraic WRITE/READ gap was found in this hybrid model.**

This does not tolerate arbitrary common-bath coupling throughout the polynomial staging circuits. It does not remove CFG's own ideal-classical primitives, replace encoded ports by accurate bare ports, derive a microscopic thermal bath, provide a universal gate set/3D layout, or establish useful constants or a favorable complete-resource advantage. The mathematical closure and those stronger physical/engineering claims remain distinct.
