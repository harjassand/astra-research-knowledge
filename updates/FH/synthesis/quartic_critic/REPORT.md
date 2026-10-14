# Independent adversarial audit: full-cone quartic rigidity

**Audit date:** 2026-10-14 (Australia/Brisbane)  
**Disposition:** no countermodel or proof-breaking defect found in Claims A–D on the stated scope. The analytic arguments appear internally sound after independent reconstruction of their load-bearing steps. This is a proof review, not formal verification, external validation, or a novelty determination.

## Scope and inputs

I reviewed the supplied note `../FH-sources/quartic/ASTRA_FULL_CONE_RIGIDITY.md`, its standalone verifier and exact-results file, its SHA-256 manifest, and `../FH-sources/quartic_PASTED_SOURCE.txt`. The source verifier was read but not run or imported. The fresh checker in this directory was written from the definitions and checked algebra; it does not import or execute producer code. All listed note-package hashes match.

For capital context I read `00_START_HERE.txt`, the scoped N740/N794/N797 notices and their relevant quartic proofs, including the N794 sharp-slice proof and N797 tensor/compatibility scope. The read-only capital checkout is at PR #83 head `74a1ab09ba75324bc3d2a14f05ce6196f43ffd77`; the stated pinned base `ace0cfc4437fe91c20ccd24d69e0ee4bb335e871` resolves locally. The checkout was clean. The capital notices correctly keep the full nine-coefficient implication open; the full-cone note narrows that status only on exact singular averaged-Hessian faces.

No FH-quartic worker artifacts were read. No repository files were edited. The literature access ledger is in `PRIMARY_ACCESS_LEDGER.md`.

## Main mathematical verdict

The singular-face closure mechanism is coherent. Its essential point is the exact use of **one indefinite quadratic constraint**. The Finsler step yields a positive-semidefinite quadratic remainder; equality in its average confines the law to that remainder's kernel. Rank-one second variations then make the Hessian of the cubic `X ↦ DF(X)[A]` vanish on the null cone of the restricted determinant. The quadratic null-cone lemma and cubic-tensor symmetry eliminate the cubic in the indefinite case; a semidefinite restriction plus the zero determinant mean places the law on the null cone and closes the same equality directly. This proves pointwise support closure, not just `b ⟂ ker H` by an averaged cancellation.

The downstream full-cone argument also appears sound. Its exact boundary is material: Theorem C proves Jensen only when the averaged Hessian is singular. The full positive-definite sector remains open, as do quantitative estimates uniform near singularity and limits of sequences of nearly singular fields. I found no argument in the note that silently crosses that boundary, and no evidence that the full nine-coefficient rank-one-convexity-to-quasiconvexity implication has been established.

## Load-bearing claims reconstructed

### A. One-quadric Finsler equality and cubic closure

For any `q` taking both signs, if `Q ≥ 0` on `q=0`, then on the plane spanned by any `x,y` with `q(x)>0>q(y)`, the restriction of `q` is a nondegenerate indefinite binary form. In coordinates `s²−t²`, null-cone nonnegativity of `Q=a s²+2c st+b t²` gives `a+b ≥ 2|c|`; choosing `λ=(a−b)/2` makes `Q−λq` positive semidefinite on that plane. Evaluating at `x,y` orders all ratios `Q(x)/q(x)` and `Q(y)/q(y)`. Their global supremum/infimum are finite by fixing one vector of each sign, so a common `λ` exists. This handles arbitrary radical directions because only two nondegenerate opposite-sign vectors are needed.

For the quadratic equality lemma with a radical, null vectors in the nondegenerate part span it. Translating any such null vector by an arbitrary radical vector and comparing `r` with `−r` forces the mixed block and radical block of a vanishing quadratic form to be zero. On the nondegenerate part, testing normalized positive and negative vectors shows the two diagonal blocks are opposite scalar identities and the mixed block vanishes. Thus the form is a scalar multiple of `q`.

