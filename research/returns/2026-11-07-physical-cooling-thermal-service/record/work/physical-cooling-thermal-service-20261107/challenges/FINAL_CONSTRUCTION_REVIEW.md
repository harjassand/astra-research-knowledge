# Final construction and source review

Constructor, 7 November 2026. Reviewed dossier:

`outputs/PHYSICAL_COOLING_THERMAL_SERVICE_RESEARCH_DOSSIER.md`

SHA256 **d7e25afde8da5874136adb99d0dd0ad7fbdb74329dabc7b756124423951e9a7e**.

This is a version-bound review of Sections 9, 10 and 13 against my frozen independent construction, `constructor/DETERMINISTIC_SWEEP_REVIEW.md` (SHA256 `e5d09a44d67266cd7b5a8c5b7f9ec67210754d810d902377d5aac906ce9c7c6a`), and `constructor/COMPILER_AND_CLASSICAL_IMPORT_AUDIT.md` (SHA256 `6ab9b3fb52a57494f923162d93bb5c4877d80b9026af0d99cd7642988821fafa`). I did not edit the dossier.

**Verdict: PASS at the declared restricted physical and staging premises.** The two-body compiler and matched-comparator conclusion are supported at their exact scopes. The dossier correctly leaves native universality and removal of CFG's noiseless internal classical processing NOT CLOSED. Two accounting clarifications below would make its standalone precision/time formulas unambiguous. Neither changes the proved construction or adds a new physical assumption.

## 1. Section 9: encoded input, recovery and computation

The actual sequence respects the prior quantum-port proof: unknown encoded input; isolated stochastic staging; positive sparse output interfaces; short noisy bath-retaining links; common-span recovery; encoded output. The output is a physical computational-code block, not an uncharged perfect bare decoder. The same DATA code/canonical module is used, and logical/reference/gauge correlations are retained.

The exact CFG imports are correctly Lemma 40 plus Lemmas 41--42, rather than the literal operational statement of Theorem 53. The displayed waiting-inclusive sizes S_E=O(n^3), S_D=O(n^4), and ell=O(n) at exp(-cn) target error match the coherent decoder addendum. Its support-tail and decoder argument correct the combined memory/link/interface error span, which is stronger than correcting each separately.

The native selected CCZ condition and identical-CSS CNOT condition are properly distinguished; no native universal gate set is inferred. Aharonov--Ben-Or's Section 4.2 quantum-interface limitation is accurately preserved. The supplied quantum staging model still has noiseless internal classical processing, so the result is the stated hybrid operation, not a fully noisy universal computer.

The coefficient 2K delta_round can remain a conservative *logical half-distance* contribution when K counts all compared cooling maps. If the complete physical actual-versus-CP/TNI comparison has norm e_K<=2K delta_round, its missing mass is <=e_K and positive on the logical marginal. Thus half the final logical trace norm is <=e_K, without an extra factor of two in that displayed half-distance budget.

### Cooling-round counting clarification

The service sequence says K storage sweeps and G gates each followed by a fixed restoring number of sweeps. The error formula and Section 13 must use the same count. Either define K from the outset to include **every physical cooling sweep**, or introduce

    K_tot=K_storage+k_restore G+k_entry

(with the actual integer entry/restoring counts) and use K_tot in 2K_tot delta_round, the source/location counts and the time formula. Gate error may instead include its restoring sequence, but that convention must be explicit. An insertion-ready sentence is:

> Here K denotes the total number of physical cooling sweeps, including entry cooling and all gate-restoring sweeps; it excludes the finite gate bursts and the charged WRITE/READ circuits.

This is bookkeeping, not a missing mathematical protection step.

## 2. Section 10: fixed-accuracy powered two-body implementation

The fixed-patch synthesis bound is source-checked. Barenco et al., arXiv:quant-ph/9503016v1, Corollary 7.6 and the end of Section 8, gives an exact ancilla-free Theta(q^3 4^q) construction from arbitrary one-qubit gates and CNOT. The dossier applies it to the fixed patch q_*, not n, and does not add free pure work ancillas.

