# Attribution and prior work boundary

This is a bounded primary-source comparison, not a proof of novelty. The radius objectives, minimax machinery, harmonic optimizers, signed lifts, and observable-estimation interpretation are established ingredients. The exact arbitrary-reference coefficient identifications in this package were independently derived in this research; external review and historical priority remain open.

## Classical radii and ordinary contraction

Csiszár, *A class of measures of informativity of observation channels*, Periodica Mathematica Hungarica 2, 191–213 (1972), is an established source for f-informativity and no-prior radii: https://link.springer.com/article/10.1007/BF02018661 . Its full text was not available in the source review, so no harmonic-special-case priority or theorem number is attributed to it. Chen–Guntuboyina–Zhang, *On Bayes risk lower bounds*, Eq. (11), gives an accessible weighted f-informativity definition and credits Csiszár: https://arxiv.org/html/1410.0503 .

Mosonyi–Ogawa, *Divergence radii and the strong converse exponent of classical-quantum channel coding with constant compositions*, Appendix A, Proposition A.1, Eq. (A.66), supplies radius minimax under convexity and lower semicontinuity in the optimized argument: https://arxiv.org/html/1811.10599 . Applying it to reversed chi-square yields the relevant minimax. Its coding application is not the contraction result asserted here.

For classical columns t_i and a prior p, write H(p)=sum_y(sum_i p_i/t_i(y))^-1. Elementary quadratic minimization gives the weighted reverse-chi-square radius 1/H(p)-1. Thus the global reverse radius R and the present coefficient satisfy C=R/(1+R). The harmonic formula itself is an elementary specialization of established radius theory; the equality with the arbitrary-quantum-reference conditional coefficient requires the matching proof in this package.

Ordentlich–Polyanskiy, *Strong Data Processing Constant Is Achieved by Binary Inputs*, Theorem 2, establishes binary-input reduction for ordinary f-divergence contraction: https://arxiv.org/abs/2010.01987 and https://people.lids.mit.edu/yp/homepage/data/2020_binsdpi.pdf . The classical binary Le Cam formula is discussed in Polyanskiy–Wu, Appendix B: https://people.lids.mit.edu/yp/homepage/data/simple-IMA.pdf . Gu–Polyanskiy, Appendix A, Proposition 40, Eq. (231), supplies the ordinary symmetric-channel formula, including negative stochastic parameters: https://people.lids.mit.edu/yp/homepage/data/nlsi_potts.pdf . These ordinary results are credited prior work.

## Quantum reverse radii

Mosonyi–Bunth–Vrana, *Geometric relative entropies and barycentric Rényi divergences*, introduces general weighted left and right quantum divergence radii: https://arxiv.org/html/2207.14282 . The relevant general definition is in the introduction; the later Definition V.2 has a more specialized relative-entropy scope.

For M_p=sum_i p_i sigma_i^-1, minimizing Tr(omega M_p omega) over density matrices gives omega=M_p^-1/Tr M_p^-1 and value 1/Tr M_p^-1. This harmonic optimizer follows by elementary algebra in the established radius framework. It is not claimed as a newly invented objective.

Jeong–Kim, *Barycenter of the arithmetic-harmonic quantum divergence*, Electronic Journal of Linear Algebra 41 (2025), 236–247, studies exactly the binary arithmetic-minus-harmonic objective that appears in the two-state dual: https://journals.uwyo.edu/index.php/ela/article/download/8883/6985 . Pitrik–Virosztek, *Quantum Hellinger distances revisited*, Eq. (7) and Remark 1, provides earlier weighted Kubo–Ando/maximal-f context: https://arxiv.org/html/1903.10455 . Matsumoto, Section 6.4, relates the RLD quadratic metric and reverse estimation: https://arxiv.org/html/1311.4722 . None of these checked sources was found to state the full multi-input arbitrary-reference channel-coefficient identification here; that limited finding does not establish priority.

## Signed lifts and estimation

Zhu–Wang, *Quantum Incapacity beyond No-Cloning and PPT Mechanisms*, Definition 3.3, Proposition 3.4, and Remark 3.8, already defines reference-complete variance-dominating signed lifts, gives a CP-defect certificate, and explicitly interprets the lift as unbiased observable estimation with no larger variance: https://arxiv.org/html/2607.24693v2 . It also distinguishes observable estimation from simulation of POVM distributions.

