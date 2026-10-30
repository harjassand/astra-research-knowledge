# Finite DATA-coupling shutoff after physical retirement
2026-10-30. Governing candidate for the actual native-to-destructive-readout mode transition. Earlier accepted memory, reusable-frame and retirement sources are unchanged. This closes a different interface from the supplied-decoupled-mode readout theorem; acceptance requires its own substantive review.

## 0. Result and exact remaining premises
Keep first native initiation OFF. Over an actual fixed finite interval Delta>0, scale every remaining native DATA payload Hamiltonian edge and its adjoint together to zero. All physical native resets/monitors are DATA identity. Coarse native readiness is not created negatively by any retained nominal operation. Consequently, from an initial nonready owner set S, ALL nominal DATA action during the ramp stays inside the fixed union of those owners' DATA footprints. A local perturbation can activate only boundedly many new owners. A forward Dyson term of order r therefore has DATA coefficients supported on the initial canonical-error support, the initial nonready footprints, and at most q_ramp r additional DATA qubits. This remains true for coherent malformed masks, arbitrary workspace, and a retained common bath.

For the permanent finite-group tracker, PROGRAM hops are also physical DATA Hamiltonians. They must be ramped off at the same time while holding a fixed target. Their target-ready subspace is absorbing, so the same support proof charges initially wrong program columns plus only local noise activations. Holding the target without stopping these hops is NOT a decoupled DATA mode.

After the ramp, every retained native/program control acts on neither DATA nor newly added readout pointers. The nominal readout can then be exactly the product of the separately supplied local DATA-pointer instruments and auxiliary dynamics. A combined ramp+readout forward expansion supplies the common exceptional-set interface needed by the root readout theorem, without treating the order-one ramp as a small extensive perturbation.

This is not a new detector primitive, pointer initialization theorem, classical processor, microscopic reservoir construction, autonomous command delivery, noisy quantum decoder or computational advantage. Those resources retain their stated scope.

## 1. Exact inputs, physical frames, and positive retired input
Use the physical generator fixed by the accepted native manuscript and unified interface:
- `native_continuous_bridge_20261030/NATIVE_CONTINUOUS_BRIDGE_MANUSCRIPT_V1.md`, SHA256 `f43ee100de24657ad0152d60725efec29e82153e45111fdb875d9eef99a2bcf1`;
- `weak_initiation_compiler_20261030/UNIFIED_GENERATOR_INTERFACE.md`, SHA256 `c083a0d491e7eb44ee0e575d222ba256152c56a682cadedd08d7785c6032105f`.

Use actual controlled retirement at:
- `physical_retirement_root_20261030/ABSORBING_READINESS_EXTRACTION_V1.md`, SHA256 `ad6a74dc81767f6be367f4ba122d57c5eaf599cce1c1efeb6e3cb2e195321dce`;
- completing whole receipt `physical_retirement_independent_audit_20261030/INDEPENDENT_REVIEW.md`, SHA256 `9e4cad517661c09e8e3a86a5d14a08906e71f8786619bd137557758f21be555e`.

The termwise coarse-readiness proof is `halted_native_alphabet_audit_20261030/ACTUAL_HALTED_ALPHABET_AND_READINESS.md`, SHA256 `a8fe85faed29cbfc7bacfd57401d664e2a279ef405a2156bff7b0cc525ac6c37`.

At the beginning of the ramp the actual input channel is within epsilon_ret(N,T_storage) of a positive trace-nonincreasing common-canonical-span channel. In its proof representation, source canonical Pauli representatives E_s have wt(E_s)<=alpha_mem N, and its native label sectors have at most beta_ctrl N coarse-nonready owners. This is the accepted killed-plus-small-readiness projection, NOT a physical mask measurement or a newly assumed arbitrary warm input. Coherences between DIFFERENT masks are retained. For the tracker additionally retain a positive source with at most beta_prog N non-target-ready program columns; its discarded mass is already priced by the accepted joint program tail/gentle comparison.

In ordinary storage the physical retired coefficients have form F E_s Enc, where F is the original native forest. For the tracker they have form G_z F E_s Enc. Neither F^{-1} nor a target forest inverse is executed at the ramp or readout.

## 2. Exhaustive PHYSICAL DATA-touching term classification
This section is in the actual physical native frame, NOT the forest frame. Forest conjugation moves DATA action into reset gains; that analytical representation must NOT be mistaken for a physical DATA-active reset.

### Base native apparatus
The ONLY nominal Hamiltonians acting nontrivially on DATA are C payload edges

    g_(h,t) [U_(h,t) tensor |C_t><C_(t-1)|
                    tensor P_(o_h on actual target resource) + h.c.].

