# Physical local-channel construction for the actual recursive quantum code

2026-11-01. Constructive derivation from the audited trace/filtered-parent inputs. This is an ideal local-channel statement, not native noisy loading. The physical geometry qualification below is indispensable.

## Result and qualifications

The earned inputs admit a substantially stronger construction than their serial polynomial encoder: two-way conversion between the normalized actual code projector (with onsite product bath reference) and every admitted weakly noncommuting low-temperature Gibbs state, to inverse-polynomial whole-state trace error, by circuits of polylogarithmic **physical causal radius**. This requires polynomial physical ball growth, bounded density of physical checks and bath sites, and the actual forward geometric ancestry bound. A polynomial number of accessible bath sites alone does not establish these geometric conditions.

Use L=C log(N/epsilon), below the logical-distance cutoff. Errors are O(epsilon+eta_n), where eta_n=C n q^L0 is the audited sector-Gram remainder. Unlike the unknown-logical-input encoder, this specified Gibbs-state claim needs neither near-zero logical holonomy nor the square-root logical-twirl bound: the maximally mixed rank-two logical state is invariant under all sector holonomies.

The proof below identifies the missing locality upgrade explicitly. Its strongest precursor is Xun–Cao–Watanabe, https://arxiv.org/html/2610.27939v1, supplementary II.6 and III.3. Those sections already contain the bounded-rate graphical sampler and physical spectral-flow architecture. The additional work here is its actual quantum-code, decoder-trace, and rank-two binding—not invention of that architecture.

## 1. Physical anchoring of an actual small trace

A nonempty isolated valid trace component gamma has w nonzero top syndrome inputs and m marked objects, with w<=m<=Aw. Its isolated replay is a valid syndrome by the full-stencil splitting theorem. The actual decoder alternately contracts syndrome weight by one half; hence there are no nonzero intermediate syndromes after t<=2 ceil(log_2(max(1,w)))+O(1) levels, unless the fixed terminal block is reached sooner. Zero-preserving local gates then give no marked gates farther down. Cancellation gates are already included and add only a constant number of local stages.

The forward geometric ancestry estimate bounds a one-level dependency displacement at level j, viewed in top-level physical units, by C lambda^j. A connected m-object trace therefore has its complete top support and all dependency stencils within distance

    R_tr(m) <= C m lambda^t <= C(1+m)^a,
    a = 1+2 log_2(lambda),

of any one of its top inputs (increase constants/exponent for the finitely many local stages or choose the maximum scale of the dual constructions). The full downward physical correction is not part of activity mass, but each emitted correction's descendants stay within C lambda^t of its trace location. Thus its entire physical support obeys the same polynomial-radius envelope. This argument is about diameter, not merely correction cardinality, and does not regard a host shortcut as a physical edge.

Every nonempty trace has a top input: follow a nonzero input backward through the zero-preserving DAG. Root it at the first such physical input in a fixed ordering. Number of mass-m traces with that root is <=K^m, since the rooted top object belongs to the bounded-degree host. No clocks or quantum gates are placed on the fictitious shortcut edges or high-level host vertices.

Two cutoff-mass traces whose stencils overlap have roots within O(R_tr(L)); otherwise the common stencil location would violate the preceding envelope. All top syndrome bits changed by a birth are in that envelope. A cutoff quantum-potential term has its independently earned polynomial physical envelope R_phi(L), from GRAM_SAMPLER_ENSEMBLE_BRIDGE.md. Consequently every birth, death, compatibility check, and bath heat-bath acceptance decision has physical dependence radius

    r_u = C[R_tr(L)+R_phi(L)] <= C L^p

for fixed p. This is the crucial conversion from abstract-host mixing to physical locality.

## 2. Local decoding without a global decoder oracle

