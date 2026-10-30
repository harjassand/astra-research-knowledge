# Independent primary-source scope check

Date: 2026-10-30. Reviewer: `producer-workspace/primary_prior_scope`.
This is a literature-applicability check, NOT approval of the local proof. Primary text was read directly; no prior child verdict was used.

## Verdict

**No checked primary theorem automatically proves the claimed fixed-rate, three-species recurrence or its all-exponential-moment strengthening.** The ASE/strong-endotactic shortcuts are invalid, and the stronger single-linkage tier criterion also fails on an explicit reachable boundary sequence. Conversely, stopping-time drift, Poisson/stopped-cost Lyapunov propagation, and region-by-region stability analysis are established methods. **Exact-network/result novelty remains unverified**, not certified and not refuted by this bounded primary comparison.

## Network facts used in the applicability tests (independently derived)

Species order is `(A,C,B)`. There are six complexes, one strongly connected linkage class, and the vectors `(1,0,1)`, `(2,0,3)`, `(1,-1,0)` are linearly independent. Thus rank is 3 and deficiency is `6-1-3=2`. Highest source order is 7; the network is not binary and has no nonzero pure-species complex.

It is strongly endotactic: a linear functional attains its maximum on a nonempty face of the strongly connected finite complex graph; if it is nonconstant, some edge leaves that maximum set and decreases the functional. It is also asiphonic. Any species subset containing A or B is defeated by `0→A+B`; the only remaining nonempty subset is `{C}`, defeated by `3A+4B→2A+C+4B`.

These facts are not stochastic recurrence proofs. Complex balance at the specified rates is impossible: balance on the leaf-attached reversible chain would force the same positive ratio A/C to equal `1/2`, `1`, and `7`.

## 1. Anderson–Cappelletti–Kim–Nguyen, arXiv:1808.05328v2