Dawson--Nielsen, arXiv:quant-ph/0505030v2, Definition 1 and Theorem 1, requires a finite inverse-closed instruction set dense in the relevant SU(d). The dossier retains these hypotheses. Operator error delta_syn/(4m_*) per synthesized rotation is sufficient because ||Ad_U-Ad_V||_diamond<=2||U-V||_infinity and telescoping makes the resulting macro-channel error <=delta_syn/2. Its stated delta_syn budget is consequently conservative. The exponent c_SK may be taken approximately 3.97 for the cited algorithm. No hardware-library universality is silently inferred.

All catalogue patches in one colour are disjoint. An elementary error inside a patch can affect only that patch until its circuit completes, and then at most one bounded enlargement per later patch colour. Thus the output cone is bounded independently of m_syn, even though the elapsed depth is chi m_syn. This requires the synthesis to use only the specified patch wires/edges. If routing leaves the patch, enlarge q_*, the colour count and the support constants to include the actual routes before applying the theorem. The stated nongeometric bounded-degree graph can provide all needed within-patch couplers; no Euclidean routing theorem follows.

The actual local synthesis/calibration/continuous-error budget is fixed independently of n and duration. The whole-sweep diamond distance may grow as O(n delta_syn); that does not harm the support-counting threshold argument. Every gate, ancilla idle, wait, source delivery, routing and switch must be included in the displayed constants. Fixed complete errors from coherent calibration are legitimate local insertions, not positive stochastic flags. Removing physical JU makes U diagnostic and the machine driven; the dossier explicitly preserves that distinction.

### Source term clarification in the standalone budget

Section 4, equation (5), already includes the finite-temperature source contribution, while Section 10 abbreviates its local budget as mu_reset. To prevent mu_reset from being read as only implementation error, use the explicit form

    mu_sweep <=c_cat(delta_syn+m_syn delta_phys)
        +mu_idle+mu_reset,impl+mu_switch+mu_route+mu_src.

For independent single-spin thermal tokens,

    mu_src=(2/n)sum_a q_(d_a).

For Section 8's interacting-pair reserve, compare the **whole delivered pair** with its ground-pair reference, giving

    mu_src <=(2/n)sum_a p_bad,a,

with both-spin support and retained/excluded partner treated exactly as stated there. A token marginal q_token is not the reference-safe pair error. This explicit spelling leaves the existing equation (5) and theorem unchanged.

The drive-work variation bound is correctly only a bound on system-Hamiltonian drive work. Source-pair decoupling or source-gap quenches, transport and cyclic refresh remain additional paid operations. No thermodynamic efficiency follows from the gate count.

## 3. Section 13: full resources and inclusion comparator

The section correctly distinguishes O(n) DATA/current-source workspace from an O(nK) finite precharged bank's **actual hardware**. It does not claim the latter is an economical indefinitely cycling refrigerator. Future reserve isolation/source stability and a replenished factory are not proved by the DATA threshold. It also correctly adds polynomial encoded staging, source acquisition, routing, clocks/programme storage and waiting costs.

For full elapsed time, make the count convention above explicit and display, if desired,

    T_full=K_tot tau_sweep+G tau_gate+T_WRITE+T_READ+T_extra,

where T_extra contains any transport/switch/entry time not already included in the corresponding primitive durations. No term should be counted twice. The analogous elementary-location bound is

    L_full <=c_cat m_syn n K_tot+L_gate n G+L_ports+L_extra.

The code-family density/effective-availability caveat for turning the admissible-length bound into uniform n=O(log(K/epsilon)) is correct. Ordinary FT remains a strong comparator with polylogarithmic overhead under its own contracts. The inclusion test is decisive and rigorous: an active controller granted the same resources can execute this exact schedule, so this compiler cannot prove strict advantage over that comparison class. It does not assert a lower bound against future thermal architectures or commercial optimality.

## 4. Insertion-ready Shtanko--Sharma comparator

Recommended paragraph for Section 12 (and cross-reference from Section 13):

