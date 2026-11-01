# Independent theorem audit: acquired radial-envelope conductance

## Verdict and exact boundary

**PASS, theorem-only**, for the frozen radial-envelope sandwich, its acquired global rational-potential premises, the two sensitivity conclusions, and the deterministic/pathwise finite-probe obstruction. No candidate consumer was imported, run, or accepted by this audit. The full executable receiving conjunction remains a separate review.

The three theorem sources are bound by `THEOREM_FROZEN_SHA256.json` SHA-256 `626fce69b92c5549a173564a01de44c56a6b7994c9f84c701ee2db4972543250`:

- `PROOF_CANDIDATE.md`: `a1b8176f77befb08ea1c842c9c26775ede41ad166d517e409dd099d9b7b944ea`.
- `SENSITIVITY_CANDIDATE.md`: `514964f4667dd9a2d73d5c785d4944565d69576a5ebde017612940a2b5a169e6`.
- `QUERY_ACCESS_OBSTRUCTION.md`: `1583a3f3e449e7d22a1c3a3ade3db2462bf9b73d6a35bbbc59ed1ea26e262e86`.

I independently read the entire three-source conjunction and the prior mixed-degree proof and review. The prior result was not treated as permission to skip the new envelope, positivity, global-process, or obstruction joins. The source hashes were checked again by the independent test script. All originals and earlier artifacts remain unchanged. A separately constructed randomized addendum is reviewed, if completed, in a separate receipt; it is not silently folded into this three-file freeze.

Throughout, the inherited physical interface is m>=1, beta>0, longitudinal mobility 1, a fixed finite constant transverse SPD matrix M, zero cross mobility, and matched noise/drift. Statements quantify over this mathematical family; potential input alone does not authenticate a physical kinetic interface.

## 1. Unnormalized ordering, basin versus slab, and cancellation

Let C_F be the unnormalized Dirichlet infimum and M_F the unnormalized left-basin mass. Then cap_mu(A,B)=C_F/Z_F and mu(A)=M_F/Z_F, so k_F=C_F/M_F exactly. One must not compare normalized capacities while dropping their different normalizers.

Because U(lz)<=F<=U(uz), the densities are ordered in the reverse direction. This gives

    C_U(u) <= C_F <= C_U(l),
    Z_U MA(u) <= M_F <= Z_U MA(l).

The first line depends only on the slab, while the second requires the whole left tail. The variational ordering is legitimate even when the weighted finite-energy spaces differ: use the common local H1 class with fixed traces and allow infinite energy, or use the inclusions of the finite-energy classes. Truncating h to [0,1] preserves boundary values and decreases energy; finite Gibbs mass supplies weighted L2 integrability. Every admitted smooth rational potential has the local regularity required for slicing.

A scalar trial for U(lz) gives C_U(l)<=Z_U/(beta R0(l)), because its longitudinal weight is exactly Z_U l^-m. The lower comparison is with U(uz), not U(lz). Combining it with the upper basin mass gives

    1/[beta MA(l) Rplus(u)] <= k_F
        <= 1/[beta MA(u) R0(l)].

The unknown partition in all four expressions is the SAME Z_U. Its cancellation therefore remains valid even though the actual F has no exact geometric factorization and no known conditional partition. Four separate scalar integrals, and the final total width, really must be received. The interval is an outer enclosure, not an exact rate or an exact mobility-range statement.

## 2. Jensen lower bound with a possibly unattained reference

For any finite u0>=max_slab u, put G(z)=U(u0 z), Z0=u0^-m Z_U, and r(y)=u(y)/u0. For each fixed z the longitudinal Cauchy inequality gives the reciprocal resistance

    [integral_slab exp(beta U(u(y)z)) dy]^-1.

Writing S(z)=integral_slab exp(beta[U(u(y)z)-G(z)])dy, its integral over z is Z0 E_rho0[1/S], with rho0=exp(-beta G)/Z0. Jensen gives E[1/S]>=1/E[S]. The sign, beta factor and reference normalizer are essential and are correct.

For each nonnegative homogeneous component of degree d<=p, concavity of t^(d/p) implies

    2-r^d >= (2-r^p)^(d/p).

