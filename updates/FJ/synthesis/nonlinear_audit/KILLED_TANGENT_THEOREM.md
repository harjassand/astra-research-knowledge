# Exact killed-tangent sampler

This is an independently derived extension of the supplied constant-rate theorem. It kills the diffusion at the positive tangent rate itself. It is an ideal-arithmetic theorem; its computational value depends on the cost of sampling that killed path.

## Statement

Let X be a conservative Markov process with generator L, and let V be finite-valued and measurable with V(x) ≥ λ > 0. Assume the path integral of V(X_t) is finite on bounded time intervals. For independent E distributed Exp(1), define

    ξ = inf{t ≥ 0 : integral from 0 to t of V(X_s) ds ≥ E},    Y = X_ξ.

Then ξ is finite almost surely and, for bounded measurable f,

    G_V f(x) = E_x[f(Y)/V(Y)]
             = E_x[integral from 0 to infinity exp(-integral_0^t V(X_s)ds) f(X_t) dt]
             = (-L+V)^(-1) f(x),

with sup-norm bound ||G_V f||∞ ≤ ||f||∞/λ.

Consider -L u + F(x,u) = s, with an evaluable predictor v, residual r = s + Lv - F(x,v), and tangent V = ∂_u F(x,v). On |e| ≤ h suppose

    F(x,v+e)-F(x,v)-V(x)e = sum_{m≥2} c_m(x)e^m.

Assume uniform absolute convergence on the tube, |r| ≤ R, |c_m| ≤ B_m, and define P(h)=sum B_m h^m and Γ(h)=sum m B_m h^(m-1). If

    R + P(h) ≤ λh,       Γ(h) < λ,

then there is a unique fixed point e in ||e||∞ ≤ h of

    e = G_V[r - sum_{m≥2} c_m e^m],

and u=v+e solves the original equation in the corresponding mild sense.

At a node, sample Y=X_ξ, then choose (with zero-probability events omitted):

| Event | Probability | Normalized return |
|---|---:|---|
| Source | abs(r(Y))/(hV(Y)) | sign(r(Y)) |
| m children, m≥2 | abs(c_m(Y)) h^(m-1)/V(Y) | -sign(c_m(Y)) times the product of child Z values |
| Zero | Remaining probability | 0 |

All child trees are independent conditional on Y. The expansion is assumed uniformly absolutely convergent on the tube and `Γ(h)<∞`; this gives the Lipschitz majorant used below. Zero coefficients are skipped; a zero child factor can short-circuit the product.

For the generated variable Z_x,

    |Z_x| ≤ 1 almost surely,     E[h Z_x] = e(x),
    E[N_x] ≤ λ/(λ-Γ(h)).

The tree terminates almost surely. For M independent samples the same Hoeffding bound as in the supplied theorem follows:

    P(|v(x) + (h/M) sum_j Z_x^(j) - u(x)| > ε)
       ≤ 2 exp(-M ε²/(2h²)).

## Proof

The Feynman–Kac identity above gives G_V=(-L+V)^(-1), a positive operator with sup-norm at most 1/λ. The map

    Φ(e) = G_V[r - sum_{m≥2} c_m e^m]

satisfies ||Φ(e)||∞ ≤ (R+P(h))/λ ≤ h. For two functions in the tube,

    ||Φ(e)-Φ(ẽ)||∞ ≤ [Γ(h)/λ] ||e-ẽ||∞ < ||e-ẽ||∞,

so Banach's theorem gives the unique fixed point.

At the killed endpoint, the event probabilities sum to at most

    (|r(Y)| + sum_{m≥2}|c_m(Y)|h^m)/(hV(Y))
       ≤ (R+P(h))/(hλ) ≤ 1.

The conditional expected number of children is bounded by

    sum_{m≥2} m|c_m(Y)|h^(m-1)/V(Y) ≤ Γ(h)/λ = q < 1.

If G_n is the number of nodes in generation n, then E[G_n] ≤ q^n, including spatially dependent branching. Therefore E[N] ≤ sum_{n≥0}q^n=1/(1-q), and the total tree is finite almost surely. Every leaf or branch factor has magnitude at most one, so |Z|≤1.

