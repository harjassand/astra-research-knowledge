# Independent coercivity check: the rank-two update and γ=1/2500000

## Verdict and scope

**PASS.** The rank-two subtraction is exactly positive definite; it yields quasiconvexity of G−(3/16000)|CA|⁴, where CA=(a−d,b+c). The primary complex-valued Beurling bound supplies the elliptic estimate needed for the affine-background fourth-power gap

∫[G(B+Dφ)−G(B)] ≥ (1/2500000)∫|Dφ|⁴.

This holds for W¹,⁴₀ perturbations on bounded Lipschitz domains, periodic W¹,⁴ perturbations on every rectangle, and zero-endpoint W¹,⁴ perturbations on finite-width periodic strips. The constant is independent of the periods and strip width. It does not assert quasiconvexity of G−γ|A|⁴ or a quadratic uniform-convexity estimate.

This review reads §§1–3 of [source coercivity report](../storage_horizon/SOURCE_QC_REPORT.md), uses the original Heat18 certificate already independently replayed, and inspects the external theorem directly. It does not use the author's numerical results or execute their scripts. The new `coercivity_replay.py` reuses only the polynomial/matrix routines and base checks in this review's own `replay.py`; it deliberately stops before the original receipt writer.

## 1. Exact subtraction, checked independently

The new replay reconstructs ℓ=CᵀZ directly and verifies the five quoted entries ℓ₀,ℓ₁₂,ℓ₁₃,ℓ₁₆,ℓ₁₇. With r=a−d,

v₁=e₀−e₁₂+e₁₆,  v₂=−e₁₃+e₁₇,
v₁·ℓ=r(z₀−z₄),  v₂·ℓ=r(z₁−z₅).

Because the Hessian of r⁴ is 12r²(dr)², the weighted compatible heat Hessian of r⁴ is exactly ℓᵀKℓ, where

K=12d₁v₁v₁ᵀ+12d₂v₂v₂ᵀ.

The checker differentiates r⁴ and compares the resulting full sparse polynomial with ℓᵀKℓ. It then constructs Sε=S−K/2000, independently computes all 18 LDL pivots, verifies that every pivot is strictly positive, and reconstructs all 324 matrix entries. Full pivot values are preserved in `coercivity_receipt.json`. Finally, it compares the entire polynomial identity

ℓᵀSεℓ = heat_Hessian(G−r⁴/2000)+ω(B₁,B₂).

The same global polynomial primitive and heat-flow argument therefore prove all-background quasiconvexity of G−r⁴/2000. This step requires no new analytic estimate or boundary assumption beyond those detailed in `PROOFCHECK.md`.

As a second positivity check, the replay solves Sx=v₁ and Sx=v₂ using the original rational LDL factorization and verifies both linear systems entrywise. It obtains

T₀=15170724338155705727902393504889168329780880496992995426977161408283379160599598090460 / 7605185216636099447554368976061853224091580485177180416636254931272609515973460963.

Exact rational comparison gives 0<T₀<2000. Its decimal 1994.7869652102925 is diagnostic only. For every ξ, the S-inner-product Cauchy–Schwarz inequality gives (v·ξ)²≤(vᵀS⁻¹v)(ξᵀSξ), hence K≤T₀S and Sε≥(1−T₀/2000)S>0. This independently confirms the direct LDL result.

## 2. Rotation average and quartic gap

Left output rotations preserve u,v,j and thus G. They preserve compatible gradient perturbations and all relevant boundary classes. For the standard rotation Rθ,

(RθA)₁₁−(RθA)₂₂ = r cosθ−s sinθ,  s=b+c.

Thus each G(A)−ε(r cosθ−s sinθ)⁴ is quasiconvex. At the four angles 0,π/4,π/2,3π/4 the average subtraction is

ε/4 [r⁴+s⁴+(r+s)⁴/4+(r−s)⁴/4]
= (3ε/8)(r²+s²)².

The equality is independently checked over rational polynomial coefficients. A positive finite average preserves quasiconvexity, so κ=3ε/8=3/16000 is valid. There is no need to trust a separately generated rotated Gram certificate: the original updated certificate plus this elementary transformation suffices.

The independently checked vector identity is

|x+h|⁴−|x|⁴−4|x|²x·h−|h|⁴/3
=6(x·h+|h|²/3)²+2(|x|²|h|²−(x·h)²)≥0.

Use x=CB and h=CDφ. The integral of h vanishes in each boundary class in the verdict. Combining this identity with quasiconvexity of G−κ|CA|⁴ gives

∫[G(B+Dφ)−G(B)]≥(κ/3)∫|CDφ|⁴.

## 3. External analytic input: checked in the primary source

