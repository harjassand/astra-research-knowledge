# Destructive CSS readout as a possible non-deferrable consumer
2026-10-30. Root derivation / candidate. Depends on unaccepted physical retirement if used on the native apparatus. Not a noisy classical-controller theorem.

## Exact algebraic interface
For a CSS code write |l_L>=|C_X|^(−1/2) Σ_(c∈C_X)|x_l+c>, with distinct logical Z labels l represented by cosets of the X-stabilizer binary subspace C_X inside the Z-check kernel. Consider the ENTIRE Pauli error span X^a Z^b of total weight≤t, with 2t below both logical X and logical Z distances.

Measure every physical DATA qubit in Z. Decode the classical bit string with one fixed rule that recovers the logical coset for every X-error of weight≤t. The rule can be chosen independently of b and all auxiliary coefficients. It yields the exact ideal logical-Z measurement instrument on arbitrary logical/reference inputs for every CPTP noise channel whose Kraus coefficients lie in this common span. This is standard CSS fault-tolerant readout algebra, not new decoding machinery.

Cross-term proof: for two error coefficients (a,b),(a',b') and physical output x, nonzero amplitudes require x+a in x_l+C_X and x+a' in x_l'+C_X. If l differs from l', then a+a' is a nontrivial logical-X representative of weight≤2t, impossible. Thus no wrong logical label or logical off-diagonal survives the grouped readout. For l=l', summing x over the corrected coset kills cross terms unless b+b' lies in C_X-perp. Its weight≤2t makes it a Z stabilizer rather than a logical Z, so the surviving scalar is independent of l. Auxiliary operator coefficients and external references may be retained throughout. This supplies the common coherent span statement, not a stochastic-Pauli assumption.

## Why this consumer matters
After actual retirement, bare DATA in a globally correctable span can be consumed immediately by destructive single-site measurements. There is no need to preserve a quantum output throughout the subsequent O(N) ideal classical queue computation. This is an actual measurement consequence rather than another uniformly deferrable Clifford frame. However it destroys the measured block, and does not itself provide quantum output, a magic-state factory or a reusable feedback computer.

## Finite-rate local measurement candidate
As a DECLARED new local readout primitive, give each site a pointer with wait,0,1 labels and separately resolved jumps J_b=√κ |b><wait|⊗P_b^Z. The summed source loss is κ|wait><wait|⊗I_DATA. Nominal readout at time T consists of an exact Z instrument with probability1−e^(−κT) and an explicit uncompleted outcome with probabilitye^(−κT), uniformly on unknown inputs. This is a local measurement reservoir, not access to an imagined environment record. It must be physically provided/calibrated and its pointer must be read.

With other DATA couplings off, nominal readout cannot spread the DATA support of bounded-body perturbations. One can therefore try a finite-time forward Dyson common-support expansion around the nominal CP readout process, as in the reviewed controller-boot proof. A norm tail beyond O(N) local perturbation insertions is exponentially small for ηT sufficiently small. Uncompleted ideal pointers also need a joint tail and a classical erasure/misread budget. Their probabilities cannot simply be treated independent after shared-bath noise is added; a positive effect/subset argument is needed.

## Still unpaid
Physical halt/retirement, actual detector coupling and calibration, joint incomplete-pointer bound under the actual continuous noise, classical pointer-read errors, reliable classical processing, and conditional use of the output. A bare ideal classical decoder is an explicit assumption until its circuit/redundancy/resource mechanism is supplied. No experimental advantage or new universal-computing theorem follows from this note.

## Constructive next step: finite noisy destructive readout
The following is a proposed complete readout bridge once the physical retirement input is earned. It is not yet independently checked.

Let M≤C_M N grouped DATA/readout sites, each pointer start wait, and the DATA/retained auxiliary channel lie (up to exp-small error) in a common Pauli span of weight≤αN acting on the code. Turn off all intersite nominal DATA couplings for readout; retain only the local J_0,J_1 pointer instruments and auxiliary/bath dynamics acting on NEITHER DATA NOR readout pointers. The input may have arbitrary DATA/controller/bath correlations supplied by retirement. No bath reset or identification is needed. Mode-transition operations need separate charging; one cannot simply erase still-live prefixes without the retirement result.

