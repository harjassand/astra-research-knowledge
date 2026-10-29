# Astra P2 — protected dynamics, bounded edges and actual readout

Research boundary: 29 October 2026. This tranche preserves earlier P2 eraser, finite-pump, calibration, protection-density and purification-flow work. Frozen predecessor proofs and their reviews were not rewritten. The current main result is a complete coherent error instrument for logical gates and renewal; it is not the predecessor's bath-representation certificate and does not inherit one for a changed physical bath.

## Main result and what it enables

[BOUNDARY_CONTROLLED_RENEWAL.md](central/BOUNDARY_CONTROLLED_RENEWAL.md) is the strongest construction in this tranche. A protected hierarchy \(P_0,\ldots,P_q\) need not live inside an invariant finite Fock cutoff. It is enough to bound the actual edges between grades and the edge leaving the last grade. Arbitrarily strong or unbounded dynamics inside a grade or beyond the protected boundary is propagated unitarily.

For a common edge envelope with lifetime integral \(\Theta_j\),
\[
\tfrac12\|\mathcal E_{\rm physical}-\mathcal E_{\rm protected}\|_\diamond
\le\min\{1,\sum_j\Theta_j^{q_j+1}/(q_j+1)!\}.
\]
The underlying ordered-edge integral is also proved. It retains the full bath, old blocks, references and actual records at their declared interfaces.

For the constructed two-mode binomial family, \(N=(q+1)^2\), a linear ladder interaction with bounded complete-memory coefficients gives
\[
\Theta_j\le[\sqrt{N+q}+\sqrt{N+q+1}]
\int_j(\|C_a(t)\|+\|C_b(t)\|)dt.
\]
The physical oscillator can develop unbounded Fock support. A driven spin bus and retired oscillators returning through that bounded bus are explicitly admitted. The proof constructs the all-Fock unitary propagators and their pinched comparisons; finite-cutoff numerics are not substituted for that existence proof.

This removes the global-norm obstruction encountered during the research. It allows the protected gate and handoff machinery to be applied without a bath reset, independent noise assumption, conserved bath charge, or permanent retirement, provided every currently active boundary satisfies the stated operator interface. An unbounded bath coefficient or an uncontrolled shortcut across grades still needs another estimate.

The result is a conditional H,T,CNOT circuit interface, not an acquired device. Fresh encoded supply, globally grade-preserving controls throughout execution, inter-block coupling, actual durations, calibration and detector interfaces remain paid obligations. There are \(N\) photons per fresh block and WN across W lifetimes. Favorable scaling of the designated exchange-noise component does not establish total fault tolerance.

If the acquired lifetime exposure remains uniformly bounded by G with \(r=e\sqrt6G<1\), choosing \(q+1\ge\log(W/\epsilon)/\log(1/r)\), and q>=1, makes that designated contribution at most epsilon. The code then uses \(O(\log^2(W/\epsilon))\) photons per block and \(O(W\log^2(W/\epsilon))\) supplied photons. This is conditional resource scaling for the proved noise component. It is not a claim that gate time, preparation error or detection error obey those scalings.

## Readout at the operation actually required

[CONSTRUCTIVE_FINE_READOUT.md](central/readout/CONSTRUCTIVE_FINE_READOUT.md) supplies direct mode-count readout for arbitrary coherent admitted syndromes. It needs no coherent inverse of the syndrome encoding. The decoded grid parity is exact, and the fine instrument includes its conditional syndrome and returning-memory update.

[ACTUAL_RECORD_FLAGGED_READOUT.md](central/readout/ACTUAL_RECORD_FLAGGED_READOUT.md) changes the comparison to a correct answer or an explicit failure flag while preserving the same actual raw counts and count-conditioned memory. For the specified vacuum-attenuation/count model, zero or one missed photon cannot produce an accepted wrong answer. The exact complete-channel comparison equals the norm of an explicit positive accepted-wrong effect W.

For q=1 it is exactly \(\eta^3(1-\eta)^2\). This is a silent-error metric for a declared correct-or-flag operation. Flags remain a separately charged, potentially first-order destructive cost; they do not grant a free retry. Lost detection fields must genuinely be retired for the classical thinning model. Returning earlier bath memory remains included.

## Actual review map

These are internal reviews with their authorship boundaries stated, not external peer review or historical priority findings.