Hub-only workspace gates are included in this list but may have empty DATA support. Every U acts on the private workspace and at most its one declared resource DATA factor. Every such source AND target is a C phase, hence B_h=I-P_h is one, where

    P_h=P_A0,h product_(r in R_h)(I-P_o_h,r-P_z_h,r).

This holds for malformed masks and arbitrary workspace. The resource ownership guard can disable an edge but cannot cause it to act outside h's fixed R_h.

Every other nominal native Hamiltonian is DATA identity: acquisition/reversal, consistency-abort drives, Q verification, lock cleanup, and actual clock/lock monitor drives. Every physical commitment, terminal, abort, new Ai abort, ready and A/Q workspace-refresh reset acts only on hub clock/workspace; lock-cleanup resets act only on locks; monitor resets act only on labels/monitor. There is no hidden DATA-dependent physical reset. All complete workspace channels remain separately resolved.

With first initiation OFF, every Hamiltonian term commutes EVERY P_h, and every resolved reset maps a ready owner only to ready. Scaling C edges therefore preserves these properties TERM BY TERM; no cancellation among different payload terms is required. Scaling an edge means scaling the Hermitian edge-plus-adjoint, not deleting one direction of a Hamiltonian.

### Permanent tracker
Use the accepted fixed G from `reusable_frame_handoff_20261030/REUSABLE_FINITE_GROUP_FRAME.md`, SHA256 `373db1d1c2b552be096d55ee415a5f428b44a79e8d1c9c1972429267b72b1054`. G acts only on colocated DATA/program registers and commutes every native P_h. G-conjugated C terms remain on the same hub/column sites, but may touch all fixed b DATA factors of a column. Native DATA-independent controls commute G and remain DATA independent.

For a held absolute target v the PHYSICAL program edge is

    Omega[u_v u_g^dagger |e_(g,v)><r_g| + h.c.],  g!=v.

Both endpoints are outside P_v=|r_v><r_v|. It commutes P_v, vanishes on P_v, and acts only on that column's b DATA factors. Every separate e_(a,b)->r_b reset is clock-only, and cannot take r_v outward. Thus scaling these program edges to zero preserves target readiness and confines their DATA action to non-target-ready columns. No command change is allowed during this terminal ramp; a new target would change the readiness condition and invalidate this confinement.

## 3. Actual finite control waveform and earned decoupled mode
For each payload edge choose a bounded piecewise-continuous scalar f_(h,t)(u) in [0,1], u in [0,Delta], with f(0)=1 and f(Delta)=0. Multiply its entire Hermitian term by f. Keep first-initiation coefficients identically zero throughout. The endpoints need not be reached at identical intermediate times, but by Delta ALL relevant DATA terms must be zero nominally. For the tracker choose analogous bounded f_prog,i,g(u) ending at zero for every currently held-target program edge.

All previously declared DATA-independent native/program resets and controls may remain on. Removing C edges may stall residual committed circuits; this is harmless here because their DATA coupling has been removed rather than falsely treated as a completed correction. One does not reset/erase a committed workspace during the ramp. We no longer claim continued QEC service after shutoff.

At u=Delta the nominal generator acts as identity on DATA. Add/enable the declared local readout-pointer instruments only after this decoupling. Native/program terms act on neither DATA nor the new readout pointers. A finite bounded turn-on waveform for the LOCAL detector rates can also be included; it creates no intersite DATA support, and its duration is charged. The root readout proof may then use a final constant-rate detection window for its unfinished-pointer estimate.

The ramp is a prescribed local control operation, not an instantaneous perfect unitary or free mode change. There is no time-dependent gauge and therefore no omitted gauge-derivative Hamiltonian. Uniformly bounded calibration/leakage/crosstalk deviations, including residual first initiation or residual payload coupling after Delta, belong to the SAME physical bounded-body joint-cb perturbation budget. They need not obey readiness. The declared nominal and actual scheduled joint generators must have normal CPTP propagators on every interval; bounded perturbations admit the forward variation-of-constants expansion. Common bath correlations are retained. Wrong macroscopic mode commands or order-one unbudgeted residual couplings are excluded, not corrected by this proof.

## 4. DATA-support module lemma, retaining coherent masks
Let S be ANY owner set, and define the auxiliary projection

    Q_S=product_(h not in S) P_h.

In the tracker additionally let H be ANY program-column set and

    Q_(S,H)=Q_S product_(i not in H) P_v,i.

These projectors restrict only auxiliary physical labels and leave DATA arbitrary. Let D(S,H) be the union of the FULL physical DATA footprints of owners in S and all b DATA qubits in program columns H. Set H empty in the base model. If r_D bounds one full owner footprint, |D(S,H)|<=r_D |S|+b|H|. r_D covers BOTH native forest factors and every ramped payload term; for the tracker use full b-qubit resource columns. This may enlarge a previously optimized forest-only constant, and that enlargement must be paid in the output-radius choice.

