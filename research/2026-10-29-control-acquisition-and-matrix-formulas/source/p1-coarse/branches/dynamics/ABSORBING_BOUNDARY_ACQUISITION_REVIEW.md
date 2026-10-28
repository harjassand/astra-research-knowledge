# Independent acquisition and receipt review: observed absorption

## Result and scope

The acquisition, confidence allocation, source-input isolation and resource accounting in `core/absorbing_boundary_compiler.py` pass this review at the frozen hashes below. This review generated **no new trajectories**. An independent exact-arithmetic replay verified all 58 confidence endpoints actually used, six acquisition receipts, the finite matrix certificate inequalities, eleven positive word-interval propagations, and the acquisition preparation ledger.

The substantive advance relative to the prior finite-cap acquisition is real at its stated interface: finite censored first-return observations yield the needed boundary dissipation form without a supplied global source norm gap. The source may have arbitrarily slow, reachable hidden states. The interface must truthfully distinguish **alive outside the boundary** from **irreversibly absorbed**. An ordinary timeout does not supply this distinction.

The infinite-dimensional Schur/resolvent identity and form-domain extension are separately reviewed by the physical and scalar branches. This note establishes the observation-to-certificate and accounting chain and independently verifies the finite certificate arithmetic. It does not replace those form-domain proofs or the already completed Julia-colligation theorem review.

Reviewed results SHA256:

`d76a834b4aa823303d31f9411cdb8604ed5eed43249b2e4da974bcfb385dcdb6`

Reviewed compiler SHA256:

`c63521f8f3c2b59c33a6b668d3081c5be135815fd9ae9b24f821214d7b04a75d`

## What the learner actually receives

The declared source class is a common symmetric substochastic Markov family on a finite or countable state space, with three individually preparable and distinguishable boundary states. Symmetry is in the common counting-measure metric. The observer can report the boundary identity, alive outside, or irreversible absorption without changing the process.

The executable inference was replayed after removing every receipt field except:

- action label, starting boundary label and fixed trial count;
- first-step boundary counts;
- excursion-return-or-pending count;
- even-excursion-return-or-pending count;
- absorption-before-boundary-return count.

The replay disabled the private source constructor and source-fixture function. It reproduced the entire saved certificate exactly. No hidden matrix, dimension, return destination restriction, rate distribution, norm cap, censor horizon or missing-tail model enters inference. The known number of boundary states and action labels are part of the experimental interface, not estimates of hidden state dimension.

The particular backend has one fast state and countably many slow states attached to each boundary state. Its unbounded geometric bit loop selects every slow level with its specified positive probability; there is no sampler truncation. Finite-level calculations appear only in private truth checks, where omitted branch probability is enclosed explicitly. They do not enter the learner or the acquisition trajectories. The call to an older finite fixture in the constructor supplies the boundary matrix; that finite fixture's cap is not a cap for the present infinite source and is not passed into inference.

## Why finite censoring is sound

Fix an action and a starting boundary state. After the first step, stop at the first later boundary hit, observed absorption, or a fixed horizon H. Immediate first-step boundary hits are recorded separately and are not excursion returns. Let E be the event of an eventual excursion return, E_even the event that this return has even total length, and D_H the event that irreversible absorption has already been observed before a boundary return by H. Let U_H mean alive outside at H.

Pathwise,

\[
E\subseteq\{\text{return by }H\}\cup U_H,
\qquad
E_{\rm even}\subseteq\{\text{even return by }H\}\cup U_H.
\]

Also, D_H is contained in the event of no eventual boundary return. Thus the saved positive flags give valid upper estimates of the total and even return masses and a valid lower estimate of boundary loss. A path that remains alive forever is included in U_H at every finite censor time. Eventual absorption is therefore unnecessary for these inclusions.

The finite observations supply bounds for the Schur denominators. Write T for the true boundary kernel, R_+ for all excursion first-return probabilities, and R_- for even minus odd excursion first-return probabilities. For a true row loss κ_j of T+R_+, the observed absorption probability is at most κ_j. On the simultaneous confidence event,

\[
\kappa_+=\max\!\left\{
\min_j a_j^{\rm lo},
\min_j(1-t_j^{\rm hi}-r_j^{\rm hi})
\right\}>0
\]

is a valid lower bound for the smallest eigenvalue of I−T−R_+. Here t_j is boundary row mass, r_j is excursion-return row mass, and a_j is observed absorption probability. Symmetry, nonnegativity and Gershgorin diagonal dominance give this statement. Likewise, using entrywise |R_-|≤R_+,

\[
\kappa_-=\min_j(2T_{jj}^{\rm lo}+a_j^{\rm lo})>0
\]

is a valid lower bound for I+T−R_-. The code's maximum of two rowwise minima for κ_+ is conservative; it does not overstate a gap. The construction can fail to certify positive denominators for another dataset, which is an honest acquisition failure rather than an assumption inserted by the program.

The finite form bound used by the implementation is

\[
L=\tfrac12(\kappa_+^{-1}+\kappa_-^{-1}),\qquad
q=\max_j e_j^{\rm hi}+L(\max_j r_j^{\rm hi})^2.
\]

