# Joint-source Stein gauge: a bounded inverse without source derivative loss

This is an analytical theorem about Gaussian Sobolev fields. It is not a value-query sampler. The frozen universal Gaussian-mean target remains open.

Let G,Z be independent standard Gaussians in R^d. Write D_G,D_Z for row Jacobians, δ_G,δ_Z for rowwise Gaussian divergences, and N_G=δ_G D_G, N_Z=δ_Z D_Z. Matrix norms inside L2 are Frobenius; coefficient bounds below use operator norm. For a symmetric matrix residual R(G,Z), we construct a centered vector u and a **two-block** kernel (J_G,J_Z) such that

```
δ_G J_G + δ_Z J_Z = u,
sym[J_Z + (D_Z u)^T] = -R,
J_G = -D_G u,
E_Z u(G,Z) = 0.
```

The source block is essential. Requiring δ_Z J_Z=u instead gives an exponentially ill-conditioned inverse even for a small affine source, as independently derived in the helper record.

## 1. Explicit construction on a source/noise bichaos

First suppose every entry of R has source Hermite degree n and noise Hermite degree m. Put N=n+m and

```
s   = δ_Z δ_Z R,
φ   = -s / [(m+2)(N+2)],
u   = D_Z φ,
w   = δ_Z R - D_Z s/(m+2),
B   = [D_Z w - (D_Z w)^T]/(m+2),
J_Z = -R - (D_Z u)^T + B,
J_G = -D_G u.
```

Here s is scalar. All operations act on explicit Gaussian functions and use no unknown mean. Sum the construction over bichaos components.

Since δ_Z u=-s/(N+2) and N_G u=n u,

```
δ_Z w = s - N_Z s/(m+2) = 0,
δ_Z B = w,
δ_Z (D_Zu)^T = D_Z δ_Zu-u.
```

Consequently

```
δ_Z J_Z
 = -δ_ZR + D_Z s/(N+2) + u + w
 = (n+1)u,
δ_G J_G = -n u.
```

This proves the divergence identity. B is skew, so the symmetric identity is pointwise. The Z degree of u is m+1, which proves conditional centering. The construction supplies the source-divergence block that pairs with the source derivative.

## 2. Dimension- and degree-independent bounds

Gaussian creation/annihilation and Bessel give

```
||s||_2 <= sqrt[(m+1)(m+2)] ||R||_2,
||u||_2 <= sqrt(m+1)/(N+2) ||R||_2 <= ||R||_2/2,
||D_Gu||_2 <= sqrt[n(m+1)]/(N+2) ||R||_2 <= ||R||_2/2,
||D_Zu||_2 <= (m+1)/(N+2) ||R||_2 <= ||R||_2,
||D_(G,Z)u||_2 <= ||R||_2.
```

w is the orthogonal Z-divergence-free projection of δ_ZR. Thus ||w||_2^2 <= (m+1)||R||_2^2, and the Gaussian divergence identity from frozen S3 section 18 gives ||B||_2 <= sqrt(2)||R||_2. With c=2+sqrt(2),

```
||J_Z||_2 <= c ||R||_2,     ||J_G||_2 <= ||R||_2/2.
```

Different bichaos components remain orthogonal in every displayed output slot. All bounds extend to arbitrary symmetric L2 fields by closure. The divergence identity holds weakly. In particular u lies in joint Gaussian W1,2 and is conditionally centered. Although the two divergences separately need not be L2 after summing all degrees, their combined divergence equals u in L2. No claim about the individual divergence domains is needed.

The helper independently derived the sharper combined estimate ||(J_G,J_Z)||_2 <= sqrt(3)||R||_2. Writing D2=||δ_ZR||_2^2 and S2=||s||_2^2, the exact identity is

```
||J||_2^2 = ||R||_2^2 + 2D2/(m+2)
 - [2/(m+2)^2 + (N+3)/((m+2)(N+2)^2)]S2
 <= 3||R||_2^2.
```

This follows by orthogonality of the symmetric R+D_Zu and skew B, Gaussian adjointness, and the divergence-free projection identity. The helper's independent exact-rational code checks this formula, while the proof supplies the all-dimension conclusion. In particular ||J_Z||_2<=sqrt(3)||R||_2, which improves c below to sqrt(3).

## 3. Full linearized inverse near an additive-noise source

Suppose

```
X = h(G)+ψ(G,Z),       E_Z ψ=0,
δ_G K = h-μ,          δ_Z A = ψ,
H = D_G X,            C = D_Z X,
M = (K,A),            D X = (H,C).
```