[Primary full text](https://arxiv.org/html/1808.05328v2).

Theorem 6.1 establishes a large-volume assumption for ASE networks. Theorem 6.2 supplies negative `L_V U^V` outside a concentration compact set **only when `V>exp(||x||_1)`**. This does not cover `||x||→∞` at fixed V.

The fixed-volume recurrence theorem is **Theorem 7.2**. Besides a strongly endotactic base graph of maximum source order m, it requires, for **each** species i, a nonempty degradation family with sources `a S_i`, `a≥m−1`, and products of total size at most `a−1`; an additional maximum-product/minimum-source size separation is required. Corollary 7.1 is the binary/all-outflows special case. This network has none of the required pure-species degradation sources, and fails that hypothesis regardless of how the base subgraph is selected.

Example 3.2 is explicitly explosive and strongly endotactic. Independently, its inflow and A-to-B production also make it asiphonic, so even ASE does not imply fixed-volume nonexplosion. The paper itself explicitly separates §§6 and 7.

## 2. Agazzi–Dembo–Eckmann, arXiv:1710.07240v2

[Primary PDF, Theorem 4.11, p.12](https://arxiv.org/pdf/1710.07240v2).

Theorem 4.11 proves: there exists b such that, for every concentration radius ρ, a volume threshold `v*(ρ)` makes

`L_v U_a^v(x) ≤ exp(bv)`

hold for `||x||_1<ρ`, `v>v*(ρ)`, and lattice `x∈v^−1 N_0^d`. This verifies Assumption A.1(a), supporting the paper's large-deviation analysis. Proposition 4.17 obtains negativity on an annulus under `v>exp(ρ)`; it does not remove the coupling of volume and accessible radius.

The reviewed network satisfies ASE, so those asymptotic-volume conclusions apply in their stated setting. But neither statement is a negative Foster bound over the entire unbounded state space of one fixed-volume process. In particular, choosing a new v for each large x changes the process; it cannot prove recurrence of the fixed listed-rate chain. No fixed-volume recurrence/moment theorem covering this network was found in this paper.

## 3. Anderson–Cappelletti–Kim, arXiv:1904.08967v2: check the stronger theorem, not just binary scope

[Primary full text, Theorems 4.1 and 6.1](https://arxiv.org/html/1904.08967v2).

Theorem 4.1 requires binary, weakly reversible, single-linkage structure and `C∩{S_i,2S_i}≠∅` for each species; both extra hypotheses fail here.

More importantly, the non-binary analytic **Theorem 6.1** requires `T^{S,1}⊆T^{D,1}` on every proper tier sequence. It also fails here, by the following complete test.

Let `x_n=(n,0,0)`. Every x_n is reachable from zero: four immigrations followed by one clearing send `(n,0,0)` to `(n+1,0,0)` through a finite enabled path. This sequence is proper. At x_n only immigration is active, hence `T^{S,1}={0}`. The D-monomials use `x_n∨1=(n,1,1)`; the unique top complex is `3A+4B`, of order n³. Thus `T^{D,1}={3A+4B}`, and the required inclusion fails. This is an obstruction to applying that theorem, not an obstruction to recurrence.

The same boundary sequence defeats the older Anderson–Kim [arXiv:1710.11263v3, Theorem 4.2](https://arxiv.org/html/1710.11263v3): its top stochastic tier has no source of a descending D-reaction. (Journal numbering differs.)

## 4. Laurence–Robert, arXiv:2310.01949v3

[Primary full text, §2.4 and Theorem 3](https://arxiv.org/html/2310.01949v3).

Theorem 3 restates Filonov's general criterion: an irreducible CTMC, a normlike energy f, an integrable stopping time bounded below by the minimum of its first-jump time and a positive constant, and `E_x[f(X_τ)]−f(x)≤−γ E_x τ` outside an energy sublevel set imply positive recurrence. That is a criterion requiring new estimates, not a graph theorem that already verifies this network.

The introduction explicitly advocates stopping-time rather than one-jump drift to avoid gluing difficulties. Its worked network applications include binary examples, a two-species Agazzi–Mattingly family (Proposition 8), and a two-species bimodal family (Proposition 10). Those generators are not the present rank-three network. Hence random-time/trace recurrence and multiregime stochastic scaling are not new principles here, while this paper does not directly settle the new network.

## 5. Athreya–Kolba–Mattingly, arXiv:1111.1755v2

[Primary full text, §2.1, §9.4.2, Proposition 9.3, Theorem 1](https://arxiv.org/html/1111.1755v2).

The model is a planar diffusion, not a reaction CTMC. Theorem 1 constructs its global super-Lyapunov function. Section 2.1 develops propagation via Poisson equations; §9.4.2, equation (17), represents a local function as expected terminal boundary data plus an expected integral running cost up to a stopping boundary, with finiteness and regularity established before use. Proposition 9.3 formalizes the resulting local solutions; later estimates and gluing produce a global function.

Thus stopped-cost/Poisson Lyapunov construction is established prior methodology. No theorem here identifies or already proves the present chemical-chain result.

## 6. Other obvious dimensional shortcuts

The primary [ConStRAINeD project report](https://constrained.polito.it/publications/) claims general weakly reversible recurrence for **two species**, not rank three. The present network has no conserved linear quantity reducing it to a two-dimensional stoichiometric class. A projection to `(A+C,B)` is not Markov at the physical rates, which retain A-dependence; invoking a planar theorem after projection would require an additional valid theorem and its hypotheses.

The recent [Agazzi–Laurence arXiv:2610.31550 abstract](https://arxiv.org/abs/2610.31550) states planar bulk stability with compatible boundary estimates still needed for positive recurrence; this also gives no direct coverage. This item was scope-checked from its primary abstract, not given a full theorem audit.

## Novelty boundary

The above is sufficient to reject the specific claim that strong endotacticity, ASE/LDP Lyapunov estimates, or the standard single-linkage tier theorems already automatically settle this example. It is **not** an exhaustive literature search and does not exclude another exact-network result, an indirect theorem application, or existing equivalents of the particular finite-head/infinite-tail combination. A correct proof may still be known. Positive recurrence alone also does not establish the claimed all-exponential-population-moment conclusion.
