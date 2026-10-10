# Focused independent end-to-end check and constructive addendum

Review date: 2026-10-09 UTC.

## Verdict first

**The uniform mathematical existence/bit-complexity theorem survives this focused check, with the explicit implementation lemmas and small mesh/input repairs below.** I did not find a fatal gap in the algebraic projector argument, the gap distortion argument, the superadiabatic sign or finite-order contraction, or the bounded-action complex contour argument. Restriction to fixed dimension and degree is not required by any step checked here.

The important addition is a fully specified projector-jet linear system and a precision argument separating the conditioning of a *grouped projector* from the internal precision of a rational-matrix spectral calculation. This fills the least explicit part of v1. This is a mathematical proof check and constructive addendum, **not** a certified implementation, practical speedup, new numerical benchmark, exhaustive independent verification, or historical novelty certificate.

### Exact theorem retained

Let `H(t)` be an explicitly represented `n` by `n` Hermitian matrix polynomial on `[0,1]`, of degree at most `p`, whose complex rational coefficients have bit length at most `B`. Let `Omega > 0` be rational with total binary encoding length `w`. Given an integer accuracy parameter `s >= 1`, there exists a deterministic algorithm that returns a dyadic complex matrix `V` satisfying

    ||V - U(1)||_op <= 2^(-s),
    i U'(t) = Omega H(t) U(t),    U(0) = I,

in bit work polynomial in `n, p, B, w, s`.

This is the full physical-coordinate endpoint matrix and includes arbitrary initial vectors. Its dimension dependence is polynomial in the explicitly supplied matrix dimension, not in a many-body qubit count. The statement does not supply free phase, eigenbasis, gap, connection-matrix, or propagator oracles.

For an arbitrary rational tolerance `epsilon`, charge its actual input length, or use a conventional accuracy input `s = ceil(log2(1/epsilon))`. A claim polynomial solely in `log(1/epsilon)` cannot silently ignore an arbitrarily long redundant rational encoding of a tolerance near, say, `1/2`. Also, for rational `Omega`, use its encoding length, not literally `log Omega`, which could be negative. These are input-contract repairs, not dynamical obstructions.

## Materials checked and preservation

The originals were read without modification:

- `NATIVE_DETERMINISTIC_THEOREM_v1.md`, SHA-256 `6e4a6a1ff335f856c465aa5cbf11ff6caeee40125ee853c5e17b3a3ffbe18609`
- `algebraic_rotation_gap_lemma.md`, SHA-256 `f6ef544f2ef121d493546eb1a6750b56c705ed1da1bb1ba62be4c52fbba28bca`
- `local_superadiabatic_contraction.md`, SHA-256 `e2c3f036bf2fa258eea7fc267f39af3550b962fd8a19c45b414a8b793c890998`

The review focused on the proposed proof, rather than reopening an opportunity scan or auditing every historical attribution. The two load-bearing external complex-analysis statements were checked in their cited papers. The rest of the local analytic mechanism was checked directly.

## 1. Algebraic reduction and complex projector/gap control

### 1.1 Squarefree reduction is legitimate, including persistent multiplicity

The monic squarefree part `q` of the characteristic polynomial over `Q(i)(t)` is a monic polynomial in `t,lambda`. Integrality of monic factors and polynomial root growth give the claimed coefficient degrees: the coefficient of `lambda^(r-j)` has `t`-degree at most `jp`.

For generic real `t`, the Hermitian matrix is diagonalizable and `q(t,H(t))=0`. As a polynomial matrix identity this extends to every complex `t`. On a discriminant-free disk, the divided-difference expression therefore supplies the projector onto the *whole* distinct eigenspace. No perturbation to split a persistent multiplicity is necessary.

At complex points outside the discriminant, `q` has distinct roots and annihilates `H`; hence the spectral resolution used in the resolvent argument is valid there, even though the matrix is not Hermitian there.

### 1.2 The polynomial degree/valency bound is polynomial, not factorial

For a scalar compression `f=u*P_j v`, the displayed resultant annihilator has `t`-degree at most `m=r(r-1)p`. Selecting the irreducible factor of a nonconstant branch removes the issue of an identically vanishing specialization. Its equation at any fixed value of `f` then has at most `m` zeros, with multiplicity. This argument uses individual branches and never forms a splitting field.

The corresponding resultant for all eigenvalue differences has the same upper bound `m` for its `t`-degree. Thus a nonconstant gap and its reciprocal are `m`-valent; both are regular and nonvanishing on the discriminant-free disk. Constant cases must be separated, as the lemma already says.

### 1.3 The cited Bernstein and distortion inputs actually provide the needed bounds