Thus 2U(u0z)-U(u(y)z)>=U(u0(2-r^p)^(1/p)z). A spatial change of variables yields

    E_rho0 exp(beta[U(u(y)z)-G(z)])
       <= (2-r(y)^p)^(-m/p).

All integrands are positive; Tonelli applies, and the displayed compact-slab bound makes E[S] finite. Coercivity and radial monotonicity also bound the reciprocal-resistance integral by an integrable fiber density. Multiplying by u0^m produces precisely

    Rplus(u)=integral_slab [u0^(2p)/(2u0^p-u(y)^p)]^(m/p)dy.

No maximum needs to be attained at u0. No transverse mixing estimate, actual inverse M, energy Gamma identity, or homogeneous-energy approximation enters. Dropping nonnegative transverse energy and using a transverse-constant upper trial make the result uniform over all declared fixed finite M.

## 3. Strong ordinary comparisons and limits of the defect language

The additive density-ratio comparison has the correct factor exp(plus/minus(b-a)); a constant offset cancels. For positive mixed-degree U, c>=1 gives

    c^(-m/d_min) Z_U(beta) <= Z_U(beta c)
                            <= c^(-m/p) Z_U(beta).

This follows by comparing cU(z) with U(c^(1/d_min)z) and U(c^(1/p)z), component by component. Comparing two positive energy multipliers gives the ratio penalty with the same coarser exponent. The homogeneous p case has exponent m/p.

Crucially, the frozen proof now says these penalties multiply nominal structural family outer endpoints. They do not identify the actual fixed-M rate under a uniform energy rescaling: changing transverse spatial scale also changes the effective transverse mobility. Likewise a global radial envelope l=a s, u=b s gives factors (a/b)^m and (b/a)^m on the nominal outer endpoints, not an assertion of rate equality for every admissible angular energy.

The dilation-defect chain rule is correct. Gronwall requires a globally valid |R|<=eta F and integrable eta along the relevant transformed ray; it is not obtained from finite defect samples. At zero-energy points the linear differential inequalities propagate zero. The unsigned defect budget loses cancellation. A small coordinate rotation without conditioning control can have a large relative energy effect; the stated anisotropic quadratic example verifies that distinction.

## 4. Global shape, profile certificates, and what is actually acquired

Both e profiles and their suprema are correct. With v=t/(1+t)^2 in [0,1/4], e_flat=v(1-4v), whose maximum is 1/16. The displayed derivative factorizations are exact. Under 0<=delta<=kappa/[2(1+kappa)] the positive bracket bounds prove that l and u decrease for 0<=y<=1 and increase for y>=1. Their positive minimum and their common slab maximum at y=0 are therefore earned, not inferred from a sampled grid. In particular u0=s(0) is valid.

For the declared raw grammar, every transverse atom is nonnegative and homogeneous of degree 2 or 4. Positive coefficients c_j=N_j(0)/s0^d define one anchor U; the positive quadratic axes supply U>=q_min||z||^2. The denominator (1+y^2)^16 is strictly positive on all physical space. Every atom inequality (V), multiplied by its nonnegative transverse atom and summed, gives the global envelope (E).

The denominator-clearing formula is exact for both e shapes. Its degree is 16+2d in t, giving total physical degree at most 52. The constant coefficient is s0^d and leading coefficient kappa^d; for a quadratic profile the required leading/base ratio is (kappa/s0)^2. The exact rational square-root proposal is only a sufficient finder. Checking the ENTIRE profile inequalities remains necessary; a matching ratio alone is not admission.

For P(t)=sum a_k t^k of degree D,

    (1-x)^D P(x/(1-x))
       = sum [a_k/binom(D,k)] B_(k,D)(x).

Thus nonnegative Bernstein coefficients on a finite exact covering subdivision of [0,1] suffice for P>=0 on every finite t>=0. The projective endpoint includes infinity only as a compactification; no finite cutoff replaces the global inequality. Exact de Casteljau subdivision is sound. A true nonnegative polynomial can fail this sufficient finite certificate (for example because of interior zeros or budgets); UNKNOWN is the appropriate outcome. Zero polynomials are a harmless separate case. Identical normalized profiles may share a mathematical proof, but that does not waive reading/binding each raw coefficient.

