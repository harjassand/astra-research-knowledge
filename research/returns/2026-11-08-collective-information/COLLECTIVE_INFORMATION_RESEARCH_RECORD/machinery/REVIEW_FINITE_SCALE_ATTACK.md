# Source and scope review of the finite-scale certificate attack

7 November 2026. Independent machinery review. No principal or constructor source file was edited.

## Pinned object and verdict

Reviewed final object: `../constructor/FINITE_SCALE_CERTIFICATE_ATTACK.md`.

- Bytes: **19757**.
- SHA256: **`42c53622d2c35a86d8acac1bc12a82bd6f31bcdb2e1269033dbc78067bf230a1`**.
- Primary source: [Funaki–Gu–Wang, 2404.12234v3](https://arxiv.org/html/2404.12234v3), cached HTML SHA256 `18350f0690e9bb0bb58ce3068f3407b752edc6c98dafc84ccb16b7c5d53252d2`.

**Verdict: PASS for the stated additional finite operations, after correction of the initial exterior-pattern objection.** The construction supplies a succinct deterministic admissible corrector, an observed all-density constitutive-residual certificate, a uniform finite-block canonical variance assay in one dimension at fixed bare range, and the stated stationary-reference spectral/entropy pressure bound. It does **not** supply a complete effective finite-N prediction theorem, arbitrary-force theorem, physical apparatus validation, priority or measured advantage.

The first object read was 14045 bytes, SHA256 `4daed6e4b7a1157fb38fbf3ff4382efc772c632201e5b64b7a42f5b0c708b758`. It incorrectly suspected that the exterior needed by the canonical H observable grows with corrector radius. Both reviewers checked source (6.78); the constructor corrected this in the pinned final object. The failed objection and the precise repair are retained below. The present verdict does not apply to later substantive changes.

## 1. Admissibility and source construction

The closed dual optimizer used for the coefficient lower bound is not automatically an admissible interior corrector for the stationary variational formula. Its domain is the full closed issued-bond graph `Lambda^+`, and it can depend on outside rates/count labels. Membership in `F_0(Lambda^-)` does not follow from a scalar primal–dual gap or an infinity bound. The SSEP path example in the attack correctly exposes that support distinction; a special gauge cancellation in SSEP is not a general conversion theorem.

The replacement uses the correct source objects:

- Source **(6.1)**: the density-dependent **primal** corrector `phi_(rho,Lambda,xi) = v(rho,Lambda,xi)-ell_xi`, supported in `Lambda^-` with its specified centering.
- **(6.34)–(6.36)**: sum the interior small-cell translates at the large-interior empirical count, clamped away from zero and one. Both spatial truncation and density clamping are present. The empirical count is computed from input bits, so the glued function is density-free and supported inside the large cell.
- **Proposition 6.7**, especially **(6.37)**: this specific glued candidate has a density-uniform finite-cell energy excess tending to zero algebraically. In dimension one, small side `ell` is of order `b^(1/12)` and clamp `a` of order `b^(-1/6)`, where `b` is the large side. The source proof explicitly tracks this shrinking cutoff; this is not a fixed-cutoff result being extrapolated.
- **Lemma 6.8(3), (6.70)**: for every admissible interior function, division by the large volume and the translation/Jensen estimate turn its finite-cell energy bound into a stationary translated-corrector energy bound.
- **Proposition 6.9**: identifies the finite-cell conductivity limit with hydrodynamic conductivity. This identification is needed to call the resulting residual `c(rho;F)-c(rho)`.

The source proposition defining an optimizer of the minimax problem (6.32) is not a requirement to solve that new optimization numerically. The explicit candidate from (6.34), its bound (6.37), and the arbitrary-function inequality (6.70) suffice. The attack correctly uses that route.

The succinct approximation does not have to inherit the exact norm estimate of the special corrector in source Proposition 7.1. Its own measured/programmed radius and proven supremum bound must instead be used in every later finite-N term. The attack retains those quantities.

## 2. Shared seeds really define a finite local function

For each permitted density `p`, the open primal corrector has the representation

`f_p(x) = integral_0^infinity E_x[j_p(X_t)] dt`.

The open chain is the exact source-matched primal chain, not the closed dual chain. In one dimension, an explicit gap lower bound is `g_0 = a^2/(12 ell^2)` and `|j_p| <= J = lambda ell`. Product minimum mass satisfies `pi_min >= a^ell`. Thus, for any desired absolute corrector error `e_f`, the truncation time

`tau >= g_0^(-1)[(ell/2) log(1/a) + log(4J/(g_0 e_f))]`

has a uniform tail at most `e_f/4`, after taking a nonnegative logarithm/maximum with a fixed positive time if needed. A uniform random-time score `tau*j_p(X_S)`, `S uniform[0,tau]`, has the correct truncated expectation and magnitude at most `tau J`.

Let `Q_p=O(b)` be the number of clamped empirical densities and let `i<=ell` be the number of persistent small-cell bits. For each `p`, independent seed blocks and Hoeffding give uniform approximation over **all** those finite inputs with, for example,

`M >= C (tau J)^2 e_f^(-2)[i log 2 + log(2Q_p/alpha)]`.

The exponential number of inputs occurs only inside this logarithm. Independence across different inputs is unnecessary: concentration applies separately to each fixed input, followed by a union bound. Independent blocks within each input are necessary and are supplied. The retained seed blocks must be reused on every later evaluation. Fresh unrelated output noise would not define an admissible deterministic function inside the corrected reference density.

Uniformization, caps and finite random bits can be fixed before evaluation. One sufficient proposal cap has order

`H = O(lambda ell tau + log(Q_p M/alpha) + log(1/e_f))`.

Increasing a finite bit budget until the displayed uniform bias bound in the attack fits its allocation is effective. Sampling `S` on a fine grid contributes at most the bounded-generator time-continuity error; threshold rounding and omitted Poisson tails contribute their explicit coupling bounds. These are uniform expected-score biases for each input. They need not assert an exact-real random clock or an independently certified typical trajectory for every possible input.

The stored program has polynomial seed storage `O(Q_p M H b_bit)` up to fixed-range/bond-index factors, and a single `f_p(x)` evaluation uses `M` capped trajectories with polynomial work per proposal. Evaluation of the glued function adds only the polynomial number of small cells. Local rate ghost averages can be computed from the fixed-radius dictionary; a sum over the entire exterior state space is not required.

For clarity, the source's shrinking cutoff gives explicit polynomial scales:

`g_0^(-1) = O(b^(1/2))`,

`tau = O_class(b^(7/12) log(b/e_f))`,

`sup |f_p| <= J g_0^(-1)[2+(ell/2)log(1/a)] = O_class(b^(2/3) log b)`.

Clipping the finite program at this last proven bound preserves its uniform approximation. After summing about `b/ell` cells and dividing by `b`,

`||F||_infty = O_class(b^(7/12) log b)`.

These are safe scale estimates, not optimized complexity claims. Constants include the fixed rate/range class and rounding conventions. The translated energy perturbation bound in the attack is correct: only `O(b)` translates affect a fixed bond, so uniform `F` error costs a polynomial factor in support and norm. Choosing `e_f` inverse-polynomial in `b` and the residual target suffices. There is no exponentially small shell-probability factor in these costs.

## 3. Direct all-density residual certificate

For the fixed retained function, the scalar translated energy score is

`Z_F = c_(0,1) [pi_(0,1)(ell+Gamma_F)]^2`.

It is a nonnegative bounded finite observable, with a known bound of order `lambda[1+C m ||F||_infty]^2`. Its expectation is **conductivity** `c(rho;F)`. The lower coefficient endpoint must be converted from diffusivity by `c_lower=2 rho(1-rho) D_lower` before subtraction. The pinned attack now states the correct normalization explicitly.

If `Z` is a bounded function of `q` Bernoulli bits, coordinatewise differentiation gives `|d E_rho Z/d rho| <= 2q ||Z||_infty`, including endpoints by one-sided limits. No density differentiability of the retained program itself is required. Here the score is zero on both constant inputs. Hence an explicit endpoint cutoff `a_R=e_R/(C q B_Z)` and mesh spacing of comparable order cover **all** densities, not just a fixed interior interval.

On the interior interval, the earlier primal–dual confidence algorithm supplies a certified lower conductivity. Its cutoff dependence remains polynomial. Source **Proposition 5.1, (5.3)** is density-uniform for conductivity; normalization to diffusivity can cost a factor `1/[2a_R(1-a_R)]`, yielding a sufficient inner cell scale of order `(C/(a_R delta_D))^(1/gamma_1)`. It does not insert an arbitrary untracked `C(a_R)` that could grow faster than a polynomial. The primal gap also has the explicit `a_R^2` dependence. Since `q B_Z` is polynomial in the outer scale, the endpoint cutoff does not secretly make the nested procedure exponential.

Confidence intervals for the energy must use fresh product samples conditional on the fixed program. Stagewise confidence allocations must cover the seed approximation, coefficient assay, rate acquisition and direct energy estimates. The attack calls for retaining these allocations; the usual summable allocation makes data-selected stopping valid.

Rate error is transferred to the true residual by the stated monotone bound

`R_true(rho,F) <= C_acquired(rho;F)/(1-eta) - c_lower,acquired(rho)/(1+eta)`.

This is valid for the same fixed `F`; there is no need for it to approximate the true-material corrector. No hidden repeat of the target experiment is present. A fixed local-table precision of order `e_R/lambda` can suffice with margins: at a successfully converging stage, `C_acquired=c_acquired+R_acquired` is bounded by `lambda/2+O(e_R)`, so the inflation floor is `O(lambda eta)`, rather than `eta` times the pessimistic pointwise score bound. Refinement during the finite offline acquisition phase is also permissible if fully charged.

Proposition 6.7 plus (6.70) gives polynomial eventual outer scale at fixed physical class. Numeric convergence constants are needed for an advance worst-case work bound, not for recognizing the observed residual certificate. This remains an assurance with class-dependent exponents, not a turnkey optimized numeric runtime.

## 4. Canonical replacement: the initial exterior obstruction is repaired

The decisive exact identity is source **(6.78)**:

`H_(L,zeta,F) = L_(Lambda_L,zeta) [sum_(x in Lambda_(L-r(F)-1)) tau_x F]`.

Every translated `F` inside the brackets is supported entirely inside `Lambda_L`. Source **(6.77)** restricts the generator to internal bonds `Lambda_L^*`; its outside dependence is only through the bare local coefficients `c_b`. Consequently, in one dimension the relevant exterior set has `O(r)` bits at the two boundaries, where `r` is the fixed bare rate range. It does **not** grow with `r(F)`. The initial statement that the H observable imports `O(r+r(F))` outside bits was incorrect. That statement is corrected in the pinned version.

This gives a concrete uniform assay rather than typical-exterior sampling. Enumerate `L+1` counts and at most `2^O(r)` exterior patterns; prepare each inside state from its exact uniform canonical law; evolve the source's internal-bond closed chain with that exterior frozen. This is polynomial at fixed bare range in dimension one. It is not polynomial in an unrestricted growing range, and a higher-dimensional boundary has a different enumeration cost.

The source observable

`W = D(k/L) A_L - (B_(L,zeta)-H_(L,zeta,F))`

has canonical mean zero for **every** count/exterior: `A_L` is a boundary-density difference and `B,H` are generator images. Source **(6.80)–(6.81)** uses the resolvent form on that conditional mean-zero space. The fixed-count path gap is at least `L^(-2)` by Dirichlet comparison and Aldous' theorem; empty/full shells have identically zero `W`. The displayed conservative norm bound `lambda+lambda L+2lambda L^2||F||_infty` is valid.

For each conditional chain with gap bound `g_0`, define

`v = (1/L)<W,G^(-1)W>`.

The estimator `tau W(X_0) W(X_S)/L`, with stationary canonical initialization and `S uniform[0,tau]`, has bounded magnitude `tau K^2/L`, and its omitted nonnegative tail is at most `K^2 exp(-g_0 tau)/(L g_0)`. Thus one may take

`tau >= g_0^(-1) log(4K^2/(L g_0 e_v))`,

`M_v >= C (tau K^2/L)^2 e_v^(-2) log(2(L+1)2^O(r)/alpha)`.

Caps, finite bits, and repeated evaluations of the retained function add polynomial costs. Only densities `k/L` are queried; their minimum nontrivial value is `1/L`, with the already accounted polynomial coefficient-cutoff cost.

The coefficient and rate uncertainty formulas in the attack are valid conservative estimates. If `||W-What||_infty<=Delta`, the Hilbert resolvent triangle inequality and positive form comparison give, for example,

`v_true <= (1-eta)^(-1)[sqrt(v_acquired) + Delta/sqrt(g_acquired L)]^2`,

where `Delta <= e_D + eta R_cell(1+2L||F||_infty)` is sufficient. All functions stay centered under their common uniform canonical law. This is stronger than merely asserting continuity of an unknown inverse generator.

**Source Proposition 6.10** controls the canonical variance by one half of the residual plus a boundary/canonical error. Together with a sufficiently small observed residual, it proves eventual smallness of the uniform canonical variance at a class-dependent polynomial block scale. The direct assay recognizes that smallness without a numeric homogenization error constant. Subtracting the residual is not needed for an upper variance certificate; if the exact source `Q_L` is used, its definition includes the `-R/2` term and that normalization must be retained.

## 5. Positive spectral lift and local-to-ring factors

The added finite-dimensional estimate is correct. For normalized `f=a1+h`, `h` mean zero, let `z^2=<h,Gh>` and `V=<W,G^(-1)W>`. Centering removes the constant–constant term; resolvent Cauchy–Schwarz bounds the cross term by `2|sa|sqrt(V)z`; and the gap bounds the remaining multiplication term by `|s|||W||_infty z^2/g`. Completing the square yields

`lambda_max(-G+sW) <= s^2 V/(1-|s|||W||_infty/g)`.

There is no uncomputed spectral constant in this step.

For a ring, each bond belongs to `L-1` translated contiguous `L`-site internal-bond blocks, so `sum_x G_x=(L-1)G_N`. Use mesoscopic blocks with the usual distinct-site/range geometry. The coefficient of the block potential is indeed `s_x=beta a_x(L-1)/(NL)`. The stated condition `beta A ||W||_infty/(N g)<=1/2` is sufficient. Summing conditional variational estimates gives the sharper factor `(L-1)/L^2`, which is bounded by the stated `1/L`. The displayed global bound therefore has the correct factors of `N`, `L` and `beta`.

For prescribed time-dependent `a_x(t)`, the instantaneous upper spectral bound integrates by the operator norm/Feynman–Kac estimate. Against stationary Bernoulli-1/2 path law, any initial microscopic law has entropy at most `N log 2`. Entropy inequality then gives exactly

`E integral_0^T (1/L) sum_x a_x(t)W_x(t)dt`

`<= log(2)/beta + 2 beta A^2 T max_(k,zeta)<W,G^(-1)W>/L`.

Applying it to either prescribed sign is valid. This is a bound on the signed expected time integral. It is not a bound on the expectation of an absolute integral, a supremum in time, or arbitrary state-dependent weights. The attack explicitly keeps those distinctions. The all-count/all-exterior conditional bound handles overlapping blocks; no block independence is invoked.

## 6. Remaining finite-N boundary and source fidelity

The attack's remaining-error accounting matches source **Proposition 7.15, (7.54)** and **(7.56)–(7.62)**. A small residual and a bounded corrector alone are insufficient: the entropy calculation includes the canonical replacement, finite-N expansion and one-block terms, the corrected-reference change, and a profile-dependent large-deviation pressure. The current delta makes the canonical variance and one stationary-reference pressure input effective, but it does not complete all those operations.

In particular, source **Remark 7.16** uses the true PDE/profile relation to make `g_delta<=0`, for sufficiently small profile-dependent `delta`. A learned primitive/coefficient interval and a numerical profile do not automatically supply every derivative-dependent cancellation or a fully numeric admissible `delta`. A checked positive upper pressure could replace negativity, but it must be included and integrated in the final error. The displayed open status is therefore warranted.

This review approves the acquisition and pressure operations at their specific uniform-ellipticity, fixed-range, one-dimensional product-reversible scope. It does not promote them to a completed operational finite-N microscopic forecast, a force-driven hydrodynamic theorem, a growing-control uniform theorem, an experimental result or a priority claim. The full finite-N closure remains **CONDITIONAL / OPEN** in the pinned attack.
