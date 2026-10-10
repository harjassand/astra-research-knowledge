# Positive replicas, global gluing, and a quantitative same-set gate

Date: 2026-10-10. Natural logarithms throughout.

## Status

This investigation does **not** prove an exponential sunflower bound or remove the logarithmic loss. It obtains a sharp, positive, marginal-preserving one-coordinate coupling primitive, an exact mixed-marginal feasibility test, and an infinite structural obstruction to charging global gluing by local information. It then makes a quantitatively charged attempt at the genuinely global same-set-hitting route. That attempt identifies an additional unresolved step, rather than declaring generic reverse hypercontractivity applicable.

A subsequent positive result is preserved separately in `KERNEL_SECTOR_PRIMITIVE.md`: an exact, polynomial-time global coupling with pointwise density cost at most 4^w for full binary latent-product projection models, and (9/2)^w for arbitrary uniform latent alphabets. This handles overlapping deterministic copies without a total-correlation charge. It requires the full latent-product support and injective subtuple recodings; a general acquisition theorem is not proved, and a fixed-rank obstruction rules out acquiring this exact class by retaining a constant fraction of every family. The general additive-code extension remains unresolved; the root record separately proves the native additive rank-at-most-two subcase.

The local results below are proved here; priority or novelty is not asserted. They are not evidence of a solution by themselves. No alphabet folding, coordinate erasure, or new small-instance optimization was used.

Two further boundary notes are preserved. `GLOBAL_DUALITY_BOUNDARY.md` applies the known Rota Bulò–Pelillo hypergraph polynomial theorem (2009) to show that the universal marginal-coupling KL bound is exactly equivalent to the sunflower independence bound; it is not promoted as a new mechanism. `LINEAR_KERNEL_EXTENSION_BOUNDARY.md` proves that a constant-codimension F_4-linear difference-support construction cannot extend unchanged to arbitrary high-rank binary output blocks, even for one identity block. Nonlinear global acquisition remains unresolved.

`MIXTURE_ACQUISITION_TEST.md` extends supplied component couplings by an exact entropy identity. The same projective-plane construction rules out low-information mixture acquisition for this exact model class, even with overlapping components. The identity exposes an additional possible cancellation term, but no general theorem controlling it is proved.

The final supplied-input closure statement is `MIXED_ALPHABET_PRIMITIVE.md`: arbitrary binary additive blocks can be combined with independent uniform nonbinary latent subtuples under injective tuple recoding, at pointwise coupling cost at most 16^w. This uses the separately preserved additive result derived from Brouwer's 1986 subspace-cover theorem. The purely binary combination adds no class beyond additive codes. None of these supplied-input statements acquires a representation for an arbitrary family.

**Closing conclusion.** The strongest explicit construction developed in this branch is the exact kernel-sector global coupling for supplied latent-product projections, with exact rational arithmetic and cost independent of alphabet size, hidden dimension, and deterministic copies. The broader binary additive theorem is preserved in the separate additive branch and yields the final mixed-alphabet closure above. Priority of the kernel-sector construction is not established. General nonlinear adaptive-reference acquisition and the quantitative same-set exponent 3+O(1/log q) remain unproved. Known hypergraph polynomial duality prevents mistaking an entropy reformulation for a solution. All permitted verification scripts in this branch have been rerun successfully; no external publication, contact, paid job, or repository push was performed.

## 1. Exact relation and information cost

For an alphabet A, let T(a,b,c) be 1 when a,b,c are all equal or all distinct, and 0 otherwise. Equivalently,

    T(a,b,c) = 1 - 1[a=b] - 1[a=c] - 1[b=c] + 3 1[a=b=c].

For a distribution P on a partite code F contained in A_1 x ... x A_w, define I_SF(P) as the minimum of D(Q || P^3) over couplings Q with all three row marginals P and with T(X_i,Y_i,Z_i)=1 for every coordinate. The diagonal coupling always makes the feasible set nonempty.

If F is sunflower-free and its rows are distinct, every admissible ordered triple is diagonal. This includes triples with exactly two identical rows: they fail T at a coordinate where the third row differs. Consequently

    I_SF(P) = 2 H(P).

In particular, for uniform P on N rows, I_SF(P)=2 log N. A universal I_SF(P)<=Cw would be a substantive theorem, not an automatic entropy chain rule.