For the cubic integrability step, write `D²C(Y)=λ(Y)q` on `U`. In a diagonal basis, for every coordinate `k` choose a distinct index `i` with `q_ii ≠ 0` (indefiniteness supplies at least two nonzero diagonal coordinates). Symmetry of `D³C` gives
`λ(e_k) q_ii = D³C(e_k,e_i,e_i) = D³C(e_i,e_k,e_i) = λ(e_i) q_ki = 0`.
Hence `λ=0`, and homogeneous cubic `C` vanishes. This argument covers every indefinite signature and any radical dimension.

In Theorem A, quartic polarization gives `D²F(A)[X,X]=D²F(X)[A,A]`. Averaging the Finsler decomposition over a law with `E q=0` proves `H ⪰ 0`. If `A ∈ ker H`, the nonnegative remainder vanishes almost surely. For every supported `R` with `q(R)=0`, the globally nonnegative quadratic polynomial `t ↦ D²F(A+tY)[R,R]` has a zero at `t=0`; its derivative vanishes. Quartic tensor symmetry converts this into the cubic Hessian condition. If `q|U` is semidefinite, `E q=0` forces `q(X)=0` almost surely; taking `Y=R=X` in the derivative identity yields `DF(X)[A]=0` by homogeneity. These two cases prove the claimed almost-sure closure, including the identically-zero restriction. Consequently `b` annihilates `ker H`, and for centered laws the affine-background quadratic has the stated attained pseudoinverse minimum.

### B. Full nine-coefficient low-rank classification and rank gap

The complete invariant basis is nine-dimensional, including both orientation-odd coefficients in `qu`, `qv`, `qw`; it is not a left-and-right-rotation slice. At rank-one distinguished backgrounds, the binary rank-one restriction is a convex nonnegative quartic. Its fourth root is a seminorm, and the zero direction supplied by `F(A)=0` reduces it by an invertible input change to `c s⁴`. Comparing the remaining coefficients and testing the Hessian at `e12` and `e11` removes `M,N,L` and leaves `c u²+λq²`, with `c,λ ≥ 0`.

At an invertible distinguished background, right multiplication sends it to `I` without changing left-rotation invariance or rank-one convexity. Homogeneity and infinitesimal left rotation fix the first two Hessian rows. Equating the full Hessian with `vvᵀ+λ diag(1,1,−1,−1)` forces the mixed first-derivative parameters to vanish. If `f<0`, the determinant remains indefinite on `ker P` and algebraic closure contradicts `DF(I)[I]=4f`. If `f>0`, the forced form is `f q²+g|w|⁴+|w|² Re(η z\bar w)`; closure on `ker P={i=0}`, where `q=j²−k²−l²` is indefinite, kills `η`. If `f=0`, the PSD rank-one `(k,l)` block gives `β≥0`, `|δ|=β`; a conjugation fixing `I` normalizes its phase. Convexity along the rank-one line from `(z−w,0)` to `(z,w)` proves nonnegativity, which first removes `Im η`; the two rank-one second-variation tests with `σ=±1` then force `β=h=0`, leaving `γ|w|⁴`. These are precisely members of `E`.

For the rank-gap theorem, a kernel vector `A` gives `tr(P_A C)=0`. Since both matrices are PSD, `ran C ⊂ ker P_A`; rank `C≥3` forces `rank P_A≤1`, so the classification applies. Conversely, each exceptional integrand has a nonzero `A` in `ker ell`; three independent rank-one matrices can be chosen in the hyperplane `(cof A):R=0`. Their Hessians are PSD and annihilate `A`, yielding a singular rank-three balanced moment. The source also realizes the trace-free triple by a compatible three-wave periodic gradient, so the exceptional rank gap is attained by an actual gradient, not only by an abstract probability law.

### C. Compatible Fourier geometry on a plane