| Construction | Status and actual review |
|---|---|
| Bounded-edge theorem and all-Fock existence | Accepted by protected_algebra; [domain/propagator review](central/boundary_review/INDEPENDENT_REVIEW.md) and receipt pin the exact subject. Separately accepted by architecture_challenge at the [driven-bus and returning-memory scope](central/boundary_physics_review/INDEPENDENT_REVIEW.md), with five complete-output diagnostics. |
| Explicit q=1 conserving loss/gain controls and protected handoff | Accepted after an invariant-domain clarification and full-output diagnostic correction; [review](reviews/protected_handoff/INDEPENDENT_REVIEW.md). |
| Arbitrary-q graded code and factorial lifetime theorem | Accepted; [review](central/general_review/INDEPENDENT_REVIEW.md) includes independent exact instances through q=4. |
| Earlier causal finite-bath energy window and synthesis | Accepted; [review](central/finite_supply/architecture_review/INDEPENDENT_REVIEW.md). Still useful, with stricter sufficient conservation/retirement assumptions than the new edge theorem. |
| Earlier modular energy-window composition | Accepted; [review](central/modular_review/INDEPENDENT_REVIEW.md). Its individual bath-charge condition belongs to that representation. |
| Complete fine-count readout | Accepted; [review](central/readout/review/INDEPENDENT_REVIEW.md). |
| Same-record correct-or-flag readout | Accepted by root; [review](central/readout/flag_review/INDEPENDENT_REVIEW.md). |
| Future-program causal-record algebra | Accepted by root; [review](algebra/review/ROOT_REVIEW.md). Fixed-instrument scope, including the changed-decoder alternative. |
| Fixed-label cq 2-design criterion and expander control counterexample | Accepted; [review](conventional/review/INDEPENDENT_REVIEW.md), with shared conceptual premises disclosed. |
| One-exchange-order loss-only conventional construction | Author-derived and executed in [architecture](architecture/ONE_EXCHANGE_ORDER_FAMILY.md); not silently covered by its author's reviews of root work. |

The source ledgers distinguish actually read governing passages, inherited acceptance, intake reconstruction, and missing producer sources. Root does not claim that all side work has an independent review.

## Executable instrument and useful failures

[boundary_budget.py](central/boundary_budget.py) computes the ordered-edge integral exactly for supplied rational, piecewise-constant edge bounds. [Usage and scope](central/BOUNDARY_BUDGET_USAGE.md) include the input format and an outward rational enclosure of the bosonic square roots. The saved example is synthetic. The program does not acquire a coupling norm or turn an analytic allowance into a measured fault probability. It is author-executed; the theorem's independent review is not an independent review of this calculator.

The program also accepts an initially occupied maximum grade. This correctly reduces the protection order instead of declaring an old syndrome fresh. The bosonic family and the simplified sufficient regime use q >= 1; the abstract edge theorem can also be used with q=0.

The productive failures are retained with their proofs and checks:

- Separate edge integrals cannot generally be multiplied and divided by a factorial. Ordered pulses can violate that expression; the actual ordered integral is valid.
- Formal zero block entries do not justify a self-adjoint pinching when the domains differ. The new theorem uses one specified bounded-perturbation realization.
- A growing global interaction norm, a driven bath, or returning energy donors defeats the earlier invariant-window method without defeating the bounded active-edge method.
- Keeping only output inside the admitted subspace hides leakage. The corrected handoff checks retain the complete output and the old logical factor.
- A fine-record distance is not the logical measurement error. The correct-or-flag readout changes the declared comparison and separately retains destructive flag probability.
- Fixed-decoder quantum-memory lower bounds do not rule out a better conventional decoder; a spectral gap and small generator defects do not alone give dimension-independent recovery.

## Strong conventional routes and remaining physical frontier

[SOURCES_AND_SCOPE.md](central/SOURCES_AND_SCOPE.md) credits established binomial codes, graded error-transparent Hamiltonians, coherent recovery, non-Markovian norm comparisons and energy-constrained methods. It records the directly read portions of current Astra sources and their corrections. Missing producer archives, unavailable complete derivations and unexecuted primary implementations remain gaps.

Existing error-transparent controls and direct coherent transfer are the constructive starting points. Current finite-energy GKP fault-tolerance results provide a stronger completed preparation/gate/detection framework under their independent-Markovian assumptions. This tranche instead proves a coherent returning-memory comparison at a narrower supplied interaction and control interface. Neither claim subsumes the other merely by comparing one error number; historical novelty and hardware advantage are not established.

The decisive remaining operational issue is acquisition of grade-preserving logical and inter-block Hamiltonians with calibrated imperfections and durations that keep exposure useful as q grows. Photon supply, coherent preparation/capture, holding, detection and reuse remain part of the operation. The present proof has removed a representation obstruction; it has not paid those implementation costs or converted its sufficient regime into a total computing threshold.
