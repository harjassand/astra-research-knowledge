# Fresh primary applicability check for the fast-connector family

2026-10-30. Reviewer: `producer-workspace/review_chemical_global_foster`.
This is separate from mathematical proof acceptance. **Exact-family novelty remains unverified.**

## Structural facts, not novelty claims

Let c be the number of homogeneous fast composition complexes. The full network has c+2 complexes and one strongly connected linkage class. Pure fast complexes span k-1 conservative composition directions. Connector increments `(1,1)` and `(m-1,q-1)` in the A/B plane have determinant q-m>0. Therefore full stoichiometric rank is k+1 and deficiency is c-k. The system is genuinely rank at least three; `(N,B)` is not a Markov projection because connector rates depend on A.

Single-linkage weak reversibility implies strong endotacticity by the usual finite-graph maximum-face argument; neither is a new graph notion here. Asiphonicity also holds: inflow defeats subsets containing A or B, and a path from mA to any omitted composition species first introduces a species of any remaining proposed siphon without consuming that subset. These properties do not independently prove fixed-volume stochastic recurrence.

## Theorems checked

1. **Ordinary complex-balanced cases really are already covered.** If the fast complex set is only the k pure complexes, c=k and deficiency is zero. Weak reversibility then gives complex balance at every positive rate choice; the product-form theorem supplies the classwise stationary law. Its conditional Poisson tails have all exponential population moments. Additional mixed complexes give positive deficiency, and the family permits non-complex-balanced rates; product form is not automatic for those members. [Anderson–Craciun–Kurtz, primary paper](https://web.math.wisc.edu/~dfanderson/papers/ACKProdFormFinal.pdf).

2. **ACK's strongest general tier criterion fails, not merely its binary corollary.** Theorem 6.1 of arXiv:1904.08967v2 requires top stochastic tiers to lie in top deterministic tiers along every proper tier sequence. Put h=q-m and take `x_n=(nh,0,...,0,B=0)`. Repeating q immigrations and one clearing reaches the next such point from the previous one. Only immigration is active there, so the top stochastic tier is `{0}`. Under x∨1, the unique largest-A-degree complex is `mA+qB`, not zero; the required inclusion fails. Theorem 4.1 also requires binary structure and species singleton/doubleton complexes, absent here. This defeats those sufficient criteria, not recurrence. [ACK, Theorems 4.1 and 6.1](https://arxiv.org/html/1904.08967v2).

3. **ASE large-volume estimates are not fixed-volume Foster bounds.** ACKN Theorem 6.2 couples volume V to concentration through `V>exp(||x||_1)`. Its fixed-volume Theorem 7.2 requires nonempty pure-species degradation families for every species; the present full network has no such nonzero pure-species source complexes. The catalytic complexes mX_i+qB are not pure complexes of the full species set. [ACKN, §§6–7](https://arxiv.org/html/1808.05328v2). ADE Theorem 4.11 likewise uses a volume threshold depending on a bounded concentration radius; increasing the radius while changing the process volume does not prove recurrence of one fixed-rate process. [ADE, primary PDF](https://arxiv.org/pdf/1710.07240v2).

4. **The 2026 first-order theorem's nonlinear extension was checked too.** Xu's Theorem 4.1 requires an actual first-order endotactic subreaction system satisfying (SUB), including a positive linear Lyapunov direction and a common closed class. Here the only possible first-order-source subreaction is the inflow `0->A+B`, which is not endotactic/dissipative; all other sources have order at least two. Independently, every positive linear function has strictly positive drift on the reachable B=0 ray above, so the negative linear Foster conclusion used by (SUB) is impossible there. Thus the nonlinear domination extension is not an automatic replacement for this family theorem. [Xu, arXiv:2601.00176v1, §4, Theorem 4.1 and (SUB)](https://arxiv.org/html/2601.00176v1).

5. **Lower-dimensional results do not become full-rank theorems by projection.** The one-dimensional stoichiometric classification has a one-dimensional hypothesis, while the recent planar bulk criteria still require compatible boundary estimates. Neither directly covers rank k+1>=3, and the non-Markov `(N,B)` projection does not remove the issue. [Wiuf–Xu](https://arxiv.org/abs/2012.07954), [Agazzi–Laurence](https://arxiv.org/abs/2610.31550).

6. **Beware a different meaning of “recurrence.”** Search results for discrete reaction networks can use recurrence to mean the existence of an enabled return path, not stochastic positive recurrence. ACK explicitly warns about this distinction in its discussion of Lemma 3.2. The present proof uses return paths only for closed communicating classes, and separately proves finite expected returns. [ACK, §3.3](https://arxiv.org/html/1904.08967v2).

## Established methods versus the exact application

Stopping-time/embedded-chain drift, Poisson stopped-cost propagation, quantitative fluid approximation, positive-kernel iteration, and uniform-block restart are established methods. The relevant primary comparators include [Laurence–Robert](https://arxiv.org/html/2310.01949v3), [Athreya–Kolba–Mattingly](https://arxiv.org/html/1111.1755v2), [Darling–Norris, §4](https://arxiv.org/pdf/0710.3269), and [Aldous–Fill, §2.4.3](https://www.stat.berkeley.edu/~aldous/RWG/Book_Ralph/Ch2.S4.html). The candidate's actual work is the uniform clearing/reset estimates and coupling of two uncapped physical stopped costs, not invention of those tools.

A fresh targeted primary search did not identify a theorem automatically replacing the full positive-deficiency family proof. That is **not** an exhaustive equivalence or novelty search. An optional full-text opening of the decomposition paper at `https://pmc.ncbi.nlm.nih.gov/articles/PMC8187217/` returned a CAPTCHA; it was not bypassed, and no theorem-scope claim about that uninspected full text is made. The requested primary checks above were completed directly after a separate-agent continuation was unavailable because the agent thread limit had been reached.

No external publication or upload was performed.
