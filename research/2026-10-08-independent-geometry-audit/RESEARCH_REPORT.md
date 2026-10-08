# Independent frontier audit: harmonic-dimension spectral capacity and exact-crossing mechanism

**Date:** 2026-10-08 (Australia/Brisbane).
**Status:** Mathematically worked research note; not peer-reviewed, formalized, or historically priority-cleared. No resolution of the single-metric Yau problem is claimed.
**Astra base (immutable for this audit):** d20c4b040f63c2fb0c8da76362046d1946d0a2b9
**OpenAI primary source revision:** openai/math fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb
**Local reproducibility:** geometry_mechanism_checks.py, same folder.

## 1. Independent problem selection

Started from Astra 00_START_HERE.txt, read frontier/PRIORITIES.md, frontier/OPEN_PROOF_GATES.jsonl, topic TSV routes, status cards, and original/captured sources. All Astra claims labelled source_derived_unreviewed stay unreviewed until their mathematical proofs are independently completed.

Candidates considered:

| Domain | Candidate | Why not selected over geometry |
| --- | --- | --- |
| Riemannian geometry / spectral PDE | N175 one Ricci-nonnegative metric with infinitely many harmonic-dimension excesses; N210–N211 Steklov upper bound | Highest importance with a specific finite-to-countable source mechanism. Selected. |
| Group algebras / soficity | N47 / family197 hyperbolic direct-finiteness and N165 source audit | Positive-characteristic Formanek/BLR citation discrepancy is unresolved; algebraic family source remains conditional for the proposed group. |
| Ergodic theory | N208 family197 residual Haar tail / Bernoulli conjugacy | Conditional entropy equality does not determine positivity of supremal Rokhlin entropy or a genuine conjugacy. |
| Reaction networks | N173 all-face log-valuation permanence and N212 critical explosive CTMC | N173 invokes separately unverified affine absorber lemma; N212 unequal-rate cases inherited, with major assumptions about kinetic clocks. |
| Quantum information | N179 critical thermal full-SEP approximation and N203 SU(d) singlet marginal threshold | Interesting candidate results, but current routes are chiefly specialized asymptotic statements and externally unreviewed. |

These comparisons are **relative research decisions**, not global claims about value or correctness.

## 2. Source-grounded geometry frontier

Family361's three-dimensional released theorem constructs, separately for every sufficiently large growth degree k, a Ric>=0 metric on R^3 for which dim H_k exceeds (k+1)^2. It does NOT supply a single metric for infinitely many k. Original paper source: openai/math, preprints/A-Three-Dimensional-Counterexample-to-Integer-Degree-Harmonic-Dimension-Comparison-September-26-2026/build/sections/{crossings,angular-program,geometry,transfer,matching,growth}.tex at the pinned OpenAI revision.

Astra N175 post-source candidate: for every 4/9<v<1 and every 1<c<9v/4, one smooth complete Ric>=0 metric on R^3, Euclidean near 0 and AVR=v, such that

    limsup_{k -> infinity} dim H_k / (k+1)^2 > c.

The proposal requires (i) all-index fixed-area angular crossings (S1–S3), (ii) an infinitely staged compact angular library, (iii) Ricci-positive slowly varying radial realization, (iv) fixed-cutoff harmonic graphs with complete local matrix control, (v) infinitely many scalar matches, and (vi) all-radius growth. Current source status is internal candidate, not externally verified.

Primary source audit:
* OpenAI crossings.tex, Lemma "Two independent splitting directions": in 2D conformal variation the trace-free double compression is represented by u^2-v^2 and 2uv; unique continuation gives independence.
* OpenAI crossings.tex, Lemma "Adjacent doubles": within a round l-block, Sym^2 Y_l -> direct sum Y_{2j} for j=0..l via product functions gives all symmetric first variations. Across round blocks, an even equatorial conformal bump gives a parity inversion of asymptotic size (1-3 mean(psi))l+o(l), and indexed parity eigenvalues locate a double at B_l,B_l+1. A preliminary axisymmetric triple degeneracy alone is NOT a valid isolated-double certificate; the parity path and retention step are essential.
* OpenAI matching.tex: for each ordered pair, stable forward/backward recurrences meet at only one kind of crossing. Reversing the ordered pair exchanges "zero cuts" and "matching cuts", so it is not automatically two independent constraints per double. The proposed signed forcing at a simple crossing has amplitude eta^(3/4), supported across an effective Gaussian width eta^(-1/2), hence mismatch scale eta^(1/4). This is a mechanism, not a proof of its infinite extension.
* Astra N175 PROOF_v3 adds stage-dependent derivative envelopes, support comparability, full matrix rather than one-entry error bounds, birth-only matching columns, countable compactness, and bandwise asymptotic averaging. External validation and actual materialization remain absent.