Copy all local stabilizer eigenvalues to nearby classical registers with bounded-color, bounded-depth check measurements; noncommuting bath onsite basis labels are measured locally. To decode cutoff traces, evaluate the actual local hierarchy only to depth t_L=O(log L). Every such gate value is a function of original input bits in a polynomial-radius backward cone, by the same forward scaling bound. For a physical root, explore marked gates and full stencils, stopping after L+1 marked objects; accept only a complete connected trace with all boundary conditions checked, no unexplored active frontier, and zero residual above the retained hierarchy. The maximum explored region has radius poly(L).

The original syndrome copy remains unchanged throughout these tests. A component accepted by this procedure is a complete component of the actual deterministic execution, not a fragment of a large component: full-stencil checks and all local values agree with that execution, and the zero boundary prevents an omitted incident active gate. Every actual component of mass <=L is recognized; its maximum active depth is <=t_L. Apply its matched Pauli correction once at its root. Trace-splitting gives factorization of the matched correction up to irrelevant Pauli phases; CSS order can be fixed globally. Overlapping physical corrections are scheduled in O(r_u^3) colors, or their classical Pauli bits are added locally before application.

On the event that all actual components have mass <=L, the result is exactly the normalized ground-code projector, because each sector initially has maximally mixed logical state. On its complement use predetermined local fallback behavior, with no postselection/global success flag. The tail probability is O(N exp(-cL)) under the positive interacting trace law. Therefore the actual state is decoded within O(epsilon+eta_n).

## 3. Parallel physically local sampler

The accepted contraction gives continuous-time mixing in T=O(log(N/epsilon)). Do not implement its polynomial-size dictionary by serial uniformization: that would not prove a phase channel.

At each physical top-syndrome root generate independent marked Poisson birth proposals for gamma at dominating rate a_gamma=w_gamma exp(2 epsilon_Phi m_gamma). The sum at a root is bounded by sum_m K^m exp(-kappa m), a fixed constant in the admitted low-temperature window. Accept using the actual truncated potential and compatibility rule. A separate rate-one clock removes the polymer currently rooted there, if present; at most one compatible present polymer can have this root. Bath sites have independent rate-one heat-bath clocks. These events realize precisely the audited joint continuous-time chain, with product-initialized random registers.

By the preceding physical envelope bound every event depends on records within radius r_u. Suppose a physical radius-r ball contains at most C(1+r)^D roots (D=3 for bounded-density 3D). A chronological dependency chain of k events obeys

    Pr(any chain of length k) <= C N (C r_u^D T)^k/k!.

This follows by summing starting roots, at most C r_u^D choices for each next root, bounded clock intensity, and the ordered-time simplex T^k/k!. Thus

    k_* = C[r_u^D T+log(N/epsilon)]

makes any longer chain probability O(epsilon). Per-root Poisson record caps are polylogarithmic. Approximate time stamps with O(log(N/epsilon)) bits, choose mesh fine enough that any tie probability is O(epsilon), and approximate all marks/coins with summed error O(epsilon). Tiny time mesh increases precision, NOT the number of circuit rounds.

Use k_* ready-event rounds: within each round use O(r_u^D) neighborhood colors, processing each root's first event whose earlier overlapping dependencies are all completed. This is a fixed circuit of arbitrary local block maps, acting on radius-O(r_u) blocks. The dependency-height bound ensures completion on good records; local fallback on bad records adds only O(epsilon) TV error. Every ancestor dependency is physically covered, so this is a causal-radius proof, not only a distributional coupling argument.

Conservative depth and causal radius are

    depth <= C r_u^D [r_u^D T+log(N/epsilon)],
    causal radius <= C r_u^(2D+1) log(N/epsilon).

For D=3, r_u=O(L^p), this is depth O(L^(6p+1)) and causal radius O(L^(7p+1)). Constants and exponents are not practical resource estimates. Add the sampled small-trace corrections to the input ground state using the local correction construction. Bath reference bits can be reset/sampled onsite; their non-dilute density is harmless.

## 4. Physical controlled spectral flow, including invalid labels

