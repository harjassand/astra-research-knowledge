# An explicit finite local GPT instrument and transactional compiler instance
2026-10-30. Constructive instantiation of the accepted finite-circuit transactional architecture, rather than an assumption that a GPT local decoder has already been compiled. The density theorem is now separately PASS under its actual GPT hypotheses; the integrated Tanner transfer is under independent review.

## 1. Fix the data to be reserved
Let w=Delta^2. Build one hub for each (CSS sector, vertex h in V0 union V1). Its correction masks are all subsets of Q(h), |Q(h)|=w. In this sector let

    V_h={v: Q(v) meets Q(h)},
    R_h=union_{v in V_h} Q(v).

Only potential terms in V_h can change under any candidate. Each data qubit is incident to two potential views, so |V_h|<=2w and |R_h|<=2w^2. Reserve EVERY data resource in R_h, not only Q(h). All data gates below are confined to R_h. The local workspace and clock are private hub resources. A resource's repaired tag alphabet contains free and BOTH labels o_h,z_h for every hub with q in R_h; bounded fixed degree gives an N-independent finite alphabet.

For every v in V_h select once and for all a basis of the local sector check space whose kernel is C_local. Embed these commuting stabilizer checks on Q(v). Keep duplicate checks if convenient. The concatenated measured list H_h has m_h<=2w^2 rows, each of weight <=w. Redundancies create only zero-probability incompatible outcomes. This is a LOCAL finite matrix, not a global syndrome inversion.

The complete physical footprint for transactional exclusion is R_h plus that hub's private workspace and clock and the resource-tag registers consulted by its gates. Conflict adjacency is enlarged accordingly. All relevant degrees remain constants at fixed Delta; the graph need not admit fixed-dimensional Euclidean embedding.

## 2. Explicit syndrome-only rule table
For each local check outcome z_v precompute

    t_v(z_v)=min{|r|: r in F_2^{Q(v)}, H_v r=z_v}.

For nonexistent local outcomes set an arbitrary default. Enumeration has at most 2^w masks per view. This minimization is over a FIXED local view only. It is not a hidden minimum-weight global decoder.

For each globally consistent local record y=(z_v)_{v in V_h}, and every f subset Q(h), compute

    D_y(f)=sum_{v in V_h}[t_v(z_v)-t_v(z_v+H_v f)].

Define f_h(y) as the lexicographically first f with D_y(f)>0; if none exists set f_h(y)=0. Fix the lexicographic order during construction. Define arbitrary f_h(y)=0 on incompatible redundant records. The table is finite, with at most 2^{m_h} inputs and w output bits. Its offline construction by exhaustive enumeration costs at most O(2^{m_h+w} poly(w)) elementary finite operations, in addition to the local distance tables. It depends on local code and incidence labels only, not on the unknown physical error or logical state.

If numerical local code matrices are desired, the existence input can be made a finite offline selection procedure: enumerate all pairs of binary generator matrices at the selected fixed Delta, check ranks, primal/dual distances and the stipulated robustness predicates by exhaustive enumeration, and retain the first pair meeting the proven conditions. The GPT existence theorem guarantees termination at a sufficiently large admissible fixed Delta. This is enormously expensive but independent of N; no efficient local-code search or numerical threshold is claimed. The finite group/complex instance then supplies the actual local incidence labels used to embed the same tables.

This table implements EXACTLY the active-hub rule used by the density theorem: no improving subset is missed. Tests of raw syndrome rather than unary energy alone are used, so the persistence correction in INTEGER_ENERGY_D0_D1.md applies.

## 3. A unitary dilation with a fully specified gate list
Allocate m_h syndrome ancillas Y, w output ancillas A, and O(m_h) clean reversible-computation scratch, all initially zero. For each listed stabilizer S_i, use a standard projective-measurement dilation: prepare its ancilla in |+>, apply ancilla-controlled S_i using one controlled single-qubit Pauli per supported data site, then apply H to the ancilla. For a Z-only or X-only sector this uses only one-/two-qubit Clifford gates after the corresponding basis convention. Since all S_i commute, after all extractions the joint state is

    sum_y Pi_y |psi> tensor |y>_Y,

where Pi_y is the simultaneous LOCAL syndrome projector. There is no intermediate destructive syndrome measurement requirement; this is a unitary circuit on data and workspace.

