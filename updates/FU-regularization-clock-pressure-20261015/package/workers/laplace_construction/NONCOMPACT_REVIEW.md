# Independent review of the noncompact regularization theorem

Review date: 2026-10-15. Reviewer: laplace_construction_v3. This is an independent internal mathematical audit, not external certification, formal verification, or historical-priority clearance.

Reviewed source: `workers/noncompact_regularization_astra/PROOF.md`, 447 lines, 22050 bytes, SHA-256

    3f27e0579c4a35084da4e189ef647a0bbfcdaf2d93f9a9aa69ac0e8d278cd90a

Exact reviewed bytes are retained at `sources/NONCOMPACT_REVIEWED_PROOF_3f27e0579c4a.md`. `NONCOMPACT_SOURCE_RECEIPT.json` records the original and retained paths. Later author amendments are separate versions and were not silently substituted into this review.

## Verdict

No fatal gap was found in the main theorem under its actual hypothesis (W). I independently reconstructed the global Bregman-remainder estimate, the weighted canonical extension, the necessity argument, and the Bochner mass/moment identities. Variable orders N_k do not invalidate the threshold diagonalization. The theorem legitimately removes compact support, replacing it with a strong all-weight distributional decay assumption.

One unqualified sentence at source line 427 is false if read literally: the boundary example does not exclude arbitrary probability noise. It excludes probability noise having all exponential moments. An explicit renewal probability regularizes that example exactly. The theorem statement and preceding proof already impose the correct all-exponential condition, so this is a scope correction rather than a defect in the main equivalence.

No independent literature audit was performed for this review. The source's prior-art comparisons remain source claims. External correctness, exact historical novelty, efficient compilation, and practical capability remain UNKNOWN.

## 1. The precise input space matters

The actual premise is, for each positive integer k, a finite A_k and finite integer N_k such that

    ||T(h)|| <= A_k max_{|alpha|<=N_k}
                    sup_y exp(-k|y|)|partial^alpha h(y)|,
    h in C_c^infinity.                                          (R1)

This is substantially stronger than merely assuming T is tempered, that some exponential weighting is tempered, or that selected formal Laplace values exist. It controls translated tests globally. The derivative order and constant may grow arbitrarily with k. The conclusion does not acquire or compute these data.

The source's equivalence with `exp(a sqrt(1+|y|^2))T` tempered for every a>0 is valid. In the forward direction choose k>a; differentiation of the smooth exponential leaves a bounded factor `exp(a sqrt(1+r^2)-kr)`. In the reverse direction use a tempered bound for weight b>k and absorb the polynomial Schwartz factor into `exp(-(b-k)r)`.

The defined extension space X consists of smooth functions whose derivatives of every order share some finite exponential growth exponent b, although their constants can vary. For h in X and k>b,

    ||chi_R h-h||_{k,N_k} -> 0.

The error outside B_R has the factor `exp(-(k-b)R)`. Product-rule terms differentiating the cutoff have the same decay and factors R^{-j}. Thus the cutoff definition of T(h) exists in norm and is independent of cutoff and admissible k. All functions used in the proof belong to this domain or to the relevant completion of compactly supported tests.

In particular:

- Constants and real exponentials belong to X.
- For a finite scalar measure nu and a compact smooth phi, `y -> integral phi(y+z)nu(dz)` has every derivative bounded; (11) defines an actual distribution.
- For the constructed p, `p(x-y)` has every derivative bounded as a function of y at each fixed x.
- The error test can be written exactly as `p(x-y)/p(x)-exp(g.y)`. This directly proves membership in X, with exponent |g|, without relying on a separate polynomial-growth argument for infinitely many derivatives.

No arbitrary noncompact test function is admitted merely because its formal pairing looks finite.

## 2. Weighted necessity is justified

Fix real g and choose k>|g|. For each fixed z, set

    f_{R,z}(y)=exp(g.y)(chi_R(y+z)-1).

For every derivative through N_k, the weighted supremum tends to zero as R tends to infinity. The support of the cutoff error or its derivatives escapes every fixed y-ball when z is fixed, and the remaining factor is bounded by `exp(-(k-|g|)|y|)`. Uniformly over R>=1 and z, that seminorm is bounded by a finite constant depending on g, N_k, and the cutoff, because the exponential factor never exceeds one and cutoff derivative factors are bounded.

