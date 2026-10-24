# Rank-2 contrast reset: finite-count certificate and closest comparators

24 October 2026. Bounded audit of the frozen rank-2 direct-contrast interface. This note records standard-theorem boundaries and does not claim novelty or comparative advantage.

## What the count bound certifies

Assume the *full controlled Hankel rank* is at most two. Let `p(h)=Pr(G | h)` be a single observable event coordinate, and let two acquired preparation histories `h0,h1` have gap `g=|p(h1)-p(h0)|>0`. Normalization plus `p` then spans the two-dimensional predictive row space. For a fixed legal open-loop macro `u`, its action on this coordinate is affine:

`p(hu) = a_u + b_u p(h)`,

so the directly observed contrast

`Delta_u = p(h0 u)-p(h1 u) = b_u (p(h0)-p(h1))`

measures the only state-dependent slope of that macro. A randomized macro `lambda` with nonnegative weights summing to one has slope `sum_u lambda_u b_u`; the unknown intercept can be arbitrary, since reset requires only that different starting histories become predictively indistinguishable.

For any fixed future adaptive control policy and any event `E` in its future observation transcript, the probability `f_E(h)` is affine in the starting predictive row. Its values at `h0,h1` lie in `[0,1]`, hence its slope in the `p` coordinate is at most `1/g` in absolute value. The post-macro `p` coordinate of any two reachable starts differs by at most `|sum lambda_u Delta_u|/g`, because `p` itself is a probability and ranges in `[0,1]`. Therefore

`sup_{h,h', pi, E} |Pr(E | h; lambda, pi) - Pr(E | h'; lambda, pi)| <= |sum_u lambda_u Delta_u| / g^2.`

Here `pi` ranges over future policies whose action choices depend only on visible future observations (and independent policy randomness). The result is also a total-variation bound on the whole future observation process: rank-two linearity holds for every finite cylinder, and extends to the cylinder-generated transcript sigma-field. It is uniform in future horizon; it does not require a union bound over future tests. It does require the supplied full-rank-two promise and the event `G` to be a complete nonconstant coordinate, not merely a locally separating statistic.

For count data, suppose every Bernoulli mean used to estimate the anchor probabilities and each word's two post-macro `G` probabilities has simultaneous error at most `w`. Then each `Delta_u` error is at most `2w`, and the true gap is at least `g_hat-2w`, where `g_hat=|p_hat(h1)-p_hat(h0)|`. Thus for a data-selected `lambda`,

`epsilon_future <= min(1, (|sum_u lambda_u Delta_hat_u|+2w)/(g_hat-2w)^2)`,

provided `g_hat>2w`. This is valid when the word library was fixed before the samples and the confidence event covers every library word (so `lambda` may be selected by the same-data LP), or when an independent validation batch is used. If `M` Bernoulli means are estimated from `n` independent expensive-initializer trials each, a sufficient Hoeffding radius is `w=sqrt(log(2M/delta)/(2n))`. With a well-separated gap bounded below by `g0`, a near-zero fitted contrast, and target `epsilon`, the count cost scales as `O(log(M/delta)/(epsilon^2 g0^4))` per estimated mean, in addition to macro execution, initializer, and LP costs. There is no certificate if the confidence gap is nonpositive or if the legal positive-mixture LP is infeasible.

The private-word convention is material. The bound is for the reset macro after its word label/random seed and any word-dependent timing are hidden from the future controller; equal-length macros remove timing leakage only. If the future controller sees which macro ran, use the conditional bound word by word, requiring `Delta_u=0` (or its robust analogue) for every supported word. The randomization cannot be described as a reset if its record remains in the future history.

## Strongest nearby primary results