Roytwarf–Yomdin, *Bernstein classes*, Theorem 3.3.1 and Corollary 3.3.2 on printed pages 844–845, give coefficient-height-independent growth control from valency. Proposition 2.1.5 supplies the real-segment comparison. The displayed dependence on the valency parameter is exponential up to a polynomial factor; for fixed geometric ratios its logarithm is `O(1+m)`.

Primary paper: https://www.numdam.org/article/AIF_1997__47_3_825_0.pdf

Friedland–Yomdin, *(s,p)-Valent Functions*, Theorem 3.1 on PDF page 6, states exactly the nonvanishing-valent modulus distortion used in the lemma, referring to Hayman's Theorem 5.1. I checked the statement in this paper; I did not independently reprove Hayman's theorem or inspect the original book.

Primary paper containing the stated result: https://arxiv.org/pdf/1503.00325

The sources are not being used to assert a pre-existing propagation algorithm. They establish the two external analytic estimates, which are applied here to explicitly constructed algebraic functions.

### 1.4 The radius shrink repairs the exponential-norm problem

The scalar real-axis bounds hold for every fixed unit `u,v`, including a sum over a cluster. The intermediate complex norm can be `n exp(Cm)`. The Chebyshev truncation and Bernstein–Walsh argument in the companion lemma then shrinks the usable radius by `O(1+m+log n)` and obtains norm at most `2`.

The Chebyshev argument checks out: the parameter-2 ellipse is contained strictly in the rescaled radius-2 disk; truncation degree is `O(1+log M)`; and the small centered disk lies inside the ellipse whose semiminor axis is its radius. Uniformity in `u,v` allows passage back to the operator norm.

The rapid-rotation counterexample in the lemma correctly explains why one cannot instead claim polynomial projector norm on a fixed fraction of the discriminant distance. The construction pays the necessary shrink, so this counterexample does not defeat it.

**Result of this section:** the original individual and cluster projectors, and every original nonzero gap, have the claimed height-independent local control on a disk of radius `d/poly(n,p)`. No growing-dimension obstruction was found.

## 2. Global acquisition and two small mesh repairs

### 2.1 Height and root-separation costs enter logarithmically

The characteristic polynomial, its squarefree part, and its discriminant have polynomial degree and logarithmic height in the native dense input. Clearing rational denominators does not change this. Univariate certified root isolation/approximation therefore works with polynomially many bits. Nonreal roots have conjugates, so their nonzero imaginary heights have inverse logarithms bounded by a polynomial in the degree and height.

Real discriminant roots in `[0,1]` can be enclosed in rational holes with a positive dyadic margin and total length at most the specified `epsilon/(16 max(1,Omega M_H))`. Replacing physical propagation by identity in the holes costs at most `Omega M_H` times their total length. This is a unitary Duhamel estimate; it does not need a spectral basis at a crossing.

### 2.2 Repair: real roots just outside the interval

The text's statement that all retained points are separated from real roots by the expanded holes does not cover real roots immediately outside `[0,1]`. Add the following sentence to the proof:

> For real roots outside `[0,1]`, apply root separation to the squarefree part of `Delta(t)t(t-1)`. Unless such a root equals an endpoint, its distance from that endpoint is at least `2^(-poly(degree,height))`; roots at endpoints are covered by the holes.

This supplies the missing lower bound without making extra holes or charging inverse distance.

### 2.3 Repair: the cap `d(c)=min(1,dist(c,Z(Delta)))`

A rejected coarse panel need not be close to any root when the cap `d=1` is active. Account separately for panels whose half-width exceeds a constant multiple of `1/(n kappa)`. A binary tree contains only `O(n kappa)` such coarse panels per initial retained interval, up to an absolute constant. At all finer scales, rejection implies proximity to some discriminant root, and each root charges only `O(n kappa)` panels per depth.

There are polynomially many initial intervals, roots, and depths. The claimed polynomial panel count follows. This is a proof-bookkeeping correction, not a need for a finer asymptotic mesh.

Certified constant-factor lower estimates for the root distances avoid undecidable equality tests. Use rational upper bounds for any expression such as `log(n+1)` in the actual acceptance threshold.

## 3. Superadiabatic sign, domains, and finite-order contraction

The recurrence sign is correct. For a complete differentiable projector family, let

    S = sum_a P_a' P_a,    K = i S.

Then `[S,P_a]=P_a'` and `[K,P_a]=i P_a'`. On the real axis, `S*=-S`, so `K` is Hermitian. Consequently

    H_ad,N = H_N + Omega^(-1)K_N