Implement the reversible truth-table oracle

    |y>_Y |a>_A -> |y>_Y |a XOR f_h(y)>_A.

An explicit synthesis iterates over every y0 and every output bit j with f_h(y0)_j=1, applying a NOT on A_j controlled on Y=y0. Convert zero-controls by X conjugations. Each m_h-control NOT decomposes exactly into O(m_h) Toffoli gates with O(m_h) reusable clean scratch (small m_h handled directly). Each Toffoli has a fixed exact one-/two-qubit universal decomposition. Undo scratch within each controlled gate. This costs O(w m_h 2^{m_h}) gates; no asymptotic computational assumption enters.

Finally for each q in Q(h) apply the sector correction Pauli on q controlled by its A bit. Leave Y and A in the workspace. Let the resulting full unitary circuit be V_h=U_L...U_1. Its gate count obeys the explicit conservative bound

    L_h=O(m_h(w+2)+w m_h 2^{m_h}+w),
    n_workspace=O(m_h+w)=O(w^2),
    dimension(workspace)=2^{O(w^2)}.

Tracing/resetting the entire workspace yields

    Phi_h(rho)=sum_y P_{f_h(y)} Pi_y rho Pi_y P_{f_h(y)}^dagger.

This is the intended full syndrome-evaluation GPT instrument, including genuine dephasing between distinct measured outcomes. Do NOT uncompute Y after correcting the data and silently replace this instrument by a coherent feedback unitary. Tracing Y and A also works on arbitrary data/reference/bath-entangled inputs. Incompatible y have Pi_y=0.

## 4. Insert this gate list into the finite transactional path
Use the reviewed acquire/commit/computation/abort/cleanup architecture with its existing all-owned guards, irreversible reset-before-release, and separate terminal workspace reset channels. Set its private computation path to C_0,...,C_{L_h}; edge t carries the concrete U_t above, with a positive fixed hopping rate. Acquisition visits all resources in R_h in the chosen fixed order. Gates are guarded by the actual resource ownership tags. Once committed, while in computation C or attached computation-origin abort phases, do not release any tag before complete terminal or abort workspace reset. Acquisition A backtracking/unacquire remains allowed exactly as in the inherited architecture; this instruction does not remove its acquisition reversals or alter the liveness generator.

Use exactly the resolved terminal instrument

    sqrt(kappa_T)|Q_0,0><C_{L_h},s|,  for EACH workspace basis s,

with equal rates and sum over s in the physical channel. The clean finite-path gauge then yields scalar clock density times Phi_h, exactly as in CLEAN_TRANSACTION_INSTRUMENT.md. The proof applies to arbitrary finite unitary payloads, not specifically FGL acceptance tests. Distinct sector hubs also lock their entire footprints, so overlapping opposite-sector computations cannot invalidate snapshot-based decisions.

Every path length, workspace dimension, owner alphabet, interaction arity, and conflict degree is now an explicitly finite function of Delta and the selected local code, independent of N. The size can be exponentially bad in Delta^4 (and constants obtained from the general density theorem are also very poor). Nothing here is a claim of practical local hardware size. The precise native grouping below, rather than a distributed workspace convention, supports the two-site-Hamiltonian/onsite-reset statement.

### Native site grouping: no distributed-clock variant in the native claim
For the native instance, combine the ENTIRE clock (including acquisition/abort/cleanup phases), ALL syndrome/output/scratch workspace, and the inherited private monitor factors into ONE finite-dimensional hub qudit. Combine each data payload qubit, its repaired free/o_h/z_h resource tag, and any inherited private resource monitor into ONE resource qudit. There are O(N) such sites. Use no one-hot spatial clock and no spatially distributed workspace in this native corollary.

If d_C is the finite number of clock/phase states and d_M the inherited private monitor dimension, then

    d_hub <= d_C 2^{O(w^2)} d_M,
    d_resource <=2(32w+1)d_M,resource.

Here d_C includes L_h+1 computation positions and the explicit finite acquisition/abort/cleanup paths of the reviewed architecture. All dimensions are enormous but fixed independently of N. Any onsite Markov-cushion bound must use these ACTUAL d_i, including tags and workspace, rather than payload dimension two.