## 2. Sharp positive local coupling theorem

**Theorem.** For every finite-alphabet probability distribution p, there is a coupling Q of three copies of p, supported on T=1, such that

    D(Q || p^3) <= log 4.

The constant is sharp: when p is uniform on two symbols the only allowed triples are diagonal, and the cost is 2 log 2.

### Proof

For a probability vector u, put

    Phi(u) = sum_{a,b,c} T(a,b,c) u_a u_b u_c
           = 1 - 3 sum_a u_a^2 + 3 sum_a u_a^3
           = 1 - 3 sum_a u_a [u_a(1-u_a)].

Since u_a(1-u_a)<=1/4 and sum_a u_a=1,

    Phi(u) >= 1/4.                                      (1)

Restrict to the support of p. Maximum entropy over the T-supported couplings with marginal p has the usual finite-dimensional entropy dual. Averaging the three dual potentials is permitted by permutation symmetry and convexity, so a common potential suffices. Therefore

    min_Q D(Q || p^3)
      = sup_{u>0, sum u=1} {-3 D(p||u) - log Phi(u)}
      <= log 4.

There is no hidden positivity assumption: the primal is a probability coupling. Strong duality follows, for example, by putting sufficiently small positive mass on every allowed triple and completing each marginal with positive diagonal mass. This gives a relative-interior feasible point whenever p is positive on its support. Zero entries were removed first.

### Constructive form and cost

At an entropy optimum, the coupling has the form

    Q(a,b,c) = T(a,b,c) u_a u_b u_c / Phi(u),

where u is chosen so that the marginals equal p. It can be found from a convex optimization in q dual variables:

    minimize_lambda log(sum_T exp(lambda_a+lambda_b+lambda_c))
                    - 3 sum_a p_a lambda_a.

The scalar partition function and its gradient can be evaluated in O(q) arithmetic operations using sums of the first three powers of exp(lambda). Numerically stable implementations should not rely on subtracting nearly equal large terms. Once u is known, draw three independent u-labels and reject exactly-two-equal outcomes. Equation (1) guarantees at most four trials in expectation.

This is an explicit finite-dimensional operation, not a polynomial-time sunflower algorithm. Exact real arithmetic or certified approximation of the optimization is needed for an exact marginal claim. With floating-point optimization, marginal residuals and objective certificates must be checked; no iteration or bit-complexity bound independent of the input probabilities is claimed here. Listing all Q entries takes O(q^3) space, but rejection sampling avoids that list. Only the supplied distribution p is needed; no external service or paid computation is involved.

## 3. Different conditional marginals: an exact feasibility test

Let p_1,p_2,p_3 be three distributions on the same alphabet. Write

    s_a = p_1(a)+p_2(a)+p_3(a),
    m_a = min_j p_j(a).

An admissible T-supported coupling exists **if and only if** there are nonnegative numbers t_a and T_0=sum_a t_a such that

    t_a <= m_a,
    s_a - 3 t_a <= 1 - T_0                 for every a.  (2)

Here t_a is the probability of the all-equal triple (a,a,a). After removing it, each replica has residual mass 1-T_0, and the sum of residual probabilities at any label must not exceed 1-T_0, since an all-distinct triple uses a label at most once. This proves necessity.

For sufficiency, the residual 3-by-q matrix, divided by 1-T_0, has row sums one and column sums at most one. It is a fractional matching in the complete bipartite graph with three replica vertices. The bipartite matching polytope is integral, so it is a convex combination of injections from the three replicas into the alphabet. These injections give the all-distinct component; add back the diagonal masses t_a. The case T_0=1 is purely diagonal.

Thus feasibility is an explicit linear program with q diagonal variables, followed by a bipartite matching decomposition. In particular, s_a<=1 for all a gives an all-distinct coupling, while (delta_a,delta_a,delta_b), a!=b, is infeasible. This is why different conditional histories cannot be ignored in a sequential gluing argument.

## 4. Infinite global obstruction to an additive local-information budget

This is an asymptotic incidence construction, not a search for another small counterexample.

Let q=2^m with m>=2. The 2q rows are indexed by (b,h) in F_2 x F_2^m. There is one coordinate for each nonzero d in F_2^m, hence w=q-1. At coordinate d, partition the rows into the pairs

    {(b,h),(b,h+d)}.