satisfies

    d/dt [V(t,s)* P_Na(t) V(t,s)] = 0

for `iV'=Omega H_ad,N V`. The alternative sign would be wrong; the sign actually printed in v1 is the right one.

The use of

    H_j = H - Omega^(-1) K_(j-1)

also checks out: it makes the physical perturbation exactly `K_N-K_(N-1)` after multiplication by `Omega`.

The union-of-small-disks contour gives a resolvent bound `8n/g` for the original matrix, a perturbed resolvent bound `16n/g`, and projector Lipschitz bound `64n^3/g`. The contour length is bounded by the sum of the circumferences. Selected and unselected eigenvalues cannot lie on the boundary. Holes in the union use their oriented boundaries; tangencies are harmless by a limiting argument.

After the initial `R/4` loss,

    ||K_0|| <= 16n/R.

On the subsequent `N` strips of width `h=R/(4N)`, the difference contraction factor is

    q = 1536 n^4 N / (Omega g R).

The stated threshold makes `q<1/2` and keeps every perturbation in the ball `g/(128n^3)`. The geometric sum then gives `||K_j||<=32n/R` and the displayed `q^j` difference estimate. The domain indices work: the previous two connections are both available on the next outer disk when the Lipschitz estimate is applied.

This is a *finite-order* construction. It is not a claim that the recurrence converges as `N` tends to infinity for fixed `Omega g R`. The accuracy-dependent clustering raises the effective gap threshold with `N`, which is exactly what the proof needs.

Because both physical evolutions are unitary on the real line, the error is the integral of the generator difference without an exponential real-time stability penalty.

## 4. Bounded-action clusters and phase extraction

The contour in Section 5 of v1 is correctly scaled by `b`, not by a potentially much larger external gap. Its boundary length is at most `pi n b/4`, and the resolvent bound for `H_N` is `32n/b` when `T>=1024n^2`. The weighted Riesz formula therefore gives

    ||(H_N-lambda_ref,a)P_Na||
       <= 4 n^2 (4 n b + b/8).

No full spectral width or `||H||/g` is hidden in this estimate. Apply it on the disk on which `H_N` has actually been constructed, in particular `D(c,R/2)`; it is not necessary to claim that the iterated object exists on the entire original radius-`R` disk.

For `W'=-i K_N W`, both `W` and `W^(-1)` have norm at most `exp(1/4)<2` on `D(c,4 ell)`, using `R=512 n ell`. These are holomorphic inverses. A conjugate transpose must not be used at complex arguments, as v1 correctly notes.

In the constant center basis the blocks of `W^(-1)H_NW` are decoupled. After subtracting the original algebraic branch `lambda_ref,a`, the normalized generator has norm at most `M=poly(n)T` on a fixed disk. Its fundamental solution has norm at most `exp(4M)` there. Consequently a Taylor order

    L_block = O(M + s + log(Q+1))

with a sufficiently large absolute constant gives certified endpoint truncation error. A weaker polynomial upper bound also suffices.

The scalar phase must be evaluated separately, exactly as proposed. Taylor-expanding the full oscillatory phase as part of the block ODE would reintroduce a cost proportional to the large action. That is not the algorithm specified here.

### Explicit phase acquisition without another oracle

At rational `c`, isolate the selected root of the exact polynomial `q(c,lambda)`. Its derivative in `lambda` is nonzero. Implicit power-series substitution determines its next coefficient by a single division by that derivative. The eigenvalue is bounded on the original disk by a coefficient norm bound for `H`, with polynomial logarithm. Since `ell/R=1/(512n)`, integrating the series term by term has a geometric tail.

The required number of coefficients is polynomial in the native bit parameters and in `s`; the absolute phase accuracy is chosen of order `2^(-s)/(Omega poly(n)(Q+1))`. Root separation for `q(c,lambda)` bounds the logarithm of every necessary inverse internal gap polynomially. This computation deals with one algebraic root at a time, not a compositum.

Certified elementary argument reduction on the real endpoint phase needs precision proportional to the logarithm of its magnitude and to the requested output bits. Both are polynomial. This is consistent with arbitrary large binary `Omega`.

## 5. Constructive projector-jet lemma closing the representation issue

Here is an explicit substitute for the potentially ambiguous instruction to solve in approximate invariant subspaces.

Let

    A(t) = sum_k A_k (t-c)^k,
    P(t) = sum_k X_k (t-c)^k,

where `A_0` is Hermitian, `P=X_0` is an orthogonal spectral group projector, and its spectrum is separated from the complementary group by at least `gamma>0`. Put `Q=I-P`. Define linear maps on all `n` by `n` matrices by

    D(X) = P X P + Q X Q,
    O(X) = P X Q + Q X P,
    L(X) = D(X) + O([A_0,X]).