**Nominal module lemma.** Every nominal ramp propagator leaves the Q_(S,H) source subspace invariant. Restricted to this source, each Stinespring/Kraus coefficient acts as DATA identity outside D(S,H), with arbitrary action on DATA inside D and all auxiliary systems.

Proof: readiness is termwise noncreating, so no nominal Hamiltonian/jump can make an owner outside S or program column outside H active. On this invariant source, all DATA-active Hamiltonians outside S/H vanish. Every remaining generator coefficient acts trivially on DATA outside D. The nominal auxiliary/bath propagators are also DATA identity. The restricted evolution therefore has the tensor identity on those DATA factors. Equivalently its Stinespring isometry restricted to Q_(S,H) factors as identity there, and ANY Kraus representation has the same restricted factorization (identity channel has one-dimensional Kraus span). Finite products/limits of nominal segments retain this support module. This proof is about operators on the full Hilbert space, not a probability distribution over classical masks.

In a coherent input sum over masks S,S', apply the lemma separately to the left and right source coefficients. Each coefficient has its OWN size bound; do not replace the coherent sum by a single union over all possible masks (which could be extensive), and do not pinch/measure masks. A left coefficient of support <=w and a right coefficient of support <=w are in the same error-correctable span even if their union has size 2w; the ordinary distance/common-span condition already pays that pairwise factor.

### One arbitrary local perturbation insertion
For a perturbation supported on a bounded set Z of PHYSICAL sites and the retained bath, define

    A(Z)={h: support(P_h) meets Z},
    P(Z)={program columns in Z},
    D_Z={DATA qubits in Z} union union_(h in A(Z)) full DATA footprint(h)
                         union all DATA in P(Z).

Readout pointers are included in their associated grouped DATA/readout column sites, as in the root readout model. Thus a pointer-only insertion STILL counts the associated DATA column in D_Z: a pointer relabeling is a possible physical bit error, not zero DATA/bit support. If a separate detector-site convention is used, include its fixed associated DATA column explicitly in D_Z and in q_ramp.

Bounded physical body size and bounded native incidence imply |D_Z|<=q_ramp for a fixed constant, even if Z's partner sites are far apart or time dependent. Bath action does not enlarge A(Z): bath is a separate retained factor and is not a physical owner/column.

A system operator supported in Z commutes P_h and P_v,i outside A(Z),P(Z). It can therefore map Q_(S,H) only into Q_(S union A(Z), H union P(Z)), while acting on DATA directly only in Z. This is true for every system coefficient of a local normal HP map. Expand only its FINITE SYSTEM legs into matrix units with arbitrary bounded normal bath maps as coefficients. No finite bath dimension, Pauli stochasticity, CP property of a signed term, or bound on a SUM of Kraus norms is assumed.

After r insertions, every left/right coefficient has DATA support contained in its original canonical-error support plus D(S,H) plus union_(j=1)^r D_(Z_j). Each later nominal segment acts only within the enlarged active set. Auxiliary correlations may propagate beyond these footprints, but they cannot turn a ready owner nonready nominally, so they do not create a DATA-support cascade.

## 5. Actual retirement-to-ramp coefficient accounting
For base storage the input F E_s coefficient is supported on supp(E_s) union D(S,empty), so after r insertions its weight is at most

    alpha_mem N+r_D beta_ctrl N+q_ramp r.          (5.1)

There is no extra r_D beta_ctrl charge for running the ramp: the initial forest and all subsequent payload action lie in the SAME union of owner footprints. If r_F in an earlier theorem was smaller than r_D, choose beta_ctrl using r_D rather than silently keeping the old radius.

For the fixed-group tracker, on a program label z write G_z=U_v M_z. Relative to the actual target code U_v Enc, the initial error coefficient is

    U_v M_z F E_s U_v^dagger.

Conjugation by U_v enlarges a local factor only within its fixed column. Let sigma_Gamma bound the Pauli spread of U_v. Initial forest/program deviations lie in D(S,H), and the canonical error contributes at most sigma_Gamma alpha_mem N. Thus the uniform physical ramp bound is

    w_r <= sigma_Gamma alpha_mem N
                    +r_D beta_ctrl N+b beta_prog N+q_ramp r.          (5.2)

This safe physical-footprint convention also covers nonmonomial owner workspace action and every DATA-Pauli coefficient. No target frame inverse is required. The target must be held fixed until program H is off; afterward clock-only resets may continue and cannot modify DATA.

## 6. Forward Dyson norm tail: the strong ramp is nominal, not a fault
Let L0(u) be the actual declared ramp generator followed by the decoupled product-readout generator. Let N(u)=sum_Z N_Z(u) be the bounded local physical perturbation. Let the total ramp plus detector turn-on/hold duration be L, a fixed finite constant independent of N. If the number of physical sites is <=C_sys N and per-site incident joint cb sum is <=eta, then

    ||N(u)||diamond<=Lambda_N<=C_sys N eta.