Relevant prior results:
* Xian-Tao Huang, "Harmonic functions with polynomial growth on manifolds with nonnegative Ricci curvature", arXiv:2109.07534, exact leading coefficient equal to normalized AVR **when the tangent cone at infinity is unique**; the cycling N175 candidate has nonunique tangent cones, so this does not contradict it.
* Xiaohan Cai and Mijia Lai, "Dimension of polynomial growth harmonic functions on locally conformally flat manifolds with nonnegative Ricci curvature", arXiv:2608.04553; the sharp Euclidean upper comparison is shown under *local conformal flatness*, which is not established for the cycling metrics.
* Tobias H. Colding and William P. Minicozzi, "On Function Theory on Spaces with a Lower Ricci Curvature Bound", Math. Research Letters 3 (1996), 241–246; foundational finiteness and nonnegative Ricci context.
* Classical Dirichlet principle, min–max, Ky Fan, compact smooth-family Weyl asymptotics, and unique continuation are used; this audit does not represent them as new results.

## 3. An independently derived spectral-capacity extension of N210

The following theorem removes two source assumptions and gives a time-averaged capacity for variable angular area. It is **new relative to the narrow N210 statement**, not independently established as historically novel.

### Theorem (averaged angular-area capacity; proposed standalone result)

Let n>=3, d=n-1. Let (M^n,g) be smooth, complete, without boundary, with a compact core and global smooth polar-product end

    g = dr^2 + f(r)^2 h_{log r}

for r>=r_0, where r is a proper radial coordinate and each h_t is a smooth Riemannian metric on the same compact sphere S^d. Assume:

1. f(r)>0 is smooth, and f(r)/r -> a>0 as r->infinity. **No assumption is made on rf'(r)/f(r).**
2. {h_t:t>=log r_0} is relatively compact in the smooth C-infinity topology and \|\partial_t h_t\|_{C^0(h_t)} ->0. **No constant-area requirement is made.**
3. A(t)=Vol(S^d,h_t) (bounded above and below automatically); set omega_d=Vol(B^d(1)),
   
       K(t) = omega_d a^d A(t)/(2pi)^d,
       L = liminf_{T->infinity} (1/T) integral_{t_0}^T K(t)^(-1/d) dt.

Then L is positive and finite. For H_k the space of global real harmonic functions with growth at most C(1+r)^k, each h_k=dim H_k is finite and

       limsup_{k->infinity} h_k/k^d <= ((d+1)/(d L))^d.                    (A)

No Ricci-curvature sign is required.

In particular, if A(t)->A_infinity, set A_d=Vol(S^d,round), v=a^d A_infinity/A_d. Then volume comparison by integration of polar area gives AVR=v and

       limsup h_k/k^d <= (2/d!) v ((d+1)/d)^d.                          (B)

This **strictly weakens** N210, whose statement assumes A(t)=A_d for all large t and rf'(r)/f(r)->1.

### Proof

**Step 1 (uniform cone-collar comparison).** Write t=log R. Fix a logarithmic width delta>0 and compare the exterior collar [R exp(-delta),R] with the frozen cone metric ds^2+a^2 s^2 h_t. Assumptions (1),(2) imply uniform C^0 quadratic-form comparison on this collar as R->infinity: f(s)/(as)->1 uniformly when s>=R exp(-delta); h_{log s}-h_t is bounded by delta sup_{u in [t-delta,t]}\|\dot h_u\|->0. Therefore both Dirichlet energies and outer boundary L^2 measures agree with the frozen-cone ones up to 1+o(1), uniformly over *all* boundary data. Dirichlet energy minimization on the whole enclosed domain is no less than minimization on the collar with free Neumann inner boundary. By min–max, the scaled Dirichlet-to-Neumann eigenvalues mu_j(t)=R sigma_j(R) satisfy, for large t, a uniform multiplicative lower comparison against the cone's free-Neumann collar eigenvalues.

