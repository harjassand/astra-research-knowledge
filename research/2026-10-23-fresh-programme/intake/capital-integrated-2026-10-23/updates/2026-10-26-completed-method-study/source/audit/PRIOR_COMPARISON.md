# Q28: comparison after additional prior-source exposure

This addendum was written **after** the completed pre-exposure REVIEW.md and DERIVATION.md. Those files and their checks are preserved unchanged; hashes are recorded in checks/post_exposure_manifest.json. The added exposure consists of the supplied PRIOR_SOURCES_AFTER_OUTPUTS.txt and its exact N965.md, N970.md, and N676.tex copies. N965/N970 are dated 24 October 2026; N676 is dated 11 October. I use the supplied version-bound internal acceptance of N965/N970 at their actual scope. No outside-specialist prerequisite is imposed. N676's quadratic cutoff is a standalone proof, independent of its separately qualified nonlocal-game/hardness discussion.

**Revised originality assessment:** Q28's arbitrary-classical-channel equality and binary theorem were already established in these earlier sources. Its valid remaining increment relative to the displayed prior statements is an **explicit bounded noncommutative formula and finite-reference/real-algebraic corollary for conditional Umegaki comparison of classical channels**. N676 already supplies the inverse-action compression and quantifier-elimination operations, but at a different metric/interface. Thus neither “the entire theorem is new” nor “N676's endpoint theorem already states the same Umegaki result” is supported.

| Frozen or reviewer claim | Exact earlier claim and operation | Assessment after exposure |
|---|---|---|
| Q28: conditional and equal-reference-marginal Umegaki comparison agree for arbitrary finite classical K,L | N965:5–18,24–41 gives exactly this equivalence for every finite c, arbitrary finite references, differing output alphabets, and finite divergence terms; it also equates these comparisons with complete equal-marginal SLD comparison | **Exact prior result**, including zero-denominator handling. This is not a new Q28 bridge beyond binary inputs |
| Q28: two-input scalar formula, with no quantum-reference improvement after optimizing all priors | N970:13–35,37–50 uses one normalized positive SLD superoperator and spectral calculus, including two arbitrary binary-input channels and degeneracies | **Exact prior result**. The global-prior and classical-input restrictions agree |
| Q28: arbitrary-input free inverse-quadratic formula and reference bound n+m_K+m_L | N965 supplies the all-classical Umegaki/SLD reduction but does not display this free formula/cutoff. N676:245–371 proves reference bounds 1+b² and 1+v for complete Petz D2 dominance through RLD quadratic forms | The explicit **classical conditional-Umegaki cutoff/formula** is not literally supplied by those theorem statements. Its compression mechanism has a strong prior antecedent; the metric transfer must still be justified |
| Q28: rational-channel finite coefficient is algebraic; rational thresholds decidable in principle | N676:355–363 already encodes finite quadratic comparisons using real coordinates, positivity, inverse variables, and real quantifier elimination | No new decision method. Q28's Umegaki-classical conclusion is a correct corollary of its finite free representation; algebraicity of a finite threshold boundary is an additional routine semialgebraic consequence |
| My pre-exposure refinement: preserve F_K, decrease F_L, reference bound n+m_K | N676:298–335 preserves target inverse solutions exactly and decreases source terms by the inverse variational principle | **Same proof operation**, independently reconstructed before exposure. Its application to Q28's free Umegaki representation is separately scoped; it has no claim to a new compression principle |

## Why the metric distinction matters

N676 concerns $D_2(A\Vert B)=\log\operatorname{Tr}A^2B^{-1}$ and $\mathcal G_A(H)=\operatorname{Tr}HA^{-1}H$. Its exact expansion is $1+t^2\mathcal G_A(H)$, so monotonicity of the logarithm identifies **unit-constant order** with RLD quadratic order. It does not identify arbitrary multiplicative D2 coefficients with RLD coefficients, or establish a Umegaki cutoff for general quantum-input POVMs. Its mathematical cutoff also allows nonzero singular effects (366–371), while its stated rational decision theorem names strictly positive POVMs.

These metrics are not pointwise interchangeable. For a Hermitian off-diagonal entry h between baseline eigenvalues a,b, their contributions are respectively

\[
|h|^2(1/a+1/b),\qquad
\frac{4|h|^2}{a+b},\qquad
2|h|^2\frac{\log a-\log b}{a-b}
\]

for RLD, SLD, and BKM. Equality of a globally optimized comparison can hold without equality of these values.