**Single-trajectory finite-sample observable identification.** Balle and Maillard, Theorem 6, give a rigorous single-trajectory spectral/Hankel estimation bound for reactive PSRs under a known finite-state behavior policy, action-exploration lower bound, supplied rank and finite Hankel prefix/suffix basis, and geometric mixing of both the coupled process and normalized reference process. This is the closest finite-sample system-identification comparator. It estimates a Hankel block; its theorem is not an all-future reset certificate, and the paper explicitly leaves full PSR PAC-RL for future work. For the present rank-two interface, direct Bernoulli contrasts avoid reconstructing the full operator matrices. An equally informed OOM/PSR or full-history likelihood learner can nevertheless estimate these same contrasts and solve the same positive LP, so this is a task-directed reduction, not an information advantage. [Balle & Maillard (ICML 2017), Theorem 6](https://proceedings.mlr.press/v70/balle17a.html).

**Output-feedback approximate reset existence and no-reset RL.** The closest theorem to the *reset function itself* is Even-Dar, Kakade, and Mansour. Their Definition 3.1 calls `H` an `(epsilon,k)` approximate reset when the *expected terminal belief* maps every pair of initial beliefs within `epsilon` in `l1`. Lemma 3.1 amplifies this contraction by repetition. Lemma 3.2 proves that a random-walk policy with fictitious stay actions has such a finite mixing time `k` for every connected finite POMDP, by irreducibility and aperiodicity. Since future event probabilities are linear in the terminal state distribution, this is a uniform future-test bound after the homing observation/action history is discarded. Theorem 4.5 then gives near-optimal average reward without reset access, but takes an approximate homing strategy as input and its finite-time cost is polynomial in its system-dependent `K_H` and exponential in the optimal-policy horizon. It does not learn or certify `K_H` from the scalar word-count interface, nor construct a data-driven fixed-length positive mixture. So it *does* establish general existence of an approximate behavioral preparation, while leaving the acquired finite-count certificate and its cost open. Its reset is output-feedback and marginal over the homing experiment; retaining that experiment's record changes the contract. [Even-Dar, Kakade & Mansour (IJCAI 2005), Definition 3.1, Lemmas 3.1–3.2, Theorem 4.5](https://www.ijcai.org/Proceedings/05/Papers/0685.pdf).

**Convex synchronization / randomized words.** Jungers and Catalano, Theorem 3.8, formulate a two-player LP over probability distributions on products from a *known* finite set of binary NZ matrices; Proposition 3.4 says the value reaches one exactly when there is a positive product. This is a close convex/random-word search analogy, but its objective is support-positive synchronization/primitive-set exponent. It is not rank-one cancellation of predictive-state differences, and it supplies no noisy operator acquisition. Exact positive-mixture feasibility for known predictive operators is itself an LP; the unsupplied step here is estimating its constraints with a complete rank/gap bridge. [Jungers & Catalano (2018), Theorem 3.8 and Proposition 3.4](https://arxiv.org/abs/1805.06685).

**Finite-horizon PSR control.** Zhan et al.'s CRANE Theorem 1 gives sublinear regret / a near-optimal finite-horizon policy for a realizable PSR model class with a bounded inverse-core-matrix (`alpha`-regularity) condition, valid PSR dynamics, and a finite bracket-complexity condition. Its bracket definition controls trajectory laws uniformly over policies for the specified finite horizon, making it a strong task-control comparator. It does not output a reusable reset word or a horizon-independent all-future distributional reset certificate. [Zhan et al. (2022), Theorem 1 and Definition 2](https://arxiv.org/abs/2207.05738).

## Older Astra source boundary

The older governing records were checked, not inferred from the recent reset-feasibility obstruction. N189's acquired parity basis is a supplied noiseless parity-block/GF(2) subclass, not a general unknown-HMM or reset-acquisition result. N662 takes rational local CTMC generators, reset hazards, and product reset laws as supplied inputs. N665's acquisition corollary assumes a known hazard-zero pattern and pays for isolated clock probes and forced labelled reset draws, with numerical conditioning floors. These archive claims remain `source_derived_unreviewed`; none implements or certifies the present behavioral reset from scalar word contrasts.

## Comparator conclusion

There is a primary theorem proving approximate all-future behavioral reset existence for connected finite POMDPs (Even-Dar et al.), plus a primary finite-sample theorem for single-stream PSR/Hankel estimation (Balle–Maillard). Neither proves the present combined statement: infer a finite positive word mixture from noisy scalar outcomes, certify its uniform future-event error via the observed rank-two gap, and charge the preparation acquisition. The displayed count bound is a short consequence of rank-two predictive linearity plus simultaneous Bernoulli concentration. An equally informed retaining PSR/likelihood controller can implement the same contrast LP and tie it; no novelty or advantage claim follows.
