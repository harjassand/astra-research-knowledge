# Positive canonical ensembles for conjugate boson histories

## 1. Task and established operations

The target is a native fixed-particle-number prediction for frustrated bosonic matter, rather than positivity of a formally continued grand trace. The many-body Hilbert space should not be stored, but its physical particle counts and interactions must remain unchanged.

The ordinary ingredients are Hubbard–Stratonovich (HS) decoupling, symmetric-power characters, canonical recurrences (Shen et al., arXiv:2010.09813, section II C), antiunitary/conjugate-field positivity (Yu–Wei–Li, arXiv:2610.31541v1), Schatten Holder, and positive trigonometric quadrature. None is claimed new here. The construction below identifies the exact compatible ensemble cone, provides a finite-number/stability repair of a concrete native model, and compiles its actual canonical calculation. It does not establish generic tractability or historical priority.

Use M spatial modes and two flavors b,c. On each flavor's K-particle sector, let Gamma_K(B) be the symmetric tensor power of the one-particle matrix B. Then

`h_K(B) := Tr Gamma_K(B) = [z^K] det(I-zB)^(-1)`.

This is a polynomial, finite even if the grand trace diverges. It obeys h_0=1 and the ordinary canonical recurrence

`h_k(B) = (1/k) sum_{j=1}^k Tr(B^j) h_{k-j}(B)`.

For a conjugate history U(B) tensor U(conjugate B), projection onto separately fixed counts K,K gives the weight

`W_K(B)=|h_K(B)|^2 >= 0`.

This equality holds configuration by configuration. It does not require a positive one-particle matrix, unfrustrated hopping, a diagonalizable B, or convergence of an infinite occupation sum.

## 2. The native nontrivial stable class

The concrete lattice class used in the consumer is

`H = b^dagger T b + c^dagger conjugate(T) c + sum_i U_i (n_bi-n_ci)^2`,

where T is Hermitian, possibly frustrated or complex, and U_i>=0. Nb and Nc are separately conserved. Each onsite interaction admits the exact imaginary HS phase

`exp[-a (n_bi-n_ci)^2] = E_phi exp[i sqrt(2a) phi (n_bi-n_ci)]`.

The two flavors therefore see conjugate potentials, and their complete hopping-plus-field histories remain conjugate. Symmetric Trotter splitting preserves this property at every finite slice count. Section 1 makes the K,K trace nonnegative for every field, with no local occupation cutoff. The finite canonical sector is the requested physical ensemble, not a regularization of another model.

For bounded-degree hopping with ||T||<=t_*, the exact Hamiltonian satisfies

`H >= -t_* (Nb+Nc)`.

At K proportional to M this is an extensive lower bound. The interaction remains genuine and noncommuting with hopping. It locks relative densities and includes interflavor attraction together with same-flavor repulsion; it is not an independent-particle model. This lower bound is stability of matter, not a proof of a phase diagram, a gap, uniqueness, finite compressibility, or rapid mixing. The model lies on a marginal total-density direction and must not be called superstable.

By contrast, adding a fixed onsite term U2(n_bi+n_ci)^2 with U2<0 destroys the grand-canonical trace. Put n particles of each flavor at one site. Its energy expectation is 4U2 n^2 plus a linear one-body/chemical-potential contribution. The diagonal Boltzmann element is at least the exponential of minus that expectation, so even this subsequence makes Tr exp[-beta(H-mu N)] infinite. At fixed K,K it is finite, but at K proportional to volume it has an O(-K^2) collapsed trial state. A negative chemical potential cannot repair the quadratic collapse. An added occupation cap, repulsion, altered ensemble, or Kac scaling changes the model and must be charged explicitly. We therefore keep U2=0 in the extensive consumer.

## 3. Exactly which finite number filters preserve this positivity universally?

Consider a PHYSICAL diagonal number filter

`F_number = sum_{k,l=0}^J f_kl Pi_k^b tensor Pi_l^c`,

where all f_kl are real and nonnegative (rescale by their maximum if a measurement effect is desired). Treat f=(f_kl) as a separate matrix on the charge labels. The filtered field weight is

`W_f(B) = sum_kl f_kl h_k(B) conjugate(h_l(B))`.