Multiplying by exp(g.z) and integrating against nu is legitimate because its genuine moment m_nu(g) is finite. Dominated convergence therefore gives the claimed convergence in the weighted norm, not merely pointwise convergence. Applying (R1) yields

    S(exp(g.x)chi_R(x)) -> m_nu(g)L_T(g)

in E. At g=0 this tends to e. Thus one finite cutoff Q_A lies in the cone interior. The elementary test inequality

    exp(g.x)chi_R(x) >= exp(-2A|g|)chi_A(x),  R>=2A,

then implies that the limiting Laplace element dominates a positive scalar multiple of the interior element Q_A. A closed convex cone's interior is stable under addition of a cone element, so L_T(g) is interior.

This argument requires neither pointedness nor normality of the cone, and it does not assume that a weakly normalized operator measure is norm tight. Norm convergence follows from the weighted input estimate.

## 3. The global Bregman jet estimate survives reconstruction

Write `rho(z)=sqrt(1+|z|^2)`, `s=log rho(x/L)`, `t=q(s)`, and

    delta=(q(s)+1)/(L rho(x/L)).

The source's threshold construction has bounded derivatives of q, q>=1, and q(s)<=1+s/2. Therefore delta<=2/L<=1. The scaled potential has derivative bounds

    ||D^j V_L(w)|| <= C_j L^{1-j}q(log rho(w/L))rho(w/L)^{1-j}, j>=2,

with constants independent of every threshold location.

For r=|y| and 0<=u<=1, the exact comparison

    (1+r/L)^{-1} <= rho(x/L-u y/L)/rho(x/L) <= 1+r/L

is valid even if the line segment crosses the origin. The logarithmic difference is at most log(1+r/L). Bounded q' gives

    q(log rho(x/L-u y/L)) <= C(q(s)+1)(1+r/L).

Substitution into the scaled jet bound yields

    ||D^j V_L(x-u y)||
       <= C_j delta (L rho)^{2-j}(1+r/L)^j
       <= C_j delta(1+r)^j, j>=2.                              (R2)

This is the critical noncompact estimate. It is global in y and includes angular derivatives because the original estimates are Cartesian derivative bounds for the smooth radial potential.

Let `F_x(y)=V_L(x-y)-V_L(x)+grad V_L(x).y`. Convexity gives F_x>=0 everywhere. Taylor's integral remainder and (R2) give

    |F_x(y)| <= C delta(1+r)^4,
    |grad_y F_x(y)| <= C delta(1+r)^3,
    |D^j_y F_x(y)| <= C_j delta(1+r)^j, j>=2.                   (R3)

For order zero, `|exp(-F)-1|<=F`. For positive derivative orders, the chain rule gives a sum of products of F jets multiplied by exp(-F)<=1. Every product has at least one factor delta, and delta^ell<=delta. A product with at most N factors has polynomial degree at most

    K_N=max(1,N)max(4,N).

Consequently

    max_{|alpha|<=N}|partial^alpha(exp(-F_x)-1)|
          <= B_N delta(1+|y|)^{K_N}.                           (R4)

After differentiating the product with exp(g.y), using |g|<=t and k>=t+1, the remaining supremum is

    sup_{r>=0} exp(-r)(1+r)^{K_N}<infinity.

This proves the source's weighted error bound (32), with a finite constant D_N depending on N,m and the fixed step only. Convexity is essential: without F>=0, differentiating exp(-F) could introduce uncontrolled growth rather than the favorable factor exp(-F)<=1.

## 4. Variable distribution order is fully charged

The pointwise choice is `k(t)=ceil(t)+1`, so k(t)>=t+1. At that point the proof uses the actual finite order N_{k(t)} and its corresponding constant D_{N_{k(t)}}. It never assumes one order works for all weights.

After making A_k,N_k,D_N nondecreasing, the function

    G(t)=max(1, A_{k(t)}D_{N_{k(t)}}(1+t)^{N_{k(t)}+1}/mu(t))

