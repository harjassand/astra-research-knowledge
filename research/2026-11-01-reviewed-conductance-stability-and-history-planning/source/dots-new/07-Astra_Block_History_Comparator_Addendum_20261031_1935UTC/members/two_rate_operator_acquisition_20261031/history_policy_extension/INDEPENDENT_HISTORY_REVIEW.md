# Independent whole review: block-observation history-policy receiving

## Verdict and exact binding

PASS within the stated mathematical and executable scope. This is a separate extension of the accepted block-Markov comparison, not a silent amendment of its archives. I read the complete proof, README, receiver and all three new diagnostic modules; reread the inherited polynomial receiver at the actual interface; verified every manifest entry; and reran the full receiving operation without changing author sources or saved results.

Frozen manifest: `HISTORY_FREEZE_MANIFEST.json`, 3,583 bytes, SHA-256 `5cdb7d25e8e8f6f40c8bdbec21a3e5e578e6775ff7e3150dde461f57ca42df81`.

Principal sources:

- `PROOF.md`: `fc86f21b7085becca2891690ce31175ab8b0435a9df4b1d42988a3611346f4a4`.
- `receive_history.py`: `d4f93cb8a57df5d461848f87316e5e8babc369cf8ca821affecc3b683ec80dc1`.
- `received_history_results.json`: `7beb256bb34df6a0b7094e156a561027d0902ed98e145c0a46e1dec11dbba00c`.
- `check_history_trees.py`: `24591e20e2241fd8b904ad08b212156597633276202b04d17db764d9723e246b`.
- `check_microscopic_limit.py`: `35b990818240e58cf5a765de450825573f5b9bedcfbde264738c42398a462cbd`.
- `integer_history_trace.py`: `b041dce294215c41ffaa129e70f29bce23908a0ddfa1e1684b85983a65bfa0b1`.

The manifest binds ten new files and five dependencies. In particular it binds feedback manifest `da0208fdba68e98e77da2d4cb25d2e0e5f452928cd7c08554dca213ed7da14fe`, its whole receipt `de32bcd24f3c11e64cc85cb66c29abf600f0baba1da85b405cfae7f2a0111c26`, and actual receiver `444feb3c9906f7a195a7e877b36729907e1bafb14e00f776341e0571c45e1403`. Their previously reviewed acquisition/provenance qualifications remain binding. No new statistical oracle is inferred.

## 1. Policy-tree induction and the important norm factors

Let H=I/n and pi_g=n_g/n. At a history node in block g, each next block h may have its OWN child continuation function f_h. Define the patched vector f by those unrelated functions on their respective blocks. Every coordinate lies in [0,1]. If the local centered norms satisfy ||Q_h f_h||_(I/n_h)<=z, their concatenation q has ||q||_H^2=sum_h pi_h ||q_h||_(I/n_h)^2<=z^2. This is the correct direct-sum argument; it does not substitute one common Markov continuation for a tree.

For the action fixed at this node:

1. The incoming term Q_g A_a P f has local norm at most e_in/sqrt(pi_g), since ||P f||_H<=1 and restriction from the global H norm costs 1/sqrt(pi_g).
2. Each observed block term Q_g C_a[g,h] Q_h f_h has local norm at most sqrt(n_h/n_g) U_gh z. Summing these norms permits completely unrelated child functions.
3. The global observation-error operator contributes at most t z/sqrt(pi_g).

Thus z_next<=c+kappa*z with precisely the constants in the source. Stochasticity also keeps each new true value in [0,1], giving the conservative local residual bound one. Taking min(1,c+kappa*z) is therefore valid, including kappa>1 and c>=1. No spectral contraction of feedback or of tree continuation has been assumed. The local variance could be bounded more sharply, but that is not needed for this certificate.

For the block-average error, (W A_a Q)[g,:] q is bounded by e_out*z in the dual H norm. Replacing the true coarse row by B_a costs at most d for block averages in [0,1]. Stochastic B_a propagates unrelated child errors by their maximum, not their sum. This proves E_(j+1)<=E_j+d+e_out*z_j and E_history=L*d+e_out*sum_{j<L}z_j.

These are counterfactual functions on every state of each block, even if a particular history has zero probability. Intermediate uniform block averages are algebraic devices, NOT assertions about the true conditional microscopic distribution. Only the original block-uniform initial law is averaged to recover the actual payoff. There is no division by history probability and no rare-history posterior guarantee.

Independent private randomness can be fixed first, giving deterministic trees, and averaged afterward. The same deterministic operator event bounds all trees and compatible block rewards simultaneously, including policies selected after acquisition. This does not enlarge the confidence guarantee to postselection on a rare PASS event or authenticate sample/probe independence.

## 2. Planning consequence and limitations

Ordinary finite-horizon Bellman induction on the coarse stochastic MDP is optimal among its history-dependent randomized policies. Consequently, for a true history competitor pi and the implemented coarse Markov optimizer pi_hat:

    V_true(pi) <= V_coarse(pi)+E_history
               <= V_coarse(pi_hat)+E_history
               <= V_true(pi_hat)+E_history+E_chosen.