This theorem audit checks the mathematical certificate interface, not whether the candidate parser and implementation enforce all of it. No unrestricted multivariate positivity oracle, hidden coordinate basis, empirical model-identification procedure, or complete SOS solver is accepted.

## 5. Full tails and the acquired Lyapunov bound

For y>=T>1,

    s(y)>=kappa y^4(1-T^-2)^2.

Together with l>=(1-delta sup e)s, this proves the stated analytic tail bound with physical exponent 4m and denominator 4m-1. For u>=s, omit the first factor. The left/right basin symmetry is available only because the declared raw grammar is even in y. The envelope and quadratic coercivity give a finite, positive full Gibbs partition. No reflected finite box is substituted.

The key new global-process join is valid. Since

    (1+t)^2 <= 2(t-1)^2+8,

alpha=min(1/8,kappa/2) obeys s>=alpha(1+t)^2. With h=alpha(1-delta sup e)>0, each admitted N_j obeys

    N_j >= c_j h^d_j (1+t)^(16+2d_j).

Writing N_j/c_j=sum b_k t^k and L_j=sum |b_k|, D_j<=16+2d_j, we have for t>=0

    |2t N'_j/c_j| <= 2D_j L_j(1+t)^D_j.

Dividing by the strictly positive lower bound proves |2t N'_j/N_j|<=2D_j L_j/h^d_j. Here N'_j is the t derivative. Since a_j(y)=N_j(y^2)/(1+y^2)^16,

    y (d a_j/dy)/(d_j a_j)
      >= -[2D_j L_j/h^d_j+32]/d_j.