is finite and nondecreasing. The delayed thresholds satisfy `G(q(s))<=G(1)exp(s/2)`. Thus the error divided by the relevant cone margin is at most `G(1)exp(-s/2)/L` everywhere. Every jump in N_k or A_k merely delays a finite threshold further; no asymptotic bound on their growth is used.

The derivative constants can be extremely large, and the countably many weight data and compact-tilt margins remain necessary input obligations. This is an existence argument, not an efficient method for discovering those bounds.

## 5. Mass and moment Fubini hold in the stated completion

The claimed weighted derivative supremum bound for p follows from the all-derivative weighted L1 class: apply a local cube W^{m,1}-to-supremum estimate and compare weights on that cube. It is not true from moments of p alone; the source correctly includes every derivative in its class.

For every k and derivative alpha, with `P_{k,n}=max_{|alpha|<=n}sup_z exp(k|z|)|partial^alpha p(z)|`, the triangle inequality yields

    exp(-k|y|)|partial^alpha p(x-y)|
       <= P_{k,n} exp(-k|y|-k|x-y|)
       <= P_{k,n}exp(-k|x|).                                  (R5)

This proves (13) and gives every weighted output integrability assertion by selecting k larger than the desired weight. One extra derivative controls continuity in x in the same completion norm.

For fixed g, choose k>|g|. The map

    x -> exp(g.x)p(x-.)

is continuous into the completion of compact smooth functions under the weighted C^{N_k} norm, and its norm is bounded by `P_{k,N_k}exp(-(k-|g|)|x|)`. It is therefore Bochner integrable. Continuity gives separable range, so no hidden strong-measurability obstruction arises even if the ambient completion is not separable.

Evaluation of any derivative through N_k at a fixed y is continuous on that completion. Evaluating the Banach integral identifies it with

    exp(g.y) integral exp(g.z)p(z)dz.

The bounded linear extension of T commutes with this Bochner integral. This proves the genuine norm-valued moment identity and, at g=0, total mass e. The identity of `T*p` with convolution (11) follows by the same argument with a compactly supported scalar test in the x variable. There is no formal interchange of a noncompact distribution and an unbounded exponential test.

## 6. Concrete scope correction and exact countercalculation

The source's boundary example is

    tau=(1+B)delta_0-eta,
    B=eta(R)>0,

where eta is positive with finite Laplace transform through g=a and infinite transform for g>a. Its argument correctly proves that no probability nu having all exponential moments can make tau*nu nonnegative: the positive-measure inequality `(1+B)nu>=eta*nu` contradicts finite left and infinite right g-moments when g>a.

The last sentence of source line 427 says, without qualification, that the obstruction excludes arbitrary probability noise. That broader assertion is false. Define the finite positive measure series

    nu = sum_{n=0}^infinity eta^{*n}/(1+B)^{n+1},
    eta^{*0}=delta_0.                                         (R6)

Its total mass is

    (1/(1+B)) sum_{n=0}^infinity (B/(1+B))^n = 1.

The series converges in total variation. Telescoping gives the exact finite-measure identity

    ((1+B)delta_0-eta)*nu = delta_0.                            (R7)

For g>a the n=1 term already has an infinite exponential moment, so this nu is not all-exponential. Equations (R6)-(R7) do not contradict the theorem. They show exactly why its noise-moment qualification must remain attached to the boundary statement.

Requested correction sent to the author: replace the unqualified phrase by "arbitrary probability noise having all exponential moments." No author file was edited by this reviewer.

## 7. Review limits

The mathematical review supports the exact theorem under (W), not a theorem for all tempered distributions or all distributions with formally positive Laplace continuations. It does not establish novelty, physical implementability, finite precision stability, a sampling algorithm, a variance bound, or a task-matched advantage.

The genuinely noncompact signed-measure example in the source has all exponential variation moments and negative atoms arbitrarily far out; its nonnegative Laplace-transform formula and the failure of integer-radius compact truncations are correct algebraic illustrations. No grid or finite window is being used to certify the global theorem.

This review did not use another reviewer's agreement as evidence and did not modify the repository working tree, the author's proof, original attachments, or GitHub state.
