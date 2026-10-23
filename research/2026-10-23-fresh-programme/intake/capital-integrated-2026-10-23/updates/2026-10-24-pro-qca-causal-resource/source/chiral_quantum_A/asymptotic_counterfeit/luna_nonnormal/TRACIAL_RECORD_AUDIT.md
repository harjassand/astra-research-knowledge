# Independent arithmetic audit of the tracial-record lower bound

Audited only `work/next_unit/root/TRACIAL_RECORD_POLYNOMIAL_BOUND.txt`; no source or frozen-note edits.

The stated conversion is consistent. For equal-trace projections, the normalized-trace identity is
\(\|P-Q\|_2^2=2\tau(P(I-Q)P)\). Applying it after the reference shift gives component defects at most \(\sqrt{2e}\). The joint full-cell rank-one projector defect is bounded by the sum of the two component defects, hence \(\delta=2\sqrt{2e}\) when both tested errors are at most \(e\).

In the compressed matrix-unit argument, \(F=P_aXP_b=E_{ab}D_0\) and \(\|X-F\|_2\le2\delta\). For each neighbor rank-one projector \(P_{jc}\), commutation with \(\alpha(P_{jc})\) gives \(\|[X,P_{jc}]\|_2\le2\delta\), and central-site compression preserves this bound. Re-embedding \(E_{ab}D_0\) contributes the factor \(1/\sqrt D\); the neighbor normalized 2-norm therefore incurs at most \(\sqrt D\). Pinching one dimension-\(D\) site costs at most \(2D\delta\) in the global normalized norm, so sequential pinching over \(K=2r\) sites yields the stated loose \(u=2(1+KD)\delta\). The diagonal clock average needs no inverse: its exact intertwiner identity gives \(\|\alpha(Y)-Y\|_2\le2KD\delta\). Since the final pinched \(D\) is diagonal, the displayed \(E_{bb}(D^*D-I)\) defect also controls the \(E_{ab}(DD^*-I)\) term in the composition.

The transpose step has the right order: \(\beta(E_{ab})\approx E_{ab}D^*\); thus \(\gamma=\alpha\beta\) has matrix-unit error \(4u+\delta+2KD\delta=(9+10KD)\delta=(9+20rD)\delta\). Transpose preserves support and index, giving radius at most \(2r\) and \(\operatorname{ind}\gamma=\operatorname{ind}(\alpha)^2\).

For the Choi step, a tensor Weyl on \(L=4r\) cells is a sum of \(D\) matrix units per site, so its normalized-2 defect is at most \(LDC\delta\). The EPR overlap/half-trace-distance conversion divides this by \(\sqrt2\), giving \(\epsilon=8rDC\sqrt e\). A radius-\(2r\) cut collar uses \(2r\) cells on each side, so each cross marginal has joint dimension \(D^{4r}\); the two collars fit inside the \(4r\)-cell Choi window. With maximally mixed marginals, Audenaert continuity gives \(I_{\rm cross}\le4r\log(D)\epsilon+h(\epsilon)\), as stated.

Finally \(\epsilon_0=\log(d_A)/(4r\log D)\le1/(4r)\le1/4\). At this point the index-one contradiction bound is at most \((\log d_A+\log2)/2\le\log d_A<2\log d_A\). Solving \(8rDC\sqrt e\le\epsilon_0\) reproduces exactly the displayed \(E_{\rm tr}\). Since \(C=9+20rD=\Theta(rD)\) for fixed local dimensions, its radius dependence is \(r^{-6}\) (with the stated additional dimension/log factors).

No constant optimization was attempted. The checks above concern the local reductions and arithmetic; the imported Choi index identity and entropy-continuity theorem remain conditional on the cited primary statements.