**Step 2 (exact frozen eigenvalues).** For an angular eigenvalue lambda>=0, the cone radial exponents solve p(p+d-1)=lambda/a^2; set p_+=-(d-1)/2+sqrt((d-1)^2/4+lambda/a^2) and p_-=-(d-1)-p_+. With rho=exp(-delta), the exact scaled free-Neumann collar eigenvalue is

     nu(lambda,delta)=p_+ [1-rho^(2p_++d-1)]/
                           [1+(p_+/(p_++d-1))rho^(2p_++d-1)].

It is zero when lambda=0, and nu(lambda,delta)/sqrt(lambda)->1/a as lambda->infinity. Since the angular family is smoothly precompact, the Weyl law is uniform:

    lambda_j(h_t) = [j / (omega_d A(t)/(2pi)^d)]^(2/d)(1+o_{j->infinity}(1)).

One way to prove this uniformity is to choose a finite multiplicative quadratic-form net of the smooth compact family, apply ordinary Weyl to the net metrics, and compare all eigenvalues using min–max. Thus, for any eps>0 there are T_eps,J_eps so that for ALL t>=T_eps and j>=J_eps,

    mu_j(t) >= (1-eps) j^(1/d) K(t)^(-1/d).                              (1)

This requires no rf'/f derivative.

**Step 3 (Gram determinant).** Fix m linearly independent u_1,...,u_m in H_k. Their traces on every sufficiently large S_R are linearly independent: a nonzero harmonic combination zero on the whole boundary is zero in the interior by Dirichlet uniqueness and everywhere by unique continuation. On the identified S^d let

    dnu_t = R^(-d) dA_{S_R} = x(t)^d dA_{h_t},    x(t)=f(exp t)/exp t;
    G_ij(t)=integral u_i(exp t,theta)u_j(exp t,theta) dnu_t.

G(t) is positive definite. Let Lambda_R be the selfadjoint positive Dirichlet-to-Neumann operator on S_R and B_t=R Lambda_R. Harmonicity gives \partial_t u=B_t u. The density derivative is

    z_t(theta) = \partial_t log(dnu_t)
               = d \partial_t log x(t) + q_t(theta),
    q_t=(1/2)tr_{h_t} \dot h_t,    ||q_t||_infinity ->0.

After orthonormalizing the trace span and applying Ky Fan,

   (d/dt) log det G(t) >= 2 sum_{j=0}^{m-1} mu_j(t)
                           + m d (d/dt)log x(t) - m ||q_t||_infinity.   (2)

This is exact at the level needed: unlike N210, the possibly wildly oscillating scalar term d(d/dt)log x is NOT discarded pointwise.

**Step 4 (integrated cancellation).** Integrate (2) from a fixed T_0 to T. The integral of the scalar logarithmic derivative equals m d log[x(T)/x(T_0)] = O_m(1) because x(t)->a>0. The angular-measure penalty is m integral ||q_t||dt=o_m(T). Each u_i has C_i exp(kt) growth at S_{exp t}, and total normalized boundary mass x(t)^d A(t) is bounded. Hadamard's determinant bound therefore gives log det G(T)<=2mkT+O_m(1). Divide by 2T and take T->infinity:

     mk >= liminf_{T->infinity} (1/T) integral_{T_0}^T
                                  sum_{j=0}^{m-1} mu_j(t)dt.           (3)

The crucial cancellation survives without pointwise convergence of rf'/f.

**Step 5 (dimension count).** Use positivity of the omitted low mu_j, (1), and the definition of L:

    mk >= (1-eps) L sum_{j=J_eps}^{m-1}j^(1/d).

As m->infinity, the sum equals [d/(d+1)]m^(1+1/d)(1+o(1)). This forbids arbitrarily large m at any fixed k, hence H_k is finite. Taking m=h_k as k->infinity and then eps->0 yields (A). If A(t)->A_infinity, then L=(omega_d a^d A_infinity/(2pi)^d)^(-1/d). The identity omega_d A_d/(2pi)^d=2/d! and v=a^d A_infinity/A_d give (B). End of proof.

