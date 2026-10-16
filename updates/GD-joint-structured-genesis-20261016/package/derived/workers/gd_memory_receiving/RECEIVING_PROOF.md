# Reconstruction of the universal completed-pair receiving proof

16 October 2026. Independent analytic reconstruction from the preserved source packet at the pin recorded in `SOURCE_MANIFEST.json`. This is a receiving investigation, not an integration update. No canonical source or pinned checkout was changed.

## 1. Three generators must remain distinct

On the periodic cubical four-torus there are `6L^4` plaquette qubits and six encoded qubits. In one CSS sector a pair corrector at `v` tests two commuting outgoing edge stabilizers `S_(v,i),S_(v,j)` and writes their positive plaquette Pauli `Q`. Set `Pi=(I-S_i)(I-S_j)/4`. The write anticommutes with both tested checks.

1. **Original active pair:** `kappa sum D[Q Pi]`, with `12L^4` active correction dissipators across both sectors. Its supplied theorem has continual independent single-face Pauli noise. The syndrome-dependent virtual base/extra clock construction applies to that classical Pauli law.
2. **Completed pair:** `kappa sum (C-Id)`, where `C(rho)=Q Pi rho Pi Q^dagger+(I-Pi)rho(I-Pi)`. It has `12L^4` physical channel streams and `24L^4` Kraus dissipators, each on an 11-qubit patch. It is the receiver for arbitrary rare bounded-patch CPTP fault proposals and structured compilers.
3. **Completed whole-vertex/depolarized regularization:** the earlier seven-pattern sweep uses up to 24-qubit correction support, its aggregated inactive completion, and real full-patch depolarizing floors. It has different support, clock and floor resources. Its generic diamond-ball radius does not become an 11-qubit implementation by substituting a pair theorem title.

For a single pair, the difference between completed and active generators is `kappa D[I-Pi]`. It vanishes on a definite-syndrome Pauli density operator; on cross-predicate coherence it supplies additional dephasing. Equality on Pauli trajectories does not imply equality on arbitrary coherent inputs. This investigation uses generator 2 only for the general receiving theorem.

## 2. Required simultaneous event

Fix a complete physical correction-clock and fault-location schedule through finite time `T`. The good event must depend only on this schedule and the declared fault boundary boxes. On that event, **every** sequence of local Paulis at those fault locations, including null Paulis, and every nonzero ideal correction Kraus record, must have trivial decoded accumulated homology under the same decoder.

A coupling that selects a virtual base pair from each branch's current syndrome is insufficient for this quantifier. Two coherent Pauli terms can choose different virtual pairs on the same physical clock schedule. The physical six-label ticket construction is the load-bearing replacement.

## 3. Ticket process and local monotonicity

Use a separate copy for each CSS sector. Its alphabet is `0` and `(r,S)`, where `r=1,2` and `S` is a nonempty subset of the six direction-pair labels `Omega`. The maximum is `(2,Omega)`. There are 127 states per site. Order first by phase number and then by mask inclusion within a phase; `0` is below all positive states.

At a matching sector pair clock at `w`, read all old states. A positive center with a positive predecessor `w-e_i` resets to maximum; otherwise its arriving label is deleted from its mask. Finishing a phase moves phase two to `(1,Omega)` and phase one to zero. A zero center remains zero. For every direction pair `{i,j}`, if `w,w+e_i,w+e_j` are old positive sites, reset both sides and `w+e_i+e_j` to maximum. The downstream resets are conservative and do not depend on the actual arriving label or actual syndrome. A fault resets both sector copies on their complete declared boxes.

Tick monotonicity follows by cases: deletion preserves mask inclusion; a smaller mask finishing a phase only lowers it; a phase-two state finishing becomes the maximum phase-one state. The predecessor and three-source predicates are increasing, and their resets go to the maximum. A downstream target either persists or is raised to maximum. All output decisions use old states, so one event cannot trigger an instantaneous cascade. Every old-input displacement has infinity norm at most one and `l_1` norm at most two.

Opposite-sector correction clocks neither tick nor reset a copy. Those operations commute with that sector's stabilizers. Spending a coupon on an opposite-sector clock would create a false service certificate; the source packet records a finite counterexample to that altered rule.

## 4. Universal syndrome-support domination

Induct over the finite event list, simultaneously for all Pauli histories. A local fault is covered by its universal reset box. At a legal pair action centered at `w`, its two checked outgoing edges are occupied. Hence `w` and both side vertices are incident syndrome vertices and, inductively, have positive tickets. The three-source predicate resets the sides and far corner, covering every changed noncentral incident vertex.

