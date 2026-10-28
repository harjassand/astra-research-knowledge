# Value-only acquisition of a smoothed derivative action

**Outcome: acquired.** Two original whole-vector evaluations suffice for an exactly unbiased action of \(H_s(c)=\mathbb E[Dg(c+sZ)]\), with the deterministic bound \(L\|v\|_2\). This is an ideal-real oracle operation; it does not acquire the stronger matrix or Gaussian-completion interfaces of the sampler programme.

The governing source is [R22, §9, lines 352–415](https://github.com/harjassand/astra-research-knowledge/blob/6360a39d9488a041f259181e38c37e638b83c609/updates/DP/package/foundational_campaign/FINAL_ROUND/r22_polylog_mean_factory.txt#L352-L415), found through the [ordinary N687 card](https://github.com/harjassand/astra-research-knowledge/blob/6360a39d9488a041f259181e38c37e638b83c609/cards/N687-gaussian-gradient-mean-sampler-stein-continuation.txt#L1-L26). R22's overall programme assumes a conservative \(g=\nabla F\), \(F\in C^{1,1}\) (lines 4–11). **Reconstructed extension:** the action proof itself uses only global Lipschitzness and absolute continuity, so the question's general vector-valued Lipschitz map is covered. Conservativity is needed for the source's subsequent symmetry claims, not for this acquisition. The card labels the campaign source-derived/unreviewed at intake; this report reconstructs the small action proof, not its end-to-end sampler candidate or novelty.

For \(v\ne0\), let \(u=v/\|v\|\). Draw mutually independent \(Z_0\sim N(0,I_d)\) and \(a_1,a_2,a_3\sim N(0,1)\), and set

\[
 Z_\perp=Z_0-(u^TZ_0)u,\quad R=s\sqrt{a_1^2+a_2^2+a_3^2},\qquad
 J_s(c;v)=\|v\|\frac{g(c+sZ_\perp+Ru)-g(c+sZ_\perp-Ru)}{2R}.
\]

Return zero with no queries for \(v=0\). For literal every-execution handling, if the three radial seeds are all zero, replace \(R=0\) by \(s\) before making the two queries. This harmless null-event repair is my explicit implementation choice within R22's allowed bounded null handling (lines 362–363); it also preserves the affine identity below on that branch. No derivative is evaluated.

To reconstruct the distributional identity, independently introduce \(U\sim\mathrm{Unif}[-1,1]\) for analysis. The radius density is

\[
 f_R(r)=\sqrt{2/\pi}\,r^2s^{-3}e^{-r^2/(2s^2)},\quad r>0.
\]

Consequently

\[
 f_{UR}(t)=\int_{|t|}^\infty\frac{f_R(r)}{2r}\,dr
 =\frac{e^{-t^2/(2s^2)}}{s\sqrt{2\pi}},
\]

so \(UR\sim N(0,s^2)\), independently of \(Z_\perp\). Thus \(X=c+sZ_\perp+URu\sim N(c,s^2I_d)\). A Lipschitz map restricts to an absolutely continuous function on every line. Rademacher's theorem and Fubini identify its line derivative with \(Dg\,u\) for almost every perpendicular base point, which suffices under the perpendicular Gaussian. Therefore, almost surely in \((Z_\perp,R)\),

\[
 \frac{g(c+sZ_\perp+Ru)-g(c+sZ_\perp-Ru)}{2R}
 =\frac12\int_{-1}^1Dg(c+sZ_\perp+tRu)u\,dt
 =\mathbb E_U[Dg(X)u\mid Z_\perp,R].
\]

The a.e. operator bound \(\|Dg\|_{\mathrm{op}}\le L\) permits expectation/interchange. Gaussian absolute continuity makes the version of the weak derivative on its null set irrelevant. We obtain

\[
 \boxed{\mathbb E[J_s(c;v)]=H_s(c)v},\qquad
 \boxed{\|J_s(c;v)\|\le\frac{\|v\|}{2R}L(2R)=L\|v\|}.
\]

The second identity is a bound on **every execution**, including the repaired zero-radius branch. The first is generally only an expectation identity. The operation takes exactly two value calls when \(v\ne0\), \(d+3\) scalar Gaussian seeds in this implementation, and \(O(d)\) vector arithmetic/storage and coordinate reads. No infinitesimal limit or derivative-continuity modulus is required. Exact Gaussian reals, exact values, square roots and arithmetic are model primitives; numerical cancellation at small \(R\), random-bit generation and finite-bit accuracy require separate analysis. A constant query count is not a polylogarithmic runtime or full sampler theorem.

For the requested fixture, \(Dg=A\) everywhere, hence \(H_2((1,2))=A\), and

\[
 Av=\begin{pmatrix}3/4\\1/6\end{pmatrix},\quad
 g(c)=\begin{pmatrix}2\\-1/12\end{pmatrix},\quad
 \|Av\|=\sqrt{85}/12.
\]

For every positive radius and every perpendicular seed the endpoint difference is \(2RAu\), so **\(J_s(c;v)=Av\) on every realization**, including the specified null repair. The offset \(b\), centre \(c\), smoothing scale \(s\) and random endpoints cancel. The sharp Lipschitz constant is the larger eigenvalue

\[
 L_*=\frac{5+\sqrt{10}}{12}\simeq0.680189805,
 \qquad \|Av\|\simeq0.768295371< L_*\sqrt5\simeq1.520950642.
\]

One exact two-call check chooses \(sZ_\perp=(2,4)\) and \(R=\sqrt5\), giving endpoints \((5,5)\), \((1,7)\), values \((19/4,23/12)\), \((13/4,19/12)\), and action \((3/4,1/6)\). [check.py](producer-workspace/check.py) independently verifies this with rational arithmetic and exercises 4,096 floating draws: two queries each, maximum action error \(1.89\times10^{-15}\); zero-direction and zero-radius branches pass. [check_results.json](producer-workspace/check_results.json) records the actual result. These finite diagnostics supplement the algebra; they do not prove the distributional theorem.

The stronger properties have different scopes:

- **A common symmetric matrix:** the question does not assume conservativity, so even \(H_s(c)\) need not be symmetric. With conservativity, the mean is symmetric, but the realized direction-dependent secant generally is not a linear map of \(v\) ([R22 lines 377–379](https://github.com/harjassand/astra-research-knowledge/blob/6360a39d9488a041f259181e38c37e638b83c609/updates/DP/package/foundational_campaign/FINAL_ROUND/r22_polylog_mean_factory.txt#L377-L379)). For example, use conservative \(g(x_1,x_2)=(\sin x_1,0)\), \(c=0,s=1,Z_0=0,R=1\) with the same natural seeds: \(J(e_1)=(\sin1,0)\), \(J(e_2)=0\), but \(J(e_1+e_2)=(\sqrt2\sin(1/\sqrt2),0)\). The additivity defect is about \(0.0772544\); it persists in nearby seeds. In this affine fixture only, cancellation gives the common deterministic symmetric SPD matrix \(A\). A single queried action still does not identify a general unknown matrix.
- **Square roots and Gaussian completion:** unbiased actions or independent matrix-word estimates cannot be inserted as a realized common matrix into a covariance square root ([R22 lines 404–414](https://github.com/harjassand/astra-research-knowledge/blob/6360a39d9488a041f259181e38c37e638b83c609/updates/DP/package/foundational_campaign/FINAL_ROUND/r22_polylog_mean_factory.txt#L404-L414)). Even a symmetric Jacobian can be indefinite without convexity. R22's conservative latent filling \(Y=Dg(X)V+(L^2I-Dg(X)^2)^{1/2}W\) has an exact Gaussian marginal and conditional mean equal to the action, but **uses an unqueried Jacobian and the displayed covariance square root** ([lines 522–545](https://github.com/harjassand/astra-research-knowledge/blob/6360a39d9488a041f259181e38c37e638b83c609/updates/DP/package/foundational_campaign/FINAL_ROUND/r22_polylog_mean_factory.txt#L522-L545)). Independent Gaussian noise loses the required conditional coupling. In the affine SPD fixture one can calculate \(A\) and its root from the supplied matrix, but that extra data is not acquired by this generic two-call action.
- **Joint Gaussian law:** retaining a Gaussian source and matching cross moments is insufficient. For the scalar conservative example \(g(x)=\sin x\), \(c=0,s=1\), fresh Gaussian \(V\) yields \(J(V)=V\sin R/R\). Its conditional variance given \(V=v\) is \(v^2\operatorname{Var}(\sin R/R)\), excluding a joint Gaussian law for \((V,J)\). In the affine fixture \((V,AV)\) is jointly Gaussian, a special case. The more elaborate positive rotation in [R28 lines 33–142](https://github.com/harjassand/astra-research-knowledge/blob/6360a39d9488a041f259181e38c37e638b83c609/updates/DP/package/foundational_campaign/FINAL_ROUND/r28_multiscale_gaussian_mean.txt#L33-L142) preserves a **new** source/output product Gaussian pair; its **original** source/output pair has the useful heat-action cross moment but is not asserted jointly Gaussian. Exchanging the source removes the useful cross block. Its scalar quantile implementation also lacks a full bit-complexity certificate (lines 110–120).

Fresh seeds preserve \(\mathbb E[J(c_t;v_t)\mid\mathcal F_{t-1}]=H_s(c_t)v_t\) for centres/directions acquired from the past, and preserve the pointwise norm bound. For deterministic mean operators, fresh compositions estimate their ordered product with the product norm bound ([R22 lines 396–402](https://github.com/harjassand/astra-research-knowledge/blob/6360a39d9488a041f259181e38c37e638b83c609/updates/DP/package/foundational_campaign/FINAL_ROUND/r22_polylog_mean_factory.txt#L396-L402)). Adaptive later centres depending on the realized word do not automatically retain fixed-centre Gaussian convex-order domination ([lines 473–496](https://github.com/harjassand/astra-research-knowledge/blob/6360a39d9488a041f259181e38c37e638b83c609/updates/DP/package/foundational_campaign/FINAL_ROUND/r22_polylog_mean_factory.txt#L473-L496)); nor may one replace the random product by a fixed product of mean matrices. Reusing internal seeds needs its own conditional proof.

The corrections prevent stronger transfer: [R22 lines 284–335](https://github.com/harjassand/astra-research-knowledge/blob/6360a39d9488a041f259181e38c37e638b83c609/updates/DP/package/foundational_campaign/FINAL_ROUND/r22_polylog_mean_factory.txt#L284-L335) charges fourth cumulants from randomized covariance even after exact covariance matching. [R21 lines 219–227](https://github.com/harjassand/astra-research-knowledge/blob/6360a39d9488a041f259181e38c37e638b83c609/updates/DP/package/foundational_campaign/FINAL_ROUND/r21_polylog_mean_compiler.txt#L219-L227) clarifies that \(K(Y)P\) is not globally Lipschitz jointly in \(Y,P\). [R28 lines 144–230](https://github.com/harjassand/astra-research-knowledge/blob/6360a39d9488a041f259181e38c37e638b83c609/updates/DP/package/foundational_campaign/FINAL_ROUND/r28_multiscale_gaussian_mean.txt#L144-L230) refutes a frozen central-secant rotation using \(g_k(x)=\sin(kx)/k\); that failure does not refute the exact chi-three action. R22 lines 547–557 explicitly leave the finite positive full-law sampler and its every-execution polylogarithmic query cap unresolved. Those are real remaining acquisition and coupling obligations.

Actual navigation: read the assigned TASK_G, then public `00_START_HERE.txt`; ordinary `rg` found N687 and an attractive bounded-oracle Gaussian-mean card N722. Reading both showed N722 assumes iid bounded vectors and is not the needed derivative operation. N687 led to `updates/DP/package/foundational_campaign/FINAL_ROUND/`; I read the governing R22 sections, R28's rotation and failed flow, the scoped findings, and R21's explicit clarification. An initial `atlas*` shell glob failed; two guessed DP metadata paths did not exist. I corrected those paths and continued to the actual proof. Some broad search outputs were truncated, so decisive passages were reread in bounded line ranges. No scientific source access failed. All links pin the assignment's supplied public snapshot revision `6360a39d9488a041f259181e38c37e638b83c609`; I did not inspect history or independently fetch/verify that revision.

Actual prior exposure: the product supplied a general Astra memory summary, including generic Gaussian-construction/research-watch topic mentions and evidence-scope preferences. It supplied no task-specific action formula, N687/R22 identifier, expected answer, or affine result. I did not consult memory files, other chats, experiment protocols/expected scopes, other experiment workers, or generated retrieval projections, and used no retrieval engine. The proof reconstruction, general-Lipschitz extension, null repair, nonlinear witnesses and executed fixture check above were performed in this run. The retained sampler gap remains unresolved.
