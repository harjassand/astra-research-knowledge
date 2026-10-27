# Independent receipt: two physical reset blocks, noncommuting logical baths

Status: PASS, 2026-10-26. Governing proof: `two_physical_block_mixed_reset_value_theorem.md`, with actual-source expansion in `rank_two_physical_block_reset_three_degree_reduction.md`.

## Actual scope and source factors

The received class is E(rho)=p rho tensor sigma+q Tr(rho)tau, tau=P1 tensor T1+P2 tensor T2, where the two physical projections are orthogonal rank-one projections, T1,T2 are arbitrary PSD logical matrices, and Tr(T1+T2)=1. No pair among sigma,T1,T2 must commute. This includes correlated but physically block-diagonal reset states. It does not include physical off-diagonal coherence or a third physical block.

Set S=p sigma/3, Qi=q Ti/3. The input success sector has weight 3S and overlap amplitude 1/sqrt(3) with each of two mutually orthogonal reset sectors Qi. Eliminating the reset blocks yields the sum P_Q1+P_Q2 with coefficient 1/3, not a resolvent of Q1+Q2. The marginal has two independent full-overlap blocks S,3Qi. In the normalized WH output the antisymmetric pair joining the two reset labels overlaps both reset sectors with amplitude 1/sqrt(2); each of the other two pairs overlaps one sector with that amplitude. Relative signs on the joining pair disappear in the Schur complement because the reset blocks are orthogonal. The entropy coefficient -2 therefore gives exactly beta=2^(1-n) multiplying the combined and separate trace powers in degree n. All uncoupled spectators cancel against the orthogonal-reference baseline. The reset component has zero deficit because its input physical factor is I3/3, not because tau is pure or logically commuting.

## Summed-bath reciprocal theorem

The Zhang input was already independently verified at [arXiv:1811.01205v2, Theorem 1.1(2)](https://arxiv.org/pdf/1811.01205v2). Its stated invertible-K hypothesis is correctly extended to the displayed singular square K by invertible K_epsilon and continuity of positive trace powers. This limit is taken pointwise first, preserving convexity; no uniform inverse-K estimate is needed.

Writing A0=I+us S^-1 and Bi=I+vs Qi^-1, the nonzero spectrum of B^-1/2 K* diag(A0^-1,A0^-1) K B^-1/2 is that of A0^-1/2(B1^-1+B2^-1)A0^-1/2. Thus the fixed-K theorem applies to precisely the desired sum of resolvents. Integration gives convex F(u,v), and the common change of integration variable gives degree -1 homogeneity. The previously received positive-convex/negative-homogeneous reciprocal lemma consequently yields the stated midpoint inequality.

For finite dimension, a bound of the form d min(2,C/s²)^n is uniform under common epsilon-identity regularization, with C depending only on fixed bounded source norms and fixed inverse-scale parameters. It is integrable for n>1/2. This receives singular S,Qi and also a vanishing bath. The division-free reciprocal inequality is used before taking limits. If the combined overlap is nonzero, all three combined integrals are positive; if it is zero all vanish. No ratio 0/0 is asserted.

## Low degrees: the same positive quantity is used twice

For n=2,3,4, define D=alpha A+b exactly as in the governing note. Positive-sandwich trace superadditivity gives A>=sum I_n(3S,Qi). The given mixed-word expansions justify superadditivity for these degrees: Tr U²V² and Tr UVUV are nonnegative for PSD U,V, as are the simpler cubic/linear mixed traces. Applying the separate reciprocal inequalities and weighted Cauchy yields D>=K1 c.

Trace-power convexity gives the combined scaled-bath integral <=2^(n-1)b. The combined reciprocal theorem and weighted Cauchy then yield D>=K2 C. These are simultaneous lower bounds on one D; therefore beta(C+c)<=beta(1/K1+1/K2)D. This is not an illegitimate sum of two budgets. All quantities and multipliers are nonnegative.

Independent exact SymPy simplification verified each displayed theta expression and its rational upper bound obtained from sqrt2>7071/5000 and sqrt3>433/250. The lower rational square-root bounds follow by squaring. The resulting upper bounds 242763/245000, 41556033/44700500, 24165027/26645000 are all strictly below one. Thus each low-degree numerator is >=(1-theta_n)D>=0, strictly positive when D>0.

## Remaining degrees, convergence and equality

For n>=5, the two scaled trace powers dominate their unscaled versions by positive-sandwich eigenvalue monotonicity. The combined sandwich obeys J<=2^(n-1)c by trace-power convexity. Since alpha-beta<0, substituting that UPPER bound has the correct inequality direction and gives [2^(n-1)/3^n-2^(1-n)]c>=0. The scalar condition is (4/3)^n>=4, valid from n=5 onward.

Degree one is exactly the sum of the two previously received pure-physical scalar linear resources K(S,Qi). It is strictly positive if S(Q1+Q2) is nonzero. Each underlying coherence log series has nonnegative terms and finite integral equal to its finite entropy loss. The finite signed collection is therefore absolutely summable after integration, so regrouping by degree is legitimate even at full-overlap/singular boundaries. No pointwise positivity of low degrees, complete monotonicity, or scalar spectral lifting is presumed.

All higher integrated degrees are nonnegative. Hence equality holds exactly when pq=0 or sigma(T1+T2)=0. For the converse, PSD order Qi<=Q1+Q2 implies each individual support overlap vanishes when the combined one vanishes, and all series are zero. Strictness is obtained from actual positive spectral overlaps, not passage of a strict inequality through a singular limit.

## Replay and limitations

Replayed `rank_two_physical_block_reset_source_check.py`: PASS, 40 complex sources, maximum discrepancy 2.78e-15. The numerical replay is supplementary; the actual Gram and analytic inequalities above receive the proof.

No operational add-on was present at this review, and none is inferred here. The theorem receives two orthogonal physical blocks with arbitrary logical baths, not arbitrary physically coherent or three-block reset states and not unrestricted WH3.

Cross-receipt: the separate scaling-worker audit `two_physical_block_summed_bath_reciprocal_audit.md` also reports PASS for the exact fixed-K orientation, limits, same-D payments and radical constants. No pending receiving dependency remains for this scoped whole-value theorem.