Hirche, *Quantum estimation, channel orders, and private capacity*, Definition 3.1 and Theorem 3.2, connects signed lifts and complete measured chi-square order; Appendix A.1 gives a general converse for Hermitian-smoothed order. Proposition 2.1 gives the measured/SLD binary-MMSE relation: https://arxiv.org/html/2610.03706 . Its separately named quantum chi-square in Section 3.2 is BKM, not standard Petz/RLD.

The compiler in this package is an erasure specialization of that established framework. Its ordinary, unsmoothed complete-SLD necessity is separately proved with one coherent reference flag. The cited general smoothed converse is not used as a substitute for that proof.

## Conditional comparison and algebraic certificates

Hirche–George–Nuradha–Wilde supplies the conditional-erasure comparison framework: https://arxiv.org/html/2608.27171v1 . Its complete coefficient convention uses equal reference marginals; the present conditional Petz/RLD optimization explicitly permits unequal marginals.

Helton–Klep–McCullough, *The convex Positivstellensatz in a free algebra*, Theorem 1.1(1), supplies established degree-two certificate machinery: https://arxiv.org/abs/1102.4859 . Volcic’s generic rational theorem is also prior art: https://arxiv.org/abs/2101.02314 . The elementary proofs here do not need either general theorem. No generic machinery is claimed as new.

## Claims still requiring external review

The source comparison did not establish historical priority for the exact conditional RLD/radius identifications, sufficient reference bounds, or ordinary-complete erasure thresholds. It does establish substantial precedent for their component machinery. A small rational-data SDP is not an exact-P complexity theorem. Product-radius identities are standard additivity structure, not claimed as new additivity principles.

## Final contraction and correlation cross check

George–Tomamichel, *A Unified Approach to Quantum Contraction and Correlation Coefficients*, Section V-A Eq. (118), Sections V-B/V-C, Lemmas 67 and 76 and Eqs. (147)–(150), is a systematic comparator for monotone-metric chi-square, fixed-baseline contraction, generalized maximal correlation, and recovery-map/eigenvalue formulations: https://arxiv.org/html/2505.15281 . The harmonic metric member is RLD and the arithmetic member is SLD. The inspected coefficient fixes the input baseline; it does not optimize arbitrary correlated references with their information subtracted. Its coupling discussion also distinguishes relaxed Hermitian couplings from genuine positive state couplings.

George–Hirche–Nuradha–Wilde, *Quantum Doeblin Coefficients: Interpretations and Applications*, Section 6, Eq. (6.15), Proposition 30, and Proposition 34, Eq. (7.2), is close prior art for reference-stable bounds and CQ semidefinite optimization: https://arxiv.org/html/2503.22823 . Its CQ Doeblin quantity is the supremum of Tr X over Hermitian common lower bounds X <= sigma_i. That optimization is different from the inverse-quadratic radius in this package; its complete-contraction convention includes equal reference marginals.

For the positive common-lower-bound subcase only, a direct relation can be deduced. If 0 <= X <= sigma_i for every i, then X sigma_i^-1 X <= X. Substituting the free radius center U=X yields

Tr[(sigma_i-X)sigma_i^-1(sigma_i-X)]
=1-2Tr X+Tr(X sigma_i^-1 X) <= 1-Tr X.

Consequently C <= 1-Tr X. This shows how a positive common-lower-bound certificate supplies a sufficient bound within the radius minimization. It does not assert that the cited general Doeblin SDP requires X to be positive, and it is not presented as a new theorem of that source.

Temme–Kastoryano–Ruskai–Wolf–Verstraete, *The chi-square-divergence and mixing times of quantum Markov processes*, Section III.2 Eqs. (45) and (50), supplies older global ordinary and fixed-state spectral contraction background: https://arxiv.org/html/1005.2358 .

The final bounded comparison did not locate a decisive identification of the faithful-CQ harmonic radius with the arbitrary-reference, reference-subtracted coefficient, nor an exact primary statement of the supplied Pauli-XYZ preparation-family values. This remains a limited search outcome, not an absence proof or priority claim. The three-Pauli example is a classical-input prepared-state family, not a coherence-preserving qubit-input Pauli channel.