Use the actual forward nominal CP propagators between insertions. For order cutoff r_*=ceil(gamma N), the norm of the discarded Dyson tail is bounded by

    epsilon_Dyson <= exp(Lambda_N L)
                       [e Lambda_N L/r_*]^(r_*).                   (6.1)

This follows from the simplex volumes and CPTP contraction, with no inverse dissipative propagator. Choose finite Delta and detector dwell first, then eta small enough that (6.1) is exp(-cN). Nominal C amplitudes can remain order one during the ramp; they do not appear in Lambda_N because Section4 controls their DATA action structurally. Uniform control waveform/calibration errors do appear in eta. This is not a global-diamond O(N Delta) approximation to sudden shutoff.

Centering individual HP perturbation adjoints to annihilate I, when needed for the pointer subset hierarchy, preserves their sum/support and costs at most factor2 in local cb norms. The total actual generator remains physical; the individual Dyson terms/truncation need not be CP. All estimates are uniform with an arbitrary reference and common retained bath.

## 7. Composition with destructive readout, not an invented positive truncation
The readout component is the root's actual local DATA-pointer instrument with auxiliary evolution acting on NEITHER DATA NOR pointers. Nominal pointer initialization/calibration and the eventual classical pointer read and processing retain their separately declared premises. At the actual classical endpoint, omit the rare event of more than beta_inc N unfinished pointers only in the proof, using its positive output-event bound delta_inc. No intermediate physical mask or syndrome projection is inserted.

Fix a low-order ramp+readout Dyson term and one permitted unfinished-pointer set. Outside the union of its initial DATA-error support, D(S,H), the D_Z insertion footprints and incomplete-pointer sites, the ramp is DATA identity and the readout is the EXACT local ideal Z instrument. These untouched local instruments commute through all remaining insertions and auxiliary/bath maps because the latter act on neither their DATA nor their pointers. Initial correlations do not obstruct this map identity. The term has an exceptional-set instrument of size at most

    w_r + beta_inc N,   r<r_*.

For base storage use (5.1); for the tracker use (5.2). Choose the constants with a strict radius margin, for example

    2[ sigma_Gamma alpha_mem+r_D beta_ctrl+b beta_prog
                                      +q_ramp gamma+beta_inc ] < delta_read,       (7.1)

where delta_read N is the relevant reviewed CSS distance/sector-decoder radius and the base model sets sigma_Gamma=1,beta_prog=0. For an efficient current-syndrome X-sector classical queue, use its smaller proved energy/confinement radius instead of mere distance.

The root common-span destructive-readout algebra then applies to EVERY left/right coefficient, including coherent masks and bath coefficients. The signed truncated+filtered map has logical classical-block form sum_l c_l |l><l| tensor <l|rho|l>. It is NOT declared positive. Compare instead with the actual CPTP implemented output A. Its distance from this signed map is at most the actual retirement input error, the positive incomplete-output event loss, and epsilon_Dyson. Actual CPTP normalization then forces |c_l-1| below the same bound and yields the root factor-two logical-instrument estimate. No Kraus-count factor or logical-dimension factor is introduced.

Crucially, compare the REAL ramp/readout channel on the actual retired input with the SAME REAL CPTP channel on the positive good retired input first. This costs epsilon_ret by contraction. Do NOT propagate epsilon_ret through the signed truncation, whose norm could be exp(C N eta L). Only then truncate the good-input evolution, whose initial CP/TNI map has norm<=1.

This section supplies the physical mode-change input to a separately reviewed readout theorem; it does not independently certify the detector/common-span/normalization/classical-processing theorem without those inputs.

## 8. Price, comparator, and excluded claims
Paid physical resources are a finite known waveform for every existing C edge, first initiation held off, and—when used—finite shutoff of every current-target program edge. Native/control resets remain the actual separately resolved maintained resources. Controller DATA interactions may stall but cannot spread beyond the charged active footprints; afterward DATA no longer receives nominal correction. Residual couplings/calibration errors are local perturbations, not assumed absent physically. Detection must start within the fixed charged mode interval; arbitrarily long unprotected waiting is not supplied.

An equally informed scheduled ordinary implementation has the same option to stop gates, wait for/retire controls, and perform standard destructive CSS measurement. The contribution here is an exact bounded-locality finite-mode-transition proof for THIS native continually corrected device; it is neither a new CSS decoder nor a computational advantage. No instantaneous perfect switching, global environmental reconstruction, autonomous command selection, non-Clifford resource, nondestructive output port, noiseless classical processor or microscopic reset-reservoir theorem is inferred.