When `det|L` is indefinite and `dim L=2`, its null set is two rank-one lines `R_j=a_j⊗b_j`. Indefiniteness forces the two input directions `b_1,b_2` to be independent. For each nonzero Fourier frequency `k`, compatibility writes `\hat G(k)=i\hat\phi(k)⊗k`. Its real and imaginary parts both lie in `L` and share input direction `k`; they cannot lie on the two distinct null lines simultaneously. Any nonzero mode therefore lies on one null line and its integer frequency is parallel to that line's input factor. Each occurring direction is represented by a primitive integer frequency `k_j`, giving `G=R_1g_1(k_1·x)+R_2g_2(k_2·x)`.

The two independent integer frequencies define a finite torus covering, which pushes Haar measure to product Haar measure. Integrating first in one phase and then the other applies ordinary one-dimensional Jensen along rank-one lines twice. The semidefinite and identically-zero determinant restrictions reduce to a rank-one line or a convex restriction, respectively. For nonexceptional `F`, Theorem B gives `rank C≤2` on a singular face, so the field lies almost everywhere in `ran C` and this planar-subspace lemma applies. For `F∈E`, determinant and ordinary convexity of `|ell|⁴` give Jensen directly. Zero-boundary extension is valid because `D²F(0)=0` for a homogeneous quartic.

I checked the Fourier selection algebra independently for a representative plane `span{e11,e22}` over 48 nonzero integer frequencies in a finite box; the general claim rests on the argument above, not on that finite enumeration.

### D. Fixed constant-coefficient parabolic monotonicity obstruction

For `F_eta=q²+eta|A|⁴`, the first term is convex in the null Lagrangian `det A`, while the second is strictly convex in `A`. For zero-boundary perturbations, determinant preservation and
`|A+B|⁴−|A|⁴−4|A|² A:B ≥ |B|⁴/3`
give the stated uniform Jensen lower bound. Thus the heat-flow example is not a failure of quasiconvexity.

Independent exact trigonometric moments reproduce
`E q(Dφ_t)² = (1/2)a²(c−b)²`,
`E|Dφ_t|⁴ = (5/4)a⁴+2a²b²+4a²c²+(5/4)b⁴+10b²c²+5c⁴`,
and the derivative `1/3 − 34621/(81·10000) = 235379/810000 > 0` at zero. The determinant and fourth-power averages follow from independent sine/cosine moments; no sampled grid is used.

The group argument handles arbitrary real output matrices, including skew parts: output dihedral averaging sends `M` to `(tr M/2)I`; input dihedral averaging sends the spatial coefficient tensor to `κ δ_ij I`. Strong parabolicity is preserved and implies `κ>0`. If any fixed operator in the stated class were dissipative for every periodic field, all its symmetry conjugates would be too; linearity of the energy derivative makes their average dissipative. The average is a positive multiple of ordinary heat, contradicted by the exact field above. This rules out only the specified universal fixed linear-diffusion mechanism.

## Independently checked near-singular sequences

The parent requested an audit of the following compatible potentials (using independent torus moment arithmetic):

`X0 = D(sin x cos y, −cos x sin y) = [[a,−s],[s,−a]]`, where `a=cos x cos y`, `s=sin x sin y`; `q0=det X0=−(cos 2x+cos 2y)/2`.

`Y=D(−sin 2x/4,−sin 2y/4)=diag(−cos 2x/2,−cos 2y/2)`, so `tr Y=q0`; and `Z=D(sin y,sin x)=[[0,cos y],[cos x,0]]`.

For `Xε=X0+εY`, and separately `Xε*=X0+εY+ε²Z`, both are smooth compatible periodic gradients, uniformly bounded in `L∞`, and `E det Xε=0`. At `B=−I/ε`,
`det(B+Xε)−det B = det Xε−q0`,
so the exact determinant-square relative gaps are
`ε²(ε²+2)/64` without `Z`, and `ε²(16ε⁶+9ε²+2)/64` with `Z`. Both are `O(ε²)` with leading coefficient `1/32`.

