# Encoded quantum ports close the restricted hybrid thermal service

Machinery researcher, 7 November 2026. This is a constructive applicability check against the full primary text of Christandl--Fawzi--Goswami (CFG), arXiv:2408.05260v3, not an import from its abstract. It supplements the consolidated [thermal service theorem](../principal/THERMAL_SERVICE_THEOREM.md). Earlier frozen reports remain unchanged.

The linked [primary import audit](../machinery/CFG_PORTS_IMPORT_AUDIT.md) records exact source locations, the source hash and the distinction between imported and derived claims.

**Verdict: CLOSED at the explicit hybrid primitives below.** Polynomial active staging can WRITE an arbitrary reference-entangled logical input supplied in a computational code, transfer it into the thermal DATA memory with an exponentially small complete error and a supported warm subchannel, and READ the processed logical state back into that computational code with an exponentially small complete error. The same actual perturbation bath stays on the memory hardware throughout. No new preparation threshold for a common microscopic bath is used.

There is one precision correction to the requested theorem citation. CFG Theorem 53 concludes the operational communication criterion of Definitions 47--48, equation (147). It does not state a decoded-channel diamond theorem on arbitrary computational gauge/bath correlations. The needed stronger statement follows directly from its underlying **Lemma 40 and Lemmas 41--42**, with the one-sided interfaces in the proof of Theorems 50/53. Theorem 43 packages the same ingredients with bare interfaces on both ends. We give that direct deduction below. The memory service itself is not assumed local stochastic or Markovian after tracing its retained perturbation bath.

## 1. The hybrid contract and what is being paid for

Let C_N be the accepted binary stabilizer DATA code, including any fixed product memory ancillas in the two-sector construction. It encodes m_N=Theta(N) logical qubits, has distance at least delta N, and has the actual local integer energy U and common canonical frame of the consolidated theorem. The Tanner version retains both energy and radius promises. The stable-duality version may use its separately proved global low-energy repair.

The memory has exactly the consolidated physical evolution: its engineered local thermal GKLS reservoir, Hamiltonian, diagonal Lamb shift, and the actual joint perturbation bath B. In particular, B is neither traced out nor reset between service intervals or gates. Its arbitrarily correlated auxiliary states and the declared normality/physicality assumptions are retained.

There is a separate active staging processor with these additional primitives:

1. Its gates, preparation, measurement, classical controls and idle locations satisfy CFG Section 2.5's independent circuit stochastic model, with parameter p. Every noisy quantum location is (1-p) times its ideal channel plus p times an arbitrary channel on that location. The fault channels and their random flags have no shared inaccessible memory with B. Purely classical computation is noiseless, as in CFG; any alternative protected classical implementation must separately be supplied and charged.
2. During the long active encoder and decoder circuits, staging has no coupling to B or to memory. B may continue evolving with the original memory hardware. A system correlated with staging can be included in the external reference in the complete circuit bounds.
3. There are N parallel, matched memory/staging links implementing a bounded-depth SWAP. During those short link intervals the actual memory Hamiltonian, thermal cooling and B couplings remain ON. All their strengths, the stochastic or other permitted local link faults, and the idle hardware enter the finite-pulse disturbance budget. The links turn off afterward; B stays with the original memory cells.
4. Input and output logical ports are already in the CFG computational code K_l. All port blocks, active workspace, ancillas, resets, quantum/classical locations, routing and link hardware are charged. No accurate unknown bare-qubit encoding or final release is assumed.

This is a strictly narrower architecture than allowing the same arbitrary B to couple throughout a polynomial-time loading circuit. It is a valid hybrid physical model, but isolation of staging is an actual physical resource. The extra stochastic/noiseless-classical assumptions must be displayed in any capability statement.

The ideal code encoder E_N and a promised recovery/unencoder D_N are specified as ordinary finite circuits. Their sizes, including waiting locations, are denoted S_E and S_D. Given the stabilizer matrices, the fixed logical basis, and the finite local energy tables, both are polynomial in N. No search for the input state occurs.