**Proof audit gate:** Step 1's uniform *all-test-function* energy/norm comparison and Step 2's uniform compact-family Weyl law are standard but should receive an independent specialist/reviewer line-by-line check before dissemination. The calculation above makes every imported theorem and limit exchange explicit. The estimate does NOT prove that the upper bound is attained by any Ric>=0 manifold, nor is it a sharp v-only theorem outside the assumed polar class.

### Strictly broader examples

*Radial derivative oscillations:* for t=log r sufficiently large,

    f(r)=a r [1 + eta sin(t^2)/t],   0<eta<1/4.

Then f(r)/r->a, and f'(r)>0 eventually, but

    r f'(r)/f(r) -1 = 2 eta cos(t^2)+o(1),

so the radial derivative does not tend to 1. With any fixed angular h_t=h_round this is covered by (A), not by the original N210 hypotheses. No nonnegative-Ricci claim is made for this example.

*Slow area oscillations:* in dimension n=3, fix f(r)=ar and let

    h_t=(1+eta sin(sqrt t)) h_round,   0<eta<1.

The h_t family is smoothly precompact, \dot h_t->0 and A(t)=4pi[1+eta sin(sqrt t)] has no limit. An integration-by-parts calculation under u=sqrt t shows its long-time average of any continuous 2pi-periodic function F(sqrt t) equals the ordinary phase average. Thus (A) reads

    limsup h_k/k^2 <= (9a^2/4) / B(eta)^2,
    B(eta)=(1/2pi)integral_0^(2pi)(1+eta sin s)^(-1/2) ds >1.

The last strict inequality follows from strict Jensen convexity. This example shows that the time-average coefficient is genuinely applicable beyond a limiting angular area; it does not assert sharpness.

## 4. Rigorous finite-dimensional crossing obstruction

Let A(s), 0<=s<=S, be a continuous real-symmetric N-by-N loop with A(S)=A(0), simple endpoints, and simple spectrum throughout. Each ordered spectral projector is continuous and is the *same* projector at both endpoints. Consequently simple-spectrum loops cannot permute the ordered eigenlines. Sign holonomy is possible but does not move a label to a different ordered eigenvalue.

If the path admits only isolated exact transverse double crossings and N continued eigenlines form one N-cycle after one period, it must contain AT LEAST N-1 double crossings. Proof: each isolated double gives a transposition of ordered rank labels. Multiplication by a transposition changes the number of cycles of a permutation by one. The identity starts with N cycles; an N-cycle ends with one. Hence >=N-1 transpositions. This is sharp (adjacent transpositions generate an N-cycle).

For a band I=(B_{M0},B_M], B_M=(M+1)^2, transitive spectral cycling therefore needs at least (M+1)^2-(M0+1)^2-1 exact pair events per period. In N175's M0=o(M) regime this is Omega(M^2), and its use of adjacent transpositions is order-optimal **within that permutation architecture**. This is a mechanism-specific cost bound, not a general lower bound for all harmonic-function constructions.

In a single transitive cycle that preserves this band's ordered positions at every phase, every continued line has, over N periods, the same exact mean frequency:

    (1/(N S)) integral_0^S sum_{j in I} frequency_j(s) ds.

This follows because at each phase all N continued lines occupy the band's N positions and their period-to-period base permutation acts transitively. It is not asserted for disconnected permutation cycles that temporarily cross between their orbits.

### Explicit 2x2 sanity check

Let R(theta) be a planar rotation and

    A_0(s) = R(pi s/2) diag(1+s,2-s) R(pi s/2)^T,  0<=s<=1.

Then A_0(0)=A_0(1)=diag(1,2), the sole exact double is at s=1/2, and the continued eigenline values 1+s and 2-s are swapped after the period. Each continued mean equals 3/2. The *ordered* upper eigenvalue has mean 7/4. Choosing a threshold k=1.6, exact cycling equalizes both modes below k.

Perturb the loop to A_eps(s)=A_0(s)+eps diag(1,-1), with 0<eps<0.1. Its spectral gap is

    2 sqrt((s-1/2)^2 + eps^2 + 2eps(s-1/2)cos(pi s)),