The symbol is the pair containing the row. Each coordinate has exactly q symbols, each occurring twice, so every one-coordinate marginal of the uniform row distribution is uniform on q symbols.

The rows are distinct as codewords: rows with different b never agree; distinct rows with the same b agree only at their difference coordinate. Since there are at least three coordinates, they cannot agree everywhere.

Every triple of distinct rows contains two with the same b. Their difference d is nonzero, and coordinate d places exactly these two in a common pair block, with the third outside it. Hence the family is sunflower-free.

Put D_q=q^2-3q+3. On a uniform q-symbol marginal, the uniform distribution on the qD_q allowed triples has all three marginals uniform and maximizes entropy over its support. The exact optimal local cost is therefore

    ell_q = log(q^2/D_q).

For the constructed family,

    sum_i I_SF(P_i) = (q-1) log(q^2/D_q) -> 3,
    I_SF(P)         = 2 log(2q) -> infinity.              (3)

Thus there is no universal multiplicative constant K for an inequality

    I_SF(P) <= K sum_i I_SF(P_i).

Even replacing KL by any fixed Renyi divergence does not repair this test. For uniform marginals the optimal local coupling is uniform on its allowed support, and its likelihood ratio against p^3 is constant there; its divergence is ell_q for every Renyi order, including 0 and infinity. The unique global coupling likewise has constant likelihood ratio N^2 and divergence 2 log N for every order.

This **does not refute** a Cw budget: here log N=O(log w). It says precisely that a valid global correction must detect coordinate incidence, not merely sum vanishing one-coordinate entropy costs. Conversely, the usual total correlation sum_i H(P_i)-H(P) is about q log q on this example, far larger than the necessary global cost O(log q). Charging all dependence naively is also badly inefficient.

## 5. The explicit correlated space is spectrally very weak

Let rho_q be uniform on the qD_q valid triples. All marginals are uniform. The conditional pair kernel has the nonconstant eigenvalue

    lambda_q = (3-q)/D_q.

More importantly, the maximal correlation between one replica and the other two is exactly

    rho_max(rho_q)^2 = 3/D_q.                            (4)

To verify (4), take a mean-zero function f with uniform second moment one. Conditional on Y=Z=a, X=a. Conditional on distinct Y=b,Z=c, X is uniform on the remaining q-2 labels and

    E[f(X)|Y=b,Z=c] = -(f(b)+f(c))/(q-2).

The equal case contributes 1/D_q to the second moment. Using

    sum_{b!=c}(f(b)+f(c))^2 = 2(q-2) sum_b f(b)^2,

the distinct case contributes 2/D_q. Every nonconstant direction has the same singular value, proving the formula. Thus rho_max<1 for q>=4 and is asymptotic to sqrt(3)/q. On the construction in Section 4,

    sum_i rho_max(rho_q)^2 = 3(q-1)/D_q -> 0,

although global coupling information diverges. An additive squared-correlation budget therefore cannot replace the missing incidence-sensitive correction either.

## 6. A genuinely sufficient quantitative same-set inequality

For F contained in [q]^w, put delta=|F|/q^w. A sufficient global analytical statement is

    E_{rho_q^w}[1_F(X)1_F(Y)1_F(Z)] >= delta^{p_q},
    p_q = 3 + c/log q,                                  (5)

with c an absolute constant, at least for all sufficiently large q. Small alphabets can be absorbed into an absolute exponential base.

Writing V(F) for the number of valid ordered triples, (5) gives

    V(F) >= |F|^{p_q} (qD_q/q^{p_q})^w
          >= |F|^3 [e^{-c} D_q/q^2]^w.

For q>=3, D_q/q^2>=1/3. Thus V(F)>=|F|^3/(3e^c)^w. On a sunflower-free family V(F)=|F|, giving |F|<=(3e^c)^{w/2}. The standard rainbow-partite reduction would then give an exponential bound for general uniform set families.

Equation (5) is an unproved gate, not a newly established inequality. Merely calling its optimal exponent a tensor capacity would rename the problem. A useful proof must exploit additional structure of rho_q.

### 6.1 Exactly charged high-density restriction

There is one rigorous piece of the proposed high-influence reduction. Fix an exponent p>3 and define

    kappa = q/(qD_q)^{1/p}.