Given the separately proved Schur identity, this bounds the true Galerkin residual form. A boundary-kernel estimation error of operator norm at most δ then yields the proposed-model bound

\[
q_{\rm proposed}\le (\sqrt q+\delta\sqrt L)^2
\]

with the right-hand side enclosed upward in the saved certificate. The replay checks this enclosure algebraically: if z is the saved upper minus q−δ²L, then z≥0 and z²≥4qδ²L. No floating square root is trusted.

## Confidence coverage and exact acceptance

There are two actions, three boundary starts per action, 2,000,000 trials per start and one fixed inference checkpoint. The horizon is fixed at 32. Within each action, symmetry permits pooling j→k and k→j counts for an off-diagonal entry. Those are equally distributed Bernoulli observations under the declared common symmetric source class. Reusing a known boundary endpoint preserves the trial law by the strong Markov property.

The confidence budget is:

| Quantity | Tails per action |
|---|---:|
| Six distinct boundary-kernel entries, two endpoints each | 12 |
| Three boundary row masses, two endpoints each | 6 |
| Three return, three even-return uppers, three absorption lowers | 9 |
| Total | 27 |

Two actions therefore use 54 tails. The two fresh direct endpoint programs use four more. Each tail has failure probability at most exp(−12); correlations between different counts do not invalidate the union bound. A finite rational lower bound on exp(12) verifies 58 exp(−12)<0.001. The unused upper endpoint of an absorption interval does not enter the simultaneous good event and costs no extra tail.

The original interval routine uses floating point only to propose an endpoint, then accepts an outward rational endpoint through a rigorous lower bound on Bernoulli relative entropy. The independent replay recomputes all 58 inequalities with a separate, longer rational atanh-series logarithm enclosure. It also verifies that every endpoint lies on the correct side of its empirical proportion. Boundary endpoints 0 and 1 are handled as trivial one-sided bounds.

The replay independently checks the model centers, pooled trial counts, entry radii, row-mass radii, κ_+, κ_-, L, q, model-error triangle bound, positive definiteness of I−T_hat², all matrix domination inequalities by every principal minor, structured correction uncertainty, acquired boundary-kernel cap, and true-Galerkin comparator constants. It checks positive word propagation for the nine saved examples and the two comparison-program records. These are verification of saved arithmetic, not additional statistical tests or extra acquisition checkpoints.

## Physical execution and preparation costs

The acquisition stops only at a boundary return, reported irreversible absorption, or H. Every physical update until that stopping point is charged and observed. Early stopping after absorption is legitimate under this new observer interface. It would not have been legitimate for the earlier rank-one membership-only interface, which could not distinguish a dead hidden state from a living one.

For N consecutive trials that all start at boundary j, let C_j be the number that terminate at j and let l_j indicate that the final trial terminates at j. The exact preparation count is

\[
1+\#\{\text{first }N-1\text{ endpoints unequal to }j\}
=N-C_j+l_j.
\]

A trial ending at the requested boundary can start its successor without a physical reset. Ending at another known boundary does not authorize a free change to the requested state. All six acquisition receipts save the final report, so the independent replay verifies this formula exactly. Batch processing does not create extra experimental resets; the batches merely group independent software draws.

| Acquisition resource | Executed and exactly replayed |
|---|---:|
| Logical trials | 12,000,000 |
| Primitive updates | 12,036,469 |
| Categorical observations | 12,036,469 |
| Physical preparations with known-boundary reuse | 1,758,723 |

The fresh direct comparator executes the same two 20-step transport programs from boundary 0 and reads the endpoint. It uses 20,000 logical trials, 400,000 charged updates and 20,000 observations. Absorbed backend trajectories skip redundant software updates but are still charged the complete program length, because this comparator reads only endpoints. Its code reports 13,715 preparations. The saved direct receipts omit the final-boundary bit, so counts alone independently certify the interval **[13,715,13,717]**. This two-preparation metadata limitation has no statistical or scientific effect and is disclosed rather than silently treated as a fully replayed exact count.

The direct comparator certifies a transport advantage in [0.086762476639, 0.147662541929]. It is substantially cheaper for this two-program question than constructing the reusable certificate. The compiler's operational addition is its simultaneous reuse guarantee, not an advantage on a single known pair.

## Accepted conclusions and remaining premises

The saved structured all-word error is approximately 0.0399059846. The stronger same-data positive true-Galerkin route has dynamical remainder approximately 0.00111250454 and certifies the primary transport difference in [0.1080212656, 0.1337115038]. Its interval propagation uses the same measured kernel and return-form bounds. Adopting that stronger classical route retains the newly acquired dissipation information.

The observation and preparation warranties remain source premises: exact boundary states, common symmetry, nonintrusive categorical reports and a truthful irreversible-absorption flag. Their calibration is not supplied by counting scalar observations. The execution is an exact-integer-RNG software experiment, not a laboratory validation. Within those premises, no hidden rank, global relaxation time or source norm cap is needed by the completed acquisition.

Reproduce the independent replay with:

```bash
python astra_p1_successor/branches/dynamics/replay_absorbing_boundary_review.py
```

The saved replay receipt is `ABSORBING_BOUNDARY_REVIEW_RESULTS.json`.
