# Equality and small-slack rigidity of an exactly protected encoder channel

Author: `producer-workspace/protected_algebra`, 2026-10-29.
Status: supplementary authored derivation; independent review pending. This is separate from the reviewed `algebra` main package and from the author's independent review of the sibling protection-reencoding theorem. No historical novelty claim.

## 1. Statement and operational premises

Let `n>=3`, let each physical site `A_i` have dimension `d>=2`, and let

\[
 \mathcal N:\mathcal B(\mathbb C^K)\longrightarrow
                 \mathcal B((\mathbb C^d)^{\otimes n})
\]

be any CPTP encoder. It may prepare a mixed gauge state, randomize without retaining a label, or discard a preparation environment. Assume that for **every** site `i` there is one CPTP decoder, independent of the logical input and of any unretained preparation label, such that

\[
 \mathcal D_i\operatorname{Tr}_{A_i}\mathcal N=\mathrm{id}_L. \tag{1}
\]

The decoder has only the remaining `n-1` physical sites. An additional noiseless register, an uncounted entanglement half, or a supplied preparation label changes this premise.

Put `h=log_2 d`, `k=log_2 K` and `Delta=(n-2)h-k`. Then:

1. `Delta>=0` (the quantum Singleton bound for this channel task).
2. If `Delta=0`, the encoder is an **isometric channel**. Discarded mixed gauge cannot remain at exact saturation under (1).
3. More generally, if `J` is its normalized Choi state, then

\[
 S(J)\le\frac{n}{n-2}\Delta. \tag{2}
\]

There is an isometric encoder `W` satisfying the same exact single-erasure recovery conditions for which

\[
 \tfrac12\|\mathcal N-\mathrm{Ad}_W\|_\diamond
       \le1-2^{-n\Delta/(n-2)}, \tag{3}
\]

This compares two encoder channels uniformly on all inputs and references; it is not a physical noise or workload estimate. The bound is sufficient; saturation of its entropy outer bound is not a claim of physical attainability at every slack. Exact erasure recovery in (1) has not been replaced by approximate recovery.

## 2. An exact total-correlation identity

Purify the normalized Choi state by a finite environment `E`, obtaining a pure state on `R A_1...A_n E`, with `R=I/K`. Dilate a decoder in (1). Its output on `R,L` is the pure maximally entangled state, so it factors from the other outputs. The untouched marginal therefore satisfies

\[
 \rho_{R A_i E}=I_R/K\otimes\rho_{A_iE} \quad\text{for every }i. \tag{4}
\]

In particular `R` and `E` are independent. Set `a_i=S(A_i)`, `b_i=S(A_iE)` and `e=S(E)=S(J)`, and use `A_bar_i` for all physical sites except `i`. Purity and (4) give

\[
 S(A_{\bar i})=k+b_i,\qquad
 S(E A_{\bar i})=k+a_i. \tag{5}
\]

For a list `X_1,...,X_m`, define total correlation and conditional total correlation by

\[
 \begin{split}
 C(X_1:\cdots:X_m)&=\sum_jS(X_j)-S(X_1\cdots X_m),\\
 C(X_1:\cdots:X_m|E)&=\sum_jS(X_j|E)-S(X_1\cdots X_m|E).
 \end{split}
\]

Both are nonnegative: the first follows by repeated subadditivity, the second is a sum of conditional mutual informations and follows by strong subadditivity. Individual conditional entropies may be negative; their total-correlation difference remains nonnegative.

For any chosen `i`, substitution of (5) proves the exact identity

\[
 \boxed{
 (n-2)\sum_{l=1}^n a_l-nk-(n-2)e
 =\sum_{j\ne i}C(A_{\bar j})+C(A_{\bar i}|E)\ge0 .}
 \tag{6}
\]

To verify coefficients, the first sum on the right is
`sum_(j!=i) sum_(l!=j) a_l -(n-1)k-sum_(j!=i)b_j`.
The conditional term is `sum_(j!=i)b_j-k-a_i-(n-2)e`.
Their sum is the left side. No symmetry of the physical state is assumed.

Thus the more informative form of the bound is

\[
 \boxed{\quad S(J)+\frac{n}{n-2}\log_2K
                  \le\sum_{i=1}^n S(A_i)\le n\log_2d.\quad} \tag{7}
\]

Nonnegativity of `S(J)` gives the quantum Singleton bound. Subtracting `n k/(n-2)` gives (2). At `Delta=0`, the Choi state is pure, so the CPTP encoder is an isometric channel. Simultaneously every site entropy is `log d`, hence each site is maximally mixed. No implication from a flat marginal to cut entanglement was assumed.

This identifies the discarded encoder's entropy as part of the storage budget. The equality case cannot hide an unrecorded mixed preparation/gauge state. Outside equality, (7) does not equate entropy with exact rank, heat, a quantum link rate, or time.

An initial valid but weaker `4 Delta` bound (`3 Delta` for `n=3`) was obtained by three-site mutual-information estimates. It is preserved in `history/first_entropy_bound/`. A finite entropy-cone diagnostic suggested replacing those pair estimates by (6). The identity is the proof; the diagnostic is not an entropy-region characterization or a physical attainability result.

## 3. Why the small-slack conclusion is uniform, not merely Choi-average

Write the spectral decomposition `J=sum_j p_j |psi_j><psi_j|`. For any erasure `i`, applying its fixed decoder gives the pure Bell state as the average of positive normalized outputs. Extremality forces **every** component to give that Bell state. Tracing the decoder output shows that every `psi_j` has `R=I/K`, hence is the normalized Choi vector of an isometry `W_j`. Each `W_j` obeys (1), using the same decoder for that erasure.

It follows that

\[
 \mathcal N=\sum_j p_j\,\mathrm{Ad}_{W_j}.
\]