**Theorem.** This is real and nonnegative for every finite complex B, with spatial dimension allowed to be at least J, if and only if the charge-label matrix f is positive semidefinite. The physical compatible cone is therefore entrywise-nonnegative real matrices intersected with the PSD cone. PSD alone would allow signed or complex weights and would not define the stated physical filter.

Sufficiency is the finite Gram identity: factor f=R R^dagger and obtain a sum of squared moduli of linear combinations of the h_k. For necessity, the vector (h_0,...,h_J) can realize any complex vector (1,a_1,...,a_J). Indeed choose d_0=1 and

`d_j = -sum_{i=1}^j a_i d_{j-i}`.

Take the companion matrix whose characteristic coefficients are d_j. Then det(I-zB)=sum_{j=0}^J d_j z^j, whose reciprocal has the specified first J coefficients. Nonnegativity on every vector with first entry one, by homogeneity and continuity, implies nonnegativity on every vector and hence f>=0. Reality first forces f to be Hermitian. If desired restrict to invertible B: singular matrices are limits, and a strict negative value persists under an invertible perturbation, which also admits a complex matrix logarithm. This necessity concerns unrestricted conjugate Gaussian histories. It is NOT a reachability theorem for one prescribed HS model. Native failures require their own native-history control.

Consequences:

* Any nonnegative mixture of separately balanced sectors is admitted.
* For an exactly fixed TOTAL count 2K, the only universally admitted nonzero finite filter has its support at (K,K). A PSD matrix with a zero diagonal entry has its whole corresponding row/column zero; all other points on the antidiagonal have zero diagonal support.
* Accepting a pair (K-r,K+r) with nonzero f forces leakage to the balanced sectors with totals 2K-2r and 2K+2r: `f_(K-r,K+r)^2 <= f_(K-r,K-r) f_(K+r,K+r)`. This is a quantified ensemble cost, not a new no-go for all canonical Monte Carlo representations.

Root independently supplied an exact native total-number counterexample in `../../root_boson_ensemble/COUNTEREXAMPLE.md`: stable zero-hopping density-difference interactions produce an open positive-measure set of HS fields with negative fixed-total-N2 weight, while their grand weights are positive. The generic PSD necessity is thus not being passed off as native reachability. That diagonal Hamiltonian has ordinary positive occupation sampling; no global hardness follows.

## 4. A finite positive auxiliary alphabet, rather than a Gaussian-tail oracle

In the K,K sector each onsite density difference has integer eigenvalues between -K and K. Only the first K Fourier moments of its phase law matter. Let mu_m=exp(-a m^2). The (K+1)-dimensional Toeplitz matrix G_ij=mu_(i-j) is strictly positive for a>0, since it is the moment matrix of a wrapped Gaussian with positive density on the circle.

Choose vectors v_0,...,v_K with Gram G. The shift v_j -> v_(j+1), j<K, is an isometry between two K-dimensional subspaces because G is Toeplitz. Extend it by a unitary map of their one-dimensional orthogonal complements. Its spectral measure in v_0 is a positive quadrature with at most K+1 phase atoms, whose moments through degree K agree EXACTLY with mu_m. A real orthogonal extension yields conjugate phase pairs and equal paired weights. This is ordinary Szego/finite trigonometric quadrature, used here as an HS compiler on the actual finite-number sector.

For K=2 a closed expression is available. Set c=exp(-a), x=(1+c+c^2+c^3)/2-1. Put atoms at 1 and exp(+-i arccos x), with each nontrivial atom having probability

`p=(1-c)/(2(1-x))`, and `p0=1-2p`.

Here -1/2<x<1 and x<=c, so all probabilities are positive. Their first moment is c and second moment c^4; the construction is exact for every a>0, not just a small-step expansion.

The all-K mathematical construction is distinct from the executed compiler, which is explicitly restricted to EVEN K>=2. It uses a determinant-positive real orthogonal extension in odd dimension, its +1 atom, and conjugate atom pairs; the odd-K normalization cases have not been implemented. The consumer records a finite dyadic probability table and rational unit-circle phases. Exact moment residuals of the rational table can be evaluated by Fraction arithmetic. The exact compiled table defines a nearby finite HS operator; its difference from the intended heat-kernel moments is reported, rather than called exact. Fixed-number finiteness does not remove moment-matrix conditioning: small a and large K may require high arithmetic precision, paid by the compiler. No fixed precision suffices uniformly without such a condition/budget.