There is nevertheless a short explicit connection to the accepted N965 result. At an equal-marginal cq SLD baseline, normalize the positive superoperators $\Omega_{A_i}$ by $\Omega_{\sum_i A_i}^{-1/2}$. This produces positive Q_i summing to identity and zero-sum vectors u_i; its output metric is Q28's F_K. Conversely, arbitrary free Q,u are realized in the limit by Q28's active/vacuum blocks

\[
\sigma_i^\epsilon=(1-\epsilon)Q_i/d\oplus\epsilon p_i,\qquad
H_i=\begin{pmatrix}0&u_i\\u_i^*&0\end{pmatrix}.
\]

Here $\sum_iH_i=0$, and direct diagonalization gives

\[
\frac{g^S_{K\sigma^\epsilon}(KH)}{4d}\longrightarrow F_K.
\]

Thus N965 plus this elementary free-witness realization recovers the free **coefficient** formula. To obtain Q28's dimension bound for actual Umegaki witnesses without a further Liouville-space enlargement, its directly checked BKM boundary calculation is still needed:

\[
\frac{g^{BKM}_{K\sigma^\epsilon}(KH)}
 {2d\log(1/\epsilon)}\longrightarrow F_K.
\]

This is an explicit specialization of the active/vacuum and metric-transfer mechanism already used by N965:26–35, not evidence for a new equality principle. It is also the precise extra connection required before N676's inverse-action method can be used for Q28's metric/domain. Merely calling both arguments “compression” would not establish it.

## What the earlier compression does to the refinement

The correspondence is exact at the inverse variational step: in the violation $F_K>cF_L$, preserve the K numerator as N676 preserves its target; permit the L source to decrease. The nonnegative factor c does not change that monotonicity. Q28's original symmetric span preserves both forms, whereas my earlier refinement implements N676's one-sided version with an unnecessarily large span containing the u_i.

A **post-exposure reviewer inference**, not frozen-output credit, makes the comparison sharper. In the free domain take only

\[
S=\operatorname{span}\{(W_y^K)^{-1}v_y^K:y=1,\ldots,m_K\},
\quad Q_i'=PQ_iP|_S,\quad u_i'=Pu_i.
\]

The projected vectors still sum to zero. Since each numerator inverse solution lies in S, $(PW_y^KP)|_S^{-1}Pv_y^K=(W_y^K)^{-1}v_y^K$, and F_K is preserved. For every denominator term,

\[
(Pv)^*(PWP|_S)^{-1}(Pv)
=\sup_{z\in S}\{2\operatorname{Re}v^*z-z^*Wz\}
\le v^*W^{-1}v.
\]

Consequently active dimension at most m_K, followed by the already checked Umegaki vacuum lift, suffices: reference dimension **m_K+1**. The zero numerator case is trivial. This has the same outcome-count dependence as N676's POVM cutoff, now with the explicit classical-Umegaki bridge above. It is a specialization using the prior operation, not a repaired Q28 result, not a new researcher contribution, and not an alteration of my pre-exposure n+m_K refinement. Twelve post-exposure numerical diagnostics are retained in checks/post_exposure_checks.json; the displayed proof, not those tests, establishes the implication.

The pre-exposure correctness judgment therefore stands. Originality of the equality/binary subclaims is decisively excluded relative to N965/N970. The residual mathematically valid increment is the explicit finite free representation/cutoff and its computability consequence **at the conditional Umegaki, finite classical-input channel-pair interface**, assembled from closely preceding proof operations. Its exact historical priority remains unestablished; the supplied earlier statements do not by themselves erase this metric-specific consequence. These sources provide no basis for assigning new operation or breakthrough credit to the broad equality claim, the compression principle, or real quantifier elimination.

Exact supplied source locations: [N965.md](/Users/harjas/Documents/ChatGPT/coordination/work/astra-method-experiment-20261026/public/prior_sources_after_outputs/N965.md:5), [N970.md](/Users/harjas/Documents/ChatGPT/coordination/work/astra-method-experiment-20261026/public/prior_sources_after_outputs/N970.md:37), [N676.tex](/Users/harjas/Documents/ChatGPT/coordination/work/astra-method-experiment-20261026/public/prior_sources_after_outputs/N676.tex:245), and [post-output source manifest](/Users/harjas/Documents/ChatGPT/coordination/work/astra-method-experiment-20261026/public/PRIOR_SOURCES_AFTER_OUTPUTS.txt:1).
