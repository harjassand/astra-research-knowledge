# A legal five-query positive correction with an implemented-law bound

This is an actual value-only finite sampler and a full-law theorem at its stated bound. Its dimension dependence does **not** meet the universal polylogarithmic Gaussian-mean target.

Normalize the ordinary additive Gaussian scale to one. Let g=grad F be globally λ-Lipschitz, F C1,1, with μ=E g(G). Fix 0<a<1, b=sqrt(1-a²), and a reserve η>0. Define only for analysis

```
h_b(y)=E g(by+aH),
K_b(y)=∫_0^b E Dg(ρy+sqrt(1-ρ²)H)dρ,
Γ_b(y)=sym[K_b(y)(Dh_b(y))^T].
```

Both K_b,Dh_b are symmetric contractions bounded by bλ. The frozen source's legal two-value factories give conditionally unbiased bounded actions for each of them. A fresh independent composition in either order, selected by a fair coin, gives a **four-value** action W_Γ(c;v) with

```
E[W_Γ(c;v)|c,v]=Γ_b(c)v,
||W_Γ(c;v)||<=b²λ²||v||.
```

No realized common Γ matrix is required.

## Finite program

Draw independent standard Gaussian vectors G,H,Z,W,V. Draw T with density 2t on [0,1] (T=sqrt(U), U uniform generated from scalar Gaussians). Let

```
C=T G+sqrt(1-T²)W,
Ucorr = -(1/2) W_Γ(C;Z),
OUTPUT = g(bG+aH) + Z + Ucorr + ηV.
```

This uses **at most five original whole-vector g-value queries on every execution**, O(d) real arithmetic/storage outside those calls, a constant number of Gaussian slots, and no potential, derivatives, mean, basis, conditional-mean or stopping oracle. All action calls use fresh internal seeds. Null radius events receive fixed values. The program is a positive ordinary pushforward and has mean exactly μ.

## Governing implemented-law theorem

Put Cη=(sqrt(2)/2)log(1+η^(-2)). Then

```
TV(Law(OUTPUT), N(μ,(1+η²)I))
 <= min{1,
     Cη [b³λ³ sqrt(d)/sqrt(2) + b⁴λ⁴ d/2]
       + sqrt(2)b⁴λ⁴ d/(8η²)
       + aλ sqrt(d)/(2η)}.                          (1)
```

The target variance includes the reserve. For a physical target variance σ², run the normalized program on g/τ and multiply its output by τ, with τ=σ/sqrt(1+η²). Then λ=L/τ. The fixed-ratio, unbounded-dimension target is not solved by (1).

### Step 1: the deterministic conditional-mean correction

Let N_G be the Gaussian number operator and define the analysis field

```
F=(N_G+2)^(-1)Γ_b = ∫_0^1 t P_t Γ_b dt,
u(G,Z)=-F(G)Z.
```

Because C has the OU conditional law given G and T has density 2t,

```
E[Ucorr|G,Z] = u(G,Z).                              (2)
```

For a source-only residual Γ_b, u is exactly the source-adjoint Hodge correction in JOINT_GAUGE_THEOREM.md (noise degree zero). Its full kernel J=(J_G,J_Z) satisfies δJ=u and

```
J_G=-D_Gu,
||D_Gu||_2 <= ||Γ_b||_2/(2sqrt(2)),
||Du||_2 <= ||Γ_b||_2/2,
||J||_2 <= ||Γ_b||_2.
```

For X=h_b(G)+Z the initial residual is Γ_b. Therefore X+u has the exact symmetric Stein residual

```
Elinear + Equadratic,
Elinear = sym[(K_b-Dh_b)(D_Gu)^T],
Equadratic = sym[J(Du)^T].
```

Since ||Γ_b||_2<=b²λ² sqrt(d),

```
E||Elinear||F <= b³λ³ sqrt(d)/sqrt(2),
E||Equadratic||F <= b⁴λ⁴ d/2.
```

