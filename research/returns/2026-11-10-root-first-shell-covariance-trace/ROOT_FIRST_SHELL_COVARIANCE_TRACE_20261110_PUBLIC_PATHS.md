ROOT P2: FIRST-SHELL TRACE FOR EVERY FUNDAMENTAL-SHEAR NOISE COVARIANCE
10 November 2026 Brisbane. Analytical finite-mode identity and its exact scope.
This extends the earlier one-input/equally-weighted calculation, rather than a claim about the full additive-force compiler or the existence condition WE.

1. Spaces and convention.
Work on the unit three-torus with normalized measure; kappa=2*pi. Let E be the real 12-dimensional mean-zero divergence-free fundamental shell, spanned by sqrt(2)*e_a*cos(kappa*x_b) and sqrt(2)*e_a*sin(kappa*x_b), a!=b. Let P be the Leray projection and
 L_F v=P[(F dot grad)v+(v dot grad)F].
Take any real orthogonal Fourier Galerkin projection P_R containing E and every wavevector k+/-e_b with k in {+/-e_1,+/-e_2,+/-e_3}. Including all |k|<=2 suffices. Set A_F=P_R L_F P_R. Everything below is an exact finite-dimensional identity, independent of any higher cutoff. No infinite-dimensional stochastic PDE assertion is needed.

For F in E define the real finite-shell trace
 K(F)=sum_(j=1)^12 [<u_j,A_F^2 u_j>+||A_F u_j||_2^2],
where (u_j) is ANY real L2-orthonormal basis of E.
Then
 K(F)=2*kappa^2*||F||_2^2.                         (1)
This includes arbitrary combinations and phases, not only coordinate shears or equal weights.

2. Literal trace calculation for one basis shear.
Take F=e_a*cos(kappa*x_b), a!=b, and let c be the remaining coordinate.
Complexify E. Its trace is unchanged under the unitary change from the real cosine/sine basis to complex modes k=+/-e_i with two transverse unit polarizations. For input mode k and sign sigma put p=k+sigma*e_b,
 P_k=I-k*k^T/|k|^2, P_0=0,
 T=P_p*(k_a I+sigma*e_a*e_b^T)*P_k,
 R=P_k*(p_a I-sigma*e_a*e_b^T)*P_p.
The first application of A_F has coefficient i*kappa*T/2. The return to k in the second application has coefficient -kappa^2*R*T/4. Therefore the contribution of mode k, summed over its transverse polarizations, is
 (kappa^2/4)*sum_sigma tr(T^*T-R*T).               (2)

For k=e_a this sum is 0. Indeed the e_b input is projected to zero because e_b+sigma*e_a is parallel to p; the e_c input has T e_c=e_c and R*T e_c=e_c, so norm and return-loop cancel.
For k=e_b it is 0: k_a=0 and every transverse input has e_b component zero, hence T=0.
For k=e_c, T=sigma*e_a*e_b^T on the transverse space, tr(T^*T)=1 and R*T=0 for each sign, so the sum is 2.
The negative modes give the identical values by reflection. The total signed-mode sum is 4, giving K(F)=kappa^2. Since ||F||_2^2=1/2, this proves (1) for that shear. Translation gives the same value for sine. The rational Fourier matrix calculation was independently evaluated with exact fractions for all six choices (a,b): the positive-axis sums are always 0 on axes a,b and 2 on the remaining axis. That finite computation confirms the displayed analytic identity, not a field sample or an extrapolation to untested high frequencies.

3. Why every off-diagonal covariance term vanishes.
K is a real quadratic form in the 12 standing-wave coefficients.
For two shears with different frequency axes, the mixed norm/return trace cannot close the wavevector loop to the original k: the two shifts must sum to zero. Their mixed term vanishes. Equivalently, translation invariance separates the frequency characters.
At the same frequency axis b, distinct target components a,c have zero mixed term: reflecting the source and target coordinate a changes the sign of the a-shear alone while preserving the trace.
For the same a,b, a quarter-period translation in coordinate b rotates cosine to minus sine and sine to cosine. Invariance forces equal diagonal coefficients and zero symmetric cross coefficient.
Thus K=kappa^2 times the sum of squares of all unnormalized real standing-wave coefficients, which is exactly (1). The projection P_R commutes with these coordinate reflections/translations on all required intermediate modes; no right-rotation or continuum-isotropy assumption is used.

4. Arbitrary positive noise covariance.
Let F_1,...,F_s be any finite family in E, with independent standard real Brownian coordinates, and consider the FINITE linear Stratonovich SDE
 dV=-sum_alpha A_(F_alpha) V circle dB_alpha.
For an initial u, Ito conversion and the quadratic energy rule give
 D(u):=(d/dt) E||V_t||_2^2 at t=0
      =sum_alpha [<u,A_(F_alpha)^2u>+||A_(F_alpha)u||_2^2].
Summing over the orthonormal fundamental inputs and applying (1),
 sum_j D(u_j)=2*kappa^2*sum_alpha ||F_alpha||_2^2. (3)
Hence any nonzero covariance has some fundamental input with
 D(u_j)>=kappa^2*sum_alpha||F_alpha||_2^2/6>0.
Every positive semidefinite covariance on E admits a finite factorization of this form, so correlated noise, unequal weights, phase changes or arbitrary linear combinations within E do not avoid the positive trace.

If the finite SDE additionally has drift nu*Delta V, the trace is exactly
 sum_j D_nu(u_j)=2*kappa^2*sum_alpha||F_alpha||_2^2
                                      -24*nu*kappa^2.
In particular noise strength sum||F_alpha||^2>12nu forces a positive derivative on some fundamental input even with this fixed viscous drift. This is a mathematical finite-mode statement, not an authorised physical noise implementation.

5. Exact consequence and remaining scope.
No nonzero constant covariance of these physical fundamental generators can be infinitesimally mean-square nonexpansive on EVERY fundamental initial field in the inviscid model. In particular their known derivative coercivity cannot be converted into a dissipative Ito energy argument by merely retuning the noise covariance. The strain/pressure return-loop has to be included.

This does NOT exclude a finite-time random evolution with an initial energy increase, time-dependent preprocessing or switching, another spatial family, a different moment/weighted norm, deterministic zero-return words, compact H1-to-L2 squeezing, or the original all-weak viscous additive-force compiler. The original first shell can leave itself, so the trace is not a spectral-growth theorem for the full evolution. H1 weighting on the input shell is a scalar rescaling; it does not turn this infinitesimal statement into a full WE obstruction. Do not charge another all-family negative result or claim that random strategies have been ruled out.

Source bindings: current P2_FULL_BODY_FORCE_AFTER_E155_XI_20261110.txt, 15495ASCII, SHA256 bcd4c7af33ab007e13cf071ba67c0a1c6e7b01bc622e7d212a753696e70087a5; completed whole available P2_XI_E155_RECOVERED_RETURN.md41838UTF8/SHA7fdbfe01a28749a0ce6727e684f07b949a853378aedd2a70b0803a47554e6a17; prior ROOT_PHYSICAL_EULER_COERCIVITY_AND_NOISE_ENERGY_20261110.txt3114ASCII/SHA7058d35068efcec21ac11ace2ad35e0a510b9601f9cf24bf3d10d39dc41a8d6b. The general covariance trace is ROOT's new deduction here; the underlying physical definition and earlier single-input Ito rule are inherited. No outside literature theorem, held source, extra worker/model/resource or physical experiment is needed or claimed. No historical priority, model comparison or impact assessment is attached.
