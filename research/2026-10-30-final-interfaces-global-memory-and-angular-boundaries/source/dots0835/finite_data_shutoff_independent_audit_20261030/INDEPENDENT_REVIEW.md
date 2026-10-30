# Independent review: actual joint native/program finite DATA shutoff
2026-10-30. Reviewer `producer-workspace/review_simple_compiler`.

## Verdict and frozen target
**SCOPED PASS** for `finite_data_shutoff_20261030/FINITE_DATA_SHUTOFF_SUPPORT_BRIDGE.md`, SHA-256 **917df5835314d93cc8c9a838f36eaae2ba6d3793e68d7e2167f711c5d9d17066**. I read the actual native/reset-first/unified alphabet and the frozen permanent tracker, not only an abstract monotonicity hypothesis. This completes the supplied-decoupled-mode seam for the base-native and fixed finite-group tracker destructive readout, under their existing input/control/noise premises.

The tracker dependency actually read is `reusable_frame_handoff_20261030/REUSABLE_FINITE_GROUP_FRAME.md`, SHA **373db1d1c2b552be096d55ee415a5f428b44a79e8d1c9c1972429267b72b1054**. The readout dependency is root V1 **3223c6df04bb4884b635c7fe54b0c1ef70f53dccf1f1c2b02740c8f55177b9f3**, independently reviewed at `destructive_readout_independent_audit_20261030/INDEPENDENT_REVIEW.md` (SHA b241e391e4bf8b540ddb42dfebdbf891fb7cb194e082fe7d7896f37ffeae55c7). This receipt does not re-certify the whole tracker or invent a detector/classical processor.

I also read the sole final-refreeze diff, which explicitly includes pointer-associated DATA columns in D_Z; it matches §3 below. The earlier bytes and draft receipt are preserved.

The important source-reading issue was caught before this source was frozen: merely holding target v leaves physical program hops DATA-active. The frozen candidate correctly ramps BOTH native C payload edges and held-target program edges. It also correctly counts full b-qubit owner columns rather than reusing an optimistically small forest-prefix support.

## 1. Exact simultaneous readiness algebra
Native coarse readiness is

    P_h=P_A0,h product_(r in R_h)(I-P_o_h,r-P_z_h,r),

identity on workspace/DATA/monitors. With first initiation off, every actual Hamiltonian term commutes every P_h, and every resolved reset preserves P_h when its source is ready. This was proved termwise in the retirement audit and is unchanged by scaling any complete Hermitian C edge. No canceled sum of Hamiltonian commutators is used.

In the BASE physical native frame, only C payload Hamiltonians touch DATA. They act within the relevant owner's declared resource footprint and both endpoints have non-A0 clock. Physical commitment, terminal, abort, new acquisition-abort, ready, refresh, cleanup and monitor resets are DATA identity. The forest's nonmonomial DATA reset instruments are an analytical conjugacy, not additional physical DATA jumps. This distinction is essential to the ramp proof and is correct in the source, including malformed masks.

For the tracker, the permanent onsite G is diagonal in program labels and acts only on program/DATA. It commutes every native P_h. Every native DATA-independent control acts on different factors and commutes G. G-conjugated native C terms can touch all b DATA qubits of a resource column but remain in a fixed full-column owner footprint. They commute every program projector P_v,i=|r_v><r_v|, since the unconjugated native terms act trivially on program and G commutes P_v,i.

The physical held-target program Hamiltonian is a sum of

    Omega[u_v u_g^dagger tensor |e_(g,v)><r_g|+h.c.], g!=v.

Neither endpoint is r_v. Each such term commutes P_v and vanishes on its ready source. Every separate e_(a,b)->r_b reset is physically clock-only because source and target have the same permanent frame b. Its source is not r_v; it may enter r_v but cannot leave it. Native terms preserve all program-ready flags; program terms preserve all native-ready flags. Thus BOTH families of readiness flags are simultaneously noncreating term by term under the declared ramp.

All target values must remain fixed throughout this terminal operation. A changed target or a residual order-one first-initiation drive would invalidate the invariant-source argument; those operations are expressly excluded or charged as small physical perturbations.

## 2. Restricted DATA identity is the needed module property
For arbitrary owner and program sets S,H define

    Q_(S,H)=product_(h not in S)P_h product_(i not in H)P_v,i.

These are auxiliary-label projectors and leave DATA arbitrary. Their source subspace is nominally invariant. Let D(S,H) contain the FULL physical DATA footprints of owners in S and all b DATA qubits in columns H. Choose r_D=max owner footprint after full-column enlargement, so |D(S,H)|<=r_D|S|+b|H|.

On that invariant source every nominal DATA-active Hamiltonian outside S,H vanishes, and every remaining coefficient is DATA identity outside D(S,H). The restricted nominal propagator therefore has tensor identity on those outside DATA factors. Its Stinespring isometry, and each restricted Kraus coefficient, acts trivially there. This holds even if auxiliary dynamics propagates correlations across the system: those correlations cannot activate a nominally ready owner/column.

This is stronger and more useful than a statement about expected active counts. It permits arbitrary coherent masks. Expand an input coefficient by its source label projections. A ket with mask S,H has its own footprint bound; a bra with S',H' has its own. Do not replace the coherent sum by the union of ALL masks, and do not measure or pinch the masks. Correctable-span arguments already compare any two coefficient supports via the usual pairwise distance margin.