The reserve-TV theorem then bounds the deterministic comparison law by the first term of (1). This step uses full-law Stein testing, not covariance matching.

The sharper source-only constants follow directly on source chaos n:
u_n=-Γ_n Z/(n+2), JG_n=(DGΓ_n)Z/(n+2), JZ_n=-(n+1)Γ_n/(n+2). Thus the squared derivative ratios are n/(n+2)^2<=1/8 and (n+1)/(n+2)^2<=1/4, while the squared combined kernel ratio is [n+(n+1)^2]/(n+2)^2<=1. These estimates sum by orthogonality. The helper independently derived them.

### Step 2: charge the actual randomized correction

The action bound gives

```
E||Ucorr-u||² <= E||Ucorr||² <= b⁴λ⁴d/4.            (3)
```

For any indicator A, let fη(x)=P(x+ηV in A). Its Hessian Frobenius norm is at most sqrt(2)/η² by Gaussian Hermite Bessel. Taylor-expand at X+u, condition on G,Z, and use (2). The linear term cancels exactly, so

```
|E fη(X+Ucorr)-E fη(X+u)|
 <= sqrt(2) E||Ucorr-u||²/(2η²)
 <= sqrt(2)b⁴λ⁴d/(8η²).                            (4)
```

This accounts for the law of the implemented random action, including the extra covariance and higher conditional cumulants. No unbiased coefficient is substituted inside a nonlinear output law.

### Step 3: acquire h_b without a mean oracle

The displayed program uses g(bG+aH), not h_b(G). Conditional Gaussian Poincare gives

```
E||g(bG+aH)-h_b(G)||² <= a²λ²d.
```

Couple all other seeds identically and use Gaussian reserve convolution to bound TV by aλ sqrt(d)/(2η). This proves the last term of (1) and closes the finite program.

## Exact covariance receipt, separate from full-law proof

The source error Esource=g(bG+aH)-h_b(G) is conditionally centered and independent of action seeds given G. Equation (2) is odd in Z, so its cross-covariance with the source vanishes. Also

```
E[Z Ucorr^T] = -(1/2)E Γ_b,
Cov(h_b)=E Γ_b.
```

Hence

```
Cov(OUTPUT)=(1+η²)I + E Cov(g(bG+aH)|G) + E Ucorr Ucorr^T.
```

The frozen fixed-center Gaussian convex-order word theorem applies because C is independent of fresh Z and action seeds. Thus

```
0 <= Cov(OUTPUT)-(1+η²)I
   <= [a²λ² + b⁴λ⁴/4] I.                          (5)
```

This is a fourth-order covariance repair with a charged source-acquisition term. Equation (1), not (5), is the full-law guarantee.

For an affine conservative field g(x)=c+B x, the entire implemented law is exactly Gaussian with covariance `(1+η²)I+a²B²+(b⁴/4)B⁴`: the two action factories become deterministic and Ucorr=-(b²/2)B²Z. This is a full-law sanity check, not an advantage fixture. A supplied affine class already permits exact target sampling from the single value g(0); ordinary two-query antithetic averaging also removes its affine source noise.

## Decision and comparators

The sampler is a concrete positive nonlinear correction using legal values; unlike an unacquired square root or formal cubic expression, (1) bounds its implemented law. It is not a quadratic Newton iteration. The leading bound is b³λ³ sqrt(d), and random correction variance contributes λ⁴d. For fixed λ and arbitrarily large d it becomes vacuous. The same-information five-query independent-average baseline has TV controlled by the frozen chi-square formula with covariance proxy λ²I/5 and target noise 1+η². The new method improves powers of small λ in some regimes, but no uniform practical or asymptotic query advantage is claimed. Fixed-positive-exponent compilers and bounded-input FORS remain stronger ordinary competitors under their actual contracts. The next required construction must iterate the correction while controlling full law and dimension, and must acquire the coupled inverse factors rather than merely their first moments.
