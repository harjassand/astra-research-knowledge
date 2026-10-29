# Frontier review: acquired integrable geometry needs a certified decoder

**Verdict (2026-10-29):** The metric/flag-to-QR candidate and the local-Abel-inversion-to-doubling operation are classical compositions, not algorithmic discoveries. The former also excludes the recurrent compact tori that motivate this direction. A more substantive, still incomplete target is certified growing-genus **physical-output** fast-forwarding for positive periodic Toda, with conditioning derived from rational input rather than promised. The new partial derivations below survive independent algebraic review; no end-to-end algorithm, raw-equation geometry acquisition, or priority claim is established.

## 1. A decisive limitation of the common-flag candidate

Suppose an acquired linear Lax representation has injective `L(x)=Σx_i A_i`, `M(x)=Σx_i B_i`, a positive definite metric making each `A_i` self-adjoint and each `B_i` skew-adjoint, and a common complete invariant flag for all `A_i+B_i`. In a metric-orthonormal flag-adapted basis, `L` is symmetric, `M` is skew-symmetric, and `L+M` is upper triangular. Therefore `M=L_upper−L_lower`: this is the classical symmetric Toda splitting, not a general compact integrable flow.

For `Ldot=[M,L]`, define `F(L)=Σ_i i L_ii`. Direct calculation gives

`Fdot = −2 Σ_(i<j) (j−i) L_ij²`.

Thus no nonconstant periodic trajectory exists in this admitted class. With the opposite commutator convention the sign reverses, with the same conclusion. Injectivity transfers the obstruction to the original state. A block flag merely leaves unresolved dynamics inside the blocks. This excludes, rather than explains, generic Euler-top recurrence and compact recurrent integrable tori.