Attach control bits near actual checks, not at abstract hierarchy nodes. Let Q_j(a) be the signed check violation projector (or onsite bath violation). Its controlled version is the local mismatch projector sum_r |r><r|_C tensor Q_j(r). Define, with s in [0,beta],

    F_tilde(s)=sum_j [e^(-sH/2) Q_tilde_j e^(sH/2)]^dagger
                         [e^(-sH/2) Q_tilde_j e^(sH/2)].

It is a direct sum of F_a(s). The physically root-connected expansion gives uniform exponentially local interactions and derivatives in the ORIGINAL physical metric, with constants independent of a. The auxiliary shortcut graph entered only the gap proof. It does not enter this interaction decomposition or the LR bound.

Subtlety: invalid redundant-syndrome control strings need not have the earned gap. There is no need to assert they do. Define the usual fixed quasiadiabatic filter integral D_tilde(s) from the local F_tilde(s), its derivative, and a filter matching the earned valid-sector gap. This defines a local Hermitian generator on the entire Hilbert space whether or not invalid blocks are gapped. It commutes with every control projector. In every VALID block, its restriction equals the standard gapped spectral-flow generator and exactly transports the rank-two ground space. Invalid blocks are arbitrary and never populated. Locality of the integral follows from the uniform physical LR bound and filter decay, without a full direct-sum spectral gap.

Quantitative quasiadiabatic locality admits a conservative tail exp(-c sqrt(r)). For inverse-polynomial global error use r_q=C log²(N/epsilon). The XCW block slicing argument in physical dimension D gives depth O(r_q^D), gate diameter O(r_q log(N r_q^D/epsilon)), causal radius O(r_q^(D+1) log(N r_q^D/epsilon)). In 3D this is O(log^9(N/epsilon)). This is an ideal block-unitary circuit. No exponentially slow adiabatic time remains.

For each valid a this sends P_a/2 to the normalized projector on e^(-beta H/2)ran(P_a), regardless of the rank-two logical holonomy. The exact Gibbs state is

    rho_H = Z^-1 sum_a e^(-beta H/2) P_a e^(-beta H/2).

Near-scalar G_a says the desired weighted normalized-projector mixture differs from this by O(eta_n). No reference-safe logical-input claim is made here; that stronger problem needs transport control separately.

## 5. Both directions and actual costs

Forward: start normalized code projector; run local classical sampler; apply local small-trace corrections and bath labels; copy labels to local control registers; apply controlled physical spectral flow; discard controls/work. Error O(epsilon+eta_n).

Reverse: locally dephase rho_H in the commuting reference checks and bath onsite basis. Its a block is B_a G_a B_a^dagger/Z. Near scalar G_a makes it O(eta_n)-close to p_a P_a/2 in summed trace norm. Run the local small-trace decoder and reset bath onsite. Error O(epsilon+eta_n). Crucially this does NOT try to invert a nonorthogonal filtered-state ensemble.

Composition gives two-way channels between any two Hamiltonians/temperatures inside the uniform admitted open parameter window, and between them and the ground-code projector, with polylog physical causal radius. There is no claim of preparation from product states: the nontrivial ground-code resource is preserved.

The block-map model allows arbitrary maps on polylog-volume blocks. Generic elementary-gate synthesis of a block on O(r^3 polylog N) bits/qubits costs exp(polylog(N/epsilon)), not necessarily polynomial, and nearest-neighbor routing/ancilla layout must be charged. Thus the safe resource claim is constructive finite polylog-causal-radius ideal channels, with a quasipolynomial or exp(polylog) generic elementary compilation upper bound depending on p. The earlier polynomial global encoder remains a separate computational guarantee. Do not combine its gate count with these channels' causal radius without another compilation proof.

## Scope boundaries

This proves the channel mechanism under the cited actual geometry inputs; it does not alone prove stable clustering against all local insertions, establish an unconditional nontrivial-phase invariant, or make native release robust to gate faults. Physical finite-density bath geometry, not merely a polynomial bath cardinality, is necessary for the displayed 3D depth bound. The construction uses ideal reset/random registers and active control, not the storage bath as a cooling oracle.
