# Independent hostile review of the backward-chain CPTP-kick threshold
2026-10-29. Reviewer: audit_ssf_window_proof. Separate from the physical-compiler review.

## Verdict and required correction
The new backward-chain argument survives the requested hostile checks **for the ideal atomic model, with D0/D1 applied sectorwise**. It supplies a positive physical-record certificate for the existence of ANY cutoff-bad Pauli branch. Consequently it genuinely avoids the invalid inference from separate Pauli-branch probability estimates to a coherent quantum threshold. I found no counterexample to the chain geometry, volume estimate, or terminal positive-tail union bound.

**Required formulation correction:** the governing SSF D1 is a one-CSS-sector statement. A minimum-weight representative in full Pauli support is not automatically minimum/reduced in each sector. Run the proof independently for X and Z errors using fixed sectorwise minimum-syndrome representatives and use final recovery R_X R_Z. A shared primitive kick record may affect both; independence between sectors is unnecessary. Union-bound the two bad-record sets. For common worst-case constants the logical diamond bound becomes

  2 min{1, 2 L R N r^ell/(1-r)}.

The single-sector bound stays as written. This is a constant-factor correction, not a failure of the proposed method. The author was notified before this review was written.

## Exact reviewed versions
- SPACETIME_CPTP_MEMORY.md SHA256:
  60b204a3b8d78279893827d346773d54c4681c381e289a44cb6d850d4aa6e4d9
- ASYNCHRONOUS_WINDOW_WITNESS.md SHA256:
  202bfab8a52bb8e8c35131464df7014f199dfb526bc227f533b0879cee62ea9d

Later changes are not silently included in this verdict; any recheck is appended below.

## 1. Deterministic interface D0/D1
D0 holds unconditionally with C_seed=2(1+w Delta) in one sector. It uses the original incoming representative and original block execution support; the terminal minimum-syndrome reduction only enlarges that support. Each component's representative has no more weight than its actual outgoing error because componentwise replacement preserves syndrome. The work budget then applies without a small-cluster assumption.

D1's fresh alternative comes from the virtual history ending at the reduced residual. Its ancestral seed-density alternative must instead use the enlarged components of the ORIGINAL history union terminal representative. Those components contain the target, meet the target componentwise, preserve the ancestor lower bound, and obey D0 with the ORIGINAL incoming representative. This is precisely the distinction made in the governing witness note. Using the virtual initial error as an independent seed distribution would be wrong; the draft does not require that.

Phrase “the block starts and ends with chosen representatives” as *boundary gauge relabeling*. A single physical serial history need not have both reduced endpoints. The virtual suffix is an analysis device, and the D0 seeds remain the original incoming boundary representative.

## 2. First bad cutoff and gauge substitutions
On prior Good blocks, every component has support strictly below code distance and the small-error cutoff. Its zero-syndrome difference is a stabilizer. Replacing the outgoing error by the fixed representative therefore changes every subsequent Pauli branch only by a scalar phase and stabilizers, preserving local syndrome decisions and logical action. This remains valid for a compatible Kraus branch of the actual ideal measurement instruments.

If no cutoff-bad block occurs, the terminal recovery restores that branch. Contraposition gives a first bad block for every uncorrected branch. The root component K is connected and has size at least ell. D0 remains available on it even though it is large. Splitting its seed mass at one half gives either fresh fault density or a nonempty earlier target of size at least |K|/(2 C_seed). No probabilistic residual induction enters.

## 3. Whole-target dichotomy and vertical connectivity
D1 must be applied to the ENTIRE target, as the draft does. Independently choosing F/A for separate components would create a branching tree and invalidate the stated one-terminal count.

For the whole-target choice, each earlier W_b component meets S_b, and S_b lies in W_{b+1}. A same-site vertical edge attaches each such component to the later union. Starting from connected root K, induction gives one connected animal in G times the block-time line. Some components can cease propagating farther backward; they remain connected through later layers and do not require new terminals. Targets need not hit every component of the later layer.

## 4. Terminal volume and time-zero termination
Every nonterminal transition creates a target at least a 1/(2 C_seed) fraction of its current witness. Every earlier ancestral witness expands that target by c_R. Hence nonterminal ancestry grows by gamma=c_R/(2 C_seed)>1 when moving backward.

