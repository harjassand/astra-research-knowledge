# Focused review: the asymptotic iid coherent-information optimum

**Reviewer:** quantum_walk_comparison.  
**Actual source reviewed:** ../IID_INFORMATION.tex, including its corrected opening entropy argument, and the relevant statements in ../ENTROPY_AND_SCOPE.tex and ../COHERENT_INPUT_ESCAPE.tex. The inherited exact depth law was checked in ../../cycle2/COHERENT_CAPACITY_FLOOR.tex.  
**Scope:** Purification, information inequalities, the uniform dependence on the single-site marginal, the matching critical-input lower limit, and the interpretation of the result. The separate corrector identity and entropy-flow proposition are dependencies; this review does not repeat their full independent audits.

## Verdict and exact statement

The stated theorem is correct conditional on the supplied corrected-drift theorem. For every fixed \(0\le\beta\le1/8\), with the one unchanged actual initializer \(\tau_\pi\), it proves

\[
 \lim_{n\to\infty}\frac1n
 \max_{\rho\in\mathcal D(\mathbb C^3)}
 I_c(\rho^{\otimes n},\mathcal N_n^{\tau_\pi})=\frac32.
\]

The upper estimate is uniform in \(\rho\), so the maximizer may change with \(n\). This is an exact **asymptotic iid/tensor-power coherent-information value**. It does not assert equality of the finite-\(n\) maximum to \(3n/2\).

The displayed input set is essential. Independent but nonidentically distributed products \(\bigotimes_{j=1}^n\rho_j\) are not included by the proof, and neither are arbitrary temporally correlated inputs or feedback protocols. The source explicitly restricts each block to a tensor power. Titles and external summaries should retain “iid” or “tensor power,” rather than allowing “independent inputs” to suggest a larger maximization.

No substantive gap remains in the reviewed section. The draft's initial shorthand attribution of \(I_c\le2S(B^n)-nS(\rho)\) to (E5) was replaced in the actual source by the correct unitary-invariance and joint-subadditivity argument. That replacement has been checked.

## 1. The mixed-bath purification is treated correctly

Let \(F\) purify the fixed initial bath, and let \(R_{\rm in}\) purify the input \(\rho^{\otimes n}\). The initial state on \(R_{\rm in}A^nEF\) is pure, and the device is unitary on \(A^nE\). Its final state on \(R_{\rm in}B^nE_nF\) is therefore pure. The complete complementary output is \(E_nF\), not \(E_n\) alone, and

\[
 I_c=S(B^n)-S(E_nF)
     =S(B^n)-S(R_{\rm in}B^n).
\]

The purification is an analytical representation of the already specified channel. It neither makes \(F\) accessible nor adds an external-purification-return requirement.

All the relevant entropies are finite. The input and output port spaces, and \(R_{\rm in}\), are finite dimensional for fixed \(n\). Thus \(S(E_nF)=S(R_{\rm in}B^n)\) is finite directly. Also \(S(F)=S(\tau_\pi)<\infty\), and the finite-dimensional per-call dilation ensures finite bath entropy at every finite horizon. There is no subtraction of undefined infinite entropies.

The spectator \(F\) keeps its marginal entropy \(S(\tau_\pi)\). Unitary invariance after tracing \(R_{\rm in}F\) gives

\[
 S(B^nE_n)=nS(\rho)+S(\tau_\pi).
\]

Subadditivity and Araki–Lieb then give

\[
 S(E_nF)\ge S(E_n)-S(F)
 \ge nS(\rho)-S(B^n).
\]

Consequently

\[
 I_c\le2S(B^n)-nS(\rho). \tag{R1}
\]

This uses the actual joint output entropy and preserves all output correlations. It does not treat the outgoing ports as independent.

There is also the general input-entropy ceiling

\[
 I_c\le S(R_{\rm in})=nS(\rho), \tag{R2}
\]

obtained from \(S(R_{\rm in}B^n)\ge S(B^n)-S(R_{\rm in})\). These two inequalities are both valid for the same purified mixed-bath channel.

## 2. The fixed-input strict upper bound

Take \(S(\rho)=3/2+\epsilon>3/2\), put \(q=\rho_{00}=1/2-\delta\), and use the spectral-window theorem, which implies \(\delta>0\). The reviewed section relies on the previously proved bounded corrector with