Conditioning on Y and the first event gives

    E[hZ_x | Y] = r(Y)/V(Y) - sum_{m≥2} c_m(Y)e(Y)^m/V(Y).

Taking expectation over the killed endpoint recovers the fixed-point equation. Bounded outputs then give the stated concentration inequality.

If C_kill bounds the expected cost of generating one exact killed-path endpoint, including coefficient evaluation and degree selection, expected arithmetic work is

    C_build + C_verify
      + O(C_kill · λ/(λ-Γ(h)) · h²/ε² · log(2/δ)).

This separates tree-size bounds from path-simulation cost. If killing is implemented by thinning at a constant envelope Λ, expected candidate path steps can scale as Λ/λ, so this proposition does not by itself establish an end-to-end speedup over uniformization.

## Sinh specialization and countable branching

For F(u)=κ² sinh(u), V=κ² cosh(v), and

    (1/V) sum_{m≥2}|c_m|h^m
       = |tanh(v)|(cosh(h)-1) + sinh(h)-h,

    (1/V) sum_{m≥2}m|c_m|h^(m-1)
       = |tanh(v)|sinh(h) + cosh(h)-1 ≤ exp(h)-1.

Thus, if |r|/V ≤ δ, 0<h<log(2), and δ ≤ 2h+1-exp(h), event probabilities are valid and

    E[N] ≤ 1/(2-exp(h)).

This removes the Λ/λ factor from the number of tree nodes in the supplied sinh corollary. It does not remove any dependence that may enter C_kill.

The infinite degree is sampleable in the ideal exact-real model. Put A=|tanh(v(Y))|. Conditional on selecting a nonlinear branch, the degree law has weights proportional to A h^(m-1)/m! for even m≥2, and h^(m-1)/m! for odd m≥3. Its total mass is

    S = [A(cosh(h)-1) + sinh(h)-h]/h,

available in closed form. Draw one uniform variate, compare it first with the source mass and then with the known total nonlinear mass. If it falls in the nonlinear interval, accumulate the factorial series in increasing m until the uniform variate is crossed. The crossing occurs at a finite degree almost surely. The conditional mean degree is a mixture of

    μ_even = h sinh(h)/(cosh(h)-1) = h coth(h/2),
    μ_odd  = h(cosh(h)-1)/(sinh(h)-h).

Both are below 4 for 0<h<log(2)<1. The even bound follows from tanh(h/2) ≥ h/4. For the odd bound, the positive series difference is

    4(sinh(h)-h) - h(cosh(h)-1)
      = h³/6 - sum_{k≥2}(2k-3)h^(2k+1)/(2k+1)! > 0,

because for h<1 the series tail is at most (7/780)h³ < h³/6: the first tail coefficient is 1/5!=1/120 and the ratio of consecutive coefficients is at most 1/14, so their sum is at most (1/120)/(1−1/14)=7/780. Thus this inverse-series degree selector examines fewer than four degree terms on average conditional on a nonlinear branch. Exact finite-bit sampling of this categorical law and a rigorously bounded implementation cost remain unprovided.

## Independent exact finite-state check

exact_cases.py uses a two-state rational CTMC with generator

    Q = [[-1/10, 1/10], [1/5, -1/5]],
    V = (2,3),    e = (1/20,1/25),    h = 1/10,

and F_i(t)=V_i t+t². It sets r=(-Q+diag(V))e+e²=(207/2000,299/2500), so the exact solution is known. The global certificates are R+P(h)=81/625 ≤ 1/5=λh and Γ(h)=1/5<2=λ.

The exact killed endpoint kernel is

    (-Q+diag(V))^(-1) diag(V) = [[64/67,3/67],[4/67,63/67]].

Direct rational evaluation of the sampler recursion returns e/h=(1/2,2/5). Its expected-node certificate is 10/9. Constant-rate uniformization on the same exact case has kernel 3(3I-Q)^(-1) and node bound 5/3. This is a finite-state algebra check, not a benchmark of killed-diffusion simulation cost.