## 2. The exact CFG imports

Primary source: [Fault-tolerant quantum input/output, v3](https://arxiv.org/html/2408.05260v3), 2 December 2025. Cached HTML:

    ../machinery/sources/arxiv-2408.05260v3.html
    SHA256 83f1b792aa4eaecf71ae6d8354716152d2e1fbd8ebb188e7c3cee5a45cf6b830

Use Definition 22's computational scheme, with constant c>1, p<1/c, computational-code length n_l=poly(l), polynomial gadget/interface size, and r=cp<1. The explicit concatenated construction is Appendix C.3, Lemmas 70--71; its recursion parameter has exponent 2^s and is reindexed by the accuracy parameter l. Do not identify l with the number of concatenation levels.

Write J_l for the physical embedding and V_l for the code/logical-gauge identification, with gauge F_l. The parts used are:

| Source | Exact mathematical content used |
| --- | --- |
| Lemma 40, (128) | Encoded realization of a circuit Phi differs from J_l V_l (Phi tensor F) V_l^dagger by at most 2 size(Phi) r^l in diamond norm, on the entire input computational module. |
| Lemma 41, (129)--(131) | A physical-qubit-to-K_l interface is within 2r^l of a code-supported channel; that channel has a positive good/bad mixture, bad probability at most cp; the good channel decodes exactly to the identity. |
| Lemma 42, (132) | On the entire computational module the physical output interface is exactly a positive mixture: good map id tensor Tr_F, bad probability at most 2cp. |
| Theorem 43, (133)--(135) | The two bare interfaces plus the encoded circuit give 4 size(Phi) r^l error, size size(Phi) poly(l), and explicitly retained auxiliary channels. |
| Theorem 53, Definition 52, (166) | Robustness to arbitrary physical local-stochastic channels of parameter 3cp at both channel ports gives encoded fault-tolerant communication, in Definition 48's operational metric. |

The two short prose introductions to Corollaries 44--45 swap the words input/output. Their hypotheses n'=0 and n=0, equations (136) and (138), and proofs are unambiguous. We use the equations, not those prose descriptions.

The literal sufficient accuracy choice for Theorem 53 is

    4 (S_E + S_D + 2 l_test(m,zeta)) r^l <= zeta/2.       (P.1)

Here l_test is the paper's preparation/measurement test-circuit size, NOT the computational accuracy parameter l. Its omission would misstate the theorem. Even if l_test is exponential in m, it enters logarithmically in the required l. For standard finite m-qubit preparation/measurement synthesis, log l_test=poly(m,log(1/zeta)); m=O(N) and zeta=exp(-c_0 N) therefore still permit polynomial l and polynomial port circuits. The direct deduction below avoids this test-circuit quantity entirely and proves the complete decoded-channel statement.

## 3. A useful complete sparse-interface lemma

The interfaces have more structure than a reduced-system estimate. For the good part of the input interface, equation (131) says that the logical marginal is exactly the identity channel. Consequently, after applying V_l^dagger, this good extension is

    X -> X tensor tau

for one fixed gauge state tau. One proof is that the identity channel has a rank-one Choi matrix; every extension of that matrix factors from its rank-one support. This statement holds with arbitrary external reference.

For N independently realized interfaces, expand the positive good/bad mixtures over the bad set A. The bad flag probabilities are products of scalars; arbitrary input entanglement, including with B, does not change them. The A branch acts nontrivially on physical sites A and auxiliary systems, and acts as identity on the complementary payload sites. The same conclusion holds for output interfaces, where the good channel simply traces that site's gauge. Output gauges may be arbitrarily correlated with one another or the input computational gauge.

Thus we can use a slightly stronger, auxiliary-retaining version of physical local-stochastic noise. If V_A are the positive support branches and p_0=2cp, then for every T subset [N],

    || sum_(A containing T) V_A ||_diamond <= p_0^|T|.    (P.2)

The norm includes every auxiliary and an arbitrary inert reference. No auxiliary is replaced by a new product state. Any branch with |A|<=rho N has payload error operators in the span of rho N-supported Paulis, with arbitrary auxiliary operator coefficients.

For any fixed rho>p_0 the complete norm of the discarded support branches obeys

    delta_LS <= exp[-N D_Ber(rho || p_0)+O(1)],          (P.3)

where D_Ber(x||y)=x log(x/y)+(1-x)log((1-x)/(1-y)).

For completeness, positivity and (P.2) give the moment inequality

    || sum_A exp(theta |A|) V_A ||_diamond
       <= [1+p_0(exp(theta)-1)]^N.

Expand exp(theta|A|) as the sum over T subset A and use (P.2). Markov's bound followed by optimization in theta proves (P.3). This also proves the support-tail assertion for a general CFG local-stochastic decomposition rather than independent flags.

If U vanishes on the ideal code and changing one site affects energy by at most D_E, then the output mixture obeys

    Tr exp(sU) rho_output
       <= [1+p_0(exp(s D_E)-1)]^N.                     (P.4)

The same estimate holds for subnormalized inputs and as a complete input bound. Equations (P.3)--(P.4) are physical support/moment certificates; a small decoded reduced-channel error alone would not give them.

## 4. The polynomial promised decoder is robust on the common span

Choose fixed positive cutoffs and fractions sufficiently small that

    u_dec < u_c,
    u_dec/h < r_0/4                  [Tanner version],
    w_* + C_0 u_dec < delta,
    2 w_* < delta,
    c_r w_* < r_0/2                 [Tanner version].   (P.5)

Here C_0>=max(1,1/h) is the canonical correction constant, r_0 is the original safe radius, and w_* bounds the **combined** physical representative before staging recovery. In the energy-only specialization use its earned global correction constant C_0 and omit the radius clauses.

A final low-energy filter of the memory proof restricts U<=u_f N for some strict u_f<u_dec. This filter is a proof subchannel, not an uncharged physical measurement. Its tail is bounded by the service's exponential moment. The memory's pre-capture state may have arbitrary coherent canonical syndrome errors and arbitrary correlations with B, its logical input and the external reference.

After a capture with at most alpha N bounded-support pulse insertions and an input-interface branch of size at most rho N, the error operators have representatives of weight at most

    w_* N = (B_link C_0 u_f + B_link q alpha + rho) N,   (P.6)

and energy support at most D_E w_* N. All constants are the actual link's support/spread constants, with harmless enlargement if needed. Choose u_f, alpha and rho so that D_E w_*<u_dec and (P.5) holds. Since all inequalities are strict and the original code has positive distance and basin margins, such fixed constants exist. Then choose p so that 2cp<rho. This choice is independent of N, T and gate count.

D_N measures the actual commuting check syndrome, finds a decreasing local U move by a scan, applies it, updates the syndrome and repeats. There are O(N) local hubs, every table is fixed size, U=O(N) is integer, and a move lowers it by at least one. At most O(N) moves and O(N^2) table evaluations suffice. Cap the computation after the uniform O(N) move bound and define any fixed output outside its promise. Finish with a Clifford unencoder for C_N. This defines a genuine CPTP map on all physical inputs.

The greedy path stays inside its promised region. In the Tanner case, if a path could first leave the radius bound, its preceding state has r<=U/h<=u_dec N/h<r_0N/4, and one bounded-support move cannot reach the radius boundary for large N. Its energy never increases. The energy-only version needs only decreasing U. Every move along this path is canonically neutral.

Most importantly, D_N corrects the **entire common error span** in (P.6), not just a stochastic Pauli list. For any such physical representative E and the canonical correction E_sigma at its final syndrome,

    wt(E_sigma^dagger E) <= (C_0 u_dec+w_*)N < d_N.

This zero-syndrome Pauli is a stabilizer up to scalar. By linearity the same conclusion holds for arbitrary operators in that span with arbitrary bath/reference coefficients. Measuring and discarding syndrome affects gauge information but preserves the logical/reference marginal. Equivalently, the restricted decoder is id_L tensor an auxiliary trace/channel on the full correctable module. Separate correction of “memory errors” and “gateway errors” would not be enough; (P.6) verifies joint correction.

A conservative explicit ordinary-circuit size bound is O(N^3), including all waiting qubits while bounded-fan-in noiseless classical scans run and while a sequential O(N^2)-gate Clifford encoder/unencoder executes. Faster scheduling is unnecessary. The local tables and stabilizer matrices must actually be available; Gaussian elimination and circuit synthesis are polynomial in their supplied descriptions. Any acquisition or nonuniform advice cost belongs to the code-construction accounting, not to an unknown input oracle.

## 5. WRITE with encoded input

The sender holds an arbitrary logical state in K_l^tensor m, possibly entangled with an inert reference and correlated with the computational gauge. Use the encoded realization of E_N and then N physical output interfaces; there is **no bare input interface**.

Lemma 40 and Lemma 42 give, uniformly on the whole computational module,

    epsilon_W,FT <= 2 S_E r^l.                          (P.7)

Up to this error, the physical output is the ideal DATA encoding with the complete sparse output noise of Section 3. It therefore has the CP supported subchannel (P.3) and moment certificate (P.4). This is unknown-state encoding, not known-state preparation.

Perform the short parallel SWAP into the original memory. The old memory state, including any correlations with B, is simply transferred into staging and treated as auxiliary. The ideal SWAP is not a bath replacement. Keep its Hamiltonian, cooling, B and link errors in the integrated pulse budget.

The finite-pulse proof of the consolidated theorem applies between the new staging payload's common code module and the memory's canonical module. Every low-order term has bounded payload support after the actual partial/suffix SWAP; arbitrary old-memory/B coefficients are auxiliary operators. Therefore every retained low-order term has the identity action on the new logical payload. The same positive CP/TNI repair as service Section 9 applies: take the logical partial trace of Q Gamma(I_L/d tensor .)Q. This keeps the same physical auxiliary systems and costs twice the high-order tail, with no bath substitution or dimension factor.

For actual integrated disturbance at most mu_link N and

    mu_link <= alpha/(8e),

the service's signed Dyson tail gives, conservatively,

    delta_link <= 2 exp[-alpha N log 8+O(1)].            (P.8)

The supported writer subchannel thus starts with U<=u_dec N, correct logical input, and only exponentially small losses. A constant initial cooling dwell brings its moment to the service pre-gate threshold, if required. The initial dwell and its boundary error are charged. Long staging preparation time does not expose the new payload to B: the only such exposure during loading is the declared short SWAP.

## 6. READ with the same actual B

At the end of the service, apply its positive final low-energy proof filter and perform the capture SWAP into fresh staging payload cells. The same (P.8) bound and low-order module argument apply. B remains coupled to the original memory hardware; it may remain correlated with the captured state. Neither measurement nor access to B is needed.

Turn the links off. The captured block is now processed by N physical-to-K_l interfaces and then the encoded realization of the promised circuit D_N. There is **no bare output interface**. Lemma 41's interface approximation and Lemma 40 give

    epsilon_R,FT <= 2 (N+S_D) r^l.                      (P.9)

The positive input-interface support branches are exactly the additional faults already included in (P.6). On the good support branches D_N corrects them jointly with the entire captured memory error span. Its output is the desired m-qubit logical state in K_l^tensor m, up to its arbitrary actual computational gauge.

Bath correlations do not invalidate this step. In (P.9), B, the old memory hardware, any auxiliary staging systems and the external reference are reference systems for the staging circuit. The complete inequality holds after tensoring their identity channel. Their actual independent evolution can be composed on that reference and contracted in norm. The assumption required is that they have no further coupling to staging; merely tracing B out and declaring staging independent would be insufficient.

For an infinite normal bath, the finite-input complete inequalities extend by finite-rank approximation of trace-class states and normal continuity. This does not relax the actual joint generator's domain/normality/physicality premises during the SWAPs.

The final many-to-one computational decoder is used to DEFINE the logical error, as in any fault-tolerant encoded-port statement. It is not an uncharged physical final bare-qubit release. Continued fault-tolerant computation or communication consumes the protected output.

## 7. Full capability bound and polynomial cost

Let E_service(N,T,G) denote the core HOLD and repeated gate/cooling terms of the consolidated theorem, for the actual admitted warm CP subchannel, with G compatible finite gate bursts and HOLD time T. Its writer-deficit terms are accounted for in E_ports below. Include the charged initial/final cooling dwells in T. Let delta_f be the complete norm cost of the final low-energy proof filter needed in (P.6). If its positive tail mass is at most exp[-(s u_f-nu_tail)N+O(1)], gentle compression gives delta_f<=2 exp[-(s u_f-nu_tail)N/2+O(1)]. The square-root loss must be retained. Its exponent is positive whenever nu_tail<s u_f; add one charged constant cooling dwell if necessary.

A conservative complete port contribution is

    E_ports <= 2(S_E+S_D+N) r^l
               +4 delta_LS +4 delta_link +2 delta_f.    (P.10)

Factors have been enlarged to cover the CP/TNI deficit and restoration at each comparison; no optimized constant is claimed. Actual hardware need not implement the proof filters. The total encoded logical/reference error is at most

    epsilon_input_port + E_service(N,T,G) + E_ports.     (P.11)

Here epsilon_input_port describes any imperfect ALREADY-ENCODED incoming port. In particular, arbitrary logical inputs including maximally entangled ones are covered by setting this term to zero for an exact computational input module; arbitrary input/gauge/reference correlations are allowed. The target is the supplied compatible logical operation sequence, not necessarily the identity.

For a desired internal circuit error exp(-c_F N), it suffices to choose

    l >= [c_F N+log(2(S_E+S_D+N))+O(1)]/|log(cp)|.       (P.12)

Thus l=O(N) for the polynomial ordinary encoder/decoder just constructed. If P(l) bounds the fixed scheme's gadget/interface size and block length, the charged port resources satisfy

    active locations <= (S_E+S_D+2N) P(l),
    encoded-port qubits <= m P(l),
    peak active workspace <= poly(N),
    duration <= poly(N) in fixed-duration circuit units,
    parallel memory/staging links = N.

All idle locations are noisy and counted. Sequential routing can also be polynomial if that is the supplied architecture, but then its extra locations and faults must be compiled. The SHORT constant-depth capture/release used here specifically requires matched parallel links; an uncharged slow serial SWAP cannot be substituted. There is no constant full-cycle space-overhead claim: the thermal DATA has constant rate but the paid computational ports/staging can be polynomially larger.

Memory cooling and B remain active while staging works. Accordingly the full-cycle count of thermal interaction opportunities includes O[N(T+tau_E+tau_D)] in addition to the actual gate/dwell/link scheduling, where tau_E and tau_D are the paid staging durations. This counts opportunities, not net heat. It does not enter the new payload's memory lifetime before WRITE or after capture because that payload is isolated in staging then. Peak link control strength must be sufficient for (P.8), with its fixed ratios to J, cooling and noise included in the physical hardware contract.

The port error remains exp(-c_port N) for a positive fixed c_port, while T and G have the exponential ranges allowed by E_service. The service's same-bath induction is unchanged; there is one WRITE and one READ, rather than a new fault-tolerant gateway after every short HOLD interval.

## 8. Exactly when Theorem 53 itself applies

For a fixed initial auxiliary/bath resource independent of the logical input, treat the entire SWAP-in, memory evolution, compatible pulse sequence and SWAP-out as one physical CPTP channel Lambda_N. Do not factor it into reduced memory channels. Sections 3--6 show that E_N and D_N are robust to arbitrary local-stochastic physical noise at the two staging boundaries, with parameter 3cp after shrinking p so that 3cp<rho and using p_0=3cp in (P.3)--(P.4). This is Definition 52's premise for the storage/identity instance. Theorem 53 then supplies its (m,2 zeta,p) communication conclusion, with accuracy choice (P.1).

There are two reasons to retain the direct proof for the stronger statement:

* If the input is correlated with the actual initial B, an input-only Lambda_N with a fixed product environment need not exist. The full-module proof still applies statewise and uniformly with an inert external reference; Theorem 53's bare communication-channel formulation does not itself express this situation.
* A long processed output has a specified logical target U rather than identity. Physically appending U^dagger merely to fit Definition 46 could make READ as long as the entire computation. The one-sided encoded-circuit proof above compares directly with U and keeps D_N polynomial.

Theorem 53 is therefore sufficient existing machinery for the fixed storage-channel encoded-port application. The mathematically stronger processing-and-retained-auxiliary version is the explicit deduction above from the lemmas used in its proof, together with the independently proved common-module thermal service. No unproved common-bath encoder threshold is hidden in this deduction.

## 9. Sharp obstacle tests and remaining scope

**Bare ports.** If one insists on m unknown bare inputs and a permitted dephasing fault before redundancy, the half-diamond floor is at least 1-(1-p)^m. A final unknown bare output has the corresponding release floor. For m=Theta(N) and fixed p, this does not vanish. No increase of l removes the first/last bare interface. Already-encoded ports genuinely change the endpoint contract; the theorem must say so.

**No staging isolation.** Coupling the arbitrary retained B throughout the polynomial circuit is outside CFG Section 2.5. A small instantaneous per-site joint cb norm does not turn into independent circuit stochastic faults. Multiplying the whole polynomial loading duration into a support expansion can destroy the linear error budget. This report does not solve that stronger problem.

**No common-span margin.** An input-interface estimate on the ideal code alone is insufficient. If a capture reaches the distance boundary, separately correctable memory and port errors can jointly be logical. Inequalities (P.5)--(P.6), including the final low-energy filter and its charged tail, are essential.

**No silent bath reset.** Using the marginal memory channel afresh between gates, replacing B by a new product state, or treating a correlated capture as a product input would invalidate the retained-bath claim. This construction does none of them.

**Noise/model limits.** Staging uses a standard independent stochastic active threshold, noiseless classical control in the cited theorem, actual resets/measurements, and the supplied routing/gate model. The memory uses an engineered local Markov thermal reservoir plus a separately retained weak actual bath. This is neither a derivation of the thermal reservoir from one finite exact Hamiltonian bath nor a generic physically local common-bath preparation threshold.

**Capability limits.** Supplied compatible Tanner CNOT layers, or the separately audited GJ/Li non-Clifford operations with their exact logical input restrictions, are covered. A universal gate set, elementary-qubit bounded-density 3D layout, a useful numerical temperature/fault threshold, and favorable full-cost comparison with an active quantum computer are not proved. Existing CFG quantum-I/O, thermal qLDPC memories, measurement-free QEC, and autonomous computing remain substantive predecessors.

**Final status.** PROVED as a constructive mathematical hybrid-model closure at the consolidated service's accepted DATA/reservoir/physicality premises and the additional explicit stochastic staging/isolation/parallel-link primitives. The remaining gaps concern stronger physical models, endpoint bare-qubit accuracy, numerical practicality and comparative advantage; they are not an algebraic WRITE/READ gap in this stated hybrid model.
