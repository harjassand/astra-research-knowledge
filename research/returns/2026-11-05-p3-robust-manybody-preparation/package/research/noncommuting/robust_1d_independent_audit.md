# Independent audit and finite-precision closure for the robust 1D block mixture

## Result

The proposed modification in `comparators/robust_1d_block_opening.md` is algebraically valid. It establishes a stronger statement than the pure-block decomposition in Pilatowsky-Cameo, Styliaris, Bakshi and Malz, arXiv:2609.35973v1: at every fixed finite inverse temperature and interaction range, every one-dimensional Gibbs state is a convex mixture of bounded contiguous **uniformly full-rank** block states. The positive floor and block-size bound depend on temperature and range but not total system size or requested accuracy. The source's classical sampler can be adapted constructively; no new global rejection step is needed.

This note independently checked the actual primary full texts, rather than inferring the operation from abstract separability:

- https://arxiv.org/pdf/2609.35973, Appendix A Lemma A1, Theorem A1, Corollary A1, equations A6--A10; Appendix B equations B1--B7; Appendix C Lemmas C1--C2 and proof of Lemma A1.
- https://arxiv.org/pdf/2602.13386, version 2 dated 2 November 2026, Lemma 8.4 and its proof. In particular, the dressing operator is an invertible product of finite-volume Gibbs exponentials; both its norm and inverse norm are bounded independently of chain size.

## Exact algebra

Let a=e^(-7m)/2, F=G'/2, and Delta=G-F. The source's G'<=G<=e^(7m)G' implies

    aG <= F <= G/2,
    G/2 <= Delta <= (1-a)G.

Thus A=G^(-1/2)Delta G^(-1/2) has spectrum in [1/2,1-a]. Given any rank-one orthogonal spectral resolution A=sum_t lambda_t P_t, put s=a/2 and

    Q_t=(1-s)P_t+sI/d,
    b_t=(lambda_t-s tr(A)/d)/(1-s).

Then sum_t Q_t=I and sum_t b_t Q_t=A exactly. Moreover b_t>=0 and b_t<=(1-a)/(1-a/2)<=1-a/2. With E_t=G^(1/2)Q_tG^(1/2), all E_t are strictly positive, sum_t E_t=G, sum_t b_t E_t=Delta, and E_t >= (s/d)G. A degeneracy in A causes no mathematical difficulty: any orthonormal basis in a degenerate eigenspace works.

The first-cut telescoping expansion is exact when products j<b include j=0:

    tensor_j G_j
      = sum_(b=1)^(L-1) (tensor_(j<b) Delta_j) tensor F_b tensor (tensor_(j>b) G_j)
        + F_0 tensor (tensor_(j>0)G_j) + tensor_j Delta_j.

The last two terms become a positive sum of

    F_0^(1/2) (I+K_t) F_0^(1/2) tensor_(j>0) E_(j,t_j),
    K_t=(product_(j>0)b_(j,t_j)) F_0^(-1/2)Delta_0F_0^(-1/2).

Therefore ||K_t|| <= a^(-1)(1-a/2)^(L-1). The proposed L makes this at most (1/2)8^(-m).

For a Hermitian K on k<=m qubits, write K=sum_P alpha_P P, c=1+alpha_I, u=1/2, and w_P=|alpha_P|u^(-wt(P)) for P!=I. Since sum_P u^(-wt(P))=7^k<=8^m, sum_(P!=I)w_P<=1/2 while c>=1-||K||>1/2. Hence

    I+K=(c-sum w_P)I + sum_(P!=I) w_P[I+sgn(alpha_P)u^wt(P)P]

has nonnegative weights. Each bracket has the elementary parity-mixture decomposition into tensor products of radius-1/2 Pauli states. Those local states have eigenvalues 1/4 and 3/4. Consequently every leaf factor remains strictly positive. Congruence by F_0^(1/2), which factors across the chosen midpoint cut, preserves that cut and strict positivity.

## Source geometry and constants