For a center `v`, partition time into epochs between complete resets to maximum. In one epoch, every actual incoming edge is constant and the actual outgoing set can only decrease through `v`'s own pair corrections. A fault changing an incident edge resets `v`. Any noncentral correction changing an incident edge has `v` as a side or far corner; the preceding three-source argument resets it, even if that change removes an edge. Thus such a change cannot occur inside an epoch.

At a progress tick all envelope predecessors are zero, so actual incoming edges are absent. Their epochwise constancy implies absence throughout that epoch. Since a syndrome is a cycle, the outgoing set is even. A complete coupon phase visits every direction pair; if a nonempty even outgoing set never changed during the phase, one visited pair contained in that set would have acted. Thus a completed phase removes at least two edges unless already empty. Two phases clear all at most four outgoing edges, and the final progress tick has no incoming edges. A cleared ticket never omits actual support.

A transient positive envelope predecessor between progress ticks causes no problem: if it reflects a real incident-edge change, the full center mask has already reset; if it does not, no actual edge was added. No assumption of permanently zero predecessors throughout a phase was used.

All ticket updates depend only on physical clocks, their pair labels and fault locations. The same process therefore dominates every Pauli summand in a fault Kraus expansion, not merely a sampled branch.

## 5. Independent service certificates

The healthy coordinate halfspaces `x_i>=a` are invariant: a reset crossing one would require the relevant side already positive in that halfspace. Healthy lower-height halfspaces `h(x)=sum_i x_i<=a` are invariant because births from correction maps are downstream.

In a finite directed-height region with a healthy lower boundary and no fault births, define certificate times recursively. Let `T_v` be the maximum predecessor certificate completion time, then let `D_v` be the duration of two fresh full coupon collections at `v` after `T_v`, and set `U_v=T_v+D_v`. Predecessors are permanently healthy by `T_v`, so neither side nor far resets can reach `v` thereafter; it clears by `U_v`.

`T_v` depends only on lower-height streams, independent of `v`'s six streams. Conditional on those lower streams, the residual waits at `v` are independent rate-`kappa` exponentials, and the conditional law does not depend on the value of `T_v`. Strong Markov at the first collection supplies the second fresh collection. Conditional joint laws at a common height are products; induction over heights proves mutual independence of the certificate service durations `D_v`. Actual clearance times and ticket states need not be independent.

For one coupon collection `M=max(E_1,...,E_6)`, the elementary domination by `sum E_i` gives `E exp(kappa M/2)<=64`. Thus `E exp(kappa D_v/2)<=4096`. There are at most `4^H` predecessor paths of height `H`, giving the conservative tail `2(16384)^H exp(-kappa t/2)`. The preserved audit improves the exact two-collection moment to `(1024/231)^2`, but this reconstruction retains the conservative source constants; that refinement does not improve the separate dependency-chain constant automatically.

## 6. Fresh fixed forcing flags

The five forcing sets are `A_i={a: ||a||_infinity<=R, a_i>=0}` for `i=1,...,4`, and `A_5={a: ||a||_infinity<=R, h(a)<=-1}`. Let `phi=OR_j AND_(a in A_j) healthy_a`.

On each independent slab of length `Delta=Cb/kappa`, the target bad flag is the union of: a fault birth whose complete reset box meets the radius-`R+2` guard; failure of a fresh lower-height halfspace service certificate to clear the target by the slab endpoint; and a strictly ordered backward old-input chain of `m=floor(Rb/2)` correction marks ending anywhere in the target at any slab time. The certificate is truncated at the endpoint and never reads a future slab. The chain may revisit clock locations but cannot reuse one event at zero elapsed time.

Each structural backward event has at most 11 anchor locations, six labels and five old inputs; 512 safely bounds all choices. The first `m` marks remain within the deterministic guard. Fault enlargement is quantified in `GUARD_RATE_THEOREM.md`; taking `b` at least the fixed boundary-reset radius preserves the literal radius-`R+3` primitive guard.

If a forcing conjunction is healthy initially and the target flag is good, compare inside the guard to the corresponding maximal infected halfspace profile. Exterior influence needs an excluded long ordered chain. A coordinate halfspace remains healthy; the lower-height profile clears by the excluded service-failure event. Hence, uniformly over microscopic inputs and exterior histories,

