# Scalar first-step chain: L4 control without higher source smoothness

This is a further analytical construction, not a sampler implementation. It strengthens the L1-only one-step estimate in one dimension and in a supplied separable coordinate system. It does not replace the universal high-dimensional target.

Let h:R->R be globally λ-Lipschitz, K its canonical Gaussian Stein resolvent, and X=h(G)+Z with independent scalar standard G,Z. Let

```
a(G)=K(G)-h'(G),   A=||a||∞<=2λ,
r_0(G)=K(G)h'(G),  ||r_0||∞<=λ².
```

Use normalized scalar Hermites e_q(Z). The full-source-adjoint inverse from JOINT_GAUGE_THEOREM.md has a particularly explicit Neumann chain. Define

```
f_q = (N_G+q+2)^(-1) r_q,
r_(q+1) = -sqrt(q+1) a D_G f_q,
u = -Σ_(q>=0) sqrt(q+1) f_q(G) e_(q+1)(Z),
J_G = -D_Gu,
J_Z = Σ_(q>=0) [-r_q+(q+1)f_q](G) e_q(Z).
```

At every q, the corresponding baseline residual is -r_q e_q and its remaining source term is r_(q+1)e_(q+1). Thus the infinite sum solves the complete initial linearized equation, and truncation at q=Q leaves exactly r_(Q+1)e_(Q+1) as linear residual. Conditional mean zero is explicit.

## Uniform coefficient estimate

The scalar OU representation is

```
(N_G+q+2)^(-1)r = ∫_0^1 t^(q+1) P_t r dt,
P_t r(x)=E r(tx+sqrt(1-t²)G).
```

Gaussian integration by parts gives

```
||D_G(N_G+q+2)^(-1)r||∞
 <= sqrt(2/pi) ∫_0^1 t^(q+2)/sqrt(1-t²) dt ||r||∞
 <= ||r||∞/sqrt(q+2).
```

For the last step substitute t=cos θ and use cos θ<=exp(-θ²/2), which follows by integrating tan θ>=θ. Hence

```
||r_q||∞ <= A^q λ².
```

No modulus of h' or higher derivative is assumed. In each noise-chaos coefficient,

```
||D_G u_q||∞ <= ||r_q||∞,
||D_Z u_q||∞ <= ||r_q||∞,
||J_Z,q||∞ <= 2||r_q||∞.
```

Here the second and third fields have noise degree q, while the first has degree q+1.

## Elementary L4 summability

The Hermite product formula gives

```
E e_q(Z)^4 = Σ_(j=0)^q binom(q,j)^2 binom(2j,j)
             <= [Σ_(j=0)^q binom(q,j)2^j]^2 = 9^q.
```

Thus ||e_q||_4<=3^(q/2). If A sqrt(3)<1, in particular if λ<1/(2sqrt(3)), the chain converges in joint Gaussian W1,4 and

```
||D_Gu||_4 <= sqrt(3)λ²/[1-A sqrt(3)],
||D_Zu||_4 <= λ²/[1-A sqrt(3)],
||J_Z||_4 <= 2λ²/[1-A sqrt(3)].
```

The exact positive update Y=X+u therefore has a valid **L2** symmetric Stein residual

```
Q = -(D_Gu)^2 + J_Z D_Zu,
||Q||_2 <= 5λ^4/[1-A sqrt(3)]²
         <= 5λ^4/[1-2sqrt(3)λ]².
```

This preserves the unknown mean and gives fourth-order residual size from a second-order initial residual. It is an exact positive one-step analytical correction, with full-law TV available after a charged Gaussian reserve. A q=Q truncation additionally has linear-residual L2 norm at most λ² A^(Q+1), or L4 norm at most λ²[A sqrt(3)]^(Q+1).

For a **supplied separable basis** with h_i depending only on G_i and independent source/noise pairs, the diagonal Stein residual satisfies

```
||Q||_(L2,F) <= 5 sqrt(d) λ^4/[1-2sqrt(3)λ]².
```

This extension assumes the coordinate structure; no hidden basis is learned or supplied for the universal problem.

## Exact remaining gate

The functions r_q,f_q are nonlocal analysis fields involving K,h' and OU expectations. Evaluating them from g values is not provided. After this positive correction the source/noise coefficients are no longer uniformly bounded; the preceding initial-coefficient inverse theorem cannot simply be invoked again. The L4 result is a valid first-step refinement, not a completed iterated Newton contraction or a polylogarithmic sampler. The Gaussian-cloud and bounded-input FORS comparators retain their respective actual contracts.