The primary PDF is [Bañuelos and Janakiraman, Lp-bounds for the Beurling–Ahlfors transform](https://www.math.purdue.edu/~banuelos/Papers/Beur_Ahl.pdf), printed page 2, Theorem 1.1, equation (1.4). It explicitly covers complex-valued f∈Lp(C;C), 2≤p<∞, with operator bound √(2(p²−p)). At p=4 this is √24. Its separate real-valued estimate is not used. The theorem's statement and applicability were directly inspected in the primary PDF, rather than inferred from another report. This review relies on that established theorem; it does not reprove its martingale argument.

For a compactly supported smooth φ=(φ₁,φ₂), let f=φ₁+iφ₂ and use the standard Wirtinger derivatives ∂=(∂x−i∂y)/2 and ∂bar=(∂x+i∂y)/2. Then

2∂bar f=(φ₁,x−φ₂,y)+i(φ₂,x+φ₁,y),
|Dφ|²=2(|∂f|²+|∂bar f|²).

The ratio of the two Fourier derivative symbols is (ξx−iξy)/(ξx+iξy), the Beurling multiplier. Consequently ∂f=B(∂bar f). At the zero frequency both derivatives vanish, so no zero-frequency choice affects the identity. Minkowski in L² applied to the squared moduli gives

||Dφ||₄²≤2(||∂f||₄²+||∂bar f||₄²)
≤2(24+1)||∂bar f||₄²
=(25/2)||CDφ||₄².

Squaring gives ∫|Dφ|⁴≤(625/4)∫|CDφ|⁴. Density extends the compactly supported estimate to W¹,⁴ functions on R² having compact support. Zero extension therefore establishes it for W¹,⁴₀ on any bounded Lipschitz domain, with exactly the same constant.

## 4. Periodic and strip transfer, including cutoff errors

### Fully periodic rectangles

Let φ∈W¹,⁴ on a rectangular torus and extend it periodically to R². Fix a nonzero smooth compactly supported scalar cutoff χ on R² and form φ_L(x)=χ(x/L)φ(x). Its gradient is χ(x/L)Dφ+L⁻¹φ⊗Dχ(x/L). Divide fourth-power integrals on R² by L². Periodic averaging gives

L⁻²∫|χ(x/L)Dφ|⁴ → (∫R²|χ|⁴) average_cell |Dφ|⁴,

and the same formula holds with C applied to the gradient. The normalized fourth-power integral of the error is O(L⁻⁴), because the periodic |φ|⁴ has bounded average over the O(L²) cutoff support. For this fixed torus the implicit bound is finite; it need not be uniform in the periods because the error tends to zero before the conclusion is drawn. Applying the whole-plane estimate to φ_L, using the triangle inequality in the normalized L⁴ norms to remove the error, and taking L→∞ gives the periodic estimate. The positive factor ∫|χ|⁴ cancels. This derives exactly the same 625/4 constant without an aspect-ratio-dependent Poincaré inequality. A nonzero mean of φ only contributes to the disappearing error term.

### Finite-width zero-endpoint strips

For φ∈W¹,⁴((0,T)×Ty) with both x-end traces zero, extend by zero in x and periodically in y. The zero traces ensure that the extension remains W¹,⁴ locally and produces no distributional boundary jump. Let η∈Cc∞(R) be nonzero and set φ_L(x,y)=η(y/L)φ(x,y). Its gradient error is L⁻¹η′(y/L)φ⊗e_y. Divide fourth-power integrals by L. The error tends to zero with O(L⁻⁴) normalized fourth power. Weighted periodic averaging in y sends the main integrals to (∫|η|⁴) times their one-period y averages, integrated over x. Apply the whole-plane estimate and cancel that factor. For each finite T the needed integrals of |φ|⁴ and |Dφ|⁴ are finite; no T-dependent constant survives. Normalizing y measure changes both sides by the same factor.

The quasiconvex ingredient on such a strip follows by identifying its two zero end traces, giving a W¹,⁴ periodic perturbation on the T-by-period rectangle. Equality of derivative traces is unnecessary for this Sobolev gluing: equality of displacement traces prevents a jump in the weak first derivative. Smooth periodic approximation followed by the quartic continuity estimate supplies the quasiconvex inequality. The integral of Dφ is zero by the zero x-end traces and periodic y traces. Moving transverse means inside the strip do not change any of these facts.

These transfers are analytic proofs, not deductions from the boundedness theorem alone, and they apply to the actual compatible gradient. They do not claim analogous estimates for an arbitrary unconstrained matrix field.

## 5. Constant and reproducibility

Combining the two inequalities yields

γ=(κ/3)(4/625)=(3/16000)(4/1875)=1/2500000.

The checker independently verifies each rational constant, including κ, 625/4, and γ. Run `python coercivity_replay.py` from any directory; it reads the preserved certificate, uses only this review's code and Python's standard library, and writes `coercivity_receipt.json`. No author script, package install, remote execution, or source-worktree write is involved.

The remaining dependencies are standard Sobolev density/gluing, heat smoothing, periodic averaging, and the stated primary-source Beurling theorem. They have been matched to the required hypotheses above. This closes the requested γ-coercivity dependency; it does not independently validate every later storage or topology claim in the source report.


Integration evidence status: `source_derived_unreviewed`. Audit verdicts and primary-source reading statements above are attributed to the supplied research, not new external review. This intake replays only its three own exact verification scripts. The conclusion applies to the particular certified Heat18 quartic G, not the full quartic cone, PR97’s newly exposed ROC ray, or general Morrey questions.
