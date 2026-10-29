# Universal experimental policies: direct predecessors

Date: 2026-10-29. Existing Astra P1 / record_geometry role.

## Finding

The chain from universal action prediction to uniform trajectory domination, polynomial-horizon policy evaluation, and selection of a useful untested policy has a direct primary predecessor. The contextual Dirichlet-half sampler is a causal instantiation whose key domination formula was already available in universal-portfolio work. A matching lower bound for *learning a useful policy*, permitting arbitrary adaptive experiments, is a different statement from the classical domination optimum. I did not establish historical priority for root's lower bound.

The companion `ORDINARY_UNIFORM_POLICY_LEARNING.md` gives an explicit conventional receiver including policies on the boundary of the simplex. It avoids relying on a potentially noncausal generic normalized maximum-likelihood sampler.

## Direct off-policy predecessor

**Peshkin and Mukherjee (2001), _Bounds on Sample Size for Policy Evaluation in Markov Environments_, COLT 2001.** Primary manuscript: <https://arxiv.org/pdf/cs/0105027>.

Read: observation model, action/world likelihood factorization, sampling method, uniform convergence discussion, and §5.2, pp. 10–12. Section 5.2 chooses a sampling policy through minimax logarithmic-loss regret, bounds trajectory likelihood ratios by exponentiating that regret, and invokes Shtarkov and Cesa-Bianchi–Lugosi. For regular parametric classes it gives regret of order `(k_1/2) log T`, hence polynomial likelihood-ratio bounds, and uses this to remove exponential horizon dependence in uniform policy evaluation. The data are experiences from operating an unknown environment. Its general sampler is existential and its regularity/covering assumptions require checking. I do not import its printed precision dependence; the companion proof uses Bernstein directly.

**Peshkin (2001/2002), _Reinforcement Learning by Policy Search_, dissertation.** Primary manuscript: <https://cs.brown.edu/media/filer_public/9b/d2/9bd22737-5b88-470f-a611-50c0bbbf72cf/peshkin.pdf>.

Read: Theorem 6.1 in §6.2, printed pp. 97–98; §6.5, printed pp. 102–105; opening §6.6. Theorem 6.1 has `epsilon^(-2)` precision dependence and linear dependence on a likelihood-ratio ceiling. Section 6.5 repeats the regret-to-exploration construction. Its conclusion conditions polynomial horizon dependence on finding the corresponding optimal sampler, leaving a constructive choice and explicit class constants open. Section 6.6 discusses policy search with uniform confidence bounds. The qualification is constructive specificity, not absence of the conceptual bridge.

## Exact contextual KT predecessor

**Cover and Ordentlich (1996), _Universal Portfolios with Side Information_, IEEE Transactions on Information Theory 42(2):348–363.** Primary manuscript: <https://isl.stanford.edu/~cover/papers/portfolios_side_info.pdf>. DOI: <https://doi.org/10.1109/18.485708>.

Read: Theorems 2–3, their proofs and the Dirichlet integral. One-hot market returns turn portfolio wealth into the product of assigned action probabilities. The Dirichlet-half portfolio becomes KT. The side-information construction runs one predictor per context and gives

\[
\frac{\sup_q\prod_tq(a_t\mid c_t)}{Q_{\rm KT}(a_{1:T}\Vert c_{1:T})}
\le2^S\prod_c(n_c+1)^{(A-1)/2}.
\]

This is an individual-sequence guarantee. It remains valid when the controlled plant generates the contexts, provided each current context is available before the action is selected. The controller, exponent `S(A-1)/2`, and context decomposition are direct specializations. These are closer predecessors than generic predictive-state or reversible-operator methods.

## Exact domination optimum and Fisher volume

**Ordentlich and Cover (1998), _The Cost of Achieving the Best Portfolio in Hindsight_, Mathematics of Operations Research 23(4):960–982.** Primary manuscript: <https://isl.stanford.edu/people/cover/papers/hindsight.pdf>. DOI: <https://doi.org/10.1287/moor.23.4.960>.

Read: Theorem 1, its following remarks, Dirichlet comparison and Shtarkov connection. For a fixed action-string horizon the optimum domination factor is

\[
Z_{T,A}=\sum_{n_1+\cdots+n_A=T}
\binom{T}{n_1,\ldots,n_A}\prod_a(n_a/T)^{n_a},
\]

and

\[
Z_{T,A}\sim
\left(\frac{T}{2\pi}\right)^{(A-1)/2}
\frac{\Gamma(1/2)^A}{\Gamma(A/2)}.
\]

For a multinomial row, `sqrt(det I(q)) = product_a q_a^(-1/2)` in simplex coordinates; integrating it gives the gamma ratio. Thus Fisher volume already describes classical domination cost. This is not an adaptive task-learning lower bound.

**Cesa-Bianchi and Lugosi (2001), _Worst-Case Bounds for the Logarithmic Loss of Predictors_, Machine Learning 43:247–264.** Primary manuscript: <https://cesa-bianchi.di.unimi.it/Pubblicazioni/ml-01.pdf>.