## 3. One arbitrary local shared-bath insertion
For a physical insertion support Z, only the owner predicates whose structural supports meet Z and program columns in Z can change. Their count is bounded by fixed body size and native incidence. Every finite system matrix leg of a local joint HP map thus sends Q_(S,H) into Q_(S union A(Z), H union P(Z)), while acting directly on DATA only in its declared local factors. The bath coefficient maps commute all system label projectors; arbitrary bath memory does not enlarge A(Z).

Add the full DATA footprints of these newly possible owners, the affected program columns and directly touched DATA/readout columns to D_Z. Its size is bounded by a fixed q_comb. This is also valid for noise supports whose partners are distant or time dependent; no fixed noise-partner graph is introduced.

**Readout-pointer convention:** the readout pointer is part of the declared grouped DATA/readout site, as in root V1, so touching it counts that associated DATA column in D_Z. If separate pointer sites are used instead, this association must explicitly be included in q_comb. A pointer-bit fault cannot be assigned zero exceptional DATA/bit support merely because it acts on no DATA factor directly.

Induction over r insertions now proves the per-leg support bound: initial canonical-error support, plus its initial active-owner/program footprints, plus the r bounded D_Z sets. Nominal evolution between insertions can shrink readiness defects but cannot cause a support cascade into freshly initiated owners. Expand only finite SYSTEM matrix legs; no positivity of a Dyson term, finite bath dimension, or sum of bath/Kraus coefficient norms is assumed.

## 4. Input alignment and exact support accounting
Use the earned positive retired channel, not an arbitrary low-DATA-weight state accompanied by an unrelated mask tail. Its BASE physical coefficients are F_mem E_s Enc, with wt(E_s)<=alpha_mem N and at most beta_ctrl N nonready owners. On each source mask, F_mem already acts only within D(S,empty). The ramp acts within the SAME union. Consequently

    w_r <= alpha_mem N+r_D beta_ctrl N+q_comb r.

There is no second r_D beta_ctrl charge. If one retained only the weaker unaligned DATA-span contract, this economical count would not follow automatically; the exact joint retirement representation is load-bearing.

For the tracker, on source program labels z write G_z=U_v M_z. Relative to the actual target code U_v Enc, the initial coefficient is

    U_v M_z F_mem E_s U_v^dagger.

M_z is confined to wrong-program columns. Uniform U_v spreads a canonical Pauli by at most sigma_Gamma, while conjugating any operator supported on a union of full b-qubit columns keeps it in those columns. Thus

    w_r <= sigma_Gamma alpha_mem N
                   +r_D beta_ctrl N+b beta_prog N+q_comb r.

No additional sigma_Gamma multiplier is needed on the already full-column footprint terms. Subsequent physical ramp coefficients act in precisely those unions. This derivation keeps the actual target logical operation; no target inverse or logical gate is inserted into the final decoder.

## 5. Finite waveform and signed expansion
Scaling each edge together with its adjoint by a bounded waveform preserves a physical nominal GKLS generator. There is one fixed physical frame, so no time-dependent gauge derivative is missing. Residual committed circuits may stall; this is not called successful recovery. Once both DATA-edge families are zero, all retained native/program dynamics acts on neither DATA nor the newly supplied readout pointers. The product readout nominal split is therefore earned.

Treat this entire order-one finite ramp as NOMINAL. Over combined fixed ramp/turn-on/readout duration L, the total perturbation norm is at most A N eta. The forward Dyson tail beyond r_*=ceil(gamma N) is

    epsilon_D <= exp(A N eta L)[e A eta L/gamma]^(gamma N),

up to rounding. Choose L first and eta sufficiently small. This uses actual CP contractive nominal propagators, not an inverse dissipative interaction picture or a false O(N Delta) approximation by sudden shutoff. Strong nominal ramp amplitudes are controlled by the support module, not counted as small faults. Calibration/leakage/crosstalk and residual initiation are genuinely budgeted perturbations.

The incoming retirement approximation must be propagated through the SAME REAL CPTP ramp/readout channel first, costing epsilon_ret by contraction. Only then truncate the evolution of its positive CP/TNI good input. Applying the signed truncation to the incoming error could amplify it by exp(A N eta L) and is not justified. The frozen source explicitly makes the correct order.

## 6. Composition and limits
At the actual classical readout endpoint filter the rare excessive-wait event only in the proof, using its CP event-probability bound. At low Dyson order, append the at-most-beta_inc N incomplete sites to the per-leg support bound. The independent readout theorem's finite-system-leg instrument reduction and signed normalization apply to this entire coherent span. Choose a strict ordinary coset-correction radius, or the stronger earned X-sector energy/confinement radius for its deterministic queue; merely falling below distance does not establish queue correctness.

For the tracker, the sufficient density is

    sigma_Gamma alpha_mem+r_D beta_ctrl+b beta_prog
                              +q_comb gamma+beta_inc,

with the ordinary pairwise distance margin, and with any separately charged finite-pointer-preparation allowance added if that extension is used. The base model sets sigma_Gamma=1 and beta_prog=0. Choose these output tolerances before the associated retirement dwell/proof parameters; all dimensions, footprints and durations are fixed independently of N. Small eta can meet both the storage threshold and finite-window support tails.

This closes the actual native/program DATA-decoupling seam under a supplied finite control waveform. It does not supply autonomous commands, arbitrary target changes during retirement, indefinite unprotected waiting, a detector or pointer factory unless separately included, classical fault tolerance, non-Clifford computation or a nondestructive output port. Standard destructive CSS readout remains the equally informed conventional comparator. The advance is an exact composition for this continuously corrected apparatus, not a computational advantage claim.