An exact SymPy check for a generic symmetric 4×4 matrix is saved in `audit/qr_recurrence_obstruction.json`. Classical context: [Symes, QR and finite nonperiodic Toda (1982)](https://doi.org/10.1016/0167-2789(82)90069-0), [Kodama–McLaughlin, full symmetric Toda hierarchy (1995)](https://arxiv.org/pdf/solv-int/9502006), and [Dubi, simultaneous triangularization (2009)](https://doi.org/10.1016/j.laa.2008.05.037).

The strongest equally informed comparator is allowed the same raw circuit, coefficient tensor, ansatz size, and metric/flag information. It can use standard coefficient matching, simultaneous triangularization, and QR factorization. Upstream coefficient acquisition remains a bilinear/quadratic polynomial-system problem. Optimizer success verifies one ansatz; failure does not prove nonintegrability. Exact positive-metric feasibility, algebraic field growth, flag conditioning, the inverse of `x↦L(x)`, and large-time matrix-exponential conditioning must all be charged.

## 2. Compatibility and conservation are not a spectral decoder

[SILO (2025 preprint; 2026 SIAM publication)](https://arxiv.org/pdf/2503.00645) already searches for sparse Lax operators computationally. The subsequent [Learning Lax Pairs: Revisiting the Classical Paradigm (July 2026)](https://arxiv.org/html/2607.01493v1) gives explicit reasons that compatibility is insufficient: learned pairs can be spectrally incomplete or degenerate, and a conservation hierarchy does not by itself certify the intended inverse spectral geometry. The parameter-free Euler hat-matrix Lax form, for example, need not encode all required integrals in its spectrum.

The stronger certificate must exhibit: (i) an injective state representation, (ii) the right spectral curve and divisor/eigenvector data, (iii) the correct translation velocity, and (iv) a full-state inverse with certified numerical complexity. Merely verifying `Ldot=[M,L]`, counting conserved quantities, or borrowing an inverse from the named scientific model does not acquire that geometry from raw equations.

## 3. Local inversion followed by doubling is established prior art

The proposed operation “invert Abel–Jacobi near a convenient divisor, divide the target by `2^m`, then use Jacobian doubling `m` times” is not new. [Couveignes–Edixhoven, Approximate computations with modular curves, §3](https://arxiv.org/pdf/1205.5896), explicitly replace continuation by fast exponentiation. Their polynomial genus/precision theorem is for modular curves and **direct accuracy**, meaning error on the analytic torus. Converting it into accuracy of the output divisor additionally requires quantitative nonspeciality at the target. The source explicitly distinguishes those two errors.

[Mascot, Computing modular Galois representations, §3.5](https://arxiv.org/pdf/1211.1635) implements local Newton inversion and fast Jacobian exponentiation. [Costa–Mascot–Sijsling–Voight, §3](https://doi.org/10.1090/mcom/3373) use the operation for general Jacobians in their endomorphism-ring computations. [Khuri-Makdisi](https://arxiv.org/pdf/math/0409209) supplies polynomial-genus group arithmetic in field operations after curve precomputation; this is not automatically a uniform finite-precision bit theorem. [Tsiganov, Bäcklund transformations and divisor doubling (2018)](https://doi.org/10.1016/j.geomphys.2018.01.017) applies divisor arithmetic to integrable systems. A Bäcklund map is not automatically the requested continuous-time increment.

The more detailed [Couveignes–Edixhoven book, Chapter 12](https://www.math.u-bordeaux.fr/~jcouveig/publi/book.pdf) makes the algebraic/analytic conditioning distinction explicit (§§12.11–12.13), and bounds target conditioning for its special modular/arithmetic divisors. A Toda transfer could be meaningful only by deriving comparable bounds from the physical data, not by renaming them favorable-condition-number promises. No claim is made here that the transfer is absent from all literature.

## 4. Independently checked partial lemma: uniform physical Abel conditioning

Let `y²=∏_(l=0)^(2g+1)(x−E_l)`, with ordered distinct real roots, `|E_l|≤M`, `M≥1`, and pairwise separation at least `Δ`, `0<Δ≤1`. The physical Dirichlet divisor has one point on each real gap oval over `[E_(2j−1),E_(2j)]`, `1≤j≤g`. Write

`μ_j=c_j+r_j cos θ_j`,

`y_j=r_j sin θ_j sqrt(|∏_(l outside gap-pair j)(μ_j−E_l)|)`.

The signed sine records the sheet. The excluded product is negative on the selected gap, as is the product of its two endpoint factors, so this is consistent with the real curve. For the unnormalized holomorphic basis `x^(k−1) dx/y`, the Abel differential is

`J_kj=−μ_j^(k−1) w_j`, where `w_j=|∏excluded(μ_j−E_l)|^(−1/2)`.

This expression extends smoothly and nonvanishingly through the band-edge crossings; the apparent sine zero cancels. Its bounds are

`(2M)^−g ≤ w_j ≤ Δ^−g`.

Different gap coordinates remain separated by the intervening band: `|μ_j−μ_k|≥Δ`. If `V_kj=μ_j^(k−1)`, Lagrange interpolation bounds the coefficient 1-norm of each cardinal polynomial by `((1+M)/Δ)^(g−1)`. Consequently

`||V^−1||₂ ≤ g ((1+M)/Δ)^(g−1)`,

`||J^−1||₂ ≤ g (2M)^g ((1+M)/Δ)^(g−1)`.

The bound is uniform on the whole physical product of ovals, not just away from the band edges. The classical real inverse-spectral identification supplies the global torus interpretation; the displayed calculation proves its quantitative local differential bound. It must not be silently applied to arbitrary complex divisors or to normalized Abel coordinates without charging the basis transformation.

If the branchpoints are roots of a squarefree integer polynomial `F` of degree `d`, leading coefficient `A`, and all roots bounded by `M`, the nonzero integer discriminant gives the elementary lower bound

`Δ ≥ |A|^(−(d−1)) (2M)^(−(d(d−1)/2−1))`.

Thus low-height polynomial input yields polynomial **logarithmic** inverse condition. It does not yield an inverse condition polynomial in dimension itself.

## 5. Independently checked periodic-to-finite Jacobi decoder

Use the periodic recurrence

`a_(k−1) ψ_(k−1)+b_k ψ_k+a_k ψ_(k+1)=λψ_k`,

with `a_k>0`, `ψ_0=0`, `ψ_1=1`. Put `g=N−1`, `C=∏_(i=1)^N a_i`, and let `μ_j` be the zeros of `ψ_N`. Set `G(λ)=∏_j(λ−μ_j)`, so `ψ_N=a_N G/C`. Let `κ_j=ψ_(N+1)(μ_j)` be the signed Floquet multiplier selected by the divisor sheet.

The discrete Lagrange/Christoffel–Darboux identity and the recurrence at `k=N` give exactly

`norm_j = Σ_(k=1)^(N−1) ψ_k(μ_j)²`

`=a_(N−1) ψ_(N−1)(μ_j) ψ'_N(μ_j)`

`=−a_N κ_j ψ'_N(μ_j)=−a_N² κ_j G'(μ_j)/C`.

Therefore

`a_N²=−C Σ_j 1/[κ_j G'(μ_j)]`,

`w_j=−C/[a_N² κ_j G'(μ_j)]>0`, `Σ_j w_j=1`.

Reconstruct the finite `g×g` Jacobi block from its eigenvalues `μ_j` and first-coordinate weights `w_j` by Stieltjes orthogonalization/Lanczos; recover `b_N` from the trace and `a_(N−1)` from `C`. If the discriminant numerator is `p`, then `κ_j=(p(μ_j)±y_j)/(2C)` with the sheet convention fixed accordingly. Use the reciprocal root to avoid cancellation when the chosen multiplier is small.

These are classical inverse-spectral formulas, not a new reconstruction method. [Grava's Toda notes, pp36–38](https://people.sissa.it/~grava/Toda.pdf) give the cyclically shifted equivalent; primary inverse-spectral sources include [Andrea–Berry (1992)](https://doi.org/10.1016/0024-3795(92)90008-X) and [Teschl (1998)](https://www.mat.univie.ac.at/~gerald/ftp/articles/TraceJac.pdf).

The useful quantitative observation is that `H=Σ(b_i²/2+a_i²)` and `C` are conserved, so `a_i≤sqrt(H)` and `a_i≥α:=C/H^((N−1)/2)`. Choose `M≥1` bounding the Jacobi operator norm and all edges. Principal-submatrix interlacing and

`ψ_k(μ)=det(μI−J_(k−1))/(a_1⋯a_(k−1))`

give `|ψ_k(μ)|≤(2M/α)^(k−1)`. Hence

`w_j ≥ [g(2M/α)^(2(g−1))]^−1`.

For the moment Gram matrix `H_mom=V diag(w)Vᵀ`,

`λ_min(H_mom)≥w_min/||V^−1||₂²`.

The same lower bound controls principal moment blocks. This supplies polynomial-log denominator/Cholesky conditioning for Stieltjes reconstruction. Floquet matrices and their inverses have norms bounded by products of `poly(M/α)` factors, so neither selected multiplier nor its reciprocal needs more than polynomially many exponent bits. The signed-angle representation avoids the artificial square-root singularity of `μ`-only coordinates at edges. Derivative/error bounds for the finite sequence of bounded-degree elementary operations can consequently be made explicit. This justifies a **partial physical-decoder conditioning lemma**, not a full fast-forward theorem.

For canonical positions, Flaschka data omit the center-of-mass coordinate. Recover relative positions with logarithms of positive `a_i`, and separately evolve the conserved-momentum center of mass. [Henrici–Kappeler](https://arxiv.org/pdf/0802.4252) establish global Birkhoff coordinates for positive periodic Toda; that qualitative global theorem should not be advertised as the missing bit-complexity theorem.

## 6. Exact open obligation: uniform approximate Jacobian arithmetic

A defensible next theorem would give, for this explicitly encoded real spectral curve and physical torsor, a certified addition/doubling algorithm with time and required precision polynomial in

`g, input coefficient bits, requested output bits`.

It must work **for every** physical divisor, including band-edge crossings and all arithmetic exceptional cases, without promising that a chosen resultant, minor, Euclidean-algorithm pivot, or reduced-divisor chart is bounded away from zero. Intermediate divisors/subspaces in Cantor or Khuri-Makdisi arithmetic need not remain in the well-conditioned physical chart even if the final divisor does. Exact field-operation counts do not bound those numerical losses.

There is a concrete classical route to investigate first: Couveignes–Edixhoven book §12.8 perturbs prescribed points to a separated divisor, rounds an evaluation matrix, chooses a normalized exact kernel vector of that rounded matrix, and bounds nearby true zeros from its small residual evaluations. It then removes those zeros and measures the residual-divisor error on the torus; §§12.9 gives arithmetic and exponentiation. This avoids assuming a safe kernel minor. Transferring its norm-equivalence and quantitative zero-closeness bounds from modular forms to explicit hyperelliptic polynomial forms is an exact technical target, not a new arithmetic principle.

Another possible route is a quantitatively controlled atlas or randomized auxiliary-divisor perturbation, followed by certified return to the physical chart. This is only a candidate: one must bound degrees/heights of bad loci, probability of a safe chart, the cost of finding it, all error propagation, and failure probability. Fixed low-genus complete formulas do not prove uniform growing-genus complexity. A generic projective embedding may itself have dimension exponential in genus.

For actual time evolution, additionally prove the acquired translation identity

`[D(t)−D(0)] = exp_J(t v)`.

Doubling a raw divisor is not time doubling. Scaling by `2^m` amplifies analytic-torus input error by `2^m`, requiring at least `m+output_bits` working accuracy. The good local chart, its integration/Newton radius, the exact velocity and its evaluation, and the final physical decoder must all be charged. Closed gaps require a separate genus-reduction/degenerate analysis; the all-distinct-root lemma does not cover them.

Finally, this entire Toda construction still starts with known Toda geometry. It is a valuable scientifically anchored decoder test, but not an acquired hidden-geometry capability until raw equations yield and certify the spectral representation at a charged cost. The strongest baseline is the same classical inverse-spectral machinery, equally informed about the raw syntax and allowed ordinary symbolic pattern recognition. The honest current deliverable is the derived conditioning bridge and an exact remaining computational obstruction—not superiority over that baseline.