\[
 \operatorname{Tr}L(\tau_n-\tau_\pi)\ge\nu n-2M,
 \qquad \nu\ge\frac32\delta
\]

for \(0\le\beta\le1/8\). Conservation and the outgoing-port entropy estimate (E4) imply

\[
 S(B^n)\le n(2-q)-\operatorname{Tr}L(\tau_n-\tau_\pi)
 \le n\left(\frac32+\delta-\nu\right)+2M.
\]

Substitution into (R1) gives

\[
\begin{split}
 I_c
 &\le n\left(\frac32+2\delta-2\nu-\epsilon\right)+4M\\
 &\le n\left(\frac32-\delta-\epsilon\right)+4M.
\end{split} \tag{R3}
\]

For a fixed high-entropy density the correction is finite, so division by \(n\) gives the source's strict asymptotic inequality below \(3/2\). This is stronger than merely showing failure of a chosen bath-compression proof for that density.

The factor \(4M\) is correct: the depth telescoping error is \(2M\), and the output-entropy bound is used twice in (R1).

## 3. The horizon-dependent marginal is genuinely controlled

A pointwise statement with an unspecified \(M_\rho\) would not justify moving the maximization inside the limit. Here the explicit corrector bound closes that obligation.

The source definitions and spectral window give

\[
 M=\frac{2\beta\|f\|}{\alpha(1-r)},\qquad
 r=\frac q{1-q},\qquad
 \|f\|\le6\|g\|,\qquad
 \|g\|^2\le\frac{\delta}{3}.
\]

Since

\[
 1-r=\frac{2\delta}{1/2+\delta},
\]

the actual substitution yields

\[
 M\le
 \frac{2\sqrt3\,\beta(1/2+\delta)}{\alpha\sqrt\delta}
 \le\frac{2\sqrt3\,\beta}{\alpha\sqrt\delta}
 \le\frac1{\sqrt\delta}. \tag{R4}
\]

The last inequality is uniform on the full stipulated interval:

\[
 \frac{2\sqrt3\,\beta}{\sqrt{1-\beta^2}}
 \le\frac2{\sqrt{21}}<1
 \quad (0\le\beta\le1/8).
\]

Pinching the single-site input into its zero/color blocks, followed by maximization of the two-dimensional color entropy, gives

\[
 S(\rho)\le h_2(q)+1-q\le\frac32+\delta.
\]

Combining this with (R2), and combining (R3) with (R4) while dropping its favorable negative terms, gives

\[
 \frac{I_c}{n}-\frac32
 \le\min\left\{\delta,\frac4{n\sqrt\delta}\right\}.
\]

For any \(a>0\),

\[
 \sup_{\delta>0}\min\{\delta,a/\sqrt\delta\}=a^{2/3}.
\]

Indeed, below \(\delta=a^{2/3}\) use the first term, and above it use the second. With \(a=4/n\), this proves the uniform bound \((4/n)^{2/3}\).

Inputs with \(S(\rho)\le3/2\) satisfy the ceiling directly by (R2), so there is no division by a vanishing \(\delta\) on the entropy boundary. In particular, an arbitrary sequence \(\rho_n\) may move between the high-entropy and low-entropy branches as \(n\) varies, without invalidating the estimate.

For fixed \(n\) the maximum exists. One can express the complementary entropy as \(S(R_{\rm in}B^n)\), using a canonical finite-dimensional purification of the input. Coherent information is then continuous in the finite-dimensional input density, and \(\rho\mapsto\rho^{\otimes n}\) is continuous on a compact domain. The infinite-dimensional bath causes no discontinuity loophole in this maximization.

## 4. The critical bath assertion retains the root exchange

Let

\[
 \rho_c=\operatorname{diag}(1/2,1/4,1/4),
 \qquad d_\ell=2^{\ell+1},
 \qquad
 \tau_j=\sum_{\ell\ge0}\frac{p_j(\ell)}{d_\ell}P_\ell.
\]

The actual initial \(\tau_\pi\) has this form with

\[
 p_0(\ell)=\frac23\,3^{-\ell}.
\]

At a diagonal zero/color input the exact reduced bath map is

\[
\begin{split}
 \Phi_q(\tau)={}&
 \alpha^2\left[q\left(R\tau R+\sum_aS_a^\dagger\tau S_a\right)
       +\frac{1-q}{2}\sum_aS_a\tau S_a^\dagger\right]
       +\beta^2\tau\\
 &+i\alpha\beta q(\tau R-R\tau).
\end{split}
\]