The 32 is exactly 2*16*t/(1+t)<=32, not a missing chain-rule factor. Choose K=1+max_j of these positive bounds. For V=1+y^2+K z^T M^-1 z,

    LV = -2 sum_j [y a'_j+K d_j a_j] phi_j
             + 2(1+Km)/beta
       <= 2(1+Km)/beta.

Every phi_j>=0. V is coercive for each fixed finite SPD M, while the smooth rational drift is locally Lipschitz. The stopped Lyapunov argument proves nonexplosion. With finite Gibbs mass and the matched constant-mobility reversible interface, this supplies the conservative global diffusion/Dirichlet process used by the capacity definition. K may be extremely large and is not a relaxation estimate; its size does not enter the conductance interval. No computational evaluation of M^-1 is required by the theorem.

## 6. Sensitive errors: true rate amplification, not merely a loose bound

The sensitive-profile expansions are correct:

    r_epsilon(y)=2[1-(1-epsilon)y^2+O(y^4)],
    r_epsilon(1+x)=a+(4+3epsilon/4)x^2+O(x^3),
    a=1+epsilon/4.

For fixed 0<epsilon<1/4 and fixed p=2 or 4, the extrema used by the Laplace argument are unique and nondegenerate on their integration domains. The left-basin integral has one minimum, at -1; by evenness it equals the integral around +1 over [1/2,infinity). There is no missing factor of two in that basin mass. The resistance slab contains the whole neighborhood of its interior maximum at zero, giving the stated full Gaussian factor.

The Jensen resistance has the same quadratic local exponent as R0. Away from zero its scalar base is strictly below its maximum, and the basin tail estimate controls the unbounded remainder. Therefore Rplus/R0 tends to one. Since every actual rate is squeezed between k_free R0/Rplus and k_free, convergence k_M/k_free->1 is uniform over the declared U and fixed-finite-M families, even if a different admitted U or M is selected at each dimension.

Consequently the displayed actual-rate ratio is correct, and its logarithm divided by m tends to log(1+epsilon/4)>0. This disproves dimension-independent worst-case geometric-error budgets that purport to guarantee a fixed relative rate accuracy for all dimensions. It does not by itself give a finite-m tolerance threshold, a uniform shrinking-epsilon asymptotic, empirical calibration accuracy, or an arbitrary-start passage-time theorem.

## 7. Flat errors: localization defeats a universal global error floor

The four flat-profile Taylor expansions are correct. The outer interval ratio equals

    [MA(l)/MA(u)] [Rplus(u)/R0(l)].

Its Laplace limit is exactly

    sqrt[(4+delta/4)/(4-delta/4)]
      * sqrt[(1+delta)/(1-delta)].

Both barrier heights remain 2 and both basin minima remain 1; only local curvatures enter. For delta=1/500 the limit is approximately 1.002127262085632. This limit concerns the outer interval, not equality of all actual rates. Replacing the localized profiles by global constant rescalings instead contributes [(1+delta/16)/(1-delta/16)]^(2m), so it can be exponentially more pessimistic while remaining valid. This is not a proof that every error shape is harmless or that finite receiving can be omitted.

## 8. Finite-probe obstruction: valid scope and global legitimacy

For a finite transcript with maximum derivative order r, the polynomial H=product_i||z-z_i||^(2r+2) is nonnegative and all its derivatives through order r vanish at every queried transverse point. Hence F_A=F0+A b(y)H(z) gives exactly the same finite values/jets; the adaptive claim follows inductively from the matching transcript. For no queries H=1 and z.grad H=0, which is the trivial exception to the positive-degree leading-term sentence.

For at least one query, H's leading term is ||z||^(2n(r+1)), so z.grad H has a strictly positive coercive leading term and a finite global lower bound. Its zero set is finite and hence null when m>=1. The scalar trial that transitions across I gives the stated capacity upper bound. Dominated convergence applies against the integrable F0 density and sends this upper bound to zero; the unnormalized basin mass is unchanged. Each fixed alternative is a legitimate finite-SPD diffusion, not a singular mobility limit.

The modified Lyapunov argument works. One can explicitly construct psi(y)=g(y^2), where g' transitions smoothly from 0 to 1 between 1/9 and 1 and an additive constant makes g(t)=t for t>=1. Then psi is flat on |y|<=1/3, equals y^2 outside |y|>=1, and 0<=psi'/(2y)<=1. The nominal drift coefficient is nonnegative with K=1+C_psi*kappa because y s'/s>=-kappa. The new longitudinal drift vanishes where b is supported. The remaining term -2K A b z.grad H is bounded above for each fixed A, and all diffusion trace terms are bounded. This yields a coercive LV<=C_A bound and nonexplosion.

**Scope restriction:** constructing H after the realized transcript proves a deterministic/pathwise compatibility obstruction: the transcript does not logically certify any nonzero universal lower factor among unrestricted smooth models. It does NOT alone prove a fixed-alternative high-probability lower bound for randomized algorithms with continuously distributed query locations. No such statistical-confidence conclusion is accepted from this frozen file. The separate root addendum uses a different fixed-barrier/coupling construction for that purpose.

Neither obstruction applies to the complete bounded-degree rational coefficient input, a known finite-dimensional class with enough interpolation data, globally certified derivative/regularity bounds, or other richer oracles without a separate argument. UNKNOWN is a valid response, not a contradiction.

## 9. Independent executed checks and limits

`check_theorem_algebra.py` never imports candidate code. It passed **425 exact assertions** covering: profile derivatives and bounding identities; all denominator-clearing/anchor/leading-degree identities; all sensitivity quadratic coefficients; projective Bernstein identities and exact left/right de Casteljau subdivision for degrees 0 through 24; representative rational atom lower/log-derivative inequalities; and all frozen-source bindings. The general inequalities are justified above, not replaced by representative test points.

The script also records explicitly NONPROOF high-precision quadrature diagnostics at m=32,128,512 for two sensitive errors. They agree with Rplus/R0->1 and the displayed Laplace factors but are not interval certificates and are not counted as finite numerical receiving. At m=512, the observed p4 intrinsic ratio remains about 1.0059; an asymptotic limit must not be mistaken for an already-achieved target.

No external source retrieval was needed for this independent derivation audit. No historical-priority, novelty, general-complexity separation, physical calibration, or civilization-scale claim is established. The result is a rigorously scoped mathematical robustness extension with explicit acquisition and information-access boundaries. The standalone executable and its saved finite cases still require their separate complete receiving review.
