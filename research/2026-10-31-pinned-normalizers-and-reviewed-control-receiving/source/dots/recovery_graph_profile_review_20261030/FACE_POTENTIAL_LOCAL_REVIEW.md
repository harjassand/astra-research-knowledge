# Independent bounded-face-potential local review

30 October 2026. This is a local principle/witness review, not a new full-network recurrence receipt or an integrated compiler acceptance.

## Verdict and frozen scope

**Accept the local replacement principle and the two-stage/killing-transform witness, with the binding precision completion.** Frozen sources in `face_potential_sources/` are:

- `BOUNDED_FACE_POTENTIAL_COMPILER.md`, SHA e45a1be7273eedd7ccdf6c38fa1c27a81eb1a063603b6efdb54217541e70f0e9;
- `TWO_STAGE_FACE_AND_KILL_REGULARIZATION.md`, SHA 7275d6a3218bcc9e774e35e64d84b499bd14739d85c7f2f301567f4c39cdd658;
- `FACE_POTENTIAL_LOCAL_PRECISIONS.md`, SHA c0b9c8adb1c351c4582d0acbf1ae3cc819231f44ca7734cf2c9775bc655753cc.

The separate 19-candidate example finder and its output were also inspected and independently rerun. Their limited certificate checks pass; this is not an implementation of the generic face-potential or full-network search. Exact hashes are recorded in `FACE_POTENTIAL_SOURCE_SHA256.txt`.

## 1. Killed generator and actual repeated-face costs

The structural restrictions are load-bearing: all internal hidden moves are a-neutral and pooled-neutral, no internal B-to-F edge is permitted, and restoration exits to positive D. Seeds produce positive D. For the local M-stage, connectors/clearing terminate, while a face seed ends its B excursion and continues in positive D.

The zero extension of psi has generator at most -1 on B for the subgenerator killed at restoration, seed and clearing. Connector stopping adds only a nonpositive contribution. Outside B, the only positive term is the summed actual positive-D ingress rate times psi at its actual output. Dynkin under finite localization, followed by nonnegative terminal discard and Fatou, therefore proves the displayed trace occupation inequality. It does not bound the number of returns or assume their probability small. Finite conserved-population shells already prevent local explosion; global recurrence is not needed.

During each B excursion A is constant until exit. Multiplying the potential by a fixed A-profile or by the inverse physical common factor consequently preserves the interior inequality. Ingress changes A by at most two, with both active endpoints above the fixed physical gate; ratios of these fixed-profile factors are bounded. Thus the same trace statement pays actual physical occupation and the weighted costs, not merely deleted-clock time. An initial B state contributes the bounded initial potential term and remains a carried launch input, not a population-reset input.

## 2. Independent moments and pooled labels

(P) yields E tau_B<=Psi uniformly. At every surviving face state, the same estimate applies; Markov at 2Psi and conditional iteration give geometric tails and all fixed face-time moments. No independent blocks are required.

The precision completion is important for global local-episode moments. At a seed-or-clear mark, the clear label has fixed probability p_clear=k0/(k_seed+k0), independent of the hidden path and mark time. Therefore a face excursion exits by restoration OR clearing within2Psi with probability at least p_clear/2. Count seed exits as failures in this lower bound. Restoration preserves pooled coordinates and clearing succeeds. Combining a finite baseline word with these face completions and the positive-D prescribed-jump probabilities c n^-2 gives a polynomial success probability in a fixed-duration block. This earns polynomial M-stage moments BEFORE sharper seed-restart occupation accounting; there is no circular bootstrap from an unproved restart duration.

Deleting a B excursion from the D-clock does not change pooled labels except for the actual terminal seed deletion. Hence the acquired baseline forcing events, adapted extra-to-a handling, geometric seed count and deterministic-horizon crossing proof remain valid. The trace inequality restores all deleted weighted holding time. With no B-to-F move, true-F entrances still have exactly the independently checked direct ingress hazards. Positive-D-start reset, fixed grades and same-episode reward ratios therefore retain their proofs.

An 'empty protected pool' must mean zero PHYSICAL mass in the D-containing pool. Y_D=0 after subtracting one protected particle is not forbidden: the old CE mixed face with one E is a valid example. With zero physical pool mass, pooled-neutral hidden moves cannot create D. Since B enablement is independent of a, evaluate the same hidden state at a=0, where seed/clear killing is absent. A bounded (P) potential would then force finite exit from a closed finite hidden chain with no killing, an impossibility. The precision completion states this distinction correctly.

## 3. Evolving-hidden launch and B-clock