A density scalar on each depth level has equal weights on the two vacua and hence commutes with \(R\). The displayed coherent root term therefore vanishes for this trajectory. The push and pop sums preserve scalarity on each depth level, and \(R\tau R\) preserves equal vacuum weights. This establishes the assertion by induction; the root exchange is retained, not discarded.

More explicitly, for general diagonal \(q\), the radial probabilities satisfy

\[
\begin{split}
 p_{j+1}(0)
   &=(\beta^2+\alpha^2q)p_j(0)+\alpha^2q\,p_j(1),\\
 p_{j+1}(\ell)
   &=\beta^2p_j(\ell)
     +\alpha^2\big[(1-q)p_j(\ell-1)+q\,p_j(\ell+1)\big],
       \qquad \ell\ge1 .
\end{split}
\]

At \(q=1/2\), this is the stated symmetric lazy reflected walk. In particular, a held downward step at zero is part of the exact kernel.

For a positive depth \(\ell\), the conditional increment of \(L^2\) is \(\alpha^2\); at zero it is \(\alpha^2/2\). Thus

\[
 \mathbb E L_{j+1}^2-\mathbb E L_j^2
 =\alpha^2\left(1-\frac12p_j(0)\right)\le\alpha^2.
\]

The initial geometric depth has second moment one. It follows that

\[
 \mathbb E L_n^2\le1+\alpha^2n,\qquad
 m_n=\mathbb E L_n\le\sqrt{1+\alpha^2n}.
\]

This uses an exact reduced observable identity. It does not assign classical move/stay probabilities to the full coherent device on arbitrary input states.

## 5. Sublinear bath entropy and the matching information lower limit

For a nonnegative integer law of mean \(m\), nonnegativity of relative entropy to the geometric law of that mean gives

\[
 H(L)\le (m+1)\log_2(m+1)-m\log_2m
       \le\log_2(e(m+1)).
\]

The \(m=0\) case is the point mass and is treated directly. Because the critical bath is uniform on the \(d_\ell=2^{\ell+1}\) coordinates at depth \(\ell\), including both seeds,

\[
 S(\tau_n)=H(p_n)+\sum_\ell p_n(\ell)\log_2d_\ell
          =H(p_n)+1+m_n.
\]

Consequently

\[
 S(\tau_n)
 \le1+\sqrt{1+\alpha^2n}
       +\log_2\!\left(e(1+\sqrt{1+\alpha^2n})\right)
 =O(\sqrt n+\log n)=o(n).
\]

There is no missing seed entropy: it is the displayed \(+1\). One could obtain the same upper bound by pinching and maximizing each depth block even without exact radiality; the exact radial evolution here establishes the stated equality as well.

Finally, unitary invariance and subadditivity give

\[
 S(B^n)\ge\frac32n+S(\tau_\pi)-S(\tau_n),
 \qquad
 S(E_nF)\le S(\tau_n)+S(\tau_\pi).
\]

The fixed bath-purification entropy cancels, giving

\[
 I_c(\rho_c^{\otimes n},\mathcal N_n^{\tau_\pi})
 \ge\frac32n-2S(\tau_n).
\]

This supplies the matching lower limit for the same fixed device and same physical initializer. No horizon-dependent bath, reset, added bath access, or bath-return condition is used.

## 6. Scientific interpretation and review limits

The result closes the possibility of raising the asymptotic iid coherent-information value above \(3/2\), including by selecting a more favorable single-site density separately at every horizon. For each fixed input density of entropy strictly greater than \(3/2\), the reviewed upper bound is strictly below \(3/2\).

This is not a quantum-capacity converse. A code's average input need not be an iid density, and the full block coherent-information maximization is over a much larger set than \(\{\rho^{\otimes n}\}\). Nor does this theorem address the stronger independent nonidentically distributed product family. The inherited constructive capacity floor remains a separate coding result with its own arbitrary-reference error guarantee.

The independent review is analytic. It included reading the actual completed source and the relevant inherited exact bath map; no finite simulation, broad literature audit, external communication, paid resource use, or upload was needed. The source of the crucial drift estimate remains the separately reviewed corrector theorem. Exact review wall time and cumulative discovery cost were not instrumented and are unknown. This is internal correctness assessment, not external certification, historical-priority certification, or a physical-performance claim.