Every workspace-only reversible gate is now a hub-ONSITE payload clock edge. Each data-touching extraction/correction gate is between that hub and ONE resource: the clock transition, private ancilla control and local hub computation all live at the hub, while the payload Pauli and actual ownership guard live at the resource. Thus it is a TWO-SITE Hamiltonian term. The usual exact Toffoli decomposition used for the table acts only inside the hub qudit. Acquisition/abort/cleanup Hamiltonian edges are the same hub/resource two-site edges of the inherited repaired controller. The complete workspace commit/terminal resets are hub-ONSITE instruments, and inherited onsite resource/private-monitor resets remain onsite under this grouping. No new conditional two-site dissipator is added by the GPT circuit.

The native interaction graph has hub/resource edges for q in R_h, with hub degree <=2w^2 and resource degree <=16w before the fixed inherited monitor connections. This is bounded-degree graph locality, not Euclidean nearest-neighbor geometry. Hamiltonian norms and all reset rates are fixed finite numbers per site/edge. The primitive-noise rate and incidence assumptions in the next section are applied to these grouped physical sites.

## 5. Noise geometry, positive record constants, and initialization
Apply the existing forest-frame construction to THESE U_t prefixes. A dressed physical primitive support D_X is enlarged by the finitely many intersecting frame factors; a marked emission support is the full associated dressed owner patch, including R_h, not merely Q(h). Form the bounded-degree DATA graph using cliques on every such D_X and emission patch as well as full raw-read and check supports.

The reviewed reset/liveness estimates hold for arbitrary fixed finite gate lists because their clean gauges remove all U_t and leave finite scalar clock paths. With the newly specified L_h and exclusion neighborhoods they produce new fixed positive good-service and regeneration constants. One must choose the physical window duration T AFTER those constants, making the miss parameter small, then choose the primitive kick-rate threshold small. The numbers can deteriorate drastically but do not scale with N. Positive fault-count estimates use the new dressed patch incidence constants, and their Hölder composition requires no independent noisy scheduler assumption.

Initialize all hubs in A_0, all private workspace zero, all resource tags free, and all marks zero, with exact encoded data tensor a fixed logical-input-independent bath. The physical forest frame is identity on this initialization. Mathematical readout applies the corresponding final inverse frame followed by sectorwise ideal GPT recovery. Unfinished transaction prefixes are NOT ignored in a bare-data output.

### Explicit conservative incidence budgets
There are at most four geometric hubs whose Q(h) contains a fixed qubit. For ONE sector, q in R_h implies a path q--v--r--h with v one of two potential views of q and r in Q(v), so at most 8w hubs contain q in R_h. Including both sectors gives

    b_read <=16w,   r_read <=2w^2,
    b_conf <=1+b_read r_read <=1+32w^3.

Thus a full-read clique DATA graph has maximum degree at most 32w^3 before adding the fixed physical noise geometry. Each resource lock requires at most 32w+1 labels: free and o_h,z_h for each of at most 16w incident owners. Duplicating clock/workspace registers per hub does not alter these DATA bounds.

Let f_size denote the number of elementary physical sites in one forest factor, counting its private clock/workspace registers and its <=r_read resource tags; the explicit circuit above fixes f_size (use the native grouping below, for which f_size<=1+r_read apart from a fixed inherited monitor-site factor). Let b_frame bound the number of frame factors containing a physical site. With private hub registers and one tag per data resource, b_frame<=1+16w is a safe bound. Because the forest factors commute, conjugating a primitive supported on s physical sites involves at most b_frame s factors, not an uncontrolled recursive closure. Hence

    |D_X| <= s[1+b_frame r_read]

is a safe dressed DATA-support bound. A marked owner operation involves only its local physical footprint; using its original footprint size s_owner<=f_size plus finite monitor/reset registers gives |D_h|<=s_owner[1+b_frame r_read]. Sharper geometry for a terminal whose original support is only its private registers is optional; no proof needs it.

Assume the native noise model has at most z primitive supports incident to any elementary physical site (and support size <=s). For a DATA site q, the set of physical sites capable of dressing into q lies within q plus the at most b_read frame factors whose DATA patch contains q. Its size is at most 1+b_read f_size. Therefore

    nu_k <= z(1+b_read f_size)

bounds primitive support types whose dressed D_X meets q. Likewise, if b_owner bounds original marked-owner footprints incident to a physical site, then

    nu_e <= b_owner(1+b_read f_size)