A terminal F witness need not obey this growth. Containment alone gives |W_next| <= 2 C_seed M, where M is terminal size. Summing the subsequent geometric sequence yields exactly

  V <= [1+2 C_seed/(1-1/gamma)] M.

The root size implies V>=ell. The initial representative is empty. A nonempty target cannot continue across time zero; D0 forces fresh noise density if the chain reaches the first block. Thus every finite chain has a terminal, including the no-noise edge case (where no bad root can exist).

## 5. Fixed-record tail and animal entropy
For every fixed terminal spatial set and time layer, the primitive fault count is dominated by a Poisson count of mean <=epsilon z tau M. The no-ring majorant uses at most h0 M fixed hubs. These variables refer to exogenous physical driving records and are independent in the ideal model. The stated count moment and Markov exponent are valid. Actual Pauli supports are bounded by the declared primitive support count, regardless of Pauli coefficients or quantum outcomes.

For a fixed spacetime animal its earliest slice determines the terminal block and set. There is no extra choice of a terminal subset. Only the R window labels require a factor. Keep only certificate animals satisfying V<=K_vol M; their number is at most the total rooted-animal count. Since r<1 implies r0<1, r0^M <= r0^(V/K_vol). Rooting at any one of N sites in the final layer supplies the stated factor N. Summing the geometric tail and then possible first bad blocks is valid.

No Pauli-label union is hidden in this step: existence of a bad label path implies existence of a geometrically counted certificate using only primitive records. All branches can share the same certificate. Positivity is used ONLY for those actual record events.

## 6. Quantum correctability, not quantum residual laws
Expand the local DATA part of every noise Kraus operator in a finite Pauli basis, leaving arbitrary retained bath operators as coefficients. Fix an actual syndrome-instrument outcome record when evaluating a Kraus branch. Incompatible Pauli branches vanish; compatible branches are genuine accepted SSF histories. Branch-dependent stabilizer phases are absorbed into the bath coefficients, not interpreted as probabilities.

On a primitive schedule with no branch certificate, every compatible branch in both sectors is restored by the same final syndrome-dependent Pauli recovery. Therefore every corrected joint Kraus operator restricts on the encoded space to identity on the logical subsystem tensor a bath/record operator. Summing the actual CP outcomes preserves arbitrary logical/reference input, including same-syndrome coherence. Fixed exogenous schedules specify CPTP channels, so averaging bad schedules gives the factor-two diamond-distance estimate.

This does not cover continuous Hamiltonian insertions, signed Dyson events, data-dependent postselected primitive records, or independently bounding each Pauli branch. It assumes exact ideal syndrome instruments and exogenous bounded-rate kick locations.

## 7. Useful strengthening: arbitrary deterministic readout time
The complete-block restriction is unnecessary for the ideal mathematical output. At a fixed t, use floor(t/tau) complete blocks and one final partial block if needed. If the first bad block is partial, its root uses only D0; every earlier backward step uses D1 on a completed block. A fresh terminal in the partial block is Q-only, and its Poisson count is bounded by the full-duration tau budget. Therefore the same proof works with L=ceil(t/tau), without evolving past t or demanding contraction in the partial block.

This is for each specified deterministic observation time, not a uniform event over all uncountably many times. It does not address real compiler output with unfinished transactions.

## 8. Scope retained
This review certifies the new ideal-model combinatorial extension conditional on the governing code/SSF hypotheses and the noted sectorwise correction. It does not endorse the full physical compiler, its good-service lemma, marked-emission tails, coefficientwise transaction semantics, or physical readout. Those require their own reviewed interfaces. It establishes no literature novelty claim.

## Recheck of sectorwise repair
The author repaired the sector ambiguity and boundary-gauge wording. Rechecked SPACETIME_CPTP_MEMORY.md SHA256

  7732507edeb72cbe8ae700a4220d74d5e95706c0d372267cf2e3337acbde3af7.

Lines defining D0/D1 now explicitly use sector representatives, the final recovery is R_X R_Z, and the final positive-record/diamond bounds pay the factor of two for sectors. The required correction in this review is therefore resolved in this version. The arbitrary-deterministic-time strengthening in §7 above remains an optional extension; it is not needed for the stated complete-block theorem.