If a restriction of k coordinates to a word a contains a fraction r_a of F, its residual density is delta_a=delta q^k r_a. Pinning those k coordinates diagonally in all three replicas has probability (qD_q)^{-k}. Therefore, if the residual family satisfies the exponent-p bound and r_a>=kappa^{-k},

    hit(F) >= (qD_q)^{-k} delta_a^p >= delta^p.           (6)

This accounts for the entire diagonal-pinning cost. Consequently, a minimum-dimension counterexample to the exponent-p same-set bound must satisfy

    Pr[X_S=a | X in F] < kappa^{-|S|}

for every nonempty coordinate restriction. For p=3+c/log q, kappa tends to e^{c/3}. Thus the exponent budget permits only a constant-spread regularization, not arbitrarily strong resilience for free.

### 6.2 Why this does not directly produce a low-influence family

Fix an integer k>kappa and consider the rare product box F=[k]^w inside [q]^w, q>k. Every s-coordinate nonempty fiber has conditional mass exactly k^{-s}, so no restriction meets the charged threshold in (6). Nevertheless, for f=1_F with delta=(k/q)^w, its ordinary coordinate influence is

    Inf_i(f) = E[Var(f | all coordinates except i)]
             = delta(1-k/q).

Every influence divided by Var(f) tends to one as q grows (with a sparse box). In particular, these influences are much larger than a threshold of the form delta^C for C>1. The family is highly structured and harmless, but it is not the low-influence case required by a direct invariance argument. Constant spread alone does not justify that invocation.

This is a decisive obstruction to the **specific** two-branch proof architecture “charged heavy-fiber pinning or apply a low-influence theorem.” It is not a counterexample to (5), to all forms of smoothing, or to a more sophisticated high-influence reduction. An additional step must recognize rare product structure or change the reference marginals without losing control of global gluing. The local coupling theorem handles an isolated rare alphabet at constant cost, but Section 4 shows that summing those costs does not solve the global problem.

### 6.3 Why the Gaussian exponent alone cannot be the answer

The weak correlation in (4) suggests a Gaussian exponent 3+O(1/q) in a genuinely low-influence regime. It cannot be the general exponent. Embedding the previously preserved 12-row, rank-three sunflower-free code into [q]^3 gives

    hit(F)=12/(qD_q)^3,
    delta=12/q^3.

Any exponent valid for all F must satisfy

    p_q >= 3 + [(2/3) log 12]/log q + o(1/log q).

Thus an O(1/log q) rare-alphabet correction is genuinely necessary. This uses the earlier established certificate; no additional small search was performed.

## 7. Current primary literature check and boundaries

The mechanism was made explicit before the targeted same-set literature check.

1. Jan Hazla, Thomas Holenstein, and Elchanan Mossel, **Product Space Models of Correlation: Between Noise Stability and Additive Combinatorics**, Discrete Analysis 2018:20, arXiv:1509.06191v3. Their theorem applies when the full one-versus-the-rest correlation is less than one. Section 9 states that the general quantitative bound is triply exponential in inverse density; its polynomial same-set result is for symmetric two-step distributions. In view of (4), qualitative same-set hitting applies to rho_q for q>=4. It does not supply (5).
   - https://arxiv.org/abs/1509.06191
   - https://arxiv.org/html/1509.06191v3 (Sections 3, 5, and 9)
   - https://doi.org/10.19086/da.6513
2. Elchanan Mossel, Krzysztof Oleszkiewicz, and Arnab Sen, **On reverse hypercontractivity**, arXiv:1108.1210. This is adjacent machinery, not a license to assert a three-function inequality for a distribution with forbidden triples.
   - https://arxiv.org/abs/1108.1210
3. Sankeerth Rao Karingula and Shachar Lovett, **Limitations of the slice rank method in additive combinatorics**, ECCC TR26-205, September 22, 2026. Its advertised sunflower obstruction is for k>=4; it does not by itself close this three-petal positive-coupling question.
   - https://eccc.weizmann.ac.il/report/2026/205/
4. Anup Rao, **The story of sunflowers**, JLMS 2026, provides a current primary-author survey of the general problem.
   - https://londmathsoc.onlinelibrary.wiley.com/doi/full/10.1112/jlms.70380

Targeted searches as of 2026-10-10 did not surface a later primary theorem giving the required three-step exponent with the necessary q dependence. That is a bounded literature search, not a certification that no such result exists. AI-generated claimed sunflower proofs were not audited or used.

