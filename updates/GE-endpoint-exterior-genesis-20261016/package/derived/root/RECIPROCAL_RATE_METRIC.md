# Reciprocal-rate stability, uniform saturation and the infinite-rate boundary

16 October 2026. Internal mathematical synthesis. The survivor-mean lemma and simultaneous normalization were independently found by ge_sampler_adversary. Root independently extended the finite local boundary form and develops the metric completion and cost consequences here. The decisive ingredients are the supplied two-sided interchange Duhamel coupling, classical reversed Chebyshev/layer-cake inequality and the exact killed-pair Green normalization. Historical priority and external correctness remain UNKNOWN.

## 1. The endpoint metric theorem

Fix a finite undirected graph with positive edge support E and connected components C. Let r and q be any strictly positive symmetric, configuration-independent rates on precisely E. For T>0 let P_r(T),P_q(T) be their full labelled interchange endpoint kernels. Put

```
c_C = binomial(|C|,2)/2 = |C|(|C|-1)/4,
d_C(r,q)=max_(e in C) |1/r_e-1/q_e|.
```

Then, uniformly over every initial permutation,

```
TV(P_r(T),P_q(T)) <= min(1, sum_C c_C² d_C(r,q)/T).       (R1)
```

The same holds for all mixtures of initial permutations and all color projections. It is a statement about the full correlated endpoint, not only one-label means. No configuration basin, permutation transition matrix, spectral gap or lower bound on other positive rates is supplied or needed. Zero-rate edges common to both models are omitted; changed positive support or adding a formerly zero-rate edge is outside this reciprocal formula, though the original pair Duhamel theorem still handles it.

## 2. Survival convolution from the full mean

For any nonnegative random X,Y with finite means, and independent copies if needed,

```
integral_0^T Pr(X>u)Pr(Y>T-u) du <= E[X] E[Y]/T.          (R2)
```

The left side is E[ell(X,Y)], where ell(a,b) is the overlap length of (0,a) and (T-b,T) inside [0,T]. Pointwise T ell(a,b)<=ab: if a,b<=T and a+b>T, this is equivalent to (T-a)(T-b)>=0; if a+b<=T the overlap is zero; if either exceeds T use ell<=the other length or T. This self-contained layer-cake proof is also the standard reversed Chebyshev integral inequality for one decreasing and one increasing function. Independence here is only an auxiliary product integration of two supplied survival functions, not an assumption that the original two endpoint dynamics or physical baths are independent.

## 3. The exact normalization that removes the edge count

On pairs wholly within C, H_r is symmetric positive definite, with row sums 2r_e at joining-edge pairs and zero at nonadjacent pairs. Its inverse is nonnegative. Let mu_r=H_r^{-1}1; this is the complete expected pair meeting time from each starting pair. Thus

```
sum_(e in C) r_e mu_r,e = c_C,                           (R3)
```

because `1^T H_r mu_r=binomial(|C|,2)` and `H_r 1=2r` on the joining-edge entries. Define x_e=r_e mu_r,e and y_e=q_e mu_q,e. Both are nonnegative and each sums to c_C.

The supplied Duhamel certificate and (R2) give

```
TV_C <= (1/T) sum_e |r_e-q_e| mu_r,e mu_q,e
      = (1/T) sum_e |1/r_e-1/q_e| x_e y_e
      <= d_C(r,q) c_C²/T.
```

There is no extra factor for the number of edges: `sum_e x_e y_e <= (sum_e x_e)(sum_e y_e)`. Independent component endpoint laws factor, and product-TV is at most the sum of component TV bounds. This proves (R1). All factors refer to unordered pairs and ordinary TV; replacing c_C by an ordered-pair constant would lose a factor but is unnecessary.

## 4. A graph-local boundary alternative

For an edge e, choose a physical vertex set D_e containing its endpoints. In each model suppress external discrepancy moves, and let mu_D,r,e be the internal pair mean. The symmetric Green maximum principle gives `mu_D,r,e<=c_D/r_e`, where `c_D=binomial(|D_e|,2)/2`; an unreachable part of D_e may simply be discarded. Let b_D,r be the sum of the two largest external weighted degrees, an upper bound on pair exit hazard.

Coupling to the stopped internal process gives `S_r,e(t)<=S_D,r,e(t)+p_r`, where `p_r<=b_D,r mu_D,r,e`. Combining (R2), the two cross terms and the constant term yields