bounds marked-owner types whose dressed patch meets q. The specified private-register/read-tag layout has finite b_owner, conservatively bounded by 1+b_read times a fixed register multiplicity. These bounds yield |E(W)|<=nu_e|W| and mean primitive counts <=epsilon nu_k tau|W| in the reviewed fault-mass formulas. Repeated events retain their full multiplicity. They also supply finite support-clique graph degree after dressing. Noise primitive supports must obey the stipulated bounded physical-range/bounded-incidence layout; small cardinality alone is not enough.

### Ideal GPT terminal recovery in the native Poisson theorem: one D0-only suffix
The native Poisson proof's fixed minimum-syndrome terminal decoder can be replaced by an ideal complete syndrome snapshot, a fixed-order classical GPT scan using the tables above, and one final Pauli mask. A scan accepts the first strictly decreasing move, updates the stored syndrome exactly, and repeats; terminate after a full scan has no accepted move. The original syndrome snapshot determines all later simulated checks, so no repeated quantum measurements or extra dephasing within one measured sector are introduced. At most U<=2N moves are accepted; naive repeated full scans use O(N^2) local tests with the fixed huge lookup costs already charged.

For the proof, append this ENTIRE noiseless scan computation as ONE formal terminal block, with Q=0 and no real duration. Apply only unconditional D0 to that suffix, not window contraction D1. If every enlarged suffix execution component is <ell, virtual reduced input/output gauges are stabilizer-equivalent to actual errors componentwise. At a terminal no-change scan with U>0, some small component has positive U; apply AD to its stabilizer-reduced representative and syndrome invariance to infer an actual improving hub, contradicting no-change. Thus final U=0, the minimum-syndrome endpoint is empty, and the actual endpoint differs from it only by stabilizers. Logical recovery is correct.

If recovery fails, the suffix has a cutoff-bad root component K. D0 with Q=0 gives |E_in intersect K|>=|K|/C_seed; use the weaker reviewed 1/(2C_seed) bound to start the usual backward chain through EARLIER REAL memory blocks. There is no fresh event to pay for in the noiseless suffix, and it requires no service or fault tail. The chain cannot terminate there and must find its fresh certificate in the real history, unless the exactly clean initial state already makes K impossible. The suffix adds one root layer, not O(N) fake physical-time windows, and the same terminal-volume/animal argument bounds it. This preserves the C N(1+t)exp(-cN) scaling.

The proof applies to every compatible Pauli coefficient history under a common safe physical-record event. Therefore the terminal GPT instrument corrects the full linear span, including retained-bath coherence, without importing a residual local-stochastic distribution. This remains a MATHEMATICAL ideal recovery map: ongoing noisy quantum storage during classical O(N^2) latency, reliable classical processing, physical F-inverse execution and operational quantum retrieval are not free.

## 6. Resulting scope
With the accepted density input, the explicit Phi_h above supplies the missing semantic premise of the coefficientwise compiler interface. INTEGER_ENERGY_D0_D1.md supplies the deterministic witness contract, and the reviewed actual-record fault/miss estimates supply its positive common envelope. Thus the finite-circuit Poisson-CPTP compiler theorem has a genuine GPT instance with ell=Theta(N), k=Theta(N), and decoded error bounded by C N(1+t)exp(-cN), below a fixed sufficiently small rate threshold.

This instantiation concerns the compiler's bounded-range local Poisson arbitrary-CPTP kicks (with retained bath) and its separately justified onsite Markov cushion when included in the primitive records. It is not a conversion of arbitrary continuous coherent Hamiltonian perturbations into Poisson faults. The ideal atomic continuous-coherent result uses UNARY_ENERGY_LIFT.md instead; its finite-duration coherent controller lift remains a distinct task.

The onsite Markov-cushion corollary has a DIFFERENT noise scope: finite system-local Hermiticity-preserving trace-annihilating generator deviations, buffered by actual full-site depolarization with the complete grouped-site dimension d_i. It does not cover arbitrary uncontrolled system–bath Hamiltonian couplings. Its clean reset/kick records may be the records of an alternative positive CP analysis unraveling of the same generator, not the original physical detector clicks. No external feedback is applied to those mathematical records. Retained common-bath memory belongs to the arbitrary-Poisson-CPTP-kick theorem and must not be imported across this distinction.

No global error-distribution premise, global minimum-weight lookup in the LOCAL controller, free twirl, fault-free physical readout, or fault-tolerant initial encoder has been introduced. The fixed-degree family has bounded graph locality, not an uncharged spatial routing implementation.