`zeta_(z,n+1) >= (1-B_(z,n)) phi(zeta_n shifted by z)`.                     (R1)

The service and chain tails tend to zero as `b` grows after `C,R` are fixed. Then choose the proposal intensity small enough for the birth term. No implemented service register, physical global clock or coarse controller is introduced.

## 7. Direct deterministic eroder proof

The map `phi` is attractive because it is a monotone DNF. Its eroder property can be checked here without an additional import. If `Z_n` is a nonempty finite zero set and `x in Z_(n+1)`, every conjunction has a zero parent. For conjunction `i<=4` choose a zero parent `x+a` with `a_i>=0`; this gives

`x_i <= max_{y in Z_n} y_i`.

For conjunction 5 choose a zero parent with `h(a)<=-1`; this gives

`h(x)>= min_{y in Z_n} h(y)+1`.

Therefore all four coordinate maxima are nonincreasing and the minimum height increases by at least one each step. If `m_i=max_{Z_0}x_i` and `h_min=min_{Z_0}h(x)`, no zero can remain after `sum_i m_i-h_min+1` steps. The same bounds keep every intermediate zero set finite. Thus `phi` meets the attractive-eroder hypothesis used by HT.

## 8. LSS and a single whole-history coupling

Each bad flag is a function of a fixed subset of independent primitive increments in one slab. Its support is disjoint from the union of primitive supports of all sufficiently distant flags, so it is independent of the joint distant sigma field. Slabs are fresh and independent.

The required external LSS premise is that a sufficiently high neighborhood-conditional healthy probability on a fixed bounded-degree dependency graph stochastically dominates iid healthy bits with any prescribed density below one. The original LSS theorem pages were not acquired in this investigation; that remains an explicit imported theorem, not a source inspected and proved here.

Apply that import to each infinite slab, then take independent copies of the slab coupling. One obtains a single iid space-time death field `Xi` dominating every native `B` simultaneously. A regular conditional kernel can retain the original primitive law while adding the coupling randomness. This is a coupling of the whole future, rather than separate one-time marginal comparisons.

Start native `theta` and iid comparator `omega` from all ones. Monotonicity and `B<=Xi` give `theta>=omega` at every space-time point. Initialize a stationary iid-death comparator from the upper invariant measure using independent past deaths, then share its future death field with `omega`. Since all ones dominates that state, `theta>=omega>=bar_omega` pathwise. Thus the native zero set is contained in the stationary comparator's zero set.

HT arXiv:2212.08437v2 Corollary 9.5 was acquired and checked at PDF page 25. For the fixed `phi` and fixed positive finite connectivity radius it supplies an exponential anchored stationary zero-component diameter tail at sufficiently rare iid death. It supplies neither a finite-torus stationary theorem nor a practical numerical death threshold.

## 9. Finite torus by stopped closed-witness replay

Use coarse side `M`, `k=4R+4` and `ell=M/128`, with `M` large enough that the fixed primitive enlargement is injective. Reveal zero output vertices by increasing time, with a deterministic order within each layer. Stop at the first insertion whose undirected `k`-connected zero component has diameter at least `ell`.

Let its inserted anchor be `z`. Every previously existing component has diameter below `ell`; each component newly joined to `z` has a point within `k` of `z`. Hence the entire newly merged component lies within distance `ell+k` of `z`, and has a point at distance at least `ell/2` from `z`.

For every nonforced zero in that component, choose one older zero parent from each forcing set. Such a parent is `k`-near, already revealed, and therefore in the same component. Recursion closes inside the component and ends at forced zeros, since layer zero has none. Only the required zero ancestors are needed; no complete backward light cone is copied.

For each deterministic prospective anchor, copy primitive increments in its deterministic spatial patch enlarged by the primitive guard into one injective infinite lift, and extend independently outside. The copied field has the ordinary infinite independent primitive law. The stopped component supplies a closed witness that replays as zeros in the infinite native process by induction. The event is contained in an infinite anchored zero path reaching `ell/2`, bounded by HT after the whole-history coupling.

Union over at most `NM^4` deterministic insertion anchors yields `C NM^4 exp(-cM)`. No region is selected adaptively and then conditioned to have an unaltered law. No LSS theorem is applied directly on the torus. The estimate is for finite horizons; eventual absorbing all-zero histories are consistent with it.

## 10. Entire slab support, including pre-jump times