```
integral_0^T S_r,e(u)S_q,e(T-u)du
 <= mu_D,r,e mu_D,q,e (1+b_D,r T)(1+b_D,q T)/T.
```

Consequently the finite local rate-change certificate is

```
TV <= sum_e [c_D_e²/T] |1/r_e-1/q_e|
                    (1+b_D_e,r T)(1+b_D_e,q T).           (R4)
```

This local formula does have an edge sum; it need not beat the global normalization bound. It replaces the earlier logarithmic local-envelope calculation with a full-mean calculation. Its boundary hazards are actual weighted rates, not geometric degree. Taking the minimum of independently valid global, local, direct-Green and computed-survival certificates is allowed; agreement is not a new proof premise.

## 5. Uniform caps and finite-bit sampling cost

Set `q_e=min(r_e,K_C)` in each component, with K_C>0. Then `d_C<=1/K_C`, so

```
TV <= sum_C c_C²/(T K_C).                                (R5)
```

There is no logarithm, large-K side condition, edge-count factor in the error, or dependence on the largest original rate. With one connected component, choosing `K>=c²/(T epsilon_cap)` suffices. The capped process has expected attempt count

```
T sum_e q_e <= |E| c²/epsilon_cap.
```

This is polynomial work at fixed endpoint accuracy, independent of the magnitude of original conductances after reading their finite-bit encodings. It is not a claimed wall-clock victory over component averaging or a scientific workload. The actual finite-bit Poisson clock/count generation, categorical edge choices, output of all n labels, random-bit rejection failures and their TV allocation remain additional costs. Continuous exact random reals are not assumed. Rational input r,T and rational epsilon give rational caps of polynomial encoding length; integer ceilings are a conservative option after rescaling the horizon to one.

For disconnected graphs and a fixed cap-error allocation, the upper event budget is `sum_C |E_C| c_C²/epsilon_C`. Minimizing it under `sum epsilon_C=epsilon_cap` gives `epsilon_C` proportional to `c_C sqrt(|E_C|)` and total upper budget `(sum_C c_C sqrt(|E_C|))²/epsilon_cap`. Square roots can be conservatively rationally enclosed; singleton/no-edge components cost zero. This is ordinary convex allocation, not an acquired optimal implementation theorem.

## 6. Continuous extension to infinite rates

Write theta_e=1/r_e. The finite endpoint kernel is uniformly Lipschitz in theta under (R1). Since probability measures on the finite permutation space are complete in TV, it extends uniquely and continuously to finite nonnegative reciprocal vectors, allowing theta_e=0. One may approach a boundary point along any positive finite-rate sequence; (R1) makes the endpoints Cauchy and makes the limit independent of approach ratios.

For the zero-reciprocal edge components, standard finite-dimensional fast/slow averaging identifies that limit with uniform within-component projection and the conditional boundary-event kernel. The uniform Lipschitz inequality remains valid on the boundary by taking limits. In particular, original-to-exact averaging is bounded by (R1) with zero reciprocal fast rates, without choosing W or importing a permutation mixing gap. This bound is often much looser than the direct Green/boundary certificate and need not pass a useful tolerance.

The extension is for T>0. At T=0 an infinite-rate component produces an instantaneous projection, so joint continuity at that time is neither asserted nor implied. Reciprocal infinity (a rate becoming zero) is not a finite point of this completion; deleting support requires the original finite pair theorem or another argument.

The same endpoint law induces a quantum random-swap channel. The standard convexity bound `half diamond(Phi_r-Phi_q)<=TV(p_r,p_q)` transfers (R1) uniformly over arbitrary quantum inputs and references. This does not acquire physical Markovian swap rates, eliminate Hamiltonian/noise errors, or outperform existing quantum gossip/symmetrization controls.

## 7. What this changes, and what it does not

The new source-relative consequence is a full-endpoint reciprocal-rate modulus, a simpler cap with no logarithm or edge multiplier in its error, and a quantitatively controlled infinite-rate boundary. It strengthens the existing N727 rate-saturation route using information already implicit in its reversible pair coupling. It does not invent Karlin–McGregor, averaging, SSA, Green functions or the rearrangement inequality. Historical originality of the combined modulus remains UNKNOWN.

For the supplied graded examples, the universal c² bound is substantially looser than the graph-specific direct certificate. The real 3D cycle-observable workload has no stiff rates requiring it and already admits output-scale exact simulation. No extraordinary scientific capability or technology advantage follows from this theorem alone. A better constant, a stronger norm, or an important workload would require its own decisive comparison.