Choose a component of largest weight `p_max`. Since `S(J)>=-log p_max`, (2) gives `p_max>=2^{-n Delta/(n-2)}`. Convexity and the unit upper bound on half-diamond distance imply (3). This avoids an unsupported dimension-independent Choi-to-diamond conversion: the exact reversibility premise supplies the decomposition into full-input isometric channels.

The nearest-isometry metric is in fact exact:

\[
 \min_{W\ \mathrm{isometry}}\frac12
       \|\mathcal N-\mathrm{Ad}_W\|_\diamond=1-p_{\max}. \tag{8}
\]

The preceding convexity argument gives the upper bound, attained by a largest-weight component which retains the same erasure decoders. For any other isometry with normalized Choi vector `w`, its target-projector test gives `T(J,|w><w|)>=1-<w|J|w>>=1-p_max`. The half-diamond distance is at least this Choi trace distance. This proves the lower bound even when the candidate isometry is not itself erasure-correctable. Equation (8) was supplied as a refinement by `producer-workspace/classical_capacity` during review coordination; that agent must not claim independent validation of its own contribution.

The argument is existential given a complete channel description. Finding and implementing `W_j`, supplying its fresh space, and calibrating controls are separate acquisition obligations.

Equations (3) and (8) compare the encoder's `n` physical output sites, with an arbitrary logical reference. They do not prescribe the returned preparation environment or its records. A comparison that also retains a particular purification of that environment can instead have a square-root dependence on `1-p_max`; the data-channel optimum must not be transferred to that stronger interface.

## 4. Sharp scope controls

- `n=2,K=1` formally saturates `K=d^(n-2)`, but a fixed product-state encoder is allowed and its sites need not be maximally mixed. A mixed fixed output is also allowed. This is why `n>=3` is essential.
- Below saturation, exact mixed encoders exist. A three-qutrit erasure code carrying one qutrit, tensored with an independent maximally mixed fourth site, corrects every single-site erasure. Every physical site is maximally mixed, but the fourth site's cut is product. Flat marginals alone are insufficient.
- Forgetting which of two individually correctable isometries was used does not ensure a common decoder. For the [[4,2,2]] code, mixing `V` and `Z_A V` dephases `A`, making that cut separable. After erasing `B`, orthogonal logical inputs become identical. The mixed encoder violates (1).
- Supplied noiseless side information, external quantum shares and known record-dependent decoders can change the resource count. Apply the theorem to each actual record branch only when its normalized encoder is CPTP on the full logical input and has the required common decoders.
- This lemma does not prove a cumulative cost per fresh replacement. A product spare can rotate into later coherent helper access; that reconnection and old-partner retirement must be charged.

Exact controls for these boundaries are in `p2_flow/reviews/protection_reencoding/independent_reencoding_audit.py`. That executable was independently authored for the sibling review. It tests the stated finite controls, not this general entropy proof. The present supplementary theorem still requires a separate reviewer.

## 5. Primary ancestry and priority scope

The quantum Singleton argument and purification of mixed encoding maps are established tools. Relevant primary sources read selectively:

- D. Gottesman, *On the Theory of Quantum Secret Sharing*, https://arxiv.org/pdf/quant-ph/9910067, Theorems 1 and 3 and the latter's purification proof. Its perfect-access-structure restrictions are not silently imposed on the present general erasure-code task.
- A. Klappenecker and P. K. Sarvepalli, *On Subsystem Codes Beating the Hamming or Singleton Bound*, https://arxiv.org/pdf/quant-ph/0703213, subsystem definitions and Theorem 3.6 statement/proof. The fetched source's stated theorem is for F_q-linear Clifford subsystem codes; it is not cited as a proof for arbitrary CPTP encoders here.
- S. A. Aly, A. Klappenecker and P. K. Sarvepalli, *Subsystem Codes*, https://arxiv.org/pdf/quant-ph/0610153, Theorems 11, 19 and 20 and their proofs. The gauge-dimension Singleton bound there is for pure Clifford subsystem codes; its exact-saturation exclusion is also stated for Clifford subsystem codes. A code being **pure** in that literature means vanishing low-weight traceless expectations, not that an arbitrary encoder channel has Kraus rank one.
- M. Grassl, F. Huber and A. Winter, *Entropic proofs of Singleton bounds for quantum error-correcting codes*, https://arxiv.org/pdf/2010.07902v4, Theorem 1, Lemmas 2-3, Corollary 4, Theorem 5 and its proof, and the general-encoder reduction in the proof of Theorem 6, equations (36) and surrounding discussion. Theorem 5 explicitly permits arbitrary CPTP encoders with a discarded output `F`; the pure-component/common-decoder reduction used in Section 3 is already present there. Their conditional entropy averaging is a strong conventional basis for (6), not evidence that mixed encoders were previously unaddressed. The displayed source theorems do not by themselves give a general bound `log K+log rank J <= (n-2) log d`; no pure/Clifford rank theorem is imported to assert such a bound here.
- C. Crepeau, D. Gottesman and A. Smith, *Secure Multi-party Quantum Computation*, https://people.csail.mit.edu/asmith/PS/vqssG.pdf, Appendix B.2. It explicitly includes mixed-state encoders in its stated correction/no-cloning boundary; no new priority for a mixed-state Singleton obstruction is claimed here.

The equality consequence, entropy accounting and nearest-isometry interface above were derived to resolve an operational challenge. Their appearance elsewhere has not been exhaustively investigated. The quantified result is a sufficient general-channel consequence of established entropy machinery. Where a stronger applicable gauge-rank theorem is supplied, it should replace this sufficient allowance. No claim of an optimal general coding bound, new historical priority or device advantage follows from this note.