At any time inside slab `n`, trace a positive ticket through old positive inputs. On a good target flag it cannot hit a local birth and cannot contain `m` correction marks, so it reaches a positive slab-start site within the fixed coarse halo. Since `theta_n<=zeta_n` in healthy order, that initial site belongs to a coarse `theta_n` zero. On a bad target flag the target itself is a forced `theta_(n+1)` zero. Hence all occupied fine sites in that slab lie in

`N_R({theta_n=0}) union {theta_(n+1)=0}`.                                    (R2)

Two adjacent fine syndrome vertices map to coarse zeros with spatial infinity distance at most `2R+1` and time difference at most one. Their Euclidean space-time distance is below `4R+4=k`. A fine syndrome component of ambient infinity diameter at least `L/32` therefore forces a coarse zero component of diameter at least `M/32-2R-1`, exceeding `M/128` for sufficiently large `M`.

This covers transient, post-event and pre-event syndromes, rather than only slab endpoints. Before coarse first escape every Pauli history has small syndrome components at every physical event.

## 11. Decoder and entire accumulated homology

For each syndrome-edge connected component of diameter below `rho=L/8`, choose its consistent short lift and a deterministic filling inside its coordinate hull. The hull is contractible; axial prism contraction gives a filling. Each component is itself a cycle by even incidence. Dependence only on the component makes identical unaffected fillings cancel. A fixed global fallback on other reachable syndromes defines a total perfect decoder, but that fallback is never used before first escape.

Let `E` be the entire accumulated error two-chain and `s=boundary E`. At a bounded-patch Pauli event `F`, every affected old component touches the event box. With pre-event component diameters below `r=L/32`, all affected old/new components, their hull fillings and `F` have one consistent lift into a box of side `2r+O(q)<rho`. The unaffected fillings cancel. Therefore

`F+D(s)+D(s+boundary F)`

is a closed two-chain in a contractible box and is a stabilizer boundary. The decoded class `[E+D(boundary E)]` cannot change at that event. This covers splits, merges, disappearing syndromes, local closed parts of `F` and arbitrarily large historical support of `E`. One must never erase historical faces because a syndrome vanished.

Induction from the zero chain gives trivial decoded homology for every Pauli history before first escape. An arbitrary global fallback with large components elsewhere would not justify a stronger localized-hazard theorem; only the global small-component regime is used here.

## 12. Whole-Kraus proof and reference-uniform bound

Condition on one full proposal schedule without exposing Kraus outcomes. The conditioned quantum map is an ordered composition of CPTP channels and remains trace preserving. Its schedule law is input independent.

For a full Kraus record, expand each local fault Kraus operator in the complete finite Pauli basis of its declared patch. Every nonzero term is a Pauli error history. At an ideal completed pair Kraus, the syndrome projector is zero or one on that history, independently of logical amplitudes and reference entanglement. A nonzero term follows a legal pair trajectory on the same physical schedule. The universal ticket event and decoder proof make its recovered action scalar on the entire code. Thus the **sum** of the terms is scalar too. For recovered Kraus operators `R_j=c_j I`, trace preservation gives `sum_j |c_j|^2=1`; the conditioned recovered channel is exactly logical identity.

There is no absolute coefficient sum, dimension factor or exponential normalization loss. No assumption that correcting selected basis states alone preserves coherence is used. The same identity holds tensored with any untouched reference.

Average schedules. The logical map is `(1-p_bad)Id+p_bad B` for a CPTP map `B`, so its ordinary unhalved diamond distance is at most `2p_bad`. Union the CSS escape events without assuming independence, take `N=ceil(T/Delta)+1`, and absorb fixed `b,C` into the constants to obtain the claimed finite-horizon form.

## 13. Structured transfer and unresolved obligations

Any exact compiler producing bounded-patch CPTP proposals with fixed input-independent rates below the explicitly charged incident budget enters this proof. The Pauli compiler and the seven-Pauli false-trigger model are made concrete in the other files. A general fixed known-operator dictionary enters by the same Kraus-span receiver, conditional on its separate exact compiler and installed floors. No unknown continuous quantum-bath coupling is admitted by changing coefficient notation.

No concrete contradiction was found to the literal completed-pair receiving interface under these assumptions. New closure here consists of the explicit guard intensity/admission formula, the exact same-patch correction-error expansion, and an explicit deterministic eroder check; it is not external certification of the asynchronous theorem. The original LSS source pages, independent specialist review, historical priority, acquired physical noise/geometry, useful constants and all hardware preparation/readout/reset/energy costs remain open.
