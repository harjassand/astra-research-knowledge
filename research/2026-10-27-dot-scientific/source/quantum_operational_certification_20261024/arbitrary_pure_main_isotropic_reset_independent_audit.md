# Independent whole pure-main/isotropic-reset VALUE audit

26 October 2026. **PASS for the corrected canonical theorem** `arbitrary_pure_main_isotropic_reset_whole_value_theorem.md`. The statement is Delta(|psi><psi|+I_3 tensor Y)>=0 for every finite reference, arbitrary pure main psi and arbitrary PSD reset Y. It is NOT an unrestricted mixed-main entropy inequality, a charged decoder theorem, an equality classification or an extraction rate.

## Actual source and homogeneous normalization

Write psi=sum_i |i>v_i and K(s)=Psi*(Y+sI)^-1 Psi. The input rank-one determinant ratio is1+TrK. The reference ratio relative to3Y is det(I+K(s/3)/3). Using the three antisymmetric Werner-Holevo Kraus operators, the reset-resolvent Gram of the three actual output vectors is(TrK I-K^T)/2. This retains the complex transpose; its determinant equals the untransposed spectral expression. Reset-only Delta is exactly zero.

The individual entropy cutoff identity requires m(logR+1), NOT m logR. I independently found the missing constant in the initial draft by the scalar A=1,A0=0 test. The author corrected the display and recorded the revision before this PASS. Both +m and m logR cancel with coefficients1+1-2. Changing variables in the reference integral leaves the positive tail3 integral_(R/3)^R logdet(I+K/3), tending m log3 because K(s)=H_infinity/s+O(s^-2). It cancels the explicit source affine term -m log3. Thus the displayed F integral is the actual original homogeneous deficit, not an abstract proxy or a same-main comparison assumption.

## Scalar balancing and deficient Schmidt rank

The exact rational positive decomposition for f_T-k f_P was independently replayed. At fixed spectator k, a pair balance preserves P+kT=e2(K), strictly lowers F unless equal, and decreases trace by (sqrt(k+x)-sqrt(k+y))^2. Repeatedly balancing the extreme pair keeps all eigenvalues between the initial extrema. For rank2, its first balance with the positive middle spectator makes the triple strictly positive. After that it lies in a fixed positive compact interval. Any subsequence with nonvanishing spread has trace drops bounded away from zero, impossible for a decreasing bounded trace. Hence it converges to sqrt(e2/3)I. This proves the pointwise lower comparison, not fixed-trace Schur convexity.

For rank1, F(x,0,0)=4log(1+x/2)-3log(1+x/3)-log(1+x), whose derivative is2x/((x+1)(x+2)(x+3))>0. Independently, the corresponding product difference is x^2/6+7x^3/54+11x^4/432. Rank0 is a reset-only product. No inverse of a singular3x3 clock is needed.

## Global analytic branch

Restrict to the fixed support of A=H_infinity=Psi*Psi, positive definite there. Every spectral effect M_j is PSD and shares the removed kernel. H(z)=sum M_j z/(z+lambda_j) has ImH>=0 in the upper half-plane. If an eigenvector has a real eigenvalue, it kills every positive-lambda effect and H acts there as A; its eigenvalue is positive. Consequently H has no zero or nonpositive-real spectrum, even for nonnormal H, and principal matrix Log H is globally analytic.

For support rank3, Im(H^-1)=-H^{-*}(ImH)H^-1<=0. Unless ImH=0, its trace is strictly negative imaginary; otherwise H=A>0. Thus TrH^-1 never vanishes or meets the logarithmic cut. Its argument lies between the extreme reciprocal eigenarguments because those reciprocals lie in a cone of width<pi. The imaginary part of TrLogH+LogTrH^-1 is between the sums of the two smallest and two largest eigenarguments, inside[0,2pi). The specified exponential half-log therefore gives a Pick g with g^2=e2(H)/3. A scalar principal square root of the determinant expression alone would not justify this branch. For rank2, exp(TrLogH_support/2)/sqrt3 gives the direct support branch and the same Pick property.

## Finite cuts, atoms and total mass

Reflection and the positive values of H on z<-L and z>0 extend the chosen branch outside[-L,0]. At infinity g=c+O(1/z), c=sqrt(e2(A)/3)>0, so h=g/z~c/z. Each finite rational e2 pole has order at most2. A square-root simple-pole singularity is integrable; a double pole becomes an ordinary simple pole. At a simple real pole the Pick sign forces the g residue nonpositive, and division by the negative pole location gives a nonnegative h residue.

At zero, H=M0+zA1+O(z^2). A1 is positive on kerM0 because A=sum M_j is positive on the fixed support. Rank M0>=2 gives a finite positive g0 and a positive h atom. Rank M0=1 gives at worst h=O(z^-1/2), integrable; rank M0=0 gives h bounded. These are all possible zero-endpoint behaviors. The finite algebraic cut contour therefore yields density Im g(-t+i0)/(pi t)>=0, positive atoms, no unreceived singular measure term, support[0,L] and mass c from the coefficient at infinity. L=0 is c delta0. No general operator-mean closure theorem is assumed.

## Actual auxiliary sources and convergence

Finite atomic approximants to this positive compact measure retain EXACT mass c. With atoms(t_j,m_j), use logical vector sqrt(m_j/c), bath diag(t_j), three reference-label copies and actual main sqrt(c) sum_i |i>phys |i>label v. Their compressed clocks are h_n(s)I, and the reset is block-diagonal physical-CQ. Normalizing yields the already independently received pure-success arbitrary-CQ class. Main mass3c need not equal the original m; only homogeneous deficit nonnegativity is used. There is no charged operation mapping the original main into these auxiliaries.

Let M=||A||. Since c<=M, original and auxiliary clocks are bounded by M/s. Direct absolute logarithm counting gives16log(1+3M/s). Exact first-order cancellation and0<=t-log(1+t)<=t^2/2 give the second bound8M^2/s^2, with group constants3,1/2,9/2. Their minimum is integrable, uniformly in auxiliary dimensions and reset traces. Dominated convergence, not dimension-dependent entropy continuity, receives the balanced integral. Combined with the actual source identity and pointwise balancing this proves the entire stated VALUE theorem.

## Executed corroboration and dependencies

Replayed `arbitrary_pure_main_e2_clock_source_check.py` on its five genuinely complex sources, including rank1/2 mains and singular/coherent resets; original entropy deficits and inverse-clock integrals agree. Replayed the exact symbolic pair-score certificate. These fixtures corroborate, not replace, the all-domain arguments above. Dependencies are the exact scalar compensated inequality and the earlier actual physical-CQ VALUE theorem; no circular use of this theorem, clean-kernel extension or aligned-Schur whole theorem is needed. Prior charged-GLS and generic channel-monotonicity failures remain untouched.