which is positive for every s (zero would force s=1/2 and eps=0). Its ordered upper eigenvalue mean is >=7/4-eps>1.6 by the 1-Lipschitz spectral perturbation inequality. No label exchange remains. Therefore replacing exact doubles by arbitrary close *avoided crossings* loses the exact frequency-equalization mechanism. This does NOT rule out entirely different dynamical mode-conversion mechanisms.

## 5. Finite diagnostics and honest limitations

The accompanying Python checks independently recompute finite frozen-cone spectral ratios and the explicit symmetric 2x2 path. At v=0.81, 9v/4=1.8225, while the band ratio (M+1)^2/(average p_l)^2 equals 1.847223690 at M=100 and 1.824961576 at M=1000. The 2x2 continued means are exactly 1.5; the sorted high mean is 1.75; for avoided gaps eps=0.01,0.05,0.1 its sampled high means are 1.744072490, 1.725651180, 1.711055319. For an area oscillation eta=0.2, phase average B=1.007668716 gives capacity 1.794865812 rather than 1.8225.

All test assertions passed in the local runtime, but these finite tests cannot validate infinite-dimensional transfer, existence of a globally Ric>=0 common metric, or the variable-area theorem's use of analytic theorems.

## 6. Source paths and continuation routes

Astra primary evidence at the pinned commit:
- frontier/review_cards/N175-single-metric-harmonic-limsup.txt
- frontier/review_cards/N210-steklov-harmonic-capacity.txt
- frontier/review_cards/N211-uniform-collar-determinant-transfer.txt
- frontier/cards/N175-single-metric-harmonic-limsup.json
- web/pages/d-413da5591afd120a.html (Astra PROOF_v3; extracted proof SHA256 f3adfef248ab5a34ca6e12f1faf9231ea35abb48398092cce60553d3cc58e5b3)
- web/pages/d-7a7b27b94021a6ef.html (current POST_SOURCE_STATUS)
- web/pages/d-8d1a632c0e6d672c.html (N210/211 Steklov source; extracted SHA256 2c0b2744e82d7e4d336abd4a6007830e7d88da6fe0ff479d0b79e2e9ab372b91)
- web/pages/d-67a9470121cebb1a.html (spectral cross-block audit)
- web/pages/d-bd1228378cea4c2d.html (spectral transversality audit)
- web/pages/d-f82eef6280e15223.html (PDE whole-matrix uniformity red team)
- web/pages/d-7d71a96e1ea2e72e.html (post-freeze transfer audit)

External paper source:
https://github.com/openai/math/tree/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-Three-Dimensional-Counterexample-to-Integer-Degree-Harmonic-Dimension-Comparison-September-26-2026/build/sections

Prior-literature links:
https://arxiv.org/abs/2109.07534
https://arxiv.org/abs/2608.04553
https://doi.org/10.4310/MRL.1996.V3.N2.A9
https://www.cambridge.org/core/services/aop-cambridge-core/content/view/25AF425E2069C808258EA860D2329372/S0008414X00050392a.pdf
https://www.heldermann-verlag.de/jlt/jlt08/VALLAT.PDF

**Immediate next research gates (in priority order):**
1. Seek an adversarial independent *complete* proof audit of Astra N175 Steps 5–7, with particular attention to transfer estimates uniform in future stage schedules, the whole local matrix, and countably many Brouwer coordinates. Do not substitute finite-dimensional diagnostics for this.
2. Either produce a fully materialized finite-stage angular spectral crossing model with rigorous error controls, or identify one exact impossible pair of conditions in the countable schedule.
3. Explore transferring the averaged spectral-capacity theorem to non-polar Ric>=0 manifolds via good-radius collar geometry, measuring and charging the radii that fail spectral control. The obstacle is uniform DtN comparison on uncontrolled boundaries.
4. Priority-clear the averaged variable-area theorem against existing Dirichlet-to-Neumann/Steklov and harmonic-dimension literature, and obtain a specialist review before claiming publication-level novelty.
5. Reconsider the alternative family197/Bowen, N173 reaction-network, or N203 quantum problem only if geometry stalls at a precise irreparable proof gate.

**Scientific claim ledger:** The time-averaged spectral bound is an independently derived extension, subject to external theorem/priority audit. The permutation crossing count and 2x2 example are self-contained elementary facts. The common-metric N175 existence is still a source-derived unreviewed candidate. No major longstanding open problem was resolved in this investigation.