The operator `L` is invertible on the full `n^2`-dimensional complex matrix space. In an orthonormal eigenbasis of `A_0`, it acts as the identity on within-group matrix entries and multiplies each cross-group entry by an eigenvalue difference. Therefore, for the Frobenius norm,

    ||L^(-1)|| <= max(1,1/gamma).

This inverse involves **no within-group inverse gap**.

For `k>=1`, define from already acquired coefficients

    S_k = sum_(j=1)^(k-1) X_j X_(k-j),
    R_k = -sum_(j=1)^k [A_j,X_(k-j)],
    D_k = -P S_k P + Q S_k Q.

Then the coefficient is determined by the single ambient linear solve

    X_k = L^(-1) [D_k + O(R_k)].

The diagonal part follows from idempotence, and the cross-group part follows from commutation. Existence of the analytic Riesz projector guarantees compatibility of the remaining identities. All entries of `L`, its right-hand side, and the coefficients can be handled by interval/ball arithmetic; an approximate `P` need not satisfy exact idempotence. It encloses the exact `P`, and the solve is certified against the exact operator using the displayed inverse bound.

At stage `j`, use fixed rational separating cuts selected between the original center groups. The original cut gaps are at least `b`; Weyl's inequality and the normal-form perturbation bound keep the later center gaps at least `b/2`. Thus one may use `gamma=b/2` uniformly. The rational cuts can be chosen with a fixed positive margin and remain valid at every stage.

To obtain `K_N` through order `L`, start with original jets through order `L+N+1`. Stage `j` uses one extra projector order to differentiate in forming `K_j`. Reusing the triangular array gives polynomially many operations and spectral queries. There is no exponentially expanding expression tree.

## 6. Rational spectral-query primitive and global guard bits

### 6.1 The essential separation of two different precision costs

Later `A_0=H_j(c)` need not be rational or have a conveniently sized algebraic description. Suppose it has been enclosed to operator error `delta`. Choose a rational Hermitian midpoint `Ahat_0`. Compute its *grouped* projector to error `eta`. Then

    error relative to the true grouped projector
        <= eta + C n^3 delta/g,

using the already proved group-projector perturbation bound. The rational spectral calculation may internally require more bits to resolve tiny eigenvalue gaps *inside* the group. It does not require the input enclosure for `A_0` to be narrowed to that internal scale.

For a rational Hermitian input of bit length `b_work`, its characteristic polynomial, squarefree part, eigenvalue isolating intervals, and divided-difference individual projectors can be computed with bit complexity polynomial in `n,b_work` and requested output accuracy. Its own distinct eigenvalues have root-separation logarithms polynomial in `n,b_work`; exact multiplicities are handled by the squarefree part. Summing the projectors on the chosen side of the fixed cuts gives the group projector.

Thus this primitive has polynomial evaluation cost and *group-gap* input conditioning, even when its chosen internal implementation resolves much smaller within-group gaps. This is why no recursive precision explosion or growing algebraic tower is forced.

### 6.2 A noncircular global precision bound

Let `S` denote a sufficiently large polynomial bound on the native parameters `n,p,B,w,s`, and let `J=L+N+1`. Root separation and the mesh proof bound the bit lengths of all centers, radii, thresholds and fixed cuts by a polynomial in `S`. `Q,N,T,L,J` are themselves bounded by polynomials in `S`.

For the exact analytic objects, Cauchy on disks of radius at least `R/2` gives

    ||(P_j)_k|| <= 3 (2/R)^k,
    ||(K_j)_k|| <= (32n/R)(2/R)^k.

The corresponding `H_j` bounds include the original polynomial norm and `Omega^(-1)K_(j-1)`. Their logarithms are still polynomial in `S,J`. The center eigenvalue jets have analogous bounds. The later frame and block-solution coefficients have logarithmic bounds polynomial in `S,J,M`, because their complex norms are bounded by `2` and `exp(4M)`, respectively.

Every exact intermediate multiplication, convolution, scalar phase operation, and matrix right-hand side therefore has norm at most `2^K` for one common **a priori polynomial** `K=poly(S,J,M)`. All inverse norms are bounded by `2^K` as well:

- the ambient projector-jet inverse uses only `gamma`;
- the implicit original-eigenvalue solve uses the original rational center polynomial's root separation;
- normalization of a projected basis column uses a certified pivot bounded below by a polynomial in `1/n`;
- endpoint matrices are unitary before numerical approximation.