For fixed `F=q²`, `H=2(D²q) C (D²q)` because `E q(Xε)=0`, and `D²q` is invertible. The no-`Z` covariance/Hessian have rank three for every `ε≠0` (an exact nonzero 3×3 minor is `ε²(ε²+4)/256`); the `+ε²Z` path has rank four for every `ε≠0` (its covariance determinant is `ε⁶(ε²+4)(ε⁴+1)/256`). At `ε=0`, the rank is two, `b=0`, and `E q0²=1/4`, so the attained minimized gap is exactly `1/4`. Since quasiconvexity gives nonnegative gaps, the `B=−I/ε` test proves that the optimized minimum tends to zero on either path. This shows discontinuity of the minimized gap, including along a path of exact singular Hessians without `Z`; it is not a quasiconvexity counterexample. With `Z`, the positive-definite path demonstrates why a theorem restricted to singular `H` cannot be passed to by qualitative continuity.

For the varying integrands `Fε=q²+ε⁴|A|⁴` on the no-`Z` path, `Fε` is strictly quasiconvex for each `ε>0`. Its averaged Hessian at `Xε` is
`Hε=2(D²q)C(D²q)+ε⁴(8C+4 tr(C)I)`,
and `tr(C)=(ε²+4)/4>0`, so `Hε` is positive definite even though `rank C=3`. It lies outside `E`: on rank-one matrices `x=t n,y=s n`, membership in `E` would force `|αt+βs|²=ε²(t²+s²)`, so `|α|=|β|=ε` and `Re(α\barβ)=0`. Hence `α\barβ=±i ε²`, which makes the global `|αx+βy|⁴` contain the nonzero mixed term `±4ε⁴ q(u+v)`, incompatible with `q²+ε⁴(u+v)²` for any coefficient of `q²`.

At the same `B=−I/ε`, the added convex fourth-power relative gap, after multiplication by `ε⁴`, is exactly
`ε²(5ε⁶+40ε⁴+208ε²+256)/64`.
The total test gap is therefore `ε²(5ε⁶+40ε⁴+209ε²+258)/64 →0`. This is nonuniformity across varying integrands; it does not refute QC or the singular-face theorem. In all cases the background used to make the gap small escapes to infinity like `1/ε`; this distinction must accompany the quantitative claim.

## Exact checks, limitations, and status

`independent_checks.py` was written independently. It checks the source-package hashes; 35-monomial quartic reciprocity and affine expansion; null-cone algebra with a radical; cubic proportionality systems for all eight indefinite signatures that can occur in subspaces of the planar determinant form; the nine-dimensional invariant basis; the low-rank branch identities including orientation-odd coefficients; the actual exceptional compatible three-wave moment; exact heat averages and derivative; the two symmetry averages; compatible Fourier selection in a representative plane; and all near-singular path identities/ranks above. `checker.log` records 12 passing exact groups, and `independent_checks.json` retains outputs. These symbolic checks corroborate finite algebra only; the measure-theoretic and Fourier arguments remain analytic proof obligations assessed above.

The supplied note itself records the same substantive limitations. External mathematical correctness remains **UNKNOWN**; historical novelty remains **UNKNOWN**; no proof-assistant formalization was attempted. The note's search for full-cone compatible counterexamples is finite numerical evidence only. N740/N794/N797 capital context does not support treating this work as completion of the full Morrey implication.

## Owned artifacts

- `INITIAL_VERDICT.md`: pre-worker-artifact assessment.
- `REPORT.md`: this independent audit.
- `independent_checks.py`, `independent_checks.json`, `checker.log`, `source_manifest_recheck.json`: fresh exact checker, results, and package-hash replay.
- `PRIMARY_ACCESS_LEDGER.md`: primary literature and internal-source access record.
- `OWNED_PUBLICATION_MANIFEST.json`: frozen SHA-256 inventory of this audit package.