For the physical wait projectors B_i, L_readout*B_i=−κB_i exactly and nominal product factors give −κ|S|∏B_i. After centering local perturbation adjoints to annihilate I, the same bounded-body incident-norm subset hierarchy gives

  Tr ρ(T) ∏_(i∈S) B_i ≤ p(T)^|S|,
  p(T)^q=exp(−qκT)+(Cη/κ)(1−exp(−qκT)).

This uses the full actual joint CPTP evolution and allows a common retained bath. It is not an independent-detector assumption. A union bound yields exponentially small probability of more than βN incomplete pointers when p(T)<β/(e C_M).

A second, independent argument controls logical information, because correctly completed pointers may still be wrong. Expand the actual finite-time process around the nominal product readout CP propagators, using the FORWARD Dyson series. Each order-r perturbation term touches at most qr DATA/pointer sites, because nominal onsite instruments and bath evolution disjoint from DATA/readout pointers cannot spread the set of affected DATA sites. The total perturbation norm is at most C_phys Nη. For r*=γN the discarded norm tail is bounded by

  exp(C_phys NηT) [e C_phys ηT/γ]^(γN).

Pick fixed T for the incomplete-pointer tail, then η sufficiently small that this is exponentially small. No inverse dissipative propagator is used.

Project analytically onto at most βN incomplete pointers, and replace their output symbols by any fixed bits. This projection is a proof tool only; the real classical readout may simply mark or default these symbols. On every low-order term and each selected incomplete set, all sites outside the union of the initial error support, perturbation support and incomplete sites undergo the exact ideal Z instrument. The exceptional set has size at most (α+qγ+β)N. An arbitrary local output-bit instrument on this exceptional set has a finite operator expansion equivalent to arbitrary DATA operator coefficients on that set followed by ideal physical Z measurement; pointer relabeling is represented by local X factors and local effects by DATA operator coefficients. Retained bath/reference operators remain as coefficients. This representation is algebraic, not a claim that the Dyson truncation is positive or a Pauli mixture.

If 2(α+qγ+β)N is below the relevant CSS distances, every such coefficient is in the exact readout-correctable span proved above. Consequently the grouped logical output of the truncated/projection map factors as the ideal logical-Z instrument times an auxiliary scalar map. The actual map is CP and trace preserving; normalization and the discarded norm/tail estimates then bound its distance from the ideal instrument. This last signed-truncation normalization step needs the same care as the controller-boot proof and is a key review obligation, not to be silently assumed.

For computational efficiency replace the arbitrary classical nearest-coset rule by the existing O(N) current-syndrome queue rule, after reducing α+qγ+β to its proved raw-energy/confinement radius. No unknown minimum-weight optimization is then supplied. The classical processor and its bit-output reliability remain explicit resources; a noisy distributed classical implementation is a different theorem.

This proposed bridge trades a quantum-preservation problem during decoding latency for immediate destructive physical measurement and later classical processing. It does not give a nondestructive quantum output port or adaptive feedback without further operations. The strong ordinary comparator is precisely standard destructive CSS readout; the potentially useful new composition is getting a native continuously corrected system into its input contract by actual retirement.

## Signed-truncation normalization lemma (root algebra)
It is enough to show the approximating HP map T has, after discarding every auxiliary output, the form

  T(ρ_LR)=Σ_l c_l |l><l|_out ⊗ <l|ρ_LR|l>_R,

with real c_l; one need not assert an auxiliary scalar independent of l when actual measurement histories are retained during the process. If the actual readout channel A is CPTP and ||A−T||_diamond≤ε, evaluating trace on |l><l| shows |c_l−1|≤ε for every l. The classical-block form then gives ||T−M_Z||_diamond=max_l|c_l−1|≤ε, hence ||A−M_Z||_diamond≤2ε. This is dimension independent, permits negative c_l in the algebraic truncation, and does not declare the truncation CP.