> Shtanko--Sharma, [arXiv:2411.04819v1](https://arxiv.org/abs/2411.04819v1), Lemma 7 and Corollary 1, equations (92)--(106), construct measurement-free RESETs by algorithmic cooling under contracting nonunital single-qubit noise. Their formal Theorem 1, equation (136), states simulation of local noiseless-circuit output at sufficiently weak noise, with polylogarithmic size/accuracy overhead at fixed physical parameters. This is a substantive powered-refrigeration and computation predecessor. Its noise is a product of the same single-qubit channel after local unitary layers, including idles, with known nonmaximally mixed fixed point. It does not supply the present arbitrary retained-bath perturbation theorem. Its proof initializes logical zero states, equation (117), and uses final logical-Z/majority readout, equations (131)--(133); it is not a reference-safe unknown-state port import. We use the construction as a comparator and do not import its exact asserted overhead exponents.

Primary PDF cached at `constructor/sources/shtanko-sharma-2411.04819v1.pdf`, SHA256 `e9f158dd9330f953d695bab621cb4dd595b6ad0cfd9e4582e2e99d93de0103df`. The relevant source contract is Section 1.2, Definitions 1--2, equations (1)--(3): strength kappa=||N-I||_diamond, contracting channel N, fixed-point purity eta>0. The threshold relation uses a fixed d>=1 and any exponent mu>log(3)/log(3/2), with sufficiently small kappa=O(eta^(mu/d)). These source parameters are unrelated to the present dossier's error-budget symbol mu.

The conservative word *polylogarithmic* is deliberate. The source's equation (135) writes a linear logarithm after substituting fixed-base powers n_B^L and Q^L with L=O(log log S); that substitution alone gives a fixed power of log S, rather than automatically exponent one. No numerical threshold or exact logarithmic exponent from that source is needed in the present theorem or inclusion comparator. This observation does not negate the substantive prior powered/reset capability.

## 5. Final scope

The reviewed dossier earns a finite fixed-accuracy construction under its named fresh-source and local joint-noise premises, plus the inherited restricted encoded-port operation. Native universality, fully noisy classical-control/port substitution, affordable recycling, practical constants, geometry, priority and full-resource advantage remain unproved, exactly as its ledger says. The recommended comparator paragraph strengthens predecessor accounting without changing any theorem.

## 6. Version-bound follow-up: accounting and comparator incorporated

The principal subsequently revised the dossier to SHA256 **558c3db6ce8ca8dfa3a22ca5f2146aef652e563f67a3f649e0eebc513233a4ca** while this review was being written. I re-read the affected Sections 9, 10, 12.6 and 13 against that version.

Both accounting clarifications above are now applied: K_tot expressly counts all entry/restoring sweeps and is used in the complete error/resource/time budget; mu_src is separated from reset implementation errors with the correct simple-token/pair-source coefficients. The full elapsed duration includes G tau_gate and T_ports. The added Shtanko--Sharma paragraph gives the right actual predecessor, theorem numbers and contract limitations, and does not import its exact overhead exponent or claim unknown-state quantum interfaces. Its text names v1; a version-suffixed link would make that bibliographic pin explicit as well.

**PASS for the checked construction/source scope at this revised hash, with no outstanding substantive construction correction.** Fixed within-patch connectivity/routing and complete budget assumptions remain the stated hardware hypotheses, not proved geometry. This follow-up does not expand the review to unrelated literature imports or promote any open universality/classical-control claim.

## 7. Settled final-hash verdict

**PASS** for dossier SHA256 **92cd3cf466b669f39ae9bab6e845330d46470a7280d7519fcc4d9a00216ceb1b**, delta-checked against the preceding reviewed version. The reset ground-basis relabeling is consistent with the collision convention; the n>=n0 qualification and independent private source-preparation/waiting/no-return clarification preserve the local support and signed-budget hypotheses. The stated Wang/Ong comparator corrections and record-index addition introduce no construction contradiction. Sections 9, 10 and 13 retain the accepted precision, port and full-resource scopes. No new research was performed, no dossier bytes were edited, and no outstanding substantive construction correction was found at this final hash.