Read: definitions, Shtarkov Proposition 1, mixture Proposition 2 and main-result discussion. The generic normalized-MLE solution is a law on complete outcome strings; computing causal conditionals can be hard. A control application must check what future side information its normalization assumes. Contextual KT avoids that issue.

**Rissanen (1996), _Fisher Information and Stochastic Complexity_, IEEE Transactions on Information Theory 42(1):40–47.** DOI: <https://doi.org/10.1109/18.481776>. Primary institution record: <https://research.ibm.com/publications/fisher-information-and-stochastic-complexity>. Only the primary abstract/metadata were inspected. This is a priority warning, not an uninspected theorem used in a proof. The explicit multinomial constant above is in the inspected Ordentlich–Cover source.

## Reusable trajectories and policy-class learning

**Kearns, Mansour and Ng (1999), _Approximate Planning in Large POMDPs via Reusable Trajectories_, NIPS 1999.** Primary manuscript: <https://papers.nips.cc/paper_files/paper/1999/file/4f398cb9d6bc79ae567298335b51ba8a-Paper.pdf>.

Read: both sampling interfaces and §5. The principal trajectory-tree construction uses strong simulator access. Section 5 also gives a random-trajectory method needing only partially observed histories generated by random actions from the stipulated start. Hidden states need not be observed; this method does not copy a hidden state to obtain multiple futures. It gives uniform restricted-class evaluation with exponential horizon dependence in that construction. It is inaccurate to dismiss the entire paper as requiring microscopic copying.

**Mansour (1999), _Reinforcement Learning and Mistake Bounded Algorithms_, COLT 1999.** DOI: <https://doi.org/10.1145/307400.307437>. Primary institutional record: <https://cris.tau.ac.il/en/publications/reinforcement-learning-and-mistake-bounded-algorithms/>. Author manuscript: <https://www.cs.tau.ac.il/~mansour/papers/99colt1.ps>.

The primary abstract states a reset-and-action algorithm with polynomial horizon dependence and exponential dependence on a strategy-class mistake bound. The PostScript manuscript was not readable through the retrieval interface, so no uninspected internal theorem is relied on. For deterministic fixed-context policies, the elementary mixture over all `A^S` maps already gives horizon-independent domination; the companion note derives that comparator.

## Other directly relevant inspected work

**Shelton (2001), _Importance Sampling for Reinforcement Learning with Multiple Objectives_.** MIT thesis/report: <https://www.cs.ucr.edu/~cshelton/papers/docs/AITR-2001-003.pdf>. Read §§2.3–2.4 and the finite-state-controller discussion. It factors hidden histories into unknown common world terms and known controller terms, discusses physical experience reuse, and distinguishes reusable simulator seeds from ordinary physical data.

**Alexander, Quarel, Du and Hutter (2023), _Universal Agent Mixtures and the Geometry of Intelligence_.** AISTATS paper: <https://proceedings.mlr.press/v206/alexander23a/alexander23a.pdf>. Read agent/environment definitions, Definition 11, and Theorem 14 with proof. It explicitly treats causal controller mixtures in arbitrary history-dependent environments. Extending cancellation beyond a finite Markov hidden state is conventional.

**Li, Munos and Szepesvári (2015), _Toward Minimax Off-policy Value Estimation_.** AISTATS paper: <https://proceedings.mlr.press/v38/li15b.pdf>. Read Theorem 1 and §3.2. It gives finite-sample unknown-reward lower bounds and extends action-space estimation to trajectory-space estimation. Its fixed logging/target setup does not settle root's adaptive policy-search lower bound, but the reward-oracle reduction is established methodology.

**Chandak et al. (2021), _Universal Off-Policy Evaluation_.** Primary manuscript: <https://arxiv.org/pdf/2104.12820>. Read scope, assumptions and the return-distribution statement. Its universality concerns return statistics, not simultaneous coverage of every policy. Its independent-trajectory premise matters for the physical data supplier.

Two further primary abstracts were checked for surrounding scope without treating them as proofs of this construction: Amortila, Foster and Krishnamurthy (2024), _Scalable Online Exploration via Coverability_, <https://proceedings.mlr.press/v235/amortila24a.html>; Krishnamurthy, Li and Sekhari (2025), _The Role of Environment Access in Agnostic Reinforcement Learning_, <https://proceedings.mlr.press/v291/krishnamurthy25a.html>. Their access and function-approximation assumptions differ.

## Research consequence

The upper mechanism and the Fisher-volume exponent for path coverage are classical. The distinct question is matching adaptive learning cost for useful controls; root's actual proof is reviewed separately in `CONTROLLER_COMPLEXITY_REVIEW.md` and its correction receipt.

A worst-case lower bound does not make Fisher volume the cost of every task. Constant rewards, unreachable contexts, finite policy lists and deterministic controls can be easier. Hidden memory is harmless for within-episode cancellation but can defeat cross-episode concentration. Preparation, calls, sensing, random selection, timing and optimization remain actual suppliers. No generic novelty or resolved priority is claimed in this audit.