The grouped-projector primitive has a Lipschitz bound of the same logarithmic size. Standard rational linear solving can be certified with this inverse-norm bound; it is not necessary to assume that arbitrary unpivoted elimination is stable.

Let `M_circ` be a polynomial upper bound for the number of arithmetic/solve/query nodes in the whole triangular computation. On a sufficiently small neighborhood of the exact values, each node has Lipschitz constant at most `2^(poly(K,log M_circ))`. Propagating absolute errors along this finite circuit gives a bound of the form

    total amplification <= 2^(poly(K,M_circ)).

Accordingly, a working precision

    s + log(Q+1) + poly(K,M_circ)

suffices. This is polynomial in the original parameters. The bound is not circular: `K` comes from the exact analytic estimates and original root separation, not from accidentally tiny internal eigenvalue gaps of an increasingly precise rational midpoint. Those gaps only affect the polynomial *cost* of the individual spectral query at the already chosen working precision.

This supplies the constructive conditioning lemma missing from the short formulation in v1. Merely saying that interval Taylor methods exist would not have supplied it.

### 6.3 Center bases

The projected-column construction can also be made interval-certified. The residual orthogonal projector of positive rank has a diagonal entry at least `1/n`. Choose a deterministic pivot whose certified lower bound exceeds `1/(2n)`, then normalize. Repeat within each group and concatenate. The exact pivot selection defines a unitary center basis; intervals enclose its entries. A polynomial number of divisions and square roots with polynomially bounded inverse magnitudes suffices.

## 7. Endpoint reconstruction and error accumulation

With block fundamental matrices `Y_a(c)=I`, the exact local reconstructed matrix is explicitly

    F(t) = W(t) S diag_a[exp(-i Omega phi_a(t)) Y_a(t)] S*.

Here `phi_a(c)=0`, so `F(c)=I`. The physical panel transition is

    F(c+ell) F(c-ell)*,

where the adjoint may be used because the *exact real-axis* factors are unitary. This also avoids an unnecessary numerical inversion. Cross-panel group splits, merges and basis changes require no additional matching oracle: the full physical-coordinate matrices are multiplied in time order.

The local normal-form error, phase error, analytic tails, arithmetic error and matrix-product error admit separate budgets of constant multiples of `epsilon/(Q+1)`. If every approximate transition differs from a unitary exact transition by at most `delta`, product error is bounded by `Q delta exp(Q delta)`. Together with the hole budget and the displayed choice of `N`, this remains below `epsilon` after choosing the harmless constants conservatively.

No exponentially large real-axis condition number is introduced by endpoint matching.

## 8. Reproducible small exact check

`verify_review_projector_jets.py` performs a small exact symbolic test on

    H(t) = [[t,1],[1,-t]],
    P(t) = (I + H(t)/sqrt(1+t^2))/2,

at `c=0`. It verifies five nonzero jet orders from the ambient linear system above against exact derivatives, checks `[K,P]=iP'`, and checks real-axis Hermiticity of `K`. The squared singular values of the ambient map are `1` and `4`, consistent with a center inter-group gap of `2`.

Run from this directory:

    python verify_review_projector_jets.py

The recorded output is `REVIEW_IDENTITY_CHECK.json`; all tests passed. Runtime was approximately half a second in the available environment. This is an exact identity sanity check, not evidence for runtime scaling of the unimplemented full algorithm.

## 9. What remains unresolved, and what does not

After including the explicit additions in this report, I found **no indispensable missing mathematical existence/bit-complexity lemma** in the advertised uniform theorem. The fixed-`n,p` statement is an immediate weaker consequence rather than the only claim retained.

Still outstanding:

1. An executable certified implementation, with a selected numerical value for every universal constant, concrete data structures, full interval error certificates, and tests on adversarial inputs.
2. Practical complexity and comparison against existing high-precision phase-function, semiclassical, and certified ODE methods. The conservative bounds here give no practical speed claim.
3. A focused novelty assessment of the *combined uniform acquisition theorem*. The two analytic tools and the superadiabatic idea are established ingredients. This review does not establish priority or rule out an equivalent known theorem.
4. Further independent mathematical review before presenting the result as settled public research. This single focused check is not a formal proof verification.

In particular, an implementation still must not silently replace the grouped spectral primitive by an ill-conditioned eigenvector-tracking routine, Taylor-expand the large scalar phase with the bounded block dynamics, use a conjugate transpose as a holomorphic inverse, or charge the mesh at the minimum gap uniformly. Each such change would undo a load-bearing part of the proof.

No paid jobs, external computation, numerical campaign, publication, third-party contact, repository push or deployment was performed. Originals were preserved.