The launch proof no longer assumes hidden metadata frozen. Internal moves preserve A,N,B and all phase/counter flags, while the reference connector and seed intensities depend only on A,B. Thus the same reference reward and its excessive envelope are constant across internal hidden jumps. The additional restoring time may be adapted to the hidden path; the pathwise jump-envelope bound and localized excessive inequality do not require it to be an independent exponential clock of fixed rate. On each total-count interval the hidden chain is finite. There is no new hidden explosion between connector jumps.

The physical mean until a terminal fast mark is bounded by Psi/[(A)_a0(b)_q]. Actual activation and immigration compensators then give O(b^(1-q)) and O(b^-q) probabilities before that mark. This is a bounded FACE-MEAN argument, not an unjustified comparison of instantaneous hazards. Conditional seed-versus-clear marking retains its fixed ratio, and restoration only adds successful launch mass. Consequently the correct active mixed Z trial remains available, with its activation treated as up, not neutral. Physical A<a0 stays outside this estimate.

These facts supply the local trace, launch and clock premises of a future carried transfer. They do not by themselves verify a particular complete raw network or its whole phase operator.

## 4. Two-stage potential algebra

For z=E+F, v=1/alpha and u=(1+delta v)/beta, direct evaluation of the killed hidden generator gives

    -Q0 psi0 = alpha v E/z - delta v F/z + beta F(u+v E/z).

At F=0 this is1. At F>=1, beta u-delta v=1 and z>=1 give the asserted lower bound. The bound psi0<=u+v follows from C>=1 and E/z<=1. This allows arbitrary internal reversals before restoration and is not a one-hold surrogate.

At unit rates, psi0=(3E+2F)/[C(E+F)], and

    -Q0 psi0-1 = F(3E+2F-2)/(E+F)>=0

on the entire integer active domain. At one-label states the actual means are3/C from E and2/C from F, matching the witness.

For f(t)=t/(1+ct), concavity including the restoring cemetery value0 gives Q0 f(psi0)<=f'(psi0)Q0 psi0. Therefore

    -(Q0-cI)f(psi0) >= 1/(1+c psi0)^2 + c psi0/(1+c psi0) >=3/4.

The factor4/3 is valid, and the exact residual after scaling is (c psi0-1)^2/[3(1+c psi0)^2]. The transform is bounded by (4/3)min(psi0,1/c), with the c=0 convention stated. Here c is fixed during a hidden face excursion; the proof does not silently allow it to change with internal hidden moves.

At the actual C-born ingress output, the 1/C factor cancels its rate. At the actual a-born output a_out=a+1, c_out=k a(a+1), and the 1/c bound pays its rate kappa_a a. The a=0 event is disabled. Summing these contributions, rather than taking their maximum, gives the required ingress certificate for the displayed channels. Other ingress channels in a full network would still need their own checks.

## 5. Finite certificate format and the limited executable

With denominators fixed and their positivity certified, multiplying by products of actual neighboring denominators leaves linear rational inequalities in numerator coefficients, Psi and C. Nonnegative coefficients are sufficient all-population proofs. A finite dictionary/degree budget is a terminating sufficient search, not a complete synthesis procedure.

An implementation must distinguish potential-formula signatures from the auxiliary 0,1,2,3,4+z refinement used to fix shifted enablement. If formulas are independently assigned to finer cells, it must refine enough to determine the actual output formula as well; it must not evaluate an unknown neighboring cell using the input formula. This is a coding obligation for the proposed generic checker, not a defect in the local generator theorem.

The separate `acquire_face_combinator.py` reconstructs the killed generator from the three specified unit-rate face reactions, enumerates the supplied finite ansatz, and verifies the three active E/F orthants. It finds coefficients(3,2) at candidate19. The two symbolic identities certify the concavity and killing squares; positivity of their denominators is explicit on x,y,c>=0. I reran a copy under /tmp and its JSON matched the frozen output exactly.

This validates that restricted example acquisition/combinator, not an unrestricted face solver: the reaction list and ansatz are supplied in the script. The reported failure of a direct monolithic nonnegative-coefficient cone is compatible with the valid analytic square certificate. A rational potential belonging to a denominator dictionary does not imply that a particular coefficient cone will find it. No failed direct search is counted as success here.

## Final boundary

The bounded killed potential plus SUMMED ingress certificate is a sound local replacement for one-hold trace compensation under the stated structural restrictions. The multi-step witness and regularization are valid. Before any new whole-network/implemented-compiler conclusion, the complete raw model must still satisfy all pool/baseline, ingress, no-B-to-F, activity, weak-reversibility and phase-transfer obligations, and the generic finder must actually be implemented and checked. No broader conclusion or novelty claim is approved by this receipt.
