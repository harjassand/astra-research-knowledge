# Independent review: closed gaps and the signed Toda Abel velocity

**Verdict: the proposed reduction and the velocity `(0,…,0,−2)` are correct with the stated conventions.** Use the signed quotient `y/K`, retain **all** Dirichlet roots for the physical decoder, and use the radical `F/K` (not only the reduced curve polynomial) for the decoder's separation bound. This is a classical closed-gap normalization, not new inverse-spectral machinery or a completed fast-forwarding algorithm.

Reviewed the actual `PERIODIC_TODA_CONDITIONING_BRIDGE.md` and the parent's proposed extension. At this review the saved draft still explicitly excluded closed gaps. The mathematical acceptance below concerns the extension stated here; it does not assert that an end-to-end certified implementation exists.

## 1. Primary-source checks

* Teschl, *Jacobi Operators and Completely Integrable Nonlinear Lattices*, §7.2, Eqs. (7.37), (7.41), (7.42), (7.50), proves the finite Dirichlet identification, periodic/antiperiodic determinant identities, edge ordering, and gap localization. **Remark 7.6, Eqs. (7.64)–(7.65), explicitly removes the product of closed-gap factors because the corresponding Dirichlet roots equal the collapsed edges.** Printed pp120–124; PDF pp133–137. [Author's primary monograph](https://www.mat.univie.ac.at/~gerald/ftp/book-jac/jacop.pdf).
* Henrici–Kappeler, *Global Birkhoff coordinates for the periodic Toda lattice*, §2, Eqs. (16)–(18), (23)–(25), states strict separation between adjacent bands, possible equality only within gap pairs, simple Dirichlet eigenvalues, and one Dirichlet root in each closed gap interval. The paper's indexing is cyclically shifted from this draft. [Original research manuscript](https://arxiv.org/pdf/0802.4252).
* Teschl's *Trace Formulas and Inverse Spectral Theory for Jacobi Operators*, Corollary 6.3, gives the one-band constant-coefficient case. [Original paper, CMP 196 (1998)](https://www.mat.univie.ac.at/~gerald/ftp/articles/TraceJac.pdf).

These sources confirm the structural facts. The exact time sign below is independently derived rather than copied across differing sheet/index conventions.

## 2. Multiplicity and the closed factor

Let `L+` and `L−` be the real symmetric `N×N` Jacobi matrices with corner entries `+a_N` and `−a_N`, respectively (`N≥3`). With the draft's transfer product and `C=∏a_i>0`,

`det(λI−L±)=p(λ)∓2C`.

Every eigenfunction of either matrix extends to a recurrence solution fixed by two initial values. Thus each eigenspace has dimension at most two; real symmetry equates algebraic and geometric multiplicities. The two characteristic polynomials have no common root since `C≠0`. Consequently **every root of `F=p²−4C²` is real and has multiplicity one or two**, never greater.

The standard edge ordering is

`E0<E1≤E2<E3≤…≤E_(2N−2)<E_(2N−1)`.

Only a gap pair can coalesce. The finite principal `(N−1)×(N−1)` Jacobi matrix is irreducible; its eigenvalues, the zeros of `G`, are simple, with `μ_j∈[E_(2j−1),E_(2j)]`. Therefore every closed gap has exactly one fixed Dirichlet root.

There is also a direct monodromy check: at a double eigenvalue of `L±`, its two independent eigenfunctions span all recurrence initial conditions, so `M(λ)=±I`. With `ψ0=0, ψ1=1`, this implies `ψN=0` and `κ=ψ_(N+1)=±1`. At a simple open-gap edge the monodromy need not be `±I`; it generally has one eigenvector. Do not conflate a repeated Floquet multiplier with a double root of `F`.

Let `r` be the number of closed gaps. Then

`K=monic gcd(F,F')`, `Ftilde=F/K²`, `g'=N−1−r`,

where `K` is squarefree, `Ftilde` is squarefree of degree `2g'+2`, and they are coprime. The full Dirichlet polynomial factors **exactly** as

`G=K Gactive`, `deg Gactive=g'`.

The closed multipliers can be recovered without algebraic sign guesses:

`Kplus=gcd(K,p−2C)`, `Kminus=gcd(K,p+2C)` (monic),

`K=Kplus Kminus`, with `κ=+1` and `−1`, respectively.

## 3. Exact time sign, including endpoints

Let `J` be the finite block on sites `1,…,N−1`, and `B` its skew tridiagonal matrix with upper entries `a_i`. Direct substitution of the specified Toda flow gives

`J'=[B,J]+diag(−2a_N²,0,…,0,+2a_(N−1)²)`.

For its eigenvector normalized by `ψ1=1`, set `S=Σ_(i=1)^(N−1)ψ_i²`. Hellmann–Feynman and the recurrence at site `N` yield

`μ'=2a_N²(κ²−1)/S`, since `a_(N−1)ψ_(N−1)=−a_N κ`.

The draft's discrete Lagrange identity gives

`S=−a_N² κ G'(μ)/C`.

Since `κ+κ^-1=p(μ)/C`, defining **exactly**

`y=2Cκ−p(μ)=C(κ−κ^-1)`

therefore gives

`μ'=−2y/G'(μ)`.

Closed roots have `κ²=1`, hence zero velocity. At an active root, `K(μ)≠0`; define `ytilde=y/K(μ)`, so

`ytilde²=Ftilde(μ)`, `μ'=−2ytilde/Gactive'(μ)`.

The **sign of K matters**. Replacing it with `|K|` can reverse the flow on an oval. At a reduced branch endpoint, the lifted smooth equations are

`μ'=−2ytilde/Gactive'(μ)`, `ytilde'=−Ftilde'(μ)/Gactive'(μ)`.

They extend across `ytilde=0`; the eigenvalue-only square-root equation is not an adequate branch-crossing prescription. For the reduced holomorphic basis `ω_l=λ^(l−1)dλ/ytilde`, Lagrange interpolation gives

`dA_l/dt = −2 Σ_active μ_j^(l−1)/Gactive'(μ_j) = −2 δ_(l,g')`.

The expression extends through endpoints in the local branch coordinate. This is the unnormalized Abel basis; any normalized basis requires its actual linear transformation. For `g'=0` the velocity vector is empty and the physical isospectral set is a point: positive coefficients are constant in space and the Toda state is stationary.

## 4. Decoder and conditioning qualifications

The finite decoder still needs the original degree-`N−1` polynomial `G`, its closed and active roots, and all corresponding multipliers. Closed roots contribute positive spectral weights and must **not** be removed from

`a_N²=−C Σ_all 1/[κ_jG'(μ_j)]`,

`W_j=−C/[a_N² κ_jG'(μ_j)]`.

For a closed root `c`, `G'(c)=K'(c)Gactive(c)≠0`. Genus reduction removes redundant curve nodes, not finite Jacobi eigenvectors. Reconstruction by the full spectral measure and Stieltjes procedure remains valid.

For root separation use the squarefree radical

`R=F/K=K Ftilde`.

A separation bound from `Ftilde` alone omits closed nodes needed by the decoder. Clearing denominators of `R` and applying the draft's discriminant argument controls separation among **all** distinct original edges. Exact rational gcd/squarefree operations and their coefficient heights have polynomial bit bounds. The existing energy/product lower bound on `a_i` and finite norming weights survives unchanged. The Abel bound uses `g'`; the finite decoder retains size `N−1`. Handle `g'=0` separately instead of substituting it into formulas with negative exponents.

This treats exact closed gaps. Numerical near-equality is not proof of a closed gap, and noisy-data rank/gcd identification has no stability guarantee here. The outstanding certified approximate Jacobian-arithmetic and raw-equation geometry-acquisition obligations remain open.

## 5. Independent exact regressions

`closed_gap_toda_replay.py` imports no producer code. Four rational cases pass: period-two data represented at `N=4`; period-three data represented at `N=6`; the all-closed equilibrium at `N=4`; and generic open-gap `N=3` data. It checks both finite characteristic identities, real/simple-or-double roots, all gcd factors, `M=±I` modulo the closed factors, and the signed Dubrovin identity by independently differentiating the finite determinant along the raw Toda vector field. It verifies the reduced Abel vector by exact polynomial interpolation, and reconstructs **every** original `b_i,a_i²` using the full-G moment/Stieltjes decoder. A generic symbolic `N=3` sign identity also passes.

Concrete sign trap: for `a=(1,2,1,2)`, `b=(0,1,0,1)`,

`K=λ²−λ−5`, `Gactive=λ`, `ytilde(0)=3`, hence `μ'=-6`.

Since `K(0)=-5`, using `|K|` incorrectly gives `+6`.

Audited hashes:

```
PERIODIC_TODA_CONDITIONING_BRIDGE.md (before proposed extension)
ec7e2058c03b4db327b8a54975d10b76d85288155f03fad84f8f38f69982ace4
audit/closed_gap_toda_replay.py
de892f4392876bd0caefeb19918ff8ad621b6cd770286526a0ffb4dd7f49a55d
audit/closed_gap_toda_replay.json
8bf0c22e974a661693c2247407a4d1beb2662f66a32be1b8c102bb8b409374b9
```