The remaining common-span obligation is therefore exactly: each low-order exceptional-set instrument cannot connect distinct logical-Z cosets and cannot retain logical off-diagonal input after ALL physical Z outcomes are grouped. Local phase/operator coefficients may affect c_l; trace normalization removes that freedom. This lemma applies to measuring the full logical-Z label. It does not automatically give selective nondestructive logical measurements that preserve unmeasured logical subsystems.

## Classical event filtering avoids a fictitious intermediate projection
At the actual endpoint all pointer labels are read as classical outcomes. The event that more than βN labels equal wait is therefore an ordinary output event, not a quantum syndrome measurement inserted during storage. Discard its CP output subchannel only in the proof. Its diamond norm equals its maximum event probability, bounded by δ_prog uniformly over input/reference. Cross terms between different pointer strings are already removed by the actual final pointer readout. Thus this filtering costs δ_prog, not a gentle-projection square root, and does not alter the physical operation. Apply the same contractive output filter to the signed Dyson truncation; its error remains the Dyson norm tail. Decode/default the retained incomplete sites by the fixed classical rule. The normalization lemma then bounds the complete implemented measurement by twice (δ_prog+Dyson tail+retirement input error), subject to the common-span proof and explicit interface premises above.

## Exact nominal split correction
The readout nominal propagator is the tensor product of the specified onsite DATA-pointer instruments and arbitrary auxiliary/bath dynamics that acts on NEITHER DATA NOR readout pointers. Initial auxiliary/bath correlations may remain. Any coupling, relabeling or control error touching DATA or pointers outside the specified onsite instruments belongs in the bounded incident perturbation budget. This is stronger and more precise than the earlier ambiguous phrase 'DATA-independent auxiliary/bath dynamics'. It is needed to commute untouched-site readout maps through the forward Dyson insertions.

## Finite shutoff ramp candidate (additional obligation, not yet accepted)
A zero-duration removal of residual DATA payload Hamiltonians is unnecessary if the following native-interface argument is completed. After retirement has made at most β_ctrl N owners nonready, keep first initiation OFF throughout a fixed finite ramp, and scale the remaining native DATA-touching terms to zero. The readiness audit shows termwise Hamiltonian commutation with every P_h and noncreating resolved resets. Scaling/removing such terms preserves these properties. On a definite initial nonready mask, nominal DATA action throughout the ramp is confined to the union of those owners' fixed DATA footprints. No new owner becomes nonready nominally. An arbitrary local continuous perturbation insertion can add only a fixed number of nonready owners/sites; subsequent nominal action enlarges its DATA support by a fixed owner-footprint factor, not by system size or a growing cascade of fresh initiations.

Thus a forward Dyson expansion through this finite ramp, followed by the nominal product readout, should retain a common DATA error span of weight at most

  α_mem N + r_F β_ctrl N + q_ramp r + β_incomplete N

at insertion order r, where q_ramp is a fixed enlarged local footprint. Coherent initial masks are retained as auxiliary coefficients; no physical mask measurement or independence is needed. The total perturbation norm tail uses the combined ramp+readout duration. This would pay the actual mode change with a finite control waveform instead of a perfect instantaneous switch.

Required checks: every nominal DATA term is indeed confined to the footprint of a currently nonready owner (A0 refresh and monitors are DATA identity); changes of owner labels under an insertion have bounded incidence; nominal reset records only remove nonready owners; and the controlled ramp does not turn initiation back on. Without these checks, the main finite readout result has an explicitly supplied decoupled-readout interface and the ramp remains unpaid.

## Classical decoder precision for destructive Z readout
Only Z-check parity bits computed from the physical Z outcomes are available. Use the sectorwise X-error queue/table from INTEGER_ENERGY_D0_D1.md and the explicit GPT circuit, not the full two-sector quantum syndrome snapshot mentioned in the generic ideal readout addendum. This queue corrects the bit string's X-error syndrome and then extracts its logical-Z coset. Physical Z errors need no measurement or correction for this destructive output. The energy/confinement radius used here is correspondingly the proved X-sector one. No X-check measurement of already destroyed DATA is assumed.
