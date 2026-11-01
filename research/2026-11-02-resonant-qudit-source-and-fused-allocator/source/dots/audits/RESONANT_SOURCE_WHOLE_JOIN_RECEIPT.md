# Independent whole-join receipt: resonant source inside autonomous protection

2026-11-01. **Qualified mathematical PASS at the explicitly specified finite-dimensional GKSL model level.** No practical threshold, atomic implementation, noisy terminal readout, or whole-controller two-body realization is certified.

Audited frozen root `RESONANT_MICROSCOPIC_SOURCE_MEMORY_JOIN.md`, SHA256 `fb3a92a6d7703f7343ae87b3799d35e4ae8d318ea31dff101fdda68c5c89e83a`. Governing independent admissions are `EXPLICIT_QUDIT_SOURCE_RECEIPT.md`, `FINITE_PATCH_CORRECTOR_RECEIPT.md`, the prior Tanner/flag-frame instance receipts, noncommuting exponential criterion, and killed-subchannel receipt. The source cache note now uses corrected z=(Delta+1)r tau+p, SHA256 `9680b4cc948b9211919079c25fb644013524a6265b797085902724a6e1ebfb74`.

## 1. What is actually joined

The quantum data checks are unchanged by witness-frame flag updates. Each measured check gets one physical source qudit of dimension 8w+6. Source Hamiltonians couple that qudit to one data qubit; source jumps are onsite on the qudit. All physical levels are legitimate apparatus states, with arbitrary initial source coherences covered by the independently audited observable-algebra argument. The remaining classical verifier is the existing finite noisy fanin-two DAG with up to three-site jumps. Flag actuation touches a flag and permission register.

Uniform stage observability, arbitrary-state cache refresh, and activity service are imported only from the explicit supplied source proof, not independent progress clocks. The positive correctors use actual truncated source terms and full-source locality residuals. No assertion that a finite patch itself refreshes is made. No new abort/lock mechanism is imported.

## 2. Exact mean coupling, including all cache writes

He and HA are functions/operators of quantum data and source qudits ONLY. They are identity on physical witness registers, correction flags, and Boolean output wires. Their source semigroups preserve the full joint cache-block-diagonal algebra.

A Boolean repair jump uses cache/witness/flag diagonal input projectors and acts on separate wires; hence it commutes with He, HA and their adjoints. A flag actuation jump acts on flag plus permission wire, so is disjoint from their support. Consequently every ideal classical repair and actuation dissipator annihilates each source corrector exactly. This verifies the stronger interface that cache diagonality alone, without the disjoint-register condition, would not establish.

The source preserves every dressed physical check and leaves witness/flag variables fixed. Thus it annihilates W. It changes E only through final cache overwrite. Summing the readout hazards gives gamma Pi_final, and each overwrite raises E by at most B_s. The operator inequality

 L_src(epsilon E)<=epsilon sum_s B_s gamma A_s

holds even on coherent probe states: E is diagonal in cache and wire labels, and the final readout instrument has total effect gamma Pi_final<=gamma A_s. It counts ALL writes, not just erroneous writes or mismatch occupation.

Adding epsilon B_s gamma HA_s cancels this term by the actual full-source corrector inequality. The remaining source floor is epsilon B_s gamma qA_s. He_s supplies -alpha_s e_s+alpha_s qE_s. The existing pointwise flag/verifier inequalities then give

 L_ideal V<=-(a c0/2)W-a E-a sum_s e_s+b_src n,
 b_src/a<=C_s(C_alpha qE+B C_gamma qA).

The algebraic reason the same R_i/R_s rates suffice is unchanged: loss of a correct flag decrease and gain of a wrong flag increase have total coefficient 1+D_W, because the epsilon B_act contributions cancel. Correct moves retain at least half their W decrease. Fast repair at the displayed gamma_i pays its own downstream consistency debt and leaves -a E. All these are inequalities on commuting check/cache/classical labels, hence extend to coherent register states.

## 3. Finite parameter hierarchy and strict margin

First choose fixed source g,gamma, overlap bounds and preparation impurity/pump r to make actual refresh and activity floors small. The source proof makes both arbitrarily small at finite intensive times. Choose finite patch radii for the remaining locality floors. This fixes TE,TA, corrector supports/norms/incidences and all hardware dimensions, independent of n. Then choose a>0 sufficiently small.

With qE,qA<=beta c0/(64 C_b), c=a c0/2,

 b_src/c<=beta/32.