The tighter already-received Markov certificate may be used for E_chosen because it concerns the SAME implemented policy and is valid on the same received operator event. No minimization over uncertified statistical events is occurring. The alternative 2E_history bound also follows.

This compares against all block-observation/action-history policies but does not solve a general POMDP, compute beliefs, implement a history tree, allow microscopic actions, or acquire a new physical sensor. The implemented policy remains the existing time-dependent block-Markov table. The exact four-state example correctly gives every one-step block-history policy value 1/2 but microscopic feedback value 11/20. Thus even a zero one-step history error cannot justify microscopic-policy optimality.

## 3. Actual receiver, external task binding and arithmetic

The callable API requires caller-supplied reward mask, initial numerator mask and denominator. It checks their exact values against the separately pinned original artifact, checks genuine integer mask entries and denominator, and binds horizon 24, two actions, confidence 1/1000 and a separately requested positive history tolerance. The prototype deliberately rejects new reward/initial tasks rather than silently claiming a generic new-task frontend. `fixture_task()` supplies the public task from the independently hash-pinned original artifact for the CLI.

The initial constants calculation is a cheap refusal/preflight only. A PASS is unavailable until `old.run()` replays the full accepted sample/probe and packed-interface arithmetic, reconstructs U from all 32 certificates, and checks all source/model/task bindings. The history receiver compares before/after model and local-record bytes and recomputes its constants after successful receiving. The local JSON comparison matrix is not trusted merely because its preflight error is small. Existing immutable source/dependency access and assertions-enabled typed API conventions remain necessary; this is not a hardened arbitrary-file/concurrent-attacker service.

The fine propagated bound used here equals the accepted L times the coarse row-error radius. The local history c uses the original per-action incoming estimate, not the larger row-selected Markov estimate, which is correct: a single action is selected at each particular history node. Outward rational square roots only enlarge the bound.

The integer backend's common denominator D includes c, kappa, e_out and the whole fine bound. If z=znum/den, it computes cnum*den+knum*znum at denominator D*den, caps by that denominator, and rescales the accumulated prior z sum consistently. Its final multiplication by e_out and addition of the fine term exactly reproduce the rational recurrence. Lcm formation, comparisons, gcd, reading and serialization remain additional costs.

## 4. Executed checks and reproducibility

All 15 manifest entries were hash/size checked, including the five exact dependencies. Full nonmutating receiving was executed with output only in `producer-workspace/history_reviewer_received.json`. Every saved non-timing output field matches `received_history_results.json` exactly.

Executed author checks:

- Full inherited receiving: 9,806 exact checks and 12 inherited preflight refusals.
- New history interface: 11 expected refusals.
- Exhaustive small history trees: 1,132 exact checks.
- Microscopic scope counterexample: 11 exact checks.
- Common-denominator recurrence: 25 exact checks.

Additional independent checks:

- 480 exact tests of counterfactual trees with unequal three-block partitions, three actions, independent randomized choices at different nodes, nonzero observation and coarse-model errors, and deliberately noncontractive kappa with eight capped steps. Saved separately as `REVIEWER_EXTRA_HISTORY_CHECKS.py` and `reviewer_extra_history_checks.json`; these do not alter the freeze or replace the proof.
- 18 task/type/alias refusals, including bool/float mask aliases, shortened/extended masks, invalid denominators, and bool/float horizon/action/tolerance/confidence substitutions. These were run against the actual receiver's preflight, not a weakened replica.

No defect or source correction was required in this new frozen extension. Diagnostics are proof checks on constructed cases, not evidence that synthetic counts have authentic physical iid provenance.

## 5. Result and honest cost

The received fixture gives:

- kappa approximately 1.0314396616974182; contraction below one is not claimed.
- E_history = 0.04210299756104081.
- E_chosen = 0.014402306334221847.
- Regret against all admitted block-history policies <=0.05650530389526265.

The new requested VALUE tolerance is 0.05. This is neither an epsilon=0.02 history certificate nor a regret<=0.05 statement. The original Markov task remains unchanged.

No new source observations or norm probes are needed for the deterministic implication. Nevertheless, actual receiving repeats 279,363,350 norm integer products and 768 Bellman products. The 99 integer recurrence products, 78-bit common denominator and 1,948-bit measured peak are only the new scalar recurrence cost. Original 3,298,951,680 represented calls, failed rounds and historical acquisition work remain paid. Synthetic aggregate sampling is not equivalent to having executed billions of physical calls. The original 2,060-byte packed map/policy/task interface and 468-byte coarse model remain; proof comparison against history trees does not require storing those trees.

The certificate can be consumed by equally informed ordinary retained-model/Bellman methods. This review establishes the particular uniform policy-tree implication and its receiving, not historical novelty, universal planning efficiency, practical superiority, or impossibility of a stronger ordinary comparator. It does not extend any physical control/sensor interface.
