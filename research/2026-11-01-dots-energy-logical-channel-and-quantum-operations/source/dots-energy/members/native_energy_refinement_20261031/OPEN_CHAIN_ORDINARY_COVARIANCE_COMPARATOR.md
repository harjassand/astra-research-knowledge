# Ordinary covariance acquisition remains a strong comparator

31 October2026. This note prevents a false interpretation of the coherent port as uniquely acquiring the chain's variance or effective white-noise coefficients. It is separate from the finite-rate retained-channel theorem.

The one-dimensional Glauber chain is a long-established exactly solvable model. The independently accessible primary abstract of Mayer–Sollich, *General Solutions for Multispin Two-Time Correlation and Response Functions in the Glauber–Ising Chain* (2003), explicitly treats the full correlation/response hierarchy and multispin two-time observables. This is substantial ordinary machinery, not a missing-classical-computation straw comparator. [Primary record](https://arxiv.org/abs/cond-mat/0307214)

A fetch of Glauber's1963 DOI10.1063/1.1703954 redirected to an AIP page inaccessible to the tool (non-retryable500). No retry or alternate copy was requested. The formulas below are directly derived for the supplied finite inhomogeneous chain; they are not attributed to uninspected equations of that paper. All earlier denied-source restrictions remain unchanged.

## Exact n-dimensional observable closure

Let M denote the matrix acting on the vector of spin observables. Heat-bath flipping gives

    Q_classical† s_i=-s_i+tanh(J_L s_(i-1)+J_R s_(i+1)).

Since the hyperbolic tangent is odd under flipping both neighbor signs, its two-bit Boolean expansion is exactly

    tanh(J_L s_L+J_R s_R)=a_i s_L+b_i s_R,
    a_i=[tanh(J_L+J_R)+tanh(J_L-J_R)]/2,
    b_i=[tanh(J_L+J_R)-tanh(J_L-J_R)]/2.

Therefore M_ii=-1, M_i,i-1=a_i, M_i,i+1=b_i. At the two ends the single-neighbor coefficient is tanh J; for n1 the matrix is simply[-1]. Thus, for every classical initial configuration, conditional mean spins evolve by exp(Mt), exactly, without a2^n state table.

The stationary covariance is C_ij=product of tanh J along the unique path. Consequently

    E_pi[s(t)s(0)^T]=exp(Mt) C,
    D_int=integral_0^infinity exp(Mt)C dt=-M^(-1)C.

Weak coupling ensures stability. For example |J|<=1/40 gives strict diagonal dominance and the earlier gap lower bound. Reversibility gives MC=CM^T, so D_int is symmetric positive semidefinite. These are exact finite-dimensional identities, not a fitted correlation model.

For rational q_i=exp(2J_i), all coefficients are rational: tanh(J_L+J_R)=(q_L q_R-1)/(q_L q_R+1), with the analogous quotient for J_L-J_R. C is a product of rational t_i=(q_i-1)/(q_i+1). Gaussian elimination therefore acquires D_int with polynomial n and coefficient-bit arithmetic. No coherent source, inverse-fibre operation, partition-function approximation or unknown statistical parameter is needed. The ordinary Markov/innovations covariance factorization underlying the new frame is also not new probability theory.

## Effective-system access and the remaining distinction

For K=sum_i A_i tensor Z_i and a stationary reversible source, the usual leading fast-noise effective generator is

    L_eff(rho)=-i[H0,rho]-sum_(i,j) (D_int)_ij [A_i,[A_j,rho]].

Its coefficient matrix is already available from the n-dimensional solve. With supplied individual A_i encodings, prepare their rectangular stack and apply an acquired finite matrix square root of2D_int to its index. This constructs the ordinary effective Lindblad stack with variance-type normalization, with all n-dimensional matrix arithmetic, operator selection and synthesis paid. Thus a variance rather than sum-of-norms normalization is not an exclusive advantage of the new retained-source port.

What is NOT obtained merely from these identities is a finite-lambda, high-precision FULL retained source/system channel with arbitrary initial joint states and prescribed source controls. Boundary layers, initial correlations, memory and source reconstruction require their own bounds. The effective generator is not silently substituted into that stronger task. Conversely, a user requesting only a system observable at fixed tolerance should be offered this ordinary reduced calculation first when its actual finite-rate error can be certified.

The frozen small n4 dense diagnostic already demonstrates the distinction: system-marginal white-noise error is about1.67e-6 at the high threshold, while retained-CQ error is about9.79e-4 for the displayed one-input test. Neither number is a uniform channel certificate. The coherent frame's useful acquired operation is the actual source-output block QKP, including reversible index erasure and noncommuting system operators—not a new way to compute static or integrated classical covariance.