The source permits arbitrary anchor positions k_j before selecting equally spaced positions for convenience. Choosing successive anchor gaps in [m0,2m0] is therefore compatible. Choose the cut between sites floor((k_(j-1)+k_j)/2) and its successor. No dressing operator crosses that cut. The cut need not be at a site outside every dressing support: for equal odd gaps, dressing supports can tile the sites. The opening's phrase "a midpoint cut remains outside every dressing support" should be understood and preferably rewritten as "no dressing operator crosses the midpoint cut."

Using m=2m0 in all conservative inequalities preserves the QPI floor and G/G' sandwich. The final incomplete superblock can contain up to 2L elementary blocks, so B=4mL safely bounds the distance between selected cuts. If the whole chain is shorter than B, treat it as one block directly.

The proposed condition-number bound is conservative and valid. In detail:

    kappa(G)<=64^m exp(2 beta m)=kappa_g,
    kappa(Delta)<=2 kappa_g,
    kappa(E_t)<=2^m kappa_g/s,
    kappa(F^(1/2) P_mix F^(1/2))<=exp(2 beta m)3^m,

where P_mix denotes one normalized product of radius-1/2 Pauli states. The chosen K0=2^(m+1)kappa_g/s bounds all four. Splitting a product at its cut cannot increase the condition number of either positive tensor factor beyond the product condition number. A congruence by a dressing M multiplies a condition-number bound by at most ||M||^2||M^-1||^2<=Lambda^4. Thus eta=(K0 Lambda^4)^(-B) gives tau_A>=eta I_A/2^|A| after normalization. Include exp(-2 beta B) for chains handled directly.

For an explicit safe Lambda without optimizing updated-source constants, use the finite-volume product defining M after folding. Its normalized local Hamiltonians have at most m0 bounded terms, with absorbed inverse temperature at most r max(1,beta). The crude choice

    Lambda=exp(2 r max(1,beta) m0)

bounds both exponential products and their inverses. This is intentionally vastly larger than needed. No numerical utility follows from these constants.

## Finite-precision sampler: a constructive closure

The exact first-stage law pi_nu in source equation B2 remains unchanged: for every nu, the modified superblock decomposition sums to exactly the same tensor product of G_j. For a fixed nu, let T_s=tensor_(j in S_s)G_j and let its constructed positive decomposition be T_s=sum_a V_(s,a), where every nonzero V_(s,a)=L_(s,a) tensor R_(s,a) has a chosen cut. The label alphabet, local matrix dimensions, number of spectral operations, and all condition numbers are constants at fixed beta and r.

The source's equation B5 remains exact for these new positive factors. The trace weight of the total label is a nearest-neighbor product, so a finite-state forward-backward sampler still applies. One stops before the source's last refinement to pure states, keeping the normalized full-rank factors.

Numerical eigenvectors need not depend continuously on the input. Compute any approximate unitary diagonalization with a certified operator residual, clip eigenvalues into the allowed compact interval, and form Q_t explicitly as a convex mixture of its rank-one projector and I/d. This preserves positive definiteness. The sum reconstructs an approximation A_tilde to A with a certified operator error. Matrix square roots, exponentials, inverses and Pauli coefficients are computable to arbitrary precision in these fixed dimensions. Their derivatives are bounded on the uniform positive spectral ranges. Construct the central positive mixture with slightly stronger slack, e.g. increase L enough to enforce ||K||<=(1/4)8^(-m), so approximation does not approach the nonnegative-weight boundary. Zero coefficients can be omitted; approximate small weights by nonnegative dyadic weights rather than require relative accuracy near zero.

Here is the error accounting that makes this constructive without a global condition-number loss. Fix zeta>0. Compute each positive superblock decomposition so its sum T_tilde_s obeys

    (1-zeta)T_s <= T_tilde_s <= (1+zeta)T_s.