The Stein matrix is T_X=M(DX)^T. A perturbation with full kernel (J_G,J_Z) has linearized symmetric residual

```
L_X(u,J) = sym[K(D_Gu)^T + A(D_Zu)^T + J_G H^T + J_Z C^T].
```

The constructed baseline inverse satisfies the **exact** identity

```
L_X(u,J) = -R
 + sym[(K-H)(D_Gu)^T + (A-I)(D_Zu)^T + J_Z(C-I)^T].
```

This uses sym[K V^T - V H^T]=sym[(K-H)V^T], valid for arbitrary K,H,V. No symmetry of H is required. Define

```
θ = (1/2)||K-H||_(L∞,op)
      + ||A-I||_(L∞,op) + sqrt(3) ||C-I||_(L∞,op).
```

If θ<1, the residual perturbation operator E has L2 norm at most θ. Apply the baseline construction to (I-E)^(-1)R=Σ_(k>=0) E^k R. This yields an exact solution L_X(u,J)=-R with

```
||D_Gu||_2 <= ||R||_2/[2(1-θ)],
||D_Zu||_2, ||D_(G,Z)u||_2 <= ||R||_2/(1-θ),
||J_Z||_2, ||J||_2 <= sqrt(3)||R||_2/(1-θ).
```

Conditional centering and J_G=-D_Gu survive the sum. Truncation after q terms leaves linear residual at most θ^(q+1)||R||_2.

In particular take **raw** globally λ-Lipschitz conservative h, λ<1, and its full canonical Stein resolvent K. Then X=h(G)+Z, A=C=I, H=Dh almost everywhere, and ||K||op,||Dh||op<=λ. Hence θ<=λ. The initial full linearization has a bounded L2 right inverse for every such h, without higher source derivatives or heat analyticity assumptions.

## 4. Exact positive update and the norm boundary

Set Y=X+u and M_Y=M+J. Then E Y=μ and δ M_Y=Y-μ. Gaussian integration by parts gives the exact preconditioned Stein matrix

```
T_Y = (M+J)[D(X+u)]^T.
```

If the full linearized equation is solved, its symmetric residual is exactly

```
sym T_Y-I = sym[J(Du)^T]
            = -(D_Gu)(D_Gu)^T + sym[J_Z(D_Zu)^T].
```

The update is a positive pushforward and preserves the unknown mean. With L2 hypotheses alone the product is controlled in **L1**, not L2:

```
E ||sym T_Y-I||F <= sqrt(3) ||R||_2^2/(1-θ)^2.
```

This is an exact quadratic one-step residual estimate. It does not justify repeated Newton steps in the same L2 space: the updated coefficients need not have the uniform bounds required in section 3, and a product of L2 fields need not lie in L2. Lp/Orlicz control, truncation, or a different invariant function space remains necessary.

For the raw initial source R=sym[K(Dh)^T], ||R||_2<=λ^2 sqrt(d). The one-step estimate is at most sqrt(3)d λ^4/(1-λ)^2. This is not dimension-free in the target regime and supplies no query advantage. The scalar refinement in SCALAR_CHAIN.md improves product integrability under its narrower contract.

## 5. Full-law interpretation with a charged reserve

Let Y have the preceding weak Stein identity with symmetric residual Q and finite E||Q||F. For independent standard Gaussian V and η>0,

```
TV(Law(Y+ηV), N(μ,(1+η^2)I))
 <= (sqrt(2)/2) log(1+η^(-2)) E||Q||F.
```

To prove this, smooth an indicator by Gaussian variance η² and solve the standard variance-one OU Stein equation. At OU time t its Hessian is Gaussian convolution at variance 1-e^(-2t)+η², multiplied by e^(-2t). Hermite Bessel bounds its Frobenius norm by sqrt(2)e^(-2t)/(1-e^(-2t)+η²), uniformly in dimension. Integrating gives the constant above. Gaussian Sobolev approximation justifies the identity. This is a full-law analytical bound; the η² reserve increases the target variance and must be allocated from σ².

## 6. Acquisition boundary

The theorem uses h, K, Dh and Hermite/OU operators as analysis fields. It gives no finite algorithm evaluating their common-source products from legal g values. Full Neumann factors are coupled coefficient fields, and J_G cannot be discarded. Frozen two-value action factories do not give a realized common K or its nonlinear field derivatives. Neither the theorem nor finite diagnostics acquire the correction, prove a reusable Lp iteration, or produce a subcritical forest/every-execution query cap. No mean or derivative oracle is runtime data. The universal polylogarithmic sampler remains unresolved.