## 8. What remains worth pursuing

The surviving global obligation is an incidence-sensitive, rare-structure-aware proof of (5), or an explicit marginal-preserving operation with cost O(w). The exact local positive sampler, feasibility test, pinning charge, and spectral formula are available. The missing theorem is a global correction that simultaneously avoids:

- summing tiny local divergences, which undercharges the incidence construction;
- charging all total correlation, which overcharges that same construction;
- treating constant spread as the low-influence hypothesis;
- invoking a three-function reverse inequality despite forbidden local triples.

No such correction is proved in this pass. These tests narrow a global mechanism; they are not themselves a transformative combinatorial primitive.

## 9. Reproduction

Run `python independent_programme/global_sunflower_20261010/verify.py` from the workspace root. The verifier uses only the Python standard library. It checks the explicit code construction and all its triples for q=4,8,16, verifies the cubic identity and lower bound on sampled rational distributions, verifies the correlation formula directly on several alphabets, and records asymptotic accounting values in `verification.json`. The asymptotic and entropy claims are proved above, not inferred from those computations.

Run `python independent_programme/global_sunflower_20261010/verify_kernel_sector.py` for the exact rational kernel-sector checks. That script verifies the global positive primitive, not a general sunflower theorem.

## 10. Additional exact formulas retained from the discussion

### Finite holomorphic cubature: a clue, not positivity

Let U be uniform on the complex cube roots of unity. Choose real a,b with ab=-1/2 and a^3+b^3=3, and put Z=1+aU+bU^2. Such a,b exist: a^3 and b^3 are the two real roots of t^2-3t-1/8, whose product is -1/8. Direct expansion gives

    E Z = 1,
    E Z^2 = 1+2ab = 0,
    E Z^3 = 1+6ab+a^3+b^3 = 1.

Use independent Z_{i,label} and S=sum_{x in F} product_i Z_{i,x_i}. Then E S=|F|, E S^2 counts ordered pairs differing in every coordinate, and E S^3 counts valid ordered triples. Thus E S^3=|F| on a sunflower-free family. These are holomorphic moments; E|S|^3 is different, so Jensen or a positive third-moment argument is not available. The positive coupling theorem in Section 2 avoids this sign issue but does not automatically globalize.

### Local three-function formula

For uniform alphabet averages, write mu_f=E f and similarly for g,h. Directly from T,

    E_{rho_q} f(X)g(Y)h(Z)
      = [q^2 mu_f mu_g mu_h
         - q ((E fg)mu_h + (E fh)mu_g + (E gh)mu_f)
         + 3 E fgh] / D_q.

For three centered functions only (3/D_q) E fgh remains. For a common indicator of k labels the accepted mass is

    [k(k-1)(k-2)+k]/(qD_q).

This formula confirms both the weak pair coefficient and the indispensable three-way dependence. It does not give a three-function reverse inequality: functions supported on a,a,b with a!=b have positive individual means and zero joint acceptance.

### Additive rank-at-most-two gate, recorded with attribution to the root derivation

For jointly injective F_2-linear maps L_i:F_2^m -> F_2^{r_i}, r_i<=2, injectively identify each output with an F_2-subspace of F_4. Extend its coordinate functional F_4-linearly to F_4^m, forming a w-by-m matrix M. If z=u+omega v lies in ker M, then L_i(u)=omega L_i(v), so every block is either zero in both vectors or gives three distinct values in (0,L_i(u),L_i(v)).

Sample z uniformly in ker M and an independent uniform a in F_2^m, and output a,a+u,a+v. This is a marginal-preserving, globally admissible coupling with pointwise density ratio 4^{rank_F4 M}, at most 4^w. Its computation is finite-field Gaussian elimination. If the support is sunflower-free, m<=w follows. Rank greater than two is not covered: a map into F_4 then has a kernel, and a hidden nonzero block direction can survive while its F_4 image is zero. Random F_4 functionals annihilate any fixed nonzero vector with probability 1/4, whether the projected pair originally had rank one or rank two; that naive randomization does not distinguish bad pairs.

The independent root code and its exact/sampled gates are under `independent_programme/root_additive_sunflower_20261010`. Computations there are evidence for the stated finite tests, not a proof for arbitrary block ranks.
