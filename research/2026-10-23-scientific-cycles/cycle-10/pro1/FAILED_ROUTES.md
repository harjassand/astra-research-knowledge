# Failures and corrected premises that affect continuation

## Raw trace-normalized squaring is obstructed at fixed temporal scale

For \(\widehat\rho_s=\sigma(I-sH)^2/(1+s^2v)\), the exact charge cost is \(s^2c_k/(1+s^2v)\), where
\[
c_k=\frac18\sum_{j=1}^{k-2}(k-1-j)\mathbb E|S_j|
\sim\frac{\sqrt{2/\pi}}{30}k^{5/2}.
\]
At \(s=\gamma_0 b\), \(b=r_0/k\), \(\gamma_0>0\) and fixed \(0<r_0\le1/2\), it grows as a positive multiple of \(\sqrt{k}\). The new all-coherence bound makes the remaining signed drift uniformly bounded. Thus the entire bulk bath operator has positive outward drift for large \(k\).

This rejects raw squaring as the inward-drift construction at this scale. It does not prove universal bath escape, impossibility of all codes using that input, or a capacity upper bound. It does not apply to the distinct Cycle9 clipped density.

The replacement is an actual mathematical change: normalization within every complete charge pattern, not a new name for global trace normalization.

## A global factor k on the repair discards the useful structure

The generic estimate \(\|D_b(Z)\|\le k\|Z\|_1\) is valid but cannot control this fixed-\(bk\) repair budget. The new theorem isolates the exact diagonal charge response and bounds the offdiagonal contribution by \(bk\,e^{2b^2k^2}\) times a weighted input norm. The proof pairs actual coherent histories and controls all final bath overlaps.

This does not assert that every small trace-norm repair is harmless. Its charge cost and weighted offdiagonal norm must be supplied separately.

## The diagonal term cannot be included in the small coherent bound

The input \(Y=A/\sqrt{k}\) has weighted norm \(1/2\), but its bulk response is \((1-b)\sqrt{k}I/2\). An estimate that omits the separate diagonal term is false at fixed small \(bk\).

## Bulk identities fail at the physical root

For one call from vacuum, \(\sigma=\operatorname{diag}(1/2,1/4,1/4)\) has depth drift \((1-b)/2\), while its bulk drift is zero. The vacuum exchange is present. The root remainder in the inherited operator Lyapunov theorem cannot be removed.

## The normalizer need not commute with H

The actual small-block computation finds nonzero \([D,H]\), including \(k=4\). The proof therefore retains \(D^{-1/2}\) on both sides of the square. An arbitrary positive matrix in the pattern algebra also need not commute with \(F\); the density \(\sigma TF\) uses a function of total charge for \(T\).

## The old clipping question has not been answered by changing the state

The original positive-part input's full signed charge cost at fixed \(bk\) remains unresolved. The normalized Gram family proves a new quadratic rate. No result about the old clipping family is inferred from it.

## Resource report correction

The initial auxiliary comparison JSON called \(\log_{10}(3^k/t)\) an upper bound on the logarithmic-cutoff coefficient. The actual coefficient is \((d+16)/t\), \(d=\operatorname{rank}\rho\), so the valid rank upper is \((3^k+16)/t\). The final script and JSON are corrected.

At \(k=4\), the input is invertible, \(d=81\), and the actual coefficient is \(97/t\), not \(81/t\). This changes the auxiliary resource record only. The full proof always retained \(d+16\); entropy, drift, rate and comparison table values are unchanged. The earlier output is preserved under evidence/pre_correction_capacity_comparison.json and clearly marked by RESOURCE_FIELD_CORRECTION.json.

## Inherited closures stay scoped and closed

The predecessor retains the fixed-affine charge-only obstruction, the original one-site iid, balanced-only, diagonal, exact-product-stationary and reflecting-cutoff failures, and the corrected endpoint-history examples. None is reopened here. In particular, the new positive family does not inherit the pair-supported response lemma; it uses a new theorem that actually includes higher endpoint coherences.

## New unproved premise

The Gibbs variational reduction does not itself bound a logarithmic moment-generating function. A second moment, a finite prefix plot or a favorable average is not such a bound. The next operation must control this quantity uniformly or produce a counterexample with its exact scope.