The ACTUAL perturbation requirement uV/a<=beta c0/64 gives uV/c<=beta/32. The positive potential density z=a K_T<=beta/32. Therefore

 L V<=-c V+c f0 n,
 f0=(b_src+uV)/c+z<=3beta/32.

Choose exponential parameter k>0 within the actual finite local nested-commutator convergence radius and with the full quadratic remainder C2 k/c<=beta/8. The resulting effective floor satisfies f<=7beta/32. Splitting at theta=beta/2 gives theta-f>=9beta/32 and

 1+theta/(theta-f)<=1+16/9=25/9<3.

Initial encoded W=0 states satisfy V<=z n on that subspace, even with arbitrary logical/apparatus correlations, because [V,W]=0 and 0<=Z<=z n. Thus their initial exponential moment is bounded by exp(k z n)<=exp(k theta n). The displayed moment prefactor3 is safe.

This selection establishes a nonempty fixed intensive noise neighborhood, not robustness at a prespecified laboratory error rate. It is not trajectory postselection: uV is an admission on the actual noise generator after rates and support constants are fixed. Slowing a does not preserve tolerance to a fixed nonzero W-noise injection. Relative errors in strong source/classical operations must be converted into their actual generator perturbation, including jump cross terms.

## 4. Protected factorization and comparison

The ordered controlled-prefix frame is finite-depth with finite support expansion for fixed check weight/degree and finite source dimension. Although its controls need not be Clifford, conjugating a local actual operator leaves bounded expanded support. Its conjugation of each complete stabilizer gives the stated dressed stabilizer: overlaps contribute apparatus-only controlled phases that commute with the data stabilizer. Combine this frame with the already audited flag Clifford frame.

He and HA commute with every dressed data check and every witness/flag label entering the old component. E is diagonal in those labels and cache/wires. Hence [P,V]=[W,V]=0; positivity gives V>=W. This is stronger than scalar W conservation and is what the exponential/killed argument needs.

Expand EVERY conjugated actual H, J and full J†J in old-system bounded-support Paulis with arbitrary apparatus coefficients. Enlarge the old admitted alphabet accordingly. The prior minimum-representative/radius/distance argument then gives protected logical identity on the old good component, for sufficiently large n. This includes non-Clifford frame expansion and the full J†J loss term; it does not assume the new source/wire Hilbert space is a fresh stabilizer code. Actual expanded support determines b_W and the two-step boundary shell.

Using the killed CP subchannel, rather than an unjustified reflected CPTP transfer, inherits the exponential Foster inequality. The boundary population has exponent -(beta-theta)kn+2k b_W. The actual-minus-killed trace estimate counts all cut-crossing ideal and noise terms, not just external perturbations. The trace-loss/logical comparison costs the additional factor2. Thus the claimed bound follows:

 error <=2 sqrt(3) n(2h_all+3Gamma_all) T_storage
                  exp(k b_W) exp(-k beta n/4).

Commuting bath-only terms may be omitted because their comparison and weighted action vanish; unbounded noncommuting environment terms cannot be hidden in that omission. Arbitrary coherent gauge/apparatus states are allowed only in the specified encoded W=0 subsystem. Arbitrary hot unencoded attachment is not covered.

## 5. Cost and boundary of this acceptance

Exact correctors are analytic certificates, not a runtime controller. Their support sizes can grow exponentially in the finite radius, with dense Hilbert-space and coefficient costs correspondingly enormous. The independently supplied finite-computation construction requires encoded local coefficients and certified numerical errors; an approximate certificate must price positivity/residual errors and preserve required commutation. The exact integral theorem does not claim that those matrices were numerically constructed.

The actual fixed local constants for the exponential bound and for noise action must include the enlarged patch supports and incidence, all qudit levels, classical wires/flags, and source rate multiplicities. The original normalization n is the original code-size parameter, not an assertion that the total apparatus count remains n or5n. Fixed-family overhead is absorbed explicitly into these intensive constants.

Terminal recovery remains ideal frame undo followed by the imported Tanner decoder. No native noisy encoding or terminal measurement theorem is inferred. Numerical two-check collision/price data are not used as a proof of uniform-network service or memory lifetime and were not rerun for this receipt.

The accepted mechanism replaces an engineered multisite quantum-sensing jump with resonant two-body source Hamiltonians plus specified onsite coherent-preserving reservoirs, while keeping the prior three-site Boolean controller and substantial resource costs. Selective multilevel/reservoir realization, geometry, practical advantage, and the pending alternative locking construction are outside this receipt. No further formal strengthening is needed to close this frozen mathematical audit.