This needs only absolute operator accuracy O(zeta lambda_min(T_s)) on a constant-dimensional matrix. Its required bit precision is O(log(1/zeta)) plus a beta,r-dependent constant. Positivity and the cut factorization are preserved by using the positive formulas above. Tensoring over q superblocks yields multiplicative factors (1+-zeta)^q. Congruence by the possibly ill-conditioned *global* dressing M preserves this Loewner sandwich exactly. Upon trace normalization, the trace-distance error is O(q zeta), uniformly in nu. Choose zeta=O(epsilon/N). Thus global inversion or global condition numbers never enter the numerical precision requirement.

Approximate sampling of the resulting finite-state chain adds its own total-variation error. Positive scalar coefficient weights can be handled separately; all normalized positive edge factors have a uniform spectral floor. Compute edge factors to relative accuracy O(epsilon/N), use positive rescaling or log-domain transfer arithmetic, and use O(log(N/epsilon)) precision plus constants depending on beta,r. If a scalar coefficient is smaller than the chosen additive threshold, discard it inside the already budgeted local operator error. This gives a polynomial algorithm. Add the source's first-stage sampling error and final block-state synthesis error by convexity and product telescoping.

No claim is made that the original source had already proved this robust-floor corollary or its noisy physical realization. The new proof ingredients are precisely the halved cut operator, softened spectral resolution, and mixed-product central decomposition. No general sampling hardness or broad hardware advantage is implied.

## Broad mathematical deduction: a uniform local-noise radius at every finite temperature

This deduction does not require Pauli, unital, or spatially homogeneous noise. Let Lambda_i be arbitrary single-site CPTP maps satisfying

    ||Lambda_i-id||_diamond <= delta < 1.

Their linear inverses exist by the Neumann series, are trace and Hermiticity preserving, and satisfy

    ||Lambda_i^(-1)||_diamond <= 1/(1-delta),
    ||Lambda_i^(-1)-id||_diamond <= delta/(1-delta).

For a block A of at most B sites, telescoping products gives

    ||Lambda_A^(-1)-id||_diamond <= (1-delta)^(-B)-1,
    Lambda_A=tensor_(i in A)Lambda_i.

If

    (1-delta)^(-B)-1 <= eta/2^(B+1),

then every block preimage sigma_A=Lambda_A^(-1)(tau_A) has unit trace and obeys

    sigma_A >= (eta/2) I_A/2^|A|.

Indeed, the inverse correction has operator norm at most its trace norm, at most eta/2^(B+1), whereas tau_A has minimum eigenvalue eta/2^|A|. Because |A|<=B, this is at most half the available floor. The same mixture labels and probabilities therefore give a positive exact preimage

    sigma_beta=E_mu[tensor_A sigma_(mu,A)],
    (tensor_i Lambda_i)(sigma_beta)=rho_beta.

No global inverse-norm bound is used. The source's polynomial classical label sampler remains valid, and every inverse calculation is on at most B qubits, a constant at fixed temperature and range. Use a slightly smaller delta and the conservative finite-precision spectral floor for an approximate implementation.

For the finite-accuracy leaf mixture, invert each actual sampled full-rank block. Applying the physical forward channels then returns that original approximate leaf exactly. Thus delivered trace error is inherited from the sampler; one must not instead bound error by applying the global inverse to an approximate Gibbs matrix. This is the same crucial positive-ensemble shortcut as in the high-temperature result.

This theorem establishes a size-independent local-noise interior of the set of thermal states in one dimension at every fixed positive temperature. The permitted delta depends on beta and range and can be catastrophically small. A size-independent threshold need not be temperature independent: even a single spin with H=-Z requires a depolarizing contraction at least tanh(beta) to reach its Gibbs state, so noise of order larger than exp(-2 beta) is impossible as beta grows. This necessary one-spin obstruction is separate from the much smaller sufficient constants supplied by the present proof.

The mathematical deduction does not on its own implement arbitrary Lambda_i in an apparatus. The already accepted history-erasing Bell/tree interface with an independent product Pauli endpoint channel supplies one completed compatible physical route. General calibrated single-site channels require their own implemented interface. Unknown-input quantum communication and indefinitely long storage are separate tasks.