## 5. An explicit independent rejection law and its real cost

For U_i>=0 all HS factors are unitary. Let beta=L delta and E=exp(-delta T). Cyclically collecting the two half hopping steps makes the one-flavor canonical trace a product of L factors Gamma_K(E)Gamma_K(U_l). Schatten Holder with exponent L yields

`|h_K(B)| <= Tr_K exp(-beta T_K) =: Z0_K`.

Thus the exact auxiliary-field law can be sampled independently: propose all its native finite phase labels from their positive base probabilities, compute f=|h_K(B)/Z0_K|^2<=1, and accept with probability f. The mean acceptance is exactly Z_L/(Z0_K)^2, with Z_L the finite-slice canonical partition function. Accepted records are iid under ideal independent random bits; no metastable-mixing promise is used.

This does not provide uniform efficiency. A computable conservative lower bound is obtained without another sampler. On the K,K Hilbert space of dimension d_K^2, with d_K=binom(M+K-1,K), define the positive symmetric one-slice transfer A. AM-GM on its eigenvalues gives

`Z_L=Tr A^L >= d_K^2 exp[-beta Tr(H)/(d_K^2)]`.

The determinant identity behind it is log det A=-delta Tr H, independent of commutators. In a uniform composition trace,

`Tr H /d_K^2 = 2K Tr T/M + (sum_i U_i)/M * [2K+4K(K-1)/(M+1)-2K^2/M]`.

Dividing the lower bound by Z0_K^2 gives a completely acquired (often exponentially poor) proposal bound. Coefficient evaluation is polynomial in M,K,L, but its statistical work need not be. Root's separate `DIRECT_VARIANCE.md` proves an exponential relative-variance lower bound for this iid Gaussian strategy at fixed density even in a stable diagonal case. That result rejects a generic polynomial sampling claim; it does not reject importance sampling, field MCMC, cluster updates, or this finite phase quadrature.

The strongest equal-input incumbent is canonical AFQMC itself. It may use field updates/importance sampling instead of this deliberately transparent iid receiver. Our independent law is a source/cost-complete execution, not evidence of speed advantage over that incumbent. Exact diagonalization is the finite small-system control, not the only ordinary comparator.

## 6. Prediction and precision boundary

The governing consumer is to use a real frustrated triangular hopping graph, U1>0, U2=0, separately fixed K,K, finite HS labels and the above free canonical envelope. It stores M by M propagators, not the d_K^2-dimensional many-body state. Direct many-body diagonalization is used only for a small input where its cost is explicitly reported.

Finite slice count means the target is Z_L. Its difference from the continuous Gibbs trace is a separate noncommuting product-formula cost; numerical convergence alone is not an all-model error theorem. The bounded canonical sector gives finite norms ||T_many||<=2K||T|| and ||V||<=2K^2 max_i U_i, so standard norm-controlled product formulas can be paid with finite, polynomially specified resources. Numerical consumers must keep their actual L and reference/convergence differences visible.

Likewise positive weights do not turn binary64 into exact arithmetic. Finite probability tables, phases, moment residuals, coefficient arithmetic, PRNG realization, and normalized statistical error must be stated separately. No hardware, material phase, practical many-body advantage or rapid Markov-chain mixing follows from a passing finite record.

For the compiled beta=log2,U1=1/2 inputs, let r0=2^(1/(2L)), let r be its rational midpoint with bracketing width w and lower endpoint rlo, let Delta be the one-particle spectral width, and let e be the maximum exact rational moment error against r^(-m^2). Put cmin=min r^(-m^2). A conservative log error for the normalized finite-slice partition function is

`L M e/(cmin-e) + L (4K Delta + M K^2) w/rlo`.

The first term compares the positive diagonal compiled HS operator with its rational-root heat kernel. The second includes BOTH hopping/free normalization and interaction-root errors; the initial receipt omitted the latter contribution and is retained separately. To justify the partition comparison without assuming products preserve Loewner order, compare the symmetric one-step positive transfers. A diagonal interaction log error gives a multiplicative Loewner bound. Changing the commuting hopping factor acts by congruence R A R with all singular values of R bounded between the corresponding exponential factors. Min-max then bounds every transfer eigenvalue by those same multiplicative factors. Raising to L and tracing proves the displayed bound. Binary64 hot-loop roundoff is not covered by this rational-input comparison.
